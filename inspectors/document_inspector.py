from core.elements import (
    Title,
    Paragraph,
    Table,
    Image
)


def inspect_document(document):

    print("\n")
    print("=" * 70)
    print("DOCUMENT INSPECTOR")
    print("=" * 70)

    for page in document.pages:

        print(f"\nPAGE {page.page_number + 1}")
        print("-" * 70)

        for index, element in enumerate(page.elements, start=1):

            print(f"\nElement {index}")

            if isinstance(element, Title):

                print("[TITLE]")
                print(element.text)

            elif isinstance(element, Paragraph):

                print("[PARAGRAPH]")

                preview = element.text

                if len(preview) > 250:
                    preview = preview[:250] + "..."

                print(preview)

            elif isinstance(element, Table):

                print("[TABLE]")

                print("Bounding Box :", element.bbox)

                print("HTML Length  :", len(element.html))

                preview = element.html

                if len(preview) > 400:
                    preview = preview[:400] + "..."

                print(preview)

            elif isinstance(element, Image):

                print("[IMAGE]")

                print("Path :", element.path)

        print("\n")