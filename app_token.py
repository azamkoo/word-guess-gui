# app_token.py

_token = None
_refresh_token = None
_user = None

def set_tokens(token, refresh_token):
    global _token, _refresh_token
    _token = token
    _refresh_token = refresh_token

def get_token():
    return _token

def get_refresh_token():
    return _refresh_token

def set_user(username):
    global _user
    _user = username

def get_user():
    return _user

def clear_auth():
    global _token, _refresh_token, _user
    _token = None
    _refresh_token = None
    _user = None
