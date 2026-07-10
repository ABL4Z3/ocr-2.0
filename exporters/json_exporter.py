import json
from dataclasses import asdict


class JsonExporter:

    def export(self, document, output):

        data = []

        for page in document.pages:

            page_data = {

                "page": page.page_number,

                "elements": []

            }

            for element in page.elements:

                page_data["elements"].append(

                    asdict(element)

                )

            data.append(page_data)

        with open(output, "w", encoding="utf8") as f:

            json.dump(data, f, indent=2, ensure_ascii=False)