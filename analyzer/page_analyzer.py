from core.page_job import PageJob

import fitz


class PageAnalyzer:

    def analyze(self, page_job: PageJob):

        pdf = fitz.open(page_job.source_path)

        page = pdf.load_page(page_job.page_number)

        text = page.get_text("text").strip()

        images = page.get_images(full=True)

        if len(text) > 50:
            page_job.page_type = "digital"
            page_job.extractor = "mineru"
        else:
            page_job.page_type = "scanned"
            page_job.extractor = "paddleocr"

        pdf.close()

        return page_job