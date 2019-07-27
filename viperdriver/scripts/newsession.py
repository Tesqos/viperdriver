import sys
import logging

from . import KWD_DIR_HOME, SessionDriver

logger = logging.getLogger(__name__)

assert len(sys.argv) > 1, 'Location argument required.'

if __name__ == "__main__":
    drv = SessionDriver()
    if sys.argv[1] != KWD_DIR_HOME:
        drv.session.location = sys.argv[1]
    drv.launch()
    drv.session.save_to_file()
    logger.info(drv.session.session_id)
    logger.debug(drv.session.full_path())
