import sys
import getopt
import logging

from viperdriver.scripts import path_session_file, viper_logger, Driver

logger = logging.getLogger(__name__)
console = logging.StreamHandler()
logger.addHandler(console)
viper_logger.addHandler(logger)

def main():
    fpath = path_session_file
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
            viper_logger.setLevel(logging.DEBUG)
    drv = Driver()
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
