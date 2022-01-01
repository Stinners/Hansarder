
# These classes represent all the information that can me retreived 
# out of the main seach page, it is retreived at this level to provide 
# metadata for the main text

from playwright.sync_api import Page

from datetime import date
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Scraper:
    page: Page
    start: date
    stop: date
    seconds_delay: int

@dataclass
class SpeachLink:
    type: str
    topic: Optional[str]
    speakers: list[str]

@dataclass
class DebateLink:
    type: str
    speaches: list[SpeachLink]

@dataclass 
class SessionDate:
    actual_date: date
    continued_from: date

@dataclass
class HansardLink:
    title: str
    dates: SessionDate
    debates: list[DebateLink]
    url: str


# TODO this call represents th structured information aquired from 
# parsing a single document 
@dataclass 
class HansardDocument:
    pass

class ScraperError(Exception):
    pass
