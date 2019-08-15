import logging
import os

logger = logging.getLogger(__name__)

PATH_TMP = __path__[0] + os.sep + 'tmp' # default location of the session file

# NOTE: do NOT place the following import statements above PATH_TMP
from viperdriver.src.core import SessionDriver as SessionDriver
from viperdriver.src.website import Websession as Websession
