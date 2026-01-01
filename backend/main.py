from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import uuid
from datetime import datetime
from database.connection import get_db, engine, Base
from database.models import DesignSystem
from rendering.universal_renderer import UniversalRenderer

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agentic Design System API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_org_id(request: Request) -> str:
    # TODO: Implement actual auth extraction
    return "test-org-1"

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "backend"}

@app.get("/")
async def root():
    return {"message": "Agentic Design System API is running"}

# ============================================================================
# DESIGN SYSTEM MANAGEMENT
# ============================================================================

@app.post("/api/design-system/ingest")
async def ingest_design_system(design_system: dict, request: Request, db: Session = Depends(get_db)):
    """
    Receive design system from Figma plugin
    Store in database with versioning
    """
    try:
        version = f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store in database
        db_system = DesignSystem(
            id=str(uuid.uuid4()),
            name=design_system.get('name', 'Untitled'),
            version=version,
            tokens=design_system['tokens'],
            components=design_system['components'],
            organization_id=get_org_id(request),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(db_system)
        db.commit()
        db.refresh(db_system)
        
        return {
            "status": "success",
            "message": f"Design system ingested as {version}",
            "design_system_id": db_system.id,
            "version": version
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/design-system/latest")
async def get_latest_design_system(request: Request, db: Session = Depends(get_db)):
    """Retrieve latest design system version"""
    try:
        org_id = get_org_id(request)
        latest = db.query(DesignSystem)\
            .filter(DesignSystem.organization_id == org_id)\
            .order_by(DesignSystem.updated_at.desc())\
            .first()
        
        if not latest:
            raise HTTPException(status_code=404, detail="No design system found")
        
        return {
            "id": latest.id,
            "version": latest.version,
            "tokens": latest.tokens,
            "components": latest.components,
            "created_at": latest.created_at,
            "updated_at": latest.updated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/design-system/versions")
async def get_design_system_versions(request: Request, db: Session = Depends(get_db)):
    """Get all versions of design system"""
    try:
        org_id = get_org_id(request)
        versions = db.query(DesignSystem)\
            .filter(DesignSystem.organization_id == org_id)\
            .order_by(DesignSystem.created_at.desc())\
            .all()
        
        return {
            "status": "success",
            "versions": [
                {
                    "id": v.id,
                    "version": v.version,
                    "created_at": v.created_at,
                    "updated_at": v.updated_at
                }
                for v in versions
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================================
# SANDBOX GENERATION
# ============================================================================

from agents.sandbox_agent import SandboxAgent
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/api/sandbox/generate")
async def generate_screen(request: GenerateRequest, http_req: Request, db: Session = Depends(get_db)):
    """Generate screen from prompt"""
    try:
        org_id = get_org_id(http_req)
        
        # Get latest design system
        latest_ds = db.query(DesignSystem)\
            .filter(DesignSystem.organization_id == org_id)\
            .order_by(DesignSystem.updated_at.desc())\
            .first()
            
        if not latest_ds:
             # Fallback to a mock empty system if none exists to avoid crash
             design_system_dict = {"tokens": {}, "components": []}
        else:
             # Convert SQLAlchemy model to dict
             design_system_dict = {
                 "tokens": latest_ds.tokens,
                 "components": latest_ds.components
             }
             print(f"DEBUG: Loaded Design System Version: {latest_ds.version}")
             print(f"DEBUG: Components found: {[c['name'] for c in latest_ds.components]}")
        
        agent = SandboxAgent(design_system_dict)
        result = await agent.generate_screen(request.prompt)
        
        return result
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
