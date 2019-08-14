import logging
import os

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
logger.addHandler(console)
logger.setLevel(logging.INFO)

PATH_TMP = __path__[0] + os.sep + 'tmp' # default location of the session file

# NOTE: do NOT place the following import statements above PATH_TMP
from .src.core import SessionDriver as SessionDriver
from .src.website import Websession as Websession
