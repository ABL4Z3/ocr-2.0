from dataclasses import dataclass, field

from core.page import Page


@dataclass
class Document:

    pages: list[Page] = field(default_factory=list)
    
    def add_page(self, page: Page):
        self.pages.append(page)

    def get_page(self, page_number: int):

        for page in self.pages:
            if page.page_number == page_number:
                return page

        page = Page(page_number=page_number)
        self.pages.append(page)

        return page