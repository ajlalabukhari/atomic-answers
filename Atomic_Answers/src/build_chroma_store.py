# STEP 5

from pathlib import Path
import os
import json
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# === Load environment ===
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# === Config ===
BASE_DIR = Path(__file__).resolve().parent.parent
EMBEDDINGS_FILE = BASE_DIR / "data" / "embeddings_openai.jsonl"
CHROMA_DIR = BASE_DIR / "chroma"
COLLECTION_NAME = "atomic_answers"

CHROMA_DIR.mkdir(exist_ok=True)

if __name__ == "__main__":
    print("📂 Current working dir:", os.getcwd())
    print("📄 Loading:", EMBEDDINGS_FILE)

    documents = []
    metadatas = []

    with EMBEDDINGS_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            documents.append(obj["content"])
            metadatas.append({
                "chunk_id": obj["chunk_id"],
                "source": obj["source"]
            })

    embedding_function = OpenAIEmbeddings(api_key=openai_key)

    db = Chroma.from_texts(
        texts=documents,
        embedding=embedding_function,
        metadatas=metadatas,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME
    )

    print(f"✅ Chroma vector store created at: {CHROMA_DIR}")
    print(f"📄 Total documents indexed: {len(documents)}")
