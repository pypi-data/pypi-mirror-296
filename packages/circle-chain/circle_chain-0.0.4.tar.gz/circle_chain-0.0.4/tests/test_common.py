import unittest
import sys
sys.path.append('./src')
# print(sys.path)
from circle_chain.common import build_url_template, get_access_key, get_session_path, http_json_get, http_json_post, load_config

class TestCommon(unittest.TestCase):

    def test_load_config(self):
        config = load_config()
        self.assertIsNotNone(config)

    def test_get_access_key(self):
        session_key = get_access_key()
        print(session_key)
        self.assertIsNotNone(session_key)

    def test_build_url_template(self):
        url = build_url_template('block', 'blockchainHashListPath')
        print("blockchainHashListPath:", url)
        self.assertIsNotNone(url)

    def test_http_json_get(self):
        url = build_url_template('block', 'blockchainHashListPath')
        response = http_json_get(url, { "baseHeight": 0 }, 30000)
        self.assertIs(response['status'], 200)

    def test_http_json_post(self):
        url = build_url_template('user', 'logout')
        response = http_json_post(url, {}, 30000)
        self.assertIsNot(response['status'], 200)

    def test_get_session_path(self):
        session_path = get_session_path()
        print("session path:", session_path)
        self.assertIsNotNone(session_path)


if __name__ == '__main__':
    unittest.main()
