# This file is responsible for reading the link of sessions and 
# extracting as much information as possible from those pages 
# it also handles managing the range of sessions to pull from 
from playwright.sync_api import Locator

from typing import TypeVar, List, Tuple
from time import sleep
import logging
import pickle

from scraper_types import *

T = TypeVar('T')

def get_links_in_range(scraper: Scraper) -> List[HansardLink]:
    links = []
    link_in_range = False

    # Goto the page to start 
    scraper.page.goto(scraper.start_url)

    while link_in_range or links == []:
        logging.debug(f"Starting page: {scraper.page.url}")
        locator = scraper.page.locator(".hansard__list-item")
        for section in Locators(scraper.page, locator):
            link = get_hansard_link(scraper, section)
            link_in_range = scraper.date_range.contains_link(link)
            if link_in_range:
                logging.debug(link.title)
                links.append(link)
                write_checkpoint(scraper, link)
            elif links != []:
                return links

        goto_next_page(scraper)
        logging.debug(f"Sleeping for {scraper.seconds_delay} seconds")
        sleep(scraper.seconds_delay)

    # this should never actually be reached
    raise Exception("This should be unreachable")

def get_debates(scraper: Scraper, elem: Locator) -> List[DebateLink]:
    sub_list = elem.locator(".hansard__sub-list")
    debates = []
    sections = Locators(scraper.page, sub_list.locator(".hansard__sub-item"))
    for section in sections:
        title = section.locator("h3").inner_text()
        speeches = get_speeches(scraper, section)

        debate = DebateLink(
            title = title,
            type = None,
            speeches = speeches
        )
        debates.append(debate)

    return debates

def expand_section(section: Locator):
    toggle = section.locator("> .js-hansard__toggle")
    is_expanded = toggle.get_attribute("aria-expanded") == "true"
    if not is_expanded:
        toggle.click()

# Do a better job of handling errors here
def get_question(section: Locator) -> Tuple[str, str]:
    question_text = section.locator("h5").inner_text()
    topic = question_text.split("—")[1].strip()        # NB this isn't a normal hyphen 

    speaker_text = section.locator("p.list__cell-text").inner_text()
    speaker = speaker_text.split("(")[0].strip()

    return (speaker, topic)

def get_speech(section: Locator) -> str:
    return section.locator("h5").inner_text().strip()

# This function is called once for each debate 
def get_speeches(scraper: Scraper, elem: Locator) -> List[SpeechLink]:
    # First we need to expand the speeches 
    expand_section(elem)
    elem.element_handle().wait_for_selector(".hansard__child-list")

    speeches = []
    locators = elem.locator(".hansard__child-list .hansard__content")
    for section in Locators(scraper.page, locators):
        speaker = None 
        topic = None

        # We need to identify if we have a speech or a question
        doctype = section.locator(".hansard__doctype").inner_text()
        if doctype == "Question":
            speaker, topic = get_question(section)
        elif doctype == "Speech":
            speaker = get_speech(section)
        elif doctype == "Vote":
            pass 
        else:
            raise ScraperError(f"Unrecognized speech type {doctype}")

        speeches.append(SpeechLink(
            type = doctype,
            topic = topic,
            speaker = speaker
        ))

    return speeches

# Takes the element corresponding to a single day of the Hansard and extracts 
# this into a HansardLink class 
# This takes a .hansard_list__item locator
def get_hansard_link(scraper: Scraper, elem: Locator) -> HansardLink:

    # Expand the Debates
    expand_section(elem)

    #Get the href for the link
    anchor = unwrap(elem.locator(".hansard__content h2 a"), "Could not find anchor element")
    url = unwrap(anchor.get_attribute("href"), "Couldn't find href")

    title = anchor.inner_text().strip()

    dates = get_dates_from_url(url)

    debates = get_debates(scraper, elem)

    # Get each of the debate
    #debate_elems = unwrap(elem.query_selector_all(".hansard__sub-item"), "Could not find debates")
    #debates = [get_debate(elem) for elem in debate_elems]

    return HansardLink(
            title=title,
            dates=dates,
            debates=debates,
            url=url,
    )

# This will need to handle parliments before this one 
# I should also check this works on slow networks
def goto_next_page(scraper: Scraper):
    next_button = scraper.page.query_selector(".pagination__next .js-pagination-link")
    if next_button != None:
        next_button.click()
        scraper.page.wait_for_load_state("networkidle")
    else:
        raise ScraperError("Couldn't find next page button")

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
    def __init__(self, page, locator: Locator):

        self.locator = locator 
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

def write_checkpoint(scraper: Scraper, last_link: HansardLink):
    if scraper.checkpoint_file == None:
        return 
    else:
        checkpoint = Checkpoint(
            current_url = scraper.page.url,
            last_date_processed = last_link.dates.actual_date
        )

        try:
            with open(scraper.checkpoint_file, 'wb') as check_file:
                pickle.dump(checkpoint, check_file)

        except:
            logging.warn(f"Couldn't write checkpoint to: {scraper.checkpoint_file}")

def unwrap(opt: Optional[T], message: str) -> T:
    if opt is None:
        raise Exception(message)
    return opt
