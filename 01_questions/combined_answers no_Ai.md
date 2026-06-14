# Finals — Combined Questions & Answers (1–12)

## Q1 — What is tokenization? __________

Question - What is tokenization? Give an example — show how the sentence "I'm learning NLP in 2025!" would be tokenized.

Answer
Tokens
["I", "'m", "learning", "NLP", "in", "2025", "!"]

In this process a system splits raw text into units that are discrete - those units are words, subwords or punctuation. By using those parts, systems for natural language processing are able to process and analyze language - this task is the first step in the sequence because models are dependent on the discrete units rather than strings of raw characters.
---

## Q2 — Stemming vs Lemmatization __________

Question: What is the difference between stemming and lemmatization? Apply both to the words "running" and "better" and explain which preserves more linguistic meaning.

Answer:
Stemming: 
Running -> run
Better -> better (Note: Simple stemmers will probably not convert an irregular form into a corresponding regular form)

Lemmatization: 
Running (verb) -> run
Better (comparative, adjective) -> good

To clarify: Stemming punishes parts of the word too regular for his own good, and will therefore produce non-words and/or leave irregular forms unchanged. Lemmatization, however, can take into account both the vocabulary and part of speech associated with that term to return a properly defined form, so it provides more semantic significance than stemming.
---

## Q3 — TF-IDF __________

Question: What does TF-IDF stand for? Explain in plain language why the word "the" scores almost zero in TF-IDF, while the word "photosynthesis" would score high.

Answer
TF- IDF = Term frequence × Inverse Document frequence.
- Term frequence( TF) how frequently a word appears in a document.
- Inverse Document frequence( IDF) downweights words that appear in numerous documents.

A word gets a high TF- IDF score when it appears constantly in one document but infrequently across the whole collection." The" appears in nearly every document so its IDF is near zero;" photosynthesis" is rare and therefore scores high.
---

## Q4 — Sentence Embedding vs One-hot __________

Question: What is a sentence embedding? How is it different from one-hot encoding? Give one advantage embeddings have.

Answer:
A sentence embedding is a fixed-length vector of numbers that represents the overall meaning of a sentence in a continuous space. One-hot encoding, on the other hand, is just a sparse list that says which words are present — it has no idea about meaning or relationships between words.
|||
question: What is a sentence embedding? How is it different from one-hot encoding? Give one advantage embeddings have.

Sentence embedding is a fixed-sized numerical vector which captures the essence of the meaning of the sentence. One-hot encoding on the other hand is just a sparse vector that tells which words are present. It doesn’t even know anything about meaning or relationship between the words.
---

## Q5 — Cosine Similarity

Question: Explain cosine similarity in plain language.

Answer:
Cosine similarity measures how aligned two vectors are by the angle between them. If two document vectors point in almost the same direction, they share similar semantic content or topics. Cosine ignores magnitude differences, focusing on orientation, which makes it robust for semantic comparisons.
|||

---

## Q6 — SQL LIKE vs Vector Index

Question: Why can't `WHERE description LIKE '%pizza%'` find semantically similar documents? What does a vector index solve?

Answer:
`LIKE` performs literal substring matching and cannot detect semantic similarity when different words express the same concept. A vector index stores dense embeddings and supports nearest-neighbor search, enabling retrieval of semantically similar documents even when they share few or no exact words.

---

## Q7 — What problem does RAG solve?

Question: What problem does RAG solve that a plain LLM cannot? Give a concrete example.

Answer:
RAG (Retrieval-Augmented Generation) augments an LLM with a retriever that fetches relevant documents and conditions the model on those documents. This addresses knowledge cutoffs, private data access, and hallucinations. Example: a support agent retrieving the customer's account record and policy doc to craft a precise, verifiable answer.

---

## Q8 — 3 main steps of a RAG pipeline

Question: Describe the 3 main steps of a RAG pipeline (ingestion vs query time).

Answer:
Ingestion: chunk → embed → store.
Query time: embed query → retrieve → generate.

Chunking splits documents into manageable passages; embedding converts text to vectors; storing saves vectors for fast search. At query time you embed the query, retrieve relevant passages, and generate the final answer conditioned on those passages.

---

## Q9 — Docker image vs container

Question: Difference between Docker image and Docker container; use an analogy.

Answer:
A Docker image is a read-only snapshot describing how to build a runnable environment (recipe/blueprint). A Docker container is a running instance created from that image (the finished cake or building). The image is the template; the container is the live process with runtime state.

---

## Q10 — LLM chatbot vs AI agent with tools

Question: What is the difference between a simple LLM chatbot and an AI agent with tools? Give an example of a tool.

Answer:
A simple LLM chatbot generates text only from its model weights and prompt. An AI agent with tools can call external systems (search, databases, code runners) to access live data and perform actions. Example: a web search tool lets the agent retrieve up-to-date info and verify facts in real time.

---

## Q11 — What is MCP (Model Context Protocol)?

Question: What is MCP and what problem does it solve? Name two examples of capabilities it might expose.

Answer:
MCP standardizes how external context providers expose structured data and tools to assistants, solving ad-hoc brittle integrations. Examples of capabilities: filesystem access (list/read files) and a GitHub API proxy (query issues/pull requests).

---

## Q12 — What are Agent Skills?

Question: What are Agent Skills and how are they different from plain prompts? Show minimal `.md` metadata example.

Answer:
Agent Skills are discoverable metadata + implementation packages that expose domain-specific capabilities as structured files (metadata and content). Unlike plain prompts, Skills are discoverable, versioned, and reusable. Minimal metadata example:

```
<skill>
  <name>mongodb-query-optimizer</name>
  <description>Help optimize MongoDB queries and suggest indexes.</description>
  <file>skills/mongodb-query-optimizer/SKILL.md</file>
</skill>
```

---
