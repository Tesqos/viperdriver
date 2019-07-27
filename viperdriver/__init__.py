import logging
import os

logger = logging.getLogger(__name__)

PATH_TMP = __path__[0] + os.sep + 'tmp'

from .src.core import SessionDriver as SessionDriver
from .src.website import Websession
