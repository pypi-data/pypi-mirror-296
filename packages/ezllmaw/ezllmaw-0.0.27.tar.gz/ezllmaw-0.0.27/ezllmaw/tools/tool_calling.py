from pydantic import BaseModel

def ollama_tools(pydantic_func:BaseModel):
    
    schema = pydantic_func.model_json_schema()
    ref_key = schema["$defs"]
    base = {"type": "function"}
    function = {
        "function": {
        "name": schema["title"],
        "description": schema["description"],
        }
    }
    
    parameters = {
        "parameters": {
            "type": schema["type"],
            "required": schema["required"]
        }
    }

    def ref_logic(v):
        if "title" in v:
            v.pop("title")
            return v
        if "allOf" in v:
            allof = v.pop("allOf")
            allof = allof[0]['$ref'].split("/")[-1]
            allof = ref_key[allof]
            allof.pop("title")
            v.update(allof)
            return v
        return v
    
    properties = {
        "properties": {
            k: ref_logic(v)
            for k, v in schema["properties"].items()
        }
    }
    parameters["parameters"].update(properties)
    function.update(parameters)
    base.update(function)
    return base