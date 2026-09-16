---
type: meeting
date: 2026-07-17
participants:
  - Andrea Piccinelli
  - Marco Mascheroni
topics:
  - Rucio caching for pilots
  - glideinWMS dynamic data movement
  - DIRAC ADR terminology (task vs meta job)
  - Transformation System input splitting
  - GitHub PR workflow
  - meeting scheduling
---

# Rucio Caching, Meta Job Terminology, and ADR Recap

## Summary

Andrea Piccinelli and Marco Mascheroni discussed several ongoing [[Submission Infrastructure]] design topics: caching interaction with [[Rucio]] for pilot-side static data, an open question about where to implement dynamic data-movement logic (at the [[DIRAC]] level or at the [[glideinWMS]]/WMS level), naming/terminology being settled in a DIRAC Architecture Decision Record (ADR) for "task"-like entities, a proposal around splitting large Transformation System inputs, a brief review of a job-execution PR, a short exchange about `gh` CLI vs. the GitHub web UI for creating pull requests, and logistics for the next bi-weekly meeting.

**Note on source quality:** this transcript is a machine-generated closed-caption transcription of a mostly Italian conversation, and much of it is fragmented or garbled (mixed English/Italian fragments, single words, apparent mistranslations). This note only reports content that could be reasonably reconstructed from context; many exchanges in the raw transcript were too unclear to summarize reliably and have been omitted.

## Decisions / Conclusions

No firm decisions were recorded. The discussion consisted of proposals, an open design question, and a recap of a prior meeting.

## Action Items

- [ ] Invite Jamie to the Wednesday bi-weekly meeting (18:00) and add it to the calendar — Marco Mascheroni

## Discussion

### Rucio interaction and pilot caching

Marco proposed contacting [[Rucio]] through a cache rather than repeatedly, since the data needed (a list used by the pilot) is essentially static. He described this as intended to be the only interaction point with Rucio in this context.

### Dynamic data movement — open design question

The group discussed the idea of moving data dynamically within [[glideinWMS]]/the pool, with some component monitoring the situation and potentially redefining a job's classad (e.g., ClassAd) based on what's happening. Marco noted this component would need to control the pool and be aware of [[DIRAC]] data and where jobs are running, and expressed reluctance about this direction ("something I didn't want to do, but there doesn't seem to be a way around it" — paraphrased). Andrea raised an open question about whether this logic should be implemented at the DIRAC level or at the WMS/[[glideinWMS]] level (the exact component name was unclear in the transcript), to react to job conditions by moving data or changing classads, and mentioned a "concept of distance" in this context — the meaning of this was not made clear in the transcript.

### DIRAC ADR: task vs. meta job terminology

Marco described an ongoing terminology discussion (apparently held the previous day with a colleague, name unclear in the transcript) about naming in a DIRAC ADR. Points mentioned:

- Entities that had informally been called "tasks" will reportedly be renamed to something else in the ADR.
- A distinction was drawn between "direct task" and products referred to as "meta job" — a meta job being built from an aggregate of job inputs.
- Separately, the "Monitor task" entities that run inside the DIRAC framework are distinct from the meta-job-like units produced by the Transformation System; both had previously been informally called "tasks" but are being renamed differently in the ADR to avoid ambiguity.

The final naming was not confirmed in this transcript.

### Transformation System input splitting (proposal)

Marco described a proposal to add the ability to split a large input to the Transformation System into two parts (e.g., when an input is too large) and retry, rather than failing outright. This was discussed at a conceptual/higher level; no decision was recorded.

### Recap of a prior ADR-related meeting

Andrea and Marco reflected on a previous set of two ~3-hour ADR discussion sessions. Marco said it left him a bit unsatisfied because the group concluded "almost nothing," though they did produce a small schema/diagram, and the discussion was not only about Rucio. There was a shared sense that even that limited output was nearly not achieved.

### Job execution PR review and hackathon models

The two briefly looked at a commit/PR related to job execution (described as related to "fully implement[ing] job execution", exact wording unclear), referencing models that had reportedly already been imported/introduced during a hackathon. Discussion also touched on sandbox/search types and matchmaking, but the specifics were not clear enough in the transcript to summarize reliably.

### GitHub PR workflow

Andrea described creating pull requests via the GitHub web interface. Marco described instead using the `gh` CLI directly from the terminal (e.g., opening a PR in draft state), and the two briefly compared the two approaches.

### Next meeting logistics

The group noted their regular Wednesday bi-weekly meeting had been skipped/replaced recently (e.g., for a separate "exploring collaboration" session), and agreed to resume on the upcoming Wednesday at 18:00. Marco said he would invite Jamie and add the meeting to the calendar, and mentioned wanting to ask about a request from Jamie's side (the transcript is unclear here — it may refer to a "feature request," but this is uncertain). There was also brief discussion about whether to invite additional people (referred to only vaguely, e.g. "Justin's" group), without a clear resolution in the transcript.

## Open Questions

- Should dynamic data-movement/classad-reaction logic be implemented at the DIRAC level or at the WMS/glideinWMS level?
- What is the final terminology that will be adopted in the DIRAC ADR for "task," "meta job," and "Monitor task" entities?
- Should additional people beyond Jamie be invited to the upcoming Wednesday meeting?

## Related

[[Rucio]] · [[DIRAC]] · [[glideinWMS]] · [[Pilot Jobs]] · [[GitHub]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-17 14.31.14 Sala riunioni personale di Andrea Piccinelli`)
