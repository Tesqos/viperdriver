import logging
import os

from .src.core import SessionDriver as SessionDriver
from .src.website import Websession as Websession

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.addHandler(console)

PATH_TMP = __path__[0] + os.sep + 'tmp'
