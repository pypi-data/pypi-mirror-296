
from typing import Any

from circle_chain.common import build_url_template, http_json_get, http_json_post


def create_wallet(timeout: int=30000):
    """
    create the wallet\n
    the return data:\n
    { 'status': 200, 'data': '12vU588JA4zGMA7gKDRuu3HGLrr3BxhkBt', 'message': 'success' }\n
    the data stores address value if success.\n
    :param timeout: the timeout for the api
    :return: the address
    """
    url = build_url_template('wallet', 'createWallet')
    return http_json_post(url, {}, timeout)

def list_wallet(timeout: int=30000):
    """
    list the user's all address\n
    the return data:\n
    { 'status': 200, 'data': ['12vU588JA4zGMA7gKDRuu3HGLrr3BxhkBt'], 'message': 'success' }\n
    the data stores the address array value if success.\n
    :param timeout: the timeout for the api
    :return: the address list
    """
    url = build_url_template('wallet', 'listWallet')
    return http_json_get(url, {}, timeout)

def balance_of_address(address: str, timeout: int=30000):
    """
    get the balance of the address\n
    the return data:\n
    { 'status': 200, 'data': 100000, 'message': 'success' }\n
    the data stores balance value if success.\n
    :param address: the input address
    :param timeout: the timeout for the api
    :return: balance value
    """
    url = build_url_template('wallet', 'balanceOfAddress')
    return http_json_get(url, { "address": address }, timeout)

def balance_of_wallet(timeout: int=30000):
    """
    get the balance of the wallet\n
    the return data:\n
    { 'status': 200, 'data': WalletSpentInfo[], 'message': 'success' }\n
    WalletSpentInfo:\n
    { 'address': '12vU588JA4zGMA7gKDRuu3HGLrr3BxhkBt', 'balance': 100000, 'spent': 0 }\n
    :param timeout: the timeout for the api
    :return: balance info
    """
    url = build_url_template('wallet', 'balanceOfWallet')
    return http_json_get(url, {}, timeout)

def send_to(request: Any, timeout: int=30000):
    """
    send assets to others\n
    the request data:\n
    {
      'from': '1Jhf7pUtmqK2ZqR9du7xa6uL1Qxdc14atG',\n
      'address': '1HDv7a7PqbYugZjaVJtMxvsnvpk7GS554s',\n
      'email': 'test@gmail.com',\n
      'transContent': {
        'type': 1,\n
        'uuid': 'ef98dad9-21da-4939-abc4-ecd658ac2a5b',\n
      },\n
      'payPassword': '222222',\n
    }\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' } or \n
    { 'status': 200, 'data': false, 'message': 'success' }\n
    :param request: the send to request
    :param timeout: the timeout for the api
    :return: boolean true success, false failure
    """
    url = build_url_template('wallet', 'sendTo')
    return http_json_post(url, request, timeout)

def pay(request: Any, timeout=30000):
    """
    pay balance to others\n
    the request data:\n
    {
      'from': '1Jhf7pUtmqK2ZqR9du7xa6uL1Qxdc14atG',\n
      'to': '1HDv7a7PqbYugZjaVJtMxvsnvpk7GS554s',\n
      'email': 'test@gmail.com',\n
      'value': 1000,\n
      'payPassword': '222222',\n
    }\n
    the return data:\n
    { 'status': 200, 'data': true, 'message': 'success' } or \n
    { 'status': 200, 'data': false, 'message': 'success' }\n
    :param request: the pay request
    :param timeout: the timeout for the api
    :return:
    """
    url = build_url_template('wallet', 'pay')
    return http_json_post(url, request, timeout)

def assets_of_wallet(timeout: int=30000):
    """
    get the assets of wallet\n
    the return data: \n
    { 'status': 200, 'data': assets_info, 'message': 'success' }\n
    assets_info: {'balance': 100000, 'identityNum': 0, 'ownershipNum': 2, 'walletNum': 1 }\n
    :param timeout: the timeout for the api
    :return assets' info.
    """
    url = build_url_template('wallet', 'assetsOfWallet')
    return http_json_get(url, {}, timeout)

def search_tx_by_type(tx_type: int, page_no: int, page_size: int, timeout: int=30000):
    """
    search transactions by type\n
    the return data:\n
    { 'status': 200, 'data': transaction_info[], 'message': 'success' }\n
    transaction_info data:\n
    {
      'fromAddress': '12cSSRmfLMH8s5MrxeEdtgbKWnk28Si6cr',\n
      'toAddress': '1APGzvGwcDKWDobEEDiHtEehVz4G4jWeoR',\n
      'txId': '3acdf6d7c032d1b300c45a75a440ef61ade78113f8e000d5ff005b8afac87466',\n
      'idx': 0,\n
      'txType': 0,\n
      'inOut': 'OUT',\n
      'value': '1000',\n
      'timestamp': '2024-09-15 10:00:00',
    }
    :param tx_type: the transaction type, 0 balance, 1 ownership, 2 identity
    :param page_no: the page no
    :param page_size: the page size
    :param timeout: the timeout for the api
    :return: transaction info list.
    """
    url = build_url_template('wallet', 'searchTxByType')
    return http_json_post(url, { "type": tx_type, "pageNo": page_no, "pageSize": page_size }, timeout)

def search_tx_by_time(start_time: int, end_time: int, page_no: int, page_size: int, timeout: int=30000):
    """
    search transaction by time\n
    the return data:\n
    { 'status': 200, 'data': transaction_info[], 'message': 'success' }\n
    transaction_info data:\n
    {
      'fromAddress': '12cSSRmfLMH8s5MrxeEdtgbKWnk28Si6cr',\n
      'toAddress': '1APGzvGwcDKWDobEEDiHtEehVz4G4jWeoR',\n
      'txId': '3acdf6d7c032d1b300c45a75a440ef61ade78113f8e000d5ff005b8afac87466',\n
      'idx': 0,\n
      'txType': 0,\n
      'inOut': 'OUT',\n
      'value': '1000',\n
      'timestamp': '2024-09-15 10:00:00',
    }
    :param start_time: the start time
    :param end_time: the end time
    :param page_no: the page no
    :param page_size: the page size
    :param timeout: the timeout for the api
    :return: the transaction info list.
    """
    url = build_url_template('wallet', 'searchTxByTime')
    return http_json_get(url, {
        "startTime": start_time,
        "endTime": end_time,
        "pageNo": page_no,
        "pageSize": page_size
    }, timeout)

def assets_of_address(address: str, tx_type: int, timeout: int=30000):
    """
    get assets of address\n
    the return data:\n
    { 'status': 200, 'data': address_assets_info[], 'message': 'success' }\n
    address_assets_info data:\n
    {
      'address': '12cSSRmfLMH8s5MrxeEdtgbKWnk28Si6cr',\n
      'txId': '3acdf6d7c032d1b300c45a75a440ef61ade78113f8e000d5ff005b8afac87466',\n
      'idx': 0,\n
      'type': 0,\n
      'value': '1000',
    }
    :param address: the searched address
    :param tx_type: the transaction type: 0 balance, 1 ownership, 2 identity
    :param timeout: the timeout for the api
    :return: address assets info
    """
    url = build_url_template('wallet', 'assetsOfAddress')
    return http_json_get(url, {
        "address": address,
        "type": tx_type
    }, timeout)

def let_me_try(timeout: int=30000):
    """
    let me try mine the block, and get the balance or assets.\n
    the return data:\n
    { 'status': 200, 'data': transaction_info, 'message': 'success' }\n
    transaction_info data:\n
    {
      'fromAddress': '12cSSRmfLMH8s5MrxeEdtgbKWnk28Si6cr',\n
      'toAddress': '1APGzvGwcDKWDobEEDiHtEehVz4G4jWeoR',\n
      'txId': '3acdf6d7c032d1b300c45a75a440ef61ade78113f8e000d5ff005b8afac87466',\n
      'idx': 0,\n
      'txType': 0,\n
      'inOut': 'OUT',\n
      'value': '1000',\n
      'timestamp': '2024-09-15 10:00:00',
    }
    :param timeout: the timeout for the api
    :return: transaction info
    """
    url = build_url_template('wallet', 'letMeTry')
    return http_json_post(url, {}, timeout)

def public_get_address_by_uid(uid: str, timeout: int=30000):
    """
    get the address info by uid\n
    the return data:\n
    { 'status': 200, 'data': ['1APGzvGwcDKWDobEEDiHtEehVz4G4jWeoR'], 'message': 'success' }\n
    :param uid: the user id
    :param timeout: the timeout for the api
    :return: address list
    """
    url = build_url_template('wallet', 'getAddressByUid')
    return http_json_get(url, { 'uid': uid }, timeout)

def public_get_assets_of_address(address, tx_type, timeout=30000):
    """
    get assets of the address\n
    the return data:\n
    { 'status': 200, 'data': address_assets_info[], 'message': 'success' }\n
    address_assets_info data:\n
    {
      'address': '12cSSRmfLMH8s5MrxeEdtgbKWnk28Si6cr',\n
      'txId': '3acdf6d7c032d1b300c45a75a440ef61ade78113f8e000d5ff005b8afac87466',\n
      'idx': 0,\n
      'type': 0,\n
      'value': '1000',
    }
    :param address: the searched address
    :param tx_type: the transaction type, 0 balance, 1 ownership, 2 identity
    :param timeout: the timeout for the api
    :return: address assets info
    """
    url = build_url_template('wallet', 'getAssetsOfAddress')
    return http_json_get(url, {
        "address": address,
        "type": tx_type
    }, timeout)

def public_key_from_address(address: str, timeout: int=30000):
    """
    get public key from address\n
    the return data:\n
    { 'status': 200, 'data': 'c9cb915836391cff67dcda806dcdc43469c2a8f2', 'message': 'success' }\n
    :param address: the address which provides the public key
    :param timeout: the timeout for the api
    :return: public key hash in hex string
    """
    url = build_url_template('wallet', 'pubKeyHashFromAddress')
    return http_json_get(url, { "address": address }, timeout)


def public_search_transaction(request: Any, timeout: int=30000):
    """
    search transactions\n
    the return data:\n
    { 'status': 200, 'data': transaction_info[], 'message': 'success' }\n
    transaction_info data:\n
    {
      'fromAddress': '12cSSRmfLMH8s5MrxeEdtgbKWnk28Si6cr',\n
      'toAddress': '1APGzvGwcDKWDobEEDiHtEehVz4G4jWeoR',\n
      'txId': '3acdf6d7c032d1b300c45a75a440ef61ade78113f8e000d5ff005b8afac87466',\n
      'idx': 0,\n
      'txType': 0,\n
      'inOut': 'OUT',\n
      'value': '1000',\n
      'timestamp': '2024-09-15 10:00:00',
    }
    :param request: the search request
    :param timeout: the timeout for the api
    :return: transaction info array
    """
    url = build_url_template('wallet', 'searchTransaction')
    return http_json_post(url, request, timeout)

def public_get_balance_of_address(address: str, timeout: int=30000):
    """
    get the balance of the address\n
    the return data:\n
    { 'status': 200, 'data': 100000, 'message': 'success' }\n
    the data stores balance value if success.\n
    :param address: the input address
    :param timeout: the timeout for the api
    :return: balance value
    """
    url = build_url_template('wallet', 'getBalanceByAddress')
    return http_json_get(url, {"address": address}, timeout)

