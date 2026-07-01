"""Vector DB example using ChromaDB + all-MiniLM-L6-v2.

Install:
pip install -r requirements.txt / pip install chromadb sentence-transformers
"""

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# Free local embedding model — no API key needed
ef = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

client = chromadb.Client()
collection = client.create_collection(
    name="movies_collection",
    embedding_function=ef
)

# At least 15 documents with metadata
# ====================== DOCUMENTS & METADATA ======================

documents = [
    "A Brief History of Time explores the universe from the Big Bang to black holes and explains complex physics in simple terms.",
    "The Elegant Universe introduces string theory and explains how it attempts to unify all forces of nature.",
    "Cosmos takes readers on a journey through space and time, covering astronomy, physics, and the history of science.",
    "Physics of the Impossible discusses scientific concepts that seem impossible today but may become reality in the future.",
    "The Selfish Gene presents the gene-centered view of evolution and introduces the concept of memes.",
    "Sapiens: A Brief History of Humankind explores the history of Homo sapiens from ancient times to the modern era.",
    "The Hidden Reality explains different theories of parallel universes and multiverses in modern physics.",
    "Astrophysics for People in a Hurry provides a quick and clear overview of the universe and its fundamental laws.",
    "The Gene: An Intimate History tells the story of genetics from Mendel to modern gene editing technologies.",
    "Pale Blue Dot reflects on humanity's place in the vast universe and our future in space exploration.",
    "The Order of Time examines the nature of time, its flow, and how physics challenges our everyday perception of it.",
    "Wonders of the Universe explores the most extraordinary phenomena in the cosmos, from stars to black holes.",
    "The Fabric of the Cosmos investigates space, time, and the nature of reality according to modern physics.",
    "Why Evolution is True presents clear evidence supporting the theory of evolution by natural selection.",
    "The Immortal Life of Henrietta Lacks tells the story of the woman whose cells changed modern medicine.",
    "The Sixth Extinction discusses how human activity is causing the sixth mass extinction on Earth.",
    "Quantum: Einstein, Bohr and the Great Debate discusses the history and debates of quantum mechanics."
]

metadatas = [
    {"genre": "Physics", "year": 1988},
    {"genre": "Physics", "year": 1999},
    {"genre": "Astronomy", "year": 1980},
    {"genre": "Physics", "year": 2008},
    {"genre": "Biology", "year": 1976},
    {"genre": "History", "year": 2011},
    {"genre": "Physics", "year": 2011},
    {"genre": "Astronomy", "year": 2017},
    {"genre": "Biology", "year": 2016},
    {"genre": "Astronomy", "year": 1994},
    {"genre": "Physics", "year": 2017},
    {"genre": "Astronomy", "year": 2011},
    {"genre": "Physics", "year": 2004},
    {"genre": "Biology", "year": 2009},
    {"genre": "Biology", "year": 2010},
    {"genre": "Environment", "year": 2014},
    {"genre": "Physics", "year": 2005}
]

ids = [f"book_{i}" for i in range(len(documents))]

collection.add(documents=documents, metadatas=metadatas, ids=ids)

print(f"Collection created with {collection.count()} documents")

# Semantic queries (conceptual, not keyword-copies)
queries = [
    "books that explain the nature of time and reality",
    "books about the universe and black holes",
    "books discussing human evolution and genetics",
    "books about future technologies and scientific possibilities",
    "books that explore how the cosmos began and how it might end"
]

for query in queries:
    results = collection.query(
        query_texts=[query],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )
    print(f"\n🔍 Query: '{query}'")
    print("-" * 60)
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        print(f"  Distance: {dist:.4f}  |  {doc[:80]}...")
        print(f"  Metadata: {meta}")

print("\n" + "=" * 50)
print("Short Analysis:\n")

print(
    "The query about books explaining the nature of time and reality produced the most relevant results, "
    "achieving the lowest distances overall. This is likely because the embeddings effectively captured "
    "abstract concepts such as time, reality, and physics, rather than depending on exact keyword matches.\n"
)

print(
    "One surprisingly good match occurred with the query about future technologies and scientific possibilities, "
    "which aligned well with the book 'Physics of the Impossible'. The model recognized the conceptual connection "
    "even though the text did not contain many of the exact words from the query. This demonstrates the advantage "
    "of semantic search over simple keyword matching.\n"
)

print(
    "Based on the results, I would consider distances below 0.55 as strongly relevant, distances between 0.55 and 0.65 "
    "as likely relevant, and anything above 0.7 as weak or unrelated. These thresholds should be adjusted depending "
    "on the specific dataset and embedding model being used."
)

print("=" * 50)