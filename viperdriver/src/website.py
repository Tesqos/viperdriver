import logging

import keyring

from viperlib import creds, jsondata
from viperdriver import SessionDriver

logger = logging.getLogger(__name__)


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
        if self.login_required and self.credentials.type == creds.CREDS_TYPE_PLAIN:
            self.credentials.plain.location = self._dataloc
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
    def credentials(self, obj):
        self._credentials = obj

    def go_page(self, page_name):
        assert page_name in self.pages.contents, 'Page not defined: ' + page_name + '.'
        self.get(self.pages.contents[page_name])
        logger.info(self.title)
