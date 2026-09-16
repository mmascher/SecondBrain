---
type: meeting
date: 2026-05-19
participants:
  - Stephan Lammel
  - Marco Mascheroni
  - Antonio Perez-Calero Yzquierdo
  - sanji (candidate)
topics:
  - candidate interview for open Submission Infrastructure position
  - candidate background: personal/academic batch-scheduling simulation project
  - CMS Submission Infrastructure / HTCondor / glideinWMS overview for candidate
  - Linux administration and configuration management (Puppet)
  - monitoring and resource-utilization efficiency
---

# Submission Infrastructure Candidate Interview — sanji

## Summary

This meeting was a candidate interview for an open position in the CMS [[Submission Infrastructure]] group, conducted by Stephan Lammel, Marco Mascheroni, and Antonio Perez-Calero Yzquierdo, with a candidate identified in the transcript only as "sanji." Stephan opened with a brief overview of CMS computing needs and the submission infrastructure operator role. Marco and Antonio then questioned the candidate about a personal/academic project simulating a small-scale batch scheduling system, compared it to the real CMS pool architecture, and asked about Linux administration, configuration-management, and monitoring experience. The transcript ends mid-interview (the candidate was describing efforts to skill up on testing/reliability topics); no closing discussion, debrief, or hiring conclusion is present in the available transcript.

## Decisions / Conclusions

None. No hiring or process decision is recorded in the available transcript.

## Action Items

None stated in the transcript.

## Discussion

### CMS computing overview (given to the candidate)
- Stephan described CMS's detector data-taking: only a subset of events is recorded, selected and read out at roughly 10 kHz, corresponding to about 10 gigabytes per second of charge/timing data, which must be reconstructed into physics information for analysis.
- This requires large computing resources: Stephan cited a pool of roughly half a million CPU cores and about a quarter of an exabyte of disk space in continuous use, with resources scattered across roughly 100 sites worldwide, joined into what looks like one large batch system.
- Later in the meeting, Marco separately described the pool as distributed "over 70 different sites," referred to as 70 distributed computing centers. The transcript does not reconcile the two site-count figures given by Stephan and Marco.

### Submission Infrastructure architecture (explained to the candidate)
- Antonio explained that submission infrastructure acquires compute resources from the grid — a globally distributed network of interconnected data centers providing compute slots and storage — and builds a virtual pool from them; it also manages the pool of jobs/requests and performs matchmaking between jobs and resources.
- Two technologies are used: [[glideinWMS]], the resource-acquisition mechanism, and [[HTCondor]], used to build the Condor pool itself.
- Marco described the "pilot" model: worker nodes are geographically distributed but run no process until resources are explicitly acquired (including authorization); glideinWMS sends "pilot"/"glidein" jobs to worker nodes, which then start a Condor process there.
- Marco described the four HTCondor processes needed to run a job: schedd (where jobs are submitted/queued), startd (where jobs actually run), and two processes that oversee matchmaking — the collector and the negotiator. The worker node (startd) opens and keeps open a persistent TCP connection to the negotiator, which performs the negotiation, before the job is acquired.
- Antonio noted that, compared to the candidate's academic simulation (~100–200 worker nodes, ~500 tasks over ~2 months), the real system runs at a much larger scale — tens of thousands of jobs, with peaks around 100,000 jobs running simultaneously.

### Linux administration and configuration management
- Antonio described the team's responsibility for a number of virtual and physical machines: CERN IT (CENIT, as transcribed) provides the basic infrastructure, but the team maintains packages, keeps configuration up to date, and runs the required services on top.
- Antonio asked about experience with [[Puppet]] for automating consistent configuration ("profiles") across machines, including package management. The candidate said their Puppet experience was very basic/early-stage, and mentioned also starting to learn Ansible.
- Marco asked about direct experience being responsible for operating and maintaining a service (installing updates, checking logs, ensuring stability) as an operator, distinct from general troubleshooting participation.

### Monitoring and resource-utilization efficiency
- Antonio stated that, besides scalability, efficient resource utilization is critical to the mission, which requires monitoring to identify and minimize causes of inefficiency, and asked about the candidate's related experience.
- Antonio noted that the monitoring tools mentioned by the candidate (Grafana, Prometheus) are also used in submission infrastructure operations.
- Antonio asked whether the candidate had experience building an end-to-end monitoring chain (metrics design, time-series ingestion, dashboarding); the candidate said their experience was limited to consuming basic worker-node metrics via Prometheus/Grafana and had not built a monitoring chain from scratch.

### Candidate background (as described by the candidate)
- Completed a Master's in computer systems at Northeastern University (Boston) about a year prior to the interview (around April of the previous year); background emphasized Linux systems debugging, monitoring, and automation.
- Described a personal/academic project (not affiliated with a company, not published to a public repository) simulating a small-scale distributed batch scheduling system: worker nodes and jobs run in Docker containers on a university-provided lab machine, using a Redis-based task queue with priority/preference-based scheduling, Prometheus for worker-node metrics, and Grafana dashboards; code was mostly Python with some backend components in Go.
- Scale of the simulation: roughly 100–200 worker nodes and around 500 tasks (described as video-simulation-type jobs) over about two months; jobs had varied resource requirements (lightweight/short vs. intentionally heavier/longer-running) to exercise different scheduling scenarios.
- Described debugging a case where jobs were delayed despite workers appearing healthy; root cause was traced to heavier tasks being repeatedly assigned to the same workers, driving up CPU/memory usage on those workers and causing queue backlog. Approach involved tracking queue depth, job execution time, retry counts, and worker health metrics (CPU/memory) to distinguish resource-pressure issues from scheduling/queue-behavior issues, followed by automating fixes with Python and shell (Bash/"SKU batch," as transcribed) scripts, with alerting suppressed for transient issues that self-resolved quickly (to avoid false alarms).
- Described their profile as roughly 80% operator-oriented and 20% development-oriented, with development mainly in Python/automation scripting; expressed a preference for the investigative, root-cause-analysis side of operations work.
- Stated their motivation for applying to CERN was primarily the appeal of an international, collaborative, community-oriented organization rather than a purely research-driven motivation, alongside interest in working at large scale.
- Described the period since completing their Master's as spent job-searching and updating technical skills, including interest in incorporating AI-assisted testing/automation, having previously focused more on networking during their studies.

## Open Questions

- The transcript ends mid-interview (candidate describing recent skill-building efforts); it is unclear whether the interview continued beyond the available recording, and no panel debrief or outcome is captured.
- The pool's number of sites was stated inconsistently in the meeting (Stephan: ~100 sites; Marco: 70 sites/70 distributed computing centers) and was not reconciled in the transcript.

## Related

[[Submission Infrastructure]] · [[CMS]] · [[HTCondor]] · [[glideinWMS]] · [[Pilot Jobs]] · [[Puppet]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-19 19.03.07 Stephan Lammel's Zoom Meeting`)
