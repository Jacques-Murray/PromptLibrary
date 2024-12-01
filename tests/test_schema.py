import pytest
from promptlibrary.schema import Schema, SchemaProperty, FUNCTION_META_SCHEMA
import json

def test_schema_property_basic():
    """Test basic SchemaProperty creation and serialization"""
    prop = SchemaProperty(
        type_="string",
        description="A test property"
    )
    prop_dict = prop.to_dict()
    
    assert prop_dict["type"] == "string"
    assert prop_dict["description"] == "A test property"
    assert "enum" not in prop_dict
    assert "items" not in prop_dict
    assert "properties" not in prop_dict

def test_schema_property_with_enum():
    """Test SchemaProperty with enum values"""
    prop = SchemaProperty(
        type_="string",
        description="A test enum property",
        enum=["option1", "option2", "option3"]
    )
    prop_dict = prop.to_dict()
    
    assert prop_dict["type"] == "string"
    assert prop_dict["enum"] == ["option1", "option2", "option3"]

def test_schema_property_with_items():
    """Test SchemaProperty with array items"""
    item_schema = {
        "type": "string",
        "description": "An array item"
    }
    prop = SchemaProperty(
        type_="array",
        description="A test array property",
        items=item_schema
    )
    prop_dict = prop.to_dict()
    
    assert prop_dict["type"] == "array"
    assert prop_dict["items"] == item_schema

def test_schema_basic():
    """Test basic Schema creation and serialization"""
    schema = Schema(
        name="test_function",
        description="A test function schema",
        properties={
            "param1": SchemaProperty(type_="string", description="First parameter"),
            "param2": SchemaProperty(type_="number", description="Second parameter")
        }
    )
    schema_dict = schema.to_dict()
    
    assert schema_dict["name"] == "test_function"
    assert schema_dict["description"] == "A test function schema"
    assert "parameters" in schema_dict
    assert schema_dict["parameters"]["type"] == "object"
    assert len(schema_dict["parameters"]["properties"]) == 2
    assert "param1" in schema_dict["parameters"]["properties"]
    assert "param2" in schema_dict["parameters"]["properties"]

def test_schema_from_dict():
    """Test creating Schema from dictionary"""
    schema_dict = {
        "name": "test_function",
        "description": "A test function",
        "parameters": {
            "type": "object",
            "required": ["param1"],
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Required parameter"
                },
                "param2": {
                    "type": "number",
                    "description": "Optional parameter"
                }
            }
        }
    }
    
    schema = Schema.from_dict(schema_dict)
    assert schema.name == "test_function"
    assert schema.description == "A test function"
    assert len(schema.properties) == 2
    assert schema.required == ["param1"]

def test_schema_with_nested_objects():
    """Test Schema with nested object properties"""
    schema = Schema(
        name="create_user",
        description="Create a new user",
        properties={
            "user": SchemaProperty(
                type_="object",
                description="User information",
                properties={
                    "name": {
                        "type": "string",
                        "description": "User's name"
                    },
                    "age": {
                        "type": "number",
                        "description": "User's age"
                    }
                }
            )
        }
    )
    schema_dict = schema.to_dict()
    
    assert "user" in schema_dict["parameters"]["properties"]
    user_prop = schema_dict["parameters"]["properties"]["user"]
    assert user_prop["type"] == "object"
    assert "name" in user_prop["properties"]
    assert "age" in user_prop["properties"]

def test_meta_schema_validity():
    """Test that FUNCTION_META_SCHEMA is a valid JSON schema"""
    # Basic structure checks
    assert "type" in FUNCTION_META_SCHEMA
    assert FUNCTION_META_SCHEMA["type"] == "object"
    assert "required" in FUNCTION_META_SCHEMA
    assert "properties" in FUNCTION_META_SCHEMA
    
    # Required fields
    required_fields = FUNCTION_META_SCHEMA["required"]
    assert "name" in required_fields
    assert "description" in required_fields
    assert "parameters" in required_fields
    
    # Parameters structure
    params = FUNCTION_META_SCHEMA["properties"]["parameters"]
    assert params["type"] == "object"
    assert "required" in params
    assert "properties" in params["properties"]
