from .providers.openai import init as openai_init

import os

def init(api_key=None):
    
    if api_key is not None:
        os.environ["NZB_API_KEY"] = api_key
    
    openai_init()