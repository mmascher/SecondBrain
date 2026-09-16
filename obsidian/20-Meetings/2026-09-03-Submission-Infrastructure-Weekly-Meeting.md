---
type: meeting
date: 2026-09-03
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Luis Simas
  - Pablo Izquierdo Gonzalez
  - Hyunwoo Kim
topics:
  - New operator Pablo Izquierdo Gonzalez joining the team
  - Negotiator cycle time degradation / low slot utilization incident
  - CPU efficiency discussion (Wednesday general meeting, upcoming topical session)
  - Run 2 HLT machines (P5 → B2K8) status
  - Pool size and utilization overview (CERN, global, Tier-1s)
  - Schedd (SCADI) security update / Condor version upgrade status
  - TEIGI tokens with infinite lifetime
  - CRAB schedd out-of-memory incident (DAG startup spike)
  - Front-end certificate renewal
  - Site (CE) tokens migration
  - HPC / dynamic resources (BSC, MareNostrum)
  - Grafana alarm tuning
  - Overloaded-slots monitoring anomaly on ITB (Fermilab front end)
---

# Submission Infrastructure Weekly Meeting (2026-09-03)

## Summary

This was the first Submission Infrastructure weekly meeting after the summer break, and the first attended by Pablo Izquierdo Gonzalez, the new devops hire who will act as main operator for the HTCondor/glideinWMS component and front-end side of the team. Antonio opened by welcoming Pablo and noting the team is back to nominal staffing (Luis and Pablo at Fermilab, Marco and Antonio remote, with Antonio also doing some coordination work).

The bulk of the meeting was Antonio catching up on news from the Monday and Wednesday general meetings and reviewing infrastructure status after his August absence. Key threads: a transient negotiator-cycle-time degradation (traced to a cluster of misbehaving CRAB schedds around Monday–Tuesday of that week, possibly related to an IGTF-driven issue affecting the wider grid), the ongoing/recurring CPU-efficiency discussion at the CMS level (with a dedicated topical slot planned the following week), status of the SCADI security-patch cycle (nearly complete except P&R's production schedd), a discussion on how to handle TEIGI tokens with infinite lifetime, a CRAB schedd out-of-memory incident caused by many DAG processes starting simultaneously when resources suddenly became available, and a round of status updates from Luis on site-tokens (ARC-CE → HTCondor-CE) migration, Grafana alarm tuning, and an unresolved anomaly in the overloaded-slots monitoring metric for a site on ITB. The meeting transcript ends mid-discussion of the latter topic.

## Decisions / Conclusions

- The August negotiator-cycle-time degradation and associated pool efficiency dip (global pool average around 92%, Tier-1s around 93%, dipping to ~85% at points) is understood to be a transitory event caused by a cluster of misbehaving CRAB schedds ("skedds") whose slow negotiation cycles caused the negotiator to drop and retry them, dragging down scheduling efficiency for the affected period. This is a known, recurring pattern, but this cluster was larger than usual. Luis suggested it may be related to an IGTF issue affecting the wider grid earlier in the week, which could have caused job failures/restarts; Antonio agreed this is plausible but unconfirmed. The group considers this closed as a transitory issue, to be watched for recurrence rather than actively investigated further.
- SCADI security patching (from the vulnerability-driven update cycle discussed before the summer) is essentially complete except for P&R's production schedd: CRAB schedds, Tier-0 schedds, CMS Connect, and the MIT institutional schedd are all updated. One P&R QA schedd has been updated to a patched version and is awaiting P&R's validation before the production schedd can be updated; P&R (Stefano's team) is currently overloaded, causing delay.
- The MIT institutional schedd is treated as a special case: it is the only "institutional schedd" allowed to overflow analysis jobs into the global pool (a historical exception negotiated in the past). Because it connects to the global pool, it must be held to the same security/update standard as other connected schedds, or the connection should be dropped.
- Central-manager/collector Condor upgrades have not yet been done; the team was waiting for Pablo to join so this can be used as a first hands-on training exercise for him.
- Root cause of the CRAB schedd out-of-memory incident: when a large amount of global-pool capacity suddenly became available (because production jobs weren't using it), CRAB's per-workflow DAG processes — normally mostly idle/sleeping — all started up near-simultaneously to submit jobs, and startup consumes more memory per process, causing the schedd to run out of memory. There is a configured limit on the number of concurrent DAGs, but it is sized for normal/staggered startup conditions, not for many DAGs starting at once; lowering the limit would reduce achievable job throughput, so it is not straightforward. The CRAB operator mitigated this by holding/releasing DAG releases gradually. Marco discussed this with Stefano, who suggested it wasn't worth raising with Jamie (HTCondor dev) at the time, but Marco still has it noted to raise when a meeting with Jamie happens (none since June/July).
- Antonio's position: CRAB should be able to scale to use most/all of the global pool (e.g. even if Fermilab's ~50-60k cores became fully available to CRAB) without being on the brink of breaking; only reaching ~50% of the pool (roughly doubling CRAB's typical scale) and then being unable to sustain it is viewed as a real scalability limitation on the SI/CRAB side, not just a timing/coincidence issue.
- The overloaded-slots monitoring metric anomaly (a site showing ~66% "overloaded" instead of the expected boolean true/false-like value) is now believed to have started around the time the Fermilab ITB front end was switched to glideinWMS 3.11.x, and appears limited to CNAF's pilots on ITB (not seen in production, and not on the CERN front end). However, Hyunwoo noted the front-end version change may not be the actual cause: he found he had not yet applied a related Mattermost-discussed config change from about four months ago, and planned to apply it the same day; Luis remained unconvinced the 3.11.x change was the cause given the issue looked complex with possibly multiple contributing causes, and proposed continuing to run the front end on Fermilab and iterating. Luis clarified the 66% figure comes from a value set on the Factory side, not the front end, differentiating it from a previously-fixed issue involving a lowercase/uppercase true-false value being overwritten on the front end.
- Grafana alarm review: the first pass of tuning is complete. Luis disabled noisy email alerts (e.g. a "site has fewer cores than expected" alarm compared against a 1-2 week average) and considers the alarms now usable ("happier than a few months ago"); further tuning is expected to be incremental, including revisiting alarm thresholds and definitions. Luis plans to discuss which alarms are most relevant to Pablo's role.
- Site (CE) tokens migration: 19 of the tracked sites are done, 3 remain plus one that gave up on ARC-CE and is migrating to HTCondor-CE (a low-activity Taiwan Tier-3 that hasn't run jobs in months). Of two MIT HTCondor-CEs, one was migrated during August; the last one is pending.

## Action Items

- [ ] Check the pilot efficiency numbers from Luis Nawal (referenced in the Condor/efficiency meeting with Stefan) — Marco Mascheroni
- [ ] Iron out remaining technical details of the data-driven matchmaking proposal with Jamie — Marco Mascheroni
- [ ] Share the data-driven matchmaking proposal with the group once it is in a more finished state — Marco Mascheroni
- [ ] Perform Condor upgrades on the central manager / collectors, as a first training exercise — Pablo Izquierdo Gonzalez
- [ ] Everyone: list any TEIGI tokens with infinite lifetime that they are aware of, so the group can build a tracked list (Luis noted he already opened a ticket for this) — all
- [ ] Update the production P&R schedd to the patched version once P&R completes validation of the QA schedd — Luis Simas
- [ ] Raise the CRAB DAG-startup-memory scaling issue with Jamie once a Condor meeting happens — Marco Mascheroni
- [ ] Apply the front-end config change from ~4 months ago (referenced on Mattermost) to the Fermilab ITB front end — Hyunwoo Kim
- [ ] Continue investigating the root cause of the overloaded-slots metric anomaly on the Fermilab ITB front end (CNAF) — Luis Simas
- [ ] Continue directing remaining site admins to complete CE token migration for the long-tail sites — Luis Simas
- [ ] Restart activity with Barcelona Supercomputing Center to reconnect their resources (including manually-launched glideins / MareNostrum) to the global pool — Antonio Perez-Calero Yzquierdo

## Discussion

### Team update

Pablo Izquierdo Gonzalez has joined as the new devops for the HTCondor component of Submission Infrastructure and the front-end side. This restores the team to its nominal core staffing: Luis and Pablo at Fermilab, Marco remote, and Antonio remote doing some competitive/coordination work. This was Pablo's first SI weekly meeting.

### Negotiator cycle time / low slot utilization

Antonio reviewed pool efficiency plots after returning from vacation, prompted by a mention at the Monday meeting of low slot utilization. Global pool efficiency averaged around 92%, Tier-1s around 93%, with a dip to around 85% during a period around Monday–Tuesday of that week. Antonio's hypothesis, offered as plausible but unconfirmed, is that a cluster of CRAB schedds ("skedds") took too long in the negotiation cycle, causing the negotiator to drop them and move to the next schedd to avoid stalling the whole cycle, which in turn slowed replacement of expiring job slots and reduced pool efficiency. Luis raised a possible connection to an IGTF issue earlier in the week that caused grid-wide problems and could plausibly have driven high job-restart rates with a matching timeline. Hyunwoo asked clarifying questions about the time window of the plots (30-day view) and whether such spikes recur (yes, periodically, though this cluster was unusually large) and whether effects on efficiency could be delayed relative to the negotiation slowdown; Antonio agreed a delayed, gradual effect is plausible since slot depletion builds up as expiring jobs fail to be promptly replaced, and that the impact would depend on whether affected schedds are running shorter analysis jobs (CRAB) versus longer production jobs. The group considers the event transitory, to be watched rather than actively pursued further.

### CPU efficiency (Wednesday general meeting)

Antonio noted the Wednesday general meeting mentioned that next week's meeting will include a topical session on efficient CPU/slot utilization, tied to a broader look computing operations has been taking (since early summer) at global CPU utilization — not just scheduling efficiency but also job failures and output-transfer failures. Marco reported that at a Condor meeting the prior day (with Stefan, not Jamie, who did not attend), Stefan mentioned a couple of proposed ideas to improve efficiency, including requesting new HTCondor features (e.g. starting a job during stage-out); Marco could not recall the second idea. Antonio and Marco noted this topic recurs at essentially every LHCC review cycle, driven by new referees repeatedly asking CMS to justify its CPU efficiency. Marco separately mentioned he showed Stefan his proposal for data-driven matchmaking (developed with Andrea after the Scientific Workflow Management retreat at LPC) and still needs Jamie's input on some technical details before sharing it more broadly with the group; he had shared the document link in the meeting announcement.

### Run 2 HLT machines / P5 activity

Antonio noted the Run 2 HLT machines being transferred from P5 to B2K8 (as previously discussed) are still not ready — they are being configured via Puppet, and the advancement expected during August did not materialize. Status of the Run 3 HLT machines (approx. 2,000-2,800 range, unclear exact figure) is unknown; Antonio observed heavy detector-decommissioning activity at P5 based on general CMS meeting slides, and flagged it as worth asking about whether/when these HLT resources might become available for offline use.

### Pool size and utilization overview

Antonio reviewed pool sizes: CERN pool averaging a bit below 80,000 CPU cores (lower than typical, attributed to the SP5 cloud resources not yet being reinstalled), global pool around 364,000 cores. Among Tier-1s: KIT is healthy with headroom; RAL is reasonable given it's a comparatively smaller active Tier-1; IN2P3 is okay; CNAF showed a period of higher-than-usual utilization, possibly from manually-launched glideins (Marco noted seeing pilots from Chula/Thailand connecting via the global pool, though the cause of CNAF's pattern is unclear) followed by a drop, possibly related to CNAF's site readiness/commissioning status (Luis noted CNAF had some tests failing, though site was not down); this may be a contributing factor to the global pool's overall reduction in size, alongside overpledge-related fluctuations elsewhere. No other issues were identified with the pools.

### SI monitoring orientation for Pablo

Antonio walked Pablo through the starting points for SI monitoring: Grafana, under the CMS area, in the Submission Infrastructure folder, which contains multiple dashboards (slots monitor for the pool, negotiator/central-manager metrics, and front-end/glideinWMS metrics). Pablo has been bookmarking the relevant URLs. Antonio proposed dedicating future sessions to go through the dashboards in depth with Pablo.

### Condor version upgrades / SCADI security patching

Antonio asked for a status update on SCADI upgrades related to previously-discussed vulnerabilities. Luis reported: CRAB schedds have been updated for a long time; Tier-0 schedds were updated the previous week; CMS Connect is updated; the MIT institutional schedd is updated. Only the P&R production schedd remains on a vulnerable version — one P&R QA schedd has a patched version awaiting P&R validation before the production schedd can be updated, and P&R is currently overloaded. Antonio explained the MIT schedd's special status as the only institutional schedd permitted to overflow analysis jobs into the global pool (a historical exception), which is why it must meet the same security bar as other globally-connected schedds. Marco noted the MIT contact (a CMS Connect / MIT-side administrator, "David Walter") was difficult to track down via forwarded emails; the relevant CMS contacts mentioned in this context were Lundsted (not Voisin) for escalation if needed. Separately, central-manager/collector Condor upgrades have not yet started; the team had been waiting for Pablo to join so this can serve as a first hands-on exercise for him.

### TEIGI tokens with infinite lifetime

Luis raised (recalling an earlier discussion with Marco and Stefano) that SCADI tokens used to connect to the global pool have a roughly one-year lifetime for QA schedds but infinite lifetime for production schedds. Prompted by having to renew tokens for some disconnected QA schedds, the question arose of whether infinite-lifetime tokens should continue to be used for production. Luis said he is wary of infinite-lifetime tokens but noted there currently isn't a good way to update/rotate them smoothly. Marco explained the practical concern: if a token is compromised, the response for a finite-token setup would be a HTCondor feature to revoke a specific token; for infinite tokens, a compromise would otherwise require rotating the schedd's whole key. Marco proposed a middle path: continue allowing infinite-lifetime tokens (to avoid the annual renewal burden, especially since the team's current tracking table of tokens has fallen out of date) but maintain an explicit, up-to-date tracked list specifically of infinite-lifetime tokens. Luis characterized this as still an open question needing further exploration, though he agreed Marco's proposal is a valid option. Hyunwoo asked for clarification on what TEIGI is (CERN's secrets-storage system, retrieved via Puppet) and noted CMS SI's ID tokens on AI machines are already effectively infinite-lifetime. The group agreed as an action item that everyone should contribute known infinite-lifetime tokens to a list Luis has already opened a ticket to track (starting with the CRAB one).

### CRAB schedd out-of-memory incident

Antonio raised a recalled report of CRAB schedds running out of memory, initially wondering if it was overflow-related. Marco clarified: the scale itself (roughly doubling CRAB's running job count, e.g. 75,000 to ~150,000) was not the problem. The actual cause was that when a large amount of pool capacity suddenly became free (because production wasn't using it), many CRAB per-workflow DAG processes — normally idle/sleeping between submitting jobs — started up nearly simultaneously; process startup uses more memory, and the resulting concurrent startups exhausted schedd memory. A configured limit exists on the number of concurrent DAGs, but it is tuned for normal (staggered) conditions, not simultaneous mass-startup; a stricter limit would constrain normal throughput. The CRAB operator mitigated the immediate incident by holding/releasing DAGs gradually. Marco discussed this with Stefano, who suggested at the time that raising it with Jamie wasn't necessary, but Marco still intends to raise it in a future Condor meeting with Jamie (none has occurred since June/July). Antonio argued this represents a real scalability limitation worth addressing proactively: CRAB should be able to make use of most/all of the global pool (e.g. even a scenario where Fermilab's full ~50-60k cores became available) with comfortable headroom rather than being pushed to the brink, and that reaching only ~50% of the pool before hitting this limit is a meaningful constraint, not just unfortunate timing. Marco noted this ties into WM/SI integration discussions (acquisition and matchmaking of slots) and that a similar concern applies on the production side for large HPC allocations. Marco suggested this could be relevant to CSA28 (a future computing/scale-testing exercise) planning.

### Front-end certificate

Luis confirmed the front-end certificate renewal issue (previously flagged by Florian) is resolved and now renews automatically; he expressed hope this is the last time manual intervention is needed.

### Site (CE) tokens migration

Luis reported the ARC-CE → HTCondor-CE migration is nearly complete: 19 of the tracked sites (previously described as needing migration) are done, 3 remain, and one site (a low-activity Taiwan Tier-3, which hasn't run jobs in months) has given up on ARC-CE and is migrating to HTCondor-CE instead. Remaining sites are being chased via their site admins, with some slow responses. Separately, of two MIT HTCondor-CEs, one was migrated during August, leaving one pending.

### HPC / dynamic resources

Antonio's plan is to restart engagement with Barcelona Supercomputing Center (BSC) to reconnect their resources (including MareNostrum) to the global pool, building on earlier work with manually-launched glideins. No other updates on HPC/special resources this week.

### Grafana alarm tuning

Luis reported the first pass of alarm review/tuning is complete; he disabled noisy email alerts, for example a "site has fewer cores than expected" alarm that compares current cores against an average of the last 1-2 weeks. He described the alarms as now usable and improved compared to a few months ago, and expects further tuning to be incremental (thresholds, definitions of what's being measured). He plans to discuss with Pablo which alarms are most relevant to his role.

### Overloaded-slots monitoring anomaly (ITB, Fermilab front end)

Luis presented a Grafana plot (linked on Mattermost) showing the percentage of "overloaded" slots in the pool, which is expected to behave like a boolean (near 0% or near 100%) but was instead showing an unexpected ~66% value for a specific case. Luis's investigation so far points to the change coinciding with switching the Fermilab ITB front end to glideinWMS 3.11.x, and the anomaly appears limited to CNAF's pilots on ITB (not seen in production, and not on the CERN front end, which does not show the issue). Hyunwoo, checking live during the meeting, said the 3.11.x version itself may not be the cause: he realized he had not yet applied a related front-end configuration change discussed on Mattermost about four months earlier, and planned to apply it the same day. Luis said he remains unconvinced the version change is the root cause, characterizing this as a complex issue with potentially multiple contributing causes, and proposed continuing to run the front end on Fermilab (rather than reverting) and iterating. He clarified that the 66% value originates from a setting on the Factory side, not the front end, distinguishing this from a previously-resolved issue where a lowercase/uppercase true/false front-end value was being overwritten. The transcript ends during this discussion, with Hyunwoo asking whether the ITB front end running 3.11.4 is otherwise okay aside from this specific problem; Luis's answer is not captured in the available transcript.

## Open Questions

- Whether the August negotiator-cycle-time degradation was actually caused (or contributed to) by the IGTF issue affecting the grid that week — unconfirmed hypothesis.
- Whether/when Run 3 HLT machines at P5 might become available for offline utilization, given heavy detector-decommissioning activity.
- Whether computing operations' broader CPU-efficiency review has requested any specific report or slot-usage information from the SI team — unclear as of the meeting.
- Whether infinite-lifetime TEIGI tokens should be phased out in favor of a renewal mechanism, versus retained with tracking — open question per Luis.
- Root cause of the overloaded-slots monitoring anomaly on the Fermilab ITB front end (CNAF) — investigation ongoing, transcript cuts off before resolution.
- Whether the ITB front end running glideinWMS 3.11.4 is otherwise functioning correctly aside from the overloaded-slots anomaly — question posed by Hyunwoo, answer not captured in the transcript.

## Related

[[HTCondor]] · [[glideinWMS]] · [[CRAB]] · [[WMAgent]] · [[Factory]] · [[Factory Operations]] · [[Submission Infrastructure]] · [[CERN]] · [[CMS]] · [[Pilot Jobs]] · [[WLCG]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-03 17.06.17 Submission Infrastructure Weekly Meeting`)
