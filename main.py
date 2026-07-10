from pathlib import Path

from splitter.pdf_splitter import PDFSplitter
from analyzer.page_analyzer import PageAnalyzer
from planner.batch_planner import BatchPlanner

from extractors.mineru import MinerUExtractor
from extractors.parser import MinerUParser
from extractors.paddleocr import PaddleOCRExtractor

from merger.document_merger import DocumentMerger

from validator.document_validator import DocumentValidator
from repair.table_repair import TableRepair

from exporters.markdown_exporter import MarkdownExporter
from exporters.json_exporter import JsonExporter


INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

SUPPORTED = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".docx",
    ".pptx",
}


def process_document(file: Path):

    print("=" * 80)
    print(f"Processing : {file.name}")
    print("=" * 80)

    # ----------------------------------------------------
    # Split
    # ----------------------------------------------------

    splitter = PDFSplitter()

    pages = splitter.split(file)

    # ----------------------------------------------------
    # Analyze
    # ----------------------------------------------------

    analyzer = PageAnalyzer()

    page_jobs = []

    for page in pages:
        page_jobs.append(
            analyzer.analyze(page)
        )

    # ----------------------------------------------------
    # Batch Planning
    # ----------------------------------------------------

    planner = BatchPlanner()

    batches = planner.create_batches(page_jobs)

    documents = []

    mineru = MinerUExtractor(OUTPUT_DIR)

    mineru_parser = MinerUParser()

    paddle = PaddleOCRExtractor()

    # ----------------------------------------------------
    # Process batches
    # ----------------------------------------------------

    for batch in batches:

        first = batch.pages[0].page_number + 1
        last = batch.pages[-1].page_number + 1

        print()
        print(
            f"Batch {first}-{last} | {batch.extractor}"
        )

        if batch.extractor == "mineru":

            output_folder = mineru.extract(batch)

            document = mineru_parser.parse(
                batch,
                output_folder
            )

        else:

            document = paddle.parse(batch)

        documents.append(document)

    # ----------------------------------------------------
    # Merge
    # ----------------------------------------------------

    merger = DocumentMerger()

    final_document = merger.merge(documents)

    # ----------------------------------------------------
    # Validate
    # ----------------------------------------------------

    validator = DocumentValidator()

    broken_tables = validator.validate(
        final_document
    )

    if broken_tables:

        print(f"Repairing {len(broken_tables)} tables...")

        repair = TableRepair()

        for page, table in broken_tables:
            repair.repair(page, table)

    # ----------------------------------------------------
    # Export Markdown
    # ----------------------------------------------------

    markdown = MarkdownExporter().export(
        final_document
    )

    md_path = OUTPUT_DIR / f"{file.stem}.md"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    # ----------------------------------------------------
    # Export JSON
    # ----------------------------------------------------

    json_path = OUTPUT_DIR / f"{file.stem}.json"

    JsonExporter().export(
        final_document,
        json_path
    )

    print()
    print("Markdown :", md_path)
    print("JSON     :", json_path)
    print("Completed.")

    return md_path


def main():

    files = [

        f

        for f in INPUT_DIR.iterdir()

        if f.suffix.lower() in SUPPORTED

    ]

    if not files:

        print("No files found.")

        return

    for file in files:

        process_document(file)

    print()
    print("=" * 80)
    print("ALL DOCUMENTS COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    main()