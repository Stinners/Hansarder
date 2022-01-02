# This file is responsible for reading the link of sessions and 
# extracting as much information as possible from those pages 
# it also handles managing the range of sessions to pull from 
from playwright.sync_api import Page, Locator

from typing import Optional, TypeVar, List
from datetime import date
from time import sleep
import logging

from parser_types import *

T = TypeVar('T')
root = "https://www.parliament.nz"

def get_links_in_range(scraper: Scraper) -> List[HansardLink]:
    links = []
    link_in_range = False

    # Goto the page to start 
    scraper.page.goto(root + "/en/pb/hansard-debates/rhr/")

    while link_in_range or links == []:
        logging.debug(f"Starting page: {scraper.page.url}")
        for section in Locators(scraper.page, ".hansard__list-item"):
            link = get_hansard_link(section)
            link_in_range = in_range(link, scraper)
            if link_in_range:
                logging.debug(link.title)
                links.append(link)
            else:
                break

        logging.debug(f"Sleeping for {scraper.seconds_delay} seconds")
        sleep(scraper.seconds_delay)
        goto_next_page(scraper.page)

    return links

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

class Locators:
    def __init__(self, page, selector):

        self.locator = page.locator(selector)
        self.page = page
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        next_elem = self.locator.nth(self.n)
        self.n += 1
        if self.n > self.locator.count():
            raise StopIteration
        else: 
            return next_elem 


def unwrap(opt: Optional[T], message: str) -> T:
    if opt is None:
        raise Exception(message)
    return opt
