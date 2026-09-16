---
type: meeting
date: 2026-07-07
participants:
  - Thomas Kello (transcribed as "tkello")
  - Jan Krzysztof Chyczynski
  - Antonio
  - Alan Malta Rodrigues
  - Andrea Piccinelli
  - Liz Sexton-Kennedy
  - Francesco Brivio
  - Marco Mascheroni
topics:
  - CMS DPG/calibration Automation Framework (PCL, Multi-Run Harvester, offline Automation Framework, manual workflows)
  - New Workload Management System (WMS) based on DIRAC/DiracX
  - Feasibility of the new WMS as an orchestrator for calibration workflows
  - Common Workflow Language (CWL) as candidate common description language
  - NGT (next-generation trigger) calibration requirements at P5
  - Latency and data-volume constraints on where workflows must run
  - Requirements for a future common automation tool
---

# Automation + WMS Meeting

## Summary

This was a first "touch ground" meeting between the CMS DPG/calibration Automation team (Thomas Kello, Jan Krzysztof Chyczynski, Antonio, Francesco Brivio) and members of the Workload Management (WM) team working on the new DIRAC/DiracX-based Workload Management System (WMS) (Andrea Piccinelli, Liz Sexton-Kennedy, Alan Malta Rodrigues, Marco Mascheroni). The Automation side is designing a common framework and tool to unify the various calibration workflow families used during Run 3 — the Prompt Calibration Loop (PCL), the Multi-Run Harvester, and the (offline) Automation Framework (AutoF) — plus currently-manual DPG workflows, into a single, flexible, user-friendly system for Run 4 and beyond, and wanted to understand whether the new WMS could serve as (one of) the orchestrator(s) for this. The WM side, in turn, explained the motivation, scope, and design of the new WMS effort (built around DIRAC/DiracX, aiming to retain HTCondor/GlideinWMS as the grid-submission layer, and adopting the Common Workflow Language, CWL). No architectural decision was reached; both sides agreed this is an early, exploratory discussion to share plans, identify overlaps, and inform each other's designs going forward.

## Decisions / Conclusions

- No commitment or architectural decision was made on whether the new WMS will serve as the orchestrator for the DPG/calibration Automation Framework. This was explicitly framed as an early exploratory discussion.
- Thomas Kello stated the Automation team's near-term focus/plan is to prioritize a common solution for the main Run 3 calibration workflows (PCL, Multi-Run Harvester, AutoF) first, rather than trying to simultaneously accommodate all requirements (including NGT) from the start; NGT integration should be kept in mind but is not the immediate starting point.
- The current standing PCL-like workflows at Tier 0 are expected to continue running largely as they do now under the WM group's Tier 0/central production plans, which are being designed to comply with CWL-based principles.
- The WM group's stated goal/milestone (Andrea Piccinelli) is for the DIRAC-based system to first be able to reproduce what CRAB currently provides for private/distributed analysis workflows; only after that milestone is reached would there be a stronger basis for evaluating whether it could also support the Automation team's calibration-workflow use case.
- Liz Sexton-Kennedy confirmed that the new WMS is intended to be able to handle any workflow describable via CWL-style diagrams, with DIRAC (via DiracX) responsible for implementing/materializing those workflow descriptions and interfacing with Rucio for data management, while the underlying grid-submission mechanism (GlideinWMS/HTCondor, i.e. "Condor-G"/grid universe) is retained largely as-is.
- NGT's optimal-calibration workflows are, per Jan Krzysztof Chyczynski, being considered separately/in parallel, with a goal of potentially sharing the same workflow orchestration engine and configuration language, but NGT wants to avoid dependencies on external/third-party services outside of P5 (e.g. Run Registry) and may need a standalone orchestrator for jobs that must run directly on bare P5 worker nodes.

## Action Items

None identified.

## Discussion

### Background and framing (Automation side)
Thomas Kello (transcribed as "tkello") opened by explaining the Automation team's goal: to place all CMS calibration workflows — those that existed during Run 3, plus any arising from the next-generation trigger (NGT) — "under one roof" with a common configuration, common infrastructure, and a user-friendly way to define workflow inputs/outputs/dependencies. He stressed the new tool needs to be very flexible, support monitoring, and possibly manual triggering, via a user interface. He described Run 3's calibration workflow "zoology":
- **Prompt Calibration Loop (PCL)** — runs on the express stream; a two-step workflow. AlCaRecos are merged into calibration-relevant objects, split by conditions granularity, producing an "AlCaPrompt" special dataset used as input to a harvesting step; conditions are derived by a harvesting job. Orchestration historically ran from the Tier-0 feeder daemon (checking for express streams), packaging the WMCore software and CMSSW workflow info, sent to the worker job; communication between the Tier-0 feeder and WMCore was via an Oracle database. Final conditions are uploaded to the Conditions DB.
- **Multi-Run Harvester** — enters at the harvesting step, taking AlCaPrompt as input and providing a "final feed" over multiple runs (hence the name). Orchestration relies on third-party tools (Run Registry API, DBS API, etc.); monitoring via a Jenkins interface. Described as similar to the (offline) Automation Framework.
- **(Offline) Automation Framework (AutoF)** — described as the most flexible of the Run 3 workflows since it does not depend on a fixed input (can process express streams, prompt datasets, ReReco, and Monte Carlo). Supports arbitrarily complex dependency graphs ("a spider of dependencies"), not just two-step. Outputs can be database conditions (requiring human sign-off to deploy) or other artifacts such as plots. Orchestration was done via a tool referred to as "run control"/automation tool, using InfluxDB (soon migrating to TimescaleDB) for job/status communication, triggered by Jenkins. Jenkins losing support was cited as one motivation for building a new Automation Framework.
- **Manual workflows** — currently manual DPG workflows that are expected to become PCL-like, Multi-Run-Harvester-like, or AutoF-like as they get automated for Run 4; Thomas noted the overall scale/number of workflows needing automation is a critical factor for Run 4.

Jan Krzysztof Chyczynski added that one Automation team goal is to avoid depending on further custom/bespoke frameworks like AutoF, and instead adopt a state-of-the-art workflow orchestration engine, adding a layer for things not typically provided out of the box (e.g. grouping workflow execution by run/luminosity-section thresholds, standard data source/dataset handling). He noted the team had not looked much into CWL specifically, but had considered Airflow and Luigi as candidate orchestration engines.

### Clarifying questions on current Run 3 workflows
Alan Malta Rodrigues asked which of the four workflow families run within the Tier-0 machinery, and how conditions get uploaded to the database. Antonio and Thomas Kello clarified: PCL is the one that currently runs within/under WMCore's system at Tier 0; conditions are uploaded to the database by a component running inside the agent (on the VM where the agent runs), not from worker nodes. The Automation Framework can run on LXPLUS nodes or wherever accessible via HTCondor submission; Multi-Run Harvester is similar.

### Is a general/common workflow-orchestration approach appropriate? (CWL discussion)
Liz Sexton-Kennedy observed that what was described looks like general workflow management and asked whether the Automation team had considered the Common Workflow Language (CWL), noting PCL dates back to Run 1 (~2010) while Multi-Run Harvester and AutoF are more recent, organic developments. She asked whether they'd consider using a more general workflow management system. Thomas Kello confirmed this is exactly the kind of thing they want to discuss, and that the new WMS could be one candidate orchestrator. Andrea Piccinelli clarified the WM group is building the new WMS "basically from scratch," rather than incrementally improving WMCore — informed by lessons learned from WMCore's issues, not a code-level rewrite of it.

Liz Sexton-Kennedy explained her view of the new WMS's design: CWL-style diagrams describing a workflow would be materialized into HTCondor jobs — this "translation" from a common workflow description into concrete jobs is one of the central things the new WMS is meant to handle, and this should work "anywhere" (thanks to GlideinWMS abstracting grid interfaces). She noted GlideinWMS/HTCondor is sufficient for resources like LXPLUS ("Alex Plus" in transcript, likely LXPLUS), but a broader WMS (like DIRAC/DiracX) is needed once other types of computing elements across the wider grid are involved.

### Where should workflows run? (latency and data volume)
Antonio raised the question of whether using the new WMS would be "overkill" for calibration workflows that mostly need to run at one site (Tier 0 / CERN, or P5 for NGT), given the new WMS's design goal of scheduling workflows anywhere on the grid.

Liz Sexton-Kennedy responded that the actual determining factors for where a workflow must run are latency requirements and data volume, not just DPG/subsystem preference:
- NGT's optimal-calibration latency requirements are expected to be extremely tight (calculate and apply corrections after a small number of luminosity sections), likely requiring this to be handled as part of the HLT's own workflow system.
- Tier 0 hosts many workflows because raw data and AOD output are very large and can only be retained briefly (worse in Run 4); results must be compacted/calculated/stored quickly.
- Workflows with small inputs (e.g. computable from MiniAOD, or from n-tuples/histograms as in Multi-Run Harvester) could in principle run anywhere.
- She characterized these placement decisions as largely static (decidable up front, expected to hold for most of Run 4 and Run 5, similar to how earlier decisions lasted ~10 years), not something requiring dynamic analysis.

Francesco Brivio noted that none of the workflows shown in the slides are as latency-constrained as Liz's HLT/5-lumisection example — PCL has a 48-hour window, Multi-Run Harvester and AutoF run on even longer timescales, and NGT calibration is planned to buffer data for 12 hours — so, in his view, all of these could potentially fit within the new WMS if it is flexible enough, provided everything is described in a common language ("harmonized," running on the same core backend/infrastructure). Liz agreed she sees a lot of potential here.

Jan Krzysztof Chyczynski asked whether the new WMS would only target HTCondor-based execution. Liz clarified that to the extent GlideinWMS hides grid interfaces, workflows could run anywhere; HTCondor was mentioned because most current resources (e.g. she referenced "Alex Plus," likely LXPLUS) use it, but a broader WMS is needed once other computing-element types are involved.

### NGT (next-generation trigger) requirements
Jan Krzysztof Chyczynski explained the team is in direct contact with the NGT group; NGT's general requirements appear to overlap strongly with the Automation team's, and ideally the same common configuration approach could extend to NGT's "optimal calibrations." Thomas Kello summarized NGT's key constraint: everything must run at P5, with no dependency on third-party/external services (e.g. Run Registry) as part of the orchestration.

Andrea Piccinelli asked whether NGT currently runs jobs directly on bare machines at P5 (rather than via any batch/condor system); Thomas confirmed this is plausible but uncertain ("I don't know" whether a local HTCondor solution there would be possible), and that NGT is asking for a standalone orchestrator able to handle their specific problem.

Liz Sexton-Kennedy gave historical context: the Run 1→Run 2 transition moved HLT data flow to a file-system-based approach (event builder writes files, HLT nodes process and write to Lustre storage), which is simple and largely data-driven/polling-based rather than requiring an HTCondor-like scheduler; she expects NGT's Run 4 workflow to remain similarly simple (discover files, process, forward), though she is not fully informed of NGT's plans and speculated they may have more complex requirements (e.g. synchronization points if waiting on calibrations computed inside the HLT nodes themselves). Jan Krzysztof Chyczynski confirmed NGT is indeed considering more complex orchestration solutions for optimal calibrations specifically, with a goal of using the same workflow orchestration engine and configuration language as the main effort ("bringing PCL[-like solution] to NGT").

Thomas Kello said the Automation team's priority is to focus first on the main Run 3 calibration workflows, and only subsequently consider NGT integration; trying to satisfy all requirements (including NGT's) simultaneously from the start was described as not a good starting point, though he did not rule out an early prototype for NGT either.

### Requirements for the new Automation tool
Thomas Kello summarized the requirements the new common Automation tool needs to satisfy:
- Access to datasets wherever stored, and (optionally/likely mandatory) access to metadata tools such as DBS.
- Support for conditions granularity down to (in some cases) the luminosity-section level, as well as coarser granularity (whole runs, full eras).
- Access to conditions stored in the Conditions DB.
- Support for conditional triggering at two levels: (1) within a workflow, ordering/dependency logic between its internal stages; (2) between workflows, e.g. one workflow's conditions (for the tracker) gating another (e.g. ECAL) once a reload of data with tracker conditions has happened — this should be supported by default.
- Flexible outputs: conditions may be stored locally, uploaded directly to a database, or produced as datasets or monitoring plots; local files may need to be passed between workflows running on different worker nodes, which was noted as potentially difficult.
- Transparent orchestration with variable job destinations/resource assignment — DIRAC was again raised as a possible mechanism for this; most current workflows use CAF resources.
- Conditional job submission.
- Robustness: resubmission logic backed by a database tracking job status.
- Monitoring and a user interface.

### WM group's perspective and current WMS design (Liz Sexton-Kennedy, Andrea Piccinelli)
Andrea Piccinelli noted that, at a high level, the Automation team's described complexity resembles what CRAB already provides in terms of flexibility, and suggested this warrants further discussion within the WM group. He stated the WM group's principal target/goal is for the DIRAC-based system to first support what CRAB currently does for private/distributed analysis workflows; once that milestone is reached, there would be a stronger basis for evaluating whether the same system could also support calibration-workflow use cases like the Automation team's — but this was explicitly framed as a preliminary idea, not a commitment ("don't rely on that too much").

At Jan Krzysztof Chyczynski's request, Liz Sexton-Kennedy explained the motivation and design of the new WMS:
- The main motivation on the offline side is long-term sustainability out to (at least) Run 4 (she said "out to 204," likely referring to a run/year figure that was garbled in the transcript). Increased manpower during the upgrade period allows rethinking systems that are 20 years old and increasingly brittle (e.g. CouchDB), which are not expected to remain viable for another 15 years.
- Another sustainability driver is moving toward common/shared solutions where possible, which motivated adopting DIRAC, and specifically DiracX (a from-scratch re-engineering of DIRAC, not a like-for-like port) because its proponents share the same sustainability goals and are willing to help retain CMS-specific strengths, notably the GlideinWMS/HTCondor interface to grid systems — identified by an external review committee as a CMS strength worth preserving. The WM group held a workshop with the DIRAC team, who agreed to prioritize the work items CMS needs most urgently.
- Adoption of CWL was cited as consistent with this "use common things wherever possible" philosophy; CWL is already used by multiple experiments, and (per discussion at HTCondor Week) experiments such as IceCube have been pushing the HTCondor team to support CWL as a first-class interface to HTCondor.
- In response to Jan Krzysztof Chyczynski's question about DIRAC's specific role: DIRAC (via DiracX) would provide the transformation service that takes a workflow description (CWL-style diagrams) and interfaces with the Rucio data-management system to ensure data availability. DIRAC also has existing support for private Monte Carlo production (using a Git-based specification of job sets and technical requirements/validation, comparable in spirit to how CMS IBs validate jobs) — Liz noted the WM group "may or may not adopt" this front-end piece of DIRAC, pending a feasibility assessment. The back-end (materializing workflow descriptions into grid jobs) is intended to continue using GlideinWMS/HTCondor largely as today.
- The overall aim is for DIRAC to become the production system for all CMS Monte Carlo generation and data reprocessing, and to also take over CRAB's current responsibilities.

## Open Questions

- Whether/how the new DIRAC/DiracX-based WMS could serve as an orchestrator for the unified calibration Automation Framework — left as an open, exploratory question; both teams agreed to continue the conversation, with the WM group planning to reach its CRAB-parity milestone first before assessing this further.
- Whether the Automation team should collect statistics from all CMS DPG/subsystem calibration workflows to share with the WM group (Thomas Kello raised this as a question for the WM side, to be revisited once feedback is gathered from all CMS subsystems).
- Whether a local HTCondor-based solution would be feasible for NGT's P5-based jobs, or whether NGT will require a fully standalone orchestrator independent of any external services — unresolved; Thomas Kello was uncertain ("I don't know").
- Whether NGT will need more complex orchestration (e.g. synchronization points to wait on calibrations computed within the HLT nodes themselves) — Jan Krzysztof Chyczynski confirmed NGT is considering more complex solutions for optimal calibrations specifically, but details were not discussed.
- Whether/how local output files could be passed between workflow stages running on different worker nodes — flagged by Thomas Kello as a potentially difficult requirement, not resolved.
- Whether DIRAC's front-end tooling for private Monte Carlo (Git-based job specification, technical validation) will be adopted by the new WMS — described by Liz Sexton-Kennedy as still subject to a feasibility assessment.

## Related

[[DIRAC]] · [[DIRACX]] · [[WMCore]] · [[CRAB]] · [[HTCondor]] · [[glideinWMS]] · [[Rucio]] · [[CMS]] · [[Workload Management]] · [[Workload Management System]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-07 16.02.38 Automation + WMS Meeting`)
