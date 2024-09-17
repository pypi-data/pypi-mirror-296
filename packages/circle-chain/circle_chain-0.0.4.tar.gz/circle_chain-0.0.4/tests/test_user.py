import sys
sys.path.append('./src')

from circle_chain.user import add_contacts, have_pay_password, list_contacts, login, register, reset_password, \
    save_login_info, save_or_update_user_info, send_pay_verify_code, send_register_verify_code, \
    send_reset_password_verify_code, send_verify_code, set_pay_password, logout
import unittest

class TestUser(unittest.TestCase):

    def test_send_register_verify_code(self):
        response = send_register_verify_code({ "email": "test@gmail.com" })
        self.assertIs(response['status'], 200)

    def test_register(self):
        response = register({
            "email": "test@gmail.com",
            "passwordInput1": "111111",
            "passwordInput2": "111111",
            "verifyCode": "222222"
        })
        self.assertIsNot(response['status'], 200)


    def test_send_verify_code(self):
        response = send_verify_code({ "email": "test@gmail.com" })
        print('test_send_verify_code response:', response)
        self.assertIs(response['status'], 200)

    def test_login(self):
        response = login({
            "email": "test@gmail.com",
            "password": "111111",
        })
        self.assertIsNot(response['status'], 200)

    def test_send_pay_verify_code(self):
        response = send_pay_verify_code({ "email": "test@gmail.com" })
        self.assertIsNot(response['status'], 200)

    def test_set_pay_password(self):
        response = set_pay_password({
            "account": {
                "email": "test@gmail.com"
            },
            "password": "333333",
            "verifyCode": "112222"
        })
        self.assertIsNot(response['status'], 200)


    def test_have_pay_password(self):
        response = have_pay_password();
        self.assertIsNot(response['status'], 200)

    def test_send_reset_password_verify_code(self):
        response = send_reset_password_verify_code({ "email": "test@gmail.com" })
        print('test_send_reset_password_verify_code response:', response)
        self.assertIs(response['status'], 200)

    def test_reset_password(self):
        response = reset_password({
            "account": {
                "email": "test@gmail.com"
            },
            "verifyCode": "222222",
            "password1": "111111",
            "password2": "222222"
        })
        self.assertIsNot(response['status'], 200)

    def test_add_contacts(self):
        response = add_contacts({
            "email": "friend@gmail.com",
            "sex": 1,
            "name": "friend",
            "address": "beijing"
        })
        self.assertIsNot(response['status'], 200)

    def test_list_contacts(self):
        response = list_contacts();
        self.assertIsNot(response['status'], 200)

    def test_save_or_update_user_info(self):
        response = save_or_update_user_info({
            "userId": "86edefcdfe3223412fdeabcdfe",
            "name": "test",
            "addresse": "beijing"
        })
        self.assertIsNot(response['status'], 200)

    def test_save_login_info(self):
        result = save_login_info({
            "userId": "3663b693a73f497f6860a57adbd640d76d27b2d69394e33a278d351df0ccb763",
            "userType": 1,
            "sessionKey": "a618cfc02c9b4e7da82cae0cddb7d29d",
            "email": "sihuic2012@gmail.com"
        })
        self.assertTrue(result)

    def test_logout(self):
        response = logout()
        print('test_logout response:', response)
        self.assertIsNot(response.get('status'), 200)

if __name__ == '__main__':
    unittest.main()
