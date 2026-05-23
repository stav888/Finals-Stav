# Build a Vector Database

This folder reproduces the assignment at https://pythonai200425.github.io/finals/02-vector-db.html

Contents:
- `vector_db_assignment.py`: runnable example that creates a ChromaDB collection with local embeddings (Sentence Transformers), adds ≥15 documents with metadata, runs 5 semantic queries and prints distances.
- `requirements.txt`: Python dependencies.

Usage

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python vector_db_assignment.py
```

Notes

- The script uses the `all-MiniLM-L6-v2` embedding model from `sentence-transformers` (local, no API key).
- Adjust document texts, metadata, and queries as desired.
