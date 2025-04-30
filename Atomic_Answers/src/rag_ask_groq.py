from dotenv import load_dotenv
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from groq import Groq

# === Load .env variables ===
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

# === Initialize Groq client ===
groq_client = Groq(api_key=groq_key)

# === Load Chroma vector store ===
embedding_function = OpenAIEmbeddings(api_key=openai_key)
db = Chroma(persist_directory="../chroma", embedding_function=embedding_function)

# === Ask a question ===
question = "How can I build a habit that sticks over time?"

# === Retrieve top chunks ===
docs = db.similarity_search(question, k=3)
context = "\n\n".join([doc.page_content for doc in docs])

# === Build prompt ===
prompt = f"""
You are a helpful assistant trained on the book Atomic Habits.

Use only the context provided below to answer the question in clear, friendly, and actionable terms.

Context:
{context}

Question: {question}
Answer:
"""

# === Query Groq (LLaMA3) ===
response = groq_client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.7
)

# === Show final result ===
print("\n🧠 Final Answer from Groq:")
print(response.choices[0].message.content)
