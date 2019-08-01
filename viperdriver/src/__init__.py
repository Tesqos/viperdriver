import logging

CREDS_TYPE_PLAIN = 'json'
CREDS_TYPE_SECURE = 'keyring'
CREDS_TYPE_SECURE_KEY_DEFAULT = 'viperdriver'

CREDS_F_NAME = 'login'

PAGES_F_NAME ='pages'

logger = logging.getLogger(__name__).addHandler(logging.NullHandler())
