import itertools
import os 

from ...libhansard.scraper.main import scrape
from ...libhansard.scraper.scraper_types import *

CHECKPOINT_FILE = "test.checkpoint"

def create_scraper():
    scraper = scrape(
        start_url = "https://www.parliament.nz/en/pb/hansard-debates/rhr/?criteria.ParliamentNumber=53&criteria.Timeframe=range&criteria.DateFrom=2021-11-30&criteria.DateTo=2022-02-01&parliamentStartDate=2020-11-24&parliamentEndDate=",
        start = "2021-12-15",
        stop = "2021-12-06",
        checkpoint_file = CHECKPOINT_FILE,
    )
    return scraper


# We have to keep the first scraper in it's own context so the first 
# Playwright instance gets shutdown
def get_first(n):
    # Get the first 3 documents
    scraper1 = create_scraper()
    docs = list(itertools.islice(scraper1, n))
    return docs

# This test takes about 2 minutes
def test_checkpointing():
    docs1 = get_first(3)

    # Start a new scraper and get the remaining docs
    scraper2 = create_scraper()
    docs2 = list(scraper2)

    assert len(docs1) == 3 
    assert len(docs2) == 4

    assert docs2[0].title == 'Thursday, 9 December 2021 - Volume 756'

    # Check that the checkpoint file gets cleaned up
    assert not os.path.isfile(CHECKPOINT_FILE) 
