import sys
import os
import getopt
import logging

from viperdriver import SessionDriver, dir_session_default

logger = logging.getLogger(__name__) # do not need root logger

def delete_saved_session(fpath=dir_session_default, browser='Chrome'):
    drv = SessionDriver()
    drv.options.headless = True
    if fpath != dir_session_default:
        drv.session.file.location = fpath
    if not drv.session.file.file_exists():
        logger.critical('No session found.')
    else:
        drv.session.file.destroy()

def main():
    fpath = dir_session_default
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:', [])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.info(__doc__)
        sys.exit(2)
    for opt, args in opts:
        if opt == '-l':
            fpath = args

    delete_saved_session(fpath=fpath)

if __name__ == "__main__":
    main()
