from pydantic import Field, BaseModel, root_validator, model_validator
from typing import Optional
from functools import partial
import ezllmaw as ez

def _Field(desc=None, prefix="", field_type="", require=True, default="", format_instructions=None, format=None, pydantic_obj=None):
    json_schema_extra = {}
    json_schema_extra["field_type"] = field_type
    json_schema_extra["prefix"] = prefix
    json_schema_extra["format"] = format
    json_schema_extra["format_instructions"] = format_instructions
    if field_type=="input":
        return Field(..., required=require, description=desc,json_schema_extra=json_schema_extra)
    else:
        return Field(required=require, description=desc,json_schema_extra=json_schema_extra, default=default)

InputField = partial(_Field, field_type="input")
OutputField = partial(_Field, field_type="output")

class Agent(BaseModel):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, 'input_prompt', self.as_prompt)
        self.initialize()

    def initialize(self):
        # Custom initialization logic
        return self()
    
    def __call__(self, **kwargs):
        self.update_attributes(**kwargs)
        return self.forward(**kwargs)

    def update_attributes(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def output_prompt(self):
        return self.as_prompt
    
    @property
    def as_prompt(self):
        prompt = f"""{self.__doc__.strip().replace("    ", "")}\n\n"""
        model_fields = self.model_fields
        model_dict = self.model_dump()
        for k, v in model_dict.items():
            json_schema_extra = model_fields[k].json_schema_extra
            if json_schema_extra["field_type"] == "output":
                if json_schema_extra["format_instructions"] is not None:
                    pydantic_obj = self.get_pydantic_obj
                    if pydantic_obj is not None:
                        prompt += "Format Instruction: "
                        # prompt += f"IMPORTANT!!"
                        prompt += f"This is the most important for the user becuase the user will use this data format in the work. "
                        prompt += f"Strictly return the {k} as JSON format with only the following field:\n\n```json\n"
                        prompt += f"""{pydantic_obj().model_dump_json()}"""
                        prompt += f"\n```\n"
                    else:
                        pass
        
            prompt += f"""{k}: \n\n{v}\n\n"""
        return prompt
    
    def _set_output(self, output):
        """Limitation: One agent must have only one output field"""
        model_fields = self.model_fields
        model_dict = self.model_dump()
        for k, v in model_dict.items():
            json_schema_extra = model_fields[k].json_schema_extra
            if json_schema_extra["field_type"] == "output":
                setattr(self, k, output)

    def log(self, **kwargs):
        pass

    def forward(self, **kwargs):
        self.log(**kwargs)
        try:
            response = ez.settings.lm(self.as_prompt)
        except TypeError as e:
            raise TypeError(f"""{e}. Set your language model first: ez.configure(lm=<your-lm>)""")
        self._set_output(response)
        return self

    @property
    def get_pydantic_obj(self):
        pydantic_obj = None
        model_fields = self.model_fields
        model_dict = self.model_dump()
        for k, v in model_dict.items():
            json_schema_extra = model_fields[k].json_schema_extra
            if json_schema_extra["field_type"] == "output":
                format_instructions = json_schema_extra["format_instructions"]
                if issubclass(format_instructions, BaseModel):
                    pydantic_obj = format_instructions
        return pydantic_obj

    def as_pydantic(self, pydantic_obj=None):
        if pydantic_obj is None:
            pydantic_obj = self.get_pydantic_obj
            if pydantic_obj is None:
                raise ValueError("pydantic_obj was missing. Initiate it with .as_pydantic(pydantic_obj=<your-pydantic-clas>) or create method pydantic_obj inside the agent.")
        model_fields = self.model_fields
        model_dict = self.model_dump()
        for k, v in model_dict.items():
            json_schema_extra = model_fields[k].json_schema_extra
            if json_schema_extra["field_type"] == "output":
                output = getattr(self, k)
        json_format = ez.JsonParser()(output)
        return pydantic_obj(**json_format)