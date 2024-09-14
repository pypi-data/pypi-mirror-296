import json

from .utils import post_request, get_request, delete_request, patch_request
from .config import get_api_key, get_base_url

def list():
    url = f"{get_base_url()}/api/collection"
    return get_request(url)

def create(collection_data):
    url = f"{get_base_url()}/api/collection"
    return post_request(url, collection_data)

def update(collection_data):
    url = f"{get_base_url()}/api/collection"
    return patch_request(url, collection_data)

def delete(collection_id):
    url = f"{get_base_url()}/api/collection/{collection_id}"
    return delete_request(url)

def get(collection_id):
    url = f"{get_base_url()}/api/collection/{collection_id}"
    return get_request(url)

def search(search_data):
    url = f"{get_base_url()}/api/collection/search"
    return post_request(url)

