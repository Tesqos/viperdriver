"""
Closes 'saved' Selenium-controlled browser session.'Saved' means the session is up and running and its session info is saved in a file.

Usage:
-l <path>   - session file location (set to default if omitted)
-v          - verbose
-h          - help (print this )
"""
import sys
import getopt
import logging

from viperdriver import SessionDriver, dir_session_default, logger, loggers_set

def main(browser='Chrome'):
    fpath = dir_session_default
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:dhv', [])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.info(__doc__)
        sys.exit(2)
    for opt, args in opts:
        if opt == '-h':
            logger.critical(__doc__)
            sys.exit()
        if opt == '-l':
            fpath = args
        if opt == '-v':
            loggers_set(logging.DEBUG)
    drv = SessionDriver(browser)
    drv.session.file.location = fpath
    if drv.session.file.file_exists():
        drv.launch(new_session=False)
        drv.quit()
    else:
        logger.critical('No saved session found.')

if __name__ == '__main__':
    main()
