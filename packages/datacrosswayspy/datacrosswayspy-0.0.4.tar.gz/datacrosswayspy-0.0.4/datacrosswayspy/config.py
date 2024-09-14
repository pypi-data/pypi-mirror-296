_api_key = None
_base_url = None

def set_credentials(credentials):
    global _api_key, _base_url
    _api_key = credentials.get("api_key")
    _base_url = credentials.get("base_url")

def get_api_key():
    return _api_key

def get_base_url():
    return _base_url