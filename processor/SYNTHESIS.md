# Knowledge Synthesis

This document defines the workflow for turning the accumulated SecondBrain
corpus into durable cross-source knowledge.

It is deliberately separate from `processor/AGENTS.md`, which governs
individual meeting-note processing.

## Purpose

Meeting processing answers:

> What happened in this meeting?

Knowledge synthesis answers:

> What do we now know, based on everything we have learned across the corpus?

Synthesis should produce durable understanding that remains useful after the
individual meetings and their chronology are forgotten.

The primary output is:

```text
obsidian/30-Concepts/
```

## Synthesis principles

### 1. Synthesize; do not summarize

A concept note must combine information from multiple relevant sources.

It should explain the concept itself, its context, relationships, evolution,
constraints, and important unresolved issues.

Do not turn a meeting note into a concept note by changing its title.

### 2. Evidence before frequency

A frequently mentioned term is not automatically a concept.

A concept candidate should normally have one or more of:

- evidence across multiple meetings;
- support from substantial reference material;
- an important architectural role;
- an established operational role;
- a durable design decision;
- a recurring constraint or problem;
- a meaningful relationship to other durable concepts.

The seed wikilink vocabulary in `AGENTS.md` is a starting point for
cross-linking, not a checklist of notes to create.

### 3. Preserve source distinctions

Synthesis must distinguish:

- established facts;
- historical decisions;
- current understanding;
- proposals;
- opinions;
- observations;
- open questions;
- unresolved disagreements.

Do not turn a proposal into an established design merely because it appears
in several discussions.

### 4. Preserve disagreement

When sources disagree:

- preserve the disagreement;
- identify the relevant sources when practical;
- explain whether the disagreement is historical or current;
- do not silently select one interpretation.

A concept note may therefore contain multiple perspectives.

### 5. Historical evolution matters

The corpus is intended to preserve institutional and technical memory.

When useful, explain how an architecture, system, policy, or practice evolved.

Do not collapse historical states into the current state.

Prefer language such as:

- "Historically, ..."
- "The 2025 review described ..."
- "Later discussions proposed ..."
- "The current understanding is ..."
- "This remains an open question ..."

### 6. Do not manufacture relationships

Obsidian links should represent meaningful relationships.

Link to an existing or anticipated concept when doing so helps explain the
knowledge graph.

Do not create links merely because two words appear in the same source.

A link does not imply that the target note already exists.

### 7. Source traceability is mandatory

Every concept note must contain:

```markdown
## Sources
```

The Sources section should identify the meeting notes, references,
presentations, proceedings, or code sources that support the note.

Prefer direct links to the relevant Obsidian notes or repository paths.

A reader should be able to trace important claims back to source material.

### 8. Do not overfit to meetings

Meetings are the primary accumulated knowledge source, but they are not the
only source.

When relevant, synthesis may use:

- meeting notes;
- CMS requirements and reviews;
- presentations;
- proceedings;
- source documentation;
- code and configuration;
- repository history when explicitly available.

Use deeper source material selectively rather than reading the entire
repository indiscriminately.

### 9. Code is evidence, not automatically knowledge

A code repository can establish how something is implemented.

It does not by itself establish:

- why it was designed that way;
- whether it is still current;
- whether the implementation is authoritative;
- whether an implementation detail is intended architecture.

Use code to support implementation claims and distinguish those claims from
design intent or organizational decisions.

## Discovery workflow

Discovery is a read-mostly operation that identifies candidates before durable
notes are created.

Run:

```bash
python3 processor/synthesize.py discover --agent codex
```

or:

```bash
python3 processor/synthesize.py discover --agent claude
```

The result is:

```text
obsidian/30-Concepts/_synthesis/concept-candidates.md
```

The discovery artifact is a human review checkpoint.

It should identify:

- candidate concept;
- why it appears durable;
- supporting sources;
- related candidates;
- disagreements or uncertainty;
- whether enough evidence exists for synthesis.

### Discovery must not create concept notes

The discovery operation must not create files such as:

```text
obsidian/30-Concepts/HTCondor.md
obsidian/30-Concepts/Factory.md
```

even if those topics are obviously important.

The purpose is to establish a candidate map first.

## Candidate approval

A candidate becomes eligible for synthesis only after explicit approval.

Do not infer approval from:

- existence of a candidate;
- its frequency;
- its position in the document;
- a seed vocabulary entry;
- a previous wikilink.

Use an explicit marker in the candidate document, for example:

```markdown
## Candidate: Workload Management Architecture

Status: approved

...
```

or:

```markdown
Status: needs-more-evidence
```

or:

```markdown
Status: rejected
```

Only candidates explicitly marked:

```text
Status: approved
```

may be synthesized by the `synthesize` command.

## Synthesis workflow

After reviewing and approving candidates:

```bash
python3 processor/synthesize.py synthesize --agent codex
```

The processor validates the generated notes before installing them into:

```text
obsidian/30-Concepts/
```

Existing concept notes are protected during `synthesize`.

An attempt to overwrite an existing concept note is an error.

## Updating existing concepts

When new source material arrives, use:

```bash
python3 processor/synthesize.py update --agent codex
```

The update operation should:

- identify concepts materially affected by new evidence;
- inspect the relevant new sources;
- preserve existing useful content;
- incorporate new information;
- preserve historical evolution;
- preserve disagreements;
- avoid stylistic rewrites with no knowledge value.

Updates are deliberately separate from initial synthesis.

## Incremental operation

Knowledge synthesis is not a one-time migration.

The intended long-term loop is:

```text
new sources
    ↓
Meeting Processing / source ingestion
    ↓
updated corpus
    ↓
Knowledge Synthesis
    ↓
new or updated concepts
    ↓
later sources
    ↓
repeat
```

When missing historical transcripts or requirements arrive, do not restart the
entire knowledge base.

Process the new sources, then revisit the affected concepts.

## Scope control

Do not process the entire repository in a single unbounded agent operation.

Prefer:

1. inspect the meeting corpus;
2. discover candidates;
3. review candidates;
4. synthesize approved candidates;
5. inspect the generated notes;
6. update concepts incrementally as new evidence appears.

Correctness, traceability, and durable usefulness are more important than
maximum throughput.

## Concept note structure

A concept note should normally look approximately like:

```markdown
---
type: concept
---

# Concept Name

## Overview

What the concept is and why it matters.

## Current Understanding

The durable understanding supported by the corpus.

## Evolution

Important historical changes, when relevant.

## Relationships

Meaningful relationships to other concepts.

## Open Questions

Unresolved issues or areas where the corpus remains uncertain.

## Sources

- [[Meeting Note]]
- [[Another Meeting Note]]
- `40-References/...`
```

Sections may be adapted when a concept genuinely does not need them, but
`## Sources` is mandatory.

## Uncertainty

The same source-fidelity standards used during meeting processing apply here.

Do not silently resolve:

- contradictory sources;
- ambiguous terminology;
- uncertain dates;
- unclear ownership;
- unclear architectural intent;
- uncertain transcription.

When evidence is insufficient, say so.

A useful synthesis can explicitly state:

> The available sources do not establish this.

That is preferable to filling the gap with inference.

## Sensitive information

Concept notes should focus on durable technical, operational,
organizational, and project knowledge.

Do not turn personnel evaluations, private circumstances, or other sensitive
meeting material into durable concept knowledge unless the information is
strictly necessary to explain a durable operational or technical consequence.

Capture the minimum necessary information.

## Relationship to Phase 1

`processor/AGENTS.md` remains authoritative for meeting-note processing.

This document governs cross-source synthesis.

The boundaries are:

```text
Transcript
    │
    ▼
Meeting Processing
    │
    ▼
20-Meetings/
    │
    ├── References / Presentations / Proceedings / Code
    │
    ▼
Knowledge Synthesis
    │
    ▼
30-Concepts/
```

Phase 1 should not create concept notes merely because it encounters a
candidate concept.

Phase 2 should not rewrite meeting notes merely to improve them.

Both layers preserve different kinds of knowledge.
