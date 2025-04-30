import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from groq import Groq
from dotenv import load_dotenv
import os

# === Load environment ===
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

# === Set up clients ===
embedding_function = OpenAIEmbeddings(api_key=openai_key)
groq_client = Groq(api_key=groq_key)
db = Chroma(persist_directory="chroma", embedding_function=embedding_function)

# === Streamlit UI ===
st.set_page_config(page_title="Atomic Answers", layout="centered")
st.title("📘 Atomic Answers")
st.subheader("Ask anything from *Atomic Habits*")

question = st.text_input("❓ Your Question", placeholder="e.g., How can I make a habit stick?")

if question:
    with st.spinner("Searching and thinking..."):
        docs = db.similarity_search(question, k=3)
        context = "\n\n".join(doc.page_content for doc in docs)

        prompt = f"""
        You are a helpful assistant trained on the book Atomic Habits.

        Use only the context below to answer the question in a clear and actionable way.

        Context:
        {context}

        Question: {question}
        Answer:
        """

        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        answer = response.choices[0].message.content

        st.markdown("### 🧠 Answer")
        st.write(answer)

        with st.expander("📄 Sources"):
            for i, doc in enumerate(docs):
                st.markdown(f"**Chunk {i+1}** — `{doc.metadata.get('source')}`")
                st.write(doc.page_content)
                st.markdown("---")
