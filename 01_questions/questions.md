# Finals — Combined Questions & Answers (1–12)

### Q1 — What is tokenization? Give an example — show how the sentence "I'm learning NLP in 2025!" would be tokenized.

> Answer:

Tokens: ["I", "'m", "learning", "NLP", "in", "2025", "!"]

Tokenization splits text into pieces so models can actually work with it. It's the first step because models need discrete tokens to convert into numbers. In simple terms, you can't feed raw sentences straight into a model; you first break them into tokens.

---

### Q2 — What is the difference between stemming and lemmatization? Apply both to the words "running" and "better" and explain which preserves more linguistic meaning.

> Answer:

Stemming (Porter): "running" > "run", "better" > "better"

Lemmatization (POS-aware): "running" > "run", "better" > "good"

Stemmers chop off endings using quick rules. They're fast, but they can leave odd or non-words. Lemmatizers use a dictionary and grammar tags. They return the real base form, so they keep more meaning. In practice, lemmatization is cleaner but a bit slower.

---

### Q3 — What does TF-IDF stand for? Explain in plain language why the word "the" scores almost zero in TF-IDF, while the word "photosynthesis" would score high.

> Answer:

TF-IDF means Term Frequency times Inverse Document Frequency.
Term frequency is simply how many times a word appears in one document. Inverse document frequency pushes down the score of words that appear in almost every document.
When you multiply them, you get a score that favors words that are common in this specific document but not common in the whole collection.
That is why "the" gets close to zero. It appears everywhere. "Photosynthesis" gets a higher score because it only shows up in certain science texts and helps describe them better.


---

### Q4 — What is a sentence embedding? How is it fundamentally different from one-hot encoding? Give one advantage embeddings have that one-hot vectors don't.

> Answer:

A sentence embedding is a numeric vector that tries to capture the meaning of a whole sentence, not just which words are inside it.
A one-hot vector just marks presence or absence of words and is mostly zeros, so it cannot express similarity between different sentences.
With embeddings, sentences that talk about similar topics end up close together in the vector space.
This is useful because we can measure semantic similarity, for example with cosine similarity, and find related sentences even if they use different wording.

---

### Q5 — Explain cosine similarity in plain language. If two document vectors point in almost the same direction, what does that tell us about the documents they represent?

> Answer:

Cosine similarity looks at the angle between two vectors.
If the angle is small and the vectors point in almost the same direction, the similarity is high, which means the two documents talk about similar things.
If the vectors point in very different directions, the similarity score is low, even if the documents are long.
The useful part is that cosine similarity ignores the length of the vectors, so a short note and a long article on the same topic can still be considered very similar.

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

1. We split each document into smaller chunks that are easier to work with.
2. We create embeddings for all of these chunks.
3. We store the vectors in a vector database or index.

At query time:

1. We embed the user's question into a vector.
2. We search for the closest chunks in the index.
3. We send those chunks along with the question into the LLM and build an answer that uses this retrieved context.

---

### Q9 — What is the difference between a Docker image and a Docker container? Use an analogy to explain.

> Answer:

A Docker image is like a recipe or a blueprint: it describes what to install and how to run the application.
A Docker container is a running instance created from that image, with its own state and lifecycle.
You can start many containers from the same image, just like you can bake several cakes from one recipe, and each one can end up in a slightly different state while it runs.

---

### Q10 — What is the difference between a simple LLM chatbot and an AI agent with tools? Give one concrete example of a "tool" and explain why it makes the agent more capable.

> Answer:

A simple LLM chatbot only generates text based on its training data and the current prompt.
An AI agent, on the other hand, can call tools such as web search, databases, or external APIs to get fresh information or perform actions.
For example, with a calendar API as a tool, the agent can actually create a meeting in the user's calendar instead of just suggesting possible times in the chat.
This makes the agent more capable because it is not limited to text predictions. It can interact with the outside world.

---

### Q11 — What is MCP (Model Context Protocol)? What problem does it solve for AI coding assistants like GitHub Copilot? Name two examples of things an MCP server might expose to an AI assistant.

> Answer:

MCP (Model Context Protocol) is a standard way for tools and AI assistants to talk to each other.
Instead of writing a different custom integration for every tool, an MCP server describes the operations it supports and the assistant can call them in a uniform way.
This makes it easier and safer to add new tools to systems like GitHub Copilot.
Examples of what an MCP server might expose include file operations, such as listing and reading project files, and GitHub actions like searching issues or creating pull requests.

---


### Q12 — What are Agent Skills in the context of AI coding assistants? How are they different from just writing instructions in a plain prompt? Show a minimal example of what a skill's .md metadata block might look like.

> Answer:

Agent Skills are small, reusable definitions that bundle metadata, documentation, and clear instructions for the assistant.
Because they are versioned and shareable, teams can update them once and reuse them across projects.
A plain prompt is something the user types ad-hoc each time and the assistant usually forgets it after the session.
A Skill, in contrast, tells the assistant in a structured way when to apply the behavior and how to do it, so it can recognize relevant situations and act consistently without the user repeating long instructions.

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
