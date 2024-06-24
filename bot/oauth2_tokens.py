import logging
from datetime import datetime, timedelta

import requests

from bot.common import bot_creds

discord_oauth2_logger = logging.Logger(__name__)


""""""
client_id = bot_creds["PUBLIC_KEY"]
client_secret = bot_creds["CLIENT_SECRET"]
redirect_uri = "http://localhost:8000/callback"
scope = "identify email messages.read messages.write"
token_url = "https://discord.com/api/oauth2/token"
""""""


class Oauth2Tokens:
    TOKEN_URL = "https://discord.com/api/oauth2/token"

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Oauth2Tokens, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        initial = not (
            hasattr(self, "_access_token")
            and hasattr(self, "_token_expiry")
            and hasattr(self, "_refresh_token")
        )
        if initial:
            self._access_token: str
            self._token_expiry: datetime
            self._refresh_token: str
            self._load_access_token()

    def expiry_in(self, seconds: int = 0):
        if datetime.now() + timedelta(seconds=seconds) >= self._token_expiry:
            self.refresh_access_token()

    def refresh_access_token(self):
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
            "redirect_uri": redirect_uri,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.TOKEN_URL, data=data, headers=headers)
        if response.status_code >= 400:
            discord_oauth2_logger.error(
                msg=(
                    "Error when refreshing access token. "
                    f"status_code={response.status_code}. "
                    f"response: {response.json()}"
                )
            )

        response_data = response.json()
        self._access_token = response_data["access_token"]
        self._token_expiry = datetime.now() + timedelta(
            seconds=response_data["expires_in"]
        )
        discord_oauth2_logger.info(msg="Access token refreshed.")

    def _load_access_token(self):
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": "YOUR_AUTHORIZATION_CODE",
            "redirect_uri": redirect_uri,
            "scope": scope,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.TOKEN_URL, data=data, headers=headers)

        import pdb

        pdb.set_trace()
        if response.status_code >= 400:
            discord_oauth2_logger.error(
                msg=(
                    "Error when obtaining access token. "
                    f"status_code={response.status_code}. "
                    f"response: {response.json()}"
                )
            )

        response_data = response.json()
        self._access_token = response_data["access_token"]
        self._refresh_token = response_data["refresh_token"]
        self._token_expiry = datetime.now() + timedelta(
            seconds=response_data["expires_in"] - 10
        )
        discord_oauth2_logger.info(msg="Access token obtained.")

    def get_access_token(self):
        return self._access_token
