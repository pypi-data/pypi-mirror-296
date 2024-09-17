import json

# parser still broken for some answer find the way to debug it later.

class JsonParser:
    def __init__(self,):
        pass
    def __call__(self, text):
        return self.forward(text)

    def _add_bracket(self, text):
        """{"property": [{"abc":"def"}]"""
        try:
            text = text+"{" if not text.startswith("{") else text
            text = text+"}" if not text.endswith("}") else text
            text = json.loads(text, strict=False)
        except:
            pass
        return text

    def _add_double_quotes_in_property(self, text):
        """[{'abc':"def"}] or [{abc:"def"}]"""
        try:
            text = json.loads(text.replace("'", '"'), strict=False)
        except:
            pass
        return text

    def _add_double_quotes_in_value(self, text):
        """[{"abc":'def'}] or [{"abc":def}]"""
        try:
            # text = json.loads(text.replace("'", '"'))
            pass
        except:
            pass
        return text
    
    def _cleaning_logic(self, text):
        text = text.split("```json")[-1].split("```")[0]
        text = text.lstrip("\n").rstrip("\n")
        text = text.replace('""', '"')
        return text
    
    def forward(self, text):
        text = self._cleaning_logic(text)
        try:
            text = json.loads(text, strict=False)
        except json.JSONDecodeError as e:
            if "Expecting ',' delimiter" in str(e):
                print("WARNING!", e)
                text = self._add_bracket(text)
            if "Expecting property name enclosed in double quotes" in str(e):
                print("WARNING!", e)
                text = self._add_double_quotes_in_property(text)
            if "Expecting value" in str(e):
                print("WARNING!", e)
                text = self._add_double_quotes_in_value(text)
        return text