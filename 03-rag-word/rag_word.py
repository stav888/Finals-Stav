# ════════════════════════════════════════════════════════════════════════════════
# 📄 RAG — Chat with a Word Document
# ════════════════════════════════════════════════════════════════════════════════
# 
# This script loads a .docx Word file, chunks it, stores embeddings in ChromaDB,
# and answers questions about the document's content using LangChain and OpenAI.
#
# REQUIREMENTS: pip install langchain langchain-community langchain-openai chromadb docx2txt
# ════════════════════════════════════════════════════════════════════════════════

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Load environment variables from .env file
load_dotenv()

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
# STEP 3: Embed and store in ChromaDB
# ════════════════════════════════════════════════════════════════════════════════
print("🔢 STEP 3: Creating embeddings and storing in ChromaDB...\n")

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY is not set.")
    print("   Please add it to a .env file in this directory:")
    print("   OPENAI_API_KEY=sk-...\n")
    print("   Or set it as an environment variable.\n")
    print("   For a free version, see the rag_word_free.py script instead.\n")
    exit(1)

embeddings = OpenAIEmbeddings()  # requires OPENAI_API_KEY env var
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_docx_db"
)
print("✅ Vector store created and persisted at ./chroma_docx_db\n")

# ════════════════════════════════════════════════════════════════════════════════
# STEP 4 & 5: Retrieve and Answer Questions
# ════════════════════════════════════════════════════════════════════════════════
print("🤖 STEP 4-5: Building QA chain...\n")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

print("✅ QA chain ready. Processing questions...\n")

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
    
    result = qa_chain.invoke({"query": question})
    
    # Print the LLM answer
    print(f"\n🤖 Answer:\n{result['result']}")
    
    # Print retrieved context chunks
    print(f"\n📚 Retrieved Context Chunks ({len(result['source_documents'])} chunks):")
    for j, src in enumerate(result["source_documents"], 1):
        print(f"\n  [{j}] {src.page_content[:200]}...")
        if len(src.page_content) > 200:
            print(f"      (continued...)")

print(f"\n{'=' * 80}")
print("✅ All questions processed successfully!")
print(f"{'=' * 80}\n")
