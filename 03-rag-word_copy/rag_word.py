# ════════════════════════════════════════════════════════════════════════════════
# 📄 RAG — Chat with a Word Document
# ════════════════════════════════════════════════════════════════════════════════
# 
# This script loads a .docx Word file, chunks it, stores embeddings in ChromaDB,
# and answers questions about the document's content using LangChain and OpenAI.
#
# REQUIREMENTS: pip install langchain langchain-community langchain-openai chromadb docx2txt
# ════════════════════════════════════════════════════════════════════════════════


# Load environment variables from .env file

# ════════════════════════════════════════════════════════════════════════════════
# STEP 1: Load the Word document
# ════════════════════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════════════════════
# Chat with a DOCX (Gradio app) — adapted from rag_pdf example
# ════════════════════════════════════════════════════════════════════════════════

import os
from dotenv import load_dotenv
import gradio as gr

from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory


load_dotenv()


def load_and_index(docx_path: str):
    """Load a DOCX, chunk it, embed it, return a retriever."""

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set. Add it to the project's .env file.")

    # Step 1: Load DOCX
    loader = Docx2txtLoader(docx_path)
    docs = loader.load()
    print(f"Loaded {len(docs)} document(s) from {docx_path}")

    # Step 2: Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    # Step 3: Embed and store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory="./chroma_docx_db")

    # Step 4: Return retriever
    return vectorstore.as_retriever(search_kwargs={"k": 4})


def build_chain(retriever):
    """Wrap retriever in a conversational RAG chain."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False,
    )
    return chain


# Global state
chain = None


def upload_docx(docx_file):
    """Called when user uploads a DOCX file."""
    global chain
    if docx_file is None:
        return "No file uploaded.", []

    retriever = load_and_index(docx_file.name)
    chain = build_chain(retriever)
    return "✅ DOCX indexed! Ask me anything about it.", []


def ask_question(question, history):
    """Called when user sends a message."""
    global chain
    history = history or []

    if chain is None:
        return history + [
            {"role": "user", "content": question},
            {"role": "assistant", "content": "Please upload a DOCX first."},
        ]

    result = chain.invoke({"question": question})
    answer = result["answer"]

    # Append source page numbers if available
    sources = result.get("source_documents", [])
    if sources:
        pages = set(doc.metadata.get("page", "?") for doc in sources)
        answer += f"\n\n_Sources: pages {', '.join(str(p) for p in sorted(pages))}_"

    return history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]


# Build the UI
with gr.Blocks(title="Chat with Your DOCX") as demo:
    gr.Markdown("## 📄 Chat with Your DOCX\nUpload a DOCX, then ask questions about it.")

    with gr.Row():
        docx_input = gr.File(label="Upload DOCX", file_types=[".docx"])

    status = gr.Textbox(label="Status", interactive=False)
    chatbot = gr.Chatbot(label="Conversation", height=400)
    question_input = gr.Textbox(placeholder="Ask a question about your DOCX...", label="Question")

    docx_input.change(fn=upload_docx, inputs=docx_input, outputs=[status, chatbot])

    question_input.submit(fn=ask_question, inputs=[question_input, chatbot], outputs=chatbot)

    gr.Examples(
        examples=[
            ["What are the main conclusions or findings, and how strong is the evidence?"],
            ["What specific recommendations or actions does the document propose?"],
            ["What risks, limitations, or open questions does the document identify?"],
            ["Are there any contradictions or unsupported claims in the text?"],
            ["Who are the key stakeholders or entities mentioned and what roles do they play?"],
        ],
        inputs=question_input,
    )


if __name__ == "__main__":
    demo.launch()
