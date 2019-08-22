import keyring

from viperdriver.src.website import Websession
from viperdriver.tests import dir_data
from viperlib import creds

secure_keyring_service_name = 'VIPER_TEST'
secure_alias = 'Viper'
secure_uid = 'username@gmail.com'
secure_pwd = 'password_viper'

plain_fname = 'login'
plain_alias = 'test user'
plain_uid = 'Tester'
plain_pwd = 'my password'

class Test_Credentials:

    class keyring_record:

        def create():
            keyring.set_password(secure_keyring_service_name, secure_alias, secure_uid)
            keyring.set_password(secure_uid, 'pwd', secure_pwd)

        def delete():
            keyring.delete_password(secure_keyring_service_name, secure_alias)
            keyring.delete_password(secure_uid, 'pwd')

    x = Websession()
    y = Websession(login_required=False)

    # AS OF AUGUST 21, 2019 THE TESTS COMMENTED BELOW DO NOT WORK WHEN LAUNCHED FROM CONSOLE WITH PYTEST EVEN THOUGH THEY WORK WHEN IMPORTED.
    # INVESTIGATION IS REQUIRED.

    # def test_credentials_unsecure(self):
    #     self.x.credentials.type = creds.CREDS_TYPE_PLAIN
    #     self.x.credentials.get_plain().filename = plain_fname
    #     self.x.credentials.get_plain().location = dir_data
    #     self.x.credentials.alias = plain_alias
    #     self.x.credentials.get()
    #     assert self.x.credentials.user == plain_uid
    #     assert self.x.credentials.password == plain_pwd
    #
    # def test_credentials_secure(self):
    #     self.keyring_record.create()
    #     self.x.credentials.alias = secure_alias
    #     self.x.credentials.get()
    #     assert self.x.credentials.user == secure_uid
    #     assert self.x.credentials.password == secure_pwd
    #     self.keyring_record.delete()


    def test_website_launch_no_login_required(self):
        # Mistery: tests fail if:
        # 1) next line is removed
        # 2) the whole test package run with 'pytest'
        # If only the current file is run or only the test alone (with 'pytest -k' ), the test does not fail even with the line commented.
        # It is even more puzzling considering that ..session.exists is False by default.
        self.y.session.exists = False
        self.y.session.savetofile = False
        self.y.data_location = dir_data
        self.y.launch()
        assert self.y.title == 'The world’s leading software development platform · GitHub'
        self.y.quit()
