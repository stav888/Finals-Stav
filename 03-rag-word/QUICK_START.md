# ════════════════════════════════════════════════════════════════════════════════
# QUICK START GUIDE
# ════════════════════════════════════════════════════════════════════════════════
#
# Follow these steps to get your RAG Word project running in 5 minutes!
#

## ⚡ 5-Minute Setup

### Step 1: Get Your Word Document Ready
- Find a `.docx` file (3-5 pages recommended for testing)
- Copy it to this directory
- Note the filename (e.g., `my_document.docx`)

### Step 2: Choose Your Path

#### Path A: FREE VERSION (Recommended for Learning) ⭐
```bash
# Install Ollama: https://ollama.ai/

# Download the model (one time, ~5-10 min)
ollama pull llama3.2

# Install dependencies
pip install -r requirements.txt

# Update this line in rag_word_free.py:
DOCX_PATH = "your_document.docx"

# Run it!
python rag_word_free.py
```

#### Path B: PAID VERSION (OpenAI GPT-4o-mini)
```bash
# Get API key: https://platform.openai.com/api-keys

# Setup
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-...

# Install dependencies
pip install -r requirements.txt

# Update this line in rag_word.py:
DOCX_PATH = "your_document.docx"

# Run it!
python rag_word.py
```

### Step 3: Customize Questions (Optional)
Edit the `questions` list in the script to ask about YOUR document:
```python
questions = [
    "What is the main topic?",
    "Who are the key people?",
    # ... add more questions
]
```

### Step 4: Run and Review Output

The script will print:
- ✅ Documents loaded & chunk count
- ✅ Vector store created
- ✅ Questions & LLM answers
- ✅ Retrieved context chunks

---

## 🎯 Expected Output

When you run the script, you should see:

```
🔄 STEP 1: Loading Word document...
✅ Loaded 1 document(s)

✂️  STEP 2: Splitting text into chunks...
✅ Split into 42 chunks

🔢 STEP 3: Creating embeddings and storing in ChromaDB...
✅ Vector store created and persisted at ./chroma_docx_db

🤖 STEP 4-5: Building QA chain...
✅ QA chain ready. Processing questions...

════════════════════════════════════════════════════════════════════════════════
📋 QUESTION & ANSWER RESULTS
════════════════════════════════════════════════════════════════════════════════

[... questions and answers ...]

✅ All questions processed successfully!
```

---

## ❌ Common Issues

### "Document not found"
→ Make sure your `.docx` file is in this directory  
→ Update `DOCX_PATH = "your_file.docx"`

### "OPENAI_API_KEY not set"
→ You need the .env file with your API key (paid version)  
→ OR use the free version instead (rag_word_free.py)

### "Could not connect to Ollama"
→ Install Ollama: https://ollama.ai/  
→ Run: ollama pull llama3.2  
→ Make sure Ollama is running before the script

### "Module not found"
→ Run: pip install -r requirements.txt  
→ Activate your virtual environment if you created one

---

## 🚀 Next Steps

1. ✅ Get the free version working first
2. ✅ Try with different Word documents
3. ✅ Customize questions for your documents
4. ✅ (Optional) Switch to paid version for better answers

---

## 📚 Learn More

- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Ollama Models](https://ollama.ai/library)
- [OpenAI API Docs](https://platform.openai.com/docs/)

---

**Happy coding! 🎉**
