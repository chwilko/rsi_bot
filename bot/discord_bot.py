import logging

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from bot.common import bot_creds
from bot.oauth2_tokens import Oauth2Tokens

tasks_logger = logging.getLogger(__name__)


CHANNEL_ID = 1254525247038951498


""""""
client_id = bot_creds["PUBLIC_KEY"]
client_secret = bot_creds["CLIENT_SECRET"]
redirect_uri = "http://localhost:8000/callback"
scope = "identify email messages.read messages.write"
token_url = "https://discord.com/api/oauth2/token"
""""""


class Bot:
    N_SECONDS = 20

    def __init__(self) -> None:
        self.scheduler = BlockingScheduler()
        # Oauth2Tokens()
        self.scheduler.add_job(
            self._check_rsi,
            "cron",
            id="check_rsi",
            minute="*",
        )  # ! TODO ustawić czas

        self.scheduler.add_job(
            self._refresh_token,
            "cron",
            id="refresh_token",
            second="45",
            minute="*",
        )  # ! TODO ustawić czas

    def _check_rsi(self):
        tasks_logger.info(msg="check_rsi begin")
        # channel_id = CHANNEL_ID
        # message = 'Regular hourly message'
        # self._send_message(channel_id, message)
        tasks_logger.info(msg="check_rsi end")

    def _refresh_token(self):
        tasks_logger.info(msg="refresh_token begin")
        # oauth2_tokens = Oauth2Tokens()
        # if oauth2_tokens.expiry_in(N_SECONDS):
        #     oauth2_tokens.refresh_access_token()
        tasks_logger.info(msg="refresh_token end")

    def _send_message(self, channel_id, message):
        oauth2_tokens = Oauth2Tokens()
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": f"Bearer {oauth2_tokens.get_access_token()}",
            "Content-Type": "application/json",
        }
        payload = {
            "content": message,
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def run(self):
        self.scheduler.start()


if __name__ == "__main__":
    Bot().run()
