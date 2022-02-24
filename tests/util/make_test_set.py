
import sys
from pathlib import Path
import pickle
import logging
from typing import List

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.scraper.main import scrape
from libhansard.scraper.scraper_types import *

# Scrape a known set of documents and store them in a pickle file
# Note this test set isn't commited to version control

##### Config 

TEST_SET_FILE = "test_set.pickle"
TEST_SET_FILE_PATH = Path(__file__).parent / TEST_SET_FILE

START_URL = "https://www.parliament.nz/en/pb/hansard-debates/rhr/?criteria.ParliamentNumber=53&criteria.Timeframe=range&criteria.DateFrom=2021-01-18&criteria.DateTo=2022-02-28&parliamentStartDate=2020-11-24&parliamentEndDate="
START_DATE = "2022-02-18"
STOP_DATE = "2021-11-18"

EXPECTED_DOCS = 18

##### Functions 

def make_test_set():
    docs = [doc for doc in scrape(
        start_url = START_URL,
        stop = STOP_DATE,
        start = START_DATE,
        log_level = logging.INFO,
    )]
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

def load_test_set() -> List[HansardLink]:
    with open(TEST_SET_FILE_PATH, 'rb') as f:
        docs = pickle.load(f)

        assert len(docs) == EXPECTED_DOCS, "Did not find expected number of documents"

        return docs

# If we run this file standalone then we probably want 
# to rejuvenate the test set 
if __name__ == "__main__":
    make_test_set()

