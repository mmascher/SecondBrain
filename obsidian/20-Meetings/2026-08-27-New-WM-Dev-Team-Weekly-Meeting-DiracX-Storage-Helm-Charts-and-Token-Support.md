---
type: meeting
date: 2026-08-27
participants:
  - Andrea Piccinelli
  - Kevin Lannon
  - Valentin Kuznetsov
  - Marco Mascheroni
  - Stephan Lammel
  - Alan
  - Camille/Kamil
  - Francesco
topics:
  - DIRAC Ops meeting report: community requirements feedback and ADR timeline
  - DiracX S3 storage choice (SeaweedFS) and optional-vs-mandatory component design
  - DiracX Helm chart compatibility issues and shared test18 Kubernetes deployment
  - WMAgent token/CVMFS crash issue and PnR CI/CD prioritization
  - Individual status reports
---

# New WM Dev Team Weekly Meeting: DiracX Storage, Helm Charts, and Token Support

## Summary

This transcript is a later segment of the New WM Dev Team weekly meeting held on 2026-08-27 (a separate meeting note, sourced from an earlier-starting recording of the same date, covers the opening roundtable/news portion of this meeting). Much of this segment's content is attributed to the shared room/connection label `[EP 40/R-C10]` rather than to individually diarized speakers; based on content and role (reporting on the DIRAC Ops meeting, moderating the discussion and the individual status roundtable), this appears to be primarily Andrea Piccinelli, though the label may represent a room with multiple participants rather than a single speaker. Individual status updates later in the segment are introduced by name (Alan, Camille/Kamil, Francesco) even though recorded under the same shared label.

Kevin Lannon opened by raising, as a recurring topic, the question of the timeline for a standalone DiracX with a minimum viable feature set — noted as something that should always be on the agenda for relevant workshops. The meeting lead indicated this would be discussed, and mentioned that someone (name transcribed unclearly, rendered as "Lease") will give a talk on the DiracX roadmap the following week.

The lead then reported back from a recent DIRAC "Ops" meeting (which appears to correspond to the DIRAC Ops meeting held the same day per a separate meeting note). Topics from that meeting included a round-table on community feedback and requirements for DiracX — several communities are interested and some are already using DiracX (transcribed unclearly as "galatex") in integration environments; a summary of common requirements across communities will be incorporated incrementally into forthcoming architecture decision records (ADRs), which will define the final shape of those documents.

A significant portion of the discussion concerned DiracX's use of S3-compatible storage (currently implemented via SeaweedFS, referred to in the transcript variously as "seaweed"/"seaweeds") for job sandboxes, and whether the choice of storage backend and other optional components (Redis, OpenSearch, S3) can be swapped or disabled without breaking the system. Valentin Kuznetsov raised concerns about whether DiracX's code and Helm charts are sufficiently generic/transparent about which components are optional vs. mandatory, and described concrete difficulties porting the DiracX Helm charts to CMS's Kubernetes storage setup (PVC incompatibility), which required him to fork the charts into his own repository as a stopgap. He raised a broader concern that DIRAC's need to support many optional components for different experiments increases development and maintenance effort and could divert effort away from CMS's specific needs. Marco Mascheroni noted that CRAB already uses S3-compatible object storage for sandboxes, that DiracX likely chose SeaweedFS to support non-CERN experiments without direct access to CERN's S3 service, and expressed hope that CMS could use an existing S3 instance (e.g., at CERN) rather than operating its own S3 server. Kevin Lannon offered a counterpoint, arguing that the flexibility/modularity of a broad community project is a strength worth the extra effort, and encouraged contributing improvements (e.g., more modular/optional Helm chart structure) back to the DIRAC community rather than only consuming it. The lead indicated this would be followed up during the upcoming CMS Offline and Computing week ("C week").

Marco asked Valentin whether he should deploy additional components he needs for his HTCondor submission prototype (scheduler, task workers) directly onto the shared test18 Kubernetes cluster or set up his own separate deployment. Valentin recommended working toward a single shared deployment (test18) that benefits the whole group and CMS, while being open to Marco experimenting independently first; he confirmed it is on his to-do list to propagate his DiracX Helm chart fixes upstream via issues, once compatibility with DIRAC's own deployments elsewhere is confirmed. Marco agreed to push his changes toward test18, and Valentin confirmed Marco could merge his own pull requests directly.

The lead reported that ADRs are expected soon, with an optimistic target of the end of the following week, potentially before the CMS Offline and Computing week.

A separate, extended discussion concerned an issue where the current (frozen) workflow management system — referred to in the transcript as "Mr. W" (likely a mistranscription; the intended system name is unclear) — crashes when a job attempts to use a token, a problem expected to become critical once token-based authentication becomes the default. The lead reported that CMS had asked the PnR team to help test and deliver a fix, but PnR indicated they are currently prioritizing improvements to their CI/CD pipelines and are not available to help. Kevin Lannon questioned this prioritization, noting his understanding that the old WM system was meant to be frozen except for critical patches handled by operations (PnR), specifically so that the small DiracX transition development effort (not yet at its ~4-5 FTE target) would not be pulled back into maintaining the old system. The lead clarified that the CI/CD work was the last open item before CMS handed over "Dublin" (transcription unclear, possibly a mistranscribed project/portal name) development responsibilities to PnR, and explained that PnR's CI/CD pipeline is reportedly non-functional (following a credential leak roughly 1-2 months prior that led to stricter repository policies) to the point that PnR currently cannot even produce a new patch release — meaning a token fix could not be deployed by PnR regardless, until CI/CD is restored. Stephan Lammel proposed that the token enhancement work should not take effort from the DIRAC-based (new) workflow management development team; the old-system maintenance team should first fix CI/CD, and only afterward implement the version-based workflow routing that is a prerequisite for enabling tokens on the old system's agents, calling this a non-urgent, sequential plan. Kevin Lannon agreed, arguing the new WM dev team needs to stay disciplined and resist pulling effort back into maintaining/evolving the frozen old system, even where team members have relevant expertise, in order to avoid missing the DiracX transition target.

The meeting closed with brief individual status updates (since one regular participant, referred to as "Toddler" in the transcript, was on vacation): Alan is preparing slides on job splitting; Camille/Kamil has been working on Marco's HTCondor/DiracX proof-of-concept effort, focused on running a CMS job and delivering output to a CMS site, and may need help from Marco; Francesco had nothing substantive to report; Kevin had nothing to report. Marco Mascheroni reported progress on several pull requests: a fix for the local Pixi-based DiracX development setup (avoiding a failure caused by needing to re-initialize an OIDC/well-known-configuration cache on every submission), a renaming change connected to a three-phase piece of work requiring Helm chart updates, and confirmation that his HTCondor submission prototype now works and has been independently replicated by both Francesco and Camille — all three can run a local DiracX server connected to a grid scheduler to submit jobs, though only submission itself works so far (no output or sandbox handling yet). Marco is now modifying the test18 Helm charts (based on Valentin's earlier copy) to add missing components for HTCondor task monitoring; a follow-up question from the lead about HTCondor-side monitoring work was met with Marco noting a miscommunication, to be resolved offline. Valentin Kuznetsov reported continued work on the Helm charts and, per Marco's request, built a new "CMS web" container image (the DiracX community's base image plus HTCondor Python bindings), uploaded to an image registry (transcribed unclearly as "term registry") since DiracX's own images are only published via GitHub rather than that registry; this image has been deployed to the test18 Kubernetes cluster for Marco's continued testing, as part of an iterative process to identify the pieces CMS needs before working on back-porting changes upstream. The transcript ends mid-sentence at this point.

## Decisions / Conclusions

- The group agreed with Stephan Lammel's proposed sequencing for the token/CI-CD issue: the old-system maintenance team should first restore/fix their CI/CD pipeline, and only then implement the version-based workflow routing needed to enable tokens on the old system's agents; no effort from the DIRAC-based (new) workflow management development team should go toward the old system's CI/CD or general maintenance.
- Marco Mascheroni will push his HTCondor/Helm chart work toward the shared test18 Kubernetes deployment rather than a separate personal deployment, and Valentin Kuznetsov agreed Marco can merge his own pull requests to the shared Helm charts directly.

## Action Items

- [ ] Prepare slides on job splitting — Alan
- [ ] Propagate SeaweedFS/DiracX Helm chart compatibility fixes upstream by opening issues against the DiracX Helm charts, ensuring changes remain optional/non-breaking for other deployments — Valentin Kuznetsov
- [ ] Push HTCondor submission / Helm chart changes toward the shared test18 deployment and merge own pull requests directly — Marco Mascheroni
- [ ] Follow up offline on the miscommunication regarding HTCondor-side monitoring work — Marco Mascheroni

## Discussion

- Kevin Lannon raised, as a recurring topic, the question of the timeline for a standalone DiracX with minimum functionality; the lead noted someone (name unclear, transcribed as "Lease") will give a roadmap talk the following week.
- Report from a recent DIRAC Ops meeting: a round-table gathered feedback/requirements from multiple communities interested in or already using DiracX in integration environments; common requirements will be incorporated incrementally into forthcoming ADRs, which will define their final shape.
- DiracX currently uses S3-compatible storage (SeaweedFS) for job sandboxes, not for physics data storage; there was no particular concern expressed at the Ops meeting about swapping SeaweedFS for another S3-compatible technology.
- The DiracX Helm chart deployment is comprehensive (covering many communities' needs) but individual communities are not required to deploy every component; the group discussed whether documentation should clearly separate mandatory vs. optional components.
- Valentin Kuznetsov raised a concern about whether DiracX's code is generic/agnostic enough that optional components (e.g., a specific storage backend) can be disabled without breaking functionality, and whether this is documented; he emphasized this needs continued attention but is not necessarily a blocking issue.
- Valentin described concrete Helm chart incompatibilities with CMS's Kubernetes storage components (PVCs), requiring him to fork the DiracX Helm charts into his own repository; he raised a broader concern that DIRAC's support for many optional components used by other experiments (Redis, OpenSearch, S3) but not by CMS adds development/maintenance effort that could divert focus from CMS's specific needs.
- Marco Mascheroni noted CRAB already uses S3-compatible object storage for sandboxes; DiracX's choice of SeaweedFS is likely driven by the need to support non-CERN experiments without CERN S3 access; he expressed hope CMS could use an existing (e.g., CERN) S3 instance rather than running its own.
- Kevin Lannon offered a counterpoint favoring the value of a flexible, modular, community-supported system despite higher aggregate effort, and encouraged contributing improvements (e.g., more modular Helm charts) back to the DIRAC community.
- Marco asked Valentin whether to deploy additional components needed for his HTCondor submission prototype directly on the shared test18 cluster or via his own separate deployment; Valentin recommended converging on the shared test18 deployment, while being open to independent experimentation first, and noted his own Helm chart fixes are on his to-do list to upstream via issues.
- ADRs are expected soon, with an optimistic target of end of the following week, possibly before the CMS Offline and Computing week.
- Extended discussion on a token/CVMFS-related crash issue in the current (frozen) workflow management system: PnR is currently prioritizing their own CI/CD pipeline work and is not available to help test/deliver a fix; the issue is not yet critical but will become so once token-based authentication is the default.
- Kevin Lannon questioned PnR's prioritization, referencing an understanding that the old WM system would be frozen except for critical patches handled by operations, specifically to protect the limited DiracX transition development effort (not yet at its ~4–5 FTE target).
- The lead explained that the CI/CD work was the last open item before CMS handed over "Dublin" (transcription unclear) development responsibilities to PnR, and that PnR's pipeline is reportedly non-functional — following a credential leak roughly 1–2 months earlier that led to stricter repository policies — to the point PnR currently cannot produce a new patch release, meaning a token fix could not be deployed regardless until CI/CD is restored.
- Stephan Lammel proposed a sequential plan: old-system team fixes CI/CD first, then implements version-based workflow routing (a prerequisite for token support on old-system agents) as a second step, with no urgency; token work should not take effort from the DIRAC-based dev team.
- Kevin Lannon agreed, emphasizing the need for the new WM dev team to stay disciplined and avoid being pulled back into maintaining/evolving the frozen old system despite relevant expertise, to avoid missing the DiracX transition target.
- Stephan Lammel noted that a clearer view of how much effort could be reduced on old-system maintenance will likely emerge once data management is separated from workload management.
- Individual status reports: Alan preparing job-splitting slides; Camille/Kamil working on Marco's HTCondor/DiracX proof-of-concept effort (running a CMS job and delivering output to a CMS site), possibly needing help; Francesco and Kevin had nothing to report; Marco reported multiple pull requests (local Pixi dev setup fix, a renaming tied to three-phase work requiring Helm chart changes, and a working HTCondor submission prototype independently replicated by Francesco and Camille — submission-only, no output/sandbox handling yet) and is now updating test18 Helm charts for HTCondor task monitoring; Valentin reported building a new "CMS web" container image (DiracX base image plus HTCondor Python bindings), uploaded to an image registry and deployed to test18 for Marco's continued testing, as part of an iterative process toward eventually back-porting CMS-specific changes upstream.

## Open Questions

- Whether DiracX's code and Helm charts are sufficiently generic/transparent to allow optional components (e.g., a given storage backend) to be disabled without breaking functionality was raised as unclear and worth continued attention, not resolved in this segment.
- Whether/how CMS could rely on an existing external S3 instance instead of operating its own S3 server for DiracX was raised as a hope by Marco Mascheroni, not resolved.
- Whether the PnR CI/CD blocker is a hard lock on any progress or something more conditional was raised as a question by the lead, not resolved in the recorded portion.
- The timeline for a standalone DiracX with minimum functionality, raised by Kevin Lannon at the start, was not directly answered in this segment beyond a note that a roadmap talk is planned for the following week.
- The transcript ends mid-sentence during Valentin Kuznetsov's status report; any further content from the remainder of the meeting is not available.

## Related

[[DIRAC]] · [[DIRACX]] · [[HTCondor]] · [[Kubernetes]] · [[CMS]] · [[Workload Management]] · [[CI/CD]] · [[CVMFS]]

## Source

meeting_saved_closed_caption.txt (from `2026-08-27 15.22.09 New WM Dev team weekly meeting`)
