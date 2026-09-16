---
type: meeting
date: 2026-04-09
participants:
  - Marco Mascheroni
  - Luis Simas
topics:
  - HTCondor training
  - factory tarball management
  - pool priorities and fair share
  - workflow terminology
  - DAGMan
---

# HTCondor Training Session (User Overview)

## Summary

Marco Mascheroni walked Luis Simas through the "HTCondor user" onboarding slide deck (one of three planned corridor-material presentations; a shorter "mission statement" deck had already been covered in a previous session). The session combined a walkthrough of HTCondor submission basics, ClassAds, pool fair-share/priorities, and workflow terminology with live, hands-on exploration of the production/ITB pools. During this exploration they found and fixed a real issue: the ITB pool had pilots running but zero usable cores because the factory's tarball configuration had not been updated after a recent HTCondor version upgrade.

## Decisions / Conclusions

- The ITB pool problem was diagnosed as: the glidein startup validation could not find the [[HTCondor]] binary version requested by the frontend, because the factory's tarball list had not been updated for HTCondor 25 after that version was rolled out (the timing lined up with an HTCondor 25 update Luis had seen referenced in a recent commit). Having pilots running is a necessary but not sufficient condition for the pool to provide usable slots — validation must also succeed.
- Fixed live during the meeting: Marco added the missing 25.0.x entry to fact-tools' `get_tarballs` YAML configuration and re-ran the `get_tarballs.py` script to download the new tarball and regenerate the XML that [[glideinWMS]] consumes.
- The Red Hat 7 → HTCondor-version manual override (HTCondor does not ship condor 24 builds for Red Hat 7, so RHEL7 requests for condor 24 are manually mapped to condor 23) exists only as a local file on the factory and is **not** currently tracked in Puppet.
- For the next-generation workload management system, management had previously decided to go with [[DIRAC]], having evaluated it against Panda and an in-house option built on Condor's [[DAGMan]] plus a "micro agent" concept (explored in an earlier proof of concept, with Dima using DAGMan for orchestration). Panda was ruled out. Marco noted the in-house option is "still on the table" pending evaluation of [[DIRACX]].
- Going forward, Marco and Luis agreed to use CMS's term "task" rather than Marco's own informal term "workload" when discussing chained processing steps, since "workload" is not standard terminology in the collaboration (e.g. Hassan Amed would not recognize it).

## Action Items

- [ ] Put the Red Hat 7 HTCondor-version manual override file under Puppet management — Luis Simas
- [ ] Ask Jeff whether the old `.htcondor.tarballs` (gittar/backup) file can be removed from fact-tools now that tarballs are sourced from glideinWMS directly — Marco Mascheroni
- [ ] Raise at the factory ops meeting: remove `get_tarballs.py` from fact-tools — Marco Mascheroni
- [ ] Raise at the factory ops meeting: remove the now-unneeded HTCondor 10 tarball entry from the YAML config — Marco Mascheroni

## Discussion

### HTCondor overview
HTCondor is a batch system used to run jobs as part of a workload management system; it has been developed for roughly 30 years and is valued for being fault-tolerant, feature-rich, and flexible. The [[Submission Infrastructure]] group works with the HTCondor developers on features such as GPU discovery/advertisement/scheduling, which the group leveraged when integrating GPUs into the [[Global Pool|global pool]]. The group holds a recurring meeting with the HTCondor team on Wednesdays at 18:00 (biweekly; not meeting that particular week, but scheduled for the following week) to raise questions.

HTCondor can be used in several modes: managing local processes, a local cluster (vanilla universe — used for the global pool), flocking across clusters, building resource overlays (the approach used with glideinWMS), or accessing external resources such as grid/cloud sites or other batch systems via grid universe (condor-G), which is how the factory contacts a site's compute element.

### Submission basics and ClassAds
To submit a job, a user accesses a submit host, chooses a universe (vanilla, local, scheduler, or grid), makes the job "batch ready" (i.e., ensures data availability), writes a submit description file, and runs `condor_submit`. In CMS, data locality means jobs are sent to sites where the data already resides — WMAgent (used by production/reprocessing and Tier0) and CRAB specify the target site in the job; the site's storage element (e.g. dCache, or EOS at CERN) holds the data, and [[Rucio]] moves data between sites, including to tape (Tier0 needs tape access and therefore runs mostly on Tier-1s; Tier-2s generally do not have tape).

There are two kinds of ClassAds: **machine ClassAds**, which live on the collector and are queried with `condor_status` (not persisted, since the `startd` on each execute node periodically republishes them), and **job ClassAds**, which live on the schedd and are persisted to a `job_queue.log` so the full job history/state can be reconstructed if the schedd restarts. `condor_q -long` shows a job's ClassAd attributes; `condor_history` retrieves attributes for completed jobs for a limited retention window. For longer-term storage, a monitoring machine (work attributed to Carlos) queries completed jobs roughly every ~12 minutes and pushes them into [[OpenSearch]].

Job attributes prefixed with `+` in the submit file (e.g. `+DESIRED_Sites`, used heavily to steer jobs to specific sites) become arbitrary custom ClassAd attributes. Statements without `+` are HTCondor "macros" (e.g. `request_cpus`); HTCondor validates macros (e.g. checks numeric values) and translates them into standard ClassAd attributes (e.g. `RequestCpus`) and may also incorporate them into the job's `Requirements` expression, but the macro's literal name is not necessarily queryable via `condor_q -long`.

### File transfer and eviction
By default HTCondor transfers output files back only on job exit. "Eviction" refers to catastrophic failures from HTCondor's point of view — e.g. a network failure between the schedd and the worker node, or the pilot terminating and killing the job — which send a job from running back to idle transparently, without transferring anything back and without leaving a useful log, making these failures hard to debug. `condor_ssh_to_job`, previously used to inspect a running job on the worker node, "doesn't work well anymore" according to Marco. HTCondor does support configuring output transfer to also occur on eviction, which Marco was investigating but had not yet confirmed is used anywhere (WMAgent submits via Python bindings rather than a static submit file, so the exact configuration used was unclear during the meeting).

### Factory tarball / version management
Worker nodes do not rely on locally installed HTCondor binaries; the glidein downloads binaries from the factory during startup (via the `glidein_startup.sh` validation step and the `condor_platform_select` script). The factory maintains a list of HTCondor tarballs (managed via fact-tools' `get_tarballs.py` script and a YAML configuration) that are downloaded from the HTCondor website and turned into an XML file consumed by glideinWMS. Previously, tarball information was maintained by hand directly inside each frontend's `.xml` configuration; this has since been split out into separate, script-generated XML files. Distributing tarballs via [[CVMFS]] was discussed as a possible next step but is not currently relied upon, since CVMFS is mandatory only for CMS and not for other experiments that also use glideinWMS.

### Frontend configuration via Capitan
Frontend XML configuration is generated using a tool called Capitan from a shared base plus small per-frontend snippets. This was introduced historically because the CMS backup frontend (Fermilab) and ITB frontend XML configurations tended to diverge despite being mostly identical, and an operator introduced Capitan to reduce that divergence. Puppet manages the underlying repository/tooling, but day-to-day operational changes (e.g. running scripts to pull tarballs, editing YAML) are made locally by Marco or the factory operators and then reconciled into Puppet by the operator, to preserve a single point of responsibility for the Puppet-managed infrastructure. Jeff manages Kubernetes-based factories (e.g. the SG one) differently; Marco noted Jeff has been automating more of this than the "classical" factory setup, and saw this ITB fix as an opportunity to automate similarly.

### Pool structure, fair share, and priorities
The [[CERN]] pool and the global pool each have their own negotiator; the global pool additionally has separate negotiators for US Tier-1s, US Tier-2s, and the rest. Three top-level accounting groups exist — Tier0, Production, and Analysis — each configured with a percentage share of resources that varies per resource pool (e.g., the CERN pool allocates roughly 80% to Tier0, 10% to Production, 10% to Analysis). Marco noted the percentages shown in the training slide for one other resource pool were outdated/incorrect, since Florian had recently changed them. "Group surplus" can be enabled or disabled per group to allow an unused share to overflow to other groups.

Within the Analysis accounting group, individual CRAB/CMS Connect users each have a priority, distinct from the group's fixed percentage share: priority does not grant a larger portion of the group's share, but determines who gets access to that share first. This matters in practice — e.g. if a popular dataset is hosted at one site, the user with the currently highest priority can dominate access to that site's resources even while other users' own shares remain unsatisfied and other sites have free resources. `condor_prio` can be used to raise or lower the priority of a user or an individual job. Production and Tier0 accounting groups each effectively contain a single user, whereas Analysis contains many (Luis recalled roughly 400 for a comparable case).

### Workflow terminology
Marco distinguished, as his own informal terminology (not standard across the collaboration): a **workload** as a bunch of jobs sharing similar requirements, and a **workflow** as multiple workloads chained together (e.g. one workload for reconstruction/AOD production, another for MiniAOD/NanoAOD production). CMS itself uses "task chain" for a workflow made of multiple tasks; the group agreed to prefer "task" over "workload" going forward.

A **step chain** runs multiple processing steps (e.g. Gen, Sim, Digi, Reco, MiniAOD, NanoAOD) within a single job. Production operators prefer step chains for faster turnaround/delivery time, but step chains are less resource-efficient because each step has different resource requirements and the job's slot must be sized for the most demanding step. Marco described a proof-of-concept, presented at a conference (the specific event was unclear in the transcript), that improved step-chain CPU efficiency from around 50% to around 95% for a given job by running multiple `cmsRun` processes in parallel during the step chain's first stage — addressing a current WMAgent limitation of one `cmsRun` invocation per step (the job's actual executable is a WMAgent/CRAB/Tier0 wrapper that invokes `cmsRun`).

HTCondor's native [[DAGMan]] tool manages job dependencies (parent/child relationships) directly, and a DAG can be submitted like any other job via `condor_submit`. Despite being a built-in feature, DAGMan is not currently used by any CMS system in production.

### Team/organizational context
Factory operations (data-management-equivalent tickets, e.g. stuck data or storage-element outages) is handled by an operations team including Christos, Panos, and Hasan Ozturk. Production and reprocessing (PnR) — mostly Monte Carlo simulation, plus building MiniAOD/NanoAOD from Tier0's AOD output — is handled by Hasan Amed and Gregor. Tier0 (prompt reconstruction, required within 48 hours of raw data arrival) is handled by Antonio and another team member whose name the transcript did not capture clearly.

## Open Questions

- Whether output-file transfer on eviction is configured anywhere in the CMS submission stack (e.g. WMAgent) was left unresolved during the meeting.
- `condor_ssh_to_job` no longer works well for debugging jobs on worker nodes; no owner or timeline was established for fixing it.

## Related

[[HTCondor]] · [[glideinWMS]] · [[Factory]] · [[Factory Operations]] · [[DIRAC]] · [[DIRACX]] · [[DAGMan]] · [[WMAgent]] · [[CRAB]] · [[Rucio]] · [[CVMFS]] · [[OpenSearch]] · [[Global Pool]] · [[Tier 0]] · [[CMS]] · [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-09 10.58.16 Submission Infrastructure Weekly Meeting`)
