import logging

import keyring

from viperlib import jsondata
from .core import SessionDriver

from . import CREDS_TYPE_PLAIN, CREDS_TYPE_SECURE, CREDS_F_NAME, PAGES_F_NAME, CREDS_TYPE_SECURE_KEY

logger = logging.getLogger(__name__)

class creds:

    _srctype = None
    _handle = None
    _loc = None
    _user = None
    _contents = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, val):
        self._user = val

    @property
    def type(self):
        return self._srctype

    @type.setter
    def type(self, val):
        self._srctype = val

    def load(self):
        assert self._user is not None, 'User key is not set. (Note: user key is not \'uid\'. Used for naming login info set.)'
        if self._srctype == CREDS_TYPE_PLAIN:
            assert self._loc is not None, 'Location is not set.'
            self._handle = creds_json()
            self._handle.location = self.location
            self._handle.get_from_file()
            self._handle.contents = self._handle.contents[self._user]
        elif self._srctype == CREDS_TYPE_SECURE:
            self._handle = creds_keyring()
            self._handle.keyring_key = self._user
            self._handle.get_from_keyring()
        else:
            raise ValueError('Expected \'json\' or \'keyring\' only.')

    @property
    def contents(self):
        return self._handle._contents

    @contents.setter
    def contents(self, obj):
        self._handle._contents = obj

    @property
    def location(self):
        return self._loc

    @location.setter
    def location(self, val):
        self._loc = val

class creds_keyring:

    _krk = None
    _contents = {}

    @property
    def keyring_key(self):
        return self._krk

    @keyring_key.setter
    def keyring_key(self, val):
        self._krk = val

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, obj):
        self._contents = obj

    def get_from_keyring(self):
        self._contents.update( {"uid": self._krk} )
        self._contents.update( {"pwd": keyring.get_password(CREDS_TYPE_SECURE_KEY, self._krk)} )

class creds_json(jsondata):

    def __init__(self):
        self.filename = CREDS_F_NAME


class SitePages(jsondata):

    def __init__(self):
        self.filename = PAGES_F_NAME

class Websession(SessionDriver):

    _url_home = None
    _url_main = None
    _credentials = None
    _dataloc = None
    _loginrequired = True

    def __init__(self, login_required=True):
        self.login_required = login_required
        super().__init__()
        if login_required:
            self._credentials = creds()
        self.pages = SitePages()

    def launch(self):
        super().launch()
        self.go_page('Home')

    @property
    def login_required(self):
        return self._loginrequired

    @login_required.setter
    def login_required(self, val):
        self._loginrequired = val

    @property
    def data_location(self):
        return self._dataloc

    @data_location.setter
    def data_location(self, val):
        self._dataloc = val
        if self.login_required:
            self.credentials.location = self._dataloc
        self.pages.location = self._dataloc
        self.pages.get_from_file()
        self.session.location = self._dataloc

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, val):
        self._pages = val

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, data):
        self._credentials = data

    def go_page(self, page_name):
        assert page_name in self.pages.contents, 'Page not defined: ' + page_name + '.'
        self.get(self.pages.contents[page_name])
        logger.info(self.title)
