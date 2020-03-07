from viperdriver import SessionDriver, f_session
from viperdriver.scripts.newsession import make_session as newsession
from viperdriver.scripts.getsaved import get_saved_session as getsaved
from viperdriver.scripts.deletesaved import delete_saved_session as deletesaved
from viperdriver.scripts.closesaved import close_saved_session as closesaved
import pytest
import os

browser = 'Firefox'

def create_session():
        newsession(browser)
        return getsaved()

def cleanup():
    closesaved()
    deletesaved()


def test_launch_brand_new_session():
    with SessionDriver(browser) as drv:
        drv.launch(new_session=True)
        assert not drv.session.file.is_empty(), 'Session info is empty!'
        drv.get('https://en.wikipedia.org/wiki/Sevastopol')
        assert drv.title == 'Sevastopol - Wikipedia', 'Wikipedia page about the legendary city is not diplayed.'
    cleanup()

def test_launch_connect_to_existing_session():
    session_info = create_session()
    with SessionDriver(browser) as drv:
        drv.launch(new_session=False)
        exp = session_info['sessionid']
        act = drv.session.attributes.id
        assert act == exp, 'Expected session id: ' + exp + 'actual: ' + act
    cleanup()

def test_session_connect():
    session_info = create_session()
    with SessionDriver(browser) as drv:
        drv.client_connect(session_info)
        drv.get('https://www.breitbart.com/')
        assert drv.title == 'Breitbart News Network'
    cleanup()

def test_client_connect_to_filed():
    session_info = create_session()
    with SessionDriver(browser) as drv:
        drv.client_connect_to_filed()
        assert drv.session.attributes.full == session_info
    cleanup()
