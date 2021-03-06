from playwright.sync_api import sync_playwright

from typing import Optional, Iterator
from datetime import date, timedelta
import logging
import pickle
import os
import sys

from .scraper_types import *
from .get_links import get_links_in_range

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

def cleanup_checkpoint_file(scraper):
    if scraper.checkpoint_file == None: return 
    try:
        os.remove(scraper.checkpoint_file)
        logging.info("Removing checkpoint file")
    except FileNotFoundError:
        pass

def init_scraper(
    browser: Browser, 
    date_range: DateRange, 
    seconds_delay: int, 
    checkpoint_file: Optional[str], 
    start_url: str) -> Scraper:

    if (checkpoint := reload_checkpoint(checkpoint_file)) != None:
        start_url = checkpoint.current_url

        # Subtract one day so we start from the day *before* the last date processed
        date_range.start = checkpoint.last_date_processed - timedelta(days=1)

    return Scraper(
        browser = browser,
        page = browser.new_page(),
        date_range = date_range,
        seconds_delay = seconds_delay,
        start_url = start_url,
        checkpoint_file = checkpoint_file,
    )

def get_logging_handlers(log_file: Optional[str], log_to_terminal: bool): 
    handlers = []
    if log_file != None: handlers.append(logging.FileHandler(log_file))
    if log_to_terminal: handlers.append(logging.StreamHandler(sys.stdout))
    return handlers

def scrape(
    stop: date | str,
    start: date | str = date.today(),
    seconds_delay: int = 5,
    log_level: int = logging.DEBUG,
    log_file: Optional[str] = None,
    log_to_terminal = True,
    checkpoint_file: Optional[str] = None,
    start_url = "https://www.parliament.nz/en/pb/hansard-debates/rhr/?criteria.ParliamentNumber=-1&criteria.Timeframe=&criteria.DateFrom=&criteria.DateTo=&parliamentStartDate=&parliamentEndDate=",
) -> Iterator[HansardLink]:

    # Loading config
    log_handlers = get_logging_handlers(log_file, log_to_terminal)
    logging.basicConfig(level=log_level, handlers=log_handlers)

    date_range = DateRange(start, stop)

    # Starting a browser and setting up the Scraper
    with sync_playwright() as p:
        browser = p.firefox.launch()
        scraper = init_scraper(browser, date_range, seconds_delay, checkpoint_file, start_url)

        logging.info("Starting Scraper")
        logging.info(f"Starting at URL: {start_url}")
        logging.info(f"Running from {start} to {stop}")

        # Running the actual Scraper 
        for link in get_links_in_range(scraper):
            yield link

        cleanup_checkpoint_file(scraper)

        browser.close()



