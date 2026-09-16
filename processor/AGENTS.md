# Transcript Processing

Process meeting transcripts into high-quality Obsidian-compatible Markdown as part of the Submission Infrastructure knowledge base.

The long-term goal is to build a reliable Obsidian knowledge base from historical meeting transcripts and other sources. Meeting notes are the primary source material for later cross-meeting knowledge synthesis.

## General rules

* Transcripts are the source of truth.
* Do not invent facts, decisions, dates, participants, action items, conclusions, or technical details.
* Do not silently resolve ambiguity in the transcript.
* If the transcription is unclear, omit the information or explicitly mark it as uncertain.
* Preserve the terminology used in the source, particularly technical terminology, project names, acronyms, and system names.
* Distinguish clearly between:

  * decisions
  * proposals
  * opinions
  * observations
  * open questions
  * action items
* Do not turn a proposal or discussion into a decision unless the transcript clearly establishes that it was decided.
* Create an Action Item only when the transcript contains an explicit commitment, assignment, or agreed follow-up. Do not promote a suggestion or possible next step into an action item merely because it sounds useful.
* Remove conversational noise, greetings, repetition, and irrelevant discussion.
* Preserve meaningful technical details, constraints, architecture information, operational knowledge, and reasoning behind important decisions.
* Preserve substantive organizational/planning topics (e.g. EPR, conference contributions, staffing/work planning) when they contain a decision, commitment, deadline, or meaningful follow-up, even if they are secondary to the meeting's main technical discussion.
* The result should be a concise synthesis, not a chronological reconstruction of the transcript.

## Language

* Meeting notes must be written in English.
* Preserve technical terminology and established names.
* Do not translate project names, product names, acronyms, repository names, or other canonical technical terms.

## Phase 1: Meeting notes

Phase 1 converts each substantive transcript into one Obsidian meeting note.

Phase 1 answers:

> "What happened in this meeting?"

For each substantive transcript, create exactly one meeting note.

The meeting note should capture the information that will remain useful after the meeting itself is forgotten:

* what was discussed
* important technical context
* decisions and conclusions
* meaningful proposals
* action items
* unresolved questions
* relevant systems, projects, concepts, and people
* relationships between topics

Do not attempt to build the complete knowledge base while processing an individual transcript.

### Meeting-note format

Meeting notes should use YAML frontmatter followed by the following structure:

```markdown
---
type: meeting
date:
participants:
topics:
---

# Meeting title

## Summary

## Decisions / Conclusions

## Action Items

- Include this section in every meeting note.
- If there are no explicit action items, write:
  `None identified.`
- Only create an action item when the transcript contains an explicit
  commitment, assignment, or agreed follow-up.

## Discussion

## Open Questions

## Related

## Source
```

Use the structure consistently. The `## Action Items` section is mandatory
and must contain `None identified.` when there are no explicit action items.
Other sections may be omitted when they genuinely have no useful content.

For action items:

* Use Markdown task items.
* Include an owner when the transcript clearly identifies one.
* Do not invent an owner.
* Do not manufacture deadlines that were not stated.

Example:

```markdown
- [ ] Update the factory configuration — Jeff
- [ ] Investigate the `arch=auto` behavior
```

If there are no explicit action items, do not invent any.

### Meeting titles

Use a concise descriptive title based on the actual content of the meeting.

Do not rely blindly on the recording filename or Zoom room title when the transcript provides enough information to identify the subject.

If the subject cannot be determined reliably, use a conservative title rather than inventing one.

### Dates and participants

Use dates and participants only when supported by the transcript, filename, surrounding repository context, or other explicitly available source information.

Do not guess.

## Obsidian wikilinks

Use Obsidian wikilinks for meaningful persistent entities.

Wikilinks are intended to make relationships between meetings visible and enable later cross-meeting synthesis.

### Canonical entities

Prefer canonical names such as:

### CMS / HEP / organizations

```text
[[CMS]]
[[WLCG]]
[[HSF]]
[[CERN]]
[[OSG]]
```

### Software and infrastructure

```text
[[HTCondor]]
[[glideinWMS]]
[[WMAgent]]
[[WMCore]]
[[CRAB]]
[[DIRAC]]
[[DIRACX]]
[[Rucio]]
[[XRootD]]
[[CVMFS]]
[[Frontier]]
```

### Platforms and computing

```text
[[Kubernetes]]
[[Docker]]
[[OpenShift]]
[[Linux]]
[[AlmaLinux]]
[[Cloud Computing]]
[[HPC]]
[[HTC]]
[[GPU]]
[[Heterogeneous Computing]]
```

### Workload-management concepts

```text
[[Workload Management]]
[[Work Queue]]
[[Workload Management System]]
[[Factory]]
[[Factory Operations]]
[[Factory Configuration]]
[[Factory Operator]]
[[Pilot Jobs]]
[[Resource Provisioning]]
[[Dynamic Resource Provisioning]]
[[Submission Infrastructure]]
[[Global Workflow Orchestrator]]
[[Data Broker]]
```

### Software engineering

```text
[[Python]]
[[Git]]
[[GitHub]]
[[CI/CD]]
[[Microservices]]
[[REST API]]
[[Monitoring]]
[[Observability]]
```

This list is a seed vocabulary, not an exhaustive list.

Additional entities may be wikilinked when they clearly meet the criteria below.

### When to create a wikilink

Prefer a wikilink when an entity is:

* a persistent technical concept
* a system, service, project, or architecture
* an important organization or community
* a recurring operational topic
* a significant component of the Submission Infrastructure ecosystem
* likely to recur across multiple meetings
* potentially useful as a future concept note

Do not create wikilinks for:

* generic words
* incidental mentions
* ordinary English terms
* every person mentioned
* every package
* every command
* one-off implementation details
* trivial filenames or variables
* entities that appear only incidentally and have no likely value for later retrieval

Repositories, files, and code components may be wikilinked when they are recurring or important to the discussion. Do not create knowledge entities for an individual file, function, command, or configuration parameter merely because it appears once.

### People

Do not wikilink every person.

A person may be wikilinked when they are a recurring or important knowledge entity whose involvement is useful for understanding the broader corpus.

Do not create person notes merely because someone attended a meeting.

### Canonicalization

Avoid multiple wikilinks for the same underlying entity.

Prefer canonical names over variants.

For example, use:

```text
[[HTCondor]]
```

rather than creating variants such as:

```text
[[Condor]]
[[HTCondor]]
[[HTC Condor]]
```

when they refer to the same entity.

If the correct canonical name is uncertain, preserve the source terminology rather than silently inventing a canonical name.

### Wikilinks do not imply note creation

A wikilink is a reference, not a request to create a note.

A Phase 1 meeting note MAY contain:

```markdown
[[Factory Patching]]
```

even when `Factory Patching.md` does not yet exist.

Do not create the target note merely because it was wikilinked.

The purpose of Phase 1 wikilinks is to create useful connections that can later support cross-meeting synthesis.

## Knowledge extraction

During Phase 1, identify candidate durable knowledge only so that it can be linked and considered later.

Durable knowledge includes:

* architecture
* design decisions
* technical concepts
* operational procedures
* important systems
* recurring problems
* project context
* constraints
* established practices
* significant interfaces and dependencies
* recurring organizational or operational structures

Do not create a separate concept note for every candidate.

A concept should normally become a durable concept note only during Phase 2, after multiple meeting notes and other relevant sources can be considered together.

Do not let the existence of a concept in one meeting trigger creation of a concept note.

Avoid duplicating the same knowledge across meeting notes and concept notes.

## Phase 2: Knowledge synthesis

Phase 2 happens after a sufficiently large meeting corpus has been processed.

Phase 2 answers:

> "What do we now know, based on everything we have learned across meetings?"

Phase 2 may create or update durable notes under:

```text
obsidian/30-Concepts/
```

Concept notes should synthesize information from multiple meetings and other available sources.

They should capture durable understanding rather than reproduce individual meeting discussions.

When sources disagree:

* preserve the disagreement
* identify the relevant sources when possible
* do not silently choose one interpretation
* distinguish historical decisions from current understanding

Phase 2 must not be performed automatically while processing individual Phase 1 transcripts unless explicitly requested.

## Source fidelity and uncertainty

The distinction between what the transcript explicitly says and what can reasonably be inferred is important.

### Transcription uncertainty

Transcription errors must not be silently corrected unless the intended
term is unambiguous from the transcript or another explicitly available
source.

When a technical term, repository name, person name, issue number, or other
specific identifier is unclear:

- preserve the uncertainty;
- do not guess or silently substitute a likely term;
- do not create a wikilink based on an uncertain transcription;
- if useful, state the likely interpretation explicitly as uncertain.

Prefer language such as:

* "The group discussed..."
* "It was proposed that..."
* "The current understanding was..."
* "The group agreed to..."
* "An open question was..."
* "The transcript is unclear about..."
* "This appears to have been..."

Do not present interpretation as fact.

When in doubt, preserve uncertainty rather than manufacture certainty.

### Speaker and room labels

Zoom speaker labels may represent an individual, a room, a conference
endpoint, or a group of participants.

Do not assume that a speaker label identifies a single person.

For example, a label such as `[WH8XE- Quarium]` may represent a meeting
room with multiple participants rather than an individual speaker.

If a label appears to represent a room or group of participants:
- do not treat the label itself as a person;
- do not infer individual identities from the label;
- include individual participants only when they are reliably identified
  elsewhere in the transcript or explicitly available source context.

## Output and source preservation

* Never modify, delete, rename, or overwrite original transcripts.
* Preserve the original transcript filename in the meeting note's `Source` section.
* Create one Markdown meeting note per substantive transcript.
* Do not overwrite an existing meeting note unless explicitly instructed.
* If a corresponding meeting note already exists, report it and skip that transcript.
* Processing should be deterministic and repeatable.
* Do not modify existing meeting notes merely to make them conform to a newer format unless explicitly instructed.

## Empty and non-substantive transcripts

Not every transcript should produce a meeting note.

Skip transcripts that are clearly:

* audio/video tests
* Zoom or recording tests
* greetings-only recordings
* silence
* accidental recordings
* empty or effectively empty recordings
* fragments that contain no substantive information

Do not create placeholder notes for these.

Short meetings are valid if they contain substantive information.

If a transcript is incomplete but contains potentially useful material, do not create a low-confidence meeting note unless the available source is sufficient to produce a reliable synthesis.

Leave the original transcript untouched and report the reason for skipping it.

## Sensitive and personal information

Meeting notes should focus on durable technical, operational, organizational, and project knowledge.

Omit:

* personnel evaluations
* performance discussions
* personal circumstances
* HR details
* private opinions that are not relevant to durable knowledge
* unnecessary personal information

If a private discussion has a substantive operational or technical consequence, capture only the minimum necessary information needed to understand that consequence.

## Large transcripts

Do not repeatedly attempt to process a transcript that is too large to review reliably in a single pass.

For large transcripts:

* do not produce a low-confidence note
* do not repeatedly retry the same single-pass strategy
* do not modify the original transcript
* report that chunked or multi-pass processing is required
* use a dedicated chunked-processing strategy when appropriate

A large transcript should be treated as a processing problem, not as a reason to lower source-fidelity standards.

## Batch processing strategy

The goal is to process a large corpus of meeting transcripts into a reliable Obsidian meeting-note corpus.

Processing should be incremental and resumable.

Before processing a batch:

1. Identify all transcript files.
2. Determine which transcripts already have a corresponding meeting note.
3. Determine which transcripts are non-substantive, incomplete, or otherwise unsuitable for processing.
4. Process only transcripts that are not already complete.
5. Never reprocess an existing meeting note unless explicitly requested.

The processor must be safe to stop and resume. A partial batch must not require starting over.

### Processing priority

Prefer this order:

1. Normal-sized substantive transcripts.
2. Medium-sized substantive transcripts.
3. Large transcripts requiring multi-pass processing.
4. Incomplete transcripts only if a complete source becomes available.

Do not spend substantial effort repeatedly retrying a transcript that has already been determined to require a different processing strategy.

### Batch size

Do not attempt to process the entire corpus in one agent turn.

Use small, bounded batches and stop after completing a reasonable batch so that the results can be inspected before continuing.

The goal is reliable corpus construction, not maximum throughput.

## Processing state

The transcript corpus is expected to contain transcripts at different stages of processing.

Do not assume that every transcript must produce a meeting note.

A transcript can be:

* `unprocessed`
* `processed`
* `skipped_non_substantive`
* `skipped_incomplete`
* `pending_large_transcript`

A transcript should normally be processed at most once unless explicitly requested.

The presence of a corresponding meeting note is sufficient to consider a transcript processed for Phase 1.

If a transcript was deliberately skipped, preserve enough information to explain why it was skipped so that a future processing pass does not repeatedly reconsider it.

## Corpus inventory and resumability

Before large-scale processing begins, establish the current corpus state.

The processor should be able to determine:

* total number of transcripts
* transcripts already processed
* transcripts already skipped
* remaining unprocessed transcripts
* large transcripts requiring special handling
* incomplete transcripts
* existing meeting notes
* existing processing scripts or state files

When practical, maintain processing state separately from the meeting-note content so that processing can be resumed without relying on model memory.

Do not create a second competing source of truth for meeting content: the transcript remains the source of truth, while processing state only records workflow status.

## Agent behavior

Prefer simple, bounded operations over large speculative operations.

When asked to process a corpus:

1. inspect first
2. classify
3. process a bounded batch
4. verify outputs
5. report results
6. continue only when explicitly requested or when the current task clearly defines the next bounded batch

Do not attempt to process hundreds of transcripts in a single unbounded operation.

When a task cannot be completed reliably within the available context or processing budget:

* stop cleanly
* preserve all completed work
* report what was completed
* report what remains
* identify the appropriate next processing strategy
* do not compensate by lowering the quality or source-fidelity requirements

The agent should optimize for correctness, traceability, and resumability rather than raw throughput.

