import logging
import os

import logging

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.addHandler(console)

PATH_TMP = __path__[0] + os.sep + 'tmp'
