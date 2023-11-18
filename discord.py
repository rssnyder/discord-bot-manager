import logging
import sqlite3
from os import getenv
from json import loads

from requests import post, get, patch, exceptions


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
        json={"name": "DST Bot", "team_id": team},
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


def create_bot_token(bot_id: str) -> bool:
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

    return True

    # token = response.json().get("token", "")
    # if token:
    #    return token
    # else:
    #    logging.error(response.text)
    #    return ""


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


def change_bot_name(token: str, name: str) -> bool:
    """
    Change the name of the bot
    """

    resp = patch(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"},
        json={"username": name},
    )

    try:
        resp.raise_for_status()
    except:
        return False

    if not resp.json().get("username", False):
        return False

    return True


def change_bot_photo(token: str, base64_photo: str) -> bool:
    """
    Change the photo of the bot
    """

    resp = patch(
        "https://discord.com/api/users/@me",
        headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"},
        json={"avatar": base64_photo},
    )

    try:
        resp.raise_for_status()
    except:
        return False

    if not resp.json().get("avatar", False):
        return False

    return True
