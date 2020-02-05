import keyring

from viperdriver import Websession
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


    def _init(self):
        self.x = Websession()
        self.x.data_location = dir_data
        self.x.session.mustdelete=False
        self.y = Websession(login_required=False)
        self.y.data_location = dir_data

    def _cleanup(self):
        self.x.quit()
        self.y.quit()

    def test_credentials_unsecure(self):
        self._init()
        self.x.credentials.type = creds.CREDS_TYPE_PLAIN
        self.x.credentials.plain.filename = plain_fname
        self.x.credentials.plain.location = dir_data
        self.x.credentials.alias = plain_alias
        self.x.credentials.get()
        assert self.x.credentials.user == plain_uid
        assert self.x.credentials.password == plain_pwd
        self._cleanup()

    def test_credentials_secure(self):
        self._init()
        self.keyring_record.create()
        self.x.credentials.type = creds.CREDS_TYPE_SECURE
        self.x.credentials.alias = secure_keyring_service_name
        self.x.credentials.KWD_UID = secure_alias
        self.x.credentials.get()
        assert self.x.credentials.user == secure_uid
        assert self.x.credentials.password == secure_pwd
        self.keyring_record.delete()
        self._cleanup()

    def test_website_launch_no_login_new_session(self):
        self._init()
        self.y.launch()
        assert self.y.title == 'The world’s leading software development platform · GitHub'
        self._cleanup()

    def test_website_launch_no_login_session_exists(self):
        self._init()
        self.x.launch()
        self.y.launch(new_session=False)
        assert self.y.title == 'The world’s leading software development platform · GitHub'
        self._cleanup()
