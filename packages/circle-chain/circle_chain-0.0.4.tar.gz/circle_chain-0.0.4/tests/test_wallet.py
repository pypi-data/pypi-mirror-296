import sys
sys.path.append('./src')

import unittest

from circle_chain.wallet import balance_of_address, balance_of_wallet, create_wallet, list_wallet, \
    public_get_address_by_uid, public_get_assets_of_address, public_key_from_address, \
    public_search_transaction, send_to, pay, public_get_balance_of_address


class TestWallet(unittest.TestCase):

    def test_create_wallet(self):
        response = create_wallet()
        self.assertIsNot(response['status'], 200)

    def test_list_wallet(self):
        response = list_wallet()
        self.assertIsNot(response['status'], 200)

    def test_balance_of_address(self):
        address = '1L8eRrBuWnBxcQ6DKCDkkPM7ozxDcmpho1'
        response = balance_of_address(address)
        self.assertIsNot(response['status'], 200)

    def test_balance_of_wallet(self):
        response = balance_of_wallet()
        self.assertIsNot(response['status'], 200)

    def test_public_key_from_address(self):
        address = '1L8eRrBuWnBxcQ6DKCDkkPM7ozxDcmpho1'
        response = public_key_from_address(address)
        self.assertTrue(response['status'] == 20002)
        print('public_key_from_address response:', response)
        self.assertIsNone(response.get('data'))

    def test_public_get_address_by_uid(self):
        uid = 'b3847f7e2f0bf0effe292501ffb05210186cc7e6ccde0ceb71dfdd7404b34a2e'
        response = public_get_address_by_uid(uid)
        self.assertIs(response['status'], 200)

    def test_public_get_assets_of_address(self):
        address = '1L8eRrBuWnBxcQ6DKCDkkPM7ozxDcmpho1'
        response = public_get_assets_of_address(address, 1)
        self.assertIs(response['status'], 200)

    def test_public_search_transaction(self):
        address = '1L8eRrBuWnBxcQ6DKCDkkPM7ozxDcmpho1'
        response = public_search_transaction({
            "address": address,
            "inOut": "IN",
            "transactionContent": {
                "type": 0
            }
        })
        self.assertIs(response['status'], 200)

    def test_send_to(self):
        response = send_to({
            'from': '1L8eRrBuWnBxcQ6DKCDkkPM7ozxDcmpho1',
            'address': '1rmzxfP5J1QjYXMa9zmSC7dCBLTDciBda',
            'email': 'test@gmail.com',
            'transContent': {
                'type': 1,
                'uuid': 'ef98dad9-21da-4939-abc4-ecd658ac2a5b'
            },
            'payPassword': '222222'
        })
        self.assertIsNot(response['status'], 200)

    def test_pay(self):
        response = pay({
            'from': '1Jhf7pUtmqK2ZqR9du7xa6uL1Qxdc14atG',
            'to': '1HDv7a7PqbYugZjaVJtMxvsnvpk7GS554s',
            'email': 'test@gmail.com',
            'value': 1000,
            'payPassword': '222222'
        })
        self.assertIsNot(response['status'], 200)

    def test_public_get_balance_of_address(self):
        response = public_get_balance_of_address('1Jhf7pUtmqK2ZqR9du7xa6uL1Qxdc14atG')
        print('test_public_get_balance_of_address response:', response)
        self.assertIs(response.get('status'), 200)

if __name__ == '__main__':
    unittest.main()
