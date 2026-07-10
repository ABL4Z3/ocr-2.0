from pathlib import Path
import numpy as np
import fitz
from PIL import Image

from core.document import Document
from core.page import Page

from core.elements import (
    Title,
    Paragraph,
    Table,
    Image as ImageElement
)

from ocr.engine import OCREngine


class PaddleOCRExtractor:

    def __init__(self):

        self.pipeline = OCREngine.get()

    # ---------------------------------------------------------
    # Main Entry
    # ---------------------------------------------------------

    def parse(self, batch):

        """
        Process every scanned page inside a PageBatch.

        Returns:
            Document
        """

        document = Document()

        for page_job in batch.pages:

            print(
                f"OCR Page {page_job.page_number + 1}"
            )

            image = self._render_pdf_page(page_job)

            results = list(
                self.pipeline.predict(image)
            )

            if not results:

                continue

            page = self._parse_result(

                page_job.page_number,

                results[0]

            )

            page_job.parsed_page = page

            document.add_page(page)

        return document

    # ---------------------------------------------------------
    # Render PDF Page
    # ---------------------------------------------------------



    def _render_pdf_page(self, page_job):

        pdf = fitz.open(page_job.source_path)

        page = pdf.load_page(page_job.page_number)

        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))

        pdf.close()

        image = np.frombuffer(
            pix.samples,
            dtype=np.uint8
        ).reshape(
            pix.height,
            pix.width,
            pix.n
        )

        return image

    # ---------------------------------------------------------
    # Parse One OCR Result
    # ---------------------------------------------------------

    def _parse_result(self, page_number, result):

        page = Page(page_number)

        md = result.markdown

        if isinstance(md, dict):

            text = md.get("markdown_texts", "").strip()

            if text:

                page.add(

                    Paragraph(

                        type="paragraph",

                        text=text,

                        bbox=[0, 0, 0, 0]

                    )

                )

        html = result.html

        if isinstance(html, dict):

            table_html = html.get("html")

            if table_html:

                page.add(

                    Table(

                        type="table",

                        html=table_html,

                        bbox=[0, 0, 0, 0]

                    )

                )

        return page