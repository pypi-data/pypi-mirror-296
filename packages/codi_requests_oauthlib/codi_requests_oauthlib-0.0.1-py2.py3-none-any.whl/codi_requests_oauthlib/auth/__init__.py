"""
Handles OAuth authentication and token management
"""
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import time


class OAuthClient:
    def __init__(self, **kwargs):
        """
        Initializes an instance of the Auth class.

        :param client_id: The client ID for authentication.
        :type client_id: str
        :param client_secret: The client secret for authentication.
        :type client_secret: str
        :param token_url: The URL for token retrieval.
        :type token_url: str
        :param base_url: The base URL for API requests.
        :type base_url: str
        :param scope: The scope of the authentication.
        :type scope: str
        """
        self.client_id = kwargs.get('client_id')
        self.client_secret = kwargs.get('client_secret')
        self.token_url = kwargs.get('token_url')
        self.base_url = kwargs.get('base_url')
        self.scope = kwargs.get('scope')
        self.client = BackendApplicationClient(client_id=self.client_id)
        self.session = OAuth2Session(client=self.client)
        self.session.fetch_token(
            token_url=self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope
        )

    @property
    def session(self):
        """Initializes and returns an OAuth session."""
        if self.is_token_expired():
            self.get_token()
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    def expire_token(self):
        """Expires the current token."""
        self.session.token['expires_at'] = time.time() - 1

    def is_token_expired(self):
        """Checks if the current token is expired."""
        if self._session.token is None or self._session.token == {}:
            return True
        return self._session.token['expires_at'] < time.time()

    # def get_oauth_session(self):

    def get_token(self):
        """Fetches a new token and saves it."""
        self._session.token = self._session.fetch_token(
            token_url=self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope
        )
