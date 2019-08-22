import logging
import os

logger = logging.getLogger(__name__)

PATH_TMP = __path__[0] + os.sep + 'tmp' # default location of the session file

from viperdriver.src.website import Websession
