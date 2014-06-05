"""Request and store the gitlab token in the keyring."""

from getpass import getpass
import keyring
from urlparse import urljoin
import webbrowser

from gitgitlab import client

KEYRING_NAME = 'gitgitlab'


class AuthException(Exception):

    """Token could not be obtained."""

    pass


def get_token(gitlab_uri=None):
    """Get the token from the keyring. If there is no token, request it and store it.

    :param str gitlab_uri: URI of the Gitlab server. By default, it takes the URI from the configuration.
    :return str: The user's Gitlab token.
    """
    if gitlab_uri is None:
        gitlab_uri = client.get_gitlab_url()
    token = keyring.get_password(KEYRING_NAME, gitlab_uri)
    if not token:
        reset_token(gitlab_uri)
    token = keyring.get_password(KEYRING_NAME, gitlab_uri)
    return token


def reset_token(gitlab_uri=None):
    """Request the token from the user and store it in the keyring.

    :param str gitlab_uri: URI of the Gitlab server. By default, it takes the URI from the configuration.

    :raise AuthException: if the token could not be obtained from the user.

    """
    if gitlab_uri is None:
        gitlab_uri = client.get_gitlab_url()
    account_url = urljoin(gitlab_uri, 'profile/account')
    print 'Please provide your Gitlab token. You can find it on your account page, {}'.format(
        account_url)
    webbrowser.open(account_url)
    token = getpass('Token: ')
    if not token:
        raise AuthException('No token')
    keyring.set_password(KEYRING_NAME, gitlab_uri, token)
