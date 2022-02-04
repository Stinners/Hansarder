
import pytest
import dotenv

from datetime import date
import random
import string 
import os
import subprocess

from ...scraper.scraper_types import HansardLink, SpeechLink, DebateLink, SessionDate
from ...db.db import get_db
from ...db.functions.insert_document import insert_document

###################################################################
#                          Data                                   #
###################################################################

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
        speaker = "Chlöe swarbRICk",
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

###################################################################
#                         Fixtures                                #
###################################################################

@pytest.fixture(autouse=True)
def set_env_test():
    # Set the current environment to test 
    dotenv.load_dotenv(".env_test")

    assert os.getenv("ENV") == "TEST", "Failed to set environment variable"

    # Initiate the testing database, making sure it wasn't already there
    subprocess.call(["dbmate", "-e", "TEST_DATABASE_URL", "drop"], stdout=subprocess.DEVNULL)
    subprocess.call(["dbmate", "-e", "TEST_DATABASE_URL", "up"], stdout=subprocess.DEVNULL)

    yield 

    # Drop the test database after the test 
    subprocess.call(["dbmate", "-e", "TEST_DATABASE_URL", "drop"], stdout=subprocess.DEVNULL)

###################################################################
#                         Tests                                   #
###################################################################

def test_insert_document():
    pool = get_db()

    with pool.getconn() as conn:
        insert_document(conn, test_document)
    
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM document""")
            doc_id, title, url, actual_date, continued_date = cur.fetchone()   # type: ignore 

            cur.execute("""SELECT * FROM debate ORDER BY id""")
            debates = cur.fetchall()

            cur.execute("""
                SELECT s.id, s.html, m.name, p.name FROM speech s
                LEFT JOIN member m ON m.id = s.member
                LEFT JOIN party p ON m.party = p.id;
            """)
            speeches = cur.fetchall()

            # Document Asserts 
            assert url == test_document.url
            assert title == test_document.title
            assert actual_date == test_document.dates.actual_date
            assert continued_date == test_document.dates.continued_from

            # Debate Asserts 
            assert len(debates) == 2 
            assert debates[0][3] == debates[1][3] == doc_id
            assert debates[0][1] == "Test Debate 1"

            # Speech Asserts 
            assert len(speeches) == 3
            assert speeches[1][2] == 'Chlöe Swarbrick'
            assert speeches[1][3] == "Green"

