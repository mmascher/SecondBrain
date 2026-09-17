---
type: concept
---

# GlideinWMS Pilot-Based Resource Provisioning

## Overview

[[glideinWMS]] is CMS's established, in-production mechanism for acquiring and allocating compute resources — the execution layer underneath [[Submission Infrastructure]]. It implements a pull, late-binding "pilot" model: rather than pushing a specific task to a specific site, glideinWMS submits generic [[Pilot Jobs]] ("glideins") to Compute Elements, and only once a pilot is running and registered in the [[HTCondor]] pool does a real user/production job get matched to it. This is the most stable, best-corroborated architectural concept in the corpus — the same architecture, components, and lifecycle were independently re-explained, consistently, across training and walkthrough sessions spanning seven months, and it is explicitly slated to remain CMS's execution/pilot layer even as the workload-management layer above it changes (see [[CMS Adoption of DiracX for Future Workflow Management]]).

## Current Understanding

### Components

- **Glidein / pilot**: a job that, once landed on a worker node (execution point), configures and starts an HTCondor `condor_startd`/`condor_master`, joining the HTCondor pool as a resource. Glidein size (cores, memory) is statically defined in factory configuration, not derived from the eventual payload job. One worker node can host multiple concurrent glidein startups, each appearing as a separate execute machine.
- **Factory**: holds per-site submission details ("entries") in XML configuration, described as VO-agnostic/"dumb" — a "waiter" that does not itself decide glidein volume. An entry is a queue on a Compute Element (CE hostname/"gatekeeper" + batch queue). The Factory is shared across VOs/experiments (unlike the Frontend). It runs its own HTCondor collector that both Factory and Frontend publish ClassAds to.
- **Frontend**: performs the first stage of matchmaking — watching user jobs in the schedulers and deciding how many pilots to request from the Factory. Described as the "brain" of a glideinWMS pool. There is **one Frontend per experiment/VO**, driven by each experiment holding its own site-access credentials and its own HTCondor Access Points; CMS itself runs multiple Frontends, one per operational pool (global pool, Tier-0 pool, ITB test pool), each with its own central manager.

### CMS's factory topology

CMS uses 3 of 4 known glideinWMS factories: the **Fermilab factory** (CMS Tier-1 sites only, for reliability), the **"Tiger"/OSG factory** (CMS plus other VOs — DUNE, IceCube, LIGO — run on a Wisconsin Kubernetes cluster, managed by Jeff Dost), and the **CERN factory** (all CMS sites, managed by Luis Simas). This is deliberate, non-uniform redundancy — each factory exists for a distinct operational reason, not as identical replicas. CMS's core SI control plane is deployed primary (CERN) / standby (Fermilab).

### Communication model and matchmaking

Communication between Frontend and Factory is **pull-based**: the Frontend polls the Factory's HTCondor collector on the order of every ~10 minutes; there is no push. Matchmaking happens in two independent stages: (1) Frontend-to-entry — the Frontend's admin-defined match expression (implemented as a Python function, comparing job requirements against entry attributes) decides how many additional pilots to request per site; (2) Condor negotiator-to-pilot — once a pilot is running, the negotiator independently matches queued jobs against it. There is **no guarantee** that the job whose demand triggered a pilot request is the one that ends up running on it. CMS generally runs under "infinite pressure" (demand exceeding capacity) except for GPU jobs, where GPU pilots are deliberately requested only against actually-queued GPU demand, to avoid starving other experiments' shared GPU access.

### Pilot lifecycle

The full lifecycle — request, submission via Condor-G to the CE, `glidein_startup.sh` download and integrity verification (hash-checked against Factory/Frontend-published hashes), node validation (standard and VO-specific plugins; a validation failure triggers a deliberate 20-minute sleep before exit, to avoid a rapid-restart "black hole" that would overload worker nodes), Condor binary download and `condor_startd`/`condor_master` startup, slot advertisement as a partitionable slot, negotiation into dynamic slots, running (potentially multiple jobs over the pilot's life, with no fixed relationship between pilot and task lifecycle), and retirement — is documented in detail across dedicated walkthrough meetings and consistently re-taught to new team members over a seven-month span.

Retirement uses two distinct deadlines: `GLIDEIN_ToRetire` (a soft deadline after which the glidein stops accepting new jobs but lets running ones finish; scheduling decisions use this buffer) and `GLIDEIN_ToDie`/`GLIDEIN_Max_Walltime` (a hard deadline at which Condor force-exits the glidein, killing any still-running job). The retire buffer (roughly 4 hours) exists because declared job walltimes are unreliable and typically overestimated.

### Authentication

Authentication has moved fully from X.509 proxy-based mutual auth to a token-based model; see [[Site Token Authentication Migration for Pilot Submission]] for the detailed migration history. As of September 2026, three distinct tokens are used: Frontend-to-Factory, the Factory's glidein/pilot submission to sites, and worker-node-to-collector.

## Evolution

Terminology and diagrams were repeatedly found outdated or inconsistent when re-explained to new operators, indicating this is actively-maintained institutional knowledge rather than static, settled trivia:

- An older diagram showing the pilot containing the execution point (rather than the reverse) was corrected in a September 2026 training session.
- Older presentation material describing the pilot's temp directory as created in the current working directory was corrected live — the actual location is entry-configurable (`$condor_scratchdir`, `$OSG_WORKER_NODE_TMP`, or `$TMP`), and is shared across all glideins under the same StartD on a node rather than being per-pilot as one operator had assumed.
- Historically, each VO/Frontend mapped to a separate Unix account on the Factory; this is no longer the case — all VOs now share a single Factory Unix identity ("gfactory"), raising an unresolved security question about blast radius (see Open Questions).
- Old proxy-based mutual-authentication diagrams were declared fully obsolete in September 2026, replaced by the three-token model described above; this was the culmination of a multi-month migration (see [[Site Token Authentication Migration for Pilot Submission]]).
- GlideinWMS 3.11 removed a 3.10-era fallback behavior ("continue if no proxy") and changed `auth_method` semantics to allow only one credential type per entry — a breaking change that caused site outages during the token migration.

## Disagreements and Open Questions

- **"Immortal pilots"** — a proposal (Marco Mascheroni, building on an idea first raised by Luis Simas) to remove pilot wall-time limits entirely and rely on glideinWMS draining for retirement, aimed at reducing whole-node fragmentation/inefficiency near end-of-pilot-life. Discussed twice (May and September 2026); Jeff Dost raised concrete unresolved concerns — no state-saving/restart mechanism if the underlying machine reboots, ambiguity in fields that assume an eventual pilot end time, and a single-core-vs-whole-node sizing tradeoff. Three "showstopper" concerns were named: fragmentation, credential expiration (pilots normally get weekly-renewed credentials; a never-ending pilot complicates this), and accounting (currently collected at pilot finish). No decision to proceed; Marco described himself as "not so sure now" but still interested in trying it as an experiment.
- **Over-provisioning from multi-entry site matching** — Marco Mascheroni's own assessment is that per-job, entry-by-entry site matching causes unintentional over-provisioning that is "likely harmless and possibly beneficial," explicitly framed as opinion rather than settled conclusion.
- **Shared Factory identity ("gfactory") security concern** — raised by Marco Mascheroni and not answered by anyone else in the corpus: if a compromised Frontend could manipulate its own ClassAd, could it cause the Factory to act on its behalf in ways affecting other VOs sharing that Factory?
- **PanDA/DIRAC integration strategy** (pre-dating, and superseded in direction by, the DiracX decision) — Marco Mascheroni and Kenyi Hurtado Anampa disagreed over which of three integration strategies to recommend; not resolved in the meeting, deferred to a separate discussion.
- **HA (front-end failover) limitation** — investigating a CERN front-end firewall incident, the team found that automatic failover to the Fermilab backup front end did not trigger, because the primary process stayed up and kept sending ClassAds even though pilots could not actually download files over port 80. Jeff Dost concluded this class of failure is very hard to distinguish automatically from a partial/site-specific issue, and that HA "could never really work" for this kind of failure in the current design. Left as a known, unresolved architectural limitation.
- **Docker/Kubernetes container-escalation risk** under a kernel privilege-escalation vulnerability was left explicitly open — whether Docker/Kubernetes-based job containers (as opposed to Singularity, which is protected by its own UID-set mechanism) are vulnerable to host escalation was not confirmed by anyone in the corpus.
- **Distance-based matchmaking for data locality** — Marco Mascheroni sketched extending desired-site matching to allow jobs to run at "close" sites reading data remotely (inspired by DUNE's use of Rucio storage-element distances), but stated explicit dissatisfaction with expressing this as an HTCondor requirement expression; unresolved as of the corpus end date.
- **"Ghost pilots"** — a rare, never-fully-understood phenomenon (Jeff Dost) where pilots keep running and serving real jobs at a site with no corresponding record at the Factory.

## Relationships

- The execution/pilot layer that [[CMS Adoption of DiracX for Future Workflow Management]] is explicitly designed to sit on top of, not replace.
- Carries [[Site Token Authentication Migration for Pilot Submission]] as a major operational workstream layered on this same architecture.
- The pilot "overloading"/oversubscription mechanism inside this architecture is a concrete, measured lever discussed under [[CMS CPU and Resource Efficiency]], and is also the mechanical explanation for observed divergence between site-reported and payload-level efficiency figures.
- Sits under the broader computing-model framing described in [[Submission Infrastructure]] (the pull/late-binding pilot model, contrasted there with push/vacuum models).

## Sources

- [[2026-05-26-GlideinWMS-Architecture-Walkthrough]]
- [[2026-05-27-GlideinWMS-Pilot-Lifecycle-Walkthrough]]
- [[2026-06-23-GlideinWMS-Architecture-Training-and-Site-Token-Migration-Status]]
- [[2026-07-24-GlideinWMS-Factory-Architecture-Walkthrough]]
- [[2026-09-04-GlideinWMS-and-HTCondor-Architecture-Walkthrough]]
- [[2026-09-07-GlideinWMS-Factory-and-Frontend-Architecture-Follow-up]]
- [[2026-09-08-GlideinWMS-Frontend-Training-Terminology-and-Infrastructure-Walkthrough]]
- [[2026-09-15-GlideinWMS-Token-Authentication-JINR-Pressure-and-WMAgent-Condor25-Prep]]
- [[2026-03-10-GlideinWMS-Integration-PanDA-DIRAC-Slide-Prep]]
- [[2026-04-01-GlideinWMS-Meeting]]
- [[2026-04-22-GlideinWMS-Meeting]]
- [[2026-06-24-GlideinWMS-Meeting]]
- [[2026-07-08-GlideinWMS-Meeting]]
- [[2026-07-29-GlideinWMS-Meeting]]
- [[2026-09-09-GlideinWMS-Meeting]]
- [[2026-03-04-CMS-Computing-Model-Submission-Infrastructure-Onboarding]]
- [[2026-05-05-OSG-Factory-Ops-Meeting]]
- [[2026-05-19-OSG-Factory-Ops-Meeting]]
- [[2026-07-14-OSG-Factory-Ops-Meeting]]
- [[2026-07-21-OSG-Factory-Ops-Meeting]]
- [[2026-09-15-OSG-Factory-Ops-Meeting]]
- Additional OSG Factory Ops weekly meetings (2026-02-17 through 2026-09-15) provide operational corroboration of the architecture and lifecycle described above without introducing new architectural facts.

Note: two presentation PDFs referenced in the discovery pass ("Exploiting Kubernetes to Simplify the Deployment and Management of the Multi-purpose CMS Pilot Job Factory-6.pdf" and "Improving GlideinWMS Factory Compute Resource Configuration with Automation Tools.pdf") were checked and do not exist anywhere in the vault; they are not cited here.
