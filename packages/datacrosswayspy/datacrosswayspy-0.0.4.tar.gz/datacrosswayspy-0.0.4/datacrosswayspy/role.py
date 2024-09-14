import json

from .utils import post_request, get_request, delete_request, patch_request
from .config import get_api_key, get_base_url

#with open("../secrets/config.json") as f:
#    config = json.load(f)
#    API_KEY = config["api_key"]
#    BASE_URL = config["base_url"]

def list():
    url = f"{get_base_url()}/api/role"
    return get_request(url)

def create(role_data):
    url = f"{get_base_url()}/api/role"
    return post_request(url, role_data)

def update(role_data):
    url = f"{get_base_url()}/api/role"
    return patch_request(url, role_data)

def delete(role_id):
    url = f"{get_base_url()}/api/role/{role_id}"
    return delete_request(url)

def get(role_id):
    url = f"{get_base_url()}/api/role/{role_id}"
    return get_request(url)