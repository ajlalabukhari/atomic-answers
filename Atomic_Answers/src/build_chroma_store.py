from pathlib import Path
import os
import json
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings


# === Load environment ===
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

# === Config ===
EMBEDDINGS_FILE = Path("../data/embeddings_openai.jsonl")
CHROMA_DIR = "../chroma"
Path(CHROMA_DIR).mkdir(exist_ok=True)

# === Load documents ===
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

# === OpenAI Embedding function (used just for vector space config) ===
embedding_function = OpenAIEmbeddings(api_key=openai_key)

# === Create and persist Chroma DB ===
db = Chroma.from_texts(
    texts=documents,
    embedding=embedding_function,
    metadatas=metadatas,
    persist_directory=CHROMA_DIR
)



print(f"✅ Chroma vector store created at: {CHROMA_DIR}")
print(f"📄 Total documents indexed: {len(documents)}")
