# QA Authoring Instructions

Use this file when adding more QA entries to this folder. Keep entries consistent and machine-readable so they can be processed automatically by scripts.

Goals
- Keep one question per `q<n>.txt` file. Follow the template exactly.
- Always include exact source blob URLs and a short extraction note per source.

Template (replace values)
 
qa #<n>

Question (from finals page — Q<n>):
<full question text — copy exactly>

Expected: <short expected format / hints>

Answer:

Tokens:
["token1", "token2", ...]

One-sentence explanation:
<one concise sentence explaining the task or concept>

Sources (file links — use GitHub blob URLs):
- https://github.com/<owner>/<repo>/blob/<branch>/path/to/file.md

Extraction notes (keep inside this HTML comment):
<!--
- path/to/file.md: one-line note describing what was extracted (definition, example, parameter values, recommended chunk size, etc.)
-->

Filename conventions
- Use `q<n>.txt` for each question (e.g., `q1.txt`).
- Keep `answer.txt` as a combined or legacy file only if needed; prefer per-question files.

Source citation rules
- Prefer `https://github.com/owner/repo/blob/main/path/to/file.md` (the blob URL) so reviewers can click directly to the source.
- Add a one-line extraction note per source inside the HTML comment block (as shown above).


Quick checklist (before saving a new `q<n>.txt`)
- [ ] File named `q<n>.txt` and placed in `qa_1/`.
- [ ] `Question` copied exactly from finals page.
- [ ] `Expected` hint included.
- [ ] `Answer:` field present with `Tokens:` and `One-sentence explanation:`.
- [ ] Sources listed as blob URLs and extraction notes added inside the HTML comment.
- [ ] Run a quick spellcheck and keep wording concise (no large pasted sections from sources).

If you want, I can convert existing `answer.txt` to per-question files or generate `answer.md` from all entries. Ask me to proceed.
