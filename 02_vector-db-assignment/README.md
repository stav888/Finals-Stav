# Task 2 — Vector Database

Semantic search with **ChromaDB** and a free local embedding model.  
Create a collection of science books, run conceptual queries, display distances, and analyze the results.

Built with **ChromaDB** and **Sentence Transformers** (`all-MiniLM-L6-v2`).

Based on [Assignment 2 — Vector Database](https://pythonai200425.github.io/finals/02-vector-db.html).

---

## Features

- ChromaDB collection with **15 documents** + metadata (`genre`, `year`)
- Free local embeddings: `all-MiniLM-L6-v2` (no API key)
- **5 semantic queries** (concepts, not keyword copies)
- L2 **distances** printed for every result
- Short written **analysis** of relevance, surprising matches, and distance thresholds

---

## Project Structure

```text
02_vector-db-assignment/
├── vector_db_assignment.py   # Collection, queries, analysis
├── requirements.txt
├── image1.png                # Output screenshot
├── image2.png                # Output screenshot
└── README.md
```

---

## Requirements

- Python 3.10+

No API key needed — embeddings run fully local.

---

## Setup

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

`requirements.txt`:

```text
chromadb
sentence-transformers
```

---

## Run

```powershell
python vector_db_assignment.py
```

The script will:

1. Create collection `Science_collection`
2. Add **15** popular-science book documents with metadata
3. Run **5** semantic queries (`n_results=3`)
4. Print document snippet, metadata, and **distance** for each hit
5. Print a short analysis (most relevant query, surprising match, distance thresholds)

---

## How It Works

1. **Embed** each document with `SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")`
2. **Store** documents + metadata in a ChromaDB collection
3. **Query** with natural-language concepts (not exact keywords)
4. Chroma returns nearest neighbors by **L2 distance** (lower = more similar)
5. **Analyze** which queries worked best and why

### Example queries

```text
books that explain the nature of time and reality
books about the universe and black holes
books discussing human evolution and genetics
books about future technologies and scientific possibilities
books that explore how the cosmos began and how it might end
```

---

## Grading Criteria (20 pts)

| Criterion | Points |
|-----------|--------|
| Collection created with ≥ 15 documents + metadata | 6 |
| 5 semantic queries run (concepts, not keyword copies) | 6 |
| Distances displayed in output | 4 |
| Short written analysis of results | 4 |

---

## Screenshots

![Output 1](https://raw.githubusercontent.com/stav888/Finals-Stav/main/02_vector-db-assignment/image1.png)

![Output 2](https://raw.githubusercontent.com/stav888/Finals-Stav/main/02_vector-db-assignment/image2.png)

---

## Notes

- No `.env` or OpenAI key required
- Model downloads once on first run (`all-MiniLM-L6-v2`)
- Distances are ChromaDB default L2; lower is better
