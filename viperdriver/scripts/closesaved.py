import sys
import getopt
import logging

from .. import PATH_TMP, logger
from ..src.core import SessionDriver

def main():
    fpath = PATH_TMP
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'l:d', [])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.info(__doc__)
        sys.exit(2)
    for opt, args in opts:
        if opt == '-l':
            fpath = args
        if opt == '-d':
            logger.setLevel(logging.DEBUG)
    drv = SessionDriver()
    drv.session.savetofile = False
    drv.session.location = fpath
    if drv.session.file_exists():
        drv.session.exists = True
        drv.launch()
        drv.quit()
    else:
        logger.info('No saved session found.')

if __name__ == '__main__':
    main()
