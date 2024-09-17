

from circle_chain.common import build_url_template, http_json_get, http_json_post


def subscribe(timeout: int=30000):
    """
    subscribe api\n
    the return data:\n
    { 'status': 200, 'data': base_info, 'message': 'success' }\n
    base info data: { 'baseHeight': 20000, 'ipPort': ['123.23.45.32:80'] }\n
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('node', 'subscribe')
    return http_json_get(url, {}, timeout)

def server_features(timeout: int=30000):
    """
    server features\n
    the return data: \n
    { 'status': 200, 'data': node_info, 'message': 'success' }\n
    node_info data:\n
    {\n
      'version': '1.0.0', 'role': 'CLOUDER', 'protolVersion': '0.0.1',\n
      'publicIP': '123.23.45.32', 'localIP': '192.168.1.10', 'port': 80,\n
      'baseHeight': 20000, 'heartbeatPort': 2602, 'publicKey': '',\n
      'hostname': '', 'visitCount': 0, 'createTime': 1726396260000, \n
    }\n
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('node', 'serverFeatures')
    return http_json_get(url, {}, timeout)

def broadcast_transaction(request, timeout: int=30000):
    """
    broadcast transaction\n
    the request data:\n
    {\n
      txid: string, type: 0|1|2, hash: string, version: number, size: number,\n
      vsize: number, weight: number, locktime: number, vin: Vin[], out: Vout[],\n
      blockhash: string, confirmations: number, time: number, blocktime: number,\n
    }\n
    Vin: {\n
      txid: string, vout: number, scriptSig: VinScriptSignature,\n
      sequence: number, addresses: string[], value: string\n
    }\n
    VinScriptSignature: { asm: string, hex: string }\n
    Vout: {value: string, n: number, scriptPubKey: ScriptPubKey}\n
    ScriptPubKey: {asm: string, hex: string, type: number, addresses: string[]}\n
    the return data:\n
    {
      'status': 200,\n
      'data': '3055b50d1d87ea6ade8df155d3cf45a3d570d982722f35a6f8d37813648b0a59',\n
      'message': 'success'\n
    }\n
    the data stores the transaction id.\n
    :param request: the broadcast transaction request
    :param timeout: the timeout for the api
    :return: dict[str,Any]
    """
    url = build_url_template('node', 'broadcastTransaction')
    return http_json_post(url, request, timeout)


