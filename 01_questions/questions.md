# Finals - Questions & Answers (1-12)

### Q1 - What is tokenization? Give an example - show how the sentence "I'm learning NLP in 2025!" would be tokenized.

> Answer:

Tokens: ["I", "'m", "learning", "NLP", "in", "2025", "!"]

Tokenization splits text into pieces so models can actually work with it. It's the first step because models need discrete tokens to convert into numbers. In simple terms, you can't feed raw sentences straight into a model; you first break them into tokens.

---

### Q2 - What is the difference between stemming and lemmatization? Apply both to the words "running" and "better" and explain which preserves more linguistic meaning.

> Answer:

Stemming: "running" -> "run", "better" -> "better"

Lemmatization: "running" -> "run", "better" -> "good"

Stemmers chop off endings using quick rules. They're fast, but they can leave odd or non-words. Lemmatizers use a dictionary and grammar tags. They return the real base form, so they keep more meaning. In practice, lemmatization is cleaner but a bit slower.

---

### Q3 - What does TF-IDF stand for? Explain in plain language why the word "the" scores almost zero in TF-IDF, while the word "photosynthesis" would score high.

> Answer:

TF-IDF stands for Term Frequency × Inverse Document Frequency.

TF (term frequency) is just how often a word shows up in a document. IDF (inverse document frequency) lowers the score for words that appear in lots of documents.

Put them together and TF-IDF boosts words that are common in this document but rare across the whole collection. So "the" gets almost zero - it's everywhere. "Photosynthesis" scores high because it's distinctive to some documents. That's why TF-IDF helps pull out the most informative words.

```
TF-IDF means Term Frequency × Inverse Document Frequency.

Term Frequency (TF) means the frequency of occurrence of the word in the document. IDF (Inverse Document Frequency) decreases the value of those words which frequently occur in many documents.

Combined, the TF-IDF gives more weight to those words which occur frequently in the document but are not found in other documents. "The" will get very low score because it occurs everywhere while "photosynthesis" will get high score because of its uniqueness.
```

---

### Q4 - What is a sentence embedding? How is it fundamentally different from one-hot encoding? Give one advantage embeddings have that one-hot vectors don't.

> Answer:

A sentence embedding is a compact numeric vector that captures a sentence's meaning. One-hot vectors, by contrast, only mark which words appear and are mostly zeros.

The neat part is that similar sentences end up close together in vector space. This matters because you can measure semantic similarity directly (for example with cosine similarity) and find related sentences even when they don't share the same words.

```
Sentence embeddings are concise numerical representations that embody the meaning of the sentence. One hot representations, however, merely indicate the presence of certain words and consist mainly of zeroes.

What’s interesting about sentence embeddings is that sentences that have a similar meaning are clustered together in the vector space. The important thing about this feature is that you can compare semantic similarity between sentences without having them share any common words.
```
---

### Q5 - Explain cosine similarity in plain language. If two document vectors point in almost the same direction, what does that tell us about the documents they represent?

> Answer:

Cosine similarity measures the angle between two vectors. If the vectors point in almost the same direction, the angle is small and the similarity is high. If they point in opposite directions, similarity is low. The key difference from Euclidean distance is that cosine ignores length. So a short note and a long article about the same topic can still score highly.

---

### Q6 - Why can't a regular SQL query like `WHERE description LIKE '%pizza%'` find semantically similar documents? What does a vector index solve that SQL can't?

> Answer:

`LIKE` does literal substring matching. You search for "pizza" and you only get entries that literally contain "pizza", nothing else. For example, "Italian food" or "pasta and risotto" won't match, even though they're about the same topic.

A vector index fixes this. You embed documents into vectors, then you search for the chunks closest to the question. That returns semantically related results even when the words differ.

---

### Q7 - What problem does RAG solve that a plain LLM (without RAG) cannot? Give a concrete example of when you would choose RAG over just prompting the LLM directly.

> Answer:

RAG gives an LLM real documents to base its answer on. That reduces hallucinations and lets the model use up-to-date or private information. For example, pick RAG for a support bot. It can fetch a customer's account record and the policy text, then give a specific, verifiable answer instead of guessing.

This matters because LLMs alone only rely on their training data, which may be out of date.

---

### Q8 - Describe the 3 main steps of a RAG pipeline in the correct order. Be clear about what happens at ingestion time (when you load documents) vs query time (when a user asks a question).

> Answer:

Ingestion (single-shot, offline):
1) Chunking – split up the document into chunks.
2) Embedding – convert these chunks into vectors.
3) Indexing/Storage – store these vectors in the vector database.

During query (when user asks):
1) Embed the user’s question.
2) Find the nearest chunks.
3) Create an answer based on these chunks.

---

### Q9 - What is the difference between a Docker image and a Docker container? Use an analogy to explain.

> Answer:

Think of an image as the recipe or blueprint. A container is the cake you bake from that recipe. The recipe is static. The cake is a running thing with state. You can make many cakes from the same recipe.

---

### Q10 - What is the difference between a simple LLM chatbot and an AI agent with tools? Give one concrete example of a "tool" and explain why it makes the agent more capable.

> Answer:

A plain LLM chatbot only generates text from its internal model and the prompt. An AI agent can call tools like web search, a database, or APIs to fetch live data or take actions. For example, a calendar API lets the agent check availability and actually schedule a meeting instead of just suggesting times.

---

### Q11 - What is MCP (Model Context Protocol)? What problem does it solve for AI coding assistants like GitHub Copilot? Name two examples of things an MCP server might expose to an AI assistant.

> Answer:

MCP (Model Context Protocol) standardizes how tools and assistants talk. Instead of building one-off integrations for every tool, a tool declares what it can do and an assistant can call those capabilities directly. That makes connecting new tools faster and less brittle.

Examples:
- Filesystem access - list files, read file contents, open editors.
- GitHub API - search issues, list pull requests, post comments.

---

### Q12 - What are Agent Skills in the context of AI coding assistants? How are they different from just writing instructions in a plain prompt? Show a minimal example of what a skill's .md metadata block might look like.

> Answer:

Agent Skills are small, shareable packages that bundle metadata, documentation, and clear instructions. They’re versioned so teams can update and reuse them easily.

A plain prompt is something you type from scratch every time. A Skill is different - it gives the assistant a structured rule for *when* and *how* to act, so the assistant can spot the right moment and apply the Skill automatically without repeated instructions.

Simple example:

```xml
<skill>
  <name>docker-compose-debugger</name>
  <description>
    Help debug Docker Compose setup issues.
    Use when the user asks "Why won't my containers start?" or "How do I fix this Docker error?"
  </description>
  <file>skills/docker-compose-debugger/SKILL.md</file>
</skill>
```
