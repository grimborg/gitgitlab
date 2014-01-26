"""Request and store the gitlab token in the keyring."""

import keyring
from getpass import getpass


KEYRING_NAME = 'gitgitlab'


class AuthException(Exception):

    """Token could not be obtained."""

    pass


def get_token(username='gitlab'):
    """Get the token from the keyring. If there is no token, request it and store it.

    :return str: The user's Gitlab token.

    """
    token = keyring.get_password(KEYRING_NAME, username)
    if not token:
        reset_token(username)
    token = keyring.get_password(KEYRING_NAME, username)
    return token


def reset_token(username):
    """Request the token from the user and store it in the keyring.

    :raise AuthException: if the token could not be obtained from the user.

    """
    token = getpass('Token: ')
    if not token:
        raise AuthException('No token')
    keyring.set_password(KEYRING_NAME, username, token)
