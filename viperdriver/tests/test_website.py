import keyring

from . import Websession
from . import dir_data

test_user = "test user"
keyring_key = "viperdriver"

class Test_Credentials:

    drv = Websession()
    drv.credentials.user = test_user

    def test_credentials_get_json(self):
        self.drv.credentials.type = 'json'
        self.drv.data_location = dir_data
        self.drv.credentials.load()
        assert self.drv.credentials.contents["uid"] == "Tester"

    def test_credentials_get_keyring(self):
        self.drv.credentials.type = 'keyring'
        self.drv.credentials.load()
        assert self.drv.credentials.contents["uid"] == test_user
        assert self.drv.credentials.contents["pwd"] == keyring.get_password(keyring_key, test_user)
