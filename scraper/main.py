from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, ElementHandle, Locator

from dataclasses import dataclass
from typing import Optional, TypeVar, List
from datetime import date
from time import sleep

T = TypeVar('T')

# These classes represent all the information that can me retreived 
# out of the main seach page, it is retreived at this level to provide 
# metadata for the main text
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


class ScraperError(Exception):
    pass

root = "https://www.parliament.nz"

def unwrap(opt: Optional[T], message: str) -> T:
    if opt is None:
        raise Exception(message)
    return opt

def get_debate(debate):
    return ()

# Takes the element corresponding to a single day of the Hansard and extracts 
# this into a HansardLink class 
# This takes a .hansard_list__item locator
def get_hansard_link(elem: Locator) -> HansardLink:

    # Expand the Debates
    hansard_toggle = unwrap(elem.locator(".hansard__toggle"), "Could not find expand button")
    is_expanded = hansard_toggle.get_attribute("aria-expanded") == "true"
    if not is_expanded:
        hansard_toggle.click()

    #Get the href for the link
    anchor = unwrap(elem.locator(".hansard__content h2 a"), "Could not find anchor element")
    url = unwrap(anchor.get_attribute("href"), "Couldn't find href")

    title = anchor.inner_text().strip()
    print(title)

    dates = get_dates_from_url(url)

    # Get each of the debate
    #debate_elems = unwrap(elem.query_selector_all(".hansard__sub-item"), "Could not find debates")
    #debates = [get_debate(elem) for elem in debate_elems]

    return HansardLink(
            title=title,
            dates=dates,
            debates=[],
            url=url,
    )

# This will need to handle parliments before this one 
# I should also check this works on slow networks
def goto_next_page(page: Page):
    next_button = page.query_selector(".pagination__next .js-pagination-link")
    if next_button != None:
        next_button.click()
        page.wait_for_load_state("networkidle")
    else:
        raise ScraperError("Couldn't find next page button")

# For the pruposes of this code start is the earliest date and stop is the latest
# This compares inclusivly
def in_range(link: HansardLink, scraper: Scraper) -> bool:
    return link.dates.continued_from <= scraper.start and link.dates.continued_from >= scraper.stop

def get_locators(page, single_selector: str) -> List[Locator]:
    single_selector = single_selector.strip()
    n_elems = len(page.query_selector_all(single_selector))
    selectors = [single_selector + f":nth-of-type({n})" for n in range(1, n_elems+1)]
    return [page.locator(selector) for selector in selectors]

def get_links_in_range(scraper: Scraper) -> List[HansardLink]:
    links = []

    # Goto the page to start 
    scraper.page.goto(root + "/en/pb/hansard-debates/rhr/")

    while True:
        sections = get_locators(scraper.page, ".hansard__list-item")
        for section in sections: 
            link = get_hansard_link(section)
            if in_range(link, scraper):
                links.append(link)
            elif links != []:
                return links

        sleep(scraper.seconds_delay)
        goto_next_page(scraper.page)


def string_to_date(string: str) -> date:
    """ Takes a date string of the format YYYYMMDD - as presented in the Hansard urls - and converts it to 
    python date object """
    year = int(string[:4])
    month = int(string[4:6])
    day = int(string[6:])
    return date(year, month, day)


def get_dates_from_url(url: str) -> SessionDate:
    """ Takes the url for a session and the extracts a SessionDate from it """
    segments = url.split("_")
    try:
        actual_date = string_to_date(segments[-1])
        contined_from = string_to_date(segments[-2])
        return SessionDate(actual_date, contined_from)
    except:
        raise ScraperError(f"Could not get date from url: {url}")

def get_text(page: Page, link: str) -> Optional[ElementHandle]:
    page.goto(link)
    return page.query_selector(".body-text--hansard")

def init_scraper(page: Page, start: date, stop: date, delay: int) -> Scraper:
    return Scraper(page, start, stop, delay)

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        stop = date.fromisoformat("2021-08-04")
        start = date.fromisoformat("2022-02-21")
        scraper = init_scraper(page, start, stop, 5)
        links = get_links_in_range(scraper)

        browser.close()

if __name__ == "__main__":
    main()
