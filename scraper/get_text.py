from .scraper_types import *
from .utilities import Locators, root_url

from typing import Iterator

# this requires nltk's punkt models to be installed
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initlialize the stemmer 
stop_words = set(stopwords.words('english'))
punctuation = ".,;!?():"
lemmatizer = WordNetLemmatizer()

def speeches(link: HansardLink) -> Iterator[SpeechLink]:
    for debate in link.debates:
        for speech in debate.speeches:
            yield speech

# We elimiate a 'word' if it's a stop word or if it's a puntuation mark 
def include_word(word: str) -> bool:
    if word in stop_words: return False
    elif len(word) == 1 and word in punctuation: return False
    else: return True

# This should really go in a different module
# This tokenized and stems the words
def process_text(text: str) -> str:
    text = text.lower()
    tokens = [word for word in word_tokenize(text) if include_word(word)]
    lemmatized = [lemmatizer.lemmatize(word) for word in tokens]
    processed_text = " ".join(lemmatized)
    return processed_text

def get_html(scraper: Scraper, link: HansardLink):
    page = scraper.browser.new_page()
    page.goto(root_url + link.url)

    text_body = page.locator("ul.hansard__level")
    speech_texts = Locators(page, text_body.locator("> li"))
    speach_links = speeches(link)

    for speach_link, speach_text in zip(speach_links, speech_texts):

        # Set the html from the text
        section = speach_text.locator(".body-text")
        speach_link.html = section.inner_html()
        speach_link.processed_text = process_text(section.inner_text())
        import pdb; pdb.set_trace()

    page.close()
