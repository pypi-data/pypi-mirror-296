# Circle Chain 
## build & install
build the project please input the following command:

```shell
python3 -m build
pip3 install --index-url https://test.pypi.org/simple/ circle_chain
```
then upload to pypi:

```shell
twine upload dist/*
```


## Install

```shell
pip install circle-chain
```

## Usage

### register and login or login with verify code

```python
# 1. first register and login or login with verify code
## option1: register and login
from circle_chain.user import send_register_verify_code,register,login,send_verify_code
response = send_register_verify_code({ "email": "<your-email>" })
if response['status'] != 200:
    raise Exception(response['message'])
# receive the register verify code in your email
response = register({
    "email": "<your-email>",
    "passwordInput1": "111111",
    "passwordInput2": "111111",
    "verifyCode": "222222"
})
if response['status'] != 200:
    raise Exception(response['message'])
    
# now login with password
response = login({
    "email": "<your-email>",
    "password": "111111",
})
if response['status'] != 200:
    raise Exception(response['message'])
# now user login success
## option2: login with verify code
response = send_verify_code({ "email": "<your-email>" })
if response['status'] != 200:
    raise Exception(response['message'])
# receive login verify code in your email
response = login({
    "email": "<your-email>",
    "verifyCode": "111111",
})
if response['status'] != 200:
    raise Exception(response['message'])
# now user login success
## for you login, option1 and option2 are ok, you just select one.
```

### Wallet functions

```python
from circle_chain.wallet import create_wallet,list_wallet,assets_of_wallet
response = create_wallet()
if response['status'] != 200:
    raise Exception(response['message'])
# get the address created
address = response['data']
response = list_wallet()
if response['status'] != 200:
    raise Exception(response['message'])
# get address list
address_list = response['data']
response = assets_of_wallet()
if response['status'] != 200:
    raise Exception(response['message'])
# the asset info of wallet
data = response['data']
```

### set pay password

```py
from circle_chain.user import send_pay_verify_code, set_pay_password
response = send_pay_verify_code({ "email": "<your-email>" })
if response['status'] != 200:
    raise Exception(response['message'])
# receive the pay verify code in your email
response = set_pay_password({
    "account": {
        "email": "test@gmail.com"
    },
    "password": "333333",
    "verifyCode": "112222"
})
if response['status'] != 200:
    raise Exception(response['message'])
# now your pay password is set success
```

### Transactions

```py
from circle_chain.wallet import send_to, pay
from_address = '1L8eRrBuWnBxcQ6DKCDkkPM7ozxDcmpho1'
to = '14hF1BynFVnBEFKxyo51FHmJksVwfxg4sg'
# send asset from `1L8eRrBuWnBxcQ6DKCDkkPM7ozxDcmpho1` to `14hF1BynFVnBEFKxyo51FHmJksVwfxg4sg`
response = send_to({
    'email': 'test@gmail.com',
    'from': from_address,
    'address': to,
    'transContent': {
        'type': 1,
        'uuid': 'e1f1d3c7-3c6e-4f3b-a50d-58710b851357'
    },
    'payPassword': '111111'
})
if response['status'] != 200:
    raise Exception(response['message'])
# asset is sent success

# pay balance from `1L8eRrBuWnBxcQ6DKCDkkPM7ozxDcmpho1` to `14hF1BynFVnBEFKxyo51FHmJksVwfxg4sg`
response = pay({
    'from': from_address,
    'to': to,
    'value': 100,
    'payPassword': "111111"
});
if response['status'] != 200:
    raise Exception(response['message'])
# the value is paid success.
```

### add contacts

```py
from circle_chain.user import add_contacts
response = add_contacts({
    'email': "test2@gmail.com",
    'name': "test2",
    'sex': 1,
    'address': "beijing"
});
if response['status'] != 200:
    raise Exception(response['message'])
# the contact is added success.
```

## APIs

### circle_node

1. `subcribe`

2. `server_features`

3. `broadcast_transaction`

### circle_user

1. `send_verify_code`
2. `login`
3. `logout`
4. `send_register_verify_code`
5. `register`
6. `add_contacts`
7. `list_contacts`
8. `send_pay_verify_code`
9. `set_pay_password`
10. `have_pay_password`
11. `send_reset_password_verify_code`
12. `reset_password`
13. `save_or_update_user_info`
14. `user_info`

### circle_wallet

#### cloud wallets

1. `create_wallet`
2. `list_wallet`
3. `balance_of_wallet`
4. `assets_of_wallet`
5. `assets_of_address`
6. `get_public_key_hash_from_address`
7. `balance_of_address`
8. `send_to`
9. `pay`
10. `search_tx_by_type`
11. `search_tx_by_time`
12. `public_key_from_address`
13. `let_me_try`

#### open wallets

1. `public_get_address_by_uid`
2. `public_get_assets_of_address`
3. `public_search_transaction`
4. `public_get_balance_of_address`

### circle_block

1. `get_block_hash_list`
2. `get_block`
3. `get_block_header_list`
4. `get_block_data`
5. `get_block_tail_hash_list`
6. `get_block_tails_po`
7. `get_transaction_by_txid`
8. `search_tx_by_txid`
9. `search_tx_by_address`
10. `search_utxo`