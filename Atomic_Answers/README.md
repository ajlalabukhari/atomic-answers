# 🧠 Atomic Answers – A RAG-based Assistant on *Atomic Habits*

**Atomic Answers** is a Retrieval-Augmented Generation (RAG) application built to answer habit-building questions using the content of *Atomic Habits* by James Clear. It uses OpenAI for embedding, Groq for generation (LLaMA3), and ChromaDB as the vector store.

Built with LangChain and Streamlit, this project demonstrates a full-stack, end-to-end RAG pipeline.

---

## 💡 Features

- 📚 Extracts and cleans PDF book into structured Markdown
- 🔗 Chunks content using LangChain's `RecursiveCharacterTextSplitter`
- 🧠 Embeds chunks using OpenAI’s `text-embedding-3-small`
- 🔍 Stores vectors in ChromaDB for similarity search
- 🤖 Uses Groq (LLaMA3-8b-8192) to generate final answers
- 🌐 Clean and simple web UI with Streamlit

---

## 🛠️ Tech Stack

| Layer             | Tool                      |
|------------------|---------------------------|
| Embeddings        | OpenAI                    |
| Generation        | Groq (LLaMA3-8b-8192)      |
| Vector Store      | ChromaDB                  |
| Framework         | LangChain (modular)       |
| UI                | Streamlit                 |
| Language          | Python                    |

---

## 📁 Project Structure

```
Atomic_Answers/
├── app.py                      # Streamlit web app
├── data/
│   ├── atomic_habits_full.md   # Full book in markdown
│   ├── chapters/               # Chapter-wise markdown files
│   ├── chunks_langchain.jsonl  # Chunks for embedding
│   └── embeddings_openai.jsonl # Chunk + embedding JSONL
├── chroma/                     # Local vector DB (auto-created)
├── src/
│   ├── pdf_to_md.py
│   ├── split_md_into_chapters.py
│   ├── chunk_markdown_langchain.py
│   ├── build_chroma_store.py
│   ├── test_chroma_query.py
│   └── rag_ask_groq.py
├── requirements.txt
└── README.md
```

---

## 🚀 Run Locally

1. **Clone the repo**
```bash
git clone https://github.com/yourusername/atomic-answers.git
cd atomic-answers
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv-rag
source .venv-rag/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add your API keys to a `.env` file**
```env
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
```

5. **Run the app**
```bash
streamlit run app.py
```

---

## ⚙️ How It Works

1. 📄 Book content is converted from PDF to Markdown
2. ✂️ Markdown is split into overlapping chunks
3. 🧠 Embeddings are generated via OpenAI
4. 📦 Stored in Chroma for vector-based retrieval
5. 🗣️ Question is matched with top chunks
6. 🤖 Groq (LLaMA3) generates a final answer using the context

---

## 🔮 Future Enhancements

- Add support for multiple books or document sources
- Implement multi-turn chat or conversation history
- Add citation UI for each retrieved chunk
- Switch to local or fine-tuned embedding models for cost savings

---

## 📄 License

MIT — free to use, remix, and share.
