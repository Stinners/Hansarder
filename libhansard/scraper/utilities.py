
from playwright.sync_api import Page, Locator

root_url = "https://www.parliament.nz"

class Locators:
    def __init__(self, page: Page, locator: Locator):

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
