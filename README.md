# Finals-Stav

Finals-Stav contains the final assignments for the course. The repository holds the written theory answers, code for the practical assignments (vector DB, RAG, and a restaurant chatbot wired with n8n), and helper tools to export and regenerate deliverables.

Table of contents
- `01_questions/` — Assignment 1 (theory): canonical answers plus `assignment_1_answers.pdf` and `assignment_1_answers.docx`.
- `02-vector-db-assignment/` — Assignment 2: ChromaDB/embeddings examples and scripts.
- `03-rag-word_copy/` — Assignment 3: RAG pipeline using a Word document and ChromaDB/chat interface.
- `04-n8n_docker/` — Assignment 4: Restaurant chatbot, SQLite DB, and n8n workflow for notifications.
- `tools/` — utility scripts used to convert markdown to DOCX/PDF and other helpers.

Assignments (summary)

- Assignment 1 — Theory (12 questions, 24 points)
	- Topics: tokenization, TF-IDF, embeddings, cosine similarity, vector indexes, RAG, Docker, AI agents, MCP, and Agent Skills.
	- Deliverable: a single PDF or DOCX containing answers to all 12 questions.

- Assignment 2 — Build a Vector Database (20 points)
	- Create a ChromaDB collection with at least 15 documents, run semantic queries, and include a script (`.py` or `.ipynb`) plus a screenshot showing query results and similarity scores.

- Assignment 3 — RAG with a Word Document (20 points)
	- Convert a `.docx` into chunks, embed them into a vector store (ChromaDB), and implement a chat interface that retrieves and answers questions using the document context. Deliver code and a screenshot showing retrieval → generated answer.

- Assignment 4 — Restaurant AI Agent + n8n Notifications (40 points)
	- Extend the restaurant chatbot to handle reservations and cancellations stored in SQLite, and wire an n8n workflow that sends notifications (email, console, or other). Deliver Python files, n8n workflow screenshot, and demo screenshot.

Submission checklist

1. Theory answers document: one PDF or DOCX containing all 12 answers.
2. Vector DB: Python file or notebook plus a screenshot showing query results with distances.
3. RAG: Python file or notebook plus a screenshot demonstrating retrieval and answer flow.
4. Restaurant chatbot: Python files, n8n workflow screenshot, and a screenshot of notification output.

Send all files to: pythonai200425+finals@gmail.com with subject `Finals – [Your Full Name]`.

Tips

- Read each assignment's demo page before starting — demos include working examples and expected outputs.
- Assignment 4 includes a free option that does not require external accounts.
- For the RAG assignment any `.docx` works; pick a document that interests you.

Regenerating deliverables

To regenerate the PDF from the canonical markdown answers, activate the venv and run:

```powershell
.venv\Scripts\Activate.ps1
python tools\md_to_pdf_reportlab.py
```

To regenerate the DOCX:

```powershell
.venv\Scripts\Activate.ps1
python tools\convert_md_to_docx.py
```

Notes about this repository

- The canonical answers are in `01_questions/combined_answers.md`.
- `04-n8n_docker/README.md` was updated to avoid referencing `.env.example` and Telegram environment variables.
- If you plan to version-control these artifacts, initialize a Git repository at the workspace root (`git init`) and commit the outputs.

Further edits

If you want a polished README with a title page, badges, or a contributor guide, say which additions you want and I will update it.