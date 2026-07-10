from bs4 import BeautifulSoup
import pandas as pd

from core.elements import Paragraph
from core.elements import Title
from core.elements import Table


class MarkdownExporter:

    def html_table_to_markdown(self, html: str) -> str:
        """
        Convert HTML tables into Markdown tables.
        Falls back to plain text if conversion fails.
        """

        try:

            dfs = pd.read_html(html)

            output = []

            for df in dfs:

                df = df.fillna("")

                output.append(

                    df.to_markdown(

                        index=False,

                        tablefmt="github"

                    )

                )

            return "\n\n".join(output)

        except Exception:

            soup = BeautifulSoup(html, "html.parser")

            return soup.get_text(
                "\n",
                strip=True
            )

    def export(self, document):

        markdown = []

        for page in document.pages:

            markdown.append(f"# Page {page.page_number}\n")

            for element in page.elements:

                if isinstance(element, Title):

                    markdown.append(f"# {element.text}\n")

                elif isinstance(element, Paragraph):

                    markdown.append(element.text + "\n")

                elif isinstance(element, Table):

                    markdown.append(
                        self.html_table_to_markdown(
                            element.html
                        )
                    )

                    markdown.append("\n")

        return "\n".join(markdown)