import logging
import sqlite3
from os import getenv
from json import loads

from requests import post, get, exceptions


def create_bot(team: str) -> str:
    """
    Create a new bot in a team
    """

    response = post(
        "https://discord.com/api/v9/applications",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Authorization": getenv("AUTH"),
            "Connection": "keep-alive",
        },
        json={"name": "Discord Stock Ticker", "team_id": team},
    )

    if response.status_code == 403:
        logging.error(response.text)
        return ""

    response.raise_for_status()

    try:
        return response.json().get("id", "")
    except:
        logging.error(response.text)
        return ""


def create_bot_token(bot_id: str) -> str:
    """
    Create a new token for a new bot
    """

    response = post(
        f"https://discord.com/api/v9/applications/{bot_id}/bot",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Authorization": getenv("AUTH"),
            "Connection": "keep-alive",
        },
    )

    response.raise_for_status()

    try:
        return response.json().get("token", "")
    except:
        logging.error(response.text)
        return ""


def get_teams() -> list:
    """
    List all teams a user is in
    """

    response = get(
        "https://discord.com/api/v9/teams",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Authorization": getenv("AUTH"),
            "Connection": "keep-alive",
        },
    )

    response.raise_for_status()

    try:
        return [x["id"] for x in response.json()]
    except:
        logging.error(response.text)
        return []


def get_bot(bot_id: str) -> dict:
    """
    Get a bot from discord
    """

    response = get(
        f"https://discord.com/api/v9/applications/{bot_id}",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Authorization": getenv("AUTH"),
            "Connection": "keep-alive",
        },
    )

    response.raise_for_status()

    try:
        return response.json()
    except:
        logging.error(response.text)
        return {}


def get_bots() -> list:
    """
    List all bots that a user owners, including teams
    """

    response = get(
        "https://discord.com/api/v9/applications?with_team_applications=true",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Authorization": getenv("AUTH"),
            "Connection": "keep-alive",
        },
    )

    response.raise_for_status()

    try:
        return response.json()
    except:
        logging.error(response.text)
        return []
