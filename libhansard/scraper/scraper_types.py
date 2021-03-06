
# These classes represent all the information that can me retreived 
# out of the main seach page, it is retreived at this level to provide 
# metadata for the main text

from playwright.sync_api import Page, Browser

from datetime import date
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class SpeechLink:
    type: str
    topic: Optional[str]
    speaker: Optional[str]
    html: Optional[str]
    processed_text: Optional[str]

@dataclass
class DebateLink:
    title: str
    type: Optional[str]
    speeches: List[SpeechLink]

@dataclass 
class SessionDate:
    actual_date: date
    continued_from: date

@dataclass
class HansardLink:
    title: str
    dates: SessionDate
    debates: List[DebateLink]
    url: str

# We always read backwards in time, from the most recent date ot the oldest
class DateRange:
    def __init__(self, start: date | str, stop: date | str):
        self.start = parse_date(start)
        self.stop = parse_date(stop)

        # Make sure start is always the most recent date
        if self.start < self.stop:
            self.start, self.stop = self.stop, self.start

    def in_range(self, a_date) -> bool:
        return a_date <= self.start and a_date >= self.stop

    def contains_link(self, link: HansardLink) -> bool:
        return self.in_range(link.dates.continued_from)

    # We're done if the data is before the stop date
    def done(self, session: SessionDate) -> bool:
        return self.stop > session.continued_from

        

def parse_date(datestring: date | str) -> date:
    if isinstance(datestring, date):
        return datestring
    else:
        try:
            return date.fromisoformat(datestring)
        except:
            raise ValueError(f"Datesting: {datestring} must be in ISO format (YYYY-MM_DD)")

class ScraperError(Exception):
    pass

@dataclass
class Checkpoint:
    current_url: str 
    last_date_processed: date

@dataclass(frozen=True)
class Scraper:
    page: Page
    date_range: DateRange
    seconds_delay: int
    start_url: str
    checkpoint_file: Optional[str]
    browser: Browser
