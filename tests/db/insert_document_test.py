from psycopg import Connection

from datetime import date
import random
import string 
from typing import Optional, List

from ...scraper.scraper_types import HansardLink, SpeechLink, DebateLink, SessionDate
from ...db.db import get_db

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

def insert_document_head(doc: HansardLink, conn: Connection) -> Optional[int]:
    with conn.cursor() as curr:
        curr = conn.cursor()
        curr.execute (
            get_query("insert_document"),
            {
                "title": doc.title,
                "url": doc.url,
                "start_date": doc.dates.actual_date,
                "continued_date": doc.dates.continued_from,
            }
        )
        fetch_id = curr.fetchone()
        return fetch_id[0] if fetch_id is not None else None

def insert_debate_head(debate: DebateLink, doc_key: int, conn: Connection) -> Optional[int]:
    with conn.cursor() as curr:
        curr = conn.cursor()
        debate_values = {"title": debate.title, "debate_type": debate.type, "document_id": doc_key}
        curr.execute(
            get_query("insert_debate"),
            debate_values
        )
        fetch_id = curr.fetchone()
        return fetch_id[0] if fetch_id is not None else None

def insert_speeches(speeches: List[SpeechLink], debate_key: int, conn: Connection):
    with conn.cursor() as curr:
        speech_mapping = [{
            "topic": it.topic,
            "member": it.speaker,
            "html": it.html,
            "speech_type": it.type,
            "debate_id": debate_key,
            "position": i,
        } for (i, it) in enumerate(speeches)]

        curr.executemany(
            get_query("insert_speech"),
            speech_mapping
        )

def insert_document(document):
    with pool.getconn() as conn:
        doc_key = insert_document_head(document, conn)

        if doc_key == None:
            raise Exception("Couldn't get key value from document")

        for debate in test_debates:
            debate_key = insert_debate_head(debate, doc_key, conn)
        
            if debate_key == None:
                raise Exception("Couldn't get key value from debate")
       
            insert_speeches(debate.speeches, debate_key, conn)

def test_insert_document():
    insert_document(test_document)
