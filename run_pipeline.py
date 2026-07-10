import os
import sys
import json
import traceback
from dataclasses import asdict
from pathlib import Path
from time import time

# Ensure backend is importable
ROOT = Path(__file__).parent
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from app.analyzer.detector import DocumentAnalyzer
from app.extractors.factory import ExtractorFactory
from app.normalizer.normalizer import Normalizer
from app.chunking.builder import ChunkBuilder
from app.metadata.enricher import MetadataEnricher

INPUT_DIR = ROOT / "input"
OUTPUT_DIR = ROOT / "output_processed"
OUTPUT_DIR.mkdir(exist_ok=True)


def find_pdfs(base: Path):
    for p in base.rglob("*.pdf"):
        yield p


def process_pdf(pdf_path: Path):
    out_dir = OUTPUT_DIR / pdf_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Processing {pdf_path}")

    # Analyzer
    print("[STAGE] Analyzer START")
    t0 = time()
    analysis = DocumentAnalyzer.analyze(str(pdf_path))
    print(f"[STAGE] Analyzer END ({time()-t0:.3f}s)")
    (out_dir / "01_analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")

    # Extractor
    print("[STAGE] Extractor START")
    t0 = time()
    extractor = ExtractorFactory.get(analysis.get("searchable", False))
    page_contents = extractor.extract(str(pdf_path))
    print(f"[STAGE] Extractor END ({time()-t0:.3f}s) - extractor={extractor.__class__.__name__}")
    raw_out = []
    for p in page_contents:
        try:
            raw_out.append({"page": getattr(p, "page_number", None), "text": getattr(p, "text", getattr(p, "content", None))})
        except Exception:
            raw_out.append({"raw": str(p)})
    (out_dir / "02_raw_text.json").write_text(json.dumps(raw_out, ensure_ascii=False, indent=2), encoding="utf-8")

    # Advanced Reconstructor (must succeed or raise)
    print("[STAGE] AdvancedReconstructor START")
    t0 = time()
    from app.table_reconstructor.advanced_reconstructor import AdvancedReconstructor

    adv = AdvancedReconstructor()
    blocks = adv.build_from_pdf(str(pdf_path))
    print(f"[STAGE] AdvancedReconstructor END ({time()-t0:.3f}s) - blocks={len(blocks)}")

    # Dump blocks
    b_out = []
    for b in blocks:
        b_out.append({"page": getattr(b, "page", None), "type": getattr(b, "type", None), "content": getattr(b, "content", None)})
    (out_dir / "03_blocks.json").write_text(json.dumps(b_out, ensure_ascii=False, indent=2), encoding="utf-8")

    # Normalizer
    print("[STAGE] Normalizer START")
    t0 = time()
    normalizer = Normalizer()
    blocks = normalizer.normalize(blocks)
    print(f"[STAGE] Normalizer END ({time()-t0:.3f}s)")

    # Table reconstructor
    print("[STAGE] TableReconstructor START")
    t0 = time()
    from app.table_reconstructor.reconstructor import TableReconstructor

    recon = TableReconstructor()
    blocks = recon.reconstruct(blocks)
    print(f"[STAGE] TableReconstructor END ({time()-t0:.3f}s)")

    # Semantic mapper -> canonical Document
    print("[STAGE] Semantic Mapper START")
    t0 = time()
    from app.document.mapper.pipeline import MapperPipeline

    pipeline = MapperPipeline()
    document = pipeline.map(blocks, document_name=pdf_path.name)
    print(f"[STAGE] Semantic Mapper END ({time()-t0:.3f}s)")

    # Dump canonical document
    # Serialize canonical document safely. Use dataclasses.asdict then sanitize
    try:
        doc_obj = asdict(document)
        # sanitize 'raw' fields that may contain unserializable objects or circular refs
        def sanitize(o):
            if isinstance(o, dict):
                if "raw" in o:
                    try:
                        json.dumps(o["raw"])  # test serializability
                        o["raw"] = o["raw"]
                    except Exception:
                        o["raw"] = None
                for k, v in list(o.items()):
                    sanitize(v)
            elif isinstance(o, list):
                for v in o:
                    sanitize(v)

        sanitize(doc_obj)
        (out_dir / "04_document.json").write_text(json.dumps(doc_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        # last-resort: fallback to string representation
        (out_dir / "04_document.json").write_text(json.dumps({"repr": str(document)}, ensure_ascii=False, indent=2), encoding="utf-8")

    # Markdown exporter
    print("[STAGE] Markdown Exporter START")
    t0 = time()
    from app.document.exporters.markdown import document_to_markdown

    markdown = document_to_markdown(document)
    (out_dir / "05_markdown.md").write_text(markdown, encoding="utf-8")
    print(f"[STAGE] Markdown Exporter END ({time()-t0:.3f}s)")

    # Chunk builder
    print("[STAGE] ChunkBuilder START")
    t0 = time()
    chunker = ChunkBuilder()
    chunks = chunker.build(markdown, document_id=pdf_path.stem)
    print(f"[STAGE] ChunkBuilder END ({time()-t0:.3f}s) - chunks={len(chunks)}")
    (out_dir / "06_chunks.json").write_text(json.dumps([asdict(c) for c in chunks], ensure_ascii=False, indent=2), encoding="utf-8")

    # Metadata
    print("[STAGE] Metadata Enricher START")
    t0 = time()
    enricher = MetadataEnricher()
    chunks = enricher.enrich_chunks(chunks, document_name=pdf_path.name, document_entities=[])
    (out_dir / "07_metadata.json").write_text(json.dumps({"document_name": pdf_path.name, "pages": analysis.get("pages"), "searchable": analysis.get("searchable")}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[STAGE] Metadata Enricher END ({time()-t0:.3f}s)")

    print(f"Wrote outputs to {out_dir}")


def main():
    pdfs = list(find_pdfs(INPUT_DIR))
    if not pdfs:
        print("No PDFs found under input/ to process.")
        return

    for p in pdfs:
        try:
            process_pdf(p)
        except Exception as e:
            print(f"Error processing {p}: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
