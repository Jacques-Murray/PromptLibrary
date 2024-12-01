from typing import Dict, List, Optional, Union, Any
import json

class SchemaProperty:
    """Represents a property in a JSON schema"""
    def __init__(self, type_: str, description: str, 
                 enum: Optional[List[str]] = None,
                 items: Optional[Dict] = None,
                 properties: Optional[Dict] = None):
        self.type = type_
        self.description = description
        self.enum = enum
        self.items = items
        self.properties = properties

    def to_dict(self) -> Dict:
        """Convert the property to a dictionary representation"""
        result = {
            "type": self.type,
            "description": self.description
        }
        if self.enum is not None:
            result["enum"] = self.enum
        if self.items is not None:
            result["items"] = self.items
        if self.properties is not None:
            result["properties"] = self.properties
        return result

class Schema:
    """Represents a JSON schema for a function"""
    def __init__(self, name: str, description: str, properties: Dict[str, SchemaProperty],
                 required: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.properties = properties
        self.required = required or list(properties.keys())

    def to_dict(self) -> Dict:
        """Convert the schema to a dictionary representation"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "required": self.required,
                "properties": {
                    name: prop.to_dict() 
                    for name, prop in self.properties.items()
                }
            }
        }

    def to_json(self, indent: int = 2) -> str:
        """Convert the schema to a JSON string"""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Schema':
        """Create a Schema instance from a dictionary"""
        name = data["name"]
        description = data["description"]
        params = data["parameters"]
        properties = {}
        
        for prop_name, prop_data in params["properties"].items():
            prop_type = prop_data["type"]
            prop_desc = prop_data.get("description", "")
            prop_enum = prop_data.get("enum")
            prop_items = prop_data.get("items")
            prop_props = prop_data.get("properties")
            
            properties[prop_name] = SchemaProperty(
                prop_type, prop_desc, prop_enum, prop_items, prop_props
            )
        
        required = params.get("required", list(properties.keys()))
        return cls(name, description, properties, required)

# Meta-schema for function definitions
FUNCTION_META_SCHEMA = {
    "type": "object",
    "required": ["name", "description", "parameters"],
    "properties": {
        "name": {
            "type": "string",
            "description": "Name of the function"
        },
        "description": {
            "type": "string",
            "description": "Description of what the function does"
        },
        "parameters": {
            "type": "object",
            "required": ["type", "properties"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["object"],
                    "description": "Type of the parameters object"
                },
                "required": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of required parameter names"
                },
                "properties": {
                    "type": "object",
                    "description": "Object containing parameter definitions"
                }
            }
        }
    }
}
