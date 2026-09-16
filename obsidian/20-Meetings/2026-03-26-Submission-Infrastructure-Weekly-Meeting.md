---
type: meeting
date: 2026-03-26
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Florian Von Cube
  - Vaiva Zokaite
  - Luís Simas
topics:
  - factory resources
  - HPC integration
  - per-pilot CPU efficiency
---

# Submission Infrastructure Weekly Meeting

## Summary

The group discussed resource-slot sizing and pledged versus opportunistic resources, a proposed integration path for Barcelona Supercomputing Center resources, and retention of factory event-log data for future per-pilot CPU-efficiency monitoring.

## Decisions / Conclusions

- Eight cores were described as the minimum useful pledged resource size for CMS; smaller resources may still be used opportunistically.
- Pledged or opportunistic status should be supplied through site-local resource tags discovered by pilots, rather than set in the factory configuration.
- Factory event-log data relevant to per-pilot CPU efficiency is being retained on EOS for later analysis.
- The next weekly meeting would be an optional roundtable for available participants because of the Easter holiday period.

## Action Items

- [ ] Ask the site how its resources should be classified and, if needed, request appropriate local resource tags — Vaiva Zokaite
- [ ] Review the Finnish-site `condor_analyze` thread and determine whether action is needed from Submission Infrastructure — Marco Mascheroni

## Discussion

### Resource classification and slot size

The team discussed a site offering four-core and eight-core resources. The group considered eight cores the threshold for resources to count as pledged and most useful for CMS, while four-core capacity could be acceptable as opportunistic work. A pilot reads the local resource tag when it starts; the factory does not set the pledged/opportunistic classification itself.

### Barcelona Supercomputing Center integration

Antonio described manually launching a glidein on a bridge machine, modifying its Condor configuration so it joins the Global Pool, and using a split-starter approach to execute work on Barcelona Supercomputing Center resources through SSHFS. The proposed next step is to replace the existing ad-hoc setup with a proper manually launched glidein while retaining the split-starter mechanism. Validation currently happens on the bridge and would not fully test the remote environment; a suitable Singularity image and equivalent validation at BSC remain necessary.

### Per-pilot efficiency data

The team wants per-pilot CPU-efficiency metrics derived from factory event logs. The raw information is already being saved on Marco’s EOS space, but systematic metric production and storage are not yet implemented. Luís had been introduced to the topic; the group considered it premature for him to lead implementation immediately.

## Open Questions

- Can the manually launched glidein and split starter provide representative validation and execution at BSC?
- How should sites mark resources that are opportunistic rather than pledged?
- What storage and aggregation approach should be used for per-pilot CPU-efficiency metrics?

## Related

[[CMS]] · [[Submission Infrastructure]] · [[Factory Operations]] · [[HPC]] · [[Barcelona Supercomputing Center]] · [[HTCondor]] · [[Pilot Jobs]] · [[Monitoring]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-26 17.16.46 Submission Infrastructure Weekly Meeting`)
