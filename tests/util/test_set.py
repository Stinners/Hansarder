


import sys
import pickle
import logging
from pathlib import Path
from typing import List

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.scraper.main import scrape
from libhansard.scraper.scraper_types import *
from libhansard.db.functions.insert_document import insert_document

# Scrape a known set of documents and store them in a pickle file
# Note this test set isn't commited to version control

##### Config 

TEST_SET_FILE = "test_set.pickle"
TEST_SET_FILE_PATH = Path(__file__).parent / TEST_SET_FILE

START_URL = "https://www.parliament.nz/en/pb/hansard-debates/rhr/?criteria.ParliamentNumber=53&criteria.Timeframe=range&criteria.DateFrom=2021-01-18&criteria.DateTo=2022-02-28&parliamentStartDate=2020-11-24&parliamentEndDate="
START_DATE = "2022-02-18"
STOP_DATE = "2021-11-18"

EXPECTED_DOCS = 19

##### Functions 

# We want to get this specific debate for testing purposes 
def get_conscience_vote_example():
    scraper = scrape(
        start_url = "https://www.parliament.nz/en/pb/hansard-debates/rhr/?criteria.ParliamentNumber=52&criteria.Timeframe=range&criteria.DateFrom=2019-11-09&criteria.DateTo=2019-11-13&parliamentStartDate=2017-11-07&parliamentEndDate=2020-11-20",
        stop = "2019-11-11",
    )
    doc = next(scraper)

    debate_titles = [debate.title for debate in doc.debates]
    assert 'End of Life Choice Bill — Third Reading' in debate_titles

    return doc

# Download the documents in the time range and store in a pickle file
# The time range and the filename can be configured in the config section of this file
def make_test_set():
    docs = [doc for doc in scrape(
        start_url = START_URL,
        stop = STOP_DATE,
        start = START_DATE,
        log_level = logging.INFO,
    )]
    docs.append(get_conscience_vote_example())

    assert len(docs) == EXPECTED_DOCS, "Did not find expected number of documents"

    log_message = ""
    try:
        old_set = load_test_set()
        if old_set == docs:
            log_message = "Test set hasn't changed"
        else:
            log_message = "Test set has changed"
    except:
        log_message = "Test set generated"
    logging.info(log_message)


    with open(TEST_SET_FILE_PATH, 'wb') as f:
        pickle.dump(docs, f, protocol=pickle.HIGHEST_PROTOCOL)

# Load a previously scraped test set from the picke file
def load_test_set() -> List[HansardLink]:
    with open(TEST_SET_FILE_PATH, 'rb') as f:
        docs = pickle.load(f)

        assert len(docs) == EXPECTED_DOCS, "Did not find expected number of documents"

        return docs

# Load a previously scraped test set and store it in hansardDB 
def insert_test_set(conn):
    test_set = load_test_set()
    for doc in test_set:
        insert_document(conn, doc)
    conn.commit()

if __name__ == "__main__":
    make_test_set()

