---
type: concept
---

# CMS Adoption of DiracX for Future Workload Management

## Overview

CMS is in the middle of replacing its HL-LHC-era [[Workload Management]] system with one built on [[DIRACX]] (DiracX), the from-scratch re-engineering of the multi-VO [[DIRAC]] framework originated primarily by the LHCb/DIRAC consortium. This is CMS's response to a 2024–2025 review of [[WMAgent]]/WMCore (commissioned by CMS Offline & Computing L1) that concluded the existing system — its core components 15+ years old — is not sustainable for HL-LHC, with knowledge concentrated in too few people and no agreed plan for HL-LHC-era user analysis or user-defined simulation (`WM_Conditions_Workshop_2026.pdf`). The legacy WM system has been frozen since September 2025.

As of the corpus end date (2026-09-16) this is an active, fast-moving transition: the top-level direction (DiracX, not a CMS-built system or PanDA) is decided and stated publicly, but most of the technical architecture connecting DiracX to CMS's existing [[Submission Infrastructure]] is still being designed, gated on Architecture Decision Records (ADRs) from the upstream DIRAC/DiracX team that have repeatedly slipped.

## Current Understanding

### The decision itself

CMS decided to adopt DIRAC, via DiracX, as its future workload-management system. The decision was presented at the March 2026 CMS collaboration (plenary) meeting and reaffirmed in a CMS computing weekly meeting; per Stephan Lammel it was already final by early May 2026, and by late May the CMS-native "fallback" architecture option's internal reservation had been released, "to be revisited only given an insurmountable issue" (`2026-05-29-Submission-Infrastructure-Candidate-Interview-and-DIRAC-Decision-Debrief.md`). A communication gap followed: weeks after the decision, many CMS computing colleagues were unaware it was final, surfacing in CHEP corridor conversations; Stephan Lammel began a standing status page in response, and questions about when it becomes "too late" to fall back were still being raised at CHEP.

The scope of the decision is broad: per Alan Malta Rodrigues's September 2026 presentation, "the future CMS WMS (DiracX-based) has a broader scope, overarching: Tier-0 processing, data reconstruction, MC simulation and distributed user analysis" (`2026-09-09-Conditions-Preparation-Workshop-2026-Validation-Tier0-and-Future-WMS.md`; `WM_Conditions_Workshop_2026.pdf`).

### Decided architectural direction: keep HTCondor/glideinWMS underneath

CMS's stated intent (reaffirmed in presentations and in New WM Dev Team meetings) is to keep its existing [[glideinWMS]]/[[HTCondor]] Submission Infrastructure layer as the resource-acquisition/pilot layer, and integrate DiracX's Transformation System on top of it, rather than adopting DIRAC's own pilot/CE-submission mechanisms. The team explicitly converged on *not* adding direct glideinWMS-DiracX links beyond HTCondor Access Points, to preserve modularity (`2026-07-15-New-WM-Dev-Team-Weekly-Meeting-DiracX-Architecture-Deep-Dive.md`). This alignment was helped by the DIRAC/DiracX core team's own mid-2026 decision to prioritize the transformation/production systems over the WMS layer — an area CMS already covers.

CMS explicitly declined to adopt DIRAC's own reimplementation of HTCondor-style matchmaking when it surfaced in a DIRAC presentation using CMS terminology; SI's matchmaking role stays with HTCondor/glideinWMS (`2026-09-08-Submission-Infrastructure-Weekly-Meeting-Team-Planning-and-Project-Roadmap.md`).

### DiracX as a system, and its relationship to legacy DIRAC

DiracX is described by its developers as a from-scratch rewrite, not a port, of DIRAC (fstagni, `2026-07-14-DiracX-InterSeed-and-HTCondor-Access-Point-Discussion.md`). As of June 2026, DiracX could not function independently — it required a running legacy DIRAC backend for databases, job management, and CE registration; Valentin Kuznetsov, evaluating it hands-on, found it "pluggable" in principle but effectively monolithic in practice, with no written JSON schema for inter-service payloads (`2026-06-24-DiracX-Evaluation-and-WMS-Integration-Planning.md`). DIRAC/DiracX developers who attend CMS meetings represent the whole DIRAC consortium, not LHCb specifically; CMS's sudden, large manpower contribution to the project was noted (Liz Sexton-Kennedy) as disproportionate relative to other VOs.

DiracX's core blocks are the production system, transformation system, workload management system, request management system, data management system, and a Resource Status System (RSS, comparable in role to CMS's CRIC). Six ADR documents were planned by the core DIRAC/DiracX team to formalize the transformation system, WMS extension points, and database-migration approach; they were repeatedly announced as imminent — "this summer," then end of July, then end of August, then mid-September — and had still not landed as of the September 2026 WM retreat planning (`2026-09-16-WM-Retreat-and-DIRAC-Session-Planning.md`). Much of CMS's own architecture work is explicitly gated on these ADRs.

### Prototyping progress

A DIRAC/DiracX hackathon in early July 2026 marked the start of active CMS engagement, followed by a dedicated **New WM Dev Team** (distinct from the operational [[Submission Infrastructure]] team) holding weekly meetings with a sprint cadence alongside the upstream DIRAC/DiracX team. By mid-August 2026, Marco Mascheroni had built a "throwaway" prototype — explicitly built pending the ADRs — that submits DiracX jobs directly to an HTCondor scheduler via a Dirac-JDL-to-Condor-JDL conversion function, bypassing the (not-yet-existent) transformation system; this was independently replicated by Camille Mauceri and Francesco Brivio by late August (submission only, no output/status/sandbox handling yet). By mid-September a Kubernetes-deployed prototype ("Test18") reached a sandbox-upload walkthrough stage (`2026-08-14-DiracX-Interim-HTCondor-Job-Submission-Walkthrough.md`; `2026-09-15-Test18-DiracX-CMS-Prototype-Sandbox-Upload-Walkthrough.md`).

### Timeline

Per the September 2026 workshop materials, the roadmap runs: 2026 (core DiracX contributions) → 2028 (a "CSA28" challenge, goal not yet defined) → feature completion / scale evaluation → 2030 (production). Separately, Alan Malta Rodrigues estimated the DiracX-based system was unlikely to exist in usable form before mid-2027, with the 2028 CSA checkpoint being a partial-capability milestone rather than a full-readiness date. The exact scope of "CSA28" is itself flagged as unclear in the source material. Tier-0 commissioning on the new system is separately targeted to begin in 2029, and Tier-0 operations/development has no dedicated staffing planned from 2027 until at least 2029, since the prior Tier-0 operator was redirected to build the new WMS (Dmytro Kovalskyi, `2026-09-09-Conditions-Preparation-Workshop-2026-Validation-Tier0-and-Future-WMS.md`).

### InterSeed / InterCEde

InterSeed (also transcribed "InterCEde" in some sources) is a DIRAC-side project, led by Alexandre Boyer, rewriting DIRAC's Compute-Element interface layer as small, typed Python protocols with Docker-based integration tests, intended to serve both DIRAC's own pilot factory and direct job pushes to HPC sites with no external connectivity. Whether HTCondor could serve as the backend implementation of the InterCEde abstraction was posed as an open discussion question in CMS presentation material (`Exploring Collaboration Between HTCondor and DiracX-4.pdf`). This idea was discussed in meetings from July through early September 2026 but, per the discovery pass, appears to have been dropped rather than resolved as an active line of work.

## Evolution

- **Dec 2025–Feb 2026**: CMS was still exploring a CMS-built HL-LHC WMS (a "global work queue" with "microagents") as one option among several, alongside evaluating PanDA and DIRAC; no architecture decision had been made (`2025-12-22-HTCondor-and-CMS-WMS-for-HL-LHC.md`, `2026-02-19-CMS-WMS-Architecture-Discussion.md`, `20251216 New CMS WM_ Discussion with HTCondor.pdf`).
- **Spring 2026 CMS Offline & Computing week**: per a later presentation, "consensus emerged" during this event favoring DiracX ("Community solution / Preferred direction") over a revamped CMS-built micro-agent architecture ("Fallback solution") and PanDA ("Evaluated during review / Not actively pursued") (`20260610_Evolving_the_CMS_Submission_Infrastructure.pdf`).
- **~Early May 2026**: the DiracX decision was finalized and presented; the CMS-native fallback option's reservation was released.
- **June 2026**: hands-on evaluation showed DiracX could not yet run standalone.
- **July 2026**: hackathon, formation of the New WM Dev Team, and the DIRAC/DiracX core team's own prioritization shift toward transformation/production systems (away from WMS).
- **Aug–Sept 2026**: first working DiracX-to-HTCondor submission prototypes; Kubernetes deployment and sandbox-upload work; ADRs repeatedly announced as imminent and repeatedly slipping.

## Disagreements and Open Questions

Several of these are still open as of the corpus end date; none have been resolved by this note.

- **Where should CMS's "job materialization" component (translating DiracX task-DB rows into HTCondor jobs) live?** Three options were debated without resolution: as a core DIRAC/DiracX capability (a consortium-wide decision, not CMS's alone), as an extension/plugin of an existing DiracX block (Todor favored a standalone approach as more "sellable" to the consortium but more rigid; Alan Malta Rodrigues leaned toward the WMS block, since it is one of the few actively being designed), or as a fully standalone component on the glideinWMS/HTCondor side (`2026-07-15-New-WM-Dev-Team-Weekly-Meeting-DiracX-Architecture-Deep-Dive.md`). A related process disagreement in the same meeting: Andrea Piccinelli felt CMS lacks the DiracX expertise to responsibly pick a placement before consulting DiracX developers directly, citing a pattern of CMS brainstorming then walking back conclusions; Alan felt CMS should still arrive at its own proposed placement to bring into that conversation.
- **Integration-test strategy — an explicit, named, unresolved disagreement.** At the 2026-07-30 meeting, Valentin Kuznetsov argued for connecting DIRAC and DiracX test deployments now to get fast integration feedback; Alan Malta Rodrigues and Andrea Piccinelli leaned toward building DiracX-only components first to avoid throwaway work on DIRAC pieces the ADRs are expected to replace, a concern Marco Mascheroni shared. The meeting ended with participants explicitly stating they were "not on the same page" (`2026-07-30-WM-Dev-Team-Weekly-DiracX-DIRAC-Deployment-and-Integration-Strategy.md`).
- **Output/metadata registration to [[Rucio]]/DBS: worker-node vs. centralized.** Flagged as a "hot topic" at the July 2026 hackathon; Todor stated he had "no answer" for this "backward path." Valentin Kuznetsov warned against uncontrolled worker-node calls to Rucio/DBS, citing a past DAS-related incident (`2026-07-15-New-WM-Dev-Team-Weekly-Meeting-DiracX-Architecture-Deep-Dive.md`). A related, separate DIRAC-side terminology effort ("direct task" vs. "meta job") was still unfinalized as of `2026-07-17-Rucio-Caching-Meta-Job-Terminology-and-ADR-Recap.md`.
- **Whether HTCondor should back the InterSeed/InterCEde CE-abstraction, or whether DIRAC should build its own** — raised as genuinely open and exploratory in July 2026, with no political mandate either way; historically, DIRAC diverged from HTCondor and built its own pilot ecosystem roughly 20 years ago, and the DiracX rewrite was described as "a natural point to re-ask" that choice.
- **Schema adequacy of DiracX's task/job data model for CMS's needs** is unresolved and distinct from the separate question of migration tooling (Alembic, under consideration by the DIRAC team, addresses migration mechanics, not whether the schema itself is adequate) (`2026-07-16-WM-Dev-Team-Weekly-DiracX-Ticket-Prioritization-and-ADR-Review-Planning.md`).
- **No secrets-management mechanism was observed in the DIRAC framework** for holding credentials needed by DiracX components to contact Rucio/DBS — flagged as a gap by Marco Mascheroni, with no evidence of resolution in later meetings (`2026-07-15-New-WM-Dev-Team-Weekly-Meeting-DiracX-Architecture-Deep-Dive.md`).
- **Storage backend**: a SeaweedFS/Helm-chart incompatibility with CMS's Kubernetes setup forced a fork; a live disagreement exists over whether DIRAC's general-purpose flexibility (supporting many optional storage backends for other VOs) is worth the added burden for CMS, with Kevin Lannon arguing it is (`2026-08-27-New-WM-Dev-Team-Weekly-Meeting-DiracX-Storage-Helm-Charts-and-Token-Support.md`).
- **Bottom-up vs. jointly-negotiated prioritization of CMS's DIRAC/DiracX backlog contributions**: Andrea Piccinelli described DIRAC's process as primarily bottom-up/developer-picked; Liz Sexton-Kennedy argued this cannot work given CMS's need to "catch up," and that prioritization needs to be a negotiated process with the DIRAC/DiracX side. Raised repeatedly without resolution; agreed to revisit once the transformation/production ADR lands.
- **Numerous Tier-0/Conditions-workflow integration questions remain unanswered** (e.g., whether the repack step fits DIRAC's "N files in, N files out" transformation model at all, and how storage-manager back-pressure — which CMS has never previously needed — would be handled), documented extensively in `WM_Conditions_Workshop_2026.pdf` as open questions posed to the Conditions/PPD side, with no dedicated forum yet established to resolve them jointly.

## Relationships

- Depends on, and motivated the creation of, the New WM Dev Team described under [[Submission Infrastructure]] — a distinct organizational grouping from day-to-day SI operations.
- Is explicitly designed to keep [[GlideinWMS Pilot-Based Resource Provisioning]] as the execution/pilot layer underneath DiracX, rather than replacing it.
- Shares an unresolved design tension with the CWL-based workflow-translation prototyping efforts around how CMS's job/workflow definitions map onto DiracX/DIRAC abstractions (not yet a synthesized concept in this vault as of this note).
- Connects to the broader [[CMS CPU and Resource Efficiency]] problem indirectly: DiracX's transformation system is expected to eventually own job/task construction decisions (e.g., StepChain vs. TaskChain) that bear on payload efficiency.

## Sources

- [[2025-12-22-HTCondor-and-CMS-WMS-for-HL-LHC]]
- [[2026-02-19-CMS-WMS-Architecture-Discussion]]
- [[2026-05-29-Submission-Infrastructure-Candidate-Interview-and-DIRAC-Decision-Debrief]]
- [[2026-06-24-DiracX-Evaluation-and-WMS-Integration-Planning]]
- [[2026-07-08-DiracX-InterSeed-HTCondor-GAHP-BLAHP-Discussion]]
- [[2026-07-09-DIRAC-DiracX-Sprint-Review-and-Planning-Meeting]]
- [[2026-07-14-DiracX-InterSeed-and-HTCondor-Access-Point-Discussion]]
- [[2026-07-15-New-WM-Dev-Team-Weekly-Meeting-DiracX-Architecture-Deep-Dive]]
- [[2026-07-16-DIRAC-DiracX-Backlog-Grooming-and-Estimation-Meeting]]
- [[2026-07-16-WM-Dev-Team-Weekly-DiracX-Ticket-Prioritization-and-ADR-Review-Planning]]
- [[2026-07-17-Rucio-Caching-Meta-Job-Terminology-and-ADR-Recap]]
- [[2026-07-23-DIRAC-DiracX-Sprint-Review-and-Retrospective-Meeting]]
- [[2026-07-30-WM-Dev-Team-Weekly-DiracX-DIRAC-Deployment-and-Integration-Strategy]]
- [[2026-08-13-DIRAC-DiracX-In-Progress-Review-and-Backlog-Triage-Meeting]]
- [[2026-08-14-DiracX-Interim-HTCondor-Job-Submission-Walkthrough]]
- [[2026-08-27-New-WM-Dev-Team-Weekly-Meeting-DiracX-Storage-Helm-Charts-and-Token-Support]]
- [[2026-09-01-DiracX-Proof-of-Concept-Update-and-DMWM-Convenership-Discussion]]
- [[2026-09-03-DIRAC-DiracX-Sprint-Review-and-Planning-Meeting]]
- [[2026-09-09-DIRAC-DiracX-Sprint-Review-Meeting]]
- [[2026-09-09-Conditions-Preparation-Workshop-2026-Validation-Tier0-and-Future-WMS]]
- [[2026-09-15-Test18-DiracX-CMS-Prototype-Sandbox-Upload-Walkthrough]]
- [[2026-09-16-WM-Retreat-and-DIRAC-Session-Planning]]
- [[2026-07-13-New-WM-Dev-Team-Weekly-Meeting-Effort-Roundtable-and-Use-Case-Boundaries]]
- [[2026-09-08-Submission-Infrastructure-Weekly-Meeting-Team-Planning-and-Project-Roadmap]]
- `60-Presentations/20251216 New CMS WM_ Discussion with HTCondor.pdf`
- `60-Presentations/Exploring Collaboration Between HTCondor and DiracX-4.pdf`
- `60-Presentations/20260610_Evolving_the_CMS_Submission_Infrastructure.pdf`
- `60-Presentations/WM_Conditions_Workshop_2026.pdf`
