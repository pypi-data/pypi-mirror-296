from pydantic import BaseModel

def pydantic_instructions(pydantic_obj:BaseModel):
    prompt = ""
    prompt += "Format Instruction: "
    # prompt += f"IMPORTANT!!"
    prompt += f"This is the most important for the user becuase the user will use this data format in the work. "
    prompt += f"Strictly return the output as JSON format with only the following field:\n\n```json\n"
    prompt += f"""{pydantic_obj().model_dump_json()}"""
    prompt += f"\n```\n"
    return prompt