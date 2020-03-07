"""
Creates new Selenium-controlled browser session.

Usage:
-l <path>   - session file location (set to default if omitted)
-a          - run in visible mode (non-headless)
-v          - verbose
-h          - help (print this )

Note: if session file path is omitted, session file is created under package's root (see PATH_TMP in <root>/__init__.py).
"""
import sys
import os
import getopt
import logging

from viperdriver import SessionDriver, dir_session_default, logger, loggers_set

logger = logging.getLogger(__name__)

def make_session(browser='Chrome', location=dir_session_default, headless=True):
    drv = SessionDriver(browser)
    drv.options.headless = headless
    drv.session.file.location = location
    if not drv.session.file.file_exists():
        drv.launch()
        logger.debug(drv.session.file.full_path())
    else:
        logger.critical('Existing session found. Exiting.')
    return drv.session.attributes.full

def main():
    fpath = dir_session_default
    headless = True
    browser ='Chrome'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ab:vhl:', [])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.info(__doc__)
        sys.exit(2)
    for opt, args in opts:
        if opt == '-b':
            browser = args
        if opt == '-h':
            logger.critical(__doc__)
            sys.exit()
        if opt == '-a':
            headless = False
        if opt == '-l':
            fpath = args
        if opt == '-v':
            loggers_set(logging.DEBUG)

    return make_session(browser=browser, location=fpath, headless=headless)

if __name__ == "__main__":
    main()
