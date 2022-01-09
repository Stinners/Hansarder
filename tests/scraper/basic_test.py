from ...scraper.main import scrape
from ...scraper.scraper_types import *

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
    assert(doc.debates[0].title == "Karakia/Prayers")

# This is mostly just testing that we don't throw an exception
def test_get_one_document():
    # Set a log level some arbitrary time in the past 
    scraper = scrape(stop="2021-08-04")
    document = next(scraper)

    validate_document(document)

def test_get_from_past():
    import logging 
    scraper = scrape(
        start = date.today() - timedelta(days=100),
        stop = date.today() - timedelta(days=200),
        log_level = logging.DEBUG,
    )
    document = next(scraper)
    print(document)

    validate_document(document)





    




