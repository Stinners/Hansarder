
# Boilerplate to make relative imports work when this is run as a script
if __name__ == "__main__" and __package__ is None:
    import sys, os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    __package__ = str("classifier")


from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


#######################################################
#                    Setting Up                       #
#######################################################

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))

templates = Jinja2Templates(directory="templates")

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
    args = {
        "request": request,
        "speech_html": speech_html, 
        "topics": get_topics(),
        "speech_id": speech_id,
    }
    return templates.TemplateResponse("show_speech.html", args)

def get_speech_html() -> tuple[str, int]:
    return "<h1>Speech-Contents</h1>", 1

def get_topics():
    topics = ["Climate", "Covid", "Defense", "Enconomy", "Education"] * 4
    topics.sort()
    return topics
