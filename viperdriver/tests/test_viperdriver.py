from viperdriver import SessionDriver, f_session, kwd_listener, kwd_sessionid
import pytest
import os

def create_session():
    """ Auxiliary (not a testing) function."""
    drv = SessionDriver()
    drv.session.mustsave = True
    drv.mustdelete=False
    drv.launch(new_session=True)
    info = drv.session.contents
    return info

def test_launch_brand_new_session():
    drv = SessionDriver()
    drv.launch(new_session=True)
    assert not drv.session.is_empty(), 'Session info is empty!'
    drv.get('https://en.wikipedia.org/wiki/Sevastopol')
    assert drv.title == 'Sevastopol - Wikipedia', 'Wikipedia page about the legendary city not diplayed.'
    drv.quit()

def test_launch_connect_to_existing_session():
    session_info = create_session()
    drv = SessionDriver()
    drv.launch(new_session=False)
    exp = session_info[kwd_sessionid]
    act = drv.session.id
    assert act == exp, 'Expected session id: ' + exp + 'actual: ' + act
    drv.quit()

def test_session_connect():
    session_info = create_session()
    drv = SessionDriver()
    drv.client_connect(session_info)
    drv.get('https://www.breitbart.com/')
    assert drv.title == 'Breitbart News Network'
    drv.quit()
