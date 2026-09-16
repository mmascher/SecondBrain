---
type: meeting
date: 2026-07-23
participants:
  - Loris Van Katwijk
  - npigoux
  - martynia
  - Ryunosuke O'Neil
  - Andrea Piccinelli
  - Marco Mascheroni
topics:
  - DIRAC/DiracX sprint close-out (reviewing in-progress issues/pull requests)
  - DiracX docstring-convention pull request (Google style) — approved, pending unresolved review comment
  - Sprint velocity/story-point metrics and how they are computed
  - Sprint retrospective (reviewer availability with several team members away)
---

# DIRAC/DiracX Sprint Review and Retrospective Meeting

## Summary

Loris Van Katwijk led this shortened end-of-sprint meeting for the DIRAC/DiracX team (explicitly noted as shorter than usual because the refinement phase was skipped). Much of the meeting was conducted together with a speaker whose Zoom label appears in the transcript only as "[EP 2/R-014]"; as in other meetings in this series, this label reads as a room/location identifier rather than a person's name, and the speaker's identity could not be reliably determined, so they are not listed as a named participant above.

The team went through the sprint board's "in progress" items one by one. Several items were carried over to the next sprint because the assignee (most often Alexander, and in one case Christophe) was away; Alexander was reported to be away for a few weeks, returning in August, and Christophe was expected back "next week." Other items were moved to the next sprint pending review (a DiracX docstring-style pull request with one unresolved comment, a "multiple listeners" job-executor pull request awaiting reviewer feedback, an OpenSearch "upserts to multiple documents" item whose US-based requester could not attend, and a pull request Marco Mascheroni is waiting to have reviewed a second time). Ryunosuke O'Neil noted he should review whether some of his older, previously opened issues are still relevant, and one such item was removed from the sprint into the backlog rather than carried forward. The meeting then covered sprint velocity/story-point metrics for the sprint that had just ended, including a clarifying exchange between Marco Mascheroni and Loris Van Katwijk about how "expected story points," "expected velocity," and team availability relate to each other. The meeting closed with the start of a sprint retrospective, raising reviewer availability (with several people away) as a possible pain point; the transcript ends abruptly mid-sentence during this discussion, before a conclusion was reached.

## Decisions / Conclusions

- The sprint just concluded; the team reviewed all "in progress" board items, and unfinished ones were moved to the next sprint (with one item moved to the backlog instead — see Action Items).
- The DiracX docstring-convention-to-Google-style pull request (referred to in the transcript as approved "yesterday") is considered ready to merge, but has one unresolved review comment on `jobdb.py`; martynia noted it is important to resolve this quickly, since further rebasing would be costly given the pull request touches many files.
- Andrea Piccinelli's pull request for the "multiple listeners" job-executor item has already been reviewed; Andrea has pushed changes addressing reviewer comments and will reply to the remaining comments, then wait for feedback from Chris or Ryan.
- No changes to the sprint goals were proposed; Loris Van Katwijk indicated he would keep them as they are, while remaining open to suggestions.

## Action Items

- [ ] Look at and help resolve the pending, unresolved review comment on `jobdb.py` in the DiracX docstring-convention pull request — martynia
- [ ] Add replies to outstanding review comments on the "multiple listeners" job-executor pull request today, then wait for feedback from Chris or Ryan — Andrea Piccinelli
- [ ] Review whether older, previously opened issues (opened "a while ago") are still relevant — Ryunosuke O'Neil
- [ ] Continue work on an in-progress personal item into the next sprint (running longer than expected) — Loris Van Katwijk

## Discussion

### Sprint board review (in-progress items)
The team was missing several people (Federico, Alexander/"Alexandro", Christophe), which affected multiple items:
- An item associated with Federico was moved to the next sprint since he was not present; Ryunosuke O'Neil separately noted that he should review whether some of his own older, previously-opened issues are still relevant — one such item was moved to the backlog (rather than the next sprint) at his request.
- An item described as "fixed job verbal status which kills the payload" (exact wording/meaning unclear in the transcript) is assigned to Alexander; since he is away for a few weeks (returning in August, per "[EP 2/R-014]"), it was moved to the next sprint for him to pick up on return.
- The docstring-convention-to-Google-style pull request (see Decisions) — martynia identified the pull request via a garbled reference transcribed as "Ranka X1" / "Dirag X" (almost certainly a mis-transcription of "DiracX"), and confirmed it was approved the day before the meeting. "[EP 2/R-014]" flagged that a review comment on `jobdb.py` remains unresolved, while a comment concerning "the user" was described as fine, so the pull request can be merged once the remaining comment is addressed.
- An item titled "fixed skip local config file argument," assigned to Alexander, was removed from the sprint for reassignment when he returns.
- The "multiple listeners" job-executor item (see Decisions).
- An OpenSearch item described as "support upserts to multiple documents for OpenSearch" (transcribed as "upsets") is waiting for review; "[EP 2/R-014]" explained the requester is based in the US and could not join this meeting (referred to in the transcript as "Valentine" and, in a possibly garbled aside, "Mr. Lupin" — identity unclear). Moved to the next sprint.
- Marco Mascheroni reported having completed a first round of review with Alexander and made the requested changes; a second round of review is pending, and the pull request is otherwise considered ready to merge once reviewed. Loris Van Katwijk moved it to the next sprint, noting Alexander will still be away but that someone else might be able to review it.
- An item to "introduce the concept of a global prefix for OpenSearch" (transcribed once as "OpenSearch Nexus," meaning unclear) is assigned to Christophe, who is not currently in the meetings but expected back "next week." Moved to the next sprint.
- An item described only as "Jack X-Web's Alexand" (unclear in the transcript) involves pull request(s) Ryunosuke O'Neil still needs to review; he moved it to the next sprint.
- A "job matchmaking" item is waiting on Alexander; "[EP 2/R-014]" and Loris Van Katwijk discussed timing and referenced "the start of August" as when it might resume, aligning with Alexander's return.
- Loris Van Katwijk reported one of his own items is not yet finished and is taking longer than expected; he will continue it in the next sprint.
- One backlog item with no assignee was moved into the sprint mainly, per Loris Van Katwijk, to keep track of work that had already been completed.

### Sprint velocity and metrics
Loris Van Katwijk reported sprint metrics for the concluded sprint. The transcript's numeric figures are difficult to reconcile and may reflect transcription errors: he stated "we expected 137 points this sprint, with 3.7 people, with an expected velocity of 10, and we did 19 points, for a CT of 5.1" (meaning of "CT" not stated). He characterized the result as less than expected but still within the team's normal range, and proposed keeping the same explanatory comment from the previous week — that several people are still ramping up following what the transcript renders as "the Rakuten" (likely referring to a recent hackathon, based on context from the prior sprint-review meeting, though this is not certain) — and that "mid-worker" related work is still ongoing "under the hood."

Marco Mascheroni asked for clarification on how these metrics are computed. The discussion (partly unclear in the transcript) established that "expected story points" is the total story points planned for the sprint, "person(s)" refers to the number of people, and "expected velocity" is described as a fixed reference value. Loris Van Katwijk explained there isn't a clean formula converting story points to a fixed number of days, since actual effort for a given point value varies considerably depending on unknowns. Marco Mascheroni asked, as a rule of thumb, roughly how many story points would be expected for a given commitment percentage (e.g., proposing "four story points" for a 20% commitment); Loris Van Katwijk responded that 100% commitment corresponds to 10 points, so 10% would correspond to roughly 1 point — a figure that does not match Marco Mascheroni's proposed rule of thumb, though this discrepancy was not explicitly resolved in the transcript.

### Sprint retrospective (incomplete)
Loris Van Katwijk opened the retrospective by asking what had slowed the team down during the sprint, removing a carried-over note from the previous sprint's retrospective. He proposed that, since several people are away, the team is sometimes short on reviewers, and asked whether this was seen as a problem. Responses in the transcript are unclear/ambiguous ("I think I heard," "No?"). The transcript ends abruptly mid-sentence during this exchange, before any conclusion was reached.

## Open Questions

- Will the pending `jobdb.py` review comment on the DiracX docstring-convention pull request be resolved in time to merge without requiring further rebasing?
- Will the "multiple listeners" job-executor pull request be merged after Andrea Piccinelli's reply and feedback from Chris or Ryan?
- Can any of the items blocked on Alexander's absence (the "job verbal status"/payload item, the "skip local config file argument" fix, Marco Mascheroni's pull request awaiting second review, and the "job matchmaking" item) be picked up by someone else before he returns in August?
- Does the team consider reduced reviewer availability (due to several members being away) an actual problem needing a response? The retrospective discussion on this point was not concluded in the available transcript.
- What is meant by "the Rakuten" in the carried-over sprint comment about people ramping up — the transcript is unclear, and this may be a mis-transcription (possibly of "hackathon," based on context from the prior sprint-review meeting).

## Related

[[DIRAC]] · [[DIRACX]] · [[OpenSearch]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-23 10.24.46 BiLD`)
