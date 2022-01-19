import psycopg

from datetime import date
import random
import string 

from ...scraper.scraper_types import HansardLink, SpeechLink, DebateLink, SessionDate
from ...db.db import get_db

test_speechs = [
    SpeechLink(
        type = "Vote",
        topic = "Test topic",
        speaker = "sIMon o'connor",
        html = "<h1>Hello World</h1>",
    ),
    SpeechLink(
        type = "Question",
        topic = "Another Test topic",
        speaker = "Chlöe SwarbRICk",
        html = "<h1>Hello World2</h1>"
    ),
    SpeechLink(
        type = "Unknown",
        topic = None,
        speaker = None,
        html = "<h1>Hello World3</h1>"
    )
]

test_debates = [
    DebateLink(
        title = "Test Debate 1",
        type = "First Reading",
        speeches = test_speechs,
    ),
    DebateLink(
        title = "Test Debate 2",
        type = "Unknown",
        speeches = [],
    )
]

test_dates = SessionDate(
    actual_date = date.fromisoformat("2021-01-17"),
    continued_from = date.fromisoformat("2021-01-16"),
)

random_id = ''.join(random.choice(string.ascii_letters) for _ in range(10))

test_document = HansardLink(
    title = "Test Documents" + random_id,
    dates = test_dates,
    debates = test_debates,
    url = "www.test_url.com2" + random_id,
)


# TODO: setup a proper testing database 

def test_insert_document():
    db = get_db()

    # I definitly need a better way of doing this
    query = """
        INSERT INTO document (title, url, start_date, continued_date) 
        VALUES (%(title)s, %(url)s, %(start_date)s, %(continued_date)s)
        RETURNING document_id;
    """

    with db.getconn() as conn, conn.cursor() as cur:
        cur.execute (query, 
        {
            "title": test_document.title,
            "url": test_document.url,
            "start_date": test_document.dates.actual_date,
            "continued_date": test_document.dates.continued_from,
        })
        result = cur.fetchone()

        cur.execute("""SELECT document_id FROM document WHERE title = %s""", [test_document.title])
        key = cur.fetchone()

        if result != None and key != None:
            assert(result[0] == key[0])
        else:
            raise Exception("Get nothing")

