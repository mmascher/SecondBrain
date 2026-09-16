---
type: meeting
date: 2026-02-18
participants:
  - Marco Mascheroni
  - Jaime Frey
  - Florian Von Cube
topics:
  - HTCondor token submissions
  - Condor tail
  - workflow deadlines
---

# CMS Submission Infrastructure Meeting

## Summary

The group clarified unsupported HTCondor behaviour involving mixed token requirements in one item-data submission, discussed `condor_tail` connectivity, and explored whether HTCondor offers native deadline-based workflow prioritisation.

## Decisions / Conclusions

- Mixing jobs that require a token with jobs that do not, in one Condor submission using empty item-data values, is unsupported behaviour and should not be relied on.
- The preferable remedy is to separate those submissions; if auto-cluster performance degrades, that should be investigated directly.
- HTCondor does not provide dedicated deadline-based prioritisation machinery; priority would need external adjustment.

## Action Items

- [ ] Review the SciTokens C++ library issue on the Condor-users mailing list and follow up if useful — Jaime Frey
- [ ] Capture logs and report concrete details if the `condor_tail` failure recurs — Marco Mascheroni

## Discussion

### Item data and token requirements

Jaime explained that empty values in batched item data are inconsistently handled, particularly with late materialization. CMS used the pattern to mix different workflows and token requirements in one cluster, apparently to reduce auto-cluster counts. HTCondor does not intend to support this usage; grouping only by matching requirements and rank should still yield the appropriate auto-clusters.

### Diagnostics and commands

Marco asked whether `condor_tail` should work with the CMS CCB configuration. Jaime said it should, though firewall/shared-port details can matter and running as root can be necessary in some configurations. Marco later reproduced successful use and treated the earlier failure as possibly intermittent.

`condor_q` custom format files were discussed: they are not expected to combine with the standard batch/no-batch display formatting. The group also discussed ideas for deadline-driven campaign priority, but no native HTCondor feature was identified.

## Open Questions

- Why did the earlier `condor_tail` invocation fail while later attempts worked?
- Does separating CMS token-bearing and non-token jobs change auto-cluster behaviour in practice?

## Related

[[CMS]] · [[Submission Infrastructure]] · [[HTCondor]] · [[SciTokens]] · [[Workload Management]] · [[Monitoring]]

## Source

meeting_saved_closed_caption.txt (from `2026-02-18 18.07.40 CMS Submission Infrastructure meeting`)
