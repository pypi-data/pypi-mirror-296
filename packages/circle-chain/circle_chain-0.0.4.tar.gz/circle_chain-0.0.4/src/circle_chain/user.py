import os
from typing import Any

from circle_chain.common import build_url_template, get_session_path, http_json_get, http_json_post


def send_register_verify_code(request: Any, timeout: int=30000):
    """
    send register verify code\n
    the request data:\n
    { 'email': 'test@gmail.com' }\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' }\n
    :param request: the request
    :param timeout: the timeout for the api
    :return: dict[str:Any]
    """
    url = build_url_template('user', 'sendRegisterVerifyCode')
    return http_json_post(url, request, timeout)


def register(request: Any, timeout: int=30000):
    """
    register api\n
    the request data:\n
    { 'email': 'test@gmail.com', 'passwordInput1': '222222', passwordInput2: '222222', verifyCode: '333333' }\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' }\n
    :param request: the register input
    :param timeout: the timeout for the api
    :return: dict[str:Any]
    """
    url = build_url_template('user', 'register')
    return http_json_post(url, request, timeout)

def send_verify_code(request: Any, timeout: int=30000):
    """
    send login verify code\n
    the request data:\n
    { 'email': 'test@gmail.com' }\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' }\n
    :param request: the login request
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'sendVerifyCode')
    return http_json_post(url, request, timeout)

def login(request: Any, timeout: int=30000):
    """
    login api\n
    the request data:\n
    { 'email': 'test@gmail.com', 'password': '333333' }\n
    the return data:\n
    { 'status': 200, 'data': login_info, 'message': 'success' }\n
    login_info data:\n
    { 'userId':'<userId>', 'sessionKey':'<sessionKey>', }\n
    :param request: the login request
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'login')
    response = http_json_post(url, request, timeout)
    if response['status'] == 200:
        session_key = response['data']['sessionKey']
        user_id = response['data']['userId']
        email = request.get('email')
        phone = request.get('phone')
        save_login_info({
            "userId": user_id,
            "sessionKey": session_key,
            "email": email,
            "phone": phone
        })
    return response

def save_login_info(login_info: dict[str,Any]):
    """
    save the login info in session path file.\n
    the login_info:\n
    { 'userId':'<userId>', 'sessionKey':'<sessionKey>', 'email':'<email>', 'phone':'<phone>', }\n
    :param login_info: the login info
    :return: true: success
    """
    session_path = get_session_path()
    home = os.environ['HOME']
    full_path = home + '/' + session_path
    session_dir = os.path.dirname(full_path)
    if not os.path.exists(session_dir):
        os.mkdir(session_dir)

    user_id = login_info['userId']
    session_key = login_info['sessionKey']
    user_key = 'email'
    user_value = ''
    user_type = 1
    if 'phone' in login_info:
        user_type = 0
        user_key = 'phone'
        user_value = login_info['phone']
    if 'email' in login_info:
        user_type = 1
        user_key = 'email'
        user_value = login_info['email']

    content = f"###### user login information\nuserType={user_type}\nuserId={user_id}\nsessionKey={session_key}\n{user_key}={user_value}"
    with open(full_path, 'w') as f:
        f.write(content)

    return True

def logout(timeout: int=30000):
    url = build_url_template('user', 'logout')
    return http_json_post(url, {}, timeout)

def send_pay_verify_code(request: Any, timeout: int=30000):
    """
    send pay password verify code\n
    the request data:\n
    { 'email': 'test@gmail.com' }\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' }
    :param request: the request
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'sendPayVerifyCode')
    return http_json_post(url, request, timeout)

def set_pay_password(request: Any, timeout: int=30000):
    """
    set pay password api\n
    the request data:\n
    { 'account': account, 'verifyCode':'222222', 'password':'333333' }\n
    account data:\n
    { 'email': 'test@gmail.com' }\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' } or \n
    { 'status': 200, 'data': false, 'message': 'success' }\n
    :param request: the request
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'setPayPassword')
    return http_json_post(url, request, timeout)

def have_pay_password(timeout: int=30000):
    """
    check the user whether set the pay password\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' } or \n
    { 'status': 200, 'data': false, 'message': 'success' }\n
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'havePayPassword')
    return http_json_get(url, {}, timeout)

def send_reset_password_verify_code(request: Any, timeout: int=30000):
    """
    send reset login password verify code\n
    the request data:\n
    { 'email': 'test@gmail.com' }\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' }\n
    :param request: the request
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'sendResetPasswordVerifyCode')
    return http_json_post(url, request, timeout)

def reset_password(request: Any, timeout: int=30000):
    """
    reset the login password\n
    the request data:\n
    { 'account': account, 'verifyCode':'222222', 'password1':'333333', 'password2':'333333' }\n
    account data:\n
    { 'email': 'test@gmail.com' }\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' }\n
    :param request: the request
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'resetPassword')
    return http_json_post(url, request, timeout)

def add_contacts(request: Any, timeout: int=30000):
    """
    add contacts\n
    the request data:\n
    {\n
      'email':'<email>', 'name':'<name>', 'sex':1,\n
      'icon':'<icon>', 'address':'<address>',\n
      'description':'<description>',
    }\n
    sex: 1 male, 0 female\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' }\n
    :param request: the request
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'addContacts')
    return http_json_post(url, request, timeout)

def list_contacts(timeout: int=30000):
    """
    list the user's contacts\n
    return data:\n
    { 'status': 200, 'data': contacts, 'message': 'success' }\n
    contacts:\n
    [{\n
      'email':'<email>', 'name':'<name>', 'sex':1,\n
      'icon':'<icon>', 'address':'<address>',\n
       description':'<description>'
    }]
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'listContacts')
    return http_json_get(url, {}, timeout)

def save_or_update_user_info(request: Any, timeout: int=30000):
    """
    save or update the user info\n
    return data:\n
    { 'status': 200, 'data': true, 'message': 'success' }\n
    :param request: the request
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'saveOrUpdateUserInfo')
    return http_json_post(url, request, timeout)

def user_info(timeout: int=30000):
    """
    get the user info\n
    return data: \n
    { 'status': 200, 'data': user_info, 'message': 'success' }\n
    userinfo data:\n
    {
      'userId':'<userId>', 'name':'<name>', 'address':'<address>',\n
      'sex':1, 'email':'<email>', 'icon':'<icon>', 'motherLang':'<motherLang>',\n
      'wechat':'<wechat>', 'entWechat':'<entWechat>', 'dingtalk':'<dingtalk>'
    }
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('user', 'userInfo')
    return http_json_get(url, {}, timeout)


