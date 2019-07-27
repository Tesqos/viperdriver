from ..src.core import SessionDriver, f_session, kwd_url, kwd_sessionid
import pytest
import os

def create_session(savetofile=True):
    """ Auxiliary (not a testing) function."""
    drv = SessionDriver()
    drv.session.savetofile = savetofile
    drv.launch()
    info = drv.session.contents
    return info

def test_launch_no_previous_session():
    drv = SessionDriver()
    drv.session.exists = False
    drv.session.savetofile = False
    drv.launch()
    assert not drv.session.is_empty(), 'Session info is empty!'
    drv.get('https://en.wikipedia.org/wiki/Sevastopol')
    assert drv.title == 'Sevastopol - Wikipedia', 'Wikipedia page about the legendary city not diplayed.'
    drv.quit()

def test_launch_with_existing_session():
    session_info = create_session()
    drv = SessionDriver()
    drv.session.savetofile = False
    drv.launch()
    exp = session_info[kwd_sessionid]
    act = drv.session.session_id
    assert act == exp, 'Expected session id: ' + exp + 'actual: ' + act
    drv.quit()

def test_session_connect():
    session_info = create_session(savetofile=False)
    drv = SessionDriver()
    drv.session_connect(session_info[kwd_url], session_info[kwd_sessionid])
    drv.get('https://www.breitbart.com/')
    assert drv.title == 'Breitbart News Network', 'Looks like we got to a fake news site instead.'
    drv.quit()

def test_N_launch_connect_to_existing_session_no_file():
    drv = SessionDriver()
    drv.session.exists = True # however, session file does not exist, which will generate an error
    with pytest.raises(Exception):
        drv.launch()
    # Do NOT add drv.quit() here because session has NOT been created
