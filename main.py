from typing import Optional, Callable
from os import getenv
import logging

from fastapi import FastAPI
from requests.exceptions import HTTPError

import psycopg2

from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_client import Gauge

from create_bot import get_bot, get_bots, create_bot, create_bot_token, get_teams
from db import (
    get_bot as get_bot_db,
    store_bot,
    claim_bot,
    unclaim_bot,
    unclaimed_bots,
    sync_token,
    sync_tokens,
    stored_bot,
)

app = FastAPI()

conn = psycopg2.connect(
    host=getenv("DB_HOST"),
    database=getenv("DB_DB"),
    user=getenv("DB_USER"),
    password=getenv("DB_PASS"),
)


def bots_total() -> Callable[[metrics.Info], None]:
    """
    Export the number of free bots left in the db
    """
    METRIC = Gauge("bots_total", "bots in the db", labelnames=("status",))

    def instrumentation(info: metrics.Info) -> None:
        METRIC.labels("free").set(unclaimed_bots(conn))

    return instrumentation


Instrumentator().add(bots_total()).instrument(app).expose(app)


@app.get("/")
def read_root():
    return {"cool": "beans"}


@app.post("/bot/create")
def new_bot(store: bool = False):
    """
    Create a new discord application, and generate a bot token
    Optional: store in a local db
    """

    # get next team with room
    new_id = ""
    teams = get_teams()
    while not new_id:
        team = teams.pop()
        logging.info(f"using {team}")
        new_id = create_bot(team)

    logging.info(f"new bot: {new_id}")

    try:
        new_token = create_bot_token(new_id)
    except:
        logging.error("Unable to generate bot token")
        return {"id": new_id}

    if not new_token:
        return {"id": new_id}

    if store:
        if store_bot(conn, new_id, new_token):
            new_token = "<redacted>"

    return {"id": new_id, "token": new_token}


@app.post("/bot/store")
def store_bot(bot_id: str, bot_token: str, claimed: bool = False):
    """
    Store an existing bot in the db
    Optional: set as claimed (in use)
    """

    if store_bot(conn, bot_id, bot_token):
        return {"id": bot_id}
    else:
        return {}


@app.get("/bot/get")
def get_db_bot(claimed: bool = False):
    """
    Get a bot from the db
    Optional: get claimed bot
    """

    bot = get_bot_db(conn, claimed)

    if bot:
        return {"id": bot[0], "token": bot[1]}
    else:
        return {}


@app.put("/bot/claim")
def claim_bot(bot_id: str):
    """
    Set a bot as claimed in the db
    """

    if get_bot_db(conn, bot_id):
        return {"id": bot_id}
    else:
        return {}


@app.put("/bot/free")
def free_bot(bot_id: str):
    """
    Set a bot as unclaimed in the db
    """

    if unclaim_bot(conn, bot_id):
        return {"id": bot_id}
    else:
        return {}


@app.put("/bot/sync")
def sync_bot(bot_id: str = ""):
    """
    Sync a bots token in the db with current value
    """

    if bot_id:

        bot = get_bot(bot_id)
        if not bot:
            return {"error": "no bot found"}
        if "bot" not in bot:
            try:
                new_token = create_bot_token(bot["id"])
            except:
                logging.error("Unable to generate bot token")
                return {"error": "app is not a bot"}
            bot["bot"] = {"token": new_token}

        result = sync_token(conn, bot)
        if result:
            return {"id": result}
        else:
            return {}

    else:

        bots = get_bots()
        if not bots:
            return {"error": "no bots found"}
        bots = [x for x in bots if "bot" in x]

        result = sync_tokens(conn, bots)
        if result:
            return {"id": result}
        else:
            return {}


@app.put("/bot/load")
def load_bots():
    """
    Adds all a users bots to the db
    """

    bots = get_bots()
    if not bots:
        return {"error": "no bots found"}

    for bot in bots:
        if "bot" in bot:
            if stored_bot(conn, bot["id"]):
                sync_bot(bot["id"])
            else:
                store_bot(bot["id"], bot["bot"]["token"], True)
                return {}


@app.get("/bot/unclaimed")
def unclaimed_bot_count():
    """
    Get unclaimed bots from db
    """

    unclaimed = unclaimed_bots(conn)

    return {"count": unclaimed}
