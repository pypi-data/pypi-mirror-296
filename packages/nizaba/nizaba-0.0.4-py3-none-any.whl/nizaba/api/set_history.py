import os
import requests
import json

from datetime import datetime

def set_history(data, tags = []):
    
    NZB_API_KEY = os.getenv("NZB_API_KEY")

    headers = {"Authorization": NZB_API_KEY}
    request_data = {
        "data": json.dumps(data),
        "tags": tags,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        response = requests.post("https://api.nizaba.com/api/set_history", headers=headers, json=request_data)
        
        if response.status_code != 200:
            print(f"Error: {response.text}", response.status_code)
            print(f"Request data: {request_data}")
            return
        
    except Exception as e:
        print(f"Error: {e}")
        return