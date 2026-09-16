---
type: meeting
date: 2026-09-01
participants:
  - Marco Mascheroni
  - Liz Sexton-Kennedy
topics:
  - DiracX job-submission proof of concept status update
  - Kubernetes deployment of the DiracX proof of concept (test18, CMS Web)
  - CSA28 staffing/effort chart corrections
  - ADR release status
  - Marco's candidacy for the DMWM L2 convener position
  - Submission Infrastructure convener succession planning
---

# DiracX Proof-of-Concept Update and DMWM Convenership Discussion

## Summary

Marco gave Liz a status update covering three topics: (1) progress on a DiracX job-submission proof of concept, including a Kubernetes deployment effort and contributions from Francesco Brivio and Camille; (2) a correction needed to Liz's CSA28 staffing/effort chart to reflect people currently working on the glideinWMS integration proof of concept; and (3) Marco's interest in applying for the open L2 convener position for what the transcript renders as "MVM"/"DMVM" (this almost certainly refers to DMWM — Data and Workload Management — though the transcript does not clearly spell out the term), which would mean stepping back from the Submission Infrastructure (SI) L2 convenership he has held since 2019.

## Decisions / Conclusions

- Liz will add the person currently working on the glideinWMS integration proof of concept (previously shown at 0% effort on the internal, named staffing chart) as an additional line/person on the anonymized chart she is preparing for a talk. For now she will count people rather than precise FTE fractions, since effort-per-task is not yet well known.
- Liz also needs to correct the chart to reflect Federico's effort (related to ADR work).
- Liz encouraged Marco to go ahead and formally propose himself for the DMWM/"MVM" L2 convener position even before Tulika's final answer arrives, on the grounds that his supervisor (James) has already approved it and the PI's (Tulika's) role is primarily about funding, not about approving personnel moves.
- Liz's current understanding is that Tulika wants the European ("Eurasian" as transcribed) part of the collaboration to provide an L2 for this position, but Liz considers this problematic because no clearly qualified candidate exists there yet. Liz had previously offered to take the role herself only as a fallback if no one else could be found, specifically so she would have a partner to work with rather than running the project alone.
- If Marco moves to the DMWM/"MVM" role, the working assumption discussed was that Francesco Brivio (new, from Milano Bicocca) could take on day-to-day SI convener duties under Marco's continued supervision, with Antonio remaining in his current operational role. Florian was also mentioned as a possible name for a European-based SI role, though there was no decision on this.

## Action Items

- [ ] Tell the person working on the glideinWMS integration proof of concept to message Liz directly about which task they are on, so she can add them to the staffing chart — Marco
- [ ] Move forward with formally proposing himself for the DMWM/"MVM" L2 convener position, pending Tulika's final answer — Marco

## Discussion

### DiracX job-submission proof of concept

Marco described DIRAC's job-submission model: `dirac-job-submit` uses a JDL (job description language) — a different, same-named concept from the [[HTCondor]] JDL. DIRAC plans to move toward [[DIRACX]] and drop the classic DIRAC JDL over time, but DiracX currently has this as more of a demo capability. At a hackathon, a member of the group implemented an executor that runs jobs directly on the DIRAC server, because DiracX does not yet have its own workload management system — DIRAC's stated plan is to eventually support classic DIRAC, DiracX, and [[HTCondor]] submission.

Marco built a proof of concept where a DiracX job is submitted (the job is stored in a database on the server) and then picked up and submitted to a Condor scheduler attached to the global pool. He tested this locally using "Pixie," a DIRAC-team tool that runs a lightweight, mocked-up version of the DiracX server suitable for a laptop. The first prototype took about two days to write. He noted his laptop (16 GB RAM) struggles to run the full (non-lightweight) DiracX stack — it crashes rather than killing the offending process when memory runs out.

Marco worked with Francesco Brivio (Milano Bicocca) and Camille, walking them through running the lightweight version; both have left comments on Marco's GitHub branch. Camille went a step further and ran an actual `cmsRun` job (not a "Hello World") through the proof of concept on the grid, using her own simplified job wrapper (e.g., stage-out copies directly to her own storage rather than going through the full site-local/merge workflow a production job wrapper would need). Marco characterized this as a good, exploratory attitude.

### Kubernetes deployment

Separately, Marco worked with Valentin on deploying the full (non-lightweight) DiracX proof of concept on "test18," a machine on the CMS Web [[Kubernetes]] cluster, using Helm — an area where Marco said he is not an expert and had to learn a lot. The deployment is almost complete; the remaining blocker is figuring out how to deploy an authentication token, which Marco discussed with Valentin that same afternoon. The goal is to have the proof of concept running somewhere public on CMS Web so others can try it.

### ADR status

Marco relayed that, as of the prior Thursday meeting, Federico said several ADRs should be ready and start being released by the end of that week; more detail is expected at the upcoming Thursday meeting.

### Other people's work (as relayed by Marco)

- Alan (name uncertain in transcript) has been working on job splitting (observed via his GitHub repository), writing code that may be reusable later, and has pull requests on what the transcript renders as "search on service" work (reference unclear).
- Marco does not know what one other team member is currently working on and had been unable to get a clear answer from colleagues he asked. He noted that if he takes on the DMWM/"MVM" position, he would need to follow up on this directly.

### DMWM/"MVM" convenership

Marco has been SI L2 convener since 2019 at 25% effort, alongside 50% glideinWMS operations (which he plans to keep, since scale — e.g., for CSA28-related scale testing — falls at the SI layer) and 25% glideinWMS development (currently blurred with his DiracX integration work). He is interested in the open L2 convenership referred to in the transcript as "MVM"/"DMVM" — most likely DMWM (Data and Workload Management) — and proposes shifting his 25% SI portion to that role. He has supervisor approval (Frank, and James as his current supervisor) and has contacted Tulika, still awaiting her final answer; this position was also open a couple of months earlier.

Liz explained her understanding of Tulika's position: Tulika wants a European L2 for this role, which Liz considers a poor fit given the lack of a clearly qualified European candidate. Liz recounted that she previously agreed to take the role herself only if no one else could be found, in order to secure a working partner rather than run the project solo. Liz noted that CMS management ("Marcus," per the transcript) has a pattern of promising positions (e.g., to Florian) and not delivering, which she believes is part of what frustrates Tulika. Liz's overall view was that Marco should propose himself regardless of Tulika's answer, since PI approval is mainly about funding and his supervisor has already approved the move.

Liz reiterated that her role in these status/effort charts is communication — giving visibility into progress toward CSA28 — rather than running the project.

## Open Questions

- Whether Tulika will approve Marco's move to the DMWM/"MVM" L2 convener position.
- Who would take over day-to-day SI convener responsibilities if Marco moves — Francesco Brivio (under Marco's supervision) and Florian were both mentioned as possibilities, but nothing was decided.
- How to deploy the authentication token for the Kubernetes-based DiracX proof-of-concept deployment on test18.
- What one team member (unclear identity in transcript — referenced only informally) is currently working on; several people Marco asked could not answer.
- Exact scope of what "search on service" work (as transcribed) refers to for Alan's pull requests.

## Related

[[DIRAC]] · [[DIRACX]] · [[HTCondor]] · [[glideinWMS]] · [[Kubernetes]] · [[CMS]] · [[Submission Infrastructure]] · [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-01 18.20.39 Marco Mascheroni's Personal Meeting Room`)
