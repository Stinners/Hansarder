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

pool = get_db()

def insert_document_head(doc: HansardLink, conn: Connection) -> Optional[int]:
    with conn.cursor() as curr:
        curr = conn.cursor()
        curr.execute (
            """
            INSERT INTO document (title, url, start_date, continued_date) 
            VALUES (%(title)s, %(url)s, %(start_date)s, %(continued_date)s)
            RETURNING document_id;
            """,
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
            """
            INSERT INTO debate (title, document, debate_type)
            VALUES (
                %(title)s, 
                %(document_id)s, 
                (SELECT debate_type_id FROM debate_type WHERE debate_type.debate_type = %(debate_type)s)
            )
            RETURNING debate_id;
            """,
            debate_values
        )
        fetch_id = curr.fetchone()
        return fetch_id[0] if fetch_id is not None else None

def insert_speeches(speeches: List[SpeechLink], debate_key: int, conn: Connection):
    with conn.cursor() as curr:
        speech_mapping = [{
            "topic": it.topic,
            "speaker": it.speaker,
            "html": it.html,
            "speech_type": it.type,
            "debate_id": debate_key,
        } for it in speeches]

        curr.executemany(
            """
            WITH ins (topic, speaker, html, speech_type, debate_id) AS
            ( VALUES 
                (%(topic)s, %(speaker)s, %(html)s, %(speech_type)s, %(debate_id)s)
            )
            INSERT INTO speech 
                (topic, speaker_id, html, speech_type_id, debate_id)
            SELECT 
                ins.topic, member.member_id, ins.html, speech_type.speech_type_id, ins.debate_id
            FROM 
                ins 
                LEFT JOIN member ON ins.speaker ILIKE member.name
                LEFT JOIN speech_type ON ins.speech_type = speech_type.description;
            """,
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





