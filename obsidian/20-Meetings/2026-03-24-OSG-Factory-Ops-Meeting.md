---
type: meeting
date: 2026-03-24
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Vaiva Zokaite
  - Luís Simas
  - Hyunwoo Kim
topics:
  - glideinWMS 3.11 testing
  - DIRACX evaluation
  - Kubernetes factories
---

# OSG Factory Ops Meeting

## Summary

The group discussed an ITB development environment for disruptive 3.11 tests, CMS’s direction to evaluate [[DIRACX]] on top of [[glideinWMS]], and access to OSG Kubernetes-factory configuration.

## Decisions / Conclusions

- CMS would explore DIRACX on top of glideinWMS; a CMS-native approach remained a backup.
- The existing ITB environment should not be disrupted for weeks; an ITB development environment was needed for 3.11 testing.

## Action Items

- [ ] Prepare an ITB development environment for 3.11 testing — Marco Mascheroni, Luís Simas, and Florian Von Cube
- [ ] Check LPC CRAB-user job-routing machinery and report back — Hyunwoo Kim
- [ ] Arrange access to OSG Kubernetes-factory configuration for Luís Simas — Jeff Dost

## Discussion

Open 3.11 issues included an Analyze Entries report failure and a site-token/project-ID syntax problem. CMS discussed its post-O&C-week direction: PanDA was not being pursued, while DIRACX’s missing transformation-system layer could potentially be developed jointly with LHCb. The OSG factory setup was described as Kubernetes-based, with production factories including Tiger and NRP/Nautilus deployments.

## Related

[[CMS]] · [[OSG]] · [[DIRACX]] · [[glideinWMS]] · [[Kubernetes]] · [[CRAB]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-24 16.13.43 OSG Factory Ops Meeting`)
