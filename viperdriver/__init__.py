import logging
import os

console = logging.StreamHandler()
console.setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

logger.addHandler(console)

PATH_TMP = __path__[0] + os.sep + 'tmp'

# NOTE: do NOT place the import statements below before PATH_TMP

from .src.core import SessionDriver as SessionDriver
from .src.website import Websession as Websession
