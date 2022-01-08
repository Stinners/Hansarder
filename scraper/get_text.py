from scraper_types import *
from utilities import Locators, root_url

from typing import Iterator

def speeches(link: HansardLink) -> Iterator[SpeechLink]:
    for debate in link.debates:
        for speech in debate.speeches:
            yield speech

def get_html(scraper: Scraper, link: HansardLink):
    page = scraper.browser.new_page()
    page.goto(root_url + link.url)

    text_body = page.locator("ul.hansard__level")
    speech_texts = Locators(page, text_body.locator("> li"))
    speach_links = speeches(link)

    for speach_link, speach_text in zip(speach_links, speech_texts):
        speach_link.html = speach_text.locator(".body-text").inner_html()

    page.close()
