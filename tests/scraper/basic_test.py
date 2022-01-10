from ...scraper.main import scrape
from ...scraper.scraper_types import *

import logging 
import calendar
import itertools
import calendar
from datetime import date, timedelta

# Validate that the title of the session is formated as we expect 
def validate_title(title: str):
    parts = title.split()

    # The first part should be a week day 
    assert(parts[0].strip(",") in list(calendar.day_name)) #["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    # The first part should be a Month 
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
    # Set a log level some arbitrary time in the past 
    scraper = scrape(stop="2021-08-04")
    document = next(scraper)

    validate_document(document)

def test_get_from_past():
    scraper = scrape(
        stop = date.today() - timedelta(days=365),
        log_level = logging.DEBUG,
    )

    # Taking 21 documents ensures that we have to 
    # Take docs from more than one page
    documents = itertools.islice(scraper, 21)
    
    for document in documents:
        validate_document(document)
