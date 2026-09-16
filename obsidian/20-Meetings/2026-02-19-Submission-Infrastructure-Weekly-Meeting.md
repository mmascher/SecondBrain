---
type: meeting
date: 2026-02-19
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Florian Von Cube
  - Vaiva Zokaite
  - Hyunwoo Kim
topics:
  - scheduling efficiency monitoring
  - overloading and pilot CPU accounting
  - scalability testing
  - factory operations
  - GPU partitioning
  - WLCG job allocation working group
---

# Submission Infrastructure Weekly Meeting

## Summary

The group reviewed fixes to scheduling-efficiency monitoring (excluding static I/O slots from the calculation), an efficiency-loss incident at a Tier-1 pool caused by 16 GB/1-core ACDC/RelVal jobs, and a broken front-end monitoring dashboard tied to a change in how the overloading flag is calculated. They discussed progress on full pilot CPU-usage/overloading accounting via a new per-pilot event record, ongoing scalability testing (submission rate around 35–40 Hz, no sandbox transfer tested yet), and several factory-operations items including a new CE for the Polish Tier-2, stalled GPU entry testing at an unnamed site due to Docker/PID-namespace restrictions, and a Dirac-benchmark error appearing at Fermilab ITB after a front-end branch merge. Antonio reported on a WLCG management board discussion proposing to extend the job allocation and handling working group's mandate to cover GPU resource discovery and allocation topics.

## Decisions / Conclusions

- Excluding static I/O slots (`SlotType == Static`, per Antonio's fix) from the scheduling-efficiency calculation corrected the previously depressed efficiency ratios (e.g., global pool and Tier-1s now showing above 90%, up from ~80–85%).
- The weekend Tier-1 efficiency drop (down to ~50% pool usage) was attributed to 16 GB/1-core ACDC (or RelVal) jobs; efficiency recovered once those jobs were removed.
- The WM Agent issue Jamie raised (submitting jobs with heterogeneous requirements — e.g., differing `request_disk` — within a single `condor_submit`) is not how Condor is meant to be used; fixing it would require refactoring that is uncomfortable to undertake during the code freeze.
- There is no native HTCondor feature for deadline scheduling in the new WM contacts checked.
- The HiToken/CRAB vault issue (with Stefano) was resolved via a component downgrade.

## Action Items

- [ ] Follow up with Carlos on why the overloading tag no longer appears to be a proper boolean in monitoring (type/casting mismatch suspected after the factory-side calculation change) — Florian Von Cube
- [ ] Investigate why the front-end monitoring (FEMonitor, negotiator monitoring) broke after the collector monitoring update — Florian Von Cube
- [ ] Debug together why the Adobe/ITB factory has stopped sending pilots — Marco Mascheroni and Florian Von Cube (tomorrow morning)
- [ ] Check with Vaiva on the status of processing factory pilot-completion logs into Kibana/OpenSearch (whether they are still being consumed) — Marco Mascheroni
- [ ] Send Vaiva's GGUS ticket/error log on the Docker/PID-namespace GPU entry issue, and try to involve Marco Mambelli — Vaiva Zokaite
- [ ] Compare the working Fermilab Docker worker-node configuration against the site having the PID-namespace issue — Vaiva Zokaite (site side)
- [ ] Send Vaiva the factory log excerpt about "can't find local starter address" / preening for Marco to check — Vaiva Zokaite
- [ ] Check whether the Fermilab ITB Dirac-benchmark error is caused by the front-end not being reconfigured after the CERN-branch merge — Hyunwoo Kim
- [ ] Save/document scalability-test dashboards and plots before data rolls off — Florian Von Cube
- [ ] Run a scalability test with a sizable sandbox (file transfer), since the recent test used no sandboxes — Florian Von Cube
- [ ] Investigate the glideinWMS 3.11.3-related issue Florian has been looking into — Marco Mascheroni and Florian Von Cube (tomorrow morning)
- [ ] Meet to discuss the Grafana y-axis scale change and the Fermilab Tier-0 backup front-end replacement — Hyunwoo Kim and Florian Von Cube (next week)
- [ ] Begin the Fermilab Tier-0 backup front-end replacement now that the window before Run 3 data-taking is open — Hyunwoo Kim, with Florian Von Cube

## Discussion

### Scheduling-efficiency monitoring fixes

Antonio changed the efficiency plots to exclude static slots (the only sizable static-slot component being I/O slots), which removed a systematic distortion in the ratios. This fixed the global pool, Tier-1, and (largely) Tier-2 comparison panels, restoring efficiency values above 90–95%. Marco noted he had previously tried achieving the same result with the `request_io_slot` parameter without success. Separately, idle-job counts had appeared inflated (~60K) because I/O slots were being counted together with regular idle slots; separating them brought the "proper" idle count back to ~20K while showing I/O slots as available and being used but not saturated.

A weekend incident caused a Tier-1 pool's usage to drop to ~50%, attributed to 16 GB/1-core jobs (ACDC or RelVal) that James had previously warned about; efficiency recovered once those jobs stopped. A Fermilab-related merge-job plot showed unexplained oscillation/decline in job counts that the group could not immediately explain and agreed to keep watching.

### Overloading monitoring breakage

Antonio noted the fraction of overloading pilots has been increased, but this cannot currently be verified because the overloading monitoring panel appears broken: it still shows only a true/false tag, and the count of pilots carrying that tag is declining even though pool size is stable, suggesting new pilots aren't carrying the tag in the expected format. Marco suspected the calculation was moved from being computed at runtime to being computed in the factory (associated with the move to reporting overloading as a percentage, e.g. 66%, for Tier-1s), which may have changed the value's type (e.g., string instead of boolean), breaking the boolean cast used by the monitoring/dashboard layer. Florian separately reported that a collector-monitoring update broke front-end monitoring (FEMonitor) and negotiator monitoring dashboards, with hard-coded names previously causing ITB dashboards not to work; that specific ITB issue was fixed, but the front-end monitoring breakage from the recent update is still open and unclear whether it's a data-ingestion problem or a Grafana data-source/visualization problem.

### Full pilot CPU usage / overloading accounting

Marco reported now having, per pilot, start and end events including CPU time, enabling calculation of wall time and efficiency, plus the overloading true/false flag in the same record — but data has only been available since the 17th (2 days before the meeting), coinciding with an unclear factory/front-end configuration change (possibly the 3.11.3 deployment) whose exact timing the group could not pin down. Once enough pilot-completion data accumulates, prior notebook-based analysis can be resumed. Antonio asked whether this could be visualized continuously (e.g., per completed pilot in Kibana); Marco said the machinery to push this data to an OpenSearch index exists and is already being used, but building a continuous/rolling-average dashboard would be a next step, contingent on checking with Vaiva whether the relevant factory logs are still being processed into Kibana.

### Scalability testing

Florian's most recent scale-test cycle (referenced as involving up to ~1 million jobs) sustained a submission/completion rate around 35–40 Hz for a single schedd, without the machine under stress. This test used no sandboxes (no file transfers). Antonio asked Florian to save dashboards/plots before the data rolls off, and requested a follow-up test using a sizable sandbox to see the impact on rate. Separately, Marco and Florian noted an issue after deploying glideinWMS 3.11.3 (previously on the 3.10 series) that Florian has been investigating; they agreed to debug it together the following morning.

### Factory operations

- A new CE was tested for the Polish Tier-2; it passed and was moved to production, with the old entry disabled.
- GPU entry testing at a site (referred to as "Rahala"/possibly misheard) resumed after a prior blocking error was fixed by site experts, but a new issue emerged: the site runs job environments in Docker and cannot support the requested namespace configuration, raising the question of whether glideinWMS requires running the pilot with `docker run --pid` (host PID namespace). The group recalled a similar unresolved issue previously seen with a CERN Tier-2's BEER entries, where suggested fixes did not help. Marco noted Fermilab runs worker nodes in Docker successfully, suggesting a configuration difference worth comparing. It was agreed this is likely something for the site to investigate on their end, and to involve Marco Mambelli via the GGUS ticket.
- The Adobe/ITB factory stopped sending any pilots; Vaiva had believed Florian rolled back a recent change, but Florian clarified he made a fix without rolling back. This left Vaiva unable to test, since entries were previously producing a Dirac-benchmark error and are now producing nothing. Marco and Florian planned to debug this together the next morning and then decide whether to roll back.
- Marco and Florian discussed whether the Dirac-benchmark error seen in ITB was linked to a CERN-branch-to-Fermilab-branch merge made about 9 days earlier, and whether Hyunwoo needed to reconfigure the Fermilab front-end afterward; confirmed the issue is present only in ITB. Hyunwoo agreed to check the relevant Git change.
- Vaiva asked about a factory log message ("can't find local starter address" and a reference to file "preening") seen for a VOMS/StarD-related entry, unsure if it is fatal or factory-side; she agreed to send Marco the log for review.
- For the site under discussion regarding cores, Daniel had told the site to go with 16 cores per the ticket, while leaving open the option for site admins to request whole nodes later; site admins had not responded so far.
- A new CE ticket for that site was actually a new-CE request (not a general reconfiguration) intended to be identical to the existing entries; testing hit the same Dirac-benchmark error, so the site was told to wait until that issue is resolved.

### GPU partitioning and related activity

Antonio raised a Mattermost discussion with KIT (Tim) about GPU partitioning modes; the group has not yet applied any of these partitioning recipes themselves and has only secondhand/theoretical knowledge so far, but intends to gain hands-on experience. A separate GPU discussion channel (with Andrea Voce and others) covers running multiple payloads on a GPU; the group needs to interact with these people to understand resource-usage intentions once GPUs are provisioned. Florian mentioned ongoing CMS GPU jobs at KIT involving Adriano (PDMV), which the infrastructure is currently supporting successfully. Marco reported a meeting with Lorenzo Valentini (HammerCloud) about developing a HammerCloud plugin to run GPU jobs more easily than the current cumbersome approach; Marco shared his test JDL with Lorenzo and speculated Lorenzo may be behind a recent spike in GPU pilot activity he observed (unconfirmed; Marco will ask). Antonio proposed that a next objective is to define representative workflows, use them to test GPU partitioning, and compare results; Marco agreed this was a good direction.

### Fermilab Tier-0 backup front-end and dashboard permissions

Hyunwoo reminded the group that the Fermilab Tier-0 backup front-end replacement has been delayed and that now — before Run 3 (2026) data-taking resumes — is the appropriate window to proceed; he will coordinate with Florian to make the change, potentially as soon as the following week. Separately, Hyunwoo asked about changing the y-axis scale (from starting at 75% to 0–100%) on a Tier-1 monitoring plot but found he lacked edit permissions on the dashboard; Florian, who has SI-team admin permissions, made the change during the meeting for the "slot usage" panel. It remained unclear to Antonio and Florian exactly how dashboard edit permissions are granted (team-based vs. individual), noting at least one dashboard had an individually granted permission.

### WLCG job allocation and handling working group

Antonio reported on Tuesday's WLCG management board meeting, where he presented as convener of the job allocation and handling working group (under WLCG operations coordination). That group's original scope (slot size, memory per core, runtime, whole-node adoption) is largely settled, with the four LHC experiments satisfied with the current state. Following the December heterogeneous-computing workshop, Antonio proposed extending the working group's mandate to also cover GPU-related resource discovery/allocation topics (e.g., how experiments discover GPUs on the grid, how to request opportunistic GPU resources, and site policies for offering GPUs), arguing this fits the same underlying theme of resource discovery and allocation already covered for CPU slots. The proposal — not a request to solve the full GPU accounting/technical picture, but to enable experience-sharing across CMS, ATLAS, LHCb, and ALICE — was well received at both operations coordination and the management board, but the board asked for concreteness on deliverables, timeline, and required expertise before proceeding further.

### Other business

Marco reported he is becoming more involved in new workload-management design work, collaborating with Brian Bockelman and Andrea (Piccinelli) on a CMS-led solution, with Dima also contributing ideas; a meeting with Dima and a presentation of the proposal are planned for the March CMS computing week. Marco offered to discuss this further with Antonio or others individually.

## Open Questions

- What is causing the unexplained decline/oscillation in the Fermilab merge-job count plot?
- Is the overloading-tag monitoring breakage a factory-side type/casting issue (string vs. boolean) or a monitoring/Grafana-side issue?
- Is the front-end monitoring breakage a data-ingestion problem or a Grafana visualization/data-source problem?
- Does glideinWMS require running Docker with a host PID namespace (`--pid`), and is this the root cause of the GPU-entry site's namespace restriction issue (and the earlier, unresolved CERN Tier-2 BEER-entry issue)?
- What exactly changed around the 17th (factory/front-end configuration) that aligns with the start of usable per-pilot CPU/overloading event data?
- Are factory pilot-completion logs still being actively processed into Kibana/OpenSearch?
- What caused the Adobe/ITB factory to stop sending pilots, and should the recent change be rolled back?
- Is the Fermilab ITB Dirac-benchmark error caused by a missing front-end reconfiguration after the CERN-to-Fermilab branch merge?
- Is the "can't find local starter address" / preening message in the factory log fatal, and is it factory-side?
- How are Grafana dashboard edit permissions actually granted (team vs. individual), and why did some SI members lack edit access?

## Related

[[CMS]] · [[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[WLCG]] · [[Monitoring]] · [[GPU]] · [[Heterogeneous Computing]] · [[CRAB]] · [[WMAgent]] · [[Work Queue]] · [[I/O Slots]]

## Source

meeting_saved_closed_caption.txt (from `2026-02-19 17.37.09 Submission Infrastructure Weekly Meeting`)
