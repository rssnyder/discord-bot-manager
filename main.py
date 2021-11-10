from typing import Optional
import logging

from fastapi import FastAPI
from requests.exceptions import HTTPError

from create_bot import create_bot, create_bot_token, store_bot, TEAMS

app = FastAPI()


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
        store_bot(getenv("DST_DB"), getenv("DST_DB_TABLE"), new_id, new_token)
        
    return {"id": new_id, "token": new_token}
