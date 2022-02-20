
from pathlib import Path
import sys

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.db.db import get_db
from libhansard.db.query_cache import QueryCache


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
    return templates.TemplateResponse("show_debate.html", {"request": request, "topics": topics, **debate})

# This is called once a classified speech is submitted 
#@app.post("/classify_debate")
#async def classify_debate(request: Request):
#    form_data = await request.form()
#    debate_id = form_data["debate-id"]
#    checked_tags = [topic for (topic, value) in form_data.items() if value == "on"]
#    return get_random_debate()

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
