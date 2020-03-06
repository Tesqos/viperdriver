import logging
import time
import subprocess
from subprocess import Popen, PIPE, STDOUT, DEVNULL
import socket
import os
from copy import deepcopy

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

from viperdriver import dir_session_default, server, port_chrome, port_firefox, f_session
from jsonnote import jsonnote

logger = logging.getLogger(__name__)


class SessionDriver(Remote):

    class _Session:

        class _filehandler(jsonnote):

            def __init__(self):
                self.filename = f_session
                self.location = dir_session_default # default location for saved sessions
                self.mustsave = True
                self.mustdelete = True

        class _attributes:

            def __init__(self):
                self._data = {'browser': None, 'listener': None, 'sessionid': None}

            @property
            def browser(self):
                return self._data['browser']

            @browser.setter
            def browser(self, val):
                self._data['browser'] = val

            @property
            def listener(self):
                return self._data['listener']

            @listener.setter
            def listener(self, val):
                self._data['listener'] = val

            @property
            def id(self):
                return self._data['sessionid']

            @id.setter
            def id(self, val):
                self._data['sessionid'] = val

            @property
            def full(self):
                return self._data

            @full.setter
            def full(self, data):
                self._data = deepcopy(data)

        class _listener:

            def __init__(self, browser):
                self._addr = server
                self._port = ''
                self._browser = browser
                self.__url_initialize__()

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

            def launch(self):
                cmd = self.__launching_command__()
                if logger.getEffectiveLevel() == logging.DEBUG:
                    subprocess.Popen(cmd)
                else:
                    subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
                time.sleep(1)

            def __launching_command__(self):
                if self._browser == 'Chrome':
                    return self.__chrome_command__()
                if self._browser == 'Firefox':
                    return self.__firefox_command__()

            def __url_initialize__(self):
                if self._browser == 'Chrome':
                    self.port = port_chrome
                if self._browser == 'Firefox':
                    self.port = port_firefox

            def __chrome_command__(self):
                return 'chromedriver'

            def __firefox_command__(self):
                def find_free_port():
                    s = socket.socket()
                    s.bind((server, 0))            # Bind to a free port provided by the host.
                    return str(s.getsockname()[1])
                new = find_free_port()
                self.port = new
                return ['geckodriver', '--port', new]

        def __init__(self, browser):
            self._browser = browser
            self.listener = self._listener(browser)
            self.file = self._filehandler()
            self.attributes = self._attributes()
            self.attributes.browser = self._browser
            self.attributes.listener = self.listener.full
            self.update()

        def update(self, from_file=False):
            if from_file:
                try:
                    self.file.file_exists()
                    self.file.get_from_file()
                    self.attributes.full = self.file.contents
                except:
                    logger.critical('Could not load session attributes from file: ' + self.file.full_path())
            else:
                self.file.contents = self.attributes.full

        def destroy(self):
            if not self.file.is_empty():
                sid = self.attributes.id # saving id for logger; will be destroyed with execution of next line
                self.file.destroy()
                if sid is not None:
                    logger.debug('Session ' + sid + ' destroyed.')
            del self.file
            del self.attributes
            del self.listener
            del self._browser

    def __init__(self, browser='Chrome', headless=True):
        self.session = self._Session(browser)
        if browser != 'Safari': # no Options exists for Safari
            self.options = eval(browser + 'Options()')
        self.options.headless = headless

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def __drv_launch__(self):
        self.session.listener.launch()
        super().__init__(command_executor=self.session.listener.full, desired_capabilities={}, options=self.options)
        logger.debug('Session ' + self.session_id + ' launched.')

    def client_start_new(self):
        self.__drv_launch__()
        self.session.attributes.id = self.session_id
        self.session.update()
        if self.session.file.mustsave:
            self.session.file.save_to_file()
        logger.debug('NEW session ' + self.session.attributes.id + ' created.')

    def client_connect(self, session_info):
        if session_info is not None and session_info is not []:
            self.session.attributes.full = session_info
            self.session.update()
        logger.debug('Attempting to connect to existing session ' + self.session.attributes.id)
        self.__drv_launch__()
        self.close()
        if self.session.attributes.browser == 'Firefox':
            self.command_executor._url = self.listener.full
        self.session_id = self.session.attributes.id
        logger.debug('Connected to EXISTING session ' + self.session_id + '.')

    def client_connect_to_filed(self):
        try:
            self.session.update(from_file=True)
            self.client_connect(self.session.attributes.full)
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

    def close(self):
        sid = self.session_id
        super().close()
        logger.debug('Session ' + sid + ' closed.')

    def quit(self):
        if self.client_is_connected():
            super().quit()
            self.session.destroy()
            self.__init__()
            if not self.client_is_connected():
                    logger.debug('Client destroyed.')
        else:
            logger.debug('No connected client.')

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
