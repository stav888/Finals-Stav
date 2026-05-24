# ════════════════════════════════════════════════════════════════════════════════
# 📄 RAG — Chat with a Word Document (FREE VERSION - No API Key Needed)
# ════════════════════════════════════════════════════════════════════════════════
#
# This script uses FREE, local alternatives:
# - SentenceTransformerEmbeddings (no setup needed, just pip install)
# - Ollama for local LLM (requires running locally)
#
# SETUP:
# 1. pip install langchain langchain-community chromadb docx2txt sentence-transformers
# 2. Install Ollama: https://ollama.ai/
# 3. Run: ollama pull llama3.2
# 4. Run this script!
#
# ════════════════════════════════════════════════════════════════════════════════

import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# ════════════════════════════════════════════════════════════════════════════════
# STEP 1: Load the Word document
# ════════════════════════════════════════════════════════════════════════════════
print("🔄 STEP 1: Loading Word document...\n")

DOCX_PATH = "your_document.docx"  # ← Change this to your .docx file path

if not os.path.exists(DOCX_PATH):
    print(f"❌ Error: '{DOCX_PATH}' not found.")
    print("   Please place your .docx file in the same directory as this script.")
    exit(1)

loader = Docx2txtLoader(DOCX_PATH)
docs = loader.load()
print(f"✅ Loaded {len(docs)} document(s)")
print(f"   Document length: {len(docs[0].page_content)} characters\n")

# ════════════════════════════════════════════════════════════════════════════════
# STEP 2: Split into chunks
# ════════════════════════════════════════════════════════════════════════════════
print("✂️  STEP 2: Splitting text into chunks...\n")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # characters per chunk
    chunk_overlap=60,    # overlap to preserve context at boundaries
)
chunks = splitter.split_documents(docs)
print(f"✅ Split into {len(chunks)} chunks")
print(f"   Sample chunk size: {len(chunks[0].page_content)} characters\n")

# ════════════════════════════════════════════════════════════════════════════════
# STEP 3: Embed and store in ChromaDB (using FREE local embeddings)
# ════════════════════════════════════════════════════════════════════════════════
print("🔢 STEP 3: Creating embeddings and storing in ChromaDB...\n")
print("   Using: SentenceTransformerEmbeddings (no setup required)\n")

# Free local embeddings - no API key or setup needed!
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_docx_db"
)
print("✅ Vector store created and persisted at ./chroma_docx_db\n")

# ════════════════════════════════════════════════════════════════════════════════
# STEP 4 & 5: Retrieve and Answer Questions (Optional: requires Ollama)
# ════════════════════════════════════════════════════════════════════════════════
print("🤖 STEP 4-5: Building QA chain...\n")

# Try to use Ollama for LLM, but allow graceful fallback
try:
    print("   Connecting to Ollama (localhost:11434)...")
    llm = Ollama(model="llama3.2")
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    print("✅ QA chain ready (using Ollama llama3.2).\n")
    use_llm = True
    
except Exception as e:
    print(f"⚠️  Could not connect to Ollama: {e}")
    print("   Install Ollama: https://ollama.ai/")
    print("   Then run: ollama pull llama3.2")
    print("   Then start Ollama before running this script.\n")
    print("   Continuing with document retrieval only (no LLM answers).\n")
    use_llm = False

# ════════════════════════════════════════════════════════════════════════════════
# Ask your 5 questions about the document
# ════════════════════════════════════════════════════════════════════════════════
questions = [
    "What is the main topic of this document?",
    "Who are the key people or entities mentioned?",
    "What are the main conclusions or findings?",
    "What problems or challenges are discussed?",
    "What solutions or recommendations are provided?",
    # ← Modify these questions to be relevant to YOUR document
]

print("=" * 80)
print("📋 QUESTION & ANSWER RESULTS")
print("=" * 80)

for i, question in enumerate(questions, 1):
    print(f"\n{'─' * 80}")
    print(f"Question {i}: {question}")
    print(f"{'─' * 80}")
    
    if use_llm:
        result = qa_chain.invoke({"query": question})
        print(f"\n🤖 Answer:\n{result['result']}")
        source_docs = result['source_documents']
    else:
        # Fallback: just retrieve relevant chunks
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        source_docs = retriever.invoke(question)
        print("\n📌 Retrieved Relevant Chunks (no LLM answer):")
    
    # Print retrieved context chunks
    print(f"\n📚 Retrieved Context Chunks ({len(source_docs)} chunks):")
    for j, src in enumerate(source_docs, 1):
        print(f"\n  [{j}] {src.page_content[:200]}...")
        if len(src.page_content) > 200:
            print(f"      (continued...)")

print(f"\n{'=' * 80}")
print("✅ All questions processed successfully!")
print(f"{'=' * 80}\n")
