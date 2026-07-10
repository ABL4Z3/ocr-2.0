from dataclasses import dataclass

from core.elements import Paragraph, Title, Table


@dataclass
class Chunk:
    text: str
    page: int
    metadata: dict


class Chunker:

    def __init__(self, max_chars=1200, overlap=200):

        self.max_chars = max_chars
        self.overlap = overlap

    def chunk(self, document):

        chunks = []

        current = ""

        current_page = 1

        for page in document.pages:

            current_page = page.page_number + 1

            for element in page.elements:

                if isinstance(element, Title):

                    text = "\n# " + element.text + "\n"

                elif isinstance(element, Paragraph):

                    text = element.text + "\n"

                elif isinstance(element, Table):

                    text = element.html + "\n"

                else:

                    continue

                if len(current) + len(text) > self.max_chars:

                    chunks.append(

                        Chunk(

                            text=current,

                            page=current_page,

                            metadata={

                                "page": current_page

                            }

                        )

                    )

                    current = current[-self.overlap:] + text

                else:

                    current += text

        if current.strip():

            chunks.append(

                Chunk(

                    text=current,

                    page=current_page,

                    metadata={

                        "page": current_page

                    }

                )

            )

        return chunks
    