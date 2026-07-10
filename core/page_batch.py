from dataclasses import dataclass

from core.page_job import PageJob


@dataclass
class PageBatch:

    extractor: str

    pages: list[PageJob]