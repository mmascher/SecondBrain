---
type: meeting
date: 2026-09-07
participants:
  - Giuseppe Bagliesi
  - Krittin
  - Chris Brew
  - Lars Sowa (KIT)
  - Antonio Perez-Calero Yzquierdo
  - Sebastien Gadrat
  - Marco Mascheroni
  - Stephan Lammel
  - Henryk Giemza
  - Pascal
  - usakornh (Que)
topics:
  - Early-September site incidents (IGTF CA bundle, redirector outage, OSG downtime accounting)
  - Security vulnerability status
  - FTS3 to FTS4 transition
  - Tape drive temperature issues
  - PIC transition to CTA tape storage manager
  - CC-IN2P3 internal network bottleneck
  - CRAB job scheduling efficiency at a French site
  - Site readiness "waiting room" state troubleshooting
  - Round-table site status reports
---

# CMS Facilities, Services and Site Support — Weekly Meeting (2026-09-07)

## Summary

This was the weekly CMS Facilities, Services and Site Support round-table meeting, chaired by Giuseppe Bagliesi, covering a mission/incident report followed by per-site and per-service status updates.

Giuseppe opened with a review of incidents at the start of September. An [[IGTF]] CA bundle update broke authentication for the first two days of September, affecting both the vacuum/validation system and "D" (unclear which system this abbreviation refers to); it was resolved by releasing a new IGTF version. At around the same time, a redirector service (transcribed as "the pizza redirect" — likely a mistranscription, possibly referring to a [[Frontier]]/Squid redirector) went down and stopped responding, causing distributed problems across user sites; Imperial College London (among others) was put into drain as a result. After the affected services were rebooted, production efficiency recovered from 84% to 94% within about an hour, and the failure rate dropped from roughly 1,000–1,500 per hour to about 100 per hour. Site readiness was corrected for sites affected by these two problems. A third, earlier issue involved an OSG downtime that was not being correctly accounted for by Monit; this was fixed, discussed at the last WLCG coordination meeting, and affected sites were corrected. A further issue around September 2 was mentioned but the transcript is too unclear to reconstruct its details; it was said to have been fixed quickly.

Giuseppe noted no news on security vulnerabilities since the previous week — the standing list of known public vulnerabilities remains valid and sites should check whether they are affected and patch accordingly.

A residual/central-services report (read by Giuseppe on behalf of someone unable to attend) noted that sites were starting to be moved to [[FTS]]4 for some transfers, and a message was posted on Friday to all CMS sites still on FTS3, because a bug had been identified in FTS3 and a fix is pending. There were also reports of unspecified problems with storage at a site where new storage is being installed, and reported problems with tape drives related to temperature requirements.

Round-table reports followed: EBSC (no report — the usual reporter was traveling), [[Frontier]] Squid (nothing to report), CMS Web (nothing to report), and Submission Infrastructure (nothing operational to report, but a team update: Pablo has joined as the new main Submission Infrastructure operator, having started the previous week). [[CRAB]] (Krittin) reported that CRAB tests were affected by the redirector problem and by a certificate-related policy renewal failure on a managed service, causing around 100,000 job failures; CRAB is now back to working as expected. Chris Brew reported roughly standard utilization (~100,000 cores through the week), generally low failure rates except for a spike tied to the redirector and IGTF certificate issues (which particularly affected Tier-1s), pulling overall efficiency down to about 73% for a couple of days around September 2; little central processing work was ongoing, so the site was running a high share of analysis, which carries relatively higher failure rates; only one new ticket this week, close to resolution.

Lars Sowa (KIT) reported KIT was also affected by the IGTF issue, causing a downtime, but no other issues. Antonio Perez-Calero Yzquierdo (PIC) reported the site had unexpectedly been left in drain for production since the previous day and re-enabled it once noticed; the main topic was PIC's transition to [[CTA]] (CERN Tape Archive) as its new tape storage manager, including commissioning of a new IBM tape library and a new environmentally controlled room (temperature/humidity). Performance and load tests run over the summer (July–August) wrote about 3 PB of CMS data to the new CTA tapes with no issues detected, which Antonio described as a success and as a useful mini stress test ahead of a planned mini tape data challenge before "Challenge 27" (Data Challenge '27) next year. The migration to CTA is scheduled to begin Monday, September 14, followed by several days of further commissioning and validation, during which there is a scheduled downtime. To avoid desynchronization between the old (transcribed as "NSTOR", exact system name unclear) and CTA databases, PIC will also have a separate scheduled downtime for writing to tape starting the next day (September 8) and lasting until the day before the migration.

Sebastien Gadrat (CC-IN2P3) reported a "blank spot" last week, likely caused by high activity from other WLCG experiments creating a bottleneck on an internal network link between storage and worker nodes on Wednesday and Thursday; the problem resolved itself. CC-IN2P3 plans to upgrade most internal links so this should not recur for the next run. A quarterly scheduled downtime was announced for September 22.

Marco Mascheroni raised a scheduling-efficiency issue he and Pablo had been debugging at a site referred to in the transcript as "N2P.3" (likely IN2P3/CC-IN2P3, though the transcript is unclear): they traced it to the absence of production jobs, combined with very short CRAB jobs (on the order of three minutes) that cycle quickly, which the workload management system is not built to handle efficiently. Marco also asked about the meaning of a yellow "production status" indicator he had seen. Stephan Lammel explained that this status (transcribed as "train", exact term unclear — possibly "drain") means jobs already in the queue continue to run, but the workload management (WM) system will not add new jobs to the queue; this was due to SAM and CE HammerCloud tests not running for about two and a half days. Stephan expected the status to switch back the next day since the underlying issue was resolved.

Henryk Giemza reported for a site Giuseppe referred to as "Sveirka" (transcription unclear). The site was affected by the IGTF issue only indirectly via external services, since it had not updated certificates on its own dCache instance. The day after the redirector issue (reported at Pisa), the site's own redirector also had a problem and needed a restart; after restarting, roughly one in four transfers to the global redirector were found to be hanging, which Henryk ticketed but believes has since been resolved elsewhere. Separately, the site had unexpectedly been placed into a "waiting room" state in site readiness despite good HammerCloud and FTS status, and Henryk asked for help understanding why. Stephan Lammel investigated live: sites are placed into the waiting room after accumulating multiple (around 3–5) "unknown" site-readiness evaluations within a two-week window; he found an "unknown" evaluation on September 5 caused by missing FTS information for that site that day, because the FTS evaluation had run too late — site readiness runs about half an hour after the FTS evaluation, and if the FTS evaluation isn't complete by then, the FTS component of the readiness score is marked unknown. Stephan characterized this as a technical issue on the site-readiness/FTS-evaluation side (not attributable to the site itself) and committed to rerun the evaluation for that day to clear the waiting-room status. Henryk raised a possible connection to IPv6 support, but Stephan attributed the issue specifically to slow delivery of monitoring information via Monit rather than confirming an IPv6 cause.

Chris Brew noted, on behalf of Katie (who was in a clashing meeting), that her report had been updated but there was nothing notable to highlight. Pascal (site not otherwise named, apparently a US-based site given the mention of the Labor Day holiday) reported nothing major, noted some SAM status irregularities seen on the dashboard, said EOS nodes had been updated to version 5.3 with one "t-cas" node still offline, and confirmed the site was not affected by the IGTF issue because it pulls CAs from OSG. Red dots seen in site readiness on September 2 were believed to be a fluke, which Pascal said they would confirm.

## Decisions / Conclusions

- The IGTF CA bundle authentication break (first two days of September) was resolved by releasing a new IGTF version.
- The redirector outage and its downstream site impact (e.g., Imperial College London drained) were resolved by rebooting the affected services; production efficiency recovered from 84% to 94% within about an hour, with failure rates dropping from ~1,000–1,500/hour to ~100/hour. Site readiness was corrected for affected sites.
- The OSG downtime accounting problem in Monit was fixed, discussed at the last WLCG coordination meeting, and affected sites' readiness was corrected.
- CRAB is confirmed back to normal operation after the redirector and certificate-renewal issues.
- PIC's CTA migration testing (summer 2026 performance/load tests, ~3 PB written with no issues) was judged successful; the transition to CTA will proceed, starting September 14 with a following period of commissioning/validation downtime. A separate tape-write downtime at PIC starts September 8 and runs until the day before the migration, to avoid database desynchronization between the old tape system and CTA.
- CC-IN2P3's network bottleneck from last week resolved itself; internal link upgrades are planned so it should not recur for the next run. A quarterly scheduled downtime is set for September 22.
- The "yellow"/drain-like production status Marco asked about was due to SAM and CE HammerCloud not running for ~2.5 days; expected to clear as tests resumed.
- Henryk Giemza's site's "waiting room" status was attributed to a technical issue (FTS evaluation completing too late for that day's site-readiness run) rather than any actual site problem; Stephan Lammel agreed to rerun the evaluation to clear it.

## Action Items

- [ ] Rerun the site-readiness/FTS evaluation for September 5 to clear the affected site's "waiting room" status — Stephan Lammel
- [ ] Confirm whether the site-readiness red dots seen on September 2 were a fluke — Pascal

## Discussion

### Early-September incidents
See Summary — IGTF CA bundle authentication break, redirector outage affecting multiple sites (e.g., Imperial College London), and OSG downtime not correctly reflected in Monit-based site readiness. An additional, unclear issue around September 2 was mentioned but not reconstructable from the transcript.

### FTS3/FTS4 and storage/tape issues
Sites still on FTS3 were notified (posted Friday) of a known bug pending a fix, as CMS begins moving some transfers to FTS4. Unspecified storage installation issues and tape drive problems tied to temperature requirements were also reported, without further detail.

### PIC / CTA tape migration
Antonio Perez-Calero Yzquierdo described the multi-month effort (new IBM tape library, new environmentally controlled room, new tape storage manager CTA) as nearing completion, with a scheduled cutover starting September 14 and an associated tape-write downtime beginning September 8 to avoid conflicts between the old and new tape database systems.

### CC-IN2P3 network bottleneck and CRAB short-job scheduling
Sebastien Gadrat linked a transient internal-network bottleneck to high activity from other WLCG experiments; a fix (internal link upgrades) is planned before the next run. Separately, Marco Mascheroni and Pablo had been debugging scheduling inefficiency they attributed to very short CRAB jobs at a site referred to as "N2P.3", which the workload management system does not handle efficiently when few/no other production jobs are running.

### Site readiness / production status mechanics
Stephan Lammel explained two related mechanisms during the meeting: (1) a "yellow"/drain-type production status that stops new job submission (but lets queued jobs finish) when SAM/CE HammerCloud tests haven't run for an extended period; and (2) the "waiting room" state, triggered by an accumulation of "unknown" readiness evaluations within a two-week window, which in this case stemmed from FTS evaluation data arriving too late for a given day's site-readiness run.

## Open Questions

- What exactly "D" refers to in Giuseppe's remark that the IGTF authentication break affected "not only vacuum/validation but also D".
- The exact nature and resolution of the additional issue mentioned as occurring around September 2 (transcript unclear).
- What system name is intended by "NSTOR" in Antonio's description of the PIC database-desynchronization risk between the old tape system and CTA.
- Whether the "N2P.3" site Marco referred to is CC-IN2P3, or a different site — the transcript does not clearly resolve this.
- Whether IPv6 support plays any role in the transfer-hanging issue Henryk Giemza raised (Stephan attributed the separate waiting-room issue to slow Monit data delivery, not IPv6, but did not directly address Henryk's IPv6 question).

## Related

[[CMS]] · [[WLCG]] · [[CRAB]] · [[Frontier]] · [[FTS]] · [[IGTF]] · [[Monit]] · [[CTA]] · [[WMAgent]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-07 16.20.22 CMS Facilities, Services and Site support`)
