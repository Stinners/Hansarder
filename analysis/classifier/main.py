
from pathlib import Path
from typing import List, Tuple
import sys
from dataclasses import dataclass

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.db.db import get_db
from libhansard.db.query_cache import QueryCache

@dataclass 
class Statistics:
    num_debates_classified: int
    num_by_topic: List[Tuple[str, int]]


#######################################################
#                    Setting Up                       #
#######################################################

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

templates = Jinja2Templates(directory="templates")
pool = get_db()
conn = pool.getconn()

queries = QueryCache(Path(__file__).parent / "queries")

#######################################################
#                    Routes                           #
#######################################################

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    topics = [topic for (_, topic) in get_topics()]
    debate = get_random_debate()
    return templates.TemplateResponse("show_debate.html", {"request": request, "topics": topics, "page": "Classify", **debate})

# This is called once a classified speech is submitted 
@app.post("/classify_debate")
async def classify_debate(request: Request):
    form_data = await request.form()
    debate_id = int(form_data["debate-id"])
    checked_tags = [topic for (topic, value) in form_data.items() if value == "on"]
    insert_classifications(debate_id, checked_tags)
    return await home(request)

@app.get("/statistics")
def statistics(request: Request):
    stats = get_statistics()
    return templates.TemplateResponse("show_statistics.html", {"request": request, "page": "Statistics", "stats": stats})


#######################################################
#                    Utilities                        #
#######################################################

def get_random_debate():
    with conn.cursor() as cur:
        cur.execute(queries.get_query("select_debate"))
        debate = cur.fetchone()

        if debate is None: 
            raise ValueError("Couldn't read debate from db")

        return {
            "debate_id": debate[0],
            "debate_title": debate[1],
            "html": debate[2],
        }

def get_topics():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, description
            FROM topic
            ORDER BY description
        """)
        topics = cur.fetchall()
        return topics

def insert_classifications(debate_id: int, topics: List[str]):

        if topics == []:
            topics = ["None"]

        parameters = [{"debate_id": debate_id, "certanty": 0.95, "topic": topic}
                      for topic in topics]

        with conn.cursor() as cur:
            cur.executemany(queries.get_query("add_classification"), parameters)
            conn.commit()

def get_statistics() -> Statistics:
    with conn.cursor() as cur:
        cur.execute(queries.get_query("get_number_classified"))
        num_classifed = cur.fetchone()

        cur.execute(queries.get_query("get_classified_numbers"))
        classified_numbers = cur.fetchall()

        if num_classifed is None or classified_numbers is None:
            raise ValueError("Couldn't read statistics from database")
        else:
            num_classifed = num_classifed[0]

        stats = Statistics(num_classifed, classified_numbers)

        return stats

