from pathlib import Path
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import time

# === Load API key ===
load_dotenv()
client = OpenAI()

# === Files ===
INPUT_FILE = Path("../data/chunks_langchain.jsonl")
OUTPUT_FILE = Path("../data/embeddings_openai.jsonl")

# === OpenAI Model ===
MODEL_NAME = "text-embedding-3-small"

# === Load chunks ===
chunks = [json.loads(line) for line in INPUT_FILE.open("r", encoding="utf-8")]
embedded = []

# === Loop through chunks with token safety
for i, chunk in enumerate(chunks):
    try:
        response = client.embeddings.create(
            model=MODEL_NAME,
            input=chunk["content"]
        )
        chunk["embedding"] = response.data[0].embedding
        embedded.append(chunk)

        # Optional delay to slow things down
        time.sleep(0.2)

    except Exception as e:
        print(f"⚠️ Error on chunk {chunk['chunk_id']}: {e}")

# === Save to file ===
with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    for item in embedded:
        f.write(json.dumps(item) + "\n")

print(f"✅ Embedded {len(embedded)} chunks with OpenAI")
print(f"📄 Output: {OUTPUT_FILE}")
