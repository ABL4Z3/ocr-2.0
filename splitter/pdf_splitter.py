from pathlib import Path

import fitz

from core.page_job import PageJob


class PDFSplitter:

    def split(self, pdf_path: Path):

        pdf = fitz.open(pdf_path)

        pages = []

        for page_number in range(len(pdf)):

            pages.append(
                PageJob(
                    document_name=pdf_path.stem,
                    source_path=pdf_path,
                    page_number=page_number
                )
            )

        pdf.close()

        return pages