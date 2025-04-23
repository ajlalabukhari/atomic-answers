from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json

# === CONFIG ===
INPUT_DIR = Path("../data/chapters")
EXTRA_FILE = Path("../data/additional_data.md")
OUTPUT_FILE = Path("../data/chunks_langchain.jsonl")

# === CHUNKING STRATEGY ===
# Explanation:
# We want ~500 character chunks with 100 character overlap.
# Recursive splitter will try to split on double newlines, single newlines, then spaces — to avoid cutting mid-sentence.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)

def load_and_chunk(file_path: Path):
    """Load a markdown file and return LangChain-style chunks"""
    content = file_path.read_text(encoding="utf-8")
    chunks = splitter.create_documents([content])
    return [
        {
            "source": str(file_path),
            "chunk_id": f"{file_path.stem}_{i}",
            "content": doc.page_content
        }
        for i, doc in enumerate(chunks)
    ]

def run_chunking():
    print("📂 Loading markdown files...")
    all_chunks = []

    for file in sorted(INPUT_DIR.glob("*.md")):
        file_chunks = load_and_chunk(file)
        all_chunks.extend(file_chunks)

    if EXTRA_FILE.exists():
        extra_chunks = load_and_chunk(EXTRA_FILE)
        all_chunks.extend(extra_chunks)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + "\n")

    print(f"✅ Chunked {len(all_chunks)} total pieces using LangChain.")
    print(f"📄 Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    run_chunking()
