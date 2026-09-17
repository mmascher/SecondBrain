---
type: concept
---

# CMS CPU and Resource Efficiency

## Overview

CPU and resource efficiency is a recurring, escalating, and — as of the corpus end date (2026-09-16) — explicitly **unresolved** cross-team problem in CMS computing. It is documented through several independent evidence lines converging in the same period: a WLCG scrutiny-group compliance requirement, a live site-debugging case study, a CMS-wide cross-team strategy meeting, and purpose-built monitoring work. As of the CMS-OC strategy meeting on 2026-09-09, **no CMS-wide agreed efficiency metric exists**, and no root cause for current inefficiency has been established with confidence. This note presents the current state of that open problem rather than a resolution; per the synthesis principle of stating when evidence is insufficient, several sub-questions below are left explicitly unanswered because the corpus does not answer them.

## Current Understanding

### Independent evidence lines

- **The "bad put" metric proposal**: prompted by a WLCG scrutiny group now requiring experiments, not just sites, to self-report failed-job resource waste. Marco Mascheroni proposed "bad put" — wall time wasted by failed jobs, independent of CPU efficiency — as a more correct metric than PnR's existing CPU-time/wall-time ratio, since efficiency is irrelevant if the job's output is discarded. Two sub-types were proposed: Condor-restart bad put (same Condor job ID, e.g. dropped connection or pilot vacating) and WMAgent-retry bad put (new Condor job ID per retry, up to 3 retries).
- **CNAF live debugging case study**: CNAF showed roughly 40% idle cores against a Tier-1-wide efficiency of 93% (target range 96–98%). Memory exhaustion was checked and ruled out. "Pilot retiring" — pilots nearing end-of-life refusing new work, tied to jobs requesting roughly 2-day wall-clock times — was identified as a "plausible major contributor" but the debugging session ended before this was confirmed against the observed idle-job count.
- **CMS-OC-wide strategy meeting (2026-09-09, chaired by Stephan Lammel)**: explicitly a strategy/brainstorming session, not a decision meeting. No metric, cause, or policy change was agreed; the group deferred to smaller working groups. Candidate causes discussed without resolution: job startup/shutdown overhead, remote I/O vs. data pre-placement tradeoffs, poor resource-requirement characterization (jobs reported as typically requesting roughly 2x their actual memory use), low-efficiency analysis/user jobs (cited as around 30% of resources), and CPU-model heterogeneity (up to 3x performance variance for the same core count).
- **Pilot-monitoring precedent**: site-reported efficiency (70%) was found to diverge substantially from payload-level efficiency (46%) at one site, attributed to the pilot "overloading" mechanism inside [[GlideinWMS Pilot-Based Resource Provisioning]] compensating for capacity the payload-level metric doesn't capture. This is the clearest concrete link in the corpus between the efficiency-measurement problem and the overloading lever described below.

### The "overload enabled" mechanism

Pilots are deliberately configured to advertise and accept more CPU and memory than their nominal size, packing more payload work into the same pilot envelope. A CHEP 2026 presentation defines "moderate overloading" as +25% extra CPU cores and memory relative to nominal pilot size, deployed since 2023 and, as of the presentation, covering roughly two-thirds of the Global Pool's resources; operational meeting notes separately record a 66% value in use at some enabled sites, with higher values (up to 100% at Tier-1s) discussed as a possible future direction but not decided. The explicit design principle is to recover otherwise-unused CPU cycles within the pledged envelope, not to gain opportunistic cycles beyond it. An April 2026 bug fix addressed a type-casting issue where the overload-enabled attribute was not being correctly interpreted as a string, causing misreporting; this is distinct from the strategy itself. The CHEP deck reports "a significant and systematic improvement" in efficiency from overloading at both Tier-1 and Tier-2 sites, based on dedicated overloading-on/off comparison monitoring built specifically to measure this effect (since no dedicated pilot/payload-level efficiency dashboard existed previously, despite this being a recurring operational discussion topic).

### Proposed mitigations (proposals, not decisions, unless stated otherwise)

- **HTCondor 26.0 "Common Input Transfers"** — confirmed by HTCondor developer Jaime Frey as actively planned for the 26.0 release: transfers a tarball common to many jobs of the same cluster/execution point once, then extracts it per job into each job's own scratch directory, amortizing per-job bootstrap cost while keeping jobs independent.
- **Job bundling** (packing several user jobs into one HTCondor job) — HTCondor's currently recommended direction (Jaime Frey) for amortizing CVMFS/container load cost per job.
- **IO-slots** — already implemented: a dedicated slot type per pilot reserved for short single-core auxiliary jobs (merge, log collection), introduced to prevent slot fragmentation from starving higher-priority large-slot scheduling such as 8-core Tier-0 prompt reconstruction.
- **Immortal pilots** and **data-aware matchmaking** — both proposal-stage ideas discussed in the same period as the CPU-efficiency strategy meeting; they are related mitigations for adjacent problems (pilot-lifecycle fragmentation, and site-locality/remote-I/O reduction respectively) but are distinct proposals and should not be merged conceptually with the efficiency-metric problem itself.
- **Raising default per-job memory requests to permit more aggressive oversubscription** (proposed by Stephan Lammel) versus **increasing pilot/slot size further** (preferred by Antonio Pérez-Calero Yzquierdo) — see Disagreements below.
- Other ideas raised but not agreed: overlapping job startup/shutdown (HTCondor developer Jaime Frey noted HTCondor tried something similar roughly 15 years ago with limited uptake and does not recommend building on it now); dynamic, minute-scale rescaling of pilots/slots (Kevin Pedro, drawing a GPU/auto-scaling analogy); a target-efficiency abort/flag mechanism for early detection of underperforming workflows (Marco Mascheroni); and policy levers such as capping the resource share of low-efficiency analysis workflows (Stefano Belforte) or routing known-inefficient jobs to older hardware (with the caveat this would not help cache-thrashing-type bottlenecks).

## Disagreements and Open Questions

- **No CMS-wide agreed efficiency metric exists**, explicitly stated at the 2026-09-09 CMS-OC meeting. Candidates debated without convergence: raw CPU/thread "busy" time (criticized as a poor proxy since it can reflect cache-thrashing rather than useful work), event throughput per CPU cycle (James Letts), and CPU-cycle/instruction delivered-vs-needed (Stephan Lammel). Kevin Pedro and Antonio Pérez-Calero Yzquierdo separately noted that oversubscription complicates any "throughput" framing, since an individual job can appear slower while aggregate throughput rises.
- **Memory-vs-slot-size dispute, explicitly unresolved**: Stephan Lammel favored raising default per-job memory requests (e.g., from 3GB to 4GB, partly via swap) to enable more aggressive oversubscription; Antonio Pérez-Calero Yzquierdo was skeptical memory was the right lever and preferred larger pilot/slot sizes instead, and separately flagged a cgroup-isolation risk where one job's spiky memory usage could affect others sharing the same pilot. Matti Kortelainen pushed back further, arguing memory cannot be treated like CPU/disk at all, since it must be provisioned for peak usage and the real gap is that per-job memory needs aren't known in advance.
- **No root cause for current inefficiency has been established** — explicitly stated by multiple participants (Matti Kortelainen, Christoph Wissing, Stefano Belforte, Marco Mascheroni) at the CMS-OC strategy meeting; Marco noted there may be no single "smoking gun," only insufficient study so far.
- **GPU/heterogeneous resources** are acknowledged (James Letts) as a coming additional dimension that will complicate whatever efficiency metric is eventually chosen — GPU offload is expected to reduce raw CPU-utilization figures even while increasing overall throughput. Not yet addressed as of the corpus end date.
- **Whether to cap or constrain the resource share of low-efficiency analysis/user workflows** (Stefano Belforte's proposal, roughly 30% of resources per his figure) was raised and left as an open policy question, along with who would have authority to grant exceptions to such a policy (Christoph Wissing).
- **Whether an ATLAS-style data pre-placement model** is worth trading away CMS's current site-flexible scheduling model was raised (Stefan, Purdue) and left unresolved; Stephan Lammel cautioned against it.

## Relationships

- Consumes and depends on the "overload"/oversubscription mechanism documented under [[GlideinWMS Pilot-Based Resource Provisioning]].
- Overlaps in participants and timing with, but is conceptually distinct from, the "Immortal Pilots" and data-aware-matchmaking proposals — those are specific candidate mitigations, not restatements of the efficiency problem itself, and this vault's synthesis treats them separately.
- Bears on [[CMS Adoption of DiracX for Future Workflow Management]] indirectly: job/task-construction decisions (e.g., StepChain vs. TaskChain) that affect payload efficiency are expected to eventually move into DiracX's transformation system.

## Sources

- [[2026-05-29-Pilot-Monitoring-and-Efficiency-Presentation-Prep]]
- [[2026-08-12-PnR-Failed-Job-CPU-Waste-Bad-Put-Discussion]]
- [[2026-09-02-HTCondor-Shadowing-Session-CNAF-Efficiency-Debugging]]
- [[2026-09-09-CMS-OC-Weekly-Meeting-CPU-Efficiency-Strategy]]
- [[2026-09-09-CMS-Submission-Infrastructure-Meeting-Data-Aware-Matchmaking-Immortal-Pilots-Condor24]]
- [[2026-04-10-Overload-Enabled-Fix-Planning-and-Condor-Overview-Training]]
- `20-Meetings/20260525_CHEP26_CMS_SI_Efficiency.pdf`
- `60-Presentations/Memory Utilisation and Unused Cores.pdf`
