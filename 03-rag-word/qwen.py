import os
from dotenv import load_dotenv
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
 
# Load the Word document
DOCX_FILE = "./Stav_Kesler_CV_Updated.docx"

loader = Docx2txtLoader(DOCX_FILE)
docs = loader.load()
print(f"✓ Loaded {len(docs)} document(s) from {DOCX_FILE}")

# Split the document into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=60,
)
chunks = splitter.split_documents(docs)
print(f"✓ Split into {len(chunks)} chunks")

# Option A: Using OpenAI (requires OPENAI_API_KEY environment variable)
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set. Add it to .env or your environment.")
embeddings = OpenAIEmbeddings()


vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_docx_db"
)
print("✓ Vector store created and persisted to ./chroma_docx_db")

# Setup the LLM and QA chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

questions = [
    "What is the main topic of this document?",
    "Who are the key people or characters mentioned?",
    "What are the most important concepts discussed?",
    "What conclusions or recommendations does the document provide?",
    "What examples or evidence support the main arguments?"
]

print("\n" + "="*70)
print("🤖 RAG QUESTION ANSWERING")
print("="*70)

for i, question in enumerate(questions, 1):
    result = qa_chain.invoke({"query": question})
    
    print(f"\n{'─'*70}")
    print(f"❓ Question {i}: {question}")
    print(f"{'─'*70}")
    print(f"🤖 Answer: {result['result']}")
    print(f"\n📚 Retrieved context ({len(result['source_documents'])} chunks):")
    
    for j, src in enumerate(result["source_documents"], 1):
        content_preview = src.page_content[:200].replace('\n', ' ')
        print(f"  [{j}] ...{content_preview}...")

print("\n" + "="*70)
print("✅ Complete!")
print("="*70)