"""
Demonstrates how to use viperdriver to both create a new browser session and connect to an orphan one.
The example should be run twice.
The first execution will create a brand new browser session.
As the result, the session info will be saved in a file.
During the second execution, the script will discover the file and will pass the session info from it to the viperdriver instance.
Then the viperdriver instance will connect to the existing session and will be able to take command of it (in this case hitting a URL and then closing it).
To execute the script: 'python -m viperdriver.examples.conntosession'
"""
import logging
import getopt
import sys
from time import sleep
from viperdriver import SessionDriver

from viperdriver import SessionDriver, dir_session_default, loggers_set
from viperdriver import logger as logger

logger.setLevel(logging.INFO) # note that the code below requires print() for its specific functionality

def exec(browser):
    logger.info('Running browser ' + browser)
    drv = SessionDriver(browser) # do not use 'with'! with context manager session will be destroyed
    drv.options.headless = False         # start viperdriver in visible mode
    if drv.session.file.file_exists():        # if previous session exists, connect to it
        logger.info('Session file found: ' + drv.session.file.full_path())
        drv.launch(new_session=False)
        print('Connecting to existing session in....')
        x = range(5)
        for i in x:
            print('\b', x[-1-i], sep='', end='', flush=True)
            sleep(1)
        print('\n')
        logger.info('The page title is ' + drv.title)
        logger.info('Will now close the browser.')
        for i in range(10):
            print('.', sep='', end='', flush=True)
            sleep(0.5)
        print('\n')
        drv.quit()
    else:                               # if session does not exist, create new one and save to file
        drv.session.file.mustdelete=False
        drv.launch(new_session=True)
        drv.set_window_size(600, 300)
        logger.info('Navigating to SeleniumHQ...')
        drv.get('https://www.selenium.dev/')
        drv.session.file.save_to_file()
        logger.info('Exiting. Please start again.')

def main():
    browser = 'Chrome'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'b:', [])
    except getopt.GetoptError as err:
        logger.error(err)
        logger.info(__doc__)
        sys.exit(2)
    for opt, args in opts:
        if opt == '-b':
            browser=args
    exec(browser)


if __name__ == '__main__':
    main()
