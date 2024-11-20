import json
def read_cookies_from_json(json_file):
    with open(json_file, 'r') as cookie_file:
        return json.load(cookie_file)