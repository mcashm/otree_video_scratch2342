import requests  # pip3 install requests
from pprint import pprint


GET = requests.get
POST = requests.post

# if using Heroku, change this to https://YOURAPP.herokuapp.com
SERVER_URL = 'http://localhost:8000'
REST_KEY = 'demo'  # fill this later

def call_api(method, *path_parts, **params) -> dict:
    path_parts = '/'.join(path_parts)
    url = f'{SERVER_URL}/api/{path_parts}'
    print(f"calling api at {url}")
    resp = method(url, json=params, headers={'otree-rest-key': REST_KEY})
    if not resp.ok:
        msg = (
            f'Request to "{url}" failed '
            f'with status code {resp.status_code}: {resp.text}'
        )
        raise Exception(msg)
    return resp.json()
