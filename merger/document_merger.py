from core.document import Document


class DocumentMerger:

    def merge(self, documents: list[Document]) -> Document:

        merged = Document()

        all_pages = []

        for document in documents:
            all_pages.extend(document.pages)

        all_pages.sort(key=lambda p: p.page_number)

        for page in all_pages:
            merged.add_page(page)

        return merged