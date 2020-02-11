import logging

import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL

from selenium.webdriver import Remote
from selenium.webdriver import ChromeOptions
from selenium.webdriver import IeOptions
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from viperdriver import dir_session_default, default_listener, f_session, kwd_listener, kwd_sessionid
from viperlib import jsondata

logger = logging.getLogger(__name__)

class Session(jsondata):

    def __init__(self):
        self.contents = { kwd_listener: default_listener, kwd_sessionid: None }
        self.filename = f_session
        self.location = dir_session_default # default location for saved sessions
        self.mustsave = True
        self.mustdelete = True

    @property
    def listener(self):
        return self.contents[kwd_listener]

    @listener.setter
    def listener(self, val):
        self.contents[kwd_listener] = val

    @property
    def id(self):
        return self.contents[kwd_sessionid]

    @id.setter
    def id(self, val):
        self.contents[kwd_sessionid] = val

    def reset(self):
        self.__init__()

    def destroy(self):
        if not self.is_empty():
            sid = self.id # saving id for logger; will be destroyed with execution of next line
            super().destroy()
            if sid is not None:
                logger.debug('Session ' + sid + ' destroyed.')
        self.reset()

class SessionDriver(Remote):

    def __init__(self, browser='Chrome', headless=True):
        self.session = Session()
        self._browser = browser
        if self._browser is not 'Safari': # no Options exists for Safari
            self.options = eval(self._browser + 'Options()')
        self.options.headless = headless

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def __listener_start__(self):
        if self._browser == 'Chrome':
            cmd = 'chromedriver'
        else:
            raise NotImplemented
        if logger.getEffectiveLevel() == logging.DEBUG:
            subprocess.Popen(cmd)
        else:
            subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)

    def __drv_launch__(self):
        self.__listener_start__()
        super().__init__(command_executor=self.session.listener, desired_capabilities={}, options=self.options)

    def quit(self):
        if self.client_is_connected():
            super().quit()
            self.session.destroy()
            if not self.client_is_connected():
                    logger.debug('Client destroyed.')
        else:
            logger.debug('No connected client.')

    def client_start_new(self):
        self.__drv_launch__()
        self.session.id = self.session_id
        logger.debug('Session ' + self.session.id + ' created.')
        if self.session.mustsave:
            self.session.save_to_file()

    def client_connect(self, session_info):
        if session_info is not None and session_info is not []:
            self.session.contents = session_info
        assert self.session.listener != None and self.session.id != None, __name__ + ": driver session parameters are empty."
        self.__drv_launch__()
        self.close()
        self.session_id = self.session.id # do not remove: we need to assign property to RemoteWebDriver parent object
        self._url = self.current_url

    def client_connect_to_filed(self):
        try:
            self.session.file_exists()
            self.session.get_from_file()
            self.client_connect(self.session.contents)
            logger.debug('Connected to session ' + self.session.id + '.')
        except:
            raise Exception('Could not connect to existing session.')

    def client_is_connected(self):
        try:
            self.current_url
            return True
        except (TypeError, AttributeError, selenium.common.exceptions.WebDriverException):
            return False

    def launch(self, new_session=True):
        """Either launches a brand new session or connects to a filed one.\nArgs: new_session=True\nTo connect to an existing session by passing the session info as an argument, use client_connect().
        """
        if new_session:
                self.client_start_new()
        else:
            assert self.session.file_exists(), 'Could not find session file: ' + self.session.full_path()
            self.client_connect_to_filed()

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

    def wait_until(self, timeout, str_condition):
        ln = 'WebDriverWait(self, ' + str(timeout) + ').until(EC.' + str_condition + ')'
        logger.debug(ln)
        return exec(ln)
