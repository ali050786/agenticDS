from typing import Dict, Any, List, Optional
import json
import os
from langchain_openai import ChatOpenAI
from rendering.universal_renderer import UniversalRenderer

class SandboxAgent:
    """
    Generates new screen designs from text prompts
    Constrained to use ONLY design system tokens and components
    """

    def __init__(self, design_system: Dict[str, Any]):
        self.design_system = design_system
        self.renderer = UniversalRenderer(design_system)
        
        # Use OpenRouter
        api_key = os.getenv("OPENROUTER_API_KEY") 
        # Fallback to OpenAI key if OpenRouter not explicit
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        
        # If still no key, use a placeholder to pass Pydantic validation
        # (OpenRouter free models might work, or it will fail with 401 later which is better than crash)
        if not api_key:
            api_key = "sk-or-v1-placeholder"

        self.llm = ChatOpenAI(
            model="tngtech/deepseek-r1t2-chimera:free",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
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

Return ONLY valid JSON, no other text. Do not wrap in markdown code blocks.

JSON Schema:
{{
  "type": "Container",
  "props": {{"background": "color-token-or-value"}},
  "children": [
    {{
      "type": "AnotherAvailableComponent",
      "props": {{"variant": "primary"}},
      "content": "Text content"
    }}
  ]
}}
"""

        # Generate design specification
        response = await self.llm.apredict(constraint_prompt)
        
        print(f"DEBUG LLM RESPONSE: {response}")
        
        # Robust JSON cleaning: extract substring from first { to last }
        clean_response = response.strip()
        start_idx = clean_response.find("{")
        end_idx = clean_response.rfind("}")
        
        if start_idx != -1 and end_idx != -1:
            clean_response = clean_response[start_idx : end_idx + 1]
        else:
            # Fallback to simple strip if braces not found (unlikely for valid JSON)
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.startswith("```"):
                clean_response = clean_response[3:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            
        try:
            design_spec = json.loads(clean_response)
        except json.JSONDecodeError as e:
            # Fallback/Error handling
            return {
                "status": "error",
                "message": f"Failed to parse LLM response: {e}",
                "raw_response": response
            }

        # Validate against design system
        try:
            self.renderer.validate_specification(design_spec)
        except ValueError as e:
             return {
                "status": "error",
                "message": f"Validation failed: {e}",
                "design": design_spec
            }
        
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
