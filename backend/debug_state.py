import urllib.request
import json

BASE_URL = "http://localhost:8000"

def check_state():
    print(f"Checking state at {BASE_URL}...")
    try:
        with urllib.request.urlopen(f"{BASE_URL}/api/design-system/latest") as response:
            if response.status != 200:
                print(f"Error: Status {response.status}")
                return
            
            data = json.loads(response.read().decode('utf-8'))
            print("\n--- Current Design System ---")
            print(f"ID: {data.get('id')}")
            print(f"Version: {data.get('version')}")
            print(f"Updated At: {data.get('updated_at')}")
            
            components = data.get("components", [])
            print(f"\nComponents ({len(components)}):")
            for c in components:
                print(f" - {c.get('name')} (id: {c.get('id')})")
                
            if any(c.get('name') == 'Container' for c in components):
                print("\n✅ 'Container' component found.")
            else:
                print("\n❌ 'Container' component NOT found.")

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        if e.code == 404:
            print("No design system found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_state()
