import json

from .utils import post_request, get_request, delete_request
from .config import get_api_key, get_base_url


def list():
    url = f"{get_base_url()}/api/policy"
    return get_request(url)

def create(policy_data):
    url = f"{get_base_url()}/api/policy"
    return post_request(url, policy_data)

def delete(policy_id):
    url = f"{get_base_url()}/api/policy/{policy_id}"
    return delete_request(url)

def get(policy_id):
    url = f"{get_base_url()}/api/policy/{policy_id}"
    return get_request(url)