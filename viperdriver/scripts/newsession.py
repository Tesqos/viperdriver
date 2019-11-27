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

def make_session(location=dir_session_default, headless=True):
    drv = SessionDriver()
    drv.options.headless = headless
    drv.session.location = location
    if not drv.session.file_exists():
        drv.launch(save_session=True)
        logger.debug(drv.session.full_path())
    else:
        logger.critical('Existing session found. Exiting.')

def main():

    # Do not remove. This assignments needed if launched as a script while efault arguments of make_session() needed if run from shell.
    fpath = dir_session_default
    headless = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'avhl:', [])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.info(__doc__)
        sys.exit(2)
    for opt, args in opts:
        if opt == '-h':
            logger.critical(__doc__)
            sys.exit()
        if opt == '-a':
            headless = False
        if opt == '-l':
            fpath = args
        if opt == '-v':
            loggers_set(logging.DEBUG)

    make_session(fpath, headless)

if __name__ == "__main__":
    main()
