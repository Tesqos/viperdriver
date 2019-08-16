import logging

from selenium.webdriver import Remote
from selenium.webdriver import ChromeOptions
from selenium.webdriver import IeOptions

from viperdriver import PATH_TMP
from viperlib import jsondata

logger = logging.getLogger(__name__)

kwd_url = 'url'
kwd_sessionid = 'sessionid'
default_listener = 'http://127.0.0.1:9515'
f_session = 'last_session.json'

class Session(jsondata):

    def __init__(self):
        self.contents = { kwd_url: None, kwd_sessionid: None }
        self.url =  default_listener
        self.filename = f_session
        self.location = PATH_TMP # default location for saved sessions
        self._exists = False
        self._savetofile = True

    @property
    def url(self):
        return self.contents[kwd_url]

    @url.setter
    def url(self, val):
        self.contents[kwd_url] = val

    @property
    def session_id(self):
        return self.contents[kwd_sessionid]

    @session_id.setter
    def session_id(self, val):
        self.contents[kwd_sessionid] = val

    @property
    def exists(self):
        return self._exists

    @exists.setter
    def exists(self, val):
        self._exists = val

    @property
    def savetofile(self):
        return self._savetofile

    @savetofile.setter
    def savetofile(self, val):
        self._savetofile = val

    def destroy(self):
        if not self.is_empty():
            sid = self.session_id # saving id for logger; will be destroyed with execution of next line
            super().destroy()
            logger.debug('Session ' + sid + ' destroyed.')
        self.__init__()

class SessionDriver(Remote):

    options = None
    session = Session()

    def __init__(self, browser='Chrome', headless=True):
        self._browser = browser
        if self._browser is not 'Safari': # no Options exists for Safari
            self.options = eval(self._browser + 'Options()')
        self.options.headless = headless

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def launch(self):
        if self.session.exists:
            try:
                self.session.get_from_file()
                self.session_connect()
                logger.debug('Connected to session ' + self.session.session_id + '.')
            except:
                raise Exception('Could not connect to existing session.')
        else:
            super().__init__(command_executor=self.session.url, options=self.options)
            self.session.session_id = self.session_id
            self.session.exists = True
            logger.debug('Session ' + self.session_id + ' created.')
            if self.session.savetofile:
                self.session.save_to_file()

    def session_connect(self, url=None, sessionid=None):
        if url is not None:
            self.session.url = url
        if sessionid is not None:
            self.session.session_id = sessionid
        assert self.session.url != None and self.session.session_id != None, __name__ + ": driver session parameters are empty."
        super().__init__(command_executor=self.session.url, desired_capabilities={}, options=self.options)
        self.close()
        self.session_id = self.session.session_id # do not remove: we need to assign property to RemoteWebDriver parent object

    def switch_to_window(self, titlestr, strict=False): # strict mode if True: title must match exaclty
       rc = False
       for handle in self.window_handles:
           super().switch_to.window(handle)
           if (strict and self.title == titlestr) or (not strict and titlestr in self.title):
              rc = self.title
              return rc

    def dropdown_all_options_list_get(self, elementId):
        lst = []
        items = self.find_elements_by_xpath('//select[@id=\'' + elementId + '\']/option')
        for item in items:
            lst.append(item.get_attribute('text'))
        return lst

    def quit(self):
        super().quit()
        if self.session.exists:
            self.session.destroy()
