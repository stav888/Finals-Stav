# ════════════════════════════════════════════════════════════════════════════════
# CONFIG.py - RAG Configuration Settings
# ════════════════════════════════════════════════════════════════════════════════
#
# Modify these settings to customize your RAG pipeline behavior
#

# 📄 DOCUMENT SETTINGS
DOCX_PATH = "your_document.docx"  # ← Change this to your Word document path

# 📚 CHUNKING SETTINGS
CHUNK_SIZE = 500           # Characters per chunk (smaller = more chunks)
CHUNK_OVERLAP = 60         # Character overlap between chunks (preserves context)

# 🔍 RETRIEVAL SETTINGS
NUM_RETRIEVE = 3           # Number of chunks to retrieve for each question

# 🤖 LLM SETTINGS
LLM_MODEL = "gpt-4o-mini"  # Model for paid version
LLM_TEMPERATURE = 0        # 0 = factual, 1 = creative

# 🔢 EMBEDDING SETTINGS (FREE VERSION)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast, accurate embeddings

# 🦙 OLLAMA SETTINGS (FREE VERSION)
OLLAMA_MODEL = "llama3.2"  # Model to use with Ollama
OLLAMA_BASE_URL = "http://localhost:11434"  # Ollama server address

# 💾 DATABASE SETTINGS
CHROMA_DB_DIR = "./chroma_docx_db"  # Where to store embeddings

# ❓ QUESTIONS TO ASK
QUESTIONS = [
    "What is the main topic of this document?",
    "Who are the key people or entities mentioned?",
    "What are the main conclusions or findings?",
    "What problems or challenges are discussed?",
    "What solutions or recommendations are provided?",
]

# ════════════════════════════════════════════════════════════════════════════════
# ADVANCED SETTINGS
# ════════════════════════════════════════════════════════════════════════════════

# Retrieve more chunks for complex questions?
ADVANCED_RETRIEVAL = False
ADVANCED_NUM_RETRIEVE = 5

# Show chunk processing details?
VERBOSE = True

# Use streaming responses? (Slower but shows real-time output)
USE_STREAMING = False

# Print retrieved chunks in detail?
SHOW_CHUNK_DETAILS = True
