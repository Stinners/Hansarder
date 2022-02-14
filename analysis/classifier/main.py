
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
    return templates.TemplateResponse("show_speech.html", {"request": request, "topics": topics})

# This is called once a classified speech is submitted 
@app.post("/classify_speech")
async def classify_speech(request: Request):
    form_data = await request.form()
    speech_id = form_data["speech-id"]
    checked_tags = [topic for (topic, value) in form_data.items() if value == "on"]
    return get_random_speech()

# "This is called to get a speech in the first place
@app.get("/get_speech")
async def serve_speech():
    return get_random_speech

#######################################################
#                    Methods                          #
#######################################################

def get_random_speech():
    with conn.cursor() as cur:
        cur.execute(queries.get_query("select_speech.sql"))
        speech = cur.fetchone()

        if speech is None: return None

        return {
            "speech_id": speech[0],
            "debate_id": speech[1],
            "speech_type": speech[2],
            "html": speech[3],
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
