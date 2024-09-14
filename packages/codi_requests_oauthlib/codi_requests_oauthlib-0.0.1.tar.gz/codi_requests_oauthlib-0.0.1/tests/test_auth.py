from dotenv import dotenv_values
import pytest

from codi_requests_oauthlib.auth import OAuthClient
from datetime import datetime


class TestAuth():

    @pytest.fixture
    def auth(self):
        config = dotenv_values("tests.env")
        return OAuthClient(
            client_id=config.get("CLIENT_ID"),
            client_secret=config.get("CLIENT_SECRET"),
            token_url=config.get("TOKEN_URL"),
            base_url=config.get("BASE_URL"),
            scope=config.get("SCOPE")
        )

    def test_config(self):
        config = dotenv_values("tests.env")
        assert 'CONFIG_TEST' in config.keys()

    def test_get_oauth_session(self, auth):
        assert auth.session is not None

    def test_get_token(self, auth):
        token = auth.session.token

        assert token is not None
        assert 'access_token' in token
        assert 'token_type' in token
        assert 'expires_in' in token
        assert 'scope' in token
        assert 'expires_at' in token

    def test_expire_token(self, auth):
        assert auth.is_token_expired() is False
        auth.expire_token()
        assert auth.is_token_expired() is True
        session = auth.session
        assert auth.is_token_expired() is False
