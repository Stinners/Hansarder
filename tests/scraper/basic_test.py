
import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.scraper.main import scrape
from libhansard.scraper.scraper_types import *

import calendar
import itertools
import calendar
from datetime import date, timedelta

# Validate that the title of the session is formated as we expect 
def validate_title(title: str):
    parts = title.split()

    # The first part should be a week day 
    assert(parts[0].strip(",") in list(calendar.day_name)) #["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    # The third part should be a Month 
    assert(parts[2].strip(",") in list(calendar.month_name))

    # Second and fourth parts should be numbers 
    int(parts[1])
    int(parts[3])

    assert(parts[-2] == "Volume")
    int(parts[-1])

# There's a lot more we could do here 
def validate_document(doc: HansardLink):
    validate_title(doc.title)

    is_continued = "continued on" in doc.title
    has_karakia = "Karakia" in doc.debates[0].title 
    assert(is_continued or has_karakia)

# This is mostly just testing that we don't throw an exception
def test_get_one_document():
    # Set a stop some arbitrary time in the past 
    scraper = scrape(stop="2021-08-04")
    document = next(scraper)

    validate_document(document)

# This takes a very long time, on order of 10 minutes
def test_get_from_over_page():
    scraper = scrape(stop="2021-01-10")

    # Taking 21 documents ensures that we have to 
    # Take docs from more than one page
    documents = itertools.islice(scraper, 21)
    
    for document in documents:
        validate_document(document)

def test_handle_no_next_page():
    scraper = scrape(
        start = "2022-01-01",
        stop = "2021-08-04",
        start_url = "https://www.parliament.nz/en/pb/hansard-debates/rhr/?criteria.ParliamentNumber=53&criteria.Timeframe=range&criteria.DateFrom=2022-01-01&criteria.DateTo=2022-02-11&parliamentStartDate=2020-11-24&parliamentEndDate=",
    )

    # We just want to force the iterator to evaluate and 
    # ensure it doesn't throw exceptions
    [doc for doc in scraper]


