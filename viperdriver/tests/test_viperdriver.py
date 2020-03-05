from viperdriver import SessionDriver, f_session, kwd_listener, kwd_sessionid
from viperdriver.scripts.newsession import main as newsession
from viperdriver.scripts.getsaved import main as getsaved
from viperdriver.scripts.deletesaved import main as deletesaved
from viperdriver.scripts.closesaved import main as closesaved
import pytest
import os

def create_session():
        newsession()
        return getsaved()

def cleanup():
    closesaved()
    deletesaved()


def test_launch_brand_new_session():
    with SessionDriver() as drv:
        drv.launch(new_session=True)
        assert not drv.session.is_empty(), 'Session info is empty!'
        drv.get('https://en.wikipedia.org/wiki/Sevastopol')
        assert drv.title == 'Sevastopol - Wikipedia', 'Wikipedia page about the legendary city is not diplayed.'

def test_launch_connect_to_existing_session():
    session_info = create_session()
    with SessionDriver() as drv:
        drv.launch(new_session=False)
        exp = session_info[kwd_sessionid]
        act = drv.session.id
        assert act == exp, 'Expected session id: ' + exp + 'actual: ' + act
    cleanup()

def test_session_connect():
    session_info = create_session()
    with SessionDriver() as drv:
        drv.client_connect(session_info)
        drv.get('https://www.breitbart.com/')
        assert drv.title == 'Breitbart News Network'
    cleanup()

def test_client_connect_to_filed():
    session_info = create_session()
    with SessionDriver() as drv:
        drv.client_connect_to_filed()
        assert drv.session.contents == session_info
        drv.session.mustdelete = True
        drv.quit()
    cleanup()
