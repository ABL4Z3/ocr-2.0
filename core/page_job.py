from dataclasses import dataclass
from pathlib import Path


@dataclass
class PageJob:

    document_name: str
    source_path: Path
    page_number: int

    page_type: str | None = None
    extractor: str | None = None

    extraction_folder: Path | None = None

    parsed_page = None