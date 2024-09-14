import json

from .utils import post_request, get_request, delete_request, patch_request
from .config import get_api_key, get_base_url


def i():
    url = f"{get_base_url()}/api/user/i"
    return get_request(url)
    
def list():
    url = f"{get_base_url()}/api/user"
    return get_request(url)
    
def get(user_id):
    url = f"{get_base_url()}/api/user/{user_id}"
    return get_request(url)
    
def files():
    url = f"{get_base_url()}/api/user/file"
    return get_request(url)

def access_keys():
    url = f"{get_base_url()}/api/user/accesskey"
    return get_request(url)
    
def create_key(exp_time):
    url = f"{get_base_url()}/api/user/accesskey/{exp_time}"
    return post_request(url)

def create(user_information):
    url = f"{get_base_url()}/api/user"
    return post_request(url, data=user_information)

def create_list(user_information_list):
    url = f"{get_base_url()}/api/user/bulk"
    return post_request(url, data=user_information_list)

def update(user_information):
    url = f"{get_base_url()}/api/user"
    return patch_request(url, data=user_information)

def delete(user_id):
    url = f"{get_base_url()}/api/user/{user_id}"
    return delete_request(url)

def logs(user_id, offset=0, limit=20):
    endpoint_url = f"{get_base_url()}/api/user/log/{user_id}"
    params = {
        'offset': offset,
        'limit': limit
    }
    return get_request(endpoint_url, params=params)
