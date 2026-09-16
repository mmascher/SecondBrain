---
type: meeting
date: 2026-01-08
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Florian Von Cube
  - Vaiva Zokaite
  - Hyunwoo Kim
topics:
  - infrastructure status
  - Factory Operations
  - CVMFS exec
  - I/O slots
---

# Submission Infrastructure Weekly Meeting

## Summary

The first meeting after the year-end break reported stable [[Submission Infrastructure]] operations. The production factory and Global Pool frontend were upgraded to 3.10.17, while work continued on site tickets, native [[CVMFS]] exec support, I/O-slot rollout, and scheduler scalability testing.

## Decisions / Conclusions

- The production factory was upgraded to 3.10.17 and was reported healthy.
- The Global Pool frontend was upgraded; the CERN Pool frontend would remain on 3.10.15 for one or two weeks before an upgrade.

## Action Items

- [ ] Investigate pilots that validate but do not acquire claims at the DESY site — Vaiva Zokaite and Marco Mascheroni
- [ ] Check ticket-notification group membership and filters — Antonio Perez-Calero Yzquierdo and Marco Mascheroni
- [ ] Resume investigation of native CVMFS exec integration for the Portuguese HPC site — Marco Mascheroni
- [ ] Review the 100,000-job scale-test monitoring data — Marco Mascheroni and Florian Von Cube

## Discussion

### Operational and factory status

Operations were described as stable during the break. HLT resources were being drained for a planned firmware upgrade and P5 was not present. Factory work included GPU configuration for an Estonian site, new entries for another resource, and a resolved Korean worker-node validation failure. A DESY ticket showed pilots completing validation but not activating or claiming work; the cause was not yet known.

### CVMFS exec on HPC resources

The Portuguese HPC site currently uses CVMFS set up manually. The group discussed the [[glideinWMS]] native `CVMFS exec` feature, which can let a pilot set up CVMFS without site intervention. Validation scripts did not find the non-root CVMFS mount because they ran outside the container where the mount was exposed; wrapper and execution ordering were also unresolved.

### I/O slots and scalability

The group discussed re-enabling I/O slots after the relevant factory/frontend upgrades. A 100,000-job test had been submitted from one scheduler before the break, but detailed analysis was pending. The intended next stage was to establish limits using Tier-0-like and production-like scheduler hardware, including a mix of short and long jobs and testing the disk-backed job queue.

## Open Questions

- Why did DESY pilots validate successfully but fail to acquire claims?
- How can validation scripts use the CVMFS environment created inside the pilot container?
- What scheduler limits emerge from the 100,000-job test and a more realistic job mix?

## Related

[[CMS]] · [[Submission Infrastructure]] · [[Factory Operations]] · [[glideinWMS]] · [[CVMFS]] · [[HPC]] · [[GPU]] · [[HTCondor]]

## Source

meeting_saved_closed_caption.txt (from `2026-01-08 17.06.42 Submission Infrastructure Weekly Meeting`)
