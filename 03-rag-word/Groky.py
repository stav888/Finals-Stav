"""Chat with DOCX files using RAG — Assignment 3 (Final Version)"""
import os
from dotenv import load_dotenv
import gradio as gr

from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# ✅ Fixed import for current LangChain versions
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


def load_and_index(docx_path: str):
    """Load DOCX, chunk it, embed it, and return retriever."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set. Add it to the project's .env file.")

    print(f"📄 Loading: {docx_path}")
    loader = Docx2txtLoader(docx_path)
    docs = loader.load()
    print(f"Loaded {len(docs)} document(s)")

    # Exact chunking as required by the assignment
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_docx_db"
    )
    print("✅ Vector store created and persisted.")
    return vectorstore.as_retriever(search_kwargs={"k": 3})


def build_qa_chain(retriever):
    """Build RetrievalQA chain (compatible with current LangChain)."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    prompt = ChatPromptTemplate.from_template(
        "Answer the question based on the following context:\n\n{context}\n\nQuestion: {question}"
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )
    return qa_chain


# ====================== AUTO EVALUATION (for Assignment Screenshot) ======================
def run_auto_evaluation(qa_chain):
    """Run 5 questions and print LLM answer + full retrieved context."""
    questions = [
        "What is the main topic of this document?",
        "Who are the key people or characters mentioned?",
        "What conclusions or recommendations are given?",
        "What facts or examples support the main point?",
        "Summarize the main points.",
    ]
    
    print("\n" + "=" * 100)
    print("AUTO EVALUATION — 5 Questions with Retrieved Context (Assignment 3)")
    print("=" * 100)
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'=' * 100}")
        print(f"Question {i}: {question}")
        print('=' * 100)
        
        result = qa_chain.invoke({"query": question})
        
        print(f"\n🤖 Answer:\n{result['result']}\n")
        print("📚 Retrieved Context (top 3 chunks):")
        
        if result.get("source_documents"):
            for j, src in enumerate(result["source_documents"], 1):
                print(f"\n[{j}] {src.page_content}\n")  # Full content
        else:
            print("No context retrieved.")
        
        print("-" * 100)


# Global state
qa_chain = None


def upload_docx(docx_file):
    """Index uploaded DOCX file and run auto evaluation."""
    global qa_chain
    if docx_file is None:
        return "No file uploaded.", []
    
    try:
        print(f"Indexing: {docx_file.name}")
        retriever = load_and_index(docx_file.name)
        qa_chain = build_qa_chain(retriever)
        
        run_auto_evaluation(qa_chain)  # For assignment screenshot
        
        return "✅ DOCX indexed successfully! You can now ask questions below.", []
    except Exception as e:
        return f"❌ Error: {str(e)}", []


def ask_question(question, history):
    """Answer a question about the uploaded DOCX."""
    global qa_chain
    history = history or []
    
    if qa_chain is None:
        return history + [
            {"role": "user", "content": question},
            {"role": "assistant", "content": "Please upload a DOCX file first."}
        ]
    
    result = qa_chain.invoke({"query": question})
    answer = result["result"]
    
    # Append retrieved context to the answer
    if result.get("source_documents"):
        answer += "\n\n📚 **Retrieved Context:**"
        for i, src in enumerate(result["source_documents"], 1):
            answer += f"\n\n[{i}] {src.page_content[:400]}..."
    
    return history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer}
    ]


# ====================== GRADIO UI ======================
with gr.Blocks(title="Chat with DOCX - Assignment 3") as demo:
    gr.Markdown("## 📄 Chat with DOCX using RAG\nUpload a DOCX file and ask questions about it.")
    
    with gr.Row():
        docx_input = gr.File(label="Upload DOCX", file_types=[".docx"])
        status = gr.Textbox(label="Status", interactive=False)
    
    chatbot = gr.Chatbot(label="Conversation", height=450)
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
    demo.launch(show_error=True)    # Try to import RetrievalQA normally; if missing, provide a tiny fallback adapter.
    try:
        from langchain.chains import RetrievalQA
        from langchain.prompts import ChatPromptTemplate
    except Exception:
        # Minimal compatibility: adapt calls to RetrievalQA.from_chain_type(...)
        class RetrievalQA:
            @staticmethod
            def from_chain_type(llm, retriever, return_source_documents=True, chain_type_kwargs=None):
                # Accept either a ChatPromptTemplate-like obj or a plain template string
                prompt_obj = (chain_type_kwargs or {}).get("prompt")
                if hasattr(prompt_obj, "from_template") or hasattr(prompt_obj, "template"):
                    # handle ChatPromptTemplate-like objects if present
                    try:
                        template = prompt_obj.template
                    except Exception:
                        template = str(prompt_obj)
                else:
                    template = str(prompt_obj) if prompt_obj is not None else "{context}\n\nQuestion: {question}"
    
                # lazy import/define a tiny chain that calls retriever.invoke() + llm.invoke()
                class _CompatChain:
                    def __init__(self, retriever, llm, template):
                        self.retriever = retriever
                        self.llm = llm
                        self.template = template
    
                    def invoke(self, inputs: dict):
                        q = inputs.get("query") or inputs.get("question") or inputs.get("q")
                        try:
                            docs = self.retriever.invoke(q)
                        except Exception:
                            try:
                                docs = self.retriever.get_relevant_documents(q)
                            except Exception:
                                docs = []
                        context = "\n\n".join([d.page_content for d in docs]) if docs else ""
                        prompt = self.template.format(context=context, question=q)
                        messages = [{"role":"system","content":"You are a helpful assistant."},
                                    {"role":"user","content":prompt}]
                        try:
                            resp = self.llm.invoke(messages)
                        except Exception:
                            try:
                                resp = self.llm(messages)
                            except Exception as e:
                                resp = str(e)
                        # normalize response
                        if isinstance(resp, dict) and "content" in resp:
                            answer = resp["content"]
                        elif isinstance(resp, (list, tuple)) and resp:
                            first = resp[0]
                            answer = first.get("content") if isinstance(first, dict) else str(first)
                        else:
                            answer = str(resp)
                        return {"result": answer, "source_documents": docs}
    
                return _CompatChain(retriever, llm, template)