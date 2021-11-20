from typing import Optional, Callable
from os import getenv
import logging

from fastapi import FastAPI
from requests.exceptions import HTTPError

import psycopg2

from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_client import Gauge

from create_bot import create_bot, create_bot_token, TEAMS
from db import store_bot, get_bot, claim_bot, unclaimed_bots

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


@app.get("/bot/new")
def bot_new(store: bool = False):
    """
    Create a new discord application, and generate a bot token
    Optional: store in a local db
    """

    # get next team with room
    new_id = ""
    while not new_id:
        team = TEAMS.pop()
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

    free_bots.set(unclaimed_bots(conn))

    return {"id": new_id, "token": new_token}


@app.get("/bot/store")
def bot_store(bot_id: str, bot_token: str, claimed: bool = False):
    """
    Store an existing bot in the db
    Optional: set as claimed (in use)
    """

    if store_bot(conn, bot_id, bot_token):
        free_bots.set(unclaimed_bots(conn))
        return {"id": bot_id}
    else:
        return {}


@app.get("/bot/get")
def bot_get(claimed: bool = False):
    """
    Get a bot from the db
    Optional: get claimed bot
    """

    bot = get_bot(conn, claimed)

    if bot:
        return {"id": bot[0], "token": bot[1]}
    else:
        return {}


@app.get("/bot/claim")
def bot_get(bot_id: str):
    """
    Set a bot as claimed in the db
    """

    if claim_bot(conn, bot_id):
        free_bots.set(unclaimed_bots(conn))
        return {"id": bot_id}
    else:
        return {}


@app.get("/bot/unclaimed")
def bot_unclaimed():
    """
    Get unclaimed bots from db
    """

    unclaimed = unclaimed_bots(conn)

    return {"count": unclaimed}
