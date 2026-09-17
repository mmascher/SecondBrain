---
type: concept
---

# Submission Infrastructure

## Overview

Submission Infrastructure (SI) is CMS's function, team, and operational umbrella responsible for acquiring and allocating compute resources — via Compute Elements — for the collaboration's workloads. It is explicitly **not** responsible for data movement or storage. `[[Submission Infrastructure]]` is the second-most-referenced entity in the corpus and is the operational umbrella under which [[GlideinWMS Pilot-Based Resource Provisioning]], the [[Site Token Authentication Migration for Pilot Submission]], [[CMS CPU and Resource Efficiency]] work, and [[CMS Adoption of DiracX for Future Workload Management]] all sit.

## Current Understanding

### Computing-model role

Per the canonical onboarding explanation given to a new hire in March 2026, SI acquires compute via Compute Elements; each CE plus an SI-defined usage configuration (memory/core, wall-clock limits, whole-node vs. fixed-size slots) forms an "entry" — a pilot submission point agreed between the CMS VO and the site. CMS uses a pull/late-binding "pilot" model: pilots are generic resource requests; task-to-site binding happens only after a pilot has actually acquired resources. This is contrasted with a push model (pre-assigned tasks) or a "vacuum model" (pilots that appear and vacate independent of demand) — SI's model instead sends pilots only in response to actual queued demand (e.g., GPU pilots are requested only when GPU jobs are queued).

Among SI's workload "customers," **Tier-0** (prompt reconstruction, repacking) has the highest operational priority, because falling behind risks saturating the online data buffer and permanent data loss — unlike Monte Carlo production or analysis, where delays are recoverable. Repack jobs specifically are considered even more time-critical than prompt reconstruction because raw-data buffering at that stage has a shorter safety margin. A later meeting nuanced this rationale: Antonio Pérez-Calero Yzquierdo noted PromptReco also matters for detector calibration timing, while Andrea Piccinelli pushed back that since all jobs run on the same underlying HTCondor infrastructure, the calibration-timing concern may reflect current priority/share configuration rather than an inherent technical constraint — this was left unresolved between them.

**Production** (centrally organized MC simulation and reprocessing, driven by WMAgent/Request Manager, run by a small group of experts) is distinguished from **analysis** (individually- or group-driven, submitted via CRAB by roughly 400 physicists); Antonio Pérez-Calero Yzquierdo cited production as roughly 80% of resources as a rough order of magnitude, though exact shares vary by pool and the source material itself flags these percentages as not fully precise.

The core SI control plane runs with CERN as primary and Fermilab as standby (master/slave), backed by 3–4 redundant glideinWMS pilot factories for additional redundancy and scale. "Tier-0" itself was explicitly flagged as an overloaded term, simultaneously denoting a physical location (CERN), a function (prompt reconstruction/repacking), and a team — these don't always coincide, since "Tier-0 work" can and does run at Tier-1 sites, including Fermilab, when CERN capacity is insufficient (confirmed operationally: Antonio Pérez-Calero Yzquierdo, preparing an LHCC talk, had not realized Fermilab was used this way, for heavy-ion Tier-0 processing via inter-pool flocking).

**Historical note on this framing**: a check of CMS's 2021 LHCC Computing Model Review (`40-References/CMS/LHCC-Computing-Model-Review-2021/`) confirms that the pilot/late-binding submission model itself is long-standing CMS doctrine, already documented in 2021 and citing an even earlier 2014 reference. However, the specific framing elements emphasized in the 2026 onboarding meeting — the Tier-0 data-loss-risk priority rationale, the explicit "vacuum model" contrast term, the ~80%/400-physicists production-versus-analysis split, the CERN/Fermilab HA control-plane description, and "Tier-0 as an overloaded term" — do not appear in the 2021 review text (confirmed by direct search of the review's source files). This may simply reflect the 2021 document's different focus (HPC integration, risk registry) rather than these framings being new in 2026; the corpus does not establish which is the case, and this should not be read as evidence the framing is recent.

### Team structure and staffing (as of September 2026 — this changes quickly)

SI is a small team (on the order of 5 people), co-led by Antonio Pérez-Calero Yzquierdo and Marco Mascheroni, distinct from two related but separate groupings: the **New WM Dev Team** (evaluating and building the future DIRAC/DiracX-based system — see [[CMS Adoption of DiracX for Future Workload Management]]), and **Factory Operations** (the multi-experiment glideinWMS factory work, led on the US/OSG side by Jeff Dost).

Staffing changed substantially within the corpus period: Luis Simas joined as a factory-operations hire in March 2026; Florian Von Cube's position (CAT-affiliated, not CERN-employed) ended around May 2026, and he departed for KIT while retaining a bounded, time-limited role on glideinWMS/DiracX global-pool integration under the DIRAC project umbrella; Pablo Izquierdo Gonzalez joined in September 2026 as the new HTCondor/front-end operator, restoring what the team called "nominal" or "full" staffing. As of early September 2026, Pablo was becoming the team's main day-to-day operator, while Luis — despite having joined only in March — was already regarded as senior enough to take on forward-looking projects (Factory-to-Kubernetes migration, AI-tooling integration).

A **WM Level-2 transition** was pending as of the corpus end date: Marco Mascheroni was in discussion about moving into the CMS Workload Management Level-2 coordinator role while retaining roughly 75% of his time on SI. James Letts framed this as SI "speeding up toward the new WM," not slowing down, since DiracX-transition support is itself SI's stated top priority. Separately, the existing SI-affiliated Level-2 coordinator, Andrea Piccinelli, was moving to a Level-2 role in physics outside Offline & Computing, further reducing SI-affiliated Level-2 headcount. As of the latest source, Marco's own transition was still pending approval from his funding-line manager.

### Budget and roadmap

A scale test recorded in June 2026 confirmed roughly 800,000 simultaneously running jobs (~3 million cores, ~8 cores/job average) as achievable, consistent with results from a couple of years earlier. Memory (roughly 2MB per running job) was identified as the binding scaling constraint on the central manager, which cannot itself scale horizontally (unlike schedulers, which scale horizontally but deliberately not indefinitely, to limit hardware cost). Assuming only failed hardware is replaced (no new purchases), current infrastructure was judged adequate through the HL-LHC era. A named staffing-risk scenario (explicitly hypothetical, not an actual/imminent event as of the source) considered the impact of losing Jeff Dost's factory-operations expertise, concentrated in relatively few people; a broader, non-scenario-specific concern Marco Mascheroni raised is the general risk inherent in CERN's roughly two-year operator-rotation model, independent of any particular funding situation.

## Disagreements and Open Questions

- **Whether removing SI's dedicated Level-2 org-chart slot is organizationally acceptable** — raised informally by Marco Mascheroni in the context of his own transition and Andrea Piccinelli's departure to a physics Level-2 role; James Letts's initial view was that this is not necessarily a problem, but the question was not conclusively resolved.
- **Job-materialization philosophy: maximize vs. constrain.** Antonio Pérez-Calero Yzquierdo argued WM should push as many jobs as possible into scheduler queues immediately and let Condor's matchmaking handle availability, since throttling submission works against SI's ability to react to sudden resource bursts (e.g., HPC allocations). Alan Malta Rodrigues and Marco Mascheroni countered that job *diversity* — not raw count — is what's needed to exploit heterogeneous resources, and that materializing large numbers of jobs has real, non-trivial cost in upper WM layers (database updates, ClassAd propagation) unlike Condor's near-zero cost for pending jobs. Antonio countered this cost should be treated as something the future system should be built to minimize, not accepted as a structural throttle. Explicitly left unresolved as a CMS-wide design tradeoff.
- **"Thin integration"/"two engines" risk.** Recurring across multiple New WM Dev Team meetings in March 2026 (predating the DiracX decision): Marco Mascheroni and Valentin Kuznetsov repeatedly warned that layering glideinWMS on top of an external system's existing brokerage/matchmaking components risks recreating the same over-engineered, hard-to-evolve architecture that motivated moving away from WMCore in the first place. Alan Malta Rodrigues argued for maximizing reuse of an adopted system's components to build shared community effort, while clarifying he did not mean simply stacking systems; Kenyi Hurtado Anampa maintained that a proposed "recycling" strategy would not duplicate an external system's core provisioning function. Both sides agreed the right tradeoff depends on available effort (FTEs); not resolved as a general principle.
- **CRAB schedd scalability limit.** A CRAB schedd ran out of memory when a large amount of suddenly-freed pool capacity caused many normally-idle per-workflow DAG processes to start near-simultaneously. Antonio Pérez-Calero Yzquierdo's position is that CRAB should be able to scale to use most or all of the global pool with headroom, and that hitting this limit at only around half the pool is a real scalability problem, not coincidental timing; Marco Mascheroni intends to raise it with HTCondor developer Jaime Frey when a suitable meeting occurs, but had not done so as of the latest source. Open as of the corpus end date.

## Relationships

- Umbrella organizational and computing-model concept for [[GlideinWMS Pilot-Based Resource Provisioning]], [[Site Token Authentication Migration for Pilot Submission]], [[CMS CPU and Resource Efficiency]], and [[CMS Adoption of DiracX for Future Workload Management]].
- The "New WM Dev Team" described here as organizationally distinct from day-to-day SI operations is the home of the work described in [[CMS Adoption of DiracX for Future Workload Management]].
- Effort-allocation and use-case-boundary decisions made within SI/New WM Dev Team meetings (e.g., CMS Connect staying outside DiracX for simple submission) materially constrain the scope of that DiracX transition.

## Sources

- [[2026-03-04-CMS-Computing-Model-Submission-Infrastructure-Onboarding]] (primary/canonical)
- [[2026-02-26-Submission-Infrastructure-Weekly-Meeting]]
- [[2026-03-02-New-WM-Dev-Team-Weekly-Meeting]]
- [[2026-03-03-New-WM-Dev-Team-Weekly-Meeting]]
- [[2026-05-08-Submission-Infrastructure-Candidate-Interview-Pablo-Izquierdo]]
- [[2026-05-19-Submission-Infrastructure-Candidate-Interview-Sanji]]
- [[2026-05-29-Submission-Infrastructure-Candidate-Interview-and-DIRAC-Decision-Debrief]]
- [[2026-06-05-Submission-Infrastructure-Budget-Review-Planning]]
- [[2026-07-13-New-WM-Dev-Team-Weekly-Meeting-Effort-Roundtable-and-Use-Case-Boundaries]]
- [[2026-08-26-CMS-OC-Weekly-Meeting]]
- [[2026-09-03-New-WM-Dev-Team-Weekly-Meeting]]
- [[2026-09-03-Submission-Infrastructure-Weekly-Meeting]]
- [[2026-09-04-Marco-WM-Level-2-Transition-and-SI-Priorities]]
- [[2026-09-08-Submission-Infrastructure-Weekly-Meeting-Team-Planning-and-Project-Roadmap]]
- [[2026-05-06-WM-Dev-Team-Weekly-Meeting-Data-Placement-and-SI-Requirements-Review]]
- `40-References/CMS/LHCC-Computing-Model-Review-2021/` (main.tex, CSW_Main.tex, CSW_Appendix_Content.tex — checked for historical framing comparison; see note above)
