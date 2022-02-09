# To put the data into the correct database this must be run with the ENV environment variable set to "PROD"

import os 
import logging
import pathlib
import sys

sys.path.insert(1, str(pathlib.Path(__file__).parent.parent))

# Boilerplate to make relative imports work when this is run as a script
#if __name__ == "__main__" and __package__ is None:
#    import sys
#    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#    sys.path.insert(1, parent_dir)
#    __package__ = "analyis"

from libhansard.db.db import get_db
from libhansard.db.functions.insert_document import insert_document
from libhansard.scraper.main import scrape
import pdb; pdb.set_trace()

log_file = "get_data.logs"

print(f"Running in environment: {os.getenv('ENV')}")
print(f"Logging to file: {log_file}")

pool = get_db() 
conn = pool.getconn()

scraper = scrape(
    stop = "2021-12-1",
    seconds_delay = 5,
    log_level = logging.DEBUG,
    log_file = log_file
)

for document in scraper:
    logging.info(f"Inserting f{document.title}")
    insert_document(conn, document)


