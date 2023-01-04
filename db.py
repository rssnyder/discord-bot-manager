import logging


def store_bot(conn, bot_id: str, bot_token: str, claimed: bool = False) -> str:
    """
    Store bot into database
    """

    q = """INSERT INTO newbots(CLIENTID, TOKEN, CLAIMED)
            VALUES(%s, %s, %s)
            RETURNING CLIENTID;"""

    cur = conn.cursor()

    cur.execute(q, (bot_id, bot_token, claimed))
    result = cur.fetchone()[0]

    if result:
        logging.info(f"stored: {result}")
        conn.commit()

    cur.close()

    return result


def stored_bot(conn, bot_id: str) -> bool:
    """
    Check if bot in db
    """

    q = """SELECT CLIENTID FROM newbots
            WHERE CLIENTID = %s
            LIMIT 1;"""

    cur = conn.cursor()

    cur.execute(q, (bot_id,))

    result = False
    if cur.fetchone():
        result = True

    conn.commit()

    cur.close()

    return result


def get_bot(conn, claimed: bool = False) -> tuple:
    """
    Get bot from db
    """

    q = """SELECT CLIENTID, TOKEN FROM newbots
            WHERE CLAIMED = %s
            LIMIT 1;"""

    cur = conn.cursor()

    cur.execute(q, (claimed,))
    result = cur.fetchone()

    if result:
        logging.debug(f"got: {result}")
        conn.commit()

    cur.close()

    return result


def get_bot_id(conn, id: str = "") -> tuple:
    """
    Get specific bot from db
    """

    q = """SELECT CLIENTID, TOKEN FROM newbots
            WHERE CLIENTID = %s
            LIMIT 1;"""

    cur = conn.cursor()

    cur.execute(q, (id,))
    result = cur.fetchone()

    cur.close()

    return result


def claim_bot(conn, bot_id: str) -> str:
    """
    Set a bot as claimed
    """

    q = """UPDATE newbots
            SET CLAIMED = true
            WHERE CLIENTID = %s
            RETURNING CLIENTID;;"""

    cur = conn.cursor()

    cur.execute(q, (bot_id,))
    result = cur.fetchone()

    if result:
        logging.info(f"claimed: {result}")
        conn.commit()

    cur.close()

    return result


def unclaim_bot(conn, bot_id: str) -> str:
    """
    Set a bot as unclaimed
    """

    q = """UPDATE newbots
            SET CLAIMED = false
            WHERE CLIENTID = %s
            RETURNING CLIENTID;;"""

    cur = conn.cursor()

    cur.execute(q, (bot_id,))
    result = cur.fetchone()

    if result:
        logging.info(f"unclaimed: {result}")
        conn.commit()

    cur.close()

    return result


def sync_token(conn, bot: dict) -> str:
    """
    Make sure token in db is accurate
    """

    q = """UPDATE newbots
            SET TOKEN = %s
            WHERE CLIENTID = %s
            RETURNING CLIENTID;;"""

    cur = conn.cursor()

    cur.execute(q, (bot["bot"]["token"], bot["id"]))
    result = cur.fetchone()

    if result:
        logging.info(f"sycned: {result}")
        conn.commit()

    cur.close()

    return result


def sync_tokens(conn, bots: list = []) -> bool:
    """
    Make sure all tokens in db are accurate
    """

    q = """UPDATE newbots
            SET TOKEN = %s
            WHERE CLIENTID = %s
            RETURNING CLIENTID;;"""

    cur = conn.cursor()

    result = True
    for bot in bots:
        cur.execute(q, (bot["bot"]["token"], bot["id"]))
        result = cur.fetchone()

        if result:
            logging.info(f"updated: {result}")
        else:
            result = False

    conn.commit()

    cur.close()

    return result


def unclaimed_bots(conn) -> int:
    """
    Get the number of unclaimed bots
    """

    q = """SELECT COUNT(CLIENTID) FROM newbots
            WHERE NOT claimed;"""

    cur = conn.cursor()

    cur.execute(q)
    result = cur.fetchone()[0]

    if result:
        logging.debug(f"unclaimed: {result}")

    cur.close()

    return result


def all_bots(conn) -> int:
    """
    Get the number of bots
    """

    q = """SELECT COUNT(CLIENTID) FROM newbots;"""

    cur = conn.cursor()

    cur.execute(q)
    result = cur.fetchone()[0]

    if result:
        logging.debug(f"total: {result}")

    cur.close()

    return result
