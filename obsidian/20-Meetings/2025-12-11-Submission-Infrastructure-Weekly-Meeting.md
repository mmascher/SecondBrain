---
type: meeting
date: 2025-12-11
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Florian Von Cube
  - Vaiva Zokaite
  - Hyunwoo Kim
topics:
  - infrastructure status
  - Factory Operations
  - heterogeneous resources
  - scheduler scalability testing
---

# Submission Infrastructure Weekly Meeting

## Summary

The group reviewed a generally healthy [[Submission Infrastructure]], site and [[Factory Operations]] updates, and early scheduler scalability tests. A production update was deferred until January; the scale test exposed unexplained scheduler errors and high load on a newly deployed test host.

## Decisions / Conclusions

- The update to version 3.10.17 will wait until January; its new features will not be enabled before the year-end break.
- Surplus-resource use was re-enabled by setting the relevant configuration to `surplus true`.
- The Global Pool and Tier 0 were reported as running versions 3.10.16 and 3.10.15 respectively, while ITB was on 3.10.17.
- The scheduler issue affecting one scheduler was considered minor and did not create pool job pressure; running the latest Condor version on that scheduler was the immediate workaround.

## Action Items

- [ ] Check the ticket-notification configuration and membership path — Antonio Perez-Calero Yzquierdo
- [ ] Add the scale-test schedulers to the Prometheus configuration — Florian Von Cube
- [ ] Investigate the high load, Condor errors, and possible RAM-disk configuration on CMS0842 — Florian Von Cube

## Discussion

### Infrastructure and release status

Pool sizes, utilisation, collector cycles, and negotiator cycles appeared normal. P5 resources had disappeared from the pool as part of a planned decommissioning and relocation. A single scheduler had submission failures thought to be another OpenSSL-related proxy-passing issue; the exact triggering update was unclear.

The team discussed 3.10.17, already tested in ITB. Its mentioned benefits included EL10 worker-node support, lower memory spikes on reconfiguration, lower disk use from Condor tarball handling, an RFD-related factory fix, and a static-slot bug fix. With no urgent production need before the break, the group chose to defer the update.

### Factory and site operations

The OHDG factory-file cleanup was completed. A Korean Tier 2 increased memory per core to 5 GB, and IFCA had a queue-name change that still needed validation after downtime. A deprecated ARC Geolite runtime environment had affected SAM tests; a factory change was made, though pilots from the CERN Factory had not yet appeared while pilots from the other factories were running.

A new Chinese Tier 3 using a TCP reverse proxy through an Alibaba Cloud VPS had developer jobs that were not running. The group also discussed gaps in Giga ticket notifications and the need to understand the relevant categories, aliases, and settings.

### Heterogeneous resources

Participants referred to a recent heterogeneous WCG resources workshop, including discussion of grid resource discovery, allocation, matchmaking, and possible GPU-related tests. They also discussed whether Run-3 HLT resources could be made available for offline use over the break; availability remained unclear.

### Scheduler scalability tests

Florian submitted 10,000 jobs to scale-test scheduler CMS0842. About 3,400 were running and 6,500 idle, but `condor_q` produced failures fetching ads and failures sending classads. The scheduler duty cycle did not appear saturated, yet the host had anomalously high load and Condor processes in states suggesting disk waits. The host was newly deployed, and its RAM-disk setup was uncertain.

The group proposed comparing the result with another identically configured scale-test scheduler, adding host monitoring through [[Prometheus]], and ensuring idle-VM limits would not constrain future tests. The limit had previously been raised from 13,000 to 30,000; further raising it was discussed, not decided.

## Open Questions

- Why did CMS0842 produce Condor communication errors and extreme load during a 10,000-job test despite low scheduler duty cycle?
- Is CMS0842 using the expected RAM-disk configuration?
- Why were CERN Factory pilots absent after the ARC runtime change while other factories’ pilots ran?
- Will Run-3 HLT resources be available for offline use over the break?

## Related

[[CMS]] · [[Submission Infrastructure]] · [[HTCondor]] · [[Factory Operations]] · [[GPU]] · [[Heterogeneous Computing]] · [[Prometheus]]

## Source

meeting_saved_closed_caption.txt (from `2025-12-11 17.18.16 Submission Infrastructure Weekly Meeting`)
