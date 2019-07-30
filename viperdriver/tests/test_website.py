import keyring

from . import Websession
from . import dir_config

test_user = "test user"
keyring_key = "viperdriver"

class Test_Credentials:

    x = Websession()
    x.credentials.user = test_user
    y = Websession(login_required=False)

    def test_credentials_get_json(self):
        self.x.credentials.type = 'json'
        self.x.data_location = dir_config
        self.x.credentials.load()
        assert self.x.credentials.contents["uid"] == "Tester"

    def test_credentials_get_keyring(self):
        self.x.credentials.type = 'keyring'
        self.x.credentials.load()
        assert self.x.credentials.contents["uid"] == test_user
        assert self.x.credentials.contents["pwd"] == keyring.get_password(keyring_key, test_user)


    def test_website_launch_no_login_required(self):
        # Mistery: tests fail if:
        # 1) next line is removed
        # 2) the whole test package run with 'pytest'
        # If only the current file is run or only the test alone (with 'pytest -k' ), the test does not fail even with the line commented.
        # It is even more puzzling considering that ..session.exists is False by default.
        self.y.session.exists = False
        self.y.session.savetofile = False
        self.y.data_location = dir_config
        self.y.launch()
        assert self.y.title == 'The world’s leading software development platform · GitHub'
        self.y.quit()
