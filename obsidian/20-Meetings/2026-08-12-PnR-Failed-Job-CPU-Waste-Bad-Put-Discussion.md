---
type: meeting
date: 2026-08-12
participants:
  - Marco Mascheroni
  - Kirill Ivanov
  - Piljun Gwak
  - Luís Simas
topics:
  - PnR failed-job CPU waste study
  - CPU efficiency vs "bad put" metric definitions
  - WMAgent job retries vs Condor restarts
  - committed core hours / HTCondor classads
  - WLCG scrutiny group reporting requirement
  - job/site resource-request mismatch (AOB)
---

# PnR Failed-Job CPU Waste Study: Bad Put vs Efficiency Metrics

## Summary

Marco Mascheroni met with Kirill Ivanov and Piljun Gwak (PnR) — with Luís Simas also invited to observe — to discuss a Level-1-requested study on CPU resources wasted due to failed jobs. Piljun explained that PnR's existing CPU-efficiency monitoring has a known limitation (it can include time spent waiting in the queue) and that PnR had been evaluating a "production efficiency" metric based on committed core hours instead. Marco used most of the meeting to explain the underlying HTCondor/WMAgent mechanics needed to define the study correctly: the distinction between WMAgent job retries and Condor restarts, the meaning of committed core hours vs. remote wall clock time, and why he believes "bad put" (wasted wall time, regardless of CPU efficiency) rather than "efficiency" is the right metric for failed jobs. The group also discussed how to break results down by site, and the broader context of why Level-1/WLCG is now asking experiments to self-report on failed-job resource waste. A separate AOB item was raised on behalf of Jennifer ("Jen") about a possibly-related study into resource waste from job/site size mismatches.

## Decisions / Conclusions

- The group agreed that "efficiency" (CPU time / wall time) is the wrong metric for failed jobs, since a failed job's output is discarded regardless of how CPU-efficient it was; the whole wall time is wasted either way. Marco proposed using the term **"bad put"** instead for failed-job studies, to avoid confusing it with the standard efficiency metric. Piljun and Kirill agreed this looks like a good metric for the PnR study.
- The group agreed the study should look at **two distinct types of "bad put"**, since they have different causes and different levels of controllability:
  - **Condor-restart bad put**: wall time lost when HTCondor itself restarts a job under the *same* Condor job ID (e.g. due to lost SCHEDD–worker-node connection, or a pilot vacating before a job that underestimated its wall time finishes). This does not depend on the job's content, though some root causes (e.g. wrong wall-time estimates, memory-related WMAgent watchdog kills) are potentially fixable upstream.
  - **WMAgent-retry bad put**: wall time lost across WMAgent's up-to-3 retries (each producing a *new* Condor job ID) when a job finishes but exits with a non-zero exit code. From Condor's perspective such a job succeeded (it ran and reported back); only WMAgent treats it as a failure.
  - Marco recommended studying both types rather than only one.
- Neither "bad put" (core hour − committed core hour) nor the underlying committed/remote-wall-clock-time classads include time a job spent idle/waiting in the queue — only time actually allocated on a machine.
- For site-level attribution of wasted resources, using the site recorded on the failed job's own record is expected to be reasonably accurate for jobs that were not subject to a Condor restart; for jobs that were restarted across multiple sites, attribution is less exact, but the group agreed not to worry too much about that complication for now.

## Action Items

- [ ] Ask Jennifer ("Jen") directly for more context on why she wants a study of wasted resources due to job/site resource-request mismatches, before scoping that work — Piljun Gwak
- [ ] Discuss the metric proposal internally and with Level-1 contacts Dima and Hasan, and come back to Marco if further input is needed — Kirill Ivanov (PnR)
- [ ] Share the meeting transcript with the group — Marco Mascheroni

## Discussion

### Background: why this study was requested

Piljun explained the study originates from a Level-1 request (the requester's name was transcribed unclearly, possibly "Elon Geis") to estimate CPU resources wasted specifically due to failed jobs. Marco added broader context: a WLCG scrutiny group reviews all four LHC experiments' resource usage efficiency. Historically, experiments have not needed to report on this themselves — sites report CPU efficiency for the pilot jobs they host (pilots are common across experiments, so this reporting is comparatively "impartial"), and a failed job that ran at 100% CPU efficiency looked fine from that site-level metric even though its output was thrown away. At the most recent WLCG scrutiny group meeting, reviewers reportedly asked experiments themselves (rather than sites) to report on failed-job waste, which Marco noted is a less objective ask than the traditional site-reported efficiency, since each experiment must now self-report and be trusted to have done a sound study. Marco believes this is why Level-1 (possibly Stefan, "Path," or Daniele — he was unsure) asked PnR to do this work, and expects Level-1 to present PnR's results to WLCG reviewers at an upcoming meeting; he does not think Level-1 has visibility into the level of technical detail discussed in this meeting.

### Existing PnR CPU-efficiency metric and its limitation

Piljun explained PnR has historically monitored CPU efficiency defined as CPU time hours over core (wall) time hours, but this metric has the limitation of including inefficiency from time jobs spend waiting in the queue. To avoid that, PnR started evaluating an alternative: inefficiency from failed jobs = 100 − "production efficiency," where production efficiency = 100 × (committed core hours of successful jobs) / (committed core hours of all jobs). Committed core hours were defined (per PnR's working definition) as core hours for only the last run of the job, excluding preempted/evicted attempts.

### WMAgent job retries vs. Condor restarts

Marco clarified a distinction he considered central to defining the study correctly:
- **WMAgent job retry**: WMAgent detects a job finished with a non-zero exit code and resubmits it, producing a **new Condor job ID** (up to 3 attempts).
- **Condor restart**: Condor itself determines a failure is infrastructure-related and resubmits the job keeping the **same Condor job ID** (Marco recalled a limit around 20 restarts but wanted to double check this is still accurate). Causes discussed include: the SCHEDD-to-worker-node TCP connection dropping, causing a new job to be scheduled without WMAgent noticing; and a job underestimating its declared wall time (the `MaxWallTimeMins` classad) — WMAgent does not enforce that a job actually finishes within its declared wall time, so a job may land on a pilot nearing the end of its lifetime and be evicted/restarted when the pilot has to vacate. In all Condor-restart cases there is no clean job failure (no non-zero exit code reported), so WMAgent cannot detect a failure and cannot perform its normal 3-retry logic.
- Kirill separately noted that HTCondor also has exit codes/limits for jobs that run for too long or remain idle for too long, causing the job to be killed (the transcript is unclear on the exact process/mechanism name involved). He noted CRAB jobs share the same submission infrastructure and commonly fail for these same reasons.
- Marco also noted that a WMAgent watchdog can end a job due to memory usage; this produces a standard error/output and a normal WMAgent-detected failure (not a Condor restart).

### Committed core hours, remote wall clock time, and "bad put"

Marco walked through the relevant base HTCondor classads (from which PnR's derived monitoring metrics, computed by the "spider" aggregation script Carlos runs every ~12 minutes, are built):
- `RemoteWallClockTime`: seconds the job has been allocated to a machine (including suspension, which is not used here); does **not** reset to zero when a job is evicted/restarted — it accumulates across all Condor-restart attempts for a given Condor job ID.
- `CommittedTime`: similar, but **does** reset to zero on eviction — it reflects only the time allocated on the machine for the current (last) attempt, excluding time spent in prior evicted attempts.
- Marco illustrated with a whiteboard sketch: for a given Condor job ID that has been evicted/restarted several times, "core hour" (derived from `RemoteWallClockTime`) covers the full accumulated wall time across all restart attempts, while "committed core hour" (derived from `CommittedTime`) covers only the final attempt.
- He described an existing monitoring definition of **"bad put" = core hour − committed core hour**, i.e. wall time lost specifically to Condor restarts, already computed via derived metrics (documented, per Marco, in OpenSearch). Marco noted this only captures Condor-restart waste; it does not by itself capture WMAgent-retry waste (separate Condor job IDs), which he suggested should also be measured for this study.
- None of these metrics involve CPU time — they are wall-time-only, which is deliberate for the failed-job use case.

### Site-level breakdown

Kirill described two related PnR goals: presenting the top 10 workflows by wasted CPU due to failed jobs, and identifying which sites account for the most wasted resources from failed jobs, in order to advise on the best way to break the study down by site. Marco raised a complication: he was unsure whether the system stores only the last site associated with a Condor-restarted job, or the full list of sites across all restart attempts (each restart attempt could in principle land on a different site). For jobs without Condor restarts, using the site recorded on the failed job record should be fairly accurate, since exit codes and the failing job's wasted wall time are both directly associated with a single site in that case.

### AOB: job/site resource-request mismatch study (raised on behalf of Jennifer)

Piljun relayed a separate request from Jennifer ("Jen"), who asked him to look into wasted computing resources caused by mismatches between what a job requests (e.g. 8 GB memory plus N cores) and what a site actually offers, which Piljun believes may relate to newly established PnR site-support processes intended to give site admins better information to manage their sites. Kirill added that Jen specifically wants to identify sites that lack accurate information about the resources they actually offer, in order to improve resource matching. Marco said the request as stated seemed vague to him and offered several possible underlying causes (a site not supporting a given job size; low-priority jobs being preempted at a site that does have the size), noting that jobs that remain pending are not themselves causing wasted/inefficient resource usage. He gave illustrative examples of per-site resource sizes he could share (e.g. CERN: 16 cores/32 GB RAM; Fermilab: much larger, subject to priority). He also asked whether the request was related to pledging (i.e. sites pledging resources that submission infrastructure isn't actually able to request/use, e.g. if a site only offers 4-core slots but the job queue for that site is 8-core), but this was not resolved. Marco recommended PnR meet with Jen directly to clarify the motivation and scope before starting analysis; Piljun agreed to ask Jen for more context.

### Logistics

Marco will be on vacation the week of August 17–21 and back on August 24. He suggested PnR could come back with a concrete metric proposal, after which a follow-up discussion (tentatively floated for a Friday morning) could take place; this was raised as a possibility rather than a confirmed commitment. Marco offered to help work out which specific classads/metrics to use once PnR has a proposal. He also introduced Luís Simas to the group as someone knowledgeable about submission infrastructure who can help if Marco is unavailable.

## Open Questions

- Is the Condor-restart limit still 20 attempts? (Marco was not certain and wanted to double check.)
- Does the monitoring pipeline record only the last site for a Condor-restarted job, or the full list of sites across all restart attempts? This affects the accuracy of any site-level breakdown of wasted resources.
- Which Level-1 contact (Stefan, "Path," or Daniele — transcription unclear) originated the request, and what exact detail level does Level-1 expect from PnR's report to WLCG reviewers?
- What is actually driving Jennifer's request about job/site resource-size mismatches — is it related to pledging accuracy, incomplete site resource information, or something else? To be clarified directly with her.
- What is the exact HTCondor/DAGMan mechanism Kirill referred to that kills jobs running or idle for too long (transcription unclear)?

## Related

[[HTCondor]] · [[WMAgent]] · [[CRAB]] · [[WLCG]] · [[CMS]] · [[Monitoring]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-08-12 10.40.14 PnR Dev Meeting`)
