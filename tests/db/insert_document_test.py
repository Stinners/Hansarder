
from datetime import date
import random
import string 

from ...scraper.scraper_types import HansardLink, SpeechLink, DebateLink, SessionDate
from ...db.db import get_db
from ...db.functions.insert_document import insert_document


test_speechs = [
    SpeechLink(
        type = "Vote",
        topic = "Test topic",
        speaker = "sIMon o'connor",
        html = "<h1>Hello World</h1>",
        processed_text = None,
    ),
    SpeechLink(
        type = "Question",
        topic = "Another Test topic",
        speaker = "Chlöe SwarbRICk",
        html = "<h1>Hello World2</h1>",
        processed_text = None,
    ),
    SpeechLink(
        type = "Unknown",
        topic = None,
        speaker = None,
        html = "<h1>Hello World3</h1>",
        processed_text = None,
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

def get_query(name):
    with open("db/queries/" + name + ".sql", 'r') as f:
        return f.read()

# TODO: setup a proper testing database 

pool = get_db()

def test_insert_document():
    with pool.getconn() as conn:
        insert_document(conn, test_document)
