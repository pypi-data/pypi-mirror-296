import os

import requests
import yaml

g_config = None

def load_config():
    """
    load configure
    :return: the configure dictionary
    """
    global g_config
    if g_config is not None:
        return g_config

    with open(os.path.dirname(__file__) + '/config.yml', 'r') as f:
        g_config = yaml.load(f, Loader=yaml.SafeLoader)
    
    return g_config

def get_access_key():
    """
    get the access key for the login user
    :return: the access key
    """
    session_path = get_session_path()
    home = os.environ['HOME']
    full_path = home + '/' + session_path
    session_dir = os.path.dirname(full_path)
    if not os.path.exists(session_dir):
        os.mkdir(session_dir)
        return None

    if not os.path.exists(full_path):
        return None

    with open(full_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith('sessionKey='):
            return line.replace('sessionKey=', '').strip('\n')

    return None

def http_json_get(url: str, params, timeout: int):
    """
    http get with `application/json` content type.
    :param url: the url string
    :param params: the params
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    access_key = get_access_key()
    headers = {
        "Content-Type": "application/json",
        "AuthorizationV2": access_key
    }
    try:
        response = requests.get(url=url, params=params, timeout=timeout, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(error)
        return {
            "status": error.errno,
            "message": error.strerror
        }


def http_json_post(url: str, data, timeout: int):
    """
    http post data with `application/json` content type.
    :param url: the url string
    :param data: the post data
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    access_key = get_access_key()
    headers = {
        "Content-Type": "application/json",
        "AuthorizationV2": access_key
    }
    try:
        response = requests.post(url=url, json=data, timeout=timeout, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print(error)
        return {
            "status": error.errno,
            "message": error.strerror
        }


def build_url_template(biz: str, path: str):
    """
    build the url with parameters
    :param biz: the business key
    :param path: the relative path
    :return: the whole url
    """
    config = load_config()
    http_config = config['http']
    return http_config['protocol'] + '://' + http_config['host'] + config[biz]['path'][path]


def get_session_path():
    """
    get the session path
    :return: the session path
    """
    config = load_config()
    return config['user']['sessionPath']
