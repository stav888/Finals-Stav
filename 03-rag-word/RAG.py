"""Chat with DOCX files using RAG — Assignment 3"""

import os
import shutil
from dotenv import load_dotenv
import gradio as gr
 
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
try:
    from langchain.chains.retrieval_qa.base import RetrievalQA
except ImportError:
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

    persist_dir = os.path.join(os.path.dirname(__file__), "chroma_docx_db")
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
    os.makedirs(persist_dir, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
    )
    print(f"Vector store created and persisted at {persist_dir}.")

    return vectorstore.as_retriever(search_kwargs={"k": 3})


def build_chain(retriever):
    """Build a RetrievalQA chain."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )


# ====================== AUTO EVALUATION ======================
def run_auto_evaluation(chain):
    """Run 5 questions and print answer + full retrieved context."""
    questions = [
"What is the main topic of this document?",
    "What are the six foundational concepts in Machine Learning and AI discussed in the document?",
    "What conclusions or recommendations does the document make regarding learning Machine Learning?",
    "What are the typical applications of RAG (Retrieval-Augmented Generation) mentioned in the document?",
    "According to the document, what are the main differences between learning ML and not learning it, and why does it matter?",
    ]

    print("\n" + "=" * 95)
    print("AUTO EVALUATION — 5 Questions with Retrieved Context (Assignment 3)")
    print("=" * 95)

    for i, question in enumerate(questions, 1):
        result = chain.invoke({"query": question})

        print(f"\n{'=' * 95}")
        print(f"Question {i}: {question}")
        print('=' * 95)

        print(f"\nAnswer:\n{result['result']}\n")

        print("Retrieved Context (top 3 chunks):")
        if result.get("source_documents"):
            for j, src in enumerate(result["source_documents"], 1):
                print(f"\n[{j}] {src.page_content}\n")
        else:
            print("No context retrieved.")

        print("-" * 95)

chain = None

def upload_docx(docx_file):
    """Index uploaded DOCX file and run auto evaluation."""
    global chain
    if docx_file is None:
        return "No file uploaded.", []

    chain = None

    file_path = docx_file.name if hasattr(docx_file, "name") else str(docx_file)

    print(f"Indexing: {file_path}")
    retriever = load_and_index(file_path)
    chain = build_chain(retriever)

    run_auto_evaluation(chain)   # For screenshot

    return "✅ DOCX indexed successfully! You can now ask questions below.", []


def ask_question(question, history):
    """Answer a question about the uploaded DOCX."""
    global chain
    history = history or []

    if chain is None:
        return history + [
            {"role": "user", "content": question},
            {"role": "assistant", "content": "Please upload a DOCX file first."}
        ]

    result = chain.invoke({"query": question})
    answer = result.get("result", "No answer generated.")

    if result.get("source_documents"):
        answer += "\n\n📚 Retrieved Context:"
        for i, src in enumerate(result["source_documents"], 1):
            answer += f"\n\n[{i}] {src.page_content[:450]}..."

    return history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer}
    ]


# ====================== GRADIO UI ======================
with gr.Blocks(title="Chat with DOCX - Assignment 3") as demo:
    gr.Markdown("## 📄 Chat with DOCX using RAG\nUpload a DOCX file and ask questions about it.")

    with gr.Row():
        docx_input = gr.File(label="Upload DOCX", type="filepath")
        status = gr.Textbox(label="Status", interactive=False)

    chatbot = gr.Chatbot(label="Conversation", height=450, type="messages")
    question_input = gr.Textbox(
        placeholder="Ask a question about your DOCX...",
        label="Your Question"
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
    demo.launch(server_name="127.0.0.1", server_port=7860)
