---
type: meeting
date: 2026-09-04
participants:
  - Marco Mascheroni
  - Pablo Izquierdo Gonzalez
topics:
  - glideinWMS factory XML configuration (entries, gatekeeper/CE, RSL vs submit attribute)
  - HTCondor pilot execution flow (glidein_startup.sh, condor_master, condor_startd, partitionable/dynamic slots)
  - Negotiator matchmaking and claim handoff to the schedd
  - glideinWMS Frontend/Factory architecture and two-stage matchmaking
  - High Throughput Computing (HTC) vs High Performance Computing (HPC) concepts
  - Pledged grid resources vs HPC allocation-based access (manual glideins, HEP Cloud)
  - User-facing implications of HTC (no interactive access, batch queuing)
  - CMS job submission tools (CRAB) and job-submission use cases
---

# GlideinWMS and HTCondor Architecture Walkthrough (Onboarding)

## Summary

This was a one-on-one walkthrough session in which Marco Mascheroni explained the [[glideinWMS]] / [[HTCondor]] architecture to Pablo Izquierdo Gonzalez, who is building up his understanding of the [[Submission Infrastructure]] stack. The session started from a diagram/understanding that Pablo had already put together and progressively filled in missing pieces.

Marco first walked through the factory configuration XML file, showing that it defines "entries" (factory entries), each corresponding to a queue on a compute element (CE) — i.e., a CE hostname (the "gatekeeper") plus its batch queue. He noted that the old CREAM-based gatekeeper mechanism is deprecated, and that job/resource attributes that used to be set via the RSL attribute are now set via the submit attribute instead. Each entry defines the pilot configuration, including the size (resources) of the pilot it will request.

Pablo described his understanding that each execution point (worker node) has a partitionable slot representing (up to) all of that machine's resources, and asked how the execution point pushes information (a ClassAd) to the collector; the transcript is unclear on the exact terminology used for this ClassAd. Marco then pointed out that Pablo's picture was missing the factory and the whole glideinWMS layer: the factory sends a pilot to the CE, the CE submits the pilot into the batch system's queue (e.g., a Slurm queue), and the pilot itself is a bash script called `glidein_startup.sh`. When the pilot starts, it performs validation, downloads files from the factory/frontend, and then starts `condor_master` and `condor_startd` on the execution point.

Once the startd is running, a partitionable slot (Marco's example: 8 cores, 16 GB RAM, unclaimed) appears in the collector. The negotiator looks at the pool's unclaimed slots and tries to do matchmaking against queued jobs (Marco's example: a job needing 1 core and 2 GB); when it finds a match, it carves a dynamic slot out of the partitionable slot (e.g., `slot1_1`, matching what Marco had shown earlier via `condor_status`) and hands the claim to the component running the job queue, referred to at various points in the transcript by garbled terms (rendered inconsistently as "SCD"/"SCID"/"SCIDD"/"SCADIs") that appear, from context, to correspond to the HTCondor **schedd**; this component can then start running the job. Marco described the resulting chain — schedd, "shadow", and "starter" — connecting back so that the job can finally execute on the worker node, noting this involves "all this infrastructure going on" that he was simplifying.

Marco then raised the open question Pablo had implicitly been missing: how are pilots actually submitted to CEs in the first place? He shared a link to introductory glideinWMS material and walked through the Frontend/Factory picture: the Frontend looks at user jobs in the schedulers (a simplified "user pool" box standing in for a schedd + collector), determines how many pilots are needed (a first stage of matchmaking, on resource requests), and queries the factory for its list of queues/entries (the same XML entries shown earlier). The factory then does its own matchmaking and sends pilots to compute elements. Marco described this as a "two-stage matchmaking" process and noted that WMAgent (mentioned only in passing, as CMS's workflow layer) adds a further layer of complexity above this that was not covered in detail.

The discussion then moved to conceptual background. Marco explained that glideinWMS was designed to address High Throughput Computing ([[HTC]]) needs, which differ from [[HPC]]: HTC involves many independent jobs, each with its own input and output and no shared memory between jobs (i.e., batch processing, as used at [[CERN]]), whereas HPC jobs may share memory across a job. The goal of HTC/batch processing is to let large numbers of CPUs be used effectively by large numbers of users, and there is always more demand than available CPUs. Sites pledge fixed resources to experiments (e.g., an example of ~1000 CPUs pledged to CMS at a site); if those pledged resources go unused, they are wasted, since there is no "banking" of unused pledge time. [[Offline Computing]]/Submission Infrastructure is responsible for keeping pledged resources busy and well-utilized; deciding what physics work to run is the responsibility of physics coordination, a separate area. Sustained utilization is therefore prioritized over peak performance.

Marco contrasted this with HPC allocations: most supercomputing centers are not owned by CMS, so access requires writing and being awarded a grant, which results in a core-hour allocation to burn through — a different model from grid pledge shares, where, e.g., a site might enforce an instantaneous 50/50 CPU split between two experiments (his example: an IFCA-like site with CMS and ATLAS), and where a week of unused ATLAS share (e.g., if ATLAS's PanDA workflow system is down) is simply lost rather than recovered later. HPC centers also typically serve many different use cases beyond high-energy physics, unlike grid resources, which are generally dedicated to HEP. For accessing HPC allocations, Marco described two approaches: either a site admin/responsible person manually launches pilots ("glideins") when they want to consume the allocation (avoiding the factory continuously pushing pilots), or a US-based project called "HEP Cloud" manages allocation-based provisioning.

From the user's point of view, HTC means there is no interactive access to worker nodes — only queued/batch job submission (a "user job"). If a job fails, the user receives an error rather than a live diagnosis opportunity. The payoff is that a user can use thousands of CPUs at once and complete computations that would take years on a single machine, since the work is embarrassingly parallel/partitionable (no shared memory, split into independent batches). Marco began describing three main use cases for how "users" submit jobs to the infrastructure; only the first was covered before the transcript ends: individual/single users (up to a few hundred people) submitting jobs mainly via [[CRAB]] (CMS's job-submission tool). He mentioned that Stefano Belforte, a retired but highly knowledgeable and still-active volunteer, is a good contact for CRAB-related questions.

The transcript ends here, before the second and third job-submission use cases were described.

## Decisions / Conclusions

- Marco and Pablo agreed it is valuable to hold more sessions like this one over the coming weeks, moving back and forth between high-level pictures and low-level technical details as Pablo's questions come up (the same approach Marco said he had previously used with Luis Simas).

## Action Items

- [ ] Review the glideinWMS Frontend/introductory material Marco shared, and bring follow-up questions on the Frontend/WMS-level architecture to a future session — Pablo Izquierdo Gonzalez

## Discussion

### Factory configuration XML and entries
The factory configuration XML defines "entries" (factory entries), each representing a queue on a compute element. An example entry showed a name and a "gatekeeper" field identifying the CE; Marco noted the old CREAM-based gatekeeper approach is deprecated, and that resource-request attributes formerly placed in the RSL attribute are now placed in the submit attribute. Entries define the pilot configuration, including pilot size.

### Execution point, slots, and the pilot start-up flow
Pablo described each execution point as exposing a partitionable slot representing (up to) all of that machine's resources, and asked how/what ClassAd information the execution point pushes to the collector — the transcript is unclear on the precise terminology he was asking about (variants like "class ID"/"ClassAd" appear, without a clean resolution in the discussion). Marco filled in the missing components: the factory sends a pilot to the CE; the CE places the pilot into the batch system's queue (e.g., Slurm); the pilot is the `glidein_startup.sh` bash script, which validates, downloads files from the factory/frontend, and starts `condor_master` and `condor_startd` on the execution point. This produces a partitionable slot in the collector (example given: 8 cores, 16 GB RAM, unclaimed).

### Negotiation, dynamic slots, and job start
The negotiator inspects the pool's unclaimed slots and performs matchmaking against queued jobs. On a match (example: a 1-core, 2 GB job), it creates a dynamic slot out of the partitionable slot (e.g., `slot1_1`) and hands the claim to the queue-holding component so it can start running jobs — referred to inconsistently in the transcript by terms that, from context, appear to correspond to the HTCondor schedd (the transcript itself is unclear/garbled on this terminology and it is preserved here as uncertain). The starter and shadow are then involved in connecting back so the job can finally execute.

### glideinWMS Frontend/Factory and two-stage matchmaking
Marco shared introductory glideinWMS material to fill in the piece Pablo's diagram was missing: the Frontend and Factory. The Frontend watches user jobs in the schedulers (simplified as a single "user pool" box, standing in for a schedd + collector), determines the resource request (how many pilots are needed) via a first stage of matchmaking, and queries the factory for its entries (the same queues shown in the XML file). The factory performs its own matchmaking and sends pilots to the compute elements — Marco described this overall process as "two-stage matchmaking." WMAgent was mentioned only as an additional layer of complexity above this, not covered in detail in this session.

### HTC vs. HPC
[[HTC]] (as used at CERN, i.e., batch processing) involves many independent jobs with their own input/output and no shared memory, in contrast to [[HPC]], where jobs may share memory. The objective in HTC is facilitating effective use of large numbers of CPUs by large numbers of users, with demand always exceeding available CPUs. Grid resources are pledged to experiments by sites (e.g., CMS being pledged on the order of 1000 CPUs at a given site in Marco's example); unused pledged time is simply wasted, with no accumulation/banking. Submission Infrastructure/offline computing is responsible for keeping these resources well-utilized; deciding what to run is the responsibility of physics coordination. Sustained utilization is prioritized over peak performance.

### Pledged resources vs. HPC allocations
At sites supporting multiple experiments, the site's CE and batch system enforce an instantaneous share split (Marco's example: a 50/50 CMS/ATLAS split); if one experiment doesn't use its share (e.g., ATLAS's PanDA system being down for a week), that unused share is lost rather than recovered later — there is no historical accounting. HPC allocations work differently: they are obtained via a grant and consist of a core-hour budget that is burned through and does not depend on continuous usage in the same way. HPC centers also typically serve many use cases beyond HEP, unlike HEP-dedicated grid resources. Access to HPC allocations happens either via a site admin/responsible person manually launching pilots when they want to consume the allocation, or via a US-based project called "HEP Cloud" that manages allocation-based provisioning.

### User-facing implications of HTC
There is no interactive access to worker nodes for users — only queued "user job" submission. If a job encounters a problem, the user receives an error rather than being able to diagnose it live. The payoff is that users can access thousands of CPUs simultaneously for computations that would otherwise take years on a single machine, since HTC work is partitionable/embarrassingly parallel (no shared memory) and can be split into independent batches.

### Job-submission use cases and CRAB
Marco began describing three main use cases for job submission into the infrastructure. The first — individual/single users, up to roughly a few hundred people — submit jobs primarily via [[CRAB]], CMS's job-submission tool. Marco mentioned Stefano Belforte, a retired but still highly active and knowledgeable volunteer, as a good contact for CRAB-related questions. The transcript ends before the second and third use cases were introduced.

## Open Questions

- What exact ClassAd/terminology applies to the information an execution point pushes to the collector (e.g., machine ClassAd vs. slot ClassAd) — the transcript's account here (Pablo's question and the follow-up) was unclear and unresolved.
- What are the second and third main use cases for job submission into the infrastructure (only the first, single-user submission via CRAB, was covered before the transcript ends)?
- What further glideinWMS Frontend/WMS-level details (beyond the introductory material shared) will Pablo need explained in follow-up sessions?

## Related

[[glideinWMS]] · [[HTCondor]] · [[Submission Infrastructure]] · [[Pilot Jobs]] · [[Factory]] · [[Factory Configuration]] · [[Workload Management]] · [[HTC]] · [[HPC]] · [[CRAB]] · [[CMS]] · [[CERN]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-04 14.18.15 Submission Infrastructure Weekly Meeting`)
