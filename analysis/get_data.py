# To put the data into the correct database this must be run with the ENV environment variable set to "PROD"

import os 
import logging
import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parent.parent))

from libhansard.db.db import get_db
from libhansard.db.functions.insert_document import insert_document
from libhansard.scraper.main import scrape

log_file = "get_data.logs"

ENV = os.getenv('ENV') or "DEV"

print(f"Running in environment: {ENV}")
print(f"Logging to file: {log_file}")

pool = get_db() 
conn = pool.getconn()

scraper = scrape(
    stop = "2021-12-01",
    seconds_delay = 5,
    log_level = logging.DEBUG,
    log_file = log_file
)

for document in scraper:
    logging.info(f"Inserting {document.title}")
    insert_document(conn, document)


