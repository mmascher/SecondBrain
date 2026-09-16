---
type: meeting
date: 2026-07-30
participants:
  - Alan Malta Rodrigues
  - Marco Mascheroni
  - Stephan Lammel
  - Liz Sexton-Kennedy
  - Andrea Piccinelli
  - Valentin Kuznetsov
  - Vijay Chakravarty
  - Camille Mauceri
  - Kevin Lannon
topics:
  - CMS DIRAC / DiracX test deployment status
  - DIRAC/DiracX integration strategy debate
  - DiracX next-steps: job splitting, InterSEED, glideinWMS ecosystem
  - ADR documents timeline and sharing practices
  - DiracX dev meeting recap
  - Team logistics: vacation, CHEP, DiracX Workshop
---

# WM Dev Team Weekly: DiracX/DIRAC Test Deployment and Integration Strategy

## Summary

This CMS WM Dev team weekly meeting covered brief team logistics (vacation tracking, upcoming CHEP and DiracX Workshop events, a project-management update from Liz Sexton-Kennedy), a recap of the DIRAC/DiracX dev meeting, and a status update on candidate next-step development items (job splitting algorithms, [[glideinWMS]] ecosystem evolution, the InterSEED repository). The bulk of the meeting was a discussion, led largely by Valentin Kuznetsov, Alan Malta Rodrigues, and Marco Mascheroni, about the current state of the CMS [[DIRAC]]/[[DIRACX]] test deployment and — more substantively — a still-unresolved debate on integration strategy: whether the group should connect the DIRAC and DiracX test instances now to run early integration tests, or instead prioritize building out DiracX-only functionality first to avoid taking on DIRAC-side technical debt that the upcoming ADR-driven redesign is expected to replace. The meeting ended without the group reaching full alignment on this question.

## Decisions / Conclusions

- No firm decision was reached on the central integration-strategy question (see Discussion below); Alan Malta Rodrigues and Andrea Piccinelli explicitly noted at the end of the meeting that the group was "not on the same page" and agreed to try to converge on this in upcoming meetings.
- Current state of the CMS DIRAC/DiracX test deployment, as described by Valentin Kuznetsov:
  - A dedicated VM ("CMS DIRAC test") runs a DIRAC instance. It can currently only submit jobs via SSH; submitting to an actual CMS site would require additional configuration work.
  - A separate DiracX deployment exists on a Kubernetes cluster via Helm charts (referred to as "CMS DiracX Test18").
  - The two are **not connected**. Connecting them requires configuration-server work that Valentin said requires additional knowledge he does not currently have.
  - Without this connection, DiracX has no functionality beyond its web interface: there is no underlying core system to submit jobs. Marco Mascheroni confirmed he had submitted single jobs directly via the DIRAC client on his own instance, but there is no transformation system, so workflows (as opposed to individual jobs) cannot currently be run or tracked.
- The DiracX configuration format is YAML-based and structurally different from DIRAC's custom format, but per Valentin the current configuration reflects the combined DIRAC+DiracX structure needed for a working system; he does not expect the DiracX configuration-server structure itself to change significantly going forward, since the DIRAC/DiracX team has already settled on it. He said there is little he can contribute upstream to DiracX from this work, since it mainly involves learning/adapting to an already-fixed configuration structure.
- Configuration files for the deployment are kept in a GitLab repository rather than GitHub, because they contain sensitive information (DNS entries, emails, etc.).
- Liz Sexton-Kennedy's view, not contested in the discussion, was that while the deployment remains small-scale, it can continue to run on the shared CMS web Kubernetes cluster; a decision on whether a dedicated/separate cluster is needed can be deferred.
- Recapping an earlier (prior meeting) agreement with Federico (DIRAC/DiracX team) as described by Andrea Piccinelli: the DIRAC/DiracX team would only be asked to test their own stack ("CMS stack"), not a full end-to-end integration test, since CMS's intent is to end up using DiracX only, not a long-term hybrid DIRAC+DiracX system.
- The DiracX dev meeting (recapped by Alan) was short (~30 minutes) and mostly went through the GitHub ticket dashboard for the current sprint; there was limited substantive discussion because several people (including Federico, just back from leave) were on vacation or catching up.

## Action Items

- [ ] Update the documentation for the DIRAC VM / DiracX deployment (gists describing each piece of the setup) — Valentin Kuznetsov.
- [ ] Update the GitLab configuration repository with recent (as of yesterday, relative to the meeting) changes — Valentin Kuznetsov.
- [ ] Email Federico to ask for a conversation about ADR timelines, now that he is back from leave — Liz Sexton-Kennedy.
- [ ] Clone the existing Indico entry (including its room/seat booking, which runs through the end of the year) to reuse the same physical meeting room for the WM Dev team meeting — Alan Malta Rodrigues.

## Discussion

### Team logistics and upcoming events
No major news since the previous week; the group was reminded to keep updating vacation availability in the shared document. Alan Malta Rodrigues said he would be off starting the day after the meeting until the following Wednesday. Liz Sexton-Kennedy noted the team was still missing vacation information from Vijay Chakravarty, who said he did not have immediate plans. Upcoming events mentioned: CHEP ("mid of September", confirmed by Stephan Lammel as the 21st) and the DiracX Workshop in Prague (mid-October). Andrea Piccinelli circulated a summary document from a recent team retreat. Andrea also mentioned an open call for nominations for an unclear item (transcribed as "WM 112 combineries" — likely conveners for an upcoming conference/session, but this is uncertain in the transcript), and noted he has booked a room through the end of the year for people interested in attending in person.

### Project management update
Liz Sexton-Kennedy said she had nothing specific to report this week; she is talking to people to better understand how work items connect and their feasibility, ahead of producing a timeline.

### DiracX dev meeting recap and ADR sharing
Alan Malta Rodrigues recapped a short DiracX dev meeting focused on the GitHub ticket dashboard for the current sprint, with limited discussion since several people were on vacation and Federico had just returned. Liz Sexton-Kennedy asked whether there was a schedule for the ADR documents; Alan said this had not been discussed with Federico yet. Liz reiterated she would like to see the ADRs even in draft/preview form, not just final versions. Andrea Piccinelli suggested a likely reason the DIRAC/DiracX team has not shared drafts: for fairness, any draft shared with CMS would need to be shared with all communities (e.g. LHCb) at the same time, so the team is likely waiting for a first public version. Liz said that, given CMS's larger sudden manpower contribution, she felt CMS should be able to look at drafts early to see how they fit CMS's plans, and said she would email Federico about timelines now that he is back.

### DiracX next-steps items
Marco Mascheroni suggested it was worth discussing progress on already-identified candidate next-step items, since some of this preliminary work will be needed regardless of the ADR outcome:
- **Job splitting algorithms**: Alan Malta Rodrigues is revisiting and refactoring the job-splitting interface to modernize it relative to the existing WMCore/Tier0 implementation, starting with file-based job splitting; details are in his written report, and the work is visible in his repository.
- **CWL-related work**: Vijay Chakravarty and Camille Mauceri are looking into CWL-related items; Alan deferred detail to their own report-section update.
- **glideinWMS ecosystem evolution**: Alan raised the open question of whether the group should invest work (major or minor) in evolving glideinWMS alongside the workload management system, describing this as needing an analysis of the glideinWMS/Submission Infrastructure ecosystem for what he referred to as "REM4" (likely a transcription artifact, possibly intended as "Run 4"; the transcript does not make this certain). Marco Mascheroni agreed some revisiting is possible (e.g. making the frontend more modular, potentially running it inside the DiracX server rather than as a standalone component), but said he would prefer to wait for the ADRs to clarify how DIRAC handles resource provisioning (including whether via RSS) before deciding on integration. He considered this work not a top priority, since the current pilot-provisioning approach works independently of DiracX today, unlike the job-splitting/WMCore-decoupling work, which he considers higher priority.
- **Factory/pilot submission**: Marco mentioned that if the factory team (in a separate meeting) decides to change how pilots are submitted, CMS could potentially help by allocating some FTE, but said it was premature to discuss in detail.
- **InterSEED**: Alan described InterSEED as a repository intended to serve as the interface between compute elements/grid gateways and DIRAC. Marco has been in cross-communication with the HTCondor team to identify commonalities and whether InterSEED's functionality could be leveraged through HTCondor. Based on Federico's comments earlier that day, the DIRAC/DiracX team is reportedly still positive about InterSEED as a standalone project, but Alan cautioned this remains premature to finalize given the holiday period.

### CMS DIRAC/DiracX deployment status and integration strategy debate
Valentin Kuznetsov described the current deployment (see Decisions/Conclusions above) and raised an open question about whether a separate/dedicated Kubernetes cluster is needed for this work going forward, versus continuing to use the shared CMS web cluster, framing this as ultimately a management decision about resource provisioning and ownership.

A substantial debate followed on whether the group should connect DIRAC and DiracX now to run integration tests:
- Andrea Piccinelli recalled that the internal conclusion had been that pursuing full DIRAC+DiracX integration was not seen as a valuable use of effort, given CMS's direction; the exact framing of this point was affected by transcription noise and is not fully clear.
- Valentin Kuznetsov argued that without connecting DIRAC and DiracX, DiracX has no real functionality beyond its web interface, and that connecting them is necessary for any meaningful job-submission integration test or workflow verification.
- Alan Malta Rodrigues initially said that if the deployment is to be used for anything, DIRAC and DiracX should be connected, since a plain DIRAC-only instance offers little value for testing.
- Marco Mascheroni raised a concern that integrating DIRAC components now risks wasted effort, since some of them are expected to be replaced after the ADRs (e.g. the transformation system is expected to be rewritten, and the RSS/resource-provisioning component is expected to be superseded by glideinWMS-based provisioning).
- Valentin disagreed with prioritizing this concern, arguing there is significant value in being able to see DiracX-only code changes reflected in a real deployed instance (a "close the loop" feedback cycle: commit code, build images, observe the change), since currently contributors have no visibility into how their merged pull requests behave once deployed. Marco suggested a local/laptop instance could serve this same feedback purpose without requiring full DIRAC+DiracX cluster integration.
- Camille Mauceri asked Valentin to confirm whether the only barrier to submitting jobs beyond local submission was CMS site configuration within DIRAC; Valentin confirmed this, but said he lacks the DIRAC-specific expertise to configure a site properly. Marco noted that learning DIRAC site configuration would itself be throwaway effort, since CMS does not plan to configure DIRAC sites long-term.
- Liz Sexton-Kennedy raised whether CMS Connect (CMS's existing token-based shell-script submission mechanism to CMS sites) could shortcut this by bypassing DIRAC's site-configuration step while still reaching the same end goal (a workflow executing on a CMS site and returning results). Alan responded that this would require changing DIRAC's current workflow-management/pilot-matchmaking system, and would likely also be throwaway work.
- After further discussion, Alan Malta Rodrigues said it now made more sense to him not to run an integration test today using what he described as "95% DIRAC infrastructure, 5% DiracX," and instead to build up DiracX's own core building blocks first (without carrying DIRAC technical debt, since the DIRAC/DiracX team has indicated DiracX will be substantially different from DIRAC), before integrating to run a simple test workflow. Valentin said he agreed with this direction, clarifying that his own point was narrower: he wants any DiracX-only code change to be visible in the deployed Kubernetes instance, regardless of whether that requires DIRAC integration.
- Alan further clarified that describing the current setup as a "preliminary DIRAC setup" was misleading, since the DiracX-only instance ("Test18") does not rely on DIRAC at all; however, he noted its functionality is still very limited — e.g. it is not yet possible to inject a production/workflow into the system, which is a prerequisite for testing something like job splitting.

The discussion closed without a firm resolution; Alan and Andrea both acknowledged the group was not yet aligned on the integration approach and agreed to continue the discussion in upcoming meetings.

## Open Questions

- Should CMS connect the DIRAC and DiracX test deployments now to enable integration testing, or prioritize building DiracX-only functionality first? Not resolved; explicitly flagged as an area where the group is not yet aligned.
- Will there be a dedicated ADR document covering the configuration system specifically? Raised by Liz Sexton-Kennedy; no one in the meeting knew.
- Is a separate/dedicated Kubernetes cluster needed for the CMS DIRAC/DiracX deployment, and if so, who provisions and manages it? Raised by Valentin Kuznetsov as a management-level decision, not yet addressed.
- Should CMS invest work (and how much) in evolving glideinWMS alongside the new workload management system, and how should pilot/resource provisioning integrate with DiracX once the relevant ADRs (workflow management system, RSS/resource state system) are available?
- Will InterSEED become a standalone project, and if so, how would it relate to HTCondor's own tooling? Still under informal discussion; described as premature to finalize during the holiday period.
- What exactly are the goals and timing for the item referred to as the "CSA team"/"ECSA" (transcription unclear), and how does it affect the group's own next steps?
- What exactly was meant by Andrea Piccinelli's nomination call (transcribed as "WM 112 combineries") — the intended term and scope are unclear in the transcript.

## Related

[[DIRAC]] · [[DIRACX]] · [[glideinWMS]] · [[Kubernetes]] · [[Workload Management]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-30 14.59.29 New WM Dev team weekly meeting`)
