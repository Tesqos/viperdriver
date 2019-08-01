import logging
import os

logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

PATH_TMP = __path__[0] + os.sep + 'tmp'

# NOTE: do NOT place the following import statements above PATH_TMP
from .src.core import SessionDriver as SessionDriver
from .src.website import Websession as Websession
