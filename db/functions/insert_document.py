from psycopg import Connection, Cursor

from typing import Optional, List

from ...scraper.scraper_types import HansardLink, SpeechLink, DebateLink

# TODO come up with a better way to do this
def get_query(name):
    with open("db/queries/" + name + ".sql", 'r') as f:
        return f.read()

def insert_document_head(doc: HansardLink, cur: Cursor) -> Optional[int]:
    cur.execute (
        get_query("insert_document"),
        {
            "title": doc.title,
            "url": doc.url,
            "start_date": doc.dates.actual_date,
            "continued_date": doc.dates.continued_from,
        }
    )
    fetch_id = cur.fetchone()
    return fetch_id[0] if fetch_id is not None else None

def insert_debate_head(debate: DebateLink, doc_key: int, cur: Cursor) -> Optional[int]:
    debate_values = {"title": debate.title, "debate_type": debate.type, "document_id": doc_key}
    cur.execute(
        get_query("insert_debate"),
        debate_values
    )
    fetch_id = cur.fetchone()
    return fetch_id[0] if fetch_id is not None else None

def insert_speeches(speeches: List[SpeechLink], debate_key: int, cur: Cursor):
    speech_mapping = [{
        "topic": it.topic,
        "member": it.speaker,
        "html": it.html,
        "speech_type": it.type,
        "debate_id": debate_key,
        "position": i,
    } for (i, it) in enumerate(speeches)]

    cur.executemany(
        get_query("insert_speech"),
        speech_mapping
    )



def insert_document(conn, document):
    with conn.cursor() as cur:
        try:
            # This will throw and exception if try to insert a document that's alread in the database
            doc_key = insert_document_head(document, cur)
        #TODO find the appropriate exception class here
        except:
            return 

        if doc_key == None:
            raise Exception("Couldn't get key value from document")

        for debate in document.debates:
                debate_key = insert_debate_head(debate, doc_key, cur)
            
                if debate_key == None:
                    raise Exception("Couldn't get key value from debate")
           
                insert_speeches(debate.speeches, debate_key, cur)

        conn.commit()
