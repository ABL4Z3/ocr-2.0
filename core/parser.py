import json

from pathlib import Path

from core.document import Document
from core.elements import (
    Title,
    Paragraph,
    Table,
    Image
)


def parse_output(original_file, output_dir):

    print("Parser started")

    try:
        folder = output_dir / original_file.stem
        print(folder)

        json_files = list(folder.glob("*content_list_v2.json"))
        print(json_files)

        if not json_files:
            print("No JSON found")
            return

        json_file = json_files[0]
        print("Opening:", json_file)

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("JSON loaded")
        print(type(data))
        print(len(data))

    except Exception as e:
        print("ERROR:", repr(e))
def parse_elements(data, document):

    for page_no, page in enumerate(data):

        current_page = document.get_page(page_no)

        for item in page:

            t = item["type"]

            if t == "title":

                text = ""

                for x in item["content"]["title_content"]:
                    text += x["content"] + " "

                current_page.add(
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

                current_page.add(
                    Paragraph(
                        type="paragraph",
                        text=text.strip(),
                        bbox=item["bbox"]
                    )
                )

            elif t == "table":

                current_page.add(
                    Table(
                        type="table",
                        html=item["content"]["html"],
                        bbox=item["bbox"]
                    )
                )

            elif t == "image":

                current_page.add(
                    Image(
                        type="image",
                        path=item["content"]["image_source"]["path"],
                        bbox=item["bbox"]
                    )
                )
def print_summary(document):

    titles = 0
    paragraphs = 0
    tables = 0
    images = 0

    for page in document.pages:

        for element in page.elements:

            if element.type == "title":
                titles += 1

            elif element.type == "paragraph":
                paragraphs += 1

            elif element.type == "table":
                tables += 1

            elif element.type == "image":
                images += 1

    print()

    print("=" * 40)

    print("DOCUMENT SUMMARY")

    print("=" * 40)

    print("Pages      :", len(document.pages))
    print("Titles     :", titles)
    print("Paragraphs :", paragraphs)
    print("Tables     :", tables)
    print("Images     :", images)

    print("=" * 40)