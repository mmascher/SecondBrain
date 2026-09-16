---
type: meeting
date: 2026-01-15
participants:
  - Marco Mascheroni
  - Florian Von Cube
  - Hyunwoo Kim
topics:
  - I/O slots
  - monitoring
  - scalability testing
  - glideinWMS releases
---

# Submission Infrastructure Weekly Meeting

## Summary

The group reviewed the I/O-slot rollout, monitoring work, and scale-test objectives. I/O slots were reported as deployed successfully after frontend limits were raised; the next goal was to characterize scheduler limits with more realistic Tier 0 workloads.

## Decisions / Conclusions

- The next scheduler-scale tests should measure limits on both Tier-0-like and production-like hardware, rather than only demonstrate that 100,000 jobs run.
- Testing of glideinWMS 3.11.x would begin with 3.11.3 in ITB; the long-term aim discussed was to converge factory versions.

## Action Items

- [ ] Update the Global Pool backup frontend XML with the latest group and global limits — Hyunwoo Kim

## Discussion

### I/O slots and monitoring

The group had enabled I/O slots but initially underestimated the frontend limits that needed adjustment. After the limits were updated, no major pool drain was observed. Marco asked that idle jobs requesting I/O slots be monitored to confirm that those jobs do not accumulate in schedulers.

Marco was working on improved factory-side monitoring for overloaded pilots. Florian continued work on a requested restructuring of long-term monitoring documents, but no completed change was reported.

### Scale-test goals

The prior 100,000-job test completed without a scheduler crash. The group wanted to inspect retained host and duty-cycle data, then progress beyond a fixed sleep-job workload: determine limits for idle and running jobs, test a Tier-0-like scheduler, compare similar production hardware, and use a mix of job durations. The disk-backed job queue was identified as a condition that needed testing because it could become a bottleneck.

### Release status

The backup Global Pool frontend was upgraded to 3.10.17. Participants discussed 3.11.3 as the appropriate development release for ITB testing and noted that OSG factories were already on 3.11.2 with patches.

## Open Questions

- What are the safe scheduler limits for realistic Tier 0 job mixes?
- Does the disk-backed job queue become a bottleneck at those limits?
- Will the proposed overloaded-pilot monitoring solution work with the required Condor attributes?

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[Monitoring]] · [[I/O Slots]] · [[Tier 0]]

## Source

meeting_saved_closed_caption.txt (from `2026-01-15 17.18.49 Submission Infrastructure Weekly Meeting`)
