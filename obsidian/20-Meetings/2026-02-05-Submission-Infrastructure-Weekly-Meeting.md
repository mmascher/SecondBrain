---
type: meeting
date: 2026-02-05
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Florian Von Cube
  - Vaiva Zokaite
topics:
  - scheduler scalability testing
  - glideinWMS 3.11.3
  - overloading monitoring
  - Kubernetes integration
---

# Submission Infrastructure Weekly Meeting

## Summary

The meeting focused on scheduler scalability results. Tests reached up to 500,000 submitted jobs and 70,000–80,000 running jobs on a 196 GB host, with memory as the observed limit rather than CPU, disk, or scheduler duty cycle. The group also discussed testing glideinWMS 3.11.3 and potential Kubernetes integration.

## Decisions / Conclusions

- Version 3.11.3 had been tested in ITB sufficiently to propose deployment to production on the following Monday.
- The scale-test host’s practical running-job limit was estimated at roughly 70,000–80,000 jobs, consistent with approximately 2 MB per running job.
- The second test actually submitted 500,000 jobs, not the 700,000 reported in the initial slides, because of the configured submission limit.

## Action Items

- [ ] Correct the scale-test slides to report 500,000 submitted jobs — Florian Von Cube
- [ ] Reply to the Beijing site about the certificate required for its proxy configuration — Marco Mascheroni

## Discussion

### Infrastructure, releases, and integration

Negotiation-cycle time had improved from the previous week, although one Tier-2 scheduler still took too long. Marco reported that 3.11.3 would expose pilot start/end time, CPU utilisation, core count, and overloading state in one record, enabling more reliable efficiency calculations. The transcript noted that some site or batch-system versions might need investigation.

The group also discussed Condor’s Bosco layer as a possible way to reach Kubernetes-based batch systems, including a system referred to as Kueue. This was exploratory; CMS did not yet have a concrete cluster to integrate. A Chinese site behind a proxy needed a certificate whose hostname covered the front-facing node.

### Scale-test results

The test scheduler had 196 GB RAM, 64 threads, and 2 TB disk. A first test submitted 200,000 eight-hour jobs and capped running jobs at 80,000. A second test had a planned total of 700,000 jobs but hit the configured maximum-submitted-jobs limit at 500,000; it ran at 70,000 after an initial 80,000-job interval.

Memory approached the host limit; CPU, disk, networking, and scheduler duty cycle did not show comparable saturation. Duty cycle remained below 0.6, while short jobs increased job start/completion rate. Participants proposed stressing auto-clustering and negotiation with more diverse job requirements and site lists, then testing job sandbox transfer in a controlled manner.

### Factory and monitoring updates

The ITB factory was updated. A Finnish site had returned to testing and was asked whether it wanted production re-enablement. The group discussed excluding static I/O slots from efficiency-oriented monitoring plots, but no completed Grafana solution was reported.

## Open Questions

- Can memory capacity be scaled or managed to raise the running-job limit safely?
- How do short job durations, auto-cluster diversity, and claim reuse affect negotiator load?
- What sandbox-transfer test realistically represents CMS workloads without harming remote workers?

## Related

[[CMS]] · [[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[Kubernetes]] · [[Monitoring]] · [[Work Queue]] · [[I/O Slots]]

## Source

meeting_saved_closed_caption.txt (from `2026-02-05 17.06.30 Submission Infrastructure Weekly Meeting`)
