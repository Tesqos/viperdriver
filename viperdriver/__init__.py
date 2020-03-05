import logging
import os

from viperlib import logger as logger_viperlib

__version__ = '0.57.2'

dir_session_default = __path__[0] + os.sep + 'tmp' # default location of the session file
kwd_listener = 'listener'
kwd_sessionid = 'sessionid'
listener_chrome = 'http://127.0.0.1:9515'
listener_firefox = '127.0.0.1:4444'
f_session = 'last_session.json'

from viperdriver.src.core import SessionDriver

logger = logging.getLogger(__name__)

console = logging.StreamHandler()
logger.addHandler(console)
logger_viperlib.addHandler(logger)

def loggers_set(level):
    logger.setLevel(level)
    logger_viperlib.setLevel(level)
