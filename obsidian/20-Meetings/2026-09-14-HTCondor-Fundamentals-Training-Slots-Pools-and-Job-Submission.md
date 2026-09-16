---
type: meeting
date: 2026-09-14
participants:
  - Marco Mascheroni
  - Pablo Izquierdo Gonzalez
topics:
  - Partitionable vs. static HTCondor slots; dedicated merge/auxiliary slot
  - WLCG governance and pilot-sizing agreements between LHC experiments
  - HTCondor overview presentation (from HTCondor Week material): pools, flocking, universes, JDL basics
  - CMS Condor pool topology (global pool, San/Tier-1 pool, negotiators)
  - HTCondor commands and job lifecycle (condor_submit, condor_q, condor_history, log files)
  - Custom ClassAd attributes (DESIRED_Sites) and data-locality matchmaking
  - Shares and priorities (group shares vs. per-user effective priority)
  - Workflows, DAGs, and DAGMan
  - Late materialization and a related HTCondor bug/CVE mitigation concern
  - Puppet failures on several machines (ongoing troubleshooting)
  - Manual changes on vocms059 and plan to puppetize them
---

# HTCondor Fundamentals Training: Slots, Pools, and Job Submission

## Summary

This was a continuation of the one-on-one onboarding/training sessions between Marco Mascheroni and Pablo Izquierdo Gonzalez, focused on [[HTCondor]] fundamentals, following on from prior sessions on [[glideinWMS]] architecture.

The session opened with Pablo's questions from his own review of material. First, Pablo asked about pilot sizing (8/16/32 cores vs. requesting a whole node), suggesting it seemed generally better to always take the whole node. Marco agreed in principle, but noted that most sites run a combination of experiments under [[WLCG]] (the body governing computing for the LHC experiments — ALICE, ATLAS, CMS, and LHCb), and that within WLCG there is an agreement between experiments to send pilots of consistent size; if one experiment sends single-core pilots while another sends whole-node pilots, it creates a scheduling problem for the site.

Second, Pablo asked about static slots, having read that they exist but assuming CMS does not typically use them. Marco confirmed CMS uses partitionable slots as the norm, then shared slides from a stakeholders' presentation to explain further: a typical CMS pilot requests 8 cores from the compute element (e.g., an ARC CE), but advertises somewhat more than 8 cores because CMS jobs (CRAB, WMAgent, user jobs) are often CPU-inefficient (e.g., 50–85% efficient, or as low as ~30% for some production jobs); the extra advertised capacity (Marco's example: a 10-core partitionable slot backed by 8 physical CPUs) recovers otherwise-wasted cycles when "overload" is enabled. In addition to the multi-core partitionable slot, each glidein pilot also carries a single-core **static slot** dedicated to auxiliary jobs — merge, cleanup, and log-collect jobs — which combine many small job output files into fewer, larger files (preferred by CMS's data management systems, which handle small files poorly) and are high-I/O, low-CPU jobs, justifying a dedicated static slot. This static slot is not published/available for analysis or other regular jobs.

Marco and Pablo then briefly checked whether they had already covered "the Condor user" tutorial material referenced in chat history, then spent the bulk of the session going through an HTCondor overview presentation (material from HTCondor Week) that Marco had been reviewing for an upcoming conference. Topics covered included: HTCondor as a workload management system developed by a team based at University of Wisconsin–Madison ("Condor" project, established 1985), used by ~200+ deployments worldwide across scientific communities; that it is used heavily for cosmology/astronomy use cases (e.g., Vera C. Rubin Observatory) among others; and that it is the second most popular batch system after Slurm.

They discussed how Condor can be used: running local/vanilla jobs via `condor_submit` from an access point, and running "grid universe" jobs, which is what the factory uses to launch a glidein (`glidein_startup.sh`) onto a compute element. Marco explained **flocking**: the ability to connect separate Condor deployments (pools), each with its own central manager/collector, so that jobs from one pool's schedulers can run on another pool's resources. CMS uses flocking in exactly this way: a "global pool" containing most resources (including WLCG sites, connected via the shared/CERN infrastructure) and a separate "San pool" (a smaller, dedicated pool CMS operates itself; the tier-1 sites/CERN's ~100,000 cores are handled within the global pool, contrary to an initial guess by Pablo). Within the global pool there are three negotiators, running on the same central manager/collector: one each for tier-1, US tier-2s, and the rest of the world. Marco also described the CMS resource-pool picture more broadly (referencing an infrastructure diagram): besides the global and San pools (which CMS Submission Infrastructure manages, along with the volunteer pool), there are minor pools not managed by the team — HEPCloud (used for HPC allocation-based access, managed by a separate US-based group) and a volunteer-computing pool (similar in spirit to tools like SETI@home, for donated public compute), plus an "external" pool whose purpose Marco was unsure of and said he would need to ask Antonio, who created the diagram.

The walkthrough continued through basic HTCondor usage: submit-file (JDL) syntax (universe, executable, arguments, input/output, logs), the `vanilla` universe (used because glideinWMS creates a vanilla pool), and pointed Pablo to a training page that lets him request a token and practice submitting a job as a user to the pool via a test access point/collector/scheduler (vocms059) — an exercise Marco recommended Pablo try himself. They covered `condor_q` (queued jobs), `condor_q -long` (all job ClassAd attributes), the job log file (recording condor-level events such as submission host, execution host, and termination — distinct from the job's own stdout/output logs), `condor_status` (pool/machine info), `condor_rm`, `condor_history` (completed jobs), and `condor_hold`/`condor_release`. They discussed file transfer (`should_transfer_files`, `transfer_input_files`, `transfer_output_files`, `when_to_transfer_output`, eviction), and Marco clarified that CMS jobs' actual physics output (ROOT files containing real or simulated collision data) is not transferred back through Condor but managed separately by the data-management system (e.g., via XRootD) to storage elements; what is described in the submit-file output-transfer examples is more relevant to smaller items like the CMS "framework job report" produced by the `cmsRun` executable, which could potentially be used for monitoring in the future.

They also discussed custom ClassAd attributes: prefixing an attribute with `+` in the submit file adds it as a custom job ClassAd attribute (without `+`, Condor treats it as an unrecognized system attribute and ignores it). CMS uses a `DESIRED_Sites` attribute heavily to steer jobs toward specific candidate sites. Pablo connected this to an earlier discussion about "distance" in matchmaking: Marco confirmed this relates to a discussion he'd had with the Condor developers (Jaime) about data locality — since data can often be read remotely, matchmaking can favor sites that are "close enough" to the data rather than requiring exact data co-location — and that he had asked whether a more expressive way to encode this in ClassAds could be added, since his own idea for implementing it via many ClassAds felt clunky.

The session covered **shares and priorities**: shares are a pie-splitting mechanism across groups (e.g., four resource "pies" in the example shown), with each group receiving a defined share; within a group, per-user priority handles fine-grained ordering. Tier-0/production jobs are treated as effectively a single user, so priority can be set directly (e.g., giving "repack" jobs — which process and derive data directly off the detector to free up buffer space — a higher priority than other Tier-0 jobs). For hundreds of individual users, HTCondor's default is FIFO ordering per user, but fairness across users is also mediated by each user's "effective priority," which increases with past resource usage — a user who has used more resources is deprioritized relative to one who has used less/none, so it is not a strict first-in-first-out queue globally. A user can raise the priority of their own individual jobs (`condor_prio`) but cannot alter their own overall user priority; Marco noted the team does not micromanage priority between users.

They covered **workflows and DAGs**: a workflow is a collection of jobs solving one task (Marco's example: analyzing a dataset by running one job per file subset), which may have inter-job dependencies (e.g., Monte Carlo generation → simulation → reconstruction). HTCondor's **DAGMan** tool handles these dependencies via a directed acyclic graph, submitted with `condor_submit_dag`, where parent/child relationships between jobs are declared explicitly.

Finally, they discussed **late materialization**: submitting large numbers of jobs (e.g., via `queue N from <file>` syntax, materializing one job per line of an input list) without submitting all of them to the schedule at once — instead materializing them in chunks (e.g., 1,000 at a time out of a million) to avoid overloading the scheduler. Marco showed a proof-of-concept example he had built previously. Pablo raised a concern (from something he had read) that mitigating a recently-referenced HTCondor vulnerability/bug related to late materialization might require more RAM if late materialization is disabled (since jobs would then materialize immediately rather than incrementally), asking whether the team had enough headroom. Marco confirmed the team does not use late materialization at all currently, so this concern does not affect them, and thanked Pablo for raising the question.

Before and after the main technical walkthrough, Marco and Pablo discussed operational follow-ups. Marco asked whether Pablo had looked further into why [[Puppet]] agent was failing to run on a particular machine ("60 something") mentioned in prior chat history. Pablo reported that DNS resolution works, but connections to the Puppet server are refused; the issue is not isolated to one machine, and that morning he had also received a Puppet-agent failure alert from a machine related to the "XSD Condor scale test" (transcribed as "8 0814"). Pablo was still investigating and had confirmed via testing on an ITB node that the problem persists. Marco suggested Pablo try running Puppet by hand on affected machines to capture the failure and attempt to reproduce it, noting he is not a Puppet expert and that ITB/scale-test machines are safe to experiment on since they are not in active use for scale testing currently. Separately, Marco raised manual changes Pablo had made on `vocms059`, suggesting these be reproduced via Puppet, "maybe waiting for Luis" — Pablo said Luis is expected back Wednesday, and that he plans to puppetize and test the changes on the ITB environment first (since the same changes will likely be needed in production).

Outside the core technical content, Marco mentioned he is working on a personal project processing roughly 130 historical meeting transcripts with AI to build a summarized, cross-linked concept map (grouping meetings by topics such as glideinWMS, factory, frontend, and people). Pablo mentioned he had adopted a similar approach in a meeting of his own.

## Decisions / Conclusions

- WLCG experiments (ALICE, ATLAS, CMS, LHCb) maintain an informal agreement to send pilots of consistent size to shared sites, because mismatched pilot sizes across experiments create scheduling problems for the site.
- CMS uses partitionable slots as the norm; a typical pilot advertises somewhat more than the requested core count (e.g., 10 cores backed by 8 physical CPUs when "overload" is enabled) to recover unused CPU cycles from inefficient jobs.
- Each glidein pilot also includes one dedicated single-core static slot reserved exclusively for auxiliary jobs (merge, cleanup, log collection); this slot is not available for analysis or other regular jobs.
- CMS operates two Condor pools connected via flocking: the global pool (containing WLCG/shared resources, including Tier-1s and CERN, split across three negotiators for tier-1, US tier-2, and rest-of-world) and a separate, smaller "San" pool. HEPCloud and the volunteer-computing pool are additional, minor pools; HEPCloud is managed by a separate US-based group, not the Submission Infrastructure team.
- The team does not currently use HTCondor late materialization, so the RAM-usage implications of a related mitigation/bug (raised by Pablo) do not affect the team's systems.
- Physics output data (ROOT files) from CMS jobs is not transferred back via Condor's file-transfer mechanism; it is handled by the separate data-management system (e.g., via XRootD) to storage elements.

## Action Items

- [ ] Investigate the Puppet agent connection-refused failures across multiple machines (including the XSD Condor scale-test machine); try running Puppet by hand to capture and reproduce the failure — Pablo Izquierdo Gonzalez
- [ ] Puppetize the manual changes made on vocms059, testing first on ITB before applying to production, coordinating with Luis Simas (back Wednesday) — Pablo Izquierdo Gonzalez
- [ ] Try the recipe for submitting a job to the ITB/skill'd test pool as a user (using the training page and requesting a token via the administrator node) — Pablo Izquierdo Gonzalez
- [ ] Continue training session the next day at 1:30 — Marco Mascheroni, Pablo Izquierdo Gonzalez

## Discussion

### Pilot sizing and WLCG pilot-size agreement
Pablo asked why pilots aren't always sized to request a whole node rather than fixed sizes like 8/16/32 cores. Marco explained that most sites serve a mix of WLCG experiments, and that there is an agreement among LHC experiments (governed by WLCG) to use consistent pilot sizes, since inconsistent sizing (e.g., one experiment sending single-core pilots while another sends whole-node pilots) creates site-level scheduling problems.

### Static vs. partitionable slots
Pablo had read that HTCondor supports static slots and assumed CMS doesn't typically use them. Marco confirmed CMS mainly uses partitionable slots, then walked through a stakeholders' presentation: a pilot requests 8 cores from the CE but advertises more (e.g., 10 cores/8 physical CPUs) to recover cycles wasted by inefficient jobs (CRAB, WMAgent, and user jobs run at roughly 50–85% efficiency, sometimes lower for production). Separately, each pilot also carries one single-core static slot dedicated to auxiliary "merge"/cleanup/log-collect jobs, which combine small output files into fewer, larger files (since CMS data-management systems handle small files poorly) and are high-I/O, low-CPU — justifying a dedicated slot. This static slot is not exposed to regular analysis jobs.

### HTCondor overview: history, pools, and usage
Using HTCondor Week training material, Marco covered: HTCondor's origin (University of Wisconsin–Madison, established 1985), scale of use (~200+ deployments worldwide), popularity as the second most-used batch system after Slurm, and its use across scientific communities including cosmology/astronomy (e.g., Vera C. Rubin Observatory). They discussed how Condor can be used to run local/vanilla jobs, and the "grid universe," which is what the factory uses to submit a glidein onto a compute element.

### Flocking and CMS pool topology
Marco explained flocking as the mechanism connecting separate Condor pools (deployments, each with its own central manager/collector) so jobs from one pool's schedulers can run on another's resources. CMS uses two flocked pools: a global pool (containing most WLCG-connected resources, including CERN's ~100,000 cores and Tier-1s) and a smaller "San" pool. The global pool runs three negotiators on the same central manager — for tier-1, US tier-2, and rest-of-world — while the San pool is a separate deployment. Other minor pools shown in the team's infrastructure diagram include HEPCloud (HPC allocation-based access, managed by a different US group) and a volunteer-computing pool (comparable to SETI@home-style donated compute); the purpose of an additional "external" pool shown in the diagram was unclear to Marco, who said he'd need to ask Antonio (the diagram's author).

### Basic job submission and commands
They walked through JDL/submit-file basics (universe, executable, arguments, input/output, logs) and the `vanilla` universe (used because glideinWMS creates a vanilla pool). Marco pointed Pablo to a training page for requesting a token and practicing job submission as a user against a test access point/collector/scheduler (vocms059), recommending Pablo try this himself since he has administrator-node access to create his own token. They also covered core commands: `condor_q` / `condor_q -long`, the Condor-generated job log (submission/execution/termination events, distinct from a job's own script output), `condor_status` (pool/worker-node info, often used with `-limit 1`), `condor_rm`, `condor_history`, and `condor_hold`/`condor_release`.

### File transfer and CMS job output
They covered file-transfer submit-file attributes (`should_transfer_files`, `transfer_input_files`, `transfer_output_files`, `when_to_transfer_output`, and eviction behavior). Marco clarified that a CMS job's actual physics output (ROOT files with real or simulated collision data) is not transferred back through Condor; it is handled separately by the data-management system (e.g., via XRootD) to storage elements. The submit-file output-transfer mechanism is more relevant to smaller artifacts, such as the "framework job report" produced by the `cmsRun` executable, which Marco suggested could potentially be analyzed for future monitoring.

### Custom ClassAd attributes and data locality
Custom job attributes prefixed with `+` in the submit file (e.g., `DESIRED_Sites`, used heavily by CMS to steer jobs to candidate sites) are added to the job's ClassAd; without the `+` prefix, Condor treats the attribute as an unrecognized system attribute and ignores it. Pablo connected this to an earlier mention of "distance" in matchmaking; Marco confirmed this referred to a discussion with Condor developer Jaime about factoring data locality into matchmaking (favoring sites "close enough" to remotely read the needed data, since data can often be read remotely rather than requiring co-location), and that he had asked whether a more expressive ClassAd mechanism could be added, since his own approach (many individual ClassAds) felt clunky.

### Shares and priorities
Shares split a pool of resources ("pie") across groups; within a group, per-user priority governs finer-grained ordering. Tier-0/production is effectively a single user, so priority can be set directly — e.g., "repack" jobs (which process/derive data straight off the detector to free buffer space) are given higher priority than other Tier-0 jobs. Across many individual users, the default ordering is FIFO per user, but overall fairness is also shaped by each user's "effective priority," which rises with past resource usage, deprioritizing heavy past users relative to users who have used fewer/no resources — so global ordering is not strictly first-in-first-out. Users can raise priority on their own jobs (`condor_prio`) but not their own overall priority; the team does not micromanage inter-user priority.

### Workflows and DAGMan
A workflow is a collection of jobs solving one task (e.g., analyzing a dataset by running per-file-subset jobs), which may have dependencies (e.g., Monte Carlo generation feeding into simulation, then reconstruction). HTCondor's DAGMan tool manages these dependencies as a directed acyclic graph, submitted via `condor_submit_dag`, with explicit parent/child job relationships.

### Late materialization
Late materialization allows submitting large numbers of jobs (e.g., via `queue N from <file>`) without generating them all at once in the schedd — materializing them in chunks (e.g., 1,000 at a time out of a much larger total) to avoid overloading the scheduler. Marco demonstrated a past proof-of-concept. Pablo raised a concern, based on something he had read, that a mitigation for an HTCondor bug/vulnerability involving late materialization might increase RAM usage if late materialization were disabled (since jobs would then materialize immediately). Marco confirmed the team does not currently use late materialization, so this does not affect them, and praised the question.

### Puppet troubleshooting and vocms059 manual changes
Pablo reported ongoing Puppet agent failures on multiple machines: DNS resolves correctly, but connection requests to the Puppet server are refused; this affects more than one machine, including one tied to the "XSD Condor scale test," which alerted that morning. Marco suggested trying to run Puppet by hand on affected machines to capture and reproduce the failure, noting ITB/scale-test machines are low-risk to experiment on. Separately, Marco asked about puppetizing manual changes Pablo had made on vocms059; Pablo said he would do this once Luis Simas is back (Wednesday), testing on ITB first since the changes will likely also be needed in production.

## Open Questions

- What is the purpose/role of the "external" pool shown in the team's resource-pool infrastructure diagram — Marco was unsure and said he would need to ask Antonio, who created it.
- What is causing the Puppet agent "connection refused" failures across multiple machines, including the XSD Condor scale-test machine?
- Root cause of the exact HTCondor bug/vulnerability Pablo referenced regarding late materialization and RAM usage was not detailed in the transcript beyond Marco's confirmation that it doesn't affect the team (since late materialization is unused).

## Related

[[HTCondor]] [[glideinWMS]] [[WLCG]] [[CMS]] [[CERN]] [[Puppet]] [[Factory]] [[Pilot Jobs]] [[CRAB]] [[WMCore]] [[XRootD]] [[HPC]] [[HTC]] [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-14 13.36.31 Submission Infrastructure Weekly Meeting`)
