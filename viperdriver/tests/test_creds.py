import pytest

import keyring

import viperdriver.src.creds as creds

class keyring_record:

    test_key = 'VIPER_TEST'
    test_user = 'viper_test_user'
    test_uid = 'user0'
    test_pwd = 'password_viper'

    def __init__(self):
        self.keyring_record_make()

    def keyring_record_make(self):
        keyring.set_password(self.test_key, self.test_user, self.test_uid)
        keyring.set_password(self.test_uid, 'pwd', self.test_pwd)

def test_keyring_credentials_valid():
    kr = keyring_record()
    x = creds.creds()
    x.type = creds.CREDS_TYPE_SECURE
    x.keyring_key = kr.test_key
    x.user = kr.test_user
    x.load()
    assert x.contents["uid"] == kr.test_uid
    assert x.contents["pwd"] == kr.test_pwd
    del kr, x
