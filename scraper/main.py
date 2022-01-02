from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, ElementHandle

from typing import Optional, List
from datetime import date
import logging

from scraper_types import *
from get_links import get_links_in_range

def get_text(page: Page, link: str) -> Optional[ElementHandle]:
    page.goto(link)
    return page.query_selector(".body-text--hansard")

def main(
    stop: date,
    start: date = date.today(),
    seconds_delay: int = 5,
    log_level: int = logging.INFO,
    log_file: Optional[str] = None
) -> List[HansardLink]:
    logging.basicConfig(filename=log_file, level=log_level)
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        date_range = DateRange(start, stop)
        scraper = Scraper(page, date_range, seconds_delay)
        links = get_links_in_range(scraper)

        browser.close()

    return links



if __name__ == "__main__":
    main(
        stop = date.fromisoformat("2021-08-04"),
        log_level = logging.DEBUG,
    )
