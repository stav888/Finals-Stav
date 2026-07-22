# Finals — Questions & Answers (1–12)

### Q1 — What is tokenization? Give an example — show how the sentence "I'm learning NLP in 2025!" would be tokenized.

> Answer:

Tokenizing just splits text into pieces - words, numbers, punctuation, whatever.

Take "I'm learning NLP in 2025!". It becomes:

["I", "'m", "learning", "NLP", "in", "2025", "!"]

That way the computer can handle each piece on its own, even with weird punctuation mixed in.

---

### Q2 — What is the difference between stemming and lemmatization? Apply both to the words "running" and "better" and explain which preserves more linguistic meaning.

> Answer:

Stemming strips suffixes based on rules.
Lemmatization gives you the original form (lemma) — the actual word you'd find in a dictionary.

For example: “running”
- Stemming: run
- Lemmatization: run

But the word “better”:

- Stemming: better (remains the same)
- Lemmatization: good

Lemmatization keeps more meaning because you get the real word, not just a chopped-up version.

---

### Q3 — What does TF-IDF stand for? Explain in plain language why the word "the" scores almost zero in TF-IDF, while the word "photosynthesis" would score high.

> Answer:

TF-IDF means Term Frequency times Inverse Document Frequency.

TF-IDF is about finding words that actually matter.

"The" appears almost everywhere - in news, books, emails.
So it doesn't help us understand what makes a document special.

"Photosynthesis" is rare. It mostly shows up in science texts. 
If a document uses it a lot, it's probably about biology.

The idea is simple: look for words that are
1. Common in THIS document
2. Rare in OTHER documents

Those are the words that tell you what the document is really about.

---

### Q4 — What is a sentence embedding? How is it fundamentally different from one-hot encoding? Give one advantage embeddings have that one-hot vectors don't.

> Answer:

A sentence embedding is basically one vector that captures what the whole sentence means. Similar sentences end up close together in space.

One-hot encoding is different - it gives every word its own slot, a vector full of zeros with a single 1. So "cat" and "kitten" are totally unrelated, even though they mean almost the same thing.

The big advantage with embeddings is you can actually check if two sentences mean the same thing - like with cosine similarity. With one-hot, you just can't do that.

---

### Q5 — Explain cosine similarity in plain language. If two document vectors point in almost the same direction, what does that tell us about the documents they represent?

> Answer:

Cosine similarity calculates the angle between two vectors.
If two document vectors point in almost the same direction, it usually means the documents are similar in meaning, even if they don’t use exactly the same words.

That’s why cosine similarity is often better than Euclidean distance for embeddings: cosine focuses on direction (meaning), while Euclidean distance is more affected by vector length.

---

### Q6 — Why can't a regular SQL query like `WHERE description LIKE '%pizza%'` find semantically similar documents? What does a vector index solve that SQL can't?

> Answer:

 A `LIKE '%pizza%'` query only does exact substring matching.
If you search for "pizza", you will only get rows that literally contain the word "pizza" in the text. Expressions like "Italian food" or "pasta dishes" will be missed, even though they describe related content.
With a vector index, we first turn each document into an embedding and do a nearest-neighbors search.
That way we can retrieve chunks that are close in meaning to the question, not only those that repeat the same word.

---

### Q7 — What problem does RAG solve that a plain LLM (without RAG) cannot? Give a concrete example of when you would choose RAG over just prompting the LLM directly.

> Answer:

RAG connects an LLM to real documents so it can ground its answers in actual data instead of guessing.
This reduces hallucinations and lets the model use information that is either private or more up to date than its training set.
For example, in a support bot, we can use RAG to fetch the relevant customer record and the latest policy document before answering.
The final reply will then point to real sources instead of relying only on the model's internal knowledge.

---

### Q8 — Describe the 3 main steps of a RAG pipeline in the correct order. Be clear about what happens at ingestion time (when you load documents) vs query time (when a user asks a question).

> Answer:

During ingestion, we do three main things:

1. split each document into smaller chunks that are easier to work with.
2. create embeddings for all of these chunks.
3. store the vectors in a vector database or index.

At query time:

1. embed the user's question into a vector.
2. search for the closest chunks in the index.
3. send those chunks along with the question into the LLM and build an answer that uses this retrieved context.

---

### Q9 — What is the difference between a Docker image and a Docker container? Use an analogy to explain.

> Answer:

I think of a Docker image as a saved package for an application. It contains the files, libraries, and settings needed to start it.
A container is what we get when Docker runs that package. It is an actual running process with its own state, so it can be started, stopped, or removed.
The same image can be used to start several containers, just as one application package can be opened in several separate environments.

---

### Q10 — What is the difference between a simple LLM chatbot and an AI agent with tools? Give one concrete example of a "tool" and explain why it makes the agent more capable.

> Answer:

A simple LLM chatbot answers from its training data and the prompt it receives. It can suggest a meeting time, but it cannot put that meeting on a calendar by itself.
An AI agent can call an external tool when it needs information or needs to do something. For example, a calendar API could let it check available times and create the event for the user.
That is the main difference: the agent can use a system outside the chat, while the basic chatbot only returns text.

---

### Q11 — What is MCP (Model Context Protocol)? What problem does it solve for AI coding assistants like GitHub Copilot? Name two examples of things an MCP server might expose to an AI assistant.

> Answer:

MCP (Model Context Protocol) defines how an AI assistant can discover and use tools provided by another program.
This solves the problem of building a separate interface for every assistant and every tool. An MCP server lists the actions it supports, and the assistant can request one of those actions in the expected format.
For example, a server could allow Copilot to list and read files in a project. Another server could connect it to GitHub so it can search issues or create a pull request.

---


### Q12 — What are Agent Skills in the context of AI coding assistants? How are they different from just writing instructions in a plain prompt? Show a minimal example of what a skill's .md metadata block might look like.

> Answer:

Agent Skills are small, reusable definitions that bundle metadata, documentation, and instructions for the assistant.
Teams can version them, update them, and reuse them across projects.
A plain prompt is typed from scratch each time and usually applies only to that conversation.
A Skill tells the assistant when to use a behavior and how to follow it, so the result is more consistent without repeating long instructions.

Minimal metadata example:

```xml
<skill>
  <name>docker-compose-debugger</name>
  <description>
    Help debug Docker Compose issues.
    Use when the user asks about containers that won't start
    or Docker errors related to services.
  </description>
  <file>skills/docker-compose-debugger/SKILL.md</file>
</skill>
```
