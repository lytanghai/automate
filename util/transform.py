import json
import re

def convert_log_to_json(log_string):
    try:
        match = re.search(r'body:({.*?})', log_string)
        if match:
            json_str = match.group(1)
            json_data = json.loads(json_str)
            return json_data
        else:
            return None 

    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the log string.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
