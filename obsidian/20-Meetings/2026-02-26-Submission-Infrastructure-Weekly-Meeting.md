---
type: meeting
date: 2026-02-26
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Florian Von Cube
  - Hyunwoo Kim
topics:
  - Tier-0 job failures
  - CPU efficiency reporting
  - GPU partitioning
  - EPR
  - WLCG roadmap document
  - global pool capacity
  - MIT/frontend glidein limits
  - overloading monitoring
  - glideinWMS 3.11.3 ITB issues
  - T0 frontend failover test
  - volunteer pool
  - staffing
---

# Submission Infrastructure Weekly Meeting

## Summary

The group reviewed follow-ups from the CMS Monday operations meeting and the general computing meeting, including a Tier-0 job failure investigation at CERN and CPU-efficiency questions raised by the LHCC. Most of the meeting covered infrastructure status: a large global pool headroom at CERN, a frontend idle-glidein limit issue that was starving MIT/UCSD-area jobs, progress on pilot CPU-overloading accounting (with a known monitoring-dashboard regression), glideinWMS 3.11.3 ITB frontend bugs, an ongoing Tier-0 frontend failover test, volunteer-pool recovery work, and team staffing changes (a new factory operations member starting and two upcoming departures).

## Decisions / Conclusions

- The SoCal overflow glidein group was disabled by Marco after it was found to be pulling pressure onto pilots with no matching jobs (it matched only hardcoded, outdated MiniAOD 2018/2019 datasets). Marco notified Diego (owner of the group) and, absent a reply, kept it disabled.
- The group agreed that if the SoCal-style fixed-pressure expression in the frontend is not kept up to date, it should not exist there at all; if a site wants to keep such behavior it should be configured locally, not as a hardcoded frontend expression.
- The idle-glidein limit for the affected group was found to be capped at 300 instead of unlimited, causing the frontend to back off; Marco concluded this limit should be increased since these particular slots (I/O-heavy, low-CPU-use "extra CPU" jobs) do not waste resources by remaining idle.
- Three bugs were identified in the glideinWMS 3.11.3 ITB frontend: (1) ID token name generation used the `GLIDEIN_Site` attribute, which is not always present — fixed by switching to the mandatory entry name attribute; (2) a proxy-validity check was broken — fixed; (3) an issue in decrypting the symmetric key used for frontend–factory communication — still under investigation (not yet resolved as of this meeting).
- The volunteer pool machine (front end + collector + Condor on one box) had to be torn down and redeployed from scratch by Florian after Puppet stopped running for about a month, causing the host certificate to expire; IT recommended the rebuild. The redeploy is partially working (Condor runs) but the frontend is not yet fully functional.
- The team will keep the volunteer pool running for now, despite acknowledging it delivers little computing benefit relative to effort, because of its outreach value.

## Action Items

- [ ] Fix the overloading-status monitoring dashboard, which is showing incorrect/zeroed values because the underlying overloading tag changed from a simple Boolean to a different representation (some values now returned as capitalized-string booleans) — Marco Mascheroni / Hyunwoo Kim
- [ ] Set up on the Fermilab factory the same pilot-monitoring script (transferring input files to a monitoring machine, requires a password file) that is already running on the CERN factory — Marco Mascheroni, with Hyunwoo Kim
- [ ] Investigate and, if confirmed as a real bug, open a ticket for the padding issue seen with the glideinWMS 3.11.3 ITB frontend — Marco Mascheroni
- [ ] Check the difference against the saved backup of the frontend XML and confirm via Puppet/Git that the increased idle-glidein limits are applied — Marco Mascheroni
- [ ] Disable Puppet again on the CERN Tier-0 frontend so the Tier-0 failover test can run overnight against the Fermilab backup — Florian Von Cube
- [ ] Investigate the remaining glideinWMS 3.11.3 symmetric-key decryption issue — Marco Mascheroni
- [ ] Give a heads-up to CERN office colleagues about the new factory operations team member (Luis) starting — Florian Von Cube
- [ ] Fix the front-end dashboard problem (separate, still-open issue mentioned at the end of the meeting) — Florian Von Cube
- [ ] Continue debugging why the volunteer pool frontend is not fully running after the redeploy — Florian Von Cube

## Discussion

### Tier-0 job failures at CERN
Marco reported that jobs failing at CERN were Tier-0 "express" jobs. Antonio noted the apparent cause is an issue with the file system on some machines (heard as "SBM file system"; exact system name unclear in the recording). The relevant teams were put in contact with each other to follow up.

### LHCC talk and CPU efficiency questions
Antonio attended a general computing meeting rehearsal for a talk that CMS level-1 management will give to the LHCC next week. The slides highlight last year's use of Tier-1 sites (including Fermilab) for Tier-0 task execution — Antonio had not realized Fermilab was used for this, noting Marco explained this happened for heavy-ion Tier-0 processing (Fermilab was not interested in that physics) via flocking between pools.

A document of LHCC questions to CMS raised CPU efficiency, including why efficiency at CERN has dropped compared to previous periods, and Tier-0-versus-Tier-1 comparisons. Antonio gave feedback that:
- Site-reported efficiency reflects the combined effect of payload inefficiency and pilot/overloading effects, not payload alone.
- Tier-1s see more overloading pressure than Tier-2s because most work is directed there and because there is little value in overloading pilots that are not already fully loaded.
- Marco noted Tier-1 scheduling efficiency is reported weekly, with concern raised if it drops below 95%; typical efficiency is around 97%, with 8-core/whole-node efficiency somewhat lower because the tail of the payload is less efficient there. He characterized Submission Infrastructure's maximum contribution to the efficiency gap as roughly 5%.
- Marco also noted that a "true"/"false" (Boolean) glideinWMS overload flag remains set only at the Tier-1 level under the current mechanism, so overload-related calculations are currently only available for Tier-1s; the group still needs to extend the tier-choice/overload-enable mechanism (previously true/false) to Tier-2s using the newer percentage-based (e.g. 66%) configuration — noted as still-pending work, possibly to be picked up with Viva.

### GPU partitioning tech-watch talk
Antonio referenced an "Epic tech watch" working-group presentation (by a colleague referred to as "Getty"/unclear name) on GPU deployment and partitioning, covering Multi-Instance GPU (MIG) versus Multi-Process Service (MPS) and how GPUs can be exposed to HPC facilities. Antonio suggested this connects to an earlier Mattermost discussion with the CAT team and recommended the group look at the slides.

Marco asked Florian whether he is in contact with the CAT people doing this work; Florian said not currently but could reach out. The group discussed that deciding who applies GPU partitioning (CMS/pilots vs. the site) is a policy question requiring agreement and discussion with sites, and that CMS's own GPU usage is still small-scale and "peaky" (occasional spikes, e.g. when ML/AI-style workflows lacked enough GPUs, followed by long periods of low demand). Florian and Antonio agreed this unsteady demand is something CMS needs to address to justify GPU capacity, and that the Submission Infrastructure team's role is to be technically ready and to advocate that available grid GPU capability is usable.

### EPR
Antonio noted the annual EPR (effort/pledge reporting) process is open; he has already entered his pledges for both Submission Infrastructure and the broader general-computing coordination categories, and asked others to spread the word for staff pledging effort to the team.

### WLCG roadmap document
Marco reported on a WLCG Technical Coordination Board meeting about the roadmap document, where he presented how he intends to structure the workflow-management chapter (target ~4–5 pages). He noted convergence with the job allocation task force and asked Antonio to help write that part of the chapter, since Antonio's name had come up in that context.

### Conference contributions
Antonio confirmed a submission to the distributed-computing track has been accepted and — because of its importance — will additionally be given as a plenary talk. He expects several other contributions to be accepted for track 4, with one or two possibly as posters; the exact split between talks and posters and number of speakers is still to be determined.

### Global pool capacity
Antonio noted the global pool was observed reaching close to half a million CPU cores, driven by CERN's shared pool being underused by another group, giving Submission Infrastructure access to over 100,000 additional CPU cores from that shared pool headroom.

### MIT/frontend idle-glidein limits and SoCal overflow pilots
Marco described two related issues affecting MIT's ability to fill resources, raised on Mattermost:
1. The frontend was backing off due to hitting an idle-glidein limit for I/O-slot glideins. Investigation found the relevant group's limit was set to 300 instead of unlimited. Because these I/O-slot glideins use little CPU while idle, the group wants to raise this limit; Marco saved the current frontend XML as a backup to diff against once the change is applied (expected to already be in Puppet/Git).
2. Many overflow "SoCal" pilots were being submitted but matched no jobs (about 2,000 pilots observed running ~10 minutes with no work), pulling submission pressure away from useful pilots. Marco found the SoCal group's frontend match expression hardcoded to only MiniAOD 2018/2019 datasets, making it effectively obsolete. He disabled the group, notified Diego (its apparent owner) via email, and kept it disabled after receiving no reply, planning to discuss further at the recurring UCSD bi-weekly meeting. Antonio noted MIT is not part of the "SoCal" region and that a West Coast input-data cache group with a stale, hardcoded dataset list no longer makes sense as a fixed frontend expression; if retained at all, such logic should live in site-local configuration rather than the shared frontend.

### Pilot CPU-overloading accounting and monitoring
Marco presented per-cluster-ID overload accounting plots (Fermilab, days 2–4 and 17–21 in an unspecified month). Overloading is applied at the cluster level, so results are grouped unevenly (e.g., one cluster showed roughly 60% overloaded pilots). Aggregated data (137 vs. 333 pilot-days in the two groups referenced) showed roughly a 10% efficiency improvement for overloaded versus non-overloaded pilots at Fermilab, including one identified anomalous/bad workflow (cluster "41") that depressed both overloaded and non-overloaded numbers; excluding it improved the comparison to roughly 90% vs. 77%.

Antonio noted the non-overloaded efficiency figure (~68–75%) matches the efficiency CMS typically observes reported by Tier-1 sites, suggesting this method can reproduce the real, combined payload+pilot inefficiency that sites see. He proposed that final validation would come from aggregating a full month of data and comparing it against the numbers Tier-1 sites report to the EGI portal (noting uncertainty whether Fermilab has resumed EGI portal reporting).

Hyunwoo asked why the MIT plot's overload-status field showed 0/empty. Antonio and Marco explained this is a known artifact: the monitoring dashboard still keys off the old Boolean overload flag, but the underlying mechanism changed so the value can now be a capitalized string ("True"/"False") or another representation depending on whether it's static or dynamic overloading, breaking the existing plot logic. This is tracked as an action item to fix, either by adding a new tag, changing the existing one, or casting the value to a consistent type.

Separately, Marco described the CERN factory's existing script that updates and transfers monitoring input files to a monitoring machine (using a password file) and proposed setting up the same mechanism on the Fermilab factory; he and Hyunwoo planned to work on this after the meeting or the next day.

### Scalability test
No updates this week; Florian noted the week was consumed by the volunteer pool rebuild.

### Volunteer pool recovery
Florian reported that Puppet had stopped running on the volunteer pool machine (which hosts the frontend, collector, and Condor together) for about a month, for reasons not fully understood, which caused the host certificate to expire. After being unable to reissue the certificate, IT advised tearing down and redeploying the machine from scratch, preserving the hostname/IP via IT's provided tooling (so it wouldn't be deregistered in LanDB). Florian copied over tokens/passwords and redeployed; some group-ID/file-ownership issues were corrected, but the frontend is still not fully running as of this meeting, and Florian is continuing to investigate. The team agreed to keep the volunteer pool running given its outreach value, despite its low direct computing contribution.

### glideinWMS 3.11.3 ITB frontend issues
Florian asked about the status of the glideinWMS 3.11.3 ITB frontend/factory issues. Marco summarized three issues encountered with this major version:
1. ID token name generation relied on the `GLIDEIN_Site` factory attribute, which is not always present — fixed by using the entry name (a mandatory attribute) instead.
2. A proxy-validity check was implemented incorrectly ("flat out broken") — fixed.
3. An issue decrypting the symmetric key used for frontend–factory communication — still open, needs further investigation.
A separate "padding" issue was also mentioned; Marco said he does not believe it is related to the credential-configuration change referenced in glideinWMS documentation, and plans to do further diligence to confirm it is a real bug before opening a ticket. Marco also referenced a new credential configuration shared over Mattermost per glideinWMS documentation for this version, and asked Florian to confirm whether it had been applied.

### T0 frontend failover test
Hyunwoo and Florian are running a failover test of the Tier-0 front end, using a replaced/long-awaited Tier-0 pool backup machine at Fermilab that Hyunwoo set up and has been testing since that morning with Florian. Results looked okay so far but need more checks. Florian noted he had forgotten to re-disable Puppet on the CERN-side frontend after an earlier step, which caused it to start again; he agreed to stop it and disable Puppet again so the failover test can run overnight, at least until the next day.

### Staffing
Marco announced a new factory operations team member, Luis (a Brazilian, per Antonio), who is expected to join the team the following Monday (the second Monday of March). Marco asked Florian to give a heads-up to CERN office colleagues. Antonio noted he will not be at CERN that week, but Stefan and "Path" (name as heard in transcript, unclear) should be there to help onboard Luis, and Viva should be back from vacation to help train him during an overlap period expected to run through March.

Where Viva will go afterward is unresolved — Antonio and Marco said they don't know; Marco noted the factory operations position is normally funded for a defined multi-year term and that continuation beyond that is uncertain from CMS's side, and Viva may be applying to other positions in the area. Marco mentioned a "Cathay"-referenced (name/spelling unclear in transcript) hiring position is already open and suggested reaching out again to candidates from the earlier hiring round, though it was noted those candidates may have already found other positions.

Florian also raised that his own position (with CAT, not directly CERN-employed) ends at the end of April, and no replacement has been identified; Antonio said the hiring process for his replacement is delayed. Marco noted the previous hire (Viva) took a long time from opening the search (around June) to onboarding, due to bureaucratic/administrative ("burglas"-sounding word, unclear) delays. Antonio added that during the search that led to Luis's hire, several strong candidates (including people with Atlas experience already at CERN) were available but the timeline did not allow catching them.

Florian also flagged that he will need to use about 15 remaining vacation days in the next two months before leaving, since he cannot carry them fully into his next position; the timing was acknowledged as likely overlapping with the resumption of data-taking activity, but seen as preferable to delaying further (into May/June).

### Step-chain testing on BSC slots
Antonio reported that Marco's recipe for running "step chains" is working (with some needed adjustments) to test slots at BSC. An initial issue encountered was unrelated to Marco's setup — some CVMFS/software repositories that WMAgent/CRAB jobs need were not mounted at BSC, which the team is now addressing to restore full use of those slots.

### Front-end dashboard problem
Antonio reiterated a still-unresolved front-end dashboard problem (separate from the overloading-monitoring issue discussed earlier) and asked Florian to look at it when he has a moment; Florian confirmed he is aware of it.

## Open Questions

- What is the underlying cause of the CERN Tier-0 "express" job failures (file-system issue) at the affected machines?
- Whether/how to extend the overload-enable mechanism from Tier-1s to Tier-2s using the percentage-based configuration instead of the old true/false flag.
- Who applies GPU partitioning in practice — CMS/pilots or the sites — and how that should be agreed with sites.
- Whether Fermilab has resumed reporting accounting numbers to the EGI portal, needed to validate the monthly aggregated overloading efficiency numbers against site-reported figures.
- What is causing the remaining glideinWMS 3.11.3 symmetric-key decryption issue, and whether the separate "padding" issue is a real bug.
- Why the volunteer pool frontend is still not fully functional after the redeploy.
- Where Viva will move on to, and whether a replacement can be found for Florian's position before he leaves at the end of April.
- Whether previously interviewed strong candidates from the earlier hiring round remain available for the newly reopened position.

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[Monitoring]] · [[WLCG]] · [[CMS]] · [[GPU]] · [[Heterogeneous Computing]] · [[Tier 0]] · [[CRAB]] · [[WMAgent]] · [[CVMFS]]

## Source

meeting_saved_closed_caption.txt (from `2026-02-26 17.09.32 Submission Infrastructure Weekly Meeting`)
