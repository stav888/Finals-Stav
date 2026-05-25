# QA Authoring Instructions

Use this file when adding more QA entries to this folder. Follow the exact format used in `answer.txt` so entries remain consistent and machine-readable.

Template (replace values):

qa #<n>

Question (from finals page — Q<n>):
<full question text>

Expected: <short expected format / hints>

Answer:

Tokens:
["token1", "token2", ...]

One-sentence explanation:
<one concise sentence explaining the task or concept>

Sources (file links):
- https://github.com/pythonai200425/pages_ai/blob/main/e_nlp/Ka-NLP-intro.md
- https://github.com/pythonai200425/pythonai200425.github.io/blob/main/vector-db.html

<!--
File-level sources and extraction notes (keep inside this HTML comment):
- pages_ai/e_nlp/Ka-NLP-intro.md: 
Defines core NLP tasks and explicitly lists "Tokenization" (טוקניזציה) with simple examples (word splitting). Use this for definitions and basic examples.

- pythonai200425.github.io/vector-db.html: 
Explains token/chunk handling in practical RAG pipelines (Token Slider, chunking calculator, chunk-size guidance ~200–500 tokens) and shows text → embedding flow. Use this for chunking guidance and pipeline rationale.

When you write an answer, add these file paths under "Sources (file links)" and also include a short comment inside the HTML comment block above explaining what you extracted from each file.
-->

Example (QA1 copied):

qa #1

Question (from finals page — Q1):
What is tokenization? Give an example — show how the sentence "I'm learning NLP in 2025!" would be tokenized.

Expected: a list of tokens and a one-sentence explanation of what tokenization does and why it's the first step in NLP.
Answer:

Tokens:
["I", "'m", "learning", "NLP", "in", "2025", "!"]

One-sentence explanation:
Tokenization splits raw text into discrete tokens (words, subwords, or punctuation) so NLP systems can process and analyze language; it's the first step because models require these discrete units instead of raw character strings.

Sources (file links):
- https://github.com/pythonai200425/pages_ai/blob/main/e_nlp/Ka-NLP-intro.md
- https://github.com/pythonai200425/pythonai200425.github.io/blob/main/vector-db.html

<!--
pages_ai/e_nlp/Ka-NLP-intro.md: 
used for the definition and simple example of tokenization.

pythonai200425.github.io/vector-db.html: 
used for chunking/token context and RAG pipeline rationale.
-->
