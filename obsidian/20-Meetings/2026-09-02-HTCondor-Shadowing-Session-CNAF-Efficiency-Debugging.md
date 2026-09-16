---
type: meeting
date: 2026-09-02
participants:
  - Marco Mascheroni
  - Pablo Izquierdo Gonzalez
topics:
  - onboarding / shadowing plan
  - HTCondor pool architecture overview
  - ClassAds
  - scheduling efficiency monitoring
  - live debugging of low scheduling efficiency at CNAF
  - partitionable vs. dynamic slots
---

# HTCondor Shadowing Session — CNAF Scheduling Efficiency Debugging

## Summary

Early in Pablo Izquierdo Gonzalez's onboarding (his second day), Marco Mascheroni ran an informal "shadowing" session — not a scheduled training — showing Pablo his routine daily work: checking [[Submission Infrastructure]] scheduling efficiency and live-debugging a low-efficiency site. Marco first gave a short verbal overview of HTCondor pool architecture and ClassAds, then walked through the CMS Monit monitoring page and a series of live `condor_status`/`condor_q` commands from his own personal "cheat sheet" to investigate low scheduling efficiency at CNAF. The session ended when Pablo had to leave for another meeting, before the final hypothesis (jobs requesting long wall-clock time) could be confirmed.

## Decisions / Conclusions

- No formal conclusion was reached on the root cause of CNAF's low efficiency during this session; the group ran out of time before the last check (idle jobs' requested wall-clock time) could be evaluated. Memory exhaustion was ruled out as a cause; "pilot retiring" (pilots nearing end of lifetime and no longer accepting new jobs) was identified as a plausible major contributor, consistent with a ~2,000 idle-job figure Pablo recalled from the monitoring.
- Going forward, onboarding will proceed via the existing training slide deck, covered "a little at a time" (roughly a couple of presentations per week), the same approach Marco used previously with Luis Simas (ongoing since March and not yet finished). Marco explained this pacing is deliberate: covering everything at once would be too much to absorb, whereas spacing it out lets the trainee form questions from real exposure to the infrastructure first.

## Action Items

- [ ] Verify SSH access to all the HTCondor schedulers (the list shown during the session) once the required eGroups access (already added by Antonio) is confirmed with Viva and Luis, and re-run the `condor_status`/`condor_q` commands demonstrated in this session to confirm access works — Pablo Izquierdo Gonzalez
- [ ] Message Marco once access/commands are confirmed working — Pablo Izquierdo Gonzalez
- [ ] Write up proper documentation from the personal "cheat sheet" used in this session (Marco mentioned feeding his notes/cheat sheet and the meeting transcript to an AI assistant to draft a page, then fixing and publishing it) — Marco Mascheroni

## Discussion

### Onboarding approach
This was described as preliminary "shadowing" rather than formal training, since no structured training had yet been done with Pablo. Marco encouraged Pablo to interrupt and ask questions throughout. Pablo mentioned he had already reviewed some documentation sent by Antonio. Marco noted the same incremental approach ("a little bit at a time") had worked well with Luis Simas, because ramping up gradually lets the trainee form better, more specific questions than dumping all the material at once.

### HTCondor pool architecture (overview)
A basic Condor pool needs three components: a submit node (also called scheduler or, more recently, "access point" — the logical point where users access the pool and submit jobs), a central manager, and execute nodes (now called "execute points," running a process Marco referred to as STARTD). Pablo noted his prior experience was with ARC for the grid layer and Slurm ("new Slurm") for the batch system; Marco drew an analogy between a Condor pool and a Slurm batch system (submission host / worker nodes / matchmaking), while noting the CMS "global pool" is more complex: it is a virtual batch system built on the fly on top of many smaller site batch systems, assembled by sending pilot jobs that grab machines and connect them to the central manager. Marco deferred the details of how machines join the global pool (largely a WMS-role topic) to a later session.

Condor's matchmaking is based on ClassAds — Marco used the classic newspaper-classifieds analogy (machines advertise what they offer, jobs advertise what they need, and ClassAd language matches them).

Machines are typically grabbed as 8-core/16GB nodes; for Tier-1s these were migrated to 16-core/32GB nodes to support larger jobs. Jobs, however, vary independently in size — individual/analysis users mostly submit single-core jobs, while centrally managed production workflows tend to be multi-core. Because job and machine sizes don't always align, matchmaking can leave some resources unused. The Submission Infrastructure team has no control over what a running job actually does with the cores it's given (e.g., an 8-core job that doesn't use all 8 cores), but it does control **scheduling efficiency** — how well jobs are packed onto the machines the pool has grabbed. Checking this scheduling efficiency was described as what Marco was about to demonstrate.

### Scheduling efficiency monitoring
Marco showed the CMS Monit page ("CMS tenants" → the SI submission infrastructure box), which hosts various aspects of Submission Infrastructure monitoring, including slots monitoring and a slots-efficiency table. Marco reports this scheduling efficiency figure every Monday at the 5 PM meeting.

Efficiency is illustrated with an example: a site with 10 worker nodes of 8 cores each (80 cores total); if the only jobs available to schedule are, say, 4-core and 3-core jobs, some cores are left idle because they don't pack perfectly — e.g. only 70 of 80 cores get filled, giving ~87.5% efficiency. In the live monitoring shown, Tier-1 efficiency overall was 93%, which Marco characterized as "a little on the low side" — he considers anything below 95% worth investigating, with 96–98% as the target range.

Looking at the last-30-minutes view (used for live debugging, as opposed to the weekly cumulative average shown elsewhere on the page), IN2P3 and CNAF (transcribed inconsistently as "Knaf"/"Naf") both showed very low average CPU-idle figures; CNAF was around 40% idle, leaving roughly 3,000 cores idle, and was picked as the site to debug live. By comparison, FNAL was at 94–95%, not considered problematic.

### Live debugging commands at CNAF
Marco used `condor_status` (querying the central manager's collector process, which continuously gathers machine ClassAds) to inspect CNAF's worker nodes, using constraints/projections for the partitionable slots at CNAF and summing total slot CPUs and idle CPUs (`condor_status -pool ... -constraint ...`). Cross-checking against the monitoring page's more recent numbers, a small discrepancy was attributed to normal reporting lag (monitoring is refreshed roughly every ~12 minutes, so a ~10-minute-old snapshot can differ by a few hundred cores).

**Partitionable vs. dynamic slots**: partitionable slots are the slots intended to be split up as jobs land on them; when a job starts, a "dynamic" sub-slot (e.g. `slot1_1`, `slot1_2`, `slot1_3`) is created on the collector to represent that running job. Dynamic slots exist for informational purposes only and are not used by the negotiator for matchmaking; querying with `-const dynamic` shows what's actually running on a machine (e.g., in one example, two production jobs from a centrally managed workflow and one single-user analysis job, each 8-core with a stated memory request). Marco emphasized that the memory value on a running slot reflects what the job *requested*, not what it actually uses — but requested memory is what's used for scheduling purposes.

Marco walked through several possible reasons jobs might be idle instead of running, checking them in order:
1. **Memory exhaustion** — a partitionable slot could have free CPUs but no free memory left (because running jobs' memory requests, even if unused, fill up the slot's advertised memory), making it unable to accept more jobs despite having idle cores. Marco queried CNAF's partitionable slots for ones with free CPUs and zero free memory; this query returned no matching machines, ruling out memory as the cause at CNAF at that moment.
2. **Pilot retiring** — pilots have a finite lifetime (Marco stated roughly 2–4 days) and stop accepting new jobs ("retiring") once close to that limit, since starting a job that can't finish before the pilot must vacate would be wasted. Marco queried machines whose remaining glidein lifetime (`GLIDEIN_ToDie` minus current time) was within the last day, cross-referenced with available CPUs/memory, and found a substantial number of such pilots at CNAF — a plausible explanation, roughly consistent with a figure of ~2,000 idle jobs Pablo recalled seeing in the monitoring. In the same discussion, Marco noted that centrally managed production requests are split into job chunks targeting roughly 12 hours of expected runtime (not an exact science, since some chunks run long), and jobs requesting long wall-clock time become harder to schedule on pilots near the end of their lifetime.
3. **Local pilots** — Marco mentioned, as an additional possible factor (not checked for CNAF in this session), that some sites reserve part of their pledged resources for local, non-CMS users beyond their official CMS pledge (using IFCA as a hypothetical example: pledging 1,000 CPUs but having 1,500, with 500 set aside for local users via an existing mechanism), which would reduce the resources visible to the global pool.

Marco then moved to checking the **job queue** (as opposed to the collector, which only reflects running jobs): idle jobs live on the scheduler (schedd), not the collector, so a different command — `condor_q` — was needed. He demonstrated querying a single schedd first (`-name`), noting the non-batch (`-DAG`-less/unclustered) view vs. the default clustered/batch view, then querying across all CMS schedds at once (`-g`), and using `-long` to see full job ClassAd attributes (request CPUs, request memory, etc.) for an individual job.

To test the "jobs requesting long wall-clock time" hypothesis directly, Marco built a query for idle jobs (`JobStatus == 1`) at CNAF (using a `stringListMember`-style constraint against the desired-sites list) projecting request CPUs, request memory, and requested wall-clock minutes. Several such jobs were seen requesting roughly two days of wall-clock time. The session ended before Marco and Pablo could evaluate whether this fully explained the observed idle-job count, since Pablo had to leave for another meeting.

### Session wrap-up and next steps
Marco said this last check (job wall-clock requirements) was already moving into more advanced territory not yet in his own cheat sheet ("something I'd show maybe 3 months from now"), and that it was a natural point to stop rather than continue into log-level debugging, which would be more complex. He said he would document the commands used (and try to include example output) and send them to Pablo. Pablo said the session was useful for seeing how to check which sites have problems and inspect jobs/CPUs. Marco outlined Pablo's immediate next step: once eGroups access (already granted by Antonio) is confirmed with Viva and Luis, verify SSH access to all the schedulers shown and re-run the demonstrated commands, then message Marco to confirm access works — explicitly framed as low-pressure, self-paced ("if you feel like, okay, what do I do now, just write to me").

## Open Questions

- Whether the "jobs requesting long wall-clock time" hypothesis fully (or partly) explains CNAF's low scheduling efficiency was left unresolved; the query was run but not evaluated before the meeting ended.
- Whether "local pilots" (resources reserved for local, non-CMS users) is a contributing factor at CNAF specifically was not checked in this session.

## Related

[[HTCondor]] · [[Submission Infrastructure]] · [[Pilot Jobs]] · [[CMS]] · [[Global Pool]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-02 10.33.40 Marco Mascheroni's Personal Meeting Room`)
