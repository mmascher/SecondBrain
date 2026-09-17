---
type: concept
---

# Site Token Authentication Migration for Pilot Submission

## Overview

Between roughly March and September 2026, CMS's [[Submission Infrastructure]] team migrated pilot-submission authentication to Compute Elements from grid-proxy (X.509/GSI) credentials to site-token (JWT/SciToken) credentials, as part of [[glideinWMS]]'s broader shift to token-based authentication. This was a discrete, multi-month infrastructure migration with concrete before/after states, several named regressions and their fixes, and an explicit end-of-period teaching moment in which proxy-based authentication was presented to a new team member as purely historical. It sits within a longer-running, CMS/WLCG-wide token-transition effort that began years earlier.

## Current Understanding

### Drivers

Several distinct drivers are documented, and the corpus is explicit that not all of them held up under scrutiny:

- **WLCG-coordinated milestone timeline** ("M1"–"M9"): described as the pacing mechanism for the broader token transition, though Marco Mascheroni was himself uncertain in March 2026 whether the timeline he recalled ("M5," roughly HTCondor GSI support ending) was still current, and planned to check with WLCG contacts.
- **Loss of SSL-client-certificate support** in a dependency used by CMS's backup front ends (Tier-0 and Global Pool), with the backup front end's certificate renewal giving less than a year of runway — this concretely prompted an inventory of proxy-authenticated entries in April 2026.
- **HTCondor 3.11 removing the proxy-fallback behavior**: pre-3.11, HTCondorCE automatically fell back to X.509 proxy authentication if a site token wasn't configured; 3.11 removed this fallback, making the token migration a practical prerequisite for any front end — CMS or otherwise — to upgrade. This specifically blocked Fermilab's non-CMS VOs (which share sites with CMS) from adopting 3.11.
- **A Fermilab certificate-authority (CA) change** was raised twice as a possible forcing function, and both times investigated and **concluded to be unrelated** — a distinct issue from an earlier CA/browser-ecosystem change that had broken host-certificates-used-as-client-certificates for some unrelated OSG services. This is an example of a driver that did not hold up and should not be conflated with the real drivers above.
- **Historical/background drivers** (from a 2022 presentation predating this migration window): moving toward industry-standard, capability-based authorization; the retirement of the Globus Toolkit (OSG 3.6, May 2022) and HTCondor's GSI end-of-life (November 2022) as the original deadlines that started the broader CMS token effort.

### Timeline

An inventory of proxy-only entries was requested in April 2026, followed by a deliberate CMS holdoff on Condor-CE token testing pending non-CMS rollout experience, then active ITB (integration test bed) testing from late April. A HTCondor 3.11 regression — removing the 3.10-era workaround that allowed both proxy and token credentials to coexist on an entry — caused breakage at IN2P3 and MIT in June 2026. A further 3.11.4 bug caused front ends to ship only one of two configured credentials per group (rather than both), which led the team to hold off upgrading production front ends to the 3.11 series until fixed upstream, even though the underlying Compute-Element-side migration continued. MIT's token-to-Unix-user mapping issue persisted for months and required repeated rollback of specific MIT Compute Elements to grid-proxy authentication as an interim fix. By mid-July 2026, Condor-CE site-token work was declared essentially complete, with remaining focus shifting to ARC/EGI sites, which lack an OSG-style RPM-based mapping mechanism. By early September 2026, all known factories — including CERN's — had migrated to glideinWMS 3.11, though the CMS Frontend itself remained on 3.10 in production, and the overload/oversubscription logic was found to be broken under the new 3.11 front-end/factory communication protocol. By mid-September, the three-token model (Frontend-to-Factory, Factory-to-site, worker-node-to-collector) was taught to a new team member as the current, normalized baseline.

### A distinct, concurrently-tracked issue: WMAgent and Condor 25

Surfacing in the same September 2026 meeting as the token-migration status update, but **explicitly a different problem**: HTCondor 25 rejects `condor_submit` invocations made under the reserved OS user `condor`, which broke WMAgent test submissions. The fix is for WMAgent to submit as its designated service accounts (`cmst1` at CERN, `cmsdataops` at Fermilab) rather than as `condor` — a WMAgent/deployment-side change, not part of the pilot-authentication migration. This should not be conflated with the site-token work even though both surfaced around HTCondor version upgrades in the same period.

## Disagreements / Open Questions

- **EGI/ARC site-mapping mechanism remains unclear.** Unlike OSG, where site-token-to-Unix-user mapping is distributed as an RPM through the same repositories used for glideinWMS/HTCondor, it is unclear who is responsible for an equivalent mapping mechanism on EGI-flavor sites, particularly for ARC CEs. As of late July 2026 this was an open gap, with Luis Simas proposing to investigate an EGI-distributable package as an alternative to opening individual per-site tickets — not resolved in the corpus.
- **JINR low core utilization** was initially suspected to be a consequence of the token migration but was determined, via live investigation, to be a demand-side issue (low CMS-side job "pressure" toward that site, not a drop in offered resources or an authentication failure). This distinction is explicit in the source material and should not be conflated with the migration's technical regressions.
- The repeated technical surprises during the migration (3.11 regressions, the front-end credential-shipping bug, MIT's persistent mapping issue) suggest the rollout was executed more cautiously, and took longer, than originally anticipated, though no source explicitly frames this as a planning failure.

## Relationships

- An operational/security workstream layered directly on [[GlideinWMS Pilot-Based Resource Provisioning]]'s Factory/Frontend/CE architecture.
- Time-correlated with, but causally independent of, the staffing changes described under [[Submission Infrastructure]].

## Sources

- [[2026-03-26-1005-GlideinWMS-Entry-Troubleshooting-and-Site-Token-Migration]]
- [[2026-04-01-GlideinWMS-Meeting]]
- [[2026-04-21-OSG-Factory-Ops-Meeting]]
- [[2026-04-28-OSG-Factory-Ops-Meeting]]
- [[2026-05-19-OSG-Factory-Ops-Meeting]]
- [[2026-06-23-GlideinWMS-Architecture-Training-and-Site-Token-Migration-Status]]
- [[2026-06-23-OSG-Factory-Ops-Meeting]]
- [[2026-06-24-GlideinWMS-Meeting]]
- [[2026-06-30-OSG-Factory-Ops-Meeting]]
- [[2026-07-07-OSG-Factory-Ops-Meeting]]
- [[2026-07-14-OSG-Factory-Ops-Meeting]]
- [[2026-07-21-OSG-Factory-Ops-Meeting]]
- [[2026-07-28-OSG-Factory-Ops-Meeting]]
- [[2026-09-09-GlideinWMS-Meeting]]
- [[2026-09-15-GlideinWMS-Token-Authentication-JINR-Pressure-and-WMAgent-Condor25-Prep]]
- `60-Presentations/20220401 Token Migration - Submission Infrastructure.pdf`
- `20-Meetings/CMS Token Transition.pdf`
