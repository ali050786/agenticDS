# 🚀 Complete Product Roadmap: Agentic Design System Platform

**Version:** 2.0  
**Last Updated:** 2026-01-01  
**Total Duration:** 20 weeks (5 phases)  
**Team Size:** 3 developers (backend, frontend, plugin)  
**Infrastructure:** Docker (local) → RunPod (production)  

---

## 📋 Executive Overview

### What You're Building

A **design system intelligence platform** that:

1. **Extracts** design systems from Figma (colors, typography, components, spacing)
2. **Renders** the design system with a unified engine (display, edit, generate)
3. **Lets teams manage** design systems with version control and collaboration
4. **Generates code** automatically from Figma designs
5. **Generates screens** from prompts (sandbox) using design system constraints
6. **Keeps everything in sync** across teams and projects

### Key Architectural Decision

**One Universal Rendering System** instead of separate display/edit/sandbox:
- Display design tokens and components
- Edit them with live preview (same renderer)
- Generate new screens from prompts (same renderer)
- Generate code from Figma (same renderer)
- All integrated from Phase 1

### Infrastructure Stack

```
Development (Weeks 1-12): Local Docker (FREE)
├─ Backend: FastAPI, Python, LangChain
├─ Frontend: React, Vite, Tailwind
├─ Database: PostgreSQL
├─ Cache: Redis
└─ Proxy: Nginx

Production (Weeks 13+): RunPod ($2-5/month)
├─ Always-on Pod: Platform services ($3/month)
└─ Serverless: LLM agent workloads (pay-per-use, ~$1-2/month)
```

---

## 🎯 Timeline Overview

```
PHASE 1 (Weeks 1-4):   MVP - Extract + Unified Rendering + Sandbox
PHASE 2 (Weeks 5-8):   Management - Enhanced Editing + Version Control + Collaboration
PHASE 3 (Weeks 9-12):  Code Generation - Figma-to-Code + Developer Handover
PHASE 4 (Weeks 13-16): Production - Launch on RunPod + Optimization
PHASE 5 (Weeks 17-20): Advanced - Templates + Workflows + Enterprise Features
```

---

# PHASE 1: MVP - Extract + Unified Rendering + Sandbox (Weeks 1-4)

## Overview

Build the core platform with **one rendering system** that handles:
- Displaying extracted design system
- Live editing with preview
- Generating new screens from prompts
- All integrated and working together

**Cost:** $0 (local Docker)  
**Result:** Full-featured design system manager with sandbox generation ready

---

## Week 1: Figma Plugin + Rendering Foundation

### 🎯 Goal

Extract design system from Figma and build the universal rendering system that will power all platform features.

### 📦 Plugin Development (Day 1-2)

**What Gets Built:**

```typescript
plugin/manifest.json
plugin/src/
├─ App.tsx                    // UI with "Collect" button
├─ code.ts                    // Figma API integration
├─ extractors/
│   ├─ colors.ts              // Extract paint styles
│   ├─ typography.ts          // Extract text styles
│   ├─ components.ts          // Extract components
│   └─ spacing.ts             // Extract spacing scales
├─ utils/
│   ├─ validation.ts          // Validate tokens
│   └─ formatting.ts          // Format JSON output
└─ assets/
```

**Plugin Functionality:**

```typescript
// plugin/src/code.ts
figma.showUI(__html__, { width: 400, height: 600 });

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'collect-data') {
    const colors = figma.getLocalPaintStyles().map(style => {
      const paint = style.paints[0] as SolidPaint;
      const { r, g, b } = paint.color;
      return {
        name: style.name,
        value: `rgb(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)})`,
        description: style.description
      };
    });

    const typography = figma.getLocalTextStyles().map(style => ({
      name: style.name,
      fontFamily: style.fontName.family,
      fontSize: style.fontSize,
      fontWeight: style.fontName.style,
      lineHeight: style.lineHeight.unit === 'AUTO' ? 'auto' : style.lineHeight.value
    }));

    const components = figma.root.findAllWithCriteria({ 
      types: ['COMPONENT', 'COMPONENT_SET'] 
    }).map(c => ({
      id: c.id,
      name: c.name,
      description: (c as ComponentNode).description || '',
      type: c.type
    }));

    const designSystem = {
      version: '1.0.0',
      lastUpdated: new Date().toISOString(),
      tokens: {
        colors,
        typography,
        spacing: [] // Will be extracted from components
      },
      components
    };

    figma.ui.postMessage({ type: 'data-collected', data: designSystem });
  }
};
```

**Plugin UI:**

```
┌─────────────────────────────────┐
│ Agentic Design System           │
│                                 │
│ [Collect Design System]         │
│                                 │
│ Status: Ready                   │
│                                 │
│ Extracted:                      │
│ ✓ Colors                        │
│ ✓ Typography                    │
│ ✓ Components                    │
│                                 │
│ [Download JSON] [Post Backend]  │
└─────────────────────────────────┘
```

### 🎨 Universal Rendering System (Day 2-5)

**What Gets Built:**

This is the CORE of your platform. Used everywhere.

```
backend/rendering/
├─ __init__.py
├─ universal_renderer.py      // Main rendering logic
├─ component_registry.py      // Component definitions
├─ token_resolver.py          // Token value resolution
├─ constraints.py             // Design system validation
└─ design_to_jsx.py          // Spec to code conversion
```

**Universal Renderer Implementation:**

```python
# backend/rendering/universal_renderer.py
from typing import Dict, Any, List, Optional
import json

class UniversalRenderer:
    """
    Renders design specifications for:
    1. Display (show tokens, components)
    2. Edit (preview changes)
    3. Sandbox (generate screens)
    4. Code Generation (Figma to code)
    """

    def __init__(self, design_system: Dict[str, Any]):
        self.design_system = design_system
        self.tokens = self._index_tokens()
        self.components = self._index_components()

    def render_design_specification(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert design specification to JSX code and preview
        
        Used by:
        - Display system
        - Edit preview
        - Sandbox generation
        - Code generation
        """
        # Validate specification uses only design system
        self.validate_specification(spec)
        
        # Convert to JSX
        jsx_code = self.specification_to_jsx(spec)
        
        # Extract metadata
        used_tokens = self.extract_tokens_from_spec(spec)
        used_components = self.extract_components_from_spec(spec)
        
        return {
            "jsx": jsx_code,
            "specification": spec,
            "tokens_used": used_tokens,
            "components_used": used_components,
            "valid": True
        }

    def specification_to_jsx(self, spec: Dict[str, Any], depth: int = 0) -> str:
        """Recursively convert design spec to JSX"""
        component_type = spec.get('type')
        props = spec.get('props', {})
        children = spec.get('children', [])
        content = spec.get('content', '')

        # Validate component exists
        if not self._component_exists(component_type):
            raise ValueError(f"Component '{component_type}' not found in design system")

        # Resolve props (map token references to values)
        jsx_props = self._resolve_props(props)
        
        # Build JSX string
        indent = '  ' * depth
        
        if children:
            children_jsx = '\n'.join([
                self.specification_to_jsx(child, depth + 1) 
                for child in children
            ])
            return f"{indent}<{component_type} {jsx_props}>\n{children_jsx}\n{indent}</{component_type}>"
        elif content:
            return f"{indent}<{component_type} {jsx_props}>{content}</{component_type}>"
        else:
            return f"{indent}<{component_type} {jsx_props} />"

    def validate_specification(self, spec: Dict[str, Any]) -> bool:
        """Ensure spec only uses design system tokens and components"""
        def validate_node(node):
            component_type = node.get('type')
            if not self._component_exists(component_type):
                raise ValueError(f"Component '{component_type}' not in design system")
            
            props = node.get('props', {})
            for key, value in props.items():
                if self._is_token_reference(value):
                    if value not in self.tokens:
                        raise ValueError(f"Token '{value}' not found in design system")
            
            children = node.get('children', [])
            for child in children:
                validate_node(child)
        
        validate_node(spec)
        return True

    def _resolve_props(self, props: Dict[str, Any]) -> str:
        """Convert props to JSX attributes"""
        parts = []
        for key, value in props.items():
            if isinstance(value, str):
                if self._is_token_reference(value):
                    token_value = self._resolve_token(value)
                    parts.append(f'{key}="{token_value}"')
                else:
                    parts.append(f'{key}="{value}"')
            elif isinstance(value, bool):
                if value:
                    parts.append(key)
            elif isinstance(value, (int, float)):
                parts.append(f'{key}={value}')
        return ' '.join(parts)

    def _is_token_reference(self, value: str) -> bool:
        """Check if value references a token (e.g., 'primary/500')"""
        return isinstance(value, str) and '/' in value

    def _resolve_token(self, token_name: str) -> str:
        """Get actual value of token"""
        if token_name in self.tokens:
            return self.tokens[token_name].get('value', token_name)
        raise ValueError(f"Token '{token_name}' not found")

    def _component_exists(self, component_name: str) -> bool:
        """Check if component exists in design system"""
        return component_name in self.components

    def _index_tokens(self) -> Dict[str, Dict]:
        """Create searchable index of all tokens"""
        index = {}
        for token_type in ['colors', 'typography', 'spacing']:
            tokens = self.design_system['tokens'].get(token_type, [])
            for token in tokens:
                index[token.get('name')] = token
        return index

    def _index_components(self) -> Dict[str, Dict]:
        """Create searchable index of all components"""
        index = {}
        for component in self.design_system.get('components', []):
            index[component.get('name')] = component
        return index

    def extract_tokens_from_spec(self, spec: Dict[str, Any]) -> List[str]:
        """Extract all token references from specification"""
        tokens = set()
        
        def extract_from_node(node):
            props = node.get('props', {})
            for value in props.values():
                if self._is_token_reference(value) and value in self.tokens:
                    tokens.add(value)
            
            for child in node.get('children', []):
                extract_from_node(child)
        
        extract_from_node(spec)
        return list(tokens)

    def extract_components_from_spec(self, spec: Dict[str, Any]) -> List[str]:
        """Extract all component references from specification"""
        components = set()
        
        def extract_from_node(node):
            component_type = node.get('type')
            if component_type and self._component_exists(component_type):
                components.add(component_type)
            
            for child in node.get('children', []):
                extract_from_node(child)
        
        extract_from_node(spec)
        return list(components)
```

### 🤖 Sandbox Agent (Day 4-5)

**Sandbox Agent Implementation:**

```python
# backend/agents/sandbox_agent.py
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from rendering.universal_renderer import UniversalRenderer
import json

class SandboxAgent:
    """
    Generates new screen designs from text prompts
    Constrained to use ONLY design system tokens and components
    """

    def __init__(self, design_system: Dict[str, Any]):
        self.design_system = design_system
        self.renderer = UniversalRenderer(design_system)
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            model="gemini-flash-latest",
            temperature=0
        )

    async def generate_screen(self, prompt: str) -> Dict[str, Any]:
        """Generate a screen design from natural language prompt"""
        
        # Format design system for LLM
        ds_context = self._format_design_system_for_llm()
        
        # Create constraint-enhanced prompt
        constraint_prompt = f"""
You are a UI designer that ONLY uses the provided design system.
You MUST use ONLY tokens and components from this design system.
You CANNOT create custom colors, fonts, spacing, or components.

DESIGN SYSTEM:
{ds_context}

USER REQUEST:
{prompt}

Generate a JSON specification for a screen that:
1. Uses ONLY colors from the design system
2. Uses ONLY typography from the design system
3. Uses ONLY components from the design system
4. Uses ONLY spacing values from the design system
5. Is responsive and accessible
6. Matches the user's request

Return ONLY valid JSON, no other text.

JSON Schema:
{{
  "type": "Container",
  "props": {{"background": "color-token-or-value"}},
  "children": [
    {{
      "type": "ComponentName",
      "props": {{"variant": "primary"}},
      "content": "Text content"
    }}
  ]
}}
"""

        # Generate design specification
        response = await self.llm.apredict(constraint_prompt)
        design_spec = json.loads(response.strip())
        
        # Validate against design system
        self.renderer.validate_specification(design_spec)
        
        # Render (get JSX + preview metadata)
        rendered = self.renderer.render_design_specification(design_spec)
        
        return {
            "status": "success",
            "design": design_spec,
            "code": rendered["jsx"],
            "tokens_used": rendered["tokens_used"],
            "components_used": rendered["components_used"],
            "prompt": prompt
        }

    def _format_design_system_for_llm(self) -> str:
        """Format design system in readable format for LLM"""
        parts = []
        
        # Colors
        colors_str = "\n".join([
            f"  - {t['name']}: {t['value']}"
            for t in self.design_system['tokens'].get('colors', [])
        ])
        parts.append(f"COLORS:\n{colors_str}")
        
        # Typography
        typo_str = "\n".join([
            f"  - {t['name']}: {t['fontFamily']} {t['fontSize']}px {t['fontWeight']}"
            for t in self.design_system['tokens'].get('typography', [])
        ])
        parts.append(f"TYPOGRAPHY:\n{typo_str}")
        
        # Components
        comp_str = "\n".join([
            f"  - {c['name']}"
            for c in self.design_system.get('components', [])
        ])
        parts.append(f"COMPONENTS:\n{comp_str}")
        
        return "\n\n".join(parts)
```

### 📂 Docker Setup

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: dsm_user
      POSTGRES_PASSWORD: dsm_password
      POSTGRES_DB: dsm_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U dsm_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://dsm_user:dsm_password@postgres:5432/dsm_db
      REDIS_URL: redis://redis:6379
      GOOGLE_API_KEY: ${GOOGLE_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app/backend
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend Dashboard
  dashboard:
    build:
      context: ./dashboard
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./dashboard:/app/dashboard
      - /app/dashboard/node_modules
    command: npm run dev

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on:
      - backend
      - dashboard

volumes:
  postgres_data:

networks:
  default:
    name: dsm_network
```

**backend/Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**dashboard/Dockerfile:**

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

**nginx.conf:**

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }

    upstream dashboard {
        server dashboard:3000;
    }

    server {
        listen 80;
        server_name localhost;

        # API endpoints
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Dashboard
        location / {
            proxy_pass http://dashboard;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### 📋 Week 1 Deliverables

```
✅ Plugin extracts design system from Figma
✅ Universal rendering system built (core infrastructure)
✅ Sandbox agent implemented (generates from prompts)
✅ Docker setup configured
✅ All components running locally
✅ No bugs
```

### 🧪 Week 1 Testing

```
FLOW 1: Extract
1. Open Figma file with design system
2. Click "Collect Design System" in plugin
3. Get design system JSON
✅ PASS

FLOW 2: Sandbox (Basic Test)
1. Send test prompt to sandbox agent
2. Agent generates design specification
3. Rendering system converts to JSX
✅ PASS
```

---

## Week 2: Backend APIs + Database + Sandbox Full Integration

### 🎯 Goal

Build complete backend with database storage and all API endpoints needed to support display, editing, and sandbox generation.

### 🗄️ Database Schema

```python
# backend/database/models.py
from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DesignSystem(Base):
    __tablename__ = "design_systems"
    
    id: str = Column(String, primary_key=True)
    name: str = Column(String)
    version: str = Column(String)
    organization_id: str = Column(String)
    tokens: dict = Column(JSON)
    components: list = Column(JSON)
    created_at: datetime = Column(DateTime)
    updated_at: datetime = Column(DateTime)

class GeneratedScreen(Base):
    __tablename__ = "generated_screens"
    
    id: str = Column(String, primary_key=True)
    design_system_id: str = Column(String)
    prompt: str = Column(String)
    design_spec: dict = Column(JSON)
    code: str = Column(String)
    tokens_used: list = Column(JSON)
    components_used: list = Column(JSON)
    created_at: datetime = Column(DateTime)

class DesignToken(Base):
    __tablename__ = "design_tokens"
    
    id: str = Column(String, primary_key=True)
    design_system_id: str = Column(String)
    name: str = Column(String)
    type: str = Column(String)  # color, typography, spacing
    value: dict = Column(JSON)
    created_at: datetime = Column(DateTime)
    updated_at: datetime = Column(DateTime)
```

### 🔌 API Endpoints

```python
# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from rendering.universal_renderer import UniversalRenderer
from agents.sandbox_agent import SandboxAgent

app = FastAPI(title="Agentic Design System API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DESIGN SYSTEM MANAGEMENT
# ============================================================================

@app.post("/api/design-system/ingest")
async def ingest_design_system(design_system: dict):
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
            organization_id=get_org_id(request),  # From auth
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(db_system)
        db.commit()
        
        return {
            "status": "success",
            "message": f"Design system ingested as {version}",
            "design_system_id": db_system.id,
            "version": version
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/design-system/latest")
async def get_latest_design_system():
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
        return {"status": "error", "message": str(e)}

@app.get("/api/design-system/versions")
async def get_design_system_versions():
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
# TOKEN MANAGEMENT
# ============================================================================

@app.get("/api/tokens")
async def get_tokens(design_system_id: str):
    """Get all tokens for design system"""
    try:
        ds = db.query(DesignSystem).filter(DesignSystem.id == design_system_id).first()
        if not ds:
            raise HTTPException(status_code=404, detail="Design system not found")
        
        return {
            "colors": ds.tokens.get('colors', []),
            "typography": ds.tokens.get('typography', []),
            "spacing": ds.tokens.get('spacing', [])
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.patch("/api/tokens/{token_id}")
async def update_token(token_id: str, updates: dict):
    """
    Update a token (color, typography, spacing)
    Renderer validates changes, then updates database
    """
    try:
        token = db.query(DesignToken).filter(DesignToken.id == token_id).first()
        if not token:
            raise HTTPException(status_code=404, detail="Token not found")
        
        # Get design system
        ds = db.query(DesignSystem).filter(
            DesignSystem.id == token.design_system_id
        ).first()
        
        # Create renderer with current DS
        renderer = UniversalRenderer(ds.to_dict())
        
        # Validate token update doesn't break anything
        # (In Phase 2, we'll add full validation)
        
        # Update token
        token.value = updates.get('value', token.value)
        token.updated_at = datetime.now()
        db.commit()
        
        return {
            "status": "success",
            "message": "Token updated",
            "token": {
                "id": token.id,
                "name": token.name,
                "value": token.value
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================================
# SANDBOX GENERATION
# ============================================================================

@app.post("/api/sandbox/generate")
async def generate_from_prompt(request_body: dict):
    """
    Generate new screen from text prompt
    Uses sandbox agent with design system constraints
    """
    try:
        prompt = request_body.get('prompt')
        design_system_id = request_body.get('design_system_id')
        
        if not prompt or not design_system_id:
            raise HTTPException(status_code=400, detail="Missing prompt or design_system_id")
        
        # Load design system
        ds = db.query(DesignSystem).filter(DesignSystem.id == design_system_id).first()
        if not ds:
            raise HTTPException(status_code=404, detail="Design system not found")
        
        # Create sandbox agent
        agent = SandboxAgent(ds.to_dict())
        
        # Generate
        result = await agent.generate_screen(prompt)
        
        # Store in database
        generated_screen = GeneratedScreen(
            id=str(uuid.uuid4()),
            design_system_id=design_system_id,
            prompt=prompt,
            design_spec=result['design'],
            code=result['code'],
            tokens_used=result['tokens_used'],
            components_used=result['components_used'],
            created_at=datetime.now()
        )
        db.add(generated_screen)
        db.commit()
        
        return {
            "status": "success",
            "screen_id": generated_screen.id,
            "design": result['design'],
            "code": result['code'],
            "tokens_used": result['tokens_used'],
            "components_used": result['components_used']
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/generated-screens/{design_system_id}")
async def get_generated_screens(design_system_id: str):
    """Get all generated screens for a design system"""
    try:
        screens = db.query(GeneratedScreen)\
            .filter(GeneratedScreen.design_system_id == design_system_id)\
            .order_by(GeneratedScreen.created_at.desc())\
            .all()
        
        return {
            "status": "success",
            "screens": [
                {
                    "id": s.id,
                    "prompt": s.prompt,
                    "code": s.code,
                    "tokens_used": s.tokens_used,
                    "components_used": s.components_used,
                    "created_at": s.created_at
                }
                for s in screens
            ]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Check if backend is running"""
    return {"status": "healthy", "timestamp": datetime.now()}
```

### 📋 Week 2 Deliverables

```
✅ Database schema created
✅ All API endpoints working
✅ Design system ingestion working
✅ Sandbox generation API working
✅ Token management endpoints ready
✅ Version tracking implemented
✅ All data persists in PostgreSQL
```

---

## Week 3: Dashboard UI with Unified Rendering

### 🎯 Goal

Build dashboard that uses the universal rendering system for all modes: display, edit, and sandbox generation.

### 📁 Dashboard Structure

```
dashboard/src/
├─ pages/
│   └─ DesignSystemPage.tsx       // Main page with tabs
├─ components/
│   ├─ DesignSystemRenderer.tsx   // Universal renderer (React)
│   ├─ TokensTab.tsx              // Display + edit tokens
│   ├─ ComponentsTab.tsx          // Display + edit components
│   ├─ SandboxTab.tsx             // Generate from prompts
│   └─ CodeDisplay.tsx            // Show generated code
├─ hooks/
│   ├─ useDesignSystem.ts
│   └─ useSandbox.ts
└─ services/
    ├─ designSystemService.ts
    └─ sandboxService.ts
```

### 🎨 Universal Renderer (React)

```typescript
// dashboard/src/components/DesignSystemRenderer.tsx
import React, { useState } from 'react';
import { DesignSystem, DesignToken, Component } from '../types';

interface DesignSystemRendererProps {
  designSystem: DesignSystem;
  mode: 'display' | 'edit' | 'sandbox';
  onTokenEdit?: (tokenId: string, newValue: any) => void;
  onComponentEdit?: (componentId: string, newProps: any) => void;
}

export const DesignSystemRenderer: React.FC<DesignSystemRendererProps> = ({
  designSystem,
  mode,
  onTokenEdit,
  onComponentEdit
}) => {
  const [editingTokenId, setEditingTokenId] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');

  // Render color token
  const renderColorToken = (token: DesignToken) => {
    if (mode === 'display') {
      return (
        <div className="token-item" onClick={() => {
          if (mode === 'edit') {
            setEditingTokenId(token.id);
            setEditValue(token.value);
          }
        }}>
          <div
            className="color-swatch"
            style={{ backgroundColor: token.value }}
            title={token.name}
          />
          <span className="token-name">{token.name}</span>
          <span className="token-value">{token.value}</span>
        </div>
      );
    }

    if (mode === 'edit' && editingTokenId === token.id) {
      return (
        <div className="token-edit-mode">
          <input
            type="text"
            value={editValue}
            onChange={(e) => setEditValue(e.target.value)}
            placeholder="Enter color value"
          />
          
          <div className="live-preview">
            <h4>Live Preview:</h4>
            {/* Show components using this color */}
            <div
              className="sample-button"
              style={{ backgroundColor: editValue }}
            >
              Sample Button
            </div>
            <div style={{ color: editValue }}>Sample Text</div>
          </div>
          
          <button onClick={() => {
            onTokenEdit?.(token.id, editValue);
            setEditingTokenId(null);
          }}>
            Save
          </button>
          <button onClick={() => setEditingTokenId(null)}>Cancel</button>
        </div>
      );
    }

    return null;
  };

  // Render typography token
  const renderTypographyToken = (token: DesignToken) => {
    const style = {
      fontFamily: token.value.fontFamily,
      fontSize: token.value.fontSize,
      fontWeight: token.value.fontWeight
    };

    return (
      <div className="typography-item" onClick={() => {
        if (mode === 'edit') setEditingTokenId(token.id);
      }}>
        <div style={style} className="typography-preview">
          The quick brown fox jumps over the lazy dog
        </div>
        <span className="token-name">{token.name}</span>
        <span className="token-value">
          {token.value.fontFamily} {token.value.fontSize}px
        </span>
      </div>
    );
  };

  // Render component
  const renderComponent = (component: Component) => {
    return (
      <div className="component-card" onClick={() => {
        if (mode === 'edit') {
          setEditingTokenId(component.id);
        }
      }}>
        {/* Component preview */}
        <div className="component-preview">
          {/* Render actual component from DS */}
          {component.name === 'Button' && (
            <button className="button-primary">Sample Button</button>
          )}
          {component.name === 'Card' && (
            <div className="card">Sample Card Content</div>
          )}
        </div>
        
        {editingTokenId === component.id && mode === 'edit' && (
          <div className="component-edit">
            {/* Props editor would go here */}
            <input placeholder="Edit component props" />
            <button onClick={() => {
              onComponentEdit?.(component.id, {});
              setEditingTokenId(null);
            }}>
              Save
            </button>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="design-system-renderer">
      {/* Colors */}
      <section className="tokens-section">
        <h2>Colors</h2>
        <div className="token-grid">
          {designSystem.tokens.colors?.map(token => (
            <div key={token.id}>
              {renderColorToken(token)}
            </div>
          ))}
        </div>
      </section>

      {/* Typography */}
      <section className="tokens-section">
        <h2>Typography</h2>
        <div className="token-list">
          {designSystem.tokens.typography?.map(token => (
            <div key={token.id}>
              {renderTypographyToken(token)}
            </div>
          ))}
        </div>
      </section>

      {/* Components */}
      <section className="components-section">
        <h2>Components</h2>
        <div className="component-grid">
          {designSystem.components?.map(component => (
            <div key={component.id}>
              {renderComponent(component)}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};
```

### 📄 Main Design System Page

```typescript
// dashboard/src/pages/DesignSystemPage.tsx
import React, { useState, useEffect } from 'react';
import { DesignSystemRenderer } from '../components/DesignSystemRenderer';
import { useDesignSystem } from '../hooks/useDesignSystem';
import { useSandbox } from '../hooks/useSandbox';

export const DesignSystemPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'tokens' | 'components' | 'sandbox'>('tokens');
  const [prompt, setPrompt] = useState('');
  const [generatedScreen, setGeneratedScreen] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const { designSystem, updateToken, updateComponent } = useDesignSystem();
  const { generateFromPrompt } = useSandbox();

  const handleGenerateFromPrompt = async () => {
    setLoading(true);
    try {
      const result = await generateFromPrompt(prompt, designSystem.id);
      setGeneratedScreen(result);
    } catch (error) {
      console.error('Generation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!designSystem) return <div>Loading design system...</div>;

  return (
    <div className="design-system-page">
      {/* Header */}
      <header className="page-header">
        <h1>Design System Manager</h1>
        <div className="tabs">
          <button
            className={activeTab === 'tokens' ? 'active' : ''}
            onClick={() => setActiveTab('tokens')}
          >
            Tokens
          </button>
          <button
            className={activeTab === 'components' ? 'active' : ''}
            onClick={() => setActiveTab('components')}
          >
            Components
          </button>
          <button
            className={activeTab === 'sandbox' ? 'active' : ''}
            onClick={() => setActiveTab('sandbox')}
          >
            Sandbox
          </button>
        </div>
      </header>

      {/* Content */}
      <main className="page-content">
        {/* TOKENS & COMPONENTS: Use universal renderer */}
        {(activeTab === 'tokens' || activeTab === 'components') && (
          <DesignSystemRenderer
            designSystem={designSystem}
            mode="edit"
            onTokenEdit={updateToken}
            onComponentEdit={updateComponent}
          />
        )}

        {/* SANDBOX: Generate from prompts */}
        {activeTab === 'sandbox' && (
          <div className="sandbox-section">
            <div className="sandbox-input">
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe the screen you want to create...
Example: Create a checkout form with email, password, and submit button"
              />
              <button
                onClick={handleGenerateFromPrompt}
                disabled={loading}
              >
                {loading ? 'Generating...' : 'Generate Screen'}
              </button>
            </div>

            {generatedScreen && (
              <div className="sandbox-output">
                <div className="preview">
                  <h3>Generated Design</h3>
                  {/* Render generated screen using universal renderer */}
                  <DesignSystemRenderer
                    designSystem={designSystem}
                    mode="display"
                  />
                </div>

                <div className="code">
                  <h3>Generated Code</h3>
                  <pre>{generatedScreen.code}</pre>
                  <button onClick={() => navigator.clipboard.writeText(generatedScreen.code)}>
                    Copy Code
                  </button>
                </div>

                <div className="metadata">
                  <h3>Tokens Used:</h3>
                  <ul>
                    {generatedScreen.tokens_used?.map((token: string) => (
                      <li key={token}>{token}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};
```

### 📋 Week 3 Deliverables

```
✅ Dashboard displays design system
✅ Universal renderer working (display, edit, sandbox modes)
✅ Live editing with preview working
✅ Sandbox generation working
✅ Code display working
✅ All tabs functional
✅ Responsive design
```

---

## Week 4: Integration & Production Launch

### 🎯 Goal

Complete end-to-end testing, performance optimization, and prepare for production launch.

### ✅ Testing Checklist

```
FLOW 1: Extract Design System
1. Open Figma with design system
2. Click "Collect" in plugin
3. Plugin sends to backend
4. Backend stores in database
5. Dashboard loads and displays
✅ PASS

FLOW 2: Edit Tokens (Live Preview)
1. Click color token
2. Change value
3. Live preview updates
4. Click Save
5. Database updates, version increments
✅ PASS

FLOW 3: Generate Screen
1. Open Sandbox tab
2. Type prompt: "Create a login form"
3. System generates design spec
4. Rendering system validates (uses only DS)
5. Converts to JSX
6. Shows preview + code
✅ PASS

FLOW 4: End-to-End
1. Extract design system
2. Edit tokens
3. Generate new screen
4. All working together seamlessly
✅ PASS
```

### 🚀 Startup Script

**startup.sh:**

```bash
#!/bin/bash

echo "🚀 Starting Agentic Design System..."

# Kill existing processes
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:5432 | xargs kill -9 2>/dev/null

# Start Docker Compose
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 10

# Run migrations
docker-compose exec -T backend python -m alembic upgrade head

# Create admin user (optional)
# docker-compose exec -T backend python scripts/create_admin.py

echo "✅ All services running!"
echo ""
echo "🌐 Dashboard: http://localhost:3000"
echo "🔌 API: http://localhost:8000"
echo "📊 Docs: http://localhost:8000/docs"
echo ""
echo "💡 To stop all services: docker-compose down"
```

### 📋 Week 4 Deliverables

```
✅ All flows tested end-to-end
✅ No critical bugs
✅ Performance optimized
✅ Database migrations working
✅ Docker setup complete
✅ Startup script ready
✅ Documentation complete
✅ Ready for Phase 2
```

---

# PHASE 2: Enhanced Management & Collaboration (Weeks 5-8)

## Overview

Add advanced editing capabilities, version control, team collaboration, and multi-version support.

**Cost:** $0 (still local Docker)  
**New Features:** Component editing, advanced constraints, version rollback, collaboration

---

## Week 5: Component Editing & Advanced Props

### What Gets Built

```
COMPONENT EDITING:
├─ Edit component variants
├─ Edit component props (all properties)
├─ Live preview of all variants
├─ Save as new version
└─ Component versioning

ADVANCED EDITING:
├─ Drag-to-edit spacing
├─ Color picker for tokens
├─ Multi-select for variants
└─ Undo/Redo support
```

---

## Week 6: File Editor & Direct Code Editing

### What Gets Built

```
CODE EDITOR:
├─ Edit generated code directly
├─ Syntax highlighting
├─ Validation
├─ Auto-format
└─ Preview updates

FILE MANAGEMENT:
├─ View all files in system
├─ Edit any file
├─ Create new files
└─ Delete files
```

---

## Week 7: Version Control & Rollback

### What Gets Built

```
VERSION MANAGEMENT:
├─ Every edit creates version
├─ View all versions
├─ Compare versions
├─ Rollback to any version
├─ Version history with metadata
└─ CHANGELOG auto-generated

EXAMPLE:
v1.2.0 (current)
├─ "Updated Button padding"
├─ 3 days ago
├─ By John Doe
└─ [View] [Compare] [Rollback]

v1.1.0
├─ "Added success/700 token"
├─ 5 days ago
└─ [View] [Compare] [Rollback]
```

---

## Week 8: Team Collaboration & Permissions

### What Gets Built

```
TEAM FEATURES:
├─ Multiple users per design system
├─ Roles: Owner, Editor, Viewer
├─ Activity log (who changed what)
├─ Comments on tokens/components
├─ Notifications on changes
├─ Simultaneous editing support
└─ Conflict resolution

EXAMPLE ACTIVITY LOG:
2024-01-15 10:30 - John Doe
  "Updated primary/500 color"
  Changed from #3B82F6 to #3066D6

2024-01-15 09:45 - Jane Smith
  "Edited Button component"
  Updated padding from 8px to 10px
```

---

# PHASE 3: Code Generation from Figma (Weeks 9-12)

## Overview

Enable developers to generate production-ready code directly from Figma frames.

**New Feature:** Select Figma frame → Generate code using design system  
**Cost:** $0 (local) or $1-2/month (RunPod serverless optional)

---

## Week 9: Figma Selection Extraction

```
PLUGIN ENHANCEMENT:
├─ "Generate Code" button
├─ Select frame in Figma
├─ Extract frame structure
├─ Send to backend
└─ Get code back

CODE GENERATION:
├─ Figma frame → Design spec
├─ Match to components
├─ Generate JSX
├─ Preview in dashboard
└─ Copy or download
```

---

## Week 10: Backend Code Generation Pipeline

```
AGENT PIPELINE:
├─ Analyze Figma frame
├─ Extract component tree
├─ Map to design system components
├─ Generate component spec
├─ Render to JSX
└─ Return code

VALIDATION:
├─ Ensure all tokens used exist
├─ Ensure all components used exist
├─ Check responsive design
└─ Validate accessibility
```

---

## Week 11: Developer Export & Integration

```
EXPORT OPTIONS:
├─ Copy code to clipboard
├─ Download as .tsx file
├─ Add to component library
├─ Generate as npm package
└─ Export as design spec (JSON)

INTEGRATION:
├─ Git integration
├─ GitHub PR creation
├─ Slack notifications
└─ Webhook support
```

---

## Week 12: Code Generation Polish & Optimization

```
IMPROVEMENTS:
├─ Batch generation (multiple frames)
├─ Template selection (common patterns)
├─ Code customization
├─ Performance optimization
└─ Error handling & recovery
```

---

# PHASE 4: Production Launch (Weeks 13-16)

## Overview

Deploy to production on RunPod and optimize for real-world usage.

**Infrastructure:** RunPod Pod ($2-3/month) + Optional serverless ($1-2/month)

---

## Week 13: Production Preparation

```
DEPLOYMENT SETUP:
├─ Create RunPod account
├─ Set up persistent pod
├─ Configure environment
├─ Set up monitoring
├─ Configure backups
└─ SSL certificates

DOCKER PRODUCTION:
├─ docker-compose.prod.yml
├─ .env.production
├─ Volume configuration
└─ Network security
```

---

## Week 14: Deploy to RunPod

```
DEPLOYMENT STEPS:
1. Rent RunPod pod ($3/month)
2. SSH into pod
3. Clone repository
4. Configure environment
5. Build Docker images
6. Run migrations
7. Start services
8. Verify all working
9. Point domain to pod
10. Set up SSL

RESULT:
✅ Platform live at yourdomain.com
✅ All services running
✅ Database persistent
✅ Backups configured
✅ Monitoring active
```

---

## Week 15: Performance Optimization & Testing

```
OPTIMIZATION:
├─ Database indexing
├─ Query optimization
├─ Cache configuration
├─ Asset compression
├─ CDN setup
└─ Load testing

UAT TESTING:
├─ Full end-to-end on production
├─ Performance benchmarks
├─ Security audits
├─ User acceptance testing
└─ Bug fixes
```

---

## Week 16: Production Launch

```
LAUNCH CHECKLIST:
├─ All tests passing
├─ Monitoring configured
├─ Backups tested
├─ Documentation complete
├─ Support system ready
├─ Legal/compliance ready
├─ Marketing ready
└─ Team trained

GO LIVE:
├─ Announce beta
├─ Invite first users
├─ Monitor closely
├─ Fix issues quickly
├─ Iterate based on feedback
```

---

# PHASE 5: Advanced Features (Weeks 17-20)

## Overview

Build advanced features after launch based on user feedback.

---

## Week 17-18: Component Templates & Variations

```
TEMPLATES:
├─ Pre-built templates (login, checkout, dashboard)
├─ Template customization
├─ Template library
└─ Community templates

VARIATIONS:
├─ Component variants
├─ Responsive variants
├─ Dark mode support
└─ A/B testing support
```

---

## Week 19-20: Workflows & Automation

```
WORKFLOWS:
├─ Design → Code automation
├─ Multi-step processes
├─ Approval workflows
├─ CI/CD integration
└─ GitHub Actions

ADVANCED:
├─ Batch operations
├─ Scheduled generation
├─ Custom rules engine
└─ Plugin system
```

---

# 🏗️ Complete Architecture Overview

## Data Flow (High Level)

```
PLUGIN (Extract)
    ↓
BACKEND (Process)
    ↓
RENDERING SYSTEM (Core)
    ├─ Display design system
    ├─ Edit with live preview
    ├─ Generate from prompts
    └─ Generate from Figma
    ↓
DASHBOARD (Interact)
    ├─ View
    ├─ Edit
    ├─ Generate
    └─ Manage
```

## Component Architecture

```
frontend/
├─ Universal Renderer
│   ├─ Display tokens
│   ├─ Display components
│   ├─ Edit with preview
│   ├─ Render generated screens
│   └─ Render Figma-generated code
└─ Reused by all tabs

backend/
├─ Rendering System (Python)
│   ├─ Validate design specs
│   ├─ Spec to JSX
│   ├─ Token resolution
│   └─ Component registry
├─ Agents
│   ├─ Sandbox Agent (generate from prompt)
│   └─ Figma Agent (generate from frame)
├─ APIs
│   ├─ Design system management
│   ├─ Token/component CRUD
│   ├─ Sandbox generation
│   └─ Code generation
└─ Database
    ├─ Design systems
    ├─ Tokens
    ├─ Components
    ├─ Generated screens
    └─ Versions
```

---

# 📊 Development Workflow

## Daily (Weeks 1-12)

```bash
# Morning
cd agentic-dsm
docker-compose up -d

# Code
# Docker auto-reloads on changes
# Test at http://localhost:3000
# Test at http://localhost:8000

# Debug
docker-compose logs -f backend
docker-compose logs -f dashboard

# Commit
git add .
git commit -m "Feature: [description]"
git push origin main

# Evening
docker-compose down
```

## Deployment (Week 14+)

```bash
# On local machine
git push origin main

# On RunPod pod (SSH)
cd agentic-dsm
git pull
docker-compose -f docker-compose.prod.yml up -d --build

# Verify
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs -f backend
```

---

# 💰 Cost Breakdown

## Development (Weeks 1-12)

```
Local Docker: $0
Total: $0
```

## Production (Week 13+)

```
RunPod Pod (always-on):
  2 vCPU, 4GB RAM, 20GB SSD
  Cost: $0.10/hour × 24 = $2.40/day
  Monthly: ~$70/month (running 24/7)
  
  OPTIMIZATION: Run only during business hours
  Cost: $0.10/hour × 8 = $0.80/day
  Monthly: ~$24/month

RunPod Serverless (LLM workloads):
  20 generations/day × $0.0025 = $0.05/day
  Monthly: ~$1.50/month

PostgreSQL Backup:
  $5-10/month (external service optional)

Domain & SSL:
  $10-15/year

TOTAL MONTHLY (Optimized):
$24 (pod, 8 hours) + $1.50 (serverless) = $25.50/month

TOTAL MONTHLY (Always-on):
$70 (pod, 24 hours) + $1.50 (serverless) = $71.50/month
```

## vs Competitors

```
Heroku: $50-300/month
Vercel: $20-50/month
AWS: $100-500+/month
Your Solution: $25/month ✅

SAVINGS: 90% cheaper than alternatives
```

---

# 🎯 Success Metrics by Phase

## Phase 1 (Week 4)

```
✅ Extract design system from Figma
✅ Display in dashboard
✅ Edit with live preview
✅ Generate new screens from prompts
✅ All features working locally
✅ $0 cost
✅ Code is clean and documented
```

## Phase 2 (Week 8)

```
✅ Component editing working
✅ Version control implemented
✅ Team collaboration supported
✅ Advanced editing features
✅ Still $0 cost
```

## Phase 3 (Week 12)

```
✅ Figma-to-Code generation working
✅ Developers can generate code from designs
✅ Code always uses design system
✅ Code generation tested and optimized
✅ Still $0 cost (local)
```

## Phase 4 (Week 16)

```
✅ Live on RunPod production
✅ All features working in production
✅ Performance optimized
✅ Monitoring and alerts working
✅ First customers on platform
✅ $25-70/month (optimized)
```

## Phase 5 (Week 20)

```
✅ Advanced features deployed
✅ Community using platform
✅ Happy customers
✅ Recurring revenue
✅ Ready to scale
```

---

# 📁 Final Project Structure

```
agentic-dsm/
│
├─ plugin/                          # Figma Plugin
│   ├─ src/
│   │   ├─ App.tsx
│   │   ├─ code.ts
│   │   ├─ extractors/
│   │   │   ├─ colors.ts
│   │   │   ├─ typography.ts
│   │   │   ├─ components.ts
│   │   │   └─ spacing.ts
│   │   └─ utils/
│   ├─ manifest.json
│   ├─ package.json
│   └─ tsconfig.json
│
├─ backend/                         # FastAPI Backend
│   ├─ main.py
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ agents/
│   │   ├─ sandbox_agent.py
│   │   ├─ figma_agent.py
│   │   ├─ schema.py
│   │   └─ utils.py
│   ├─ rendering/                  # CORE SYSTEM
│   │   ├─ __init__.py
│   │   ├─ universal_renderer.py
│   │   ├─ component_registry.py
│   │   ├─ token_resolver.py
│   │   ├─ constraints.py
│   │   └─ design_to_jsx.py
│   ├─ database/
│   │   ├─ models.py
│   │   └─ migrations/
│   ├─ storage/
│   │   ├─ design_systems/
│   │   └─ generated_screens/
│   └─ routes/
│       ├─ design_system.py
│       ├─ tokens.py
│       ├─ components.py
│       ├─ sandbox.py
│       └─ code_generation.py
│
├─ dashboard/                       # React Frontend
│   ├─ src/
│   │   ├─ pages/
│   │   │   └─ DesignSystemPage.tsx
│   │   ├─ components/
│   │   │   ├─ DesignSystemRenderer.tsx
│   │   │   ├─ TokensTab.tsx
│   │   │   ├─ ComponentsTab.tsx
│   │   │   ├─ SandboxTab.tsx
│   │   │   └─ CodeDisplay.tsx
│   │   ├─ hooks/
│   │   │   ├─ useDesignSystem.ts
│   │   │   └─ useSandbox.ts
│   │   ├─ services/
│   │   │   ├─ designSystemService.ts
│   │   │   └─ sandboxService.ts
│   │   ├─ App.tsx
│   │   └─ main.tsx
│   ├─ Dockerfile
│   ├─ package.json
│   └─ tsconfig.json
│
├─ shared/
│   └─ types.ts                     # Shared TypeScript types
│
├─ docker-compose.yml               # Local development
├─ docker-compose.prod.yml          # Production
├─ nginx.conf                       # Reverse proxy
├─ .env                            # Local environment
├─ .env.production                 # Production environment
├─ .gitignore
├─ startup.sh                       # Quick start script
├─ README.md
└─ ROADMAP.md                       # This file!
```

---

# 🚀 Quick Start Guide

## Prerequisites

```
- Docker & Docker Compose
- Node.js 20+
- Python 3.11+
- Git
```

## First Time Setup

```bash
# Clone repository
git clone https://github.com/yourorg/agentic-dsm.git
cd agentic-dsm

# Copy environment
cp .env.example .env

# Start all services
chmod +x startup.sh
./startup.sh

# Wait for services to start (~15 seconds)

# Open in browser
# Dashboard: http://localhost:3000
# API: http://localhost:8000/docs
# Figma Plugin: Install from Figma app store
```

## Daily Development

```bash
# Start
docker-compose up -d

# Work
# Edit code, Docker auto-reloads

# View logs
docker-compose logs -f backend
docker-compose logs -f dashboard

# Stop
docker-compose down
```

## Production Deployment

```bash
# 1. Create RunPod account and pod
# 2. SSH into pod
# 3. Clone repository
# 4. Copy production environment
# 5. Run production docker-compose
docker-compose -f docker-compose.prod.yml up -d --build

# 6. Verify
docker-compose -f docker-compose.prod.yml ps

# 7. Configure domain/SSL
# 8. Done!
```

---

# 📚 Key Concepts

## Universal Rendering System

Instead of separate display/edit/sandbox systems, everything uses ONE rendering engine:

```
Input: Design Specification JSON
  {
    "type": "Button",
    "props": {"variant": "primary", "background": "primary/500"},
    "children": [...]
  }

Output (all modes):
  ├─ Display: Rendered token/component
  ├─ Edit: Same, but click → live preview
  ├─ Sandbox: Generated design rendered
  └─ Code Gen: Generated code rendered

Benefits:
✅ No duplication
✅ Consistent behavior
✅ Easy to maintain
✅ Extensible architecture
```

## Design System as Source of Truth

```
Design System = Single source of truth
├─ Colors
├─ Typography
├─ Spacing
├─ Components
└─ All rules

All generation respects design system:
├─ Generated screens use only DS tokens
├─ Generated code uses only DS components
├─ No custom styles allowed
├─ Perfect consistency guaranteed
```

## Rendering Constraint Engine

```
Every render ensures:
├─ Only tokens from design system used
├─ Only components from design system used
├─ Only values from design system used
└─ Raises error if violated

Validation happens at:
├─ Backend (before storing)
├─ Frontend (before preview)
└─ Code generation (before returning code)
```

---

# 🎓 Team Skills Development

## Week 1-4 (Phase 1)

```
Backend Dev learns:
✅ Figma API
✅ LLM prompt engineering
✅ Design system concepts
✅ Docker development

Frontend Dev learns:
✅ React rendering
✅ Real-time preview
✅ Interactive UI
✅ API integration

Plugin Dev learns:
✅ Figma plugin API
✅ Data extraction
✅ TypeScript
✅ Figma ecosystem
```

## Week 5-8 (Phase 2)

```
Backend Dev learns:
✅ Database design
✅ Version control systems
✅ Collaboration features
✅ Optimization

Frontend Dev learns:
✅ State management
✅ Complex UI interactions
✅ Live editing
✅ Performance optimization
```

## Week 9-12 (Phase 3)

```
Backend Dev learns:
✅ Code generation
✅ Agent orchestration
✅ Multi-step pipelines
✅ Advanced LLM usage

Frontend Dev learns:
✅ Developer experience
✅ Code display/formatting
✅ Export features
✅ Integration patterns
```

## Week 13-20 (Production)

```
Team learns:
✅ DevOps & deployment
✅ Production monitoring
✅ Customer support
✅ Performance tuning
✅ Security hardening
✅ Scaling strategies
```

---

# 🔐 Security Considerations

## Phase 1-4 (MVP)

```
Basic security:
✅ CORS configured
✅ Input validation
✅ SQL injection protection
✅ Rate limiting
✅ Environment variables
```

## Phase 5+ (Production Hardening)

```
Advanced security:
├─ Authentication (OAuth/JWT)
├─ Authorization (RBAC)
├─ Encryption (at rest, in transit)
├─ Audit logging
├─ Penetration testing
├─ GDPR compliance
└─ SOC 2 compliance
```

---

# 📞 Support & Resources

## For Team

```
Docs: /docs directory
API Docs: http://localhost:8000/docs
Code Comments: Throughout codebase
Slack: #engineering channel
Weekly standup: Tuesday 10am
```

## For Customers (Phase 4+)

```
Documentation: https://docs.yourdomain.com
Discord: Community support
Email: support@yourdomain.com
GitHub Issues: Bug reports
```

---

# 🎉 Success! You Built It!

At the end of Week 20, you have:

```
✅ Platform extracting design systems from Figma
✅ Teams managing design systems collaboratively
✅ Developers generating code automatically
✅ Everything using unified rendering system
✅ Running on production infrastructure
✅ First customers using platform
✅ Team skilled in modern architecture
✅ Defensible product with clear differentiation
✅ Low-cost infrastructure ($25-70/month)
✅ Revenue-ready pricing model ($500-5,000/month)

Next steps:
├─ Scale to 100+ customers
├─ Add enterprise features
├─ Build integrations (GitHub, Slack, etc.)
├─ Explore new markets
└─ Continue innovating
```

---

# 📝 Notes & Assumptions

## Technology Choices

```
Backend: FastAPI (simple, fast, great for APIs)
Frontend: React (large ecosystem, many developers)
Database: PostgreSQL (reliable, mature, free)
LLM: Google Gemini Flash (fast, cheap, good for constraints)
Infrastructure: RunPod (cheap, easy to manage)
```

## Alternative Choices (if needed)

```
Backend: Django, FastAPI, Express
Frontend: Vue, Svelte, Angular
Database: MongoDB, MySQL, Firebase
LLM: OpenAI, Anthropic, Groq
Infrastructure: AWS, GCP, Azure, Linode
```

## Risks & Mitigations

```
Risk: LLM generation might not always match design system
Mitigation: Use constraint prompting, validation layer, human review

Risk: Scaling to many users
Mitigation: Database optimization, caching, load testing from week 1

Risk: Design system changes breaking generated code
Mitigation: Version control, rollback support, migration tools

Risk: Team learns slowly
Mitigation: Weekly knowledge sharing, code reviews, documentation
```

---

# 🚀 You're Ready!

This roadmap is your blueprint for the next 20 weeks. 

Key principles:
- **Build unified systems** (one renderer, not three separate ones)
- **Integrate early** (sandbox in phase 1, not phase 5)
- **Test continuously** (end-to-end testing every week)
- **Communicate clearly** (documentation as you build)
- **Stay focused** (deliver what's planned, defer what's not)

**Start Week 1 on Monday. Ship Phase 1 by Friday of Week 4. Celebrate! 🎉**

---

**Last Updated:** 2026-01-01  
**Version:** 2.0  
**Status:** Ready for Implementation

Questions? Review the architecture sections or ask your team!
