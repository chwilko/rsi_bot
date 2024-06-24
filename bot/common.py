import json
from typing import Dict, TypedDict


class Creds(TypedDict):
    NAME: str
    APPLICATION_ID: str
    PUBLIC_KEY: str
    CLIENT_SECRET: str
    TOKEN: str
    url: str


with open(".keys.json", "r") as f:
    creds: Dict[str, Creds] = json.load(f)

bot_creds = creds["discord_bot"]
