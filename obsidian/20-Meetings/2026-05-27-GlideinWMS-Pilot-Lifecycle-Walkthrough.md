---
type: meeting
date: 2026-05-27
participants:
  - Marco Mascheroni
  - Luis Simas
topics:
  - LPC facility site-token ticket (local-token-only hypothesis)
  - Syracuse and other factory entries' token/proxy migration status
  - Factory/frontend machine kernel updates and an AFS kernel-module mismatch incident
  - Tier-1 pilot memory efficiency anomaly
  - CHEP 2026 conference presentation planning
  - GlideinWMS pilot startup script download and Squid/HTTP caching
  - Hash-based integrity verification of downloaded pilot scripts
  - Node validation and the "black hole" failure mode
  - StartD/Condor configuration publishing (GLIDEIN_ attributes)
  - Custom per-entry validation scripts
  - Partitionable slots
  - VO-specific StartD customizations (CRAB)
  - Pilot log collection, postmortem, and compression
  - Glidein lifetime: to-die vs. to-retire, scheduling efficiency, retire-time buffer
  - "Infinite pilot" idea and WLCG pilot-lifetime policy
  - Security: site token vs. ID token, GLEXEC deprecated in favor of Apptainer/Singularity containers
  - Factory default attributes (start expressions, JOB_MAX_TIME, USE_SINGULARITY)
---

# Submission Infrastructure Weekly Meeting: Ticket Review, CHEP 2026 Planning, and GlideinWMS Pilot Lifecycle Walkthrough

## Summary

The meeting opened with a short operational/ticket review before continuing an ongoing GlideinWMS architecture training series (a continuation of the walkthrough begun the previous day, [[2026-05-26-GlideinWMS-Architecture-Walkthrough|GlideinWMS Architecture Walkthrough]]).

On tickets, Marco raised that LPC is a facility used primarily by local users, and it may be intentionally rejecting normal site tokens because it only wants to accept locally-scoped tokens for its pledged resources. Luis said he would check this and could close the related ticket if confirmed. Luis then reviewed factory entries by token/proxy status: LPC appeared to be the only entry not working with site tokens (explained by the local-only-token hypothesis above); Syracuse — a mixed site contributing roughly 2,000–3,000 cores — was confirmed to still work correctly using a grid proxy rather than a site token. Luis noted the overall entry list has a mix of older entries still using grid proxies and newer ones using site tokens, and that two entries have not been working for at least the past 30 days (the visibility window). He suggested a future cleanup of stale entries. Marco proposed coordinating with Jeff next week on these findings, then moving on to review Condor-based entries in production, followed by a similar check for ARC-CE entries.

Luis separately mentioned he is updating the kernel on factory and frontend machines to address vulnerabilities, and is writing a script to help manage this at scale (4 factory machines vs. 20+ frontend machines, plus load-balancer considerations). He also flagged a pilot/memory efficiency monitoring concern: some entries show memory usage above 100%, and tier-1 memory efficiency showed a large, currently unexplained drop starting last weekend, which Luis tentatively linked to a period when the frontend was down and a firewall was disabled, though he was not sure this fully explains the drop and considered it not urgent to chase further right now.

The group also discussed planning for Luis's upcoming CHEP 2026 presentation. Marco confirmed the standard slot is 20 minutes (roughly 15 slides plus questions) and pointed Luis to relevant slides from Marco's older decks (e.g., an overloading explanation slide, and a one-off event-rate study slide that could go in backup slides). Marco suggested Luis first send an outline before building the full deck, echoing an approach used previously, and noted Antonio should probably be involved as well. There is currently no CMS/GlideinWMS slide template; Marco said they should probably create one.

The bulk of the meeting was then spent continuing the technical walkthrough of the GlideinWMS pilot lifecycle, covering: how pilots download startup scripts/configuration from the factory and frontend via Squid/HTTP with cache-busting, time-based IDs embedded in URLs; hash-based integrity verification of downloaded files; node validation and the rationale for the pilot's 20-minute sleep-before-exit behavior (to avoid a rapid pilot-restart "black hole" that could overload web servers and risk a distributed-denial-of-service-like effect); how Condor configuration attributes can be published from factory/frontend into the StartD via `GlideinPublish`/`JobPublish`/etc. flags in entry XML; custom per-entry validation scripts; partitionable slots; VO-specific StartD-level customizations (e.g., CRAB's tweaks, which live in the ScheDD/VO layer rather than on worker nodes); log handling (postmortem mining of Condor logs for job exit codes/efficiency, log compression and base64 encoding into stderr); pilot cleanup and its limits (e.g., `kill -9` from the batch system); and glidein lifetime concepts (`GLIDEIN_ToDie`, `GLIDEIN_ToRetire`, scheduling efficiency, and the retire-time buffer that exists because declared job walltimes are unreliable estimates). The group also discussed a security section covering the site token vs. ID token distinction and the historical shift away from GLEXEC toward Apptainer/Singularity-based per-job containers with UID remapping, plus factory default attributes (start expressions, `JOB_MAX_TIME`, `USE_SINGULARITY`) shipped in the factory RPM.

## Decisions / Conclusions

- The team will coordinate with Jeff next week on the site-token ticket findings (LPC likely intentionally local-token-only; Syracuse and other entries reviewed).
- After finishing the Condor-entry token review, the team will move on to review ARC-CE entries for the same kind of access check.
- CRAB (not GlideinWMS/HTCondor itself) is what kills user jobs that exceed their declared wall time; GlideinWMS/HTCondor does not kill a job for exceeding its declared time unless the enclosing glidein hits its "to die" deadline.
- Scheduling decisions (whether to start a new job in a pilot) are based on the glidein's retire time, not the to-die deadline — this was a correction Marco made mid-discussion after initially answering "to die."
- `GLIDEIN_Max_Idle` defaults to 20 minutes in GlideinWMS, but the frontend currently sets it to 10 minutes for CMS pools, since roughly 5 minutes is used as a rule-of-thumb threshold for an acceptably fast negotiator matchmaking cycle.
- GLEXEC is no longer used; user jobs now run in per-job Apptainer/Singularity containers with UID remapping, invoked today via a Condor `PREPARE_JOB`-style prescript (a `SingularityWrapper`/OSG-provided mechanism), with a plan to migrate to Condor's native container-execution support in the future (which would also restore compatibility with `condor_ssh_to_job`, currently broken by the custom container-invocation approach).
- Standard CHEP presentation slot length is 20 minutes (~15 slides plus Q&A).

## Action Items

- [ ] Check whether the LPC ticket is explained by LPC intentionally accepting only local (not site) tokens, and close the ticket if confirmed — Luis Simas
- [ ] Coordinate with Jeff next week on the site-token/proxy review findings — Marco Mascheroni / Luis Simas
- [ ] Continue reviewing Condor-based factory entries for site-token status, then review ARC-CE entries — Luis Simas
- [ ] Do a cleanup of stale/non-working factory entries in the future — Luis Simas
- [ ] Send an outline of the CHEP 2026 presentation to Marco before building the full slide deck — Luis Simas
- [ ] Ask other people in WLCG (transcribed as "WCG"/"WSCG") about the feasibility/policy implications of longer-lived or open-ended ("infinite") pilots — Marco Mascheroni
- [ ] Show Luis how `condor_q -better-analyze` works, to clarify the still-unclear third "static expression" used in second-stage matchmaking — Marco Mascheroni

## Discussion

### LPC and Syracuse ticket review
LPC serves local users and may deliberately reject standard site tokens, accepting only locally-scoped tokens tied to specific users for its pledged resources (roughly 2,000 cores). Syracuse, a mixed site (~2,000–3,000 cores), was confirmed to still authenticate via grid proxy rather than site token, and this was working correctly. Luis noted the broader entry list has a mix of legacy grid-proxy entries and newer site-token entries, and that two entries have shown no activity for at least 30 days (the limit of Luis's visibility window). A cleanup of stale entries was suggested for the future.

### Factory/frontend kernel updates
Luis is updating kernels on factory (4 machines) and frontend (20+ machines, referred to in the transcript as "Frontier," which in this context appears to mean the GlideinWMS frontend/front-end machines rather than the CMS Frontier conditions service) machines to address security vulnerabilities, and is scripting this to handle the larger frontend fleet plus load-balancer coordination. Separately, Luis described updating only the kernel package (not a full system update) on one machine, which caused AFS to break after reboot because the AFS kernel module package remained built for the older kernel. Marco's general recommendation: prefer full-system updates over single-package updates; the AlmaLinux repositories at CERN are usually considered stable, but changes should still go through ITB first and sit for about a week before being applied in production — except for urgent security issues, where a faster, higher-risk rollout may be warranted.

### Pilot/memory efficiency monitoring
Some factory entries show pilot memory usage above 100%. Tier-1 memory efficiency showed a large, unexplained drop starting last weekend; Luis tentatively associated this with a period when the frontend was not working and a firewall was disabled, but was not fully sure this explains it and did not consider it urgent to investigate further at this time.

### CHEP 2026 presentation planning
Luis's presentation slot is the standard 20 minutes (~15 slides plus questions), scheduled for the 10th (not yet listed on the agenda at the time of the meeting). Marco pointed Luis to specific slides from his own older decks that could be reused or adapted (an overloading-explanation slide, and a one-off event-rate study slide suitable for backup slides in case of audience questions). There is no existing CMS/GlideinWMS presentation template; Marco said one should probably be created. Marco suggested Luis send an outline first so they can discuss structure before Luis builds the full deck, and that Antonio should likely be involved in preparing the talk as well.

### Pilot startup script download and caching
Pilots download startup scripts, configuration, and validation scripts from both the factory and the frontend via Squid/HTTP, using URLs passed as `glidein_startup.sh` arguments (visible via `condor_q -l` on pilot ClassAds). These URLs embed a time-based unique ID (e.g., in `group_description` / `description.cfg` filenames) that is regenerated on every factory/frontend reconfigure, ensuring pilots always fetch the newest version rather than hitting a stale cached copy under the same filename. Because of this, after a reconfigure, changes only propagate once idle pilots are cycled — a behavior the group previously encountered while rolling out the overloading feature. Idle pilots (in the factory only, not yet submitted to the CE) can safely be removed to speed this up without affecting running pilots; the factory distinguishes idle-in-factory from idle-in-CE, and an alert exists for pilots stuck idle in the factory but not the CE.

### Integrity verification
Hashes of downloaded scripts/files are calculated, written to a hash file, and published by both factory and frontend; `glidein_startup.sh` downloads scripts and their hash file and verifies integrity (including a hash of the hash file itself), intended to prevent tampering with files after a pilot has been submitted.

### Node validation and the "black hole" concept
Validation scripts and wrapper/plugin scripts (provided by both factory and frontend, distinguished via a map file) run on the worker node before Condor starts; a failing script is treated as a validation failure. On failure, `glidein_startup.sh` sleeps for 20 minutes before terminating rather than exiting immediately, specifically to avoid a "black hole" — a rapid pilot-restart loop that would place excessive load on worker nodes and generate excess web-server traffic (`wget` requests) from factory/frontend, with a risk of a denial-of-service-like effect.

### StartD/Condor configuration and custom attributes
Entry- and frontend-level attributes can be flagged (e.g., `GlideinPublish`, `JobPublish`, `ParamPublish`) to control whether a given value is transferred into the StartD's Condor configuration and/or published as a ClassAd attribute (e.g., `GLIDEIN_Overload_Enabled`); this is a per-attribute property, not name-based. Custom validation scripts can also be added per entry (via a `files` section in the entry XML) to run additional detection/validation logic on the worker node, though in practice the team leans toward handling such cases generically in `glidein_startup.sh` rather than per-entry scripts.

### Slots and VO-specific customization
`GLIDEIN_CPUS` defines how many cores a glidein advertises/requests, distinct from what is actually requested from the CE/batch system. The frontend typically requests a partitionable slot layout, allowing multiple jobs to run concurrently within one pilot (partitionable slots being a newer HTCondor concept vs. older one-machine-one-job models). Users submit jobs to the ScheDD, and VO-specific job-placement policy (e.g., site or GPU requirements) is a property of the StartD/job-matching layer, not the glidein itself. CRAB (Stefano) applies its own ScheDD-level tweaks distinct from worker-node-level configuration.

### Logs, postmortem, and cleanup
Pilot logs are transferred back to the factory (`var/log/<WMS>/client`) once a pilot finishes; on termination, job information (job count, exit codes, signal termination, efficiency) is mined from Condor logs, and the Condor StartD/master/starter logs themselves are compressed and base64-encoded into the job's stderr. Neither disk nor "the cloud" (as Marco put it) guarantees log durability. On cleanup, files are removed before pilot termination where possible, though a hard `kill -9` from the batch system (e.g., due to memory overuse) can prevent full cleanup; users should not expect any data to survive a job unless explicitly copied to a storage element. The batch system itself also provisions and later reclaims a job-specific working directory/filesystem area.

### Glidein lifetime and retirement
Glideins are treated as temporary, leased resources meant to exit cleanly and be monitored/cleaned up rather than killed abruptly. `GLIDEIN_Max_Walltime` sets the point at which Condor forces the glidein to exit, killing any remaining running jobs (wasted work); this deadline is advertised as `GLIDEIN_ToDie` and derived by `glidein_startup.sh` into underlying Condor exit configuration. To reduce this waste, an earlier "to retire" deadline (`GLIDEIN_ToRetire`) is set, after which the glidein stops accepting new jobs but lets already-running ones finish; jobs are scheduled based on the retire-time buffer (not the to-die deadline). Condor itself will still kill a running job if it exceeds the to-die deadline, but does not kill jobs merely for exceeding their declared walltime before that point — CRAB, separately, does enforce this at the job level. The ~4-hour retire-time buffer exists because declared job walltimes are unreliable estimates (jobs often run shorter than declared); if declared walltimes were fully reliable, a large retire buffer would not be needed. The team currently targets roughly 95% overall scheduling efficiency for tier-1s; this is visible as a "slot usage" plot in monitoring (measuring how well slots are filled with payloads, distinct from actual CPU usage), which Luis initially misread as raw CPU usage and which Marco suggested may need more explanation for a general audience if referenced in the CHEP talk.

### "Infinite pilot" idea and WLCG policy (exploratory, not decided)
Luis raised the idea of a long-lived or "infinite" glidein that only exits when explicitly told to, rather than on a fixed schedule, potentially reducing scheduling-efficiency losses near the end of a pilot's life. Marco noted this could work on a CMS-exclusive site (he cited Fermilab, where negotiated pilot durations have shifted from one week down to 4–5 days for site cleanup needs, and where a separate mechanism exists to force pilots into retirement) but is riskier on shared multi-VO sites, since site admins generally do not preempt/kill glideins, creating a risk of indefinitely holding resources if demand from another VO (e.g., ATLAS) disappears. Marco noted finite/consistent pilot shapes are also a broader WLCG-level policy consideration (not something CMS can unilaterally decide) and said he would ask others in WLCG about this. Related to this, Luis observed that per-job (rather than per-pilot) retirement/grace periods might reduce the need for whole-pilot retire buffering, though Marco noted this would only help if job walltimes vary — if all jobs in the queue declare similarly long walltimes, scheduling would still stall near the end of a pilot regardless.

### Security: tokens and containers
Two tokens are used by a pilot: a site token, used to authenticate to the CE, and an ID token, used to authenticate the StartD; both originate from the frontend. Since GlideinWMS moved away from X.509 proxies toward tokens representing a VO rather than a specific end user, the final user running inside a pilot is not known a priori — Marco noted this matters mainly for incident response (e.g., identifying a compromised credential, referencing a past Bitcoin-mining incident), which would be CMS's own responsibility given CMS holds the relevant visibility. GLEXEC (the older mechanism for switching to a specific user's UID) is no longer used; today, jobs run in per-job Apptainer/Singularity containers with UID remapping, currently invoked via a Condor prescript mechanism inherited from earlier "SingularityWrapper"/OSG-style integration, with a stated intent to move to Condor's native container-support mechanism, which would also make tools like `condor_ssh_to_job` work again (currently confused by the custom container invocation). Marco believes Condor added native container support after observing widespread external use of the wrapper-script pattern across VOs, preferring to formally support it rather than have users bolt on external logic; the group did not further confirm who specifically pushed for this integration.

### Factory default attributes
Factory RPM packaging includes default attributes such as `OSG_def`-related connection settings, the start expression used for first- and second-stage matchmaking, `JOB_MAX_TIME`, and whether Singularity/Apptainer usage is mandatory (mandatory for CMS). Luis noted the third ("static") expression used in second-stage matchmaking is not yet fully clear to him; Marco said he would revisit this later using `condor_q -better-analyze` as a worked example.

## Open Questions

- What fully explains the recent unexplained drop in tier-1 pilot memory efficiency (tentatively, but not confirmedly, linked to a frontend outage/firewall disablement)?
- Would WLCG support longer-lived or open-ended ("infinite") glideins, and under what conditions could this work safely on shared multi-VO sites?
- How exactly does the third ("static") expression used in second-stage (negotiator) matchmaking work, and how is it structured relative to the other start expressions?
- Which layer/mechanism precisely converts `GLIDEIN_Max_Walltime` into the underlying Condor exit configuration used by the StartD?

## Related

[[glideinWMS]] · [[HTCondor]] · [[Submission Infrastructure]] · [[CMS]] · [[WLCG]] · [[Factory Operations]] · [[Factory Configuration]] · [[CRAB]] · [[2026-05-26-GlideinWMS-Architecture-Walkthrough|GlideinWMS Architecture Walkthrough (2026-05-26)]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-27 14.49.05 Submission Infrastructure Weekly Meeting`)
