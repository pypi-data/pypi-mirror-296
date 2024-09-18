import json
import math

from json import JSONEncoder

from nizaba.api import set_history
from nizaba.lang import parse_and_build_specification

def shorten(s: str):
    if len(s) > 255 - 6:
        return s[:125] + " ... " + s[-125:]
    else:
        return s

def nan2None(obj):
    if isinstance(obj, dict):
        return {k:nan2None(v) for k,v in obj.items()}
    elif isinstance(obj, list):
        return [nan2None(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    elif 'json' in dir(obj):
        return json.loads(obj.json())
    return str(obj)

class NanConverter(JSONEncoder):
    def encode(self, obj, *args, **kwargs):
        return super().encode(nan2None(obj), *args, **kwargs)

def nzb_create(
        self
):
    
    def f(*args, **kwargs):
        
        SPEC = {}
        
        if "messages" in kwargs:
            new_messages = []
            for m in kwargs["messages"]:
                raw_text, spec = parse_and_build_specification(m["content"])
                
                for Ak, Av in spec["Annotations"].items():
                    SPEC[shorten(Ak)] = shorten(Av)
                for Vk, Vv in spec["Variables"].items():
                    SPEC[shorten(Vk)] = shorten(Vv)
                
                new_messages.append({
                    **m, 
                    "content": raw_text
                })
            
            kwargs["messages"] = new_messages
        
        print(SPEC)
        
        completion = self.chat.completions._NZB_create(*args, **kwargs)
    
        new_message = dict(completion.choices[0].message)
    
        all_messages = kwargs.get("messages", []) + [new_message]
    
        data = json.loads(json.dumps(all_messages, cls=NanConverter))

        tags = [{"key": k, "value": v} for k, v in SPEC.items()]

        set_history(data, tags=tags)
    
        return completion
    
    return f

def nzb_init(
        self, *args, **kwargs
):
    
    self._NZB__init__(*args, **kwargs)
    
    self.chat.completions._NZB_create = self.chat.completions.create
    
    self.chat.completions.create = nzb_create(self)
    
def init():
    import openai
    
    if not hasattr(openai.OpenAI, "_NZB__init__"):
        openai.OpenAI._NZB__init__ = openai.OpenAI.__init__
    
        openai.OpenAI.__init__ = nzb_init