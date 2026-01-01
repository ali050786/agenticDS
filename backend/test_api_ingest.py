import urllib.request
import json
import sys

BASE_URL = "http://localhost:8000"

def test_integration():
    print(f"Testing against running API at {BASE_URL}...")
    
    # 1. Ingest
    payload = {
        "name": "Integration Test System",
        "tokens": {
            "colors": [{"name": "primary", "value": "#FF0000"}],
            "typography": [],
            "spacing": []
        },
        "components": [
             {"name": "Button", "id": "123"},
             {"name": "Container", "id": "124"},
             {"name": "Text", "id": "125"},
             {"name": "Input", "id": "126"}
        ]
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/api/design-system/ingest",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Ingest Status: {response.status}")
            data = json.loads(response.read().decode('utf-8'))
            print(f"Ingest Response: {data}")
            
            if response.status != 200:
                print("FAILED: Ingest returned non-200")
                return

            design_system_id = data.get("design_system_id")
            if not design_system_id:
                print("FAILED: No design_system_id returned")
                return
                
            print(f"Design System ID: {design_system_id}")

            # 2. Get Tokens
            print("\nFetching Tokens...")
            with urllib.request.urlopen(f"{BASE_URL}/api/tokens?design_system_id={design_system_id}") as token_response:
                 print(f"Tokens Status: {token_response.status}")
                 tokens = json.loads(token_response.read().decode('utf-8'))
                 print(f"Tokens Response: {tokens}")
                 
                 if token_response.status == 200 and len(tokens.get("colors", [])) > 0:
                     if tokens["colors"][0]["name"] == "primary":
                        print("\n✅ SUCCESS: Full flow verified against running Docker container.")
                     else:
                        print("\n❌ FAILED: Token name mismatch.")
                 else:
                     print("\n❌ FAILED: Token verification failed.")

    except urllib.error.URLError as e:
        print(f"\n❌ FAILED: Could not connect to {BASE_URL}. Is Docker running? Error: {e}")
        print("Note: If Docker is running, make sure port 8000 is exposed.")
    except Exception as e:
        print(f"\n❌ FAILED: Unexpected error: {e}")

if __name__ == "__main__":
    test_integration()
