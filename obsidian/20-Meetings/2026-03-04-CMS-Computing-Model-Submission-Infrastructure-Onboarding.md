---
type: meeting
date: 2026-03-04
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Luís Simas
  - Florian Von Cube
  - Vaiva Zokaite
topics:
  - CMS computing model overview
  - online vs offline processing
  - Tier-0 / production / analysis
  - Monte Carlo simulation
  - WMAgent and Request Manager
  - pilot model and glideinWMS
  - factories and front-ends
  - high availability
  - team structure
  - onboarding logistics
---

# CMS Computing Model & Submission Infrastructure Onboarding

## Summary

This was largely an onboarding/training session in which Antonio Perez-Calero Yzquierdo and Marco Mascheroni walked new team member Luís Simas through the CMS offline computing model and where Submission Infrastructure fits into it: the online-to-offline data path (HLT output → Tier-0 repacking/prompt reconstruction), the distinction between centrally-organized "production" (Monte Carlo simulation and data (re)processing via WMAgent/Request Manager) and user-driven "analysis" (via CRAB), and the pilot-based resource-provisioning model (glideinWMS entries, factories, front-ends, late binding). They also covered team structure, staffing, high-availability deployment (CERN/Fermilab), and practical onboarding logistics (recurring meetings, Indico/CMS registration, upcoming CMS computing week and CHEP conference). Florian Von Cube and Vaiva Zokaite joined briefly before leaving for other commitments.

## Decisions / Conclusions

- No capacity ceiling is imposed by Submission Infrastructure itself on the number of pilots submitted to a site; the team always tries to acquire as many resources as workload pressure justifies, relying on the site's own fair-share policy to cap/deny requests when a site is saturated by other virtual organizations.
- Among Submission Infrastructure's "customers," Tier-0 (prompt reconstruction and repacking) has the highest operational priority: failure to keep up with Tier-0 processing risks saturating the online data buffer and permanent data loss, whereas delays in centralized Monte Carlo production or user analysis are recoverable (at most causing schedule slippage, e.g. for conference deadlines).
- Repack jobs (which build the raw-data files from HLT output at P5) are considered even more time-critical than prompt reconstruction, since raw-data buffering at that stage is less organized and has a shorter safety margin.
- The resource-request model used is a "pull"/late-binding model (informally also called the pilot model, contrasted with the "vacuum model"): empty resource requests (pilots) are submitted to multiple sites, and the task/job is bound to whichever resource becomes available first, rather than being pushed to a pre-selected site.
- Matchmaking/pilot-submission cycles run on the order of minutes, so there is no significant inherent delay in acquiring resources once jobs enter a queue; a job pending for hours generally indicates saturation (demand exceeding a site's available slots for that job type) rather than a problem in the pilot-submission machinery.

## Action Items

- [ ] Send Luís Simas an LLM-generated summary of the full Zoom transcript of this meeting (Marco's recording missed the first ~15 minutes) — Marco Mascheroni
- [ ] Send Luís Simas the Mattermost link needed to access the CMS general computing meeting (Wednesdays 3pm), since he cannot yet access the restricted Indico category — Marco Mascheroni
- [ ] Get registered/associated as a CMS member (associate CERN computing account with the CMS group) in order to access restricted Indico categories and meetings — Luís Simas

## Discussion

### Online-to-offline data path and Tier-0

The LHC produces collisions at a 40 MHz bunch-crossing rate; the hardware trigger and High-Level Trigger (HLT) filter this down to an output on the order of a few–10 kHz, meaning the large majority of events are rejected online before reaching offline computing. By the time data leaves the HLT, no further event filtering occurs offline — offline processing reconstructs all events it receives. The Tier-0, physically at CERN but logically part of the grid (distinct from "P5," the online detector site), performs event building/repacking (assembling sub-detector fragments into raw files), stores data to disk and tape, replicates a copy to Tier-1s, and performs prompt reconstruction (converting raw detector hits into physical objects such as tracks and momenta). The repack step is what bridges online to offline and produces the raw data files; before repacking, data exists in less-organized buffers, not yet on tape.

### Production vs. analysis

CMS offline data processing is organized into two categories:
- **Production**: large, centrally organized campaigns (Monte Carlo simulation and data reprocessing) run by a small set of experts via the Request Manager and WMAgent, taking days to weeks and consuming the majority of resources (Antonio cited roughly 80% of resources as a rough order of magnitude for centrally-run production/Tier-0-type work, though exact shares vary by resource pool).
- **Analysis**: individually or group-driven, comparatively unpredictable in timing and target datasets, submitted via CRAB by roughly 400 physicists.

Both are distinct from Tier-0 processing, though all three consume resources from the same underlying Submission Infrastructure pools (rather than separate dedicated infrastructures). Marco noted that Submission Infrastructure defines resource shares between these categories — e.g., at CERN a large majority share was described as dedicated to Tier-0 with the remainder split between production and analysis, and at Tier-1s the split was described as split differently (skewed heavily toward production); the exact percentages given in the discussion were not fully clear/consistent in the transcript and should be treated as illustrative rather than precise.

The Request Manager is the software layer that collects processing/simulation requests (workflows, defined as a set of CMSSW algorithm steps to run); WMAgent is the agent that executes production workflows. Submission Infrastructure does not manage the Request Manager itself but provides the compute resources that WMAgent-driven jobs run on.

### Monte Carlo simulation

Antonio explained Monte Carlo (MC) as the statistical simulation method (originating from the probabilistic nature of quantum mechanics) used to generate simulated ("fake") data based on a hypothesized physical model (e.g. variants of the Standard Model). Comparing real detector data ("experimental data") against Monte Carlo predictions is how CMS tests physics hypotheses, since there is no way to compare a theoretical equation directly against reality. MC simulation must also model the detector response (radiation interacting with detector layers, producing digitized signals) so simulated data is comparable to real raw detector data. Monte Carlo production is computationally heavy and enters Submission Infrastructure through the same WMAgent/Request Manager production path.

### Submission Infrastructure's role and resource-provisioning model

Submission Infrastructure does not handle CMS data movement or storage; its scope is acquiring and allocating compute resources. It interacts with grid sites via their **compute elements** (CEs) — as opposed to **storage elements** (SEs), which are out of scope. A site's CE, combined with an SI-defined usage configuration (memory per core, wall-clock runtime, whole-node vs. fixed-size slots, etc.), defines what SI calls an **entry** — effectively a submission point through which pilot jobs can be sent to acquire resources. This configuration is an agreement between the CMS virtual organization (VO) and the resource-providing site.

The model works as a pull/late-binding system: SI submits pilot jobs (resource requests, not tasks) to compute elements based on current queue pressure at CMS access points; whichever site grants resources first "wins" the pending task, with actual task-to-site binding happening only once resources are acquired (as opposed to a push model where a task is pre-assigned to one site). Idle jobs at access points are first split by SI's own fair share (Tier-0 / production / analysis); the resulting pilots then queue at each site's compute element alongside pilots from other VOs (CMS, ATLAS, other experiments), where the site applies its own fair-share policy. SI does not impose resource caps on itself; enforcement of saturation limits is the site's responsibility. Because SI never has zero workload pressure, it always tries to acquire as many resources as it is entitled to under fair share, rather than self-limiting.

Marco distinguished this from the "vacuum model" (pilots that appear and immediately vacate if there's no work) — SI's approach only sends pilots in response to actual queued demand (e.g., GPU pilots are only sent to GPU-capable resources when there are GPU-requesting jobs queued, to avoid wasting shared GPU capacity that other experiments could use).

Matchmaking/pilot-acquisition cycles operate on the order of minutes: the system continuously re-checks queue content and resubmits pilots as needed, so there's no meaningful built-in delay between a job entering a queue and a pilot being requested for it. A job pending for many hours typically indicates saturation (e.g., a task type restricted to a site that is already at its resource ceiling) rather than a fault in the pilot-submission mechanism. There is no fixed relationship between a pilot's lifecycle and a task's lifecycle — a single pilot can run many tasks over its lifetime.

### Frontier

The Frontier layer, which provides remote access to databases needed to process detector data, is a separate but related "connective tissue" component of the grid, alongside Submission Infrastructure's compute-resource-routing role. It was noted this may be a separate area of responsibility for Luís (in addition to Submission Infrastructure duties).

### Terminology note: overloaded terms

Antonio flagged that terms like "Tier-0" are overloaded — referring simultaneously to a physical location (CERN), a function (prompt reconstruction/repacking), and a team (the Tier-0 operations team). These don't always coincide: for example, "Tier-0 tasks" (prompt reconstruction responsibility) can run at Tier-1 sites when Tier-0's own CERN resources are insufficient to keep up with the incoming data rate (e.g., after a luminosity increase), a practice that emerged after CMS moved away from a strict decades-old division where Tier-0 only ran Tier-0 work, Tier-1s only did processing/storage, and Tier-2s only did Monte Carlo production. This flexibility (including moving Tier-0 tasks as far as Fermilab in the US) was adopted because it was judged beneficial for CMS overall, given sufficiently fast networking between sites.

### High availability and infrastructure redundancy

The core Submission Infrastructure machinery (the decision-making "control plane" that creates pilots) is deployed redundantly: a primary instance runs at CERN with an always-running secondary/standby instance at Fermilab (primary/secondary or master/slave model), so that a CERN-side problem (e.g. network) does not stop the whole system. Similarly, there are at least 3–4 glideinWMS pilot factories running in parallel (CERN, Fermilab, and at least one more in the US) for redundancy and scalability. Factories are multi-experiment (shared infrastructure serving CMS, ATLAS, OSG/Dune, etc.), whereas the front-end (which decides when to request pilots) is experiment-specific — CMS runs its own front-end. The team's Friday factory-operations meeting with Jeff (who leads the US, multi-experiment factory operations) covers deploying new factory/glideinWMS versions and site-specific issues, distinct from the CMS-specific front-end work the SI team owns directly.

### Team structure and staffing

The Submission Infrastructure team is small — typically around 5 people minimum: Antonio and Marco, two positions at CERN, and one person at Fermilab. Responsibility is split, with roughly one full FTE dedicated to the "core" Condor components (currently Florian) and roughly 0.5 FTE dedicated to the factory-building component (the transcript's attribution here — referencing Vaiva and Luís — was unclear and should not be taken as definitive). Because the team lacks 24/7 human coverage but the mission runs 24/7, the team relies heavily on monitoring, documentation, redundancy (primary/secondary deployment), and scalability testing to keep the infrastructure stable without constant supervision.

### Onboarding logistics

Antonio recommended Luís attend the Monday 4pm facilities/site meeting, the Monday 5pm computing-operations meeting, and the Wednesday 3pm CMS general computing meeting, primarily to build familiarity rather than to actively report. Luís does not yet have full CMS-member registration in Indico, so he could not access the (CMS-restricted) meeting category during the call; he needs his computing account associated with the CMS group. Antonio and Marco noted the value of being physically present at CERN (versus remote work) for organic knowledge-building through team interaction. Luís is already listed on the agenda to give a short self-introduction at the upcoming spring 2026 CMS Offline & Computing Week (occurring twice yearly, spring/autumn, a couple of weeks from this meeting); Antonio noted future opportunities to present actual work results at the Wednesday general computing meeting once available. The CHEP (Computing for High Energy Physics) conference, held roughly every 1.5 years, was also mentioned as upcoming in May 2026, with the team expecting to have results/talks prepared for it.

## Open Questions

- What are the precise, current resource-share percentages between Tier-0, production, and analysis at CERN and at Tier-1s? (The figures mentioned in the meeting were inconsistent/unclear.)
- What exactly is the current FTE/role split within the SI team for the factory-building component, and who currently holds it (the transcript's attribution was unclear)?
- (Raised by Luís, deferred) What is the recovery time / potential job loss window during a primary→secondary high-availability failover?
- (Raised by Luís, deferred to the other "Antonio," the Tier-0 operator) How many hours of buffer exist at Tier-0 before data loss risk begins?

## Related

[[CMS]] · [[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[WMAgent]] · [[CRAB]] · [[Pilot Jobs]] · [[Factory]] · [[Factory Operations]] · [[Resource Provisioning]] · [[Frontier]] · [[WLCG]] · [[CERN]] · [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-04 11.43.28 Submission Infrastructure Weekly Meeting`)
