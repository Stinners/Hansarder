from ...libhansard.scraper.main import scrape
from ...libhansard.scraper.scraper_types import *

import logging
import html.parser

def assert_valid_html(text):
    parser = html.parser.HTMLParser()
    parser.feed(text)
    assert parser.get_starttag_text() is not None


def test_scrape_single_document():
    documents = scrape(
        stop = "2020-11-30",
        seconds_delay = 1,
    )
    result = next(documents)

    assert len(result.debates) != 0
    assert len(result.debates[0].speeches) != 0
    assert_valid_html(result.debates[0].speeches[0].html)


# This test can take a long time - approx 2 minutes
# We should enable logging to a file if we want realtime feedback 
def test_basic_scraping():
    documents = scrape(
        stop = "2021-11-30",
        start = "2021-11-18",
        seconds_delay = 1,
        log_level = logging.INFO,
        start_url = "https://www.parliament.nz/en/pb/hansard-debates/rhr/?criteria.ParliamentNumber=53&criteria.Timeframe=range&criteria.DateFrom=2021-11-01&criteria.DateTo=2021-11-30&parliamentStartDate=2020-11-24&parliamentEndDate="
    )
    docs = [doc for doc in documents]
    
    assert len(docs) == 4
    assert docs[0].title == "Thursday, 25 November 2021 - Volume 756"
    assert len(docs[1].debates) == 17

    karakia = docs[3].debates[0]

    assert karakia.type == "Karakia"
    assert karakia.speeches[0].speaker == "adrian rurawhe"

    html = karakia.speeches[0].html
    assert html is not None
    assert "Kia tau anō te rangimārie ki a tātou" in html
