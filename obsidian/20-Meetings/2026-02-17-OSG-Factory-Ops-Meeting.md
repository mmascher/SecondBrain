---
type: meeting
date: 2026-02-17
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Vaiva Zokaite
  - Hyunwoo Kim
topics:
  - glideinWMS 3.11.3
  - GPU entries
  - ITB validation failures
---

# OSG Factory Ops Meeting

## Summary

The group reviewed a GPU-entry parsing bug in glideinWMS 3.11.3, planned a small production patch for OSG/Kubernetes factories, and investigated ITB manual-submit and validation failures affecting CMS GPU and other entries.

## Decisions / Conclusions

- A missing comma in a Condor configuration can cause GPU entries to parse a CPU count as a percentage; the issue had existed for years and was reproduced as fixed by adding the comma.
- Jeff Dost planned to patch and upgrade OSG/Kubernetes factories, rather than wait for a later release.
- The CMS ITB 3.11.3 frontend was expected to reveal new bugs because it is a major release; CMS-specific issues should be reported through the internal channel.

## Action Items

- [ ] Raise the GPU-entry missing-comma bug at the glideinWMS meeting — Marco Mascheroni
- [ ] Upgrade OSG/Kubernetes factories and apply the minimal GPU-entry patch — Jeff Dost
- [ ] Report the ITB `direct_benchmark.py` validation failures in the internal Mattermost channel and compare with Florian’s scale-test configuration — Vaiva Zokaite and Florian Von Cube
- [ ] Investigate manual glidein submission failures in ITB — Marco Mascheroni

## Discussion

### GPU-entry parsing issue

Jeff described a typo in the Condor configuration used for GPU entries: a missing comma between CPU and disk fields caused Condor to interpret a core count as a percentage. The resulting slot had 2.56 rather than 16 CPUs. A one-character patch worked in ITB. The issue was considered functional but significant enough to patch in OSG production.

### ITB issues

Manual glidein submission returned “could not find any frontend requests for the specified entry frontend pair” for GPU entries in both CERN and Fermilab ITB contexts. Separately, existing Bari and new DESY entries failed `client_group_direct_benchmark.py` validation in ITB while production entries worked. The transcript did not establish whether these failures had a common cause.

CMS had encountered 3.11.3 requirements for additional configuration, including `GLIDEIN_Site` in relevant XML. The Fermilab ITB frontend was reported on 3.10.17, while the CERN ITB frontend used the 3.11 series.

## Open Questions

- Are the manual-submit and direct-benchmark validation failures related to the ITB upgrade or separate CMS configuration issues?
- Which 3.11.3 fixes belong upstream in glideinWMS versus CMS-specific scripts?

## Related

[[OSG]] · [[glideinWMS]] · [[HTCondor]] · [[Factory Operations]] · [[GPU]] · [[Kubernetes]] · [[CMS]]

## Source

meeting_saved_closed_caption.txt (from `2026-02-17 17.24.54 OSG Factory Ops Meeting`)
