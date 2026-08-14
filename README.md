# Finals-Stav Kesler — AI Advanced Final Assignments

Complete submission for **Final Assignments — AI Advanced**  
Course page: [pythonai200425.github.io/finals](https://pythonai200425.github.io/finals/index.html)

**Total: 104 points** across 4 assignments covering theory, vector databases, RAG, and a full restaurant AI agent with n8n automation.

---

## Assignments Overview

| # | Assignment | Folder | Points | Status |
|---|------------|--------|--------|--------|
| 1 | [Theory Questions](https://pythonai200425.github.io/finals/01-theory.html) | `01_questions/` | 24 | Written answers (12 questions) |
| 2 | [Vector Database](https://pythonai200425.github.io/finals/02-vector-db.html) | `02_vector-db-assignment/` | 20 | ChromaDB + semantic queries |
| 3 | [RAG with Word Document](https://pythonai200425.github.io/finals/03-rag-word.html) | `03-rag-word/` | 20 | LangChain RAG + Gradio |
| 4 | [Restaurant AI Agent + n8n](https://pythonai200425.github.io/finals/04-n8n-restaurant.html) | `04-n8n_docker/` | 40 | Chatbot + SQLite + n8n + Telegram |

---

## Repository Structure

```text
Finals-Stav/
├── 01_questions/
│   └── Questions & Answers.pdf
├── 02_vector-db-assignment/
│   ├── README.md
│   ├── image1.png
│   ├── image2.png
│   ├── requirements.txt
│   └── vector_db_assignment.py
├── 03-rag-word/
│   ├── screenshots/
│   ├── .env.example
│   ├── .gitignore
│   ├── ML_Concepts_English.docx
│   ├── RAG.py
│   ├── README.md
│   └── requirements.txt
├── 04-n8n_docker/
│   ├── screenshots/
│   ├── .env.example
│   ├── .gitignore
│   ├── README.md
│   ├── chatbot_db.py
│   ├── docker-compose.yml
│   ├── n8n_workflow.json
│   ├── requirements.txt
│   ├── reservation_chatbot_app.py
│   └── restaurant.db
└── README.md
```

Each task folder has its own `README.md` with setup and run instructions.

---

## Assignment 1 — Theory Questions (24 pts)

12 conceptual questions on:

- Tokenization, stemming / lemmatization, TF-IDF  
- Sentence embeddings, cosine similarity  
- Vector indexes vs SQL  
- RAG pipeline, Docker image vs container  
- AI agents with tools, MCP, Agent Skills  

**Deliverable:** `Questions & Answers.pdf`

📁 Folder: [`01_questions/`](./01_questions/)

---

## Assignment 2 — Vector Database (20 pts)

- ChromaDB collection with **≥ 15 documents** + metadata  
- Free local model: `all-MiniLM-L6-v2`  
- **5 semantic queries** (concepts, not keyword copies)  
- L2 **distances** printed for each result  
- Short written **analysis** of results  

```powershell
cd 02_vector-db-assignment
pip install -r requirements.txt
python vector_db_assignment.py
```

📁 Folder: [`02_vector-db-assignment/`](./02_vector-db-assignment/)

---

## Assignment 3 — RAG with Word Document (20 pts)

- Load `.docx` → chunk → embed → store in ChromaDB  
- Answer **5 non-trivial questions** with LLM  
- Print **answer + retrieved context** for each question  
- Optional Gradio UI for interactive chat  

```powershell
cd 03-rag-word
pip install -r requirements.txt
copy .env.example .env   # add OPENAI_API_KEY
python RAG.py
```

📁 Folder: [`03-rag-word/`](./03-rag-word/)

---

## Assignment 4 — Restaurant AI Agent + n8n (40 pts)

- SQLite `reservations` table + `book_reservation` / `cancel_reservation`  
- Classifier: `reservation` | `cancellation` | `menu` | `hours` | `general`  
- LLM extraction of name / date / time / party size  
- Webhook to n8n on **booking and cancellation**  
- n8n: Webhook → IF (by `event`) → two notification branches  
- Bonus: Telegram real notifications  

```powershell
cd 04-n8n_docker
pip install -r requirements.txt
copy .env.example .env
docker compose up -d
# Import n8n_workflow.json and activate
python reservation_chatbot_app.py
```

📁 Folder: [`04-n8n_docker/`](./04-n8n_docker/)

---

## Grading Summary

| Assignment | Max | Focus |
|------------|-----|--------|
| 1 — Theory | 24 | NLP, vectors, RAG, agents concepts |
| 2 — Vector DB | 20 | Embeddings, semantic search, analysis |
| 3 — RAG Word | 20 | Full RAG pipeline on a document |
| 4 — Agent + n8n | 40 | Agent + DB + webhooks + automation |
| **Total** | **104** | |

---

## Tech Stack

| Area | Tools |
|------|--------|
| NLP / Theory | Concepts only (Assignment 1) |
| Vector search | ChromaDB, Sentence Transformers |
| RAG | LangChain, OpenAI Embeddings, Gradio |
| Agent | LangChain, SQLite, Gradio |
| Automation | n8n (Docker), webhooks, Telegram |

---

## Environment & Security

- Secrets live only in local `.env` files (never committed)
- Each coding task includes `.env.example` and `.gitignore`
- Local DB / Chroma folders are ignored by Git

---

## Quick Links

- Course finals hub: https://pythonai200425.github.io/finals/index.html  
- Task 1: https://pythonai200425.github.io/finals/01-theory.html  
- Task 2: https://pythonai200425.github.io/finals/02-vector-db.html  
- Task 3: https://pythonai200425.github.io/finals/03-rag-word.html  
- Task 4: https://pythonai200425.github.io/finals/04-n8n-restaurant.html  

---

## Author

**Stav Kesler** · AI / ML / Data Science portfolio project

---
## Submission

📧 **Send all files to:**  
pythonai200425+finals@gmail.com
