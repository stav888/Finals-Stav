# 📄 RAG — Chat with a Word Document

Build a complete RAG (Retrieval-Augmented Generation) pipeline that loads a `.docx` Word file, chunks it, stores the embeddings in ChromaDB, and lets you ask questions about the document's content.

## 🎯 Project Overview

This project implements a 5-step RAG pipeline:

1. **Load** — Load a `.docx` Word document using LangChain's `Docx2txtLoader`
2. **Chunk** — Split text into chunks using `RecursiveCharacterTextSplitter`
3. **Embed & Store** — Create embeddings and store in ChromaDB vector database
4. **Retrieve** — Find relevant chunks for each question
5. **Answer** — Use an LLM to generate answers based on retrieved chunks

## 📋 Features

✅ Load and process `.docx` Word documents  
✅ Split large documents into manageable chunks  
✅ Store embeddings in persistent ChromaDB  
✅ Ask 5+ questions about the document  
✅ Get LLM answers with source context  
✅ Two versions: **Paid (OpenAI)** and **Free (Local)**  

## 🚀 Quick Start

### Option 1: Free Version (No API Key Needed) ⭐

```bash
# 1. Install Ollama first: https://ollama.ai/
# 2. Download model: ollama pull llama3.2
# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Place your Word document in this directory
# 5. Update DOCX_PATH in rag_word_free.py
# 6. Run the script
python rag_word_free.py
```

**Requirements:**
- Python 3.8+
- Ollama (free, local LLM)
- ~5-10 minutes for first run (model download & embedding creation)

**No costs. No API keys. Runs locally.**

---

### Option 2: Paid Version (Using OpenAI GPT-4o-mini)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up your OpenAI API key
#    - Copy .env.example to .env
#    - Add your OpenAI API key: OPENAI_API_KEY=sk-...
#    - Get key at: https://platform.openai.com/api-keys

# 3. Place your Word document in this directory
# 4. Update DOCX_PATH in rag_word.py
# 5. Run the script
python rag_word.py
```

**Requirements:**
- Python 3.8+
- OpenAI API key (paid, but cheap ~$0.01 per request)

**Faster responses. Better answers. Costs money.**

---

## 📁 Project Structure

```
03-rag-word/
├── rag_word.py              # Main script (uses OpenAI GPT-4o-mini)
├── rag_word_free.py         # Free version (uses local Ollama + embeddings)
├── requirements.txt          # Python dependencies
├── .env.example              # Template for API key configuration
├── your_document.docx        # 👈 YOUR WORD DOCUMENT GOES HERE
├── chroma_docx_db/           # Vector store (auto-created)
└── README.md                 # This file
```

## 🔧 Installation & Setup

### Step 1: Clone / Navigate to Project

```bash
cd 03-rag-word
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4a: Free Version Setup (Recommended for Learning)

```bash
# Install Ollama from https://ollama.ai/
# Then download the model:
ollama pull llama3.2

# Now you're ready! No API key needed.
```

### Step 4b: Paid Version Setup (Recommended for Production)

```bash
# Get your OpenAI API key at https://platform.openai.com/api-keys

# Create .env file
cp .env.example .env

# Edit .env and add your key:
# OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 5: Prepare Your Word Document

- Place any `.docx` file in this directory
- Update the `DOCX_PATH` variable in the Python script

Example:
```python
DOCX_PATH = "my_research_paper.docx"  # Change this line
```

### Step 6: Run the Script

```bash
# Free version
python rag_word_free.py

# Or paid version
python rag_word.py
```

## 📊 Output Example

```
════════════════════════════════════════════════════════════════════════════════
📋 QUESTION & ANSWER RESULTS
════════════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────────────
Question 1: What is the main topic of this document?
────────────────────────────────────────────────────────────────────────────────

🤖 Answer:
The main topic of this document is [LLM's answer based on document content]...

📚 Retrieved Context Chunks (3 chunks):

  [1] [First 200 characters of relevant chunk 1]...
      (continued...)

  [2] [First 200 characters of relevant chunk 2]...
      (continued...)

  [3] [First 200 characters of relevant chunk 3]...
      (continued...)
```

## 🎓 Assignment Requirements

✅ **4 pts** — Load `.docx` and split into chunks (print chunk count)  
✅ **4 pts** — Create embeddings and store in ChromaDB  
✅ **6 pts** — Answer 5 questions with LLM  
✅ **4 pts** — Print retrieved context chunks alongside answers  
✅ **2 pts** — Questions are relevant and non-trivial  

**Total: 20 Points**

## 📝 Customizing Your Questions

Edit the `questions` list in either script to ask specific questions about your document:

```python
questions = [
    "What is the main topic of this document?",
    "Who are the key people or entities mentioned?",
    "What are the main conclusions or findings?",
    "What problems or challenges are discussed?",
    "What solutions or recommendations are provided?",
    # Add your own questions here
]
```

## 🔍 How It Works

### 1. Document Loading
- Uses `Docx2txtLoader` to extract text from Word files
- Prints number of pages/sections loaded

### 2. Chunking
- Splits text into 500-character chunks
- 60-character overlap preserves context at boundaries
- Prevents loss of information at chunk boundaries

### 3. Embedding
- Creates vector embeddings for each chunk
- **Free version**: Uses `SentenceTransformerEmbeddings` (local)
- **Paid version**: Uses OpenAI's `text-embedding-3-small` (best quality)

### 4. Vector Storage
- Stores embeddings in ChromaDB
- Persists to `./chroma_docx_db` directory
- Enables fast similarity search

### 5. Question Answering
- Retrieves top-3 most relevant chunks for each question
- Passes chunks + question to LLM
- LLM generates answer based on context
- **Result**: Answers grounded in your document, not just LLM knowledge!

## ⚡ Troubleshooting

### Error: `OPENAI_API_KEY is not set`

**Solution**: Use the free version OR set your API key:
```bash
# Create .env file with:
OPENAI_API_KEY=sk-your-key-here
```

### Error: `your_document.docx not found`

**Solution**: Place your Word document in the same directory and update:
```python
DOCX_PATH = "your_actual_file.docx"
```

### Error: `Could not connect to Ollama`

**Solution**: Install and start Ollama:
1. Download Ollama: https://ollama.ai/
2. Run: `ollama pull llama3.2`
3. Start Ollama (it runs in the background)
4. Then run the script

### Error: `chromadb` or other import errors

**Solution**: Reinstall dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## 📚 Reference Implementation

This project is based on the official LangChain RAG tutorial:
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [RAG Tutorial](https://python.langchain.com/docs/modules/retrieval_augmented_generation/)

## 🆓 Free Alternatives

### Embedding Models (No API Key)
- `SentenceTransformerEmbeddings` ← Used in `rag_word_free.py`
- `HuggingFaceEmbeddings`
- `LlamaCppEmbeddings`

### LLM Models (No API Key)
- `Ollama` (llama3.2) ← Used in `rag_word_free.py`
- `LlamaCpp` (via llama.cpp)
- `GPT4All`

### Vector Databases
- `ChromaDB` ← Used in both versions
- `Faiss`
- `Milvus`

## 💡 Pro Tips

1. **Start with the free version** to learn the concepts
2. **Adjust chunk size** if answers are too generic (increase to 1000) or too specific (decrease to 250)
3. **Modify search_kwargs** to retrieve more/fewer chunks:
   ```python
   search_kwargs={"k": 5}  # Retrieve 5 chunks instead of 3
   ```
4. **Use temperature=0** for consistent, factual answers
5. **Save your vector store** — it's reusable without re-processing!

## 📞 Support

If you encounter issues:
1. Check the error message in the console
2. Try the **Free Version** first
3. Ensure all dependencies are installed: `pip list | grep langchain`
4. Check that your Word document is valid and readable

## 📜 License

This project is provided for educational purposes as part of the Python AI course.

---

**Happy RAG-ing! 🚀 Ask your documents questions now!**
