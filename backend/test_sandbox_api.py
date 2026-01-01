import urllib.request
import json
import sys

BASE_URL = "http://localhost:8000"

def test_sandbox():
    print(f"Testing Sandbox Agent at {BASE_URL}...")
    
    payload = {
        "prompt": "Create a login card"
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/api/sandbox/generate",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        print("Sending request to LLM (this may take a few seconds)...")
        with urllib.request.urlopen(req) as response:
            print(f"Status: {response.status}")
            data = json.loads(response.read().decode('utf-8'))
            
            if response.status != 200:
                print(f"FAILED: API returned non-200. Response: {data}")
                return

            if data.get("status") == "error":
                print(f"FAILED: Agent returned error: {data.get('message')}")
                return

            print("\n--- Generated Design ---")
            print(json.dumps(data.get("design"), indent=2))
            
            print("\n--- Generated Code ---")
            print(data.get("code"))
            
            print("\n--- Metadata ---")
            print(f"Tokens Used: {data.get('tokens_used')}")
            
            if data.get("code") and "<Container" in data.get("code"):
                 print("\n✅ SUCCESS: Sandbox Agent generated valid code.")
            else:
                 print("\n⚠️ WARNING: Code might vary based on LLM output, but response was received.")

    except urllib.error.URLError as e:
        print(f"\n❌ FAILED: Could not connect to {BASE_URL}. Is Docker running? Error: {e}")
    except Exception as e:
        print(f"\n❌ FAILED: Unexpected error: {e}")

if __name__ == "__main__":
    test_sandbox()
