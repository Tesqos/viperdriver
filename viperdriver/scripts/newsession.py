"""
Creates new Selenium-controlled browser session.

Usage:
-l <path>   - session file location (set to default if omitted)
-v          - run in visible mode (non-headless)
-d          - run in debug mode (logger on)
-h          - help (print this )

Note: if session file path is omitted, session file is created under package's root (see PATH_TMP in <root>/__init__.py).
"""
import sys
import os
import getopt
import logging

from viperdriver.scripts import path_session_file, viper_logger, Driver

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
logger.addHandler(console)
viper_logger.addHandler(logger)

def main():

    headless = True
    fpath = path_session_file
    savetofile = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dhl:v', [])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.info(__doc__)
        sys.exit(2)
    for opt, args in opts:
        if opt == '-h':
            logger.setLevel(logging.INFO)
            logger.info(__doc__)
            sys.exit()
        if opt == '-v':
            headless = False
        if opt == '-l':
            fpath = args
        if opt == '-d':
            logger.setLevel(logging.DEBUG)
            viper_logger.setLevel(logging.DEBUG)

    drv = Driver()
    drv.options.headless = headless
    if fpath != path_session_file:
        drv.session.location = fpath
    if drv.session.file_exists():
        logger.critical('Existing session found. Exiting.')
        sys.exit(1)
    drv.session.savetofile = savetofile
    drv.launch()
    logger.debug(drv.session.full_path())


if __name__ == "__main__":
    main()
