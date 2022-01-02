from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, ElementHandle

from typing import Optional, List
from datetime import date
import logging

from parser_types import *
from get_links import get_links_in_range

def get_text(page: Page, link: str) -> Optional[ElementHandle]:
    page.goto(link)
    return page.query_selector(".body-text--hansard")

def init_scraper(page: Page, start: date, stop: date, delay: int) -> Scraper:
    return Scraper(page, start, stop, delay)

"""
def main():
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        stop = date.fromisoformat("2021-08-04")
        start = date.fromisoformat("2022-02-21")
        scraper = init_scraper(page, start, stop, 5)
        links = get_links_in_range(scraper)

        browser.close()
"""

def main(
    start: date,
    stop: date,
    seconds_delay: int = 5,
    log_level: int = logging.INFO,
    log_file: Optional[str] = None
) -> List[HansardLink]:
    logging.basicConfig(filename=log_file, level=log_level)
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        stop = date.fromisoformat("2021-08-04")
        start = date.fromisoformat("2022-02-21")
        scraper = init_scraper(page, start, stop, seconds_delay)
        links = get_links_in_range(scraper)

        browser.close()

    return links



if __name__ == "__main__":
    main(
        stop = date.fromisoformat("2021-08-04"),
        start = date.fromisoformat("2022-02-21"),
        log_level = logging.DEBUG,
    )
