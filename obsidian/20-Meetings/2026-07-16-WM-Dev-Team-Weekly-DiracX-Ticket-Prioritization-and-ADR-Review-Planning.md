---
type: meeting
date: 2026-07-16
participants:
  - Valentin Y Kuznetsov
  - Alan Malta Rodrigues
  - Liz Sexton-Kennedy
  - Andrea Piccinelli
  - Marco Mascheroni
  - Francesco Brivio
topics:
  - DiracX schema versioning and Alembic
  - ADR (Architecture Design Review) documents and review planning
  - DIRAC/DiracX backlog grooming and story-point estimation process
  - Ticket assignment and CMS priorities for DIRAC/DiracX contributions
  - CMS housekeeping of functionality to bring into the DiracX ecosystem
---

# WM Dev Team Weekly: DiracX Ticket Prioritization and ADR Review Planning

## Summary

This transcript begins mid-conversation (the recording/caption file starts at 15:23, a couple of minutes before the folder's nominal start time), continuing a discussion about whether the [[DIRACX]] database schema is flexible enough for CMS use cases, since the schema is currently embedded directly in code. The meeting then moved to a recap of a recent DIRAC/DiracX backlog-grooming session (planning poker for story points) and a broader, largely unresolved discussion about how the CMS group should decide which DIRAC/DiracX tickets to pick up, given CMS-specific priorities. The group also discussed the schedule and process for reviewing the DIRAC/DiracX team's upcoming Architecture Design Review (ADR) documents, and considered CMS-side "housekeeping" work — reviewing which existing CMS/[[Submission Infrastructure]] functionality (e.g. [[glideinWMS]]-related runtime code, job splitting) will need to become plugins/extensions in the DiracX ecosystem, independent of the DIRAC team's own timeline.

## Decisions / Conclusions

- No formal decisions were recorded in this transcript; the meeting was primarily exploratory/process discussion. The items below are conclusions or shared understanding reached during discussion, not new decisions on scope of work.
- Valentin Y Kuznetsov's underlying concern: the DiracX schema is bound directly in code (no separate schema layer), so if the schema proves insufficient for CMS use cases, changing it requires code changes to already-existing objects. It remained unclear during the discussion how such schema evaluation/changes would be handled going forward.
- Alan Malta Rodrigues noted that the DIRAC/DiracX team has reportedly begun considering **Alembic**, a Python library used for database migrations, to help version schemas and keep them consistent across upgrades. This addresses schema *migration* tooling, not the separate question Valentin raised about whether the current schema is adequate for CMS needs.
- The DIRAC/DiracX team's ADR documents were said to be scheduled for release "this summer," but Alan Malta Rodrigues assessed that, in practice, they likely would not appear before at least mid-August, due to vacation time affecting part of the team. It was separately noted (Francesco Brivio) that Federico (described as the DIRAC/DiracX product manager) was already on vacation at the time of this meeting.
- Liz Sexton-Kennedy stated it would be useful to plan on being in a position to negotiate/discuss architecture decisions with the DIRAC/DiracX decision-makers at the end of August, once Federico returns.
- Recap of a recent backlog-grooming/planning-poker session: Marco Mascheroni described initially voting a high story-point estimate (5) on a ticket about renaming something in the codebase, because as a newcomer it would have required significant ramp-up (including, he believed, installing part of DIRAC). After discussion in that meeting revealed the change was a simple one-line fix, he revised his estimate. Alan Malta Rodrigues characterized this not as a "disagreement" but as the intended process: the scrum master (named as Alexander) averages story-point votes across participants and specifically follows up with outlier voters to understand their reasoning, sometimes prompting a live look at the code before re-voting.
- Marco Mascheroni raised a concern about this grooming format: because only a limited number of tickets can be discussed and voted on within the allotted hour, the process may not scale well if there are many participants, though he was unsure and suggested this remains to be seen.
- CMS priorities relevant to DIRAC/DiracX ticket selection, as reported by Liz Sexton-Kennedy from a prior CMS management/face-to-face meeting: (1) accelerating the community's (and LHCb's) move to DiracX by removing dependencies on DIRAC components, so as to avoid a long-term hybrid DIRAC/DiracX system; (2) [[glideinWMS]] integration with DiracX. Liz noted it is often not obvious to someone without detailed knowledge whether a given ticket advances either priority, and that developers close to the code (e.g. Alan or other developers) would need to help assess this.
- Discussing a specific example, Liz suggested a "TS Catalog Client"-type ticket would likely not be an appropriate CMS pick, since CMS has its own catalog and intends to use [[Rucio]] for placement/location cataloging rather than adopt a different catalog client.
- Clarification of the DIRAC/DiracX backlog/sprint mechanics: tickets marked "needs triage" have no assigned story points and cannot be picked up until they are discussed/estimated (they must go through the same grooming/estimation process) and placed in the backlog. Once the current sprint finishes, backlog tickets become available; when a new sprint starts, team members reportedly have roughly 24 hours to pick tickets from the current sprint before others do. Alan Malta Rodrigues corrected an earlier assumption in the discussion (also acknowledged by Marco) that tickets could be freely taken from the backlog at any time — in practice, new items only enter the backlog once triaged together as a group.
- Andrea Piccinelli described the DIRAC-side process from their team's perspective: at the end of a sprint, the team decides which issues to bring into the backlog for the next sprint, and this is the point at which participants can propose issues they're interested in.
- Andrea Piccinelli raised an open point about the policy for CMS creating new tickets related to "transformation and production" (exact scope unclear in the transcript), noting this would need to be discussed with the DIRAC/DiracX team, particularly regarding timing of when such tickets could be raised.
- Regarding the six ADR documents: Alan Malta Rodrigues stated they will be published as GitHub pull requests once released by the core team, after which the community can review and comment, with some review time given before merging. He said he had not received (and did not expect to receive) draft copies ahead of the public release.
- There was discussion, without a firm final decision, about how the group should divide the work of reading the six ADR documents. Valentin Y Kuznetsov proposed assigning documents by individual expertise/area rather than everyone reading all six, to make better use of limited time. Alan Malta Rodrigues felt it was important that everyone go through the documents (or at minimum that some read them in detail and present a summary to the rest). Liz Sexton-Kennedy proposed that, during team meetings, one person volunteers to read a given ADR in detail and then present a summary and gather group opinions, in order to help decide what CMS feedback to send back to the DIRAC team. Andrea Piccinelli mentioned he, Valentin, and Alan would likely be involved in this document review.
- Alan Malta Rodrigues proposed that CMS does not need to wait for the DIRAC/(unclear: transcribed as "ALHCP")/LHCb team's own timeline to begin "housekeeping": reviewing which CMS/Submission Infrastructure functionality needs to be brought into the DiracX ecosystem (not by copying code, but by re-evaluating it in the context of DIRAC as an ecosystem). Examples raised: the runtime/job-wrapper code that runs on grid worker nodes (covering user analysis, central production, and Tier-0 use cases), and job-splitting algorithms. Liz Sexton-Kennedy agreed, framing this as identifying which current CMS-specific functionality will need to become "plugins"/"extensions" in DiracX's plugin/extension system.
- Andrea Piccinelli asked whether a similar review exercise should be done for other components, mentioning [[Rucio]]. Liz Sexton-Kennedy distinguished two different scopes: (a) understanding how much of Rucio's cataloging functionality DIRAC already uses, to know what CMS would still need to add — which she considered reasonable to look into; versus (b) CMS's more advanced use of Rucio, such as locking datasets and releasing them as part of workflow chains — which she said should not be tackled yet, since it requires first aligning with the DIRAC team on how the workflow itself should run.

## Action Items

- [ ] Share references/links to the (existing and upcoming) ADR documents with the group — Andrea Piccinelli (requested by Valentin Y Kuznetsov; Andrea's response was affirmative but the specifics were unclear in the transcript).

## Discussion

### DiracX schema flexibility and Alembic
Valentin Y Kuznetsov raised a concern that because the DiracX schema is defined directly in code, evaluating whether it meets CMS requirements and then changing it if it doesn't would require code modifications to already-existing objects, and he was unsure how the DIRAC/DiracX team plans to handle this. Alan Malta Rodrigues noted the team has started considering Alembic for schema versioning/migrations, though he had not used it himself and acknowledged this addresses migration tracking rather than the adequacy of the schema itself. Alan suggested this would likely become clearer once the ADR documents are available.

### Backlog grooming recap and estimation process
In response to a question from Liz Sexton-Kennedy about a reported disagreement over a story-point estimate, Marco Mascheroni and Alan Malta Rodrigues described the planning-poker-style estimation process used in DIRAC/DiracX grooming meetings, including how the scrum master (Alexander) averages votes and probes outliers for their reasoning. Marco raised a scalability concern about the one-hour time limit constraining how many tickets can be discussed with many participants.

### Ticket selection and CMS priorities
Valentin Y Kuznetsov raised repeated, still partly unresolved questions about how the CMS group should decide which DIRAC/DiracX tickets to work on, how personal interest expressed in an earlier meeting relates to actual ticket assignment, and how CMS priorities should factor into this. Liz Sexton-Kennedy summarized the two CMS priorities set at a prior management/face-to-face meeting (accelerating the DiracX transition, and glideinWMS integration) but acknowledged it is not always obvious from a ticket description whether it serves those priorities. Valentin proposed spending time in a future meeting walking through the DIRAC ticket board as a group to jointly identify candidate tickets aligned with CMS priorities. Marco Mascheroni and Alan Malta Rodrigues clarified backlog/sprint mechanics (needs-triage tickets have no story points and require group estimation before being picked up; a ~24-hour window exists at the start of a new sprint to claim tickets).

### ADR review planning and CMS "housekeeping"
The group discussed the practicalities of the six upcoming ADR documents (their expected release as GitHub PRs, no drafts being shared in advance) and how the team should divide the work of reading and providing feedback on them, converging loosely around Liz Sexton-Kennedy's proposal of a rotating volunteer summarizing one ADR per meeting. Separately, Alan Malta Rodrigues proposed that CMS start reviewing, independent of the DIRAC team's own schedule, which existing CMS functionality (e.g. glideinWMS-related grid-node runtime code, job splitting algorithms) will need to be adapted into DiracX plugins/extensions. Liz Sexton-Kennedy agreed and extended the question to Rucio usage, distinguishing basic cataloging reuse (worth investigating now) from CMS's more advanced Rucio-based workflow use cases (considered premature until aligned with the DIRAC team).

## Open Questions

- How will the DIRAC/DiracX team evaluate and, if needed, change the schema if it turns out not to be sufficient for CMS use cases, given the schema is embedded in code?
- How exactly should CMS ticket assignment work — how should personal interest, CMS priorities, and DIRAC/DiracX team priorities be weighed and reconciled? This was raised repeatedly by Valentin Y Kuznetsov and was not resolved in this meeting.
- What is the exact scope of the "transformation and production" ticket-creation policy question raised by Andrea Piccinelli, and how/when should this be discussed with the DIRAC/DiracX team?
- How should the group best divide effort in reading and providing feedback on the six ADR documents (individual expertise-based assignment vs. everyone reading everything vs. rotating summaries)? No firm approach was settled on.
- Does an existing S3-related or otherwise adjacent component still depend on older cataloging behavior, and how much of Rucio's cataloging functionality does DIRAC already use versus what CMS would still need to add? (Raised but not resolved.)
- The identity of the group(s)/team referenced by Alan Malta Rodrigues as needing to be waited on (transcribed unclearly as "ALHCP") is uncertain.

## Related

[[DIRAC]] · [[DIRACX]] · [[glideinWMS]] · [[Rucio]] · [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-16 15.25.49 New WM Dev team weekly meeting`)
