---
type: meeting
date: 2026-07-14
participants:
  - Todd Tannenbaum
  - Marco Mascheroni
  - Alexandre Boyer
  - Jaime Frey
  - fstagni (addressed in the meeting as "Federico"; DIRAC consortium representative — surname not fully confirmed in transcript, likely Federico Stagni)
  - Alan Malta Rodrigues
  - Valentin Kuznetsov
topics:
  - DIRAC/DiracX InterSeed pilot-submission library — build vs. reuse HTCondor
  - HTCondor architecture (Access Point, Central Manager, Execution Point)
  - Grid universe (Condor-G) vs. vanilla universe
  - ClassAds data model and query interface
  - Access Point reliability (in-memory DB + replay/journal log)
  - Pilot monitoring (event log, query interface, no pub/sub)
  - History archive and optional Elasticsearch export
  - GlideinWMS factory scalability
  - ATLAS Harvester/PanDA comparison
  - Access Point deployment (Puppet/yum vs. Kubernetes)
  - Upcoming events — DIRAC Users Workshop, HTCondor Week Europe (Lyon)
---

# DiracX InterSeed and HTCondor Access Point Discussion

## Summary

This was a joint session between the CMS/GlideinWMS/HTCondor side of the Submission Infrastructure meeting and members of the DIRAC/DiracX team (Alexandre Boyer and fstagni, both introduced as attending as DIRAC consortium representatives rather than specifically for LHCb), with HTCondor developers Todd Tannenbaum and Jaime Frey joining to answer technical questions. The context, given by Marco Mascheroni and fstagni: DIRAC (the "legacy" project) is being rewritten from scratch as DiracX. At a hackathon roughly two weeks before this meeting, Alexandre Boyer introduced "InterSeed" (rendered in the transcript variously as "intercede," "inter-CD," and "InterCD"; referred to elsewhere in this knowledge base as InterSeed), a library intended as a common interface for DIRAC's pilot factory/site director to submit pilot jobs, including to HPC sites with no external connectivity. InterSeed is currently only a design-stage "empty shell." Marco has been pushing the DIRAC team to consider whether InterSeed needs to be built from scratch or whether it could instead reuse HTCondor, and fstagni framed this explicitly as an open, exploratory question with no political mandate behind it — it might lead nowhere, or might take several more meetings to resolve. CMS itself has been clear from the start that it intends to stay on HTCondor.

Most of the meeting consisted of Todd Tannenbaum (with Jaime Frey, who had to leave partway through for another commitment) explaining HTCondor's architecture and how it could be used purely as a pilot-submission layer, in response to questions from Alexandre Boyer, fstagni, Alan Malta Rodrigues, and Valentin Kuznetsov, with Marco Mascheroni providing CMS/GlideinWMS-specific context and live examples from `condor_q`. No decision was reached on whether DiracX/InterSeed will build on HTCondor; the meeting closed with a brief, inconclusive discussion of possible next steps, complicated by the DIRAC side heading into a holiday period.

## Decisions / Conclusions

- No decision was made on whether DiracX's InterSeed library will be built from scratch or will reuse HTCondor; this remains an open, exploratory investigation on the DIRAC side, described by fstagni as possibly resolving in a couple more meetings or possibly not going anywhere.
- CMS's existing position (stated as already established, not decided in this meeting) is to remain on HTCondor for pilot submission.
- Alexandre Boyer and fstagni are participating in this discussion as DIRAC consortium representatives, not specifically as LHCb representatives, because DIRAC has many other customers/users besides LHCb whose alignment needs to be considered.
- For the pilot-submission use case DIRAC is interested in, only the HTCondor Access Point component would be needed — not the Central Manager or Condor Execution Points, since DIRAC has its own downstream pilot/worker software.
- ATLAS's pilot system follows a comparable pattern to GlideinWMS/CMS: Harvester is described as ATLAS's equivalent of the GlideinWMS factory, and PanDA is described as the equivalent of the glidein/execution point; both were confirmed to use HTCondor to submit pilots.
- CMS's GlideinWMS factories currently run roughly 40,000 pilots in total, spread across three factories, with no scalability issues observed so far.

## Action Items

None identified.

## Discussion

### Background: DIRAC/DiracX and InterSeed
DIRAC ("legacy" project) is being rewritten from scratch as DiracX; per fstagni, this is a re-engineering effort, not a like-for-like port. At a hackathon roughly two weeks before this meeting, Alexandre Boyer introduced InterSeed as a common interface library for reaching wherever DIRAC's jobs ultimately run. Marco Mascheroni has been pushing the concrete question of whether this needs to be built at all, given that HTCondor already exists. Alexandre Boyer clarified InterSeed is meant to be used both by DIRAC's own pilot factory (site director) and to push jobs into HPC sites with no external connectivity. fstagni noted this reconsideration is notable because DIRAC deviated from HTCondor and built its own ecosystem roughly 20 years ago, and the DiracX rewrite is a natural point to re-ask whether that was still the right call.

### HTCondor architecture overview (Todd Tannenbaum, Jaime Frey)
Todd described three main HTCondor software pieces:
- **Access Point (AP)** — where jobs are submitted.
- **Central Manager (CM)** — matches Execution Points to Access Points (the "matchmaker").
- **Execution Point (EP)** — manages compute nodes (equivalent to a worker node in generic batch/grid terminology, per Jaime Frey).

For DIRAC/InterSeed's pilot-submission use case, only an Access Point would be needed. Without a Central Manager, jobs submitted to that Access Point would need to explicitly specify their destination (e.g., a specific CE or Slurm cluster) rather than being matched automatically.

### Grid universe vs. vanilla universe
Setting `universe = grid` in a job description tells HTCondor not to schedule the job itself, but to delegate submission to another system (a CE, or Slurm via SSH, etc.) and then monitor and report on it — this is the mechanism (also referred to as Condor-G) used for pilot submission, and is what GlideinWMS's factory uses. `universe = vanilla` is HTCondor's traditional batch-scheduling mode, used for payload/user jobs, which are matched by the Central Manager onto Condor Execution Points. Marco confirmed GlideinWMS's factory uses the grid/Condor-G universe to submit pilots to CEs, while regular CMS payload jobs run under the vanilla universe.

There was some back-and-forth attempting to map DIRAC's own concepts (DIRAC's workload management system has two databases, referred to as "jobs" and "pilots") onto HTCondor's model. It was clarified that HTCondor's Access Point database can hold both pilot (grid-universe) and payload (vanilla-universe) jobs together — the two are differentiated by the `universe` attribute and treated differently, not stored in separate systems. Alexandre Boyer proposed, as a possible integration sketch, that DIRAC's pilot factory/site director could submit via Condor-G (acting like DIRAC's pilot database) to a CE, with the resulting worker-node process starting an Execution Point that runs DIRAC-specific logic to contact DIRAC's own matcher and fetch a payload job. fstagni characterized this as "a possibility" and "yet another story" — not a decision.

### Access Point reliability and monitoring
- The Access Point's job database is in-memory, backed by a replay/journal log so that if the Access Point is restarted (including for upgrades), it can reconstruct its in-memory state from the log. Alan Malta Rodrigues noted this feature is already heavily relied on in CMS/GlideinWMS operations (restarts and reconnecting to Condor shadows).
- The Access Point can retry submissions/queries automatically, or delegate retry policy to the submitter; it batches queries to remote CEs/Slurm where possible for efficiency, and can alert when there is trouble communicating with a remote system (per Jaime Frey).
- File staging is supported; streaming stdout/stderr is not supported on essentially any of the remote systems used (staged I/O instead).
- Status/monitoring is pull-based: clients query the Access Point via CLI or Python bindings (with support for constraints and attribute projections), or consume a structured event log the Access Point writes out (e.g., pilot submitted, idle→running, stopped) — either via periodic polling or by tailing the event log file. In response to a question from Valentin Kuznetsov, Todd Tannenbaum confirmed there is **no pub/sub mechanism** for pilot-job events; consumers must either query or tail the file.
- Completed pilots move from an in-memory "active" database to a history archive file; HTCondor can optionally be configured to also push history records into Elasticsearch for longer-term querying.

### ClassAds data model
In response to a question from Valentin Kuznetsov about schema stability across upgrades, Todd Tannenbaum explained that HTCondor's job records ("ClassAds") are semi-structured key-value pairs, not a relational/SQL schema — comparable to a key-value store such as Redis. A typical job has 50–150 attributes. Some attributes are well-defined and documented in the HTCondor manual (e.g., pilot status); others are freely added by whichever software is using the system for its own purposes (GlideinWMS, for example, adds custom attributes such as factory software version, front end, and CMS pilot credential information) and can be queried like any other attribute. Queries use three-value logic (true/false/undefined), including the ability to request a default value when an attribute is undefined. When many jobs are submitted together as one cluster/set (analogous to a Slurm job array), attributes shared across the whole set are deduplicated in memory rather than stored per-job.

### Scalability
Marco Mascheroni reported CMS's GlideinWMS factories currently run about 40,000 pilots in total across three factories with no scalability issues so far, and suggested a scalability test of the factories could be worth doing (not committed to). He noted that running multiple schedulers/shadow processes per machine was a workaround used roughly 15 years ago when Condor was less scalable, which he believes is likely unnecessary today given subsequent HTCondor scalability improvements, though this was not tested in this meeting.

Discussion with Alan Malta Rodrigues clarified that pilot-to-payload granularity is not necessarily one-to-one: a single pilot can run multiple payload jobs concurrently depending on available resources (e.g., a 16-core pilot might run 16 one-core payload jobs at once). Todd Tannenbaum explained that vanilla-job scalability is primarily memory-bound (one shadow process per job), whereas grid/pilot-job scalability is bound differently — a single grid-manager process handles many jobs — with both memory footprint and submission/query rate ("Hertz rate") as limiting factors; per Todd, in CMS and most experiments he is aware of, the Hertz rate of pilot submissions is lower than that of payload jobs, partly because pilot jobs tend to live longer than the payload jobs they run.

### ATLAS comparison
In response to a question from fstagni, it was confirmed (Marco Mascheroni, Jaime Frey) that ATLAS uses a comparable model: Harvester is ATLAS's equivalent of the GlideinWMS factory, and PanDA is the equivalent of the glidein/execution point; both submit pilots via HTCondor.

### Deployment questions
Alexandre Boyer asked how easy it is to set up and maintain an Access Point, and how many would be needed. Marco Mascheroni said it is fairly easy to set up; CMS/GlideinWMS currently deploys via Puppet and `yum install` rather than Kubernetes. He noted the DIRAC team has expressed interest in a Kubernetes-based deployment, and deferred further comment on that to Todd Tannenbaum and Jaime Frey, but this was not addressed in the remaining meeting time (Jaime Frey left the call shortly afterward).

### Next steps and organizational context
With time running short, Todd Tannenbaum proposed — as a suggestion, not agreed to — a possible follow-up such as a small Docker-based recipe demonstrating how to stand up an Access Point and submit a job to a remote Slurm cluster over SSH or to an ARC CE, to let the DIRAC side "kick the tires." fstagni responded that it was not a good time to decide next steps, since the DIRAC side is heading into a holiday period and needs to discuss internally first. Marco Mascheroni noted that CMS's current focus is on the transformation system (a separate, ongoing effort), and framed this HTCondor/DiracX discussion as a long-term (~10-year horizon) exploration that does not need to be decided in the near term. He pointed to two upcoming events in September/October 2026 as opportunities to continue the conversation: a DIRAC Users Workshop in October, and HTCondor Week Europe (referred to in the transcript as "HDC") in Lyon, which Todd Tannenbaum noted is free (sponsored) and linked from the top of the HTCondor.org homepage ("2026 European HTCondor Week," with registration going to an Indico event page). fstagni suggested the two teams could send cross-representatives to each other's events. Marco articulated what he sees as the main potential value of this effort: if multiple LHC experiments converge on a common pilot-submission interface, it could make the case for CERN IT to invest effort on behalf of experiments collectively — drawing an analogy to how the GlideinWMS factory is already operated as a shared/common service across experiments.

## Open Questions

- Should DiracX's InterSeed library be built from scratch, or should it reuse HTCondor (via its Access Point / Condor-G / grid-universe mechanism) for pilot submission? Explicitly unresolved; under investigation by the DIRAC team.
- What would a concrete DIRAC/HTCondor integration architecture look like — e.g., DIRAC's pilot factory submitting via Condor-G to an Access Point, with a DIRAC-specific Execution Point contacting DIRAC's own matcher to fetch payload jobs? Raised as a possibility by Alexandre Boyer, not decided.
- Could an HTCondor Access Point be deployed via Kubernetes (as the DIRAC team is reportedly interested in), rather than the Puppet/yum-based approach CMS/GlideinWMS currently uses? Not addressed before the meeting ended.
- Would a scalability test of the GlideinWMS factories confirm that current architecture can scale beyond the current ~40,000-pilot level without the multi-scheduler workarounds used historically? Suggested by Marco Mascheroni, not carried out.
- What are the concrete next steps for continuing this investigation (e.g., Todd Tannenbaum's proposed Docker-based Access Point demo)? Left open; the DIRAC team indicated it needs to discuss internally first, and timing is complicated by an upcoming holiday period.

## Related

[[DIRAC]] · [[DIRACX]] · [[HTCondor]] · [[glideinWMS]] · [[CMS]] · [[ATLAS]] · [[LHCb]] · [[CERN]] · [[Factory]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-14 16.12.44 Submission Infrastructure Weekly Meeting`)
