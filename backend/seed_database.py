import urllib.request
import json
import sys

BASE_URL = "http://localhost:8000"

def seed_database():
    print(f"Seeding database at {BASE_URL}...")
    
    payload = {
        "name": "Seeded Design System",
        "tokens": {
            "colors": [
                {"name": "primary/500", "value": "#3B82F6"},
                {"name": "neutral/100", "value": "#F3F4F6"},
                {"name": "neutral/900", "value": "#111827"}
            ],
            "typography": [
                 {"name": "body/md", "fontFamily": "Inter", "fontSize": 16, "fontWeight": 400}
            ],
            "spacing": [
                 {"name": "spacing/4", "value": "1rem"}
            ]
        },
        "components": [
             {"name": "Button", "id": "seed-btn"},
             {"name": "Container", "id": "seed-container"},
             {"name": "Text", "id": "seed-text"},
             {"name": "Input", "id": "seed-input"}
        ]
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/api/design-system/ingest",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                print("✅ Database seeded successfully!")
                print(f"Design System ID: {data.get('design_system_id')}")
                print(f"Version: {data.get('version')}")
            else:
                print(f"❌ Failed to seed database. Status: {response.status}")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")

if __name__ == "__main__":
    seed_database()
