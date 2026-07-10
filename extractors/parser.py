import json
from pathlib import Path
from core.document import Document
from core.page import Page
from core.elements import (
    Title,
    Paragraph,
    Table,
    Image
)


class MinerUParser:

    def parse(self, batch, output_folder):

        batch_folder = output_folder / "batch"

        auto = batch_folder / "auto"

        if not auto.exists():
            raise FileNotFoundError(
                f"Auto folder not found: {auto}"
            )

        json_files = sorted(
            auto.glob("*content_list_v2.json")
        )

        if not json_files:
            raise FileNotFoundError(
                f"No content_list_v2.json found inside {auto}"
            )

        print(f"Using JSON: {json_files[0]}")

        with open(
            json_files[0],
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        if len(data) != len(batch.pages):

            raise RuntimeError(
                "Batch page count does not match JSON page count."
            )

        document = Document()

        for json_page, page_job in zip(data, batch.pages):

            page = self._parse_page(
                page_job.page_number,
                json_page
            )

            page_job.parsed_page = page

            document.add_page(page)

        return document
    def _parse_page(self, page_number, page_data):

        page = Page(page_number)

        for item in page_data:

            t = item["type"]

            if t == "title":

                text = ""

                for x in item["content"]["title_content"]:
                    text += x["content"] + " "

                page.add(
                    Title(
                        type="title",
                        text=text.strip(),
                        bbox=item["bbox"],
                        level=item["content"]["level"]
                    )
                )

            elif t == "paragraph":

                text = ""

                for x in item["content"]["paragraph_content"]:
                    text += x["content"] + " "

                page.add(
                    Paragraph(
                        type="paragraph",
                        text=text.strip(),
                        bbox=item["bbox"]
                    )
                )

            elif t == "table":

                page.add(
                    Table(
                        type="table",
                        html=item["content"]["html"],
                        bbox=item["bbox"]
                    )
                )

            elif t == "image":

                page.add(
                    Image(
                        type="image",
                        path=item["content"]["image_source"]["path"],
                        bbox=item["bbox"]
                    )
                )

        return page