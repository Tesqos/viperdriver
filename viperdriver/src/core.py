import logging
import time
import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL
import socket
import os

from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver import ChromeOptions
from selenium.webdriver import IeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from viperdriver import dir_session_default, server, port_chrome, port_firefox, f_session, kwd_listener, kwd_sessionid
from jsonnote import jsonnote

logger = logging.getLogger(__name__)


class SessionDriver(Remote):

    class Session:

        class _listener:

            _addr = server
            _port = ''

            @property
            def address(self):
                return self._addr

            @address.setter
            def address(self, val):
                self._addr = val

            @property
            def port(self):
                return self._port

            @port.setter
            def port(self, val):
                self._port = val

            @property
            def full(self):
                return self._addr + ':' + self._port

        def __init__(self):
            self._json = jsonnote()
            self._lsnr = self._listener()
            self._json.contents = { kwd_listener: self.listener.full, kwd_sessionid: None}
            self._json.filename = f_session
            self._json.location = dir_session_default # default location for saved sessions
            self._json.mustsave = True
            self._json.mustdelete = True

        def listener_update(self):
            self.attributes.update({kwd_listener: self.listener.full})

        @property
        def file(self):
            return self._json

        @property
        def attributes(self):
            return self._json.contents

        @attributes.setter
        def attributes(self, dct):
            self._json.contents = dct

        @property
        def listener(self):
            return self._lsnr

        @property
        def id(self):
            return self.attributes[kwd_sessionid]

        @id.setter
        def id(self, val):
            self.attributes[kwd_sessionid] = val

        def save_to_file(self):
            self.file.save_to_file()

        def get_from_file(self):
            self.file.get_from_file()

        def destroy(self):
            if not self.file.is_empty():
                sid = self.id # saving id for logger; will be destroyed with execution of next line
                self.file.destroy()
                if sid is not None:
                    logger.debug('Session ' + sid + ' destroyed.')
            self.file.__init__()


    def __init__(self, browser='Chrome', headless=True):
        self.session = self.Session()
        self._browser = browser
        self.session.attributes.update({'browser': self._browser})
        if self._browser != 'Safari': # no Options exists for Safari
            self.options = eval(self._browser + 'Options()')
        self.options.headless = headless

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def __listener_set__(self):
        if self._browser == 'Chrome':
            self.session.listener.port = port_chrome
        if self._browser == 'Firefox':
            self.session.listener.port = port_firefox
        self.session.listener_update()

    def __listener_Chrome_command__(self):
        return 'chromedriver'

    def __listener_Firefox_command__(self):
        def find_free_port():
            s = socket.socket()
            s.bind((server, 0))            # Bind to a free port provided by the host.
            return str(s.getsockname()[1])
        new = find_free_port()
        self.session.listener.port = new
        return ['geckodriver', '--port', new]

    def __listener_start__(self):
        self.__listener_set__()
        if self._browser == 'Chrome':
            cmd = self.__listener_Chrome_command__()
        if self._browser == 'Firefox':
            cmd = self.__listener_Firefox_command__()
            port = cmd[2]
            self.session.listener.port = port
        if logger.getEffectiveLevel() == logging.DEBUG:
            subprocess.Popen(cmd)
        else:
            subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
        time.sleep(1)

    def __drv_launch__(self):
        self.__listener_start__()
        super().__init__(command_executor=self.session.listener.full, desired_capabilities={}, options=self.options)

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
        if self.session.file.mustsave:
            self.session.save_to_file()

    def client_connect(self, session_info):
        if session_info is not None and session_info is not []:
            self.session.attributes = session_info
        self.__drv_launch__()
        self.close()
        if self._browser == 'Firefox':
            self.command_executor._url = session.attributes[kwd_listener]
        self.session_id = self.session.id # do not remove: we need to assign property to RemoteWebDriver parent object

    def client_connect_to_filed(self):
        try:
            self.session.file.file_exists()
            self.session.get_from_file()
            self.client_connect(self.session.attributes)
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
            assert self.session.file.file_exists(), 'Could not find session file: ' + self.session.file.full_path()
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
