import json
import sys
import os

# Ensure backend acts as package root if running directly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from backend.rendering.universal_renderer import UniversalRenderer
except ImportError:
    try:
        from rendering.universal_renderer import UniversalRenderer
    except ImportError:
        print("Error: Could not import UniversalRenderer. Make sure you are running from the project root or backend directory.")
        sys.exit(1)

def test_renderer():
    # Mock Design System
    mock_design_system = {
        "tokens": {
            "colors": [
                {"name": "primary/500", "value": "#3B82F6"},
                {"name": "neutral/100", "value": "#F3F4F6"}
            ],
            "typography": [
                {"name": "body/md", "fontFamily": "Inter", "fontSize": 16, "fontWeight": 400}
            ],
            "spacing": [
                {"name": "spacing/4", "value": "1rem"}
            ]
        },
        "components": [
            {"name": "Container", "id": "1"},
            {"name": "Button", "id": "2"},
            {"name": "Text", "id": "3"}
        ]
    }

    # Mock Design Specification
    mock_spec = {
        "type": "Container",
        "props": {
            "background": "neutral/100",
            "padding": "spacing/4"
        },
        "children": [
            {
                "type": "Text",
                "props": {
                    "color": "primary/500"
                },
                "content": "Hello World"
            },
            {
                "type": "Button",
                "props": {
                    "variant": "primary"
                },
                "content": "Click Me"
            }
        ]
    }

    print("Initializing UniversalRenderer...")
    renderer = UniversalRenderer(mock_design_system)

    print("Rendering specification...")
    try:
        result = renderer.render_design_specification(mock_spec)
        
        print("\n--- Generated JSX ---")
        print(result["jsx"])
        
        print("\n--- Metadata ---")
        print("Tokens Used:", result["tokens_used"])
        print("Components Used:", result["components_used"])
        print("Valid:", result["valid"])

        # Expected output check (rough)
        assert "<Container" in result["jsx"]
        assert 'background="#F3F4F6"' in result["jsx"]
        assert 'padding="1rem"' in result["jsx"]
        assert "<Text" in result["jsx"]
        assert 'color="#3B82F6"' in result["jsx"]
        assert "Hello World" in result["jsx"]
        assert "<Button" in result["jsx"]
        assert "Click Me" in result["jsx"]
        
        print("\n✅ Verification Successful: Output matches expected structure.")

    except Exception as e:
        print(f"\n❌ Verification Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_renderer()
