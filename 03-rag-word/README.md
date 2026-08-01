# Task 3 — RAG with Word Document

Chat with a `.docx` file using **Retrieval-Augmented Generation (RAG)**.  
Load a Word document, split it into chunks, embed into **ChromaDB**, and answer questions with an LLM grounded in the retrieved context.

Built with **LangChain**, **ChromaDB**, **OpenAI**, and **Gradio**.

Based on [Assignment 3 — RAG with Word Document](https://pythonai200425.github.io/finals/03-rag-word.html).

---

## Features

- Load `.docx` with `Docx2txtLoader`
- Chunk text with `RecursiveCharacterTextSplitter` (size 500, overlap 60)
- Embeddings stored in **ChromaDB** (`text-embedding-3-small`)
- Retrieval of top-k context chunks (`k=3`)
- Answers generated with `ChatOpenAI` (`gpt-4o-mini`)
- Prints **LLM answer + retrieved context** for each question
- Auto-evaluation with 5 non-trivial questions
- Optional Gradio UI for interactive chat

---

## Project Structure

```text
03-rag-word/
├── RAG.py                      # Main RAG script + Gradio UI
├── ML_Concepts_English.docx    # Source Word document
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── screenshots/                # Demo screenshots
```

> `chroma_docx_db/` and `.env` are created locally and ignored by Git.

---

## Requirements

- Python 3.10+
- OpenAI API key

---

## Setup

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

### 2. Configure environment

```powershell
copy .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=sk-your-openai-key-here
```

**Do not commit `.env`.**

---

## Run

```powershell
python RAG.py
```

The script will:

1. Load `ML_Concepts_English.docx`
2. Split into chunks and print the chunk count
3. Embed and store in `./chroma_docx_db`
4. Run **5 evaluation questions** and print for each:
   - LLM answer
   - Retrieved context chunks (up to 3)
5. Optionally launch the Gradio UI for interactive questions

Gradio (if enabled): [http://127.0.0.1:7860](http://127.0.0.1:7860) or the port shown in the terminal.

---

## How It Works

### Ingestion time

1. **Load** — `Docx2txtLoader` reads the Word document  
2. **Chunk** — `RecursiveCharacterTextSplitter` (chunk_size=500, chunk_overlap=60)  
3. **Embed + Store** — `OpenAIEmbeddings` → ChromaDB (`persist_directory="./chroma_docx_db"`)

### Query time

1. **Embed** the user question  
2. **Retrieve** top-3 relevant chunks  
3. **Generate** answer with the LLM using only the retrieved context  

---

## Example Questions (non-trivial)

```text
What is the main topic of this document?
Summarize the main points.
Who are the key people or concepts mentioned?
What conclusions or recommendations are given?
What facts or examples support the main point?
```

Answers are grounded in the document — not general LLM knowledge.

---

## Grading Criteria (20 pts)

| Criterion | Points |
|-----------|--------|
| `.docx` loaded and split into chunks (print chunk count) | 4 |
| Embeddings stored in ChromaDB | 4 |
| 5 questions answered with LLM | 6 |
| Retrieved context chunks printed alongside answers | 4 |
| Questions are relevant and non-trivial | 2 |

---

## Screenshots

### Terminal — 5 questions + answers + context

![Terminal output 1](https://github.com/user-attachments/assets/1455bd42-3f9d-4a75-be02-6065b1ec2270)

![Terminal output 2](https://github.com/user-attachments/assets/77af1b3c-9636-45b5-bbe7-ef2ff2cb126a)

![Terminal output 3](https://github.com/user-attachments/assets/b7827eb1-1f1a-4538-9180-518c230bc32b)

![Terminal output 4](https://github.com/user-attachments/assets/9819e90c-f35f-4a59-a1d2-cb540b79ed8e)

![Terminal output 5](https://github.com/user-attachments/assets/d4e0c794-30d8-46ae-b57c-cba93fe9ed01)

### Gradio UI

![Gradio chat 1](https://github.com/user-attachments/assets/17921707-7043-4d7c-8029-9404312ddaa7)

![Gradio chat 2](https://github.com/user-attachments/assets/59497e61-8208-4b8e-a271-43f9093871c3)

![Gradio chat 3](https://github.com/user-attachments/assets/7ae7bcc9-ac5b-48f4-94d2-28baeed8d7b8)

![Gradio chat 4](https://github.com/user-attachments/assets/55f09640-74c8-41c4-888a-8c7ac7f60088)

![Gradio chat 5](https://github.com/user-attachments/assets/358cfd3b-bd52-4141-b89d-bcf277ebb269)

---

## Security Notes

- Keep the API key only in `.env`
- `.gitignore` should exclude: `.env`, `chroma_docx_db/`, `__pycache__/`, `.venv/`
- Use `.env.example` as a safe template
```