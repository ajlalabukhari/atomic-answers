from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# === Step 1: Load .env and embedding function ===
load_dotenv()
embedding_function = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

# === Step 2: Load persisted Chroma store ===
CHROMA_DIR = "../chroma"
db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding_function)

# === Step 3: Ask a question ===
query = "How do I make a habit stick?"
top_k = 3

# === Step 4: Get top results ===
results = db.similarity_search(query, k=top_k)

# === Step 5: Print matches ===
for i, doc in enumerate(results):
    print(f"\n🔹 Match {i+1}:")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Chunk ID: {doc.metadata.get('chunk_id')}")
    print("Content:")
    print(doc.page_content)
    print("-" * 60)
