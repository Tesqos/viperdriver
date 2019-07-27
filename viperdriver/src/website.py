import logging

from viperbox.vebdriver import SessionDriver
from viperbox.viperlib import jsondata
from viperbox.viperlib.misc import dir_get

logger = logging.getLogger(__name__)

class logininfo(jsondata):

    def __init__(self):
        self.filename = 'login'
        self._user = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, val):
        self._user = val
        self._contents = self.contents[self.user]

    @jsondata.contents.getter
    def contents(self):
        return self._contents


class SitePages(jsondata):

    def __init__(self):
        self.filename = 'pages'

class Websession(SessionDriver):

    _url_home = None
    _url_main = None
    _credentials = None
    _dataloc = None
    _loginrequired = True

    def __init__(self, login_required=True):
        self.login_required = login_required
        super().__init__()
        self._credentials = logininfo()
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
            self.credentials.get_from_file()
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
