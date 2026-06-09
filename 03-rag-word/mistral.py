"""Chat with DOCX files using RAG."""

import os
from dotenv import load_dotenv
import gradio as gr

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
 
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def load_and_index(docx_path: str):
    """Load DOCX, chunk it, embed it, and return a retriever."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set. Add it to the project's .env file.")

    loader = Docx2txtLoader(docx_path)
    docs = loader.load()
    print(f"Loaded {len(docs)} document(s)")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory="./chroma_docx_db"
    )
    print("Vector store created and persisted.")

    return vectorstore.as_retriever(search_kwargs={"k": 3})

def build_chain(retriever):
    """Build a RetrievalQA chain."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )

# Global state
chain = None

def upload_docx(docx_file):
    """Index uploaded DOCX file."""
    global chain
    if docx_file is None:
        return "No file uploaded.", []

    print(f"Indexing: {docx_file.name}")
    retriever = load_and_index(docx_file.name)
    chain = build_chain(retriever)
    return "✅ DOCX indexed! Ask me anything.", []

def ask_question(question, history):
    """Answer question about DOCX."""
    global chain
    history = history or []

    if chain is None:
        return history + [
            {"role": "user", "content": question},
            {"role": "assistant", "content": "Please upload a DOCX first."}
        ]

    result = chain.invoke({"query": question})  # Correct key for RetrievalQA
    answer = result["result"]                   # Correct key for RetrievalQA

    # Append retrieved context to the answer for display in Gradio
    if result.get("source_documents"):
        answer += "\n\n📚 Retrieved context:"
        for i, src in enumerate(result["source_documents"], 1):
            answer += f"\n  [{i}] ...{src.page_content[:200]}..."

    return history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer}
    ]

# Build the UI
with gr.Blocks(title="Chat with DOCX") as demo:
    gr.Markdown("## 📄 Chat with DOCX\nUpload a DOCX file and ask questions about it.")

    with gr.Row():
        docx_input = gr.File(label="Upload DOCX", file_types=[".docx"])
        status = gr.Textbox(label="Status", interactive=False)

    chatbot = gr.Chatbot(label="Conversation", height=400)
    question_input = gr.Textbox(
        placeholder="Ask a question about your DOCX...",
        label="Question"
    )

    docx_input.change(
        fn=upload_docx,
        inputs=docx_input,
        outputs=[status, chatbot]
    )

    question_input.submit(
        fn=ask_question,
        inputs=[question_input, chatbot],
        outputs=chatbot
    )

    gr.Examples(
        examples=[
            ["What is the main topic of this document?"],
            ["Summarize the main points."],
            ["Who are the key people or characters mentioned?"],
            ["What conclusions or recommendations are given?"],
            ["What facts or examples support the main point?"],
        ],
        inputs=question_input,
    )

if __name__ == "__main__":
    demo.launch()