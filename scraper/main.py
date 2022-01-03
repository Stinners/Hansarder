from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, ElementHandle

from typing import Optional, List
from datetime import date, timedelta
import logging
import pickle
import os

from scraper_types import *
from get_links import get_links_in_range


def get_text(page: Page, link: str) -> Optional[ElementHandle]:
    page.goto(link)
    return page.query_selector(".body-text--hansard")

def reload_checkpoint(checkpoint_file: Optional[str]) -> Optional[Checkpoint]:
    if checkpoint_file == None: return None

    try:
        with open(checkpoint_file, 'rb') as chk_file:
            checkpoint = pickle.loads(chk_file.read())
            return checkpoint

    except:
        if os.path.exists(checkpoint_file):
            logging.warning(f"Couldn't load checkpoint file: {checkpoint_file}")
        return None

def init_scraper(
    page: Page, 
    date_range: DateRange, 
    seconds_delay: int, 
    checkpoint_file: Optional[str], 
    start_url: str) -> Scraper:

    if (checkpoint := reload_checkpoint(checkpoint_file)) != None:
        start_url = checkpoint.current_url

        # Subtract one day so we start from the day *before* the last date processed
        date_range.start = checkpoint.last_date_processed - timedelta(days=1)

    return Scraper(
        page = page,
        date_range = date_range,
        seconds_delay = seconds_delay,
        start_url = start_url,
        checkpoint_file = checkpoint_file,
    )

def cleanup_checkpoint_file(scraper):
    if scraper.checkpoint_file == None: return 
    try:
        os.remove(scraper.checkpoint_file)
        logging.info("Removing checkpoint file")
    except FileNotFoundError:
        pass

def main(
    stop: date,
    start: date = date.today(),
    seconds_delay: int = 5,
    log_level: int = logging.INFO,
    log_file: Optional[str] = None,
    checkpoint_file: Optional[str] = None,
) -> List[HansardLink]:

    # Loading config
    logging.basicConfig(filename=log_file, level=log_level)
    root = "https://www.parliament.nz"
    start_url = root + "/en/pb/hansard-debates/rhr/"
    date_range = DateRange(start, stop)

    # Starting a browser and setting up the Scraper
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        scraper = init_scraper(page, date_range, seconds_delay, checkpoint_file, start_url)

        # Running the actual Scraper 
        logging.info("Starting Scraper")
        links = get_links_in_range(scraper)

        #cleaning up
        cleanup_checkpoint_file(scraper)

        browser.close()



    return links



if __name__ == "__main__":
    main(
        stop = date.fromisoformat("2021-08-04"),
        log_level = logging.DEBUG,
        checkpoint_file = "checkpoint.json",
    )
