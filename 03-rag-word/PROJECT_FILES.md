# 📂 Project Files Overview

This document describes each file in the 03-rag-word project.

## 🚀 Main Scripts (Choose One)

### `rag_word.py` ⭐ **PAID VERSION**
- **Use when**: You have an OpenAI API key
- **Features**: Uses GPT-4o-mini for best quality answers
- **Cost**: ~$0.01 per run (very cheap)
- **Speed**: Faster responses
- **Setup**: Requires `.env` file with `OPENAI_API_KEY`
- **Run**: `python rag_word.py`

### `rag_word_free.py` ⭐ **FREE VERSION (Recommended)**
- **Use when**: You want no costs, local solution
- **Features**: Uses Ollama + local embeddings
- **Cost**: $0 (completely free)
- **Speed**: Slower but works offline
- **Setup**: Requires Ollama installed locally
- **Run**: `python rag_word_free.py`

---

## 📚 Documentation

### `README.md` 📖
**Complete project documentation**
- Project overview & goals
- Installation instructions (both versions)
- Feature list & project structure
- Troubleshooting guide
- Pro tips for optimization
- **Read this first!**

### `QUICK_START.md` ⚡
**5-minute setup guide**
- Fast instructions for getting started
- Common issues & solutions
- Expected output format
- Next steps after setup

### `PROJECT_FILES.md` (This File)
**Description of all project files**
- What each file does
- When to use each file
- File relationships

---

## ⚙️ Configuration & Demo

### `config.py` ⚙️
**Configuration file for settings**
- Document path
- Chunk size & overlap settings
- Retrieval parameters
- LLM model settings
- Questions to ask
- Advanced settings
- **Edit this to customize behavior**

### `demo.py` 🎓
**Example implementations & code snippets**
- Example 1: Basic RAG pipeline
- Example 2: With local LLM
- Example 3: With OpenAI
- Example 4: Batch questions
- Example 5: Custom configuration
- Example 6: Load existing vector store
- Example 7: With metadata
- **Copy & modify for your projects**

---

## 📦 Dependencies & Setup

### `requirements.txt` 📦
**Python packages to install**
- langchain (RAG framework)
- langchain-community (connectors)
- langchain-openai (OpenAI integration)
- chromadb (vector database)
- docx2txt (Word document reading)
- python-dotenv (environment variables)
- sentence-transformers (local embeddings)

**Install with**: `pip install -r requirements.txt`

### `.env.example` 🔐
**Template for API keys**
- Shows how to structure `.env` file
- Add your OpenAI API key here
- **Never commit real `.env` to git!**
- **Rename to `.env` and add your key**

---

## 📁 Auto-Generated Folders

### `chroma_docx_db/` 🗄️
**Vector store (created by script)**
- Auto-generated after first run
- Stores embeddings for your document
- Persists so you don't re-process
- Safe to delete & recreate anytime

---

## 🎯 Quick File Reference

| File | Purpose | Read Time | Edit? |
|------|---------|-----------|-------|
| `README.md` | Full documentation | 10 min | ❌ No |
| `QUICK_START.md` | Fast setup guide | 2 min | ❌ No |
| `rag_word.py` | Main script (paid) | - | ⚠️ Change DOCX_PATH only |
| `rag_word_free.py` | Main script (free) | - | ⚠️ Change DOCX_PATH only |
| `config.py` | Settings & questions | 5 min | ✅ Yes, customize! |
| `demo.py` | Code examples | 5 min | ✅ Yes, copy snippets |
| `requirements.txt` | Dependencies | 1 min | ❌ No |
| `.env.example` | API key template | 1 min | ✅ Copy to .env |

---

## 🔄 Typical Workflow

1. **Read**: `README.md` (5-10 minutes)
2. **Setup**: `QUICK_START.md` (5 minutes)
3. **Configure**: Edit `config.py` with your questions
4. **Place**: Your `.docx` file in this directory
5. **Update**: `DOCX_PATH` in main script
6. **Run**: `python rag_word_free.py` (or rag_word.py)
7. **Review**: Output with answers & sources
8. **Customize**: Modify `config.py` for different questions
9. **Learn**: Read `demo.py` for advanced usage

---

## 💡 Pro Tips

- **Start with `QUICK_START.md`** — fastest way to run
- **Use FREE version first** — learn concepts without costs
- **Customize in `config.py`** — no need to edit main scripts
- **Check `demo.py`** — copy snippets for your projects
- **Keep `.env` private** — never share your API key
- **Save your vector store** — no re-processing needed
- **Modify `QUESTIONS`** — ask about YOUR document

---

## 🆘 If Something's Wrong

1. Check **Errors Section** in `README.md`
2. Check **Common Issues** in `QUICK_START.md`
3. Verify dependencies: `pip list | grep langchain`
4. Check `.env` has correct API key (paid version)
5. Check Ollama is running (free version)
6. Check `.docx` file exists and is valid

---

## 📞 Next Steps

1. **New to RAG?** → Read `README.md`
2. **Want to start now?** → Follow `QUICK_START.md`
3. **Need ideas?** → Check `demo.py`
4. **Want to customize?** → Edit `config.py`
5. **Having issues?** → See troubleshooting sections

---

**You're all set! Pick `rag_word_free.py` or `rag_word.py` and run it! 🚀**
