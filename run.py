import subprocess
from pathlib import Path

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

supported = {".pdf", ".docx", ".pptx", ".png", ".jpg", ".jpeg"}

files = [
    f for f in INPUT_DIR.iterdir()
    if f.suffix.lower() in supported
]

if not files:
    print("No supported files found.")
    exit()

for file in files:
    print(f"\nProcessing: {file.name}")

    command = [
        "mineru",
        "-p",
        str(file),
        "-o",
        str(OUTPUT_DIR),
        "-b",
        "pipeline"      # CPU backend
    ]

    result = subprocess.run(command)

    if result.returncode == 0:
        print(f"✓ Finished {file.name}")
    else:
        print(f"✗ Failed {file.name}")

print("\nDone.")