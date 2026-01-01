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
                available = list(self.components.keys())
                raise ValueError(f"Component '{component_type}' not in design system. Available: {available}")
            
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
