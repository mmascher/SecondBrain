---
type: meeting
date: 2026-01-22
participants:
  - Marco Mascheroni
  - Florian Von Cube
  - Vaiva Zokaite
  - Hyunwoo Kim
topics:
  - Condor history monitoring
  - scheduler scalability testing
  - I/O slots
  - held pilots
---

# Submission Infrastructure Weekly Meeting

## Summary

The group reviewed Condor developer discussions, held-pilot issues, and a successful 50,000-job scale test. They also clarified the purpose and resource model of I/O slots and identified changes needed before more aggressive scale tests.

## Decisions / Conclusions

- The earlier slow `condor_history` result was attributed to storage performance, not the command’s forward/reverse option.
- The direct benchmark script will be removed from ITB test groups while retained for non-test groups.
- The old RAM-disk mount on the scale-test scheduler should be removed before the next test.
- I/O slots were enabled on 12 January; they reserve a virtual core for I/O-heavy jobs and limit jobs to one per worker node.

## Action Items

- [ ] Investigate held pilots at CERN and raise the issue with Ben Jones if it continues — Vaiva Zokaite and Marco Mascheroni
- [ ] Remove the RAM-disk mount from the scale-test scheduler — Florian Von Cube
- [ ] Repeat scale testing around 100,000 running jobs and validate memory monitoring — Florian Von Cube
- [ ] Investigate why Fermilab pilots have remained held — Hyunwoo Kim

## Discussion

### Condor and infrastructure topics

The previous Condor-developer meeting covered the broken Refresh GSI API, `condor_history` performance, and a possible timeout for `condor_status` when a collector does not respond. The pool was generally healthy, though high-memory workflows had temporarily increased idle jobs.

### Held pilots and factory work

CERN pilots were held after disappearing from the remote scheduler or failing to obtain proxy-expiration information. Some old held pilots were not being cleared. Vaiva also reported Fermilab held pilots, visible over a longer period in monitoring. The exact reasons and the difference between pilots that clear and those that remain held were unresolved.

### Scale testing

CMS0814, a former Global Pool central manager with 196 GB RAM, was repurposed as a scale-test scheduler. It handled 50,000 eight-hour sleep jobs, with about 47,000 running concurrently. A direct benchmark script caused excessive load on remote nodes; a merge request would keep it out of ITB test groups.

The group questioned unexpectedly low reported memory use and suspected a monitoring issue. They discussed a nominal 2 MB per running job estimate, the need to remove the obsolete RAM disk, and testing a more Tier-0-like distribution of shorter jobs.

### I/O-slot model

Marco explained that an I/O slot advertises an extra virtual core, which is reserved for jobs that are I/O-heavy rather than CPU-heavy. This prevents many I/O jobs from landing on a single worker node. Existing agent-side limits on I/O-job submission were considered obsolete now that I/O slots are available.

## Open Questions

- Why do some held pilots clear while others persist?
- Is scale-test memory monitoring accurate, and what is the real per-running-job memory cost?
- How should obsolete agent-side I/O-job limits be removed?

## Related

[[CMS]] · [[Submission Infrastructure]] · [[HTCondor]] · [[Factory Operations]] · [[Monitoring]] · [[I/O Slots]] · [[Tier 0]]

## Source

meeting_saved_closed_caption.txt (from `2026-01-22 17.37.33 Submission Infrastructure Weekly Meeting`)
