

from circle_chain.common import build_url_template, http_json_get


def get_block_hashlist(base_height: int, timeout: int=30000):
    """
    get block hash list\n
    the return data:\n
    {
      'status': 200,\n
      'data': ['00000007753a949830211b0683efe9b687a4305cd203b00718508789faf3974a'],\n
      'message': 'success'
    }\n
    :param base_height: the base height
    :param timeout: the timeout for the api
    :return: the hash list
    """
    url = build_url_template('block', 'blockchainHashListPath')
    return http_json_get(url, { "baseHeight": base_height }, timeout)

def get_block(hash_str: str, timeout: int=30000):
    """
    get block data\n
    the return data:\n
    {
      'status': 200,\n
      'data': block,\n
      'message': 'success'
    }\n
    block data:\n
    {
      'header': {
        'hash': string,\n
        'minedTimestamp': string,\n
        'version': string,\n
        'height': number,\n
        'prevBlockHash': string,\n
        'merkleTreeRoot': string,\n
        'minerIpPort': string,\n
        'minerInfo': string,\n
        'timeStamp': number,\n
        'difficulty': number,\n
        'nonce': number,\n
      },\n
      'dataHexStr': string,
    }
    :param hash_str: the block hash
    :param timeout: the timeout for the api
    :return: the block
    """
    url = build_url_template('block', 'blockchainPath')
    return http_json_get(url, { "hash": hash_str}, timeout)

def get_block_header_list(base_height: int, timeout: int=30000):
    """
    get the block header list\n
    the return data:\n
    {
      'status': 200,\n
      'data': block_header,\n
      'message': 'success'
    }\n
    block_header:\n
    {
      'hash': string,\n
      'minedTimestamp': string,\n
      'version': string,\n
      'height': number,\n
      'prevBlockHash': string,\n
      'merkleTreeRoot': string,\n
      'minerIpPort': string,\n
      'minerInfo': string,\n
      'timeStamp': number,\n
      'difficulty': number,\n
      'nonce': number,\n
    }\n
    :param base_height: the base height
    :param timeout: the timeout for the api
    :return: the block header list
    """
    url = build_url_template('block', 'blockchainHeaderListPath')
    return http_json_get(url, { "baseHeight": base_height }, timeout)

def get_block_data(hash_str: str, timeout: int=30000):
    """
    get block data\n
    the return data:\n
    the return data:\n
    {
      'status': 200,\n
      'data': '<block data in hex string>',\n
      'message': 'success'\n
    }\n
    :param hash_str: the block hash
    :param timeout: the timeout for the api
    :return: the block data
    """
    url = build_url_template('block', 'blockchainDataPath')
    return http_json_get(url, { "hash": hash_str}, timeout)

def get_blocktails_hashlist(base_height: int, timeout: int=30000):
    """
    get the blocktails hash list\n
    the return data:\n
    {
      'status': 200,\n
      'data': ['00000007753a949830211b0683efe9b687a4305cd203b00718508789faf3974a'],\n
      'message': 'success'
    }\n
    :param base_height: the base height
    :param timeout: the timeout for the api
    :return: the blocktails hash list
    """
    url = build_url_template('block', 'blockchainTailsHashListPath')
    return http_json_get(url, { "baseHeight": base_height }, timeout)

def get_blocktails_po(hash_str: str, timeout: int=30000):
    """
    get blocktails by hash\n
    the return data:\n
    {
      'status': 200,\n
      'data': blocktails_po,\n
      'message': 'success'
    }\n
    blocktails_po:\n
    {
      'height': 106692,\n
      'hash': '00000007753a949830211b0683efe9b687a4305cd203b00718508789faf3974a',\n
      'hashCrc32': 12324,\n
      'prevHash': '00000006e7ebf7aa563701d3fe04b6e32416929a1426d287a394b62ffe867436',\n
      'isMaster': 1,\n
    }
    :param hash_str: the block hash
    :param timeout: the timeout for the api
    :return: the block tails object
    """
    url = build_url_template('block', 'blockchainTailsPOPath')
    # print('url:', url)
    return http_json_get(url, { "hash": hash_str}, timeout)

def get_tx_by_txid(tx_id: str, timeout: int=30000):
    """
    get transaction by txid
    :param tx_id: the transaction id
    :param timeout: the timeout for the api
    :return: transaction detail
    """
    url = build_url_template('block', 'transactionByTxIdPath')
    return http_json_get(url, { "txId": tx_id}, timeout)

def search_tx_by_txid(tx_id: str, timeout: int=30000):
    """
    search transaction by txid
    :param tx_id: the transaction id
    :param timeout: the timeout for the api
    :return: the transaction detail list
    """
    url = build_url_template('block', 'searchTxByTxIdPath')
    # print('url:', url)
    return http_json_get(url, { "txId": tx_id}, timeout)

def search_tx_by_address(address: str, tx_id: str, limit: int, timeout: int=30000):
    """
    search transaction by address and tx_id
    :param address: the address
    :param tx_id: the transaction id
    :param limit: the limit page
    :param timeout: the timeout for the api
    :return: address tx info list
    """
    url = build_url_template('block', 'searchTxByAddressPath')
    return http_json_get(url, { "txId": tx_id, "address": address, "limit": limit}, timeout)

def search_utxos(address: str, tx_id: str, limit: int, timeout: int=30000):
    """
    search utxos
    :param address: the address
    :param tx_id:  the transaction id
    :param limit: the limit page
    :param timeout: the timeout for the api
    :return: the utxos.
    """
    url = build_url_template('block', 'searchUTXOsPath')
    return http_json_get(url, { "txId": tx_id, "address": address, "limit": limit}, timeout)

