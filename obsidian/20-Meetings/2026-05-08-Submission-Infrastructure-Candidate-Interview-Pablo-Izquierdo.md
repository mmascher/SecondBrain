---
type: meeting
date: 2026-05-08
participants:
  - Stephan Lammel
  - Marco Mascheroni
  - Antonio Perez-Calero Yzquierdo
  - Phat Srimanobhas
  - Pablo Izquierdo
topics:
  - candidate interview for open Submission Infrastructure position
  - candidate background: Tier-2 (IFCA/Cantabria) system administration, ARC/Slurm, GPU benchmarking (BSC internship)
  - CMS Global Pool / HTCondor / glideinWMS overview for candidate
  - position logistics: location, start date, fixed-term duration
  - panel debrief and assessment of candidate
  - brief internal discussion about giving Luis Simas visibility for his work
---

# Submission Infrastructure Candidate Interview — Pablo Izquierdo

## Summary

This meeting was primarily a candidate interview for an open position in the CMS [[Submission Infrastructure]] group, conducted by Stephan Lammel and Phat Srimanobhas (computing coordination) together with Antonio Perez-Calero Yzquierdo and Marco Mascheroni (Submission Infrastructure conveners). The candidate, Pablo Izquierdo, is currently an assistant system administrator at the IFCA Tier-2 site in Cantabria, Spain, responsible for grid/HTC infrastructure (ARC CEs with a Slurm backend, [[CVMFS]], [[XRootD]], Squid). The panel explained the role (operating and maintaining the CMS Global Pool, a [[HTCondor]]-based pool built with [[glideinWMS]] that aggregates worker nodes from roughly 180 Tier-1/Tier-2 sites via [[Pilot Jobs]]) and discussed the candidate's technical background, tooling experience, debugging approach, scalability experience, and logistics (relocation to Geneva/CERN, notice period, fixed-term contract length). The interview closed with candidate questions about team structure, work environment, hardware access, and expectations for the first months. A short panel-only debrief followed, with generally positive impressions and a couple of open concerns. The recording also opened with a brief, unrelated internal exchange between Marco, Antonio, and Stephan about giving Luis Simas more visibility for his work.

## Decisions / Conclusions

- The panel (Marco, Antonio) proposed, and Stephan agreed in principle, that Luis Simas should be given visibility for his work — e.g. presenting his work on pilot overloading and pilot monitoring at a Wednesday meeting, potentially before the CMS offline computing week (referenced as being before July/August) rather than waiting for it. Stephan stated he did not fully follow the specifics but supports giving Luis visibility for anything he has worked on and can present.
- No hiring decision was made in this meeting; the panel noted they have "just started" the interview process and that a decision may take a while.

## Action Items

- [ ] Send the link to the GPU benchmark repository/tool worked on during the BSC internship (transcript unclear on the exact name — heard as "Ximenome benchmark" and later "Hibino Benchmark") to Marco, by email — Pablo Izquierdo

## Discussion

### Position and team overview (given to the candidate)
- CMS operates the [[CMS Global Pool]], a central [[HTCondor]] pool built using [[glideinWMS]], aggregating worker nodes from roughly 180 Tier-1 and Tier-2 sites via [[Pilot Jobs]] sent to sites' compute elements.
- The Submission Infrastructure team is small (~5 people), distributed (Antonio in Barcelona, Marco frequently remote), and works alongside a larger CERN-based CMS DevOps/computing team of about 15–20 people running core CMS computing elements (mentioned examples: FTS, XRootD/"X4D", the Global Pool).
- The role would be based at CERN; some fraction of teleworking is allowed by standard CERN policy. CERN IT provides the underlying physical/virtual machine infrastructure; the team administers configuration and services on top (mostly via VMs), without direct hardware contact except in rare cases requiring physical machines.
- The position is fixed-term, typically around 2 years, with possible extension; the panel described it as potentially opening further opportunities within CMS computing or other research institutions afterward.
- New hires go through an induction process where goals for the first ~5–6 months are agreed jointly, and training/courses are available.
- The main ongoing responsibility is keeping the always-on (24/7) data processing/simulation infrastructure running reliably; additional "side project" time is available for infrastructure improvements (scalability, efficiency, resource utilization) as capacity allows.
- The team maintains close contact with HTCondor developers.

### Candidate background
- Currently assistant administrator (~2 years) at the IFCA Tier-2 in Cantabria, responsible for the site's grid/HTC computing: ARC compute elements with a Slurm batch backend, [[CVMFS]] (including proxy generation/updates), [[XRootD]] pools, and some involvement with Squid.
- IFCA's infrastructure group has ~5 people, each generally responsible for a different area (grid, cloud, storage/GPFS), with close collaboration and some overlap (e.g. Pablo also occasionally helps manage HPC/Slurm nodes shared with the grid).
- Tooling used at IFCA: [[Puppet]] (recently upgraded to Puppet 8 and PuppetDB) for configuration management; Grafana/Prometheus and collectd for monitoring; Icinga-type alerting; Bacula for backups; Jira for ticketing (rotating on-call shift for grid-user tickets); starting to learn and adopt [[Terraform]] for infrastructure deployment.
- Scalability approach at IFCA: virtualizing grid nodes via [[OpenStack]] to flexibly add capacity, using general-purpose parallel file systems, and adding Slurm queues as needed; high availability achieved via duplicated ARC servers. Bottlenecks are identified through infrastructure meetings covering network bandwidth and storage connection limits.
- No hands-on production experience specifically with HTCondor, but familiar with the underlying concepts due to similarity with ARC/Slurm.
- Described a debugging case: after volunteering to test ARC7 (upgrading from an older ARC version) together with a Slurm 25 upgrade, jobs stopped being scheduled. Root causes were (1) an ARC configuration change needed for ARC–Slurm communication after the Slurm upgrade, and (2) a permission-denied issue traced to proxy generation in ARC, resolved after contacting ARC developers, since a previously modified/patched version of that component had been overwritten by the update.
- Prior experience includes a BSC (Barcelona Supercomputing Center) summer internship on GPU architecture and CUDA parallel programming, adapting an existing (community-maintained, CPU-oriented) benchmark to run on GPU to compare performance for large-data matrix operations; also some earlier development of an AI tool for image processing.
- Candidate described himself as balancing both developer and system-administrator roles and enjoying both.
- Visited CERN once before (November, during a "third school of computing" / computing school), including the data center.

### Logistics
- Candidate is based in Santander; open to relocating to Geneva.
- Requires roughly 15 days' notice at his current job; earliest realistic availability is around June, with July also acceptable — consistent with the position's target start date (mentioned in the application documentation as around June).

### Candidate questions
- Asked about the working environment (remote/telework vs. office) — panel described a good, collaborative, largely young team, with some in-person events, and encouraged being on-site for cross-team visibility.
- Asked about hardware access — panel clarified CERN IT manages physical infrastructure; the role is primarily administering configuration/services on VMs provided by CERN IT.
- Asked what would be expected of him after ~3 months — panel reiterated the main expectation is helping keep the existing, already fairly mature system running reliably, with room for improvement projects over time.

### Panel debrief (after candidate left the call)
- Overall impression was positive: profile and experience were seen as well aligned with the position, and communication was rated positively.
- Marco and Antonio noted the transition would be close to immediate given the similarity between ARC/Slurm/Condor concepts, though some ramp-up on HTCondor specifics would be needed.
- Prior GPU/HPC experience at BSC was seen as a positive additional asset.
- Antonio raised, as an observation, that IFCA's Tier-2 has historically not been among the most stable sites, though this was not attributed specifically to Pablo's responsibility.
- Stephan noted it seemed somewhat surprising that a candidate about a year and a half into his current job would move to what he characterized as an "intern type" (fixed-term) position; Antonio offered as a possible (unconfirmed) explanation that the candidate's current position at IFCA might itself be project-funded/fixed-term, combined with the general attractiveness of CERN/Geneva and its salary levels compared to Spain.

### Earlier, unrelated discussion (start of recording)
- Marco and Antonio expressed satisfaction with Luis Simas's performance on the team, describing him as self-motivated and autonomous. Stephan agreed. This led to the proposal (see Decisions/Conclusions) to give him a presentation opportunity.

## Open Questions

- What kind of position (fixed-term vs. indefinite) Pablo currently holds at IFCA was not established; Stephan raised this as a point of mild surprise but it was left unresolved ("I don't know a specific[s]... it's a specific case").
- No concrete timeline was given for the remaining hiring process beyond "we just started" and that it "might take a while."

## Related

[[Submission Infrastructure]] · [[CMS]] · [[CERN]] · [[HTCondor]] · [[glideinWMS]] · [[Pilot Jobs]] · [[CVMFS]] · [[XRootD]] · [[OpenStack]] · [[Puppet]] · [[Terraform]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-08 11.42.56 Stephan Lammel's Zoom Meeting`)
