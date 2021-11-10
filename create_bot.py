#!/usr/bin/python3
import logging
import sqlite3
from os import getenv
from json import loads

from requests import post, exceptions


def create_bot(team: str) -> str:
    """
    Create a new bot in a team
    """

    if not team:
        return None

    response = post(
        "https://discord.com/api/v9/applications",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Authorization": getenv("AUTH"),
            "Connection": "keep-alive"
        },
        json={
            "name": "Discord Stock Ticker",
            "team_id": team
        }
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

    if not bot_id:
        return None

    response = post(
        f"https://discord.com/api/v9/applications/{bot_id}/bot",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/json",
            "Authorization": getenv("AUTH"),
            "Connection": "keep-alive"
        }
    )

    response.raise_for_status()

    try:
        return response.json().get("token", "")
    except:
        logging.error(response.text)
        return ""


def store_bot(location: str, table: str, bot_id: str, bot_token: str) -> None:
    """
    Store bot into database
    """

    con = sqlite3.connect(location)
    con.execute("insert into newbots values (?, ?)", (bot_id, bot_token))
    con.commit()
    con.close()


if __name__ == "__main__":

    teams = loads(getenv("TEAMS"))

    new_id = ""
    while not new_id:
        team = teams.pop()
        print(f"using {team}")
        new_id = create_bot(team)

    new_token = create_bot_token(new_id)
    if new_id and new_token:
        print(f"{new_id} '{new_token}'")
        store_bot(getenv("DST_DB"), getenv("DST_DB_TABLE"), new_id, new_token)
        print("saved")
    else:
        print(new_id)
