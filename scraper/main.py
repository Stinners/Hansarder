from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, ElementHandle, Locator

from dataclasses import dataclass
from typing import Optional, TypeVar, List
from datetime import date
from time import sleep

from parser_types import *
from get_links import get_links_in_range


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

        for link in links:
            print(link.title)

        browser.close()

if __name__ == "__main__":
    main()
