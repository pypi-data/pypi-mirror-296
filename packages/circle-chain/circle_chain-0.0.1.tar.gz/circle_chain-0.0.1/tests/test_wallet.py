import sys
sys.path.append('./src')

import unittest

from circle_chain.wallet import balance_of_address, balance_of_wallet, create_wallet, list_wallet, public_get_address_by_uid, public_get_assets_of_address, public_key_from_address, public_search_transaction


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
        self.assertIsNotNone(response['data'])

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

if __name__ == '__main__':
    unittest.main()
