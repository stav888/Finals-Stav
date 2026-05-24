# ════════════════════════════════════════════════════════════════════════════════
# DEMO - RAG Word Document Examples
# ════════════════════════════════════════════════════════════════════════════════
#
# This file shows different ways to use the RAG pipeline:
# - Basic usage
# - Custom configuration
# - Multiple documents
# - Advanced retrieval
#
# Copy and modify snippets for your own projects!
#

# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Basic RAG Pipeline (Simplest)
# ════════════════════════════════════════════════════════════════════════════════

def example_basic():
    """Minimal example to get started quickly."""
    from langchain_community.document_loaders import Docx2txtLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    
    # Load document
    loader = Docx2txtLoader("my_document.docx")
    docs = loader.load()
    print(f"📄 Loaded: {len(docs)} document(s)")
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)
    chunks = splitter.split_documents(docs)
    print(f"✂️  Chunked: {len(chunks)} chunks")
    
    # Create vector store
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
    print(f"✅ Vector store created!")
    
    return vectorstore


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: With LLM (Free Local Version)
# ════════════════════════════════════════════════════════════════════════════════

def example_with_local_llm():
    """Add local LLM (Ollama) for question answering."""
    from langchain_community.document_loaders import Docx2txtLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    from langchain_community.llms import Ollama
    from langchain.chains import RetrievalQA
    
    # Step 1: Load & chunk
    loader = Docx2txtLoader("my_document.docx")
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)
    chunks = splitter.split_documents(docs)
    
    # Step 2: Create vector store
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
    
    # Step 3: Create QA chain with local LLM
    llm = Ollama(model="llama3.2")
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    # Step 4: Ask a question
    result = qa_chain.invoke({"query": "What is the main topic?"})
    
    print(f"🤖 Answer: {result['result']}")
    print(f"📚 Sources: {len(result['source_documents'])} chunks")
    
    return qa_chain


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: With OpenAI GPT-4o-mini (Paid Version)
# ════════════════════════════════════════════════════════════════════════════════

def example_with_openai():
    """Use OpenAI for better quality answers."""
    from langchain_community.document_loaders import Docx2txtLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain.chains import RetrievalQA
    import os
    
    # Requires OPENAI_API_KEY env var
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Set OPENAI_API_KEY environment variable!")
        return
    
    # Step 1: Load & chunk
    loader = Docx2txtLoader("my_document.docx")
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)
    chunks = splitter.split_documents(docs)
    
    # Step 2: Create vector store with OpenAI embeddings
    embeddings = OpenAIEmbeddings()  # Uses OPENAI_API_KEY
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
    
    # Step 3: Create QA chain with OpenAI LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    # Step 4: Ask a question
    result = qa_chain.invoke({"query": "What is the main topic?"})
    
    print(f"🤖 Answer: {result['result']}")
    print(f"📚 Sources: {len(result['source_documents'])} chunks")
    
    return qa_chain


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Batch Ask Multiple Questions
# ════════════════════════════════════════════════════════════════════════════════

def example_batch_questions(qa_chain, questions):
    """Ask multiple questions and collect results."""
    results = []
    
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] {question}")
        result = qa_chain.invoke({"query": question})
        
        results.append({
            "question": question,
            "answer": result["result"],
            "sources": result["source_documents"]
        })
        
        print(f"✅ Answer received")
    
    return results


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Custom Chunk Size & Retrieval
# ════════════════════════════════════════════════════════════════════════════════

def example_custom_config(chunk_size=1000, chunk_overlap=100, num_retrieve=5):
    """Customize chunking and retrieval parameters."""
    from langchain_community.document_loaders import Docx2txtLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    
    # Load & chunk with custom sizes
    loader = Docx2txtLoader("my_document.docx")
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(docs)
    print(f"⚙️  Custom chunking: {len(chunks)} chunks (size={chunk_size}, overlap={chunk_overlap})")
    
    # Create vector store
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
    
    # Retrieve with custom number of docs
    retriever = vectorstore.as_retriever(search_kwargs={"k": num_retrieve})
    results = retriever.invoke("Your question here")
    
    print(f"🔍 Retrieved: {len(results)} chunks (k={num_retrieve})")
    
    return vectorstore


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Load Existing Vector Store (Reuse)
# ════════════════════════════════════════════════════════════════════════════════

def example_load_existing_vectorstore():
    """Load a previously created vector store (no re-processing!)."""
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    
    # Load from disk
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    print(f"✅ Loaded existing vector store!")
    
    # Use it directly
    results = vectorstore.similarity_search("Your question")
    print(f"🔍 Found {len(results)} similar chunks")
    
    return vectorstore


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 7: Advanced - Metadata Filtering
# ════════════════════════════════════════════════════════════════════════════════

def example_with_metadata():
    """Include metadata with chunks for better filtering."""
    from langchain_community.document_loaders import Docx2txtLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    from datetime import datetime
    
    # Load document
    loader = Docx2txtLoader("my_document.docx")
    docs = loader.load()
    
    # Add metadata to each document
    for doc in docs:
        doc.metadata["source"] = "my_document.docx"
        doc.metadata["loaded_at"] = datetime.now().isoformat()
    
    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)
    chunks = splitter.split_documents(docs)
    
    # Create vector store with metadata
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
    
    print(f"📝 Chunks created with metadata!")
    print(f"   Metadata: {chunks[0].metadata}")
    
    return vectorstore


# ════════════════════════════════════════════════════════════════════════════════
# MAIN - Run Examples
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 80)
    print("RAG DEMO - Example Implementations")
    print("=" * 80)
    
    print("\n1️⃣  EXAMPLE 1: Basic Pipeline")
    print("   → Run: example_basic()")
    
    print("\n2️⃣  EXAMPLE 2: With Local LLM (Free)")
    print("   → Run: example_with_local_llm()")
    
    print("\n3️⃣  EXAMPLE 3: With OpenAI (Paid)")
    print("   → Run: example_with_openai()")
    
    print("\n4️⃣  EXAMPLE 4: Batch Questions")
    print("   → Run: example_batch_questions(qa_chain, questions)")
    
    print("\n5️⃣  EXAMPLE 5: Custom Configuration")
    print("   → Run: example_custom_config(chunk_size=1000)")
    
    print("\n6️⃣  EXAMPLE 6: Load Existing Vector Store")
    print("   → Run: example_load_existing_vectorstore()")
    
    print("\n7️⃣  EXAMPLE 7: With Metadata")
    print("   → Run: example_with_metadata()")
    
    print("\n" + "=" * 80)
    print("Copy these functions and modify them for your use case!")
    print("=" * 80 + "\n")
