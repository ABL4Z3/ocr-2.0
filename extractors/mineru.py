import shutil
import subprocess
import tempfile

from pathlib import Path

import fitz

from core.page_batch import PageBatch


class MinerUExtractor:

    def __init__(self, output_root: Path):

        self.output_root = output_root

    def extract(self, batch: PageBatch):

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_dir = Path(temp_dir)

            temp_pdf = temp_dir / "batch.pdf"

            # -----------------------------------
            # Create temporary PDF
            # -----------------------------------

            src = fitz.open(batch.pages[0].source_path)

            dst = fitz.open()

            for page in batch.pages:

                dst.insert_pdf(
                    src,
                    from_page=page.page_number,
                    to_page=page.page_number
                )

            dst.save(temp_pdf)

            dst.close()
            src.close()

            # -----------------------------------
            # Output Folder
            # -----------------------------------

            first = batch.pages[0].page_number + 1
            last = batch.pages[-1].page_number + 1

            output_folder = (
                self.output_root
                / batch.pages[0].document_name
                / f"pages_{first:03d}_{last:03d}"
            )

            output_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            # -----------------------------------
            # Run MinerU
            # -----------------------------------

            command = [

                "mineru",

                "-p",
                str(temp_pdf),

                "-o",
                str(output_folder),

                "-b",
                "pipeline"

            ]

            result = subprocess.run(command)

            if result.returncode != 0:

                return None

            return output_folder