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


def get_bot(conn, claimed: bool = False) -> tuple:
    """
    Store bot into database
    """

    q = """SELECT CLIENTID, TOKEN FROM newbots
            WHERE CLAIMED = %s
            LIMIT 1;"""

    cur = conn.cursor()

    cur.execute(q, (claimed,))
    result = cur.fetchone()

    if result:
        logging.info(f"got: {result}")
        conn.commit()

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
        logging.info(f"unclaimed: {result}")

    cur.close()

    return result
