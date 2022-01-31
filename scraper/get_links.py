# This file is responsible for reading the link of sessions and 
# extracting as much information as possible from those pages 
# it also handles managing the range of sessions to pull from 
from playwright.sync_api import Locator

from typing import TypeVar, List, Tuple, Iterator
from time import sleep
import logging
import pickle

from .scraper_types import *
from .utilities import Locators
from .get_text import get_html
from .debate_types import DebateTypes

T = TypeVar('T')

def get_links_in_range(scraper: Scraper) -> Iterator[HansardLink]:
    links = []

    # Goto the page to start 
    scraper.page.goto(scraper.start_url)

    while True:
        logging.debug(f"Starting page: {scraper.page.url}")
        locator = scraper.page.locator(".hansard__list-item")
        days_on_page = Locators(scraper.page, locator)

        for day_section in days_on_page:
            logging.debug("Reading New Day")

            # Get the information readily avilible on this page 
            day = get_hansard_link(day_section)

            # Only do further processing if the link is in out date range
            if scraper.date_range.contains_link(day):
                logging.info(f"Getting Data for: {day.title}")
                day.debates = get_debates(scraper, day_section)
                get_html(scraper, day)
                yield day
                write_checkpoint(scraper, day)

            # If we'er out of the range then we can return 
            elif scraper.date_range.done(day.dates):
                logging.info(f"Stopped before: {day.title}")
                return links
            
            else:
                logging.info(f"Skipping: {day.title}")

        goto_next_page(scraper)
        logging.debug(f"Sleeping for {scraper.seconds_delay} seconds")
        sleep(scraper.seconds_delay)

def get_type(debate_title: str) -> Optional[str]:
    for text, type in DebateTypes.exact_matches.items():
        if debate_title == text: return type

    for text, type in DebateTypes.contains.items():
        if text in debate_title: return type

    #for regex, type in debate_types.regex.items():
    #    if regex.search(debate_title): return type 

    return None

def get_debates(scraper: Scraper, elem: Locator) -> List[DebateLink]:
    logging.debug("Expanding Day")
    expand_section(elem)
    sub_list = elem.locator(".hansard__sub-list")
    debates = []
    sections = Locators(scraper.page, sub_list.locator(".hansard__sub-item"))
    for section in sections:
        title = section.locator("h3").inner_text().strip()
        speeches = get_speeches(scraper, section)

        type = get_type(title)

        debate = DebateLink(
            title = title,
            type = type,
            speeches = speeches
        )
        debates.append(debate)

    return debates

def expand_section(section: Locator):
    toggle = section.locator("> .js-hansard__toggle")
    is_expanded = toggle.get_attribute("aria-expanded") == "true"
    if not is_expanded:
        toggle.click()
        section.element_handle().wait_for_selector('> .js-hansard__toggle[aria-expanded="true"]')

# Do a better job of handling errors here
def get_question(section: Locator) -> Tuple[str, str]:
    question_text = section.locator("h5").inner_text()
    topic = question_text.split("—")[1].strip()        # NB this isn't a normal hyphen 

    speaker_text = section.locator("p.list__cell-text").inner_text()
    speaker = speaker_text.split("(")[0].strip()

    return (speaker, topic)

# This just gets the title of the speech, it should be used to get the 
# name of the speaker in a regular speech
def get_speech(section: Locator) -> str:
    title = section.locator("h5").inner_text().strip()

    # If there are multiple speakers we just get the first one 
    parts = title.split(";")
    return parts[0]

def normalize_name(name: Optional[str]) -> Optional[str]:
    if name == None:
        return None

    # We just make the name lowercase and then rely on Potgres's case insensitive 
    # matching to find a connonical form later
    name = name.lower()

    # We need to remove honorifics
    # TODO possibly these should be stored in the member table
    name = name.removeprefix("hon ")
    name = name.removeprefix("dr ")

    parts = name.split(", ")
    if len(parts) == 2:
        # If the name is comma sepatrated then it's in lastname firstname format, so we flip them
        name = f"{parts[1]} {parts[0]}"

    return name

# This function is called once for each debate 
def get_speeches(scraper: Scraper, debate_selector: Locator) -> List[SpeechLink]:
    # First we need to expand the speeches 
    logging.debug("Expanding Debate")
    expand_section(debate_selector)
    debate_selector.element_handle().wait_for_selector(".hansard__child-list")

    speeches = []
    speech_selector = debate_selector.locator(".hansard__child-list .hansard__content")
    for speech in Locators(scraper.page, speech_selector):
        speaker = None 
        topic = None

        # We need to identify if we have a speech or a question
        doctype = speech.locator(".hansard__doctype").inner_text()
        if doctype == "Question":
            speaker, topic = get_question(speech)
        elif doctype == "Speech":
            speaker = get_speech(speech)
        elif doctype == "Vote":
            pass 
        else:
            raise ScraperError(f"Unrecognized speech type {doctype}")

        speaker = normalize_name(speaker)

        # At this stage we create the speech with an empty text field
        # this will be populated later
        speeches.append(SpeechLink(
            type = doctype,
            topic = topic,
            speaker = speaker,
            html = None,
            processed_text = "",
        ))

    return speeches

# This only get the information availible on the main page, it doesn't make any additional HTTP requests
# This takes a .hansard_list__item locator
def get_hansard_link(elem: Locator) -> HansardLink:

    #Get the href for the link
    anchor = unwrap(elem.locator(".hansard__content h2 a"), "Could not find anchor element")
    url = unwrap(anchor.get_attribute("href"), "Couldn't find href")

    title = anchor.inner_text().strip()

    dates = get_dates_from_url(url)

    #debates = get_debates(scraper, elem)

    link = HansardLink(
            title=title,
            dates=dates,
            debates=[],
            url=url,
    )

    #get_html(scraper, link)

    return link

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
