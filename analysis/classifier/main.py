
from pathlib import Path
import sys

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.db.db import get_db


#######################################################
#                    Setting Up                       #
#######################################################

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

templates = Jinja2Templates(directory="templates")
pool = get_db()
conn = pool.getconn()

#######################################################
#                    Routes                           #
#######################################################


# Load a random template and display it
@app.get("/", response_class=HTMLResponse)
async def get_random_speech(request: Request):
    return serve_speech(request)

@app.post("/classify_speech")
async def classify_speech(request: Request):
    form_data = await request.form()
    speech_id = form_data["speech-id"]
    check_tags = [topic for (topic, value) in form_data.items() if value == "on"]
    return serve_speech(request)

#######################################################
#                    Methods                          #
#######################################################

def serve_speech(request: Request):
    speech_html, speech_id = get_speech_html()
    topic_ids, topic_names = zip(*get_topics())
    args = {
        "request": request,
        "speech_html": speech_html, 
        "topics": topic_names,
        "speech_id": speech_id,
    }
    return templates.TemplateResponse("show_speech.html", args)

def get_speech_html() -> tuple[str, int]:
    return "<h1>Speech-Contents</h1>", 1

def get_topics():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, description
            FROM topic
            ORDER BY description
        """)
        topics = cur.fetchall()
        return topics
