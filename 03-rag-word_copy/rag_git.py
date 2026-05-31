"""Chat with DOCX files using RAG."""
import os
from dotenv import load_dotenv
import gradio as gr

from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory

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
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory="./chroma_docx_db")
    
    return vectorstore.as_retriever(search_kwargs={"k": 4})
 

def build_chain(retriever):
    """Build a conversational RAG chain."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        verbose=False,
    )


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
        return history + [{"role": "user", "content": question}, {"role": "assistant", "content": "Please upload a DOCX first."}]
    
    result = chain.invoke({"question": question})
    answer = result["answer"]
    sources = result.get("source_documents", [])

    if sources:
        passages = []
        for i, doc in enumerate(sources[:3], 1):
            snippet = doc.page_content[:200].strip()
            passages.append(f"Passage {i}:\n{snippet}")
        answer += "\n\nRetrieved context:\n" + "\n\n".join(passages)

    return history + [{"role": "user", "content": question}, {"role": "assistant", "content": answer}]


with gr.Blocks(title="Chat with DOCX") as demo:
    gr.Markdown("## 📄 Chat with DOCX\nUpload a DOCX file and ask questions about it.")

    with gr.Row():
        docx_input = gr.File(label="Upload DOCX", file_types=[".docx"])

    status = gr.Textbox(label="Status", interactive=False)
    chatbot = gr.Chatbot(label="Conversation", height=400)
    question_input = gr.Textbox(placeholder="Ask a question about your DOCX...", label="Question")

    docx_input.change(fn=upload_docx, inputs=docx_input, outputs=[status, chatbot])

    question_input.submit(fn=ask_question, inputs=[question_input, chatbot], outputs=chatbot)

    gr.Examples(
        examples=[
            ["what is RAG?"],
            ["What specific recommendations or actions does the document propose?"],
            ["What risks, limitations, or open questions does the document identify?"],
            ["Are there any contradictions or unsupported claims in the text?"],
            ["Who are the key stakeholders or entities mentioned and what roles do they play?"],
        ],
        inputs=question_input,
    )


if __name__ == "__main__":
    demo.launch()
