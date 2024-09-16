import sys
sys.path.append('./src')

import unittest

from circle_chain.block import get_block_hashlist, get_block, get_block_header_list, get_block_data, \
    get_blocktails_hashlist, get_blocktails_po, get_tx_by_txid, search_tx_by_txid, search_tx_by_address, search_utxos


class TestBlock(unittest.TestCase):
    def test_get_block_hashlist(self):
        response = get_block_hashlist(10)
        print('response:', response)
        self.assertIs(response['status'], 200)

    def test_get_block(self):
        response = get_block('00000006e7ebf7aa563701d3fe04b6e32416929a1426d287a394b62ffe867436')
        print('response:', response)
        self.assertIs(response['status'], 200)

    def test_get_block_header_list(self):
        response = get_block_header_list(10)
        print('response:', response)
        self.assertIs(response['status'], 200)

    def test_get_block_data(self):
        response = get_block_data('00000006e7ebf7aa563701d3fe04b6e32416929a1426d287a394b62ffe867436')
        print('response:', response)
        self.assertIs(response['status'], 200)

    def test_get_blocktails_hashlist(self):
        response = get_blocktails_hashlist(10)
        print('response:', response)
        self.assertIs(response['status'], 200)

    def test_get_blocktails_po(self):
        response = get_blocktails_po('00000006e7ebf7aa563701d3fe04b6e32416929a1426d287a394b62ffe867436')
        print('response:', response)
        self.assertTrue(response['status'] == 404)

    def test_get_tx_by_txid(self):
        response = get_tx_by_txid('adf54afa65668e28700476eabf22760d97f4a0b715d855dffe60f57b12ad0c87')
        print('response:', response)
        self.assertIs(response['status'], 200)

    def test_search_tx_by_txid(self):
        response = search_tx_by_txid('adf54afa65668e28700476eabf22760d97f4a0b715d855dffe60f57b12ad0c87')
        print('response:', response)
        self.assertIs(response['status'], 200)

    def test_search_tx_by_address(self):
        response = search_tx_by_address('16rcESr6pm3x3PByQH6JEbJBzZkf5W5NQk',
                                        '3acdf6d7c032d1b300c45a75a440ef61ade78113f8e000d5ff005b8afac87466',
                                        10)
        print('response:', response)
        self.assertIs(response['status'], 200)

    def test_search_utxos(self):
        response = search_utxos('16rcESr6pm3x3PByQH6JEbJBzZkf5W5NQk',
                                 '3acdf6d7c032d1b300c45a75a440ef61ade78113f8e000d5ff005b8afac87466',
                             10)
        print('response:', response)
        self.assertIs(response['status'], 200)


if __name__ == '__main__':
    unittest.main()
