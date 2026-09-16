---
type: meeting
date: 2026-05-07
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Luis Simas
  - Hyunwoo Kim
topics:
  - OpenSearch index mapping/type inconsistency and the decision to wait for data expiration
  - manual gliding entry parameter fix (monitoring script correction)
  - long-term (non-expiring) Monit/OpenSearch index setup and backfill plan
  - handling of missing CPU-count and missing-memory pilot entries in monitoring (RAL, MIT, US Tier-2s)
  - overloading/efficiency dashboard review with corrected data
  - concern about historical data-format inconsistencies ahead of long-term backfill
  - factory operations: Nanjing Normal University, Rome Tier-2, Bristol Tier-2-to-Tier-3 move
  - upcoming site-token migration for Condor-CE entries
  - GPU/MIG status (RAL, CERN Tier-2, AMD GPU testing at Finland site)
  - "copy fail" kernel vulnerability patching on factory machines
  - CHEP rehearsals/posters next week
  - Fermilab outage follow-up and idle-CPU/memory-depletion analysis
---

# Submission Infrastructure Weekly Meeting

## Summary

Luis opened with monitoring work. An OpenSearch index used for pilot overloading/efficiency data had a field-mapping inconsistency: data inserted earlier in a malformed way created one field type, and correctly-formatted data now being inserted has a different type, causing the dashboard to break. The group discussed two options — deleting the affected index (losing about 7 days of data) or waiting for the affected data to expire naturally (the index has a 30-day retention) — and agreed to wait, since only the 7 oldest days currently have the wrong type and the problem resolves itself within a week. Luis confirmed he had already fixed the underlying script (on the monitoring machine, VOCMS0850) that was pushing a malformed "manual gliding entry" parameter, enforcing the expected type going forward and logging whenever a conversion is needed. Luis also reported he backfilled data from Marco's separate long-running collection effort into the standard 30-day Monit index to eliminate anomalous efficiency values (e.g., values over 400%) that had appeared before the script fix; those anomalies are gone both before and after the fix once corrected data is used.

Discussion moved to the newly created long-term (non-expiring) Monit/OpenSearch index/stream, which the Monit team has already set up after Luis described the use case and expected data volume; the factory is technically ready to push production data to it via Monit's routing layer (which can send data to the default 30-day stream, the long-term stream, or both). Before doing that backfill, Luis wants to validate that currently-collected data is correct, to avoid pushing malformed data into a stream with no expiration (unlike the 30-day stream, where bad data eventually ages out). Marco raised a related concern: because his manually-collected long-term dataset spans about a year and a half, during which the data format changed at least once (e.g., an "overloaded" field changed from Boolean to a percentage/string at some point), there could be latent inconsistencies that only surface once historical and current data coexist in a single non-expiring index — a different failure mode from the current dashboard break, and one that would require reviewing and re-inserting corrected historical data if it occurs. Luis agreed to double-check this before proceeding.

Antonio and Luis then reviewed Antonio's updated overloading dashboard (edited to fix the time window at ~12 hours and remove the earlier variable time-window option) using the corrected data. Overall trends looked reasonable, with a clear gap between overloaded-true/false efficiency values, though some sites still showed gaps or irregular patterns. Investigating specific cases surfaced two related monitoring gaps: (1) some entries (e.g., RAL) are missing a reported CPU count, and the current script response is to skip inserting data entirely for those pilots rather than compute possibly-wrong values; (2) some sites (RAL, MIT, and reportedly many US Tier-2s) don't report memory usage/request at all, and these were also being skipped, even though CPU data was correct — which was unexpectedly affecting sites as significant as RAL (a Tier-1). The group agreed that: (a) skipping insertion when CPU count is unknown is acceptable, being both correct behavior and a minor/corner case overall; but (b) when CPU is known and only memory is missing, the data should still be pushed, accepting a partial dataset for memory (favoring CPU over memory), rather than skipping the whole entry. The root cause of missing memory reporting (possibly related to translation between condor/pilot software and remote ARC-CE/batch-system stacks, e.g., Slurm) is not understood and was flagged for follow-up investigation, though not treated as urgent since CPU remains available in these cases.

Luis said that after implementing this adjustment (push data when only memory is missing) and double-checking the historical-format concern, he will redo the test-index backfill and then push to the production long-term index, tentatively "maybe tomorrow"; this requires coordinating with the Monit team, who need to create the query mapping once real data starts flowing.

On factory operations, Luis reported a quiet week for tickets: Nanjing Normal University's SAM tests are still pending on the site side (not blocked on Submission Infrastructure); the Rome Tier-2 entry (working in ITB but not in production) remains blocked on the site admin investigating the local batch system, with Luis offering to look for additional grid-manager logs; and the Bristol entry move from Tier-2 to Tier-3 (raised by Antonio via Mattermost) mainly requires changing the entry name and the CMS site class. Luis also flagged an upcoming factory task to migrate all Condor-CE entries' authentication method from grid proxy to site tokens — more than 100 entries — which will need to be tested and validated in ITB before being flipped in production.

On GPUs, there was no progress since Tuesday's discussion. The RAL entries remain blocked on the site admin due to a failing "obtainer" validation. Thomas (Finland) pointed the team to another contact (identified as Andrea Bocchi) experimenting with AMD GPUs, but there has been no follow-up yet; Antonio clarified the team's interest is specifically in how pilots interact with and discover GPU resources (scheduling, resource discovery) rather than physics-code performance, and noted this AMD testing appears to use local (non-grid) access rather than grid access, which is a different setup from what the team needs. Luis noted the only MIG-enabled entry currently usable is at RAL (currently blocked), but a MIG-enabled entry also exists at the CERN Tier-2, which Luis said he could start using for testing. Antonio suggested it would be useful to compare the output of the Condor discovery tool run via the pilot at a MIG-enabled site versus a full-GPU site, noting the device-name attribute already shows an indication that a MIG instance (not a full GPU) is being received, and there may be other discoverable differences worth documenting.

As an aside, Antonio reminded the group that next week's CHEP-related deliverables (TikToks, posters, rehearsals) are coming up and drafts/material need to be worked on; placeholders for pending plots or information are acceptable for the rehearsal. Antonio expressed particular concern about the GPU-related contribution, describing it as the least advanced and most open-ended of the team's contributions, still in a preliminary/data-gathering phase rather than one based on hands-on experimentation.

Luis noted, for completeness, that all factory machines are already patched against the "copy fail" kernel vulnerability; he is unsure which other machines can safely be rebooted and asked to be told if action is needed elsewhere.

Hyunwoo gave a Fermilab update: electricity from the power company is fully restored with no ongoing power issues, though the power company is still working to re-establish one of the affected towers (one gate remains closed in the meantime). Hyunwoo then shared efficiency plots showing the effect of the earlier power outage and of the "copy fail" patching/reboot cycle (done on the following Thursday), plus a separate, more recent efficiency drop starting the day before the meeting (down to roughly 70-80%). Antonio recapped an explanation from a Monday discussion with Dave Mason: the recent dip was attributed not to the outage/reboot events but to a period of high-memory-per-core job requests at Fermilab, which depleted available pilot memory and left CPUs idle even though cores were technically free (since no new payload could be matched without available memory). Hyunwoo's "idle CPU by cause" plot was consistent with this explanation. It emerged during the discussion that Hyunwoo had already investigated and reported this same explanation to Dave Mason over the weekend, so Antonio's account of "what Dave Mason said" was, in fact, based on Hyunwoo's own earlier analysis relayed back through Dave Mason — a point the group noted with amusement before wrapping up.

## Decisions / Conclusions

- The group agreed to wait for the mismatched-type OpenSearch index data to expire naturally (about 7 more days) rather than delete the affected index, since only the oldest 7 days currently have the incorrect field type and deleting would lose that data outright with no faster fix available from the Monit team.
- The underlying script bug causing the malformed "manual gliding entry" parameter has already been fixed (on VOCMS0850); the script now enforces the expected type and logs when a conversion occurs, so data inserted going forward is expected to be consistent.
- For pilot entries with an unknown/unreported CPU count, the monitoring script will continue to skip inserting data for that pilot (as it already does), since this is considered a correct and low-impact behavior overall.
- For pilot entries where CPU data is known but memory usage/request is not reported (e.g., RAL, MIT, many US Tier-2s), the decision was made to still push the data rather than skip it — favoring CPU-metric completeness over memory-metric completeness, and accepting a partial memory dataset for now.
- The long-term (non-expiring) Monit/OpenSearch index/stream has already been created by the Monit team based on Luis's described use case and volume; the factory is technically ready to begin pushing production data to it, pending the data-correctness checks above and coordination with the Monit team to set up the query mapping.

## Action Items

- [ ] Notify the Monit team on the existing ticket that the team is okay waiting for the mismatched-type index data to expire — Luis Simas
- [ ] Adjust the monitoring script so pilot entries with missing memory (but known CPU) are still pushed rather than skipped — Luis Simas
- [ ] Double-check whether older long-term backfill data (collected by Marco over ~1.5 years) contains format inconsistencies (e.g., the "overloaded" field's earlier Boolean-vs-percentage/string representation) before pushing it into the non-expiring long-term index — Luis Simas
- [ ] Redo the backfill in the test index with the corrected logic, then push data to the production long-term Monit index (tentatively next day), coordinating with the Monit team to set up the query mapping — Luis Simas
- [ ] Investigate why some sites (e.g., RAL, MIT, several US Tier-2s) do not report memory usage/request — Luis Simas
- [ ] Continue troubleshooting the Rome Tier-2 entry, including looking for additional grid-manager logs to assist the site admin — Luis Simas
- [ ] Complete the Bristol entry move from Tier-2 to Tier-3 (change entry name and CMS site class) — Luis Simas
- [ ] Test and validate the Condor-CE grid-proxy-to-site-token authentication migration in ITB before flipping entries to site tokens in production (100+ entries) — Luis Simas
- [ ] Start using the MIG-enabled CERN Tier-2 entry for GPU testing, comparing Condor discovery tool output between MIG and full-GPU sites — Luis Simas
- [ ] Finish the factory-related CHEP poster/material draft — Marco Mascheroni

## Discussion

### OpenSearch index mapping inconsistency
Luis explained OpenSearch assigns a type to each indexed field the first time it sees it; because data had previously been inserted in a malformed way, the index's field types no longer match the now-corrected data, breaking the dashboard. Only entries in the current 30-day window are inconsistent, and only the oldest 7 days still have the old (wrong) type — this will self-resolve as those days age out. Antonio confirmed this only affects the specific pilot-overloading stream and not the broader pool of data (which continues to accumulate normally), and asked whether simply correcting future data would suffice going forward — Luis confirmed that once the source data is correct, all newly inserted data should be consistent, and the problem is confined to the already-inserted, differently-typed historical entries within the current 30-day window.

### Long-term Monit index and backfill readiness
The Monit team has created a dedicated long-term (non-expiring) index/stream after Luis described the use case and expected data volume. Data reaches both the standard 30-day and long-term streams via Monit's routing layer, without direct control from the factory side beyond sending to an AMQ topic; separate Grafana data sources can be selected to query either stream. Before backfilling historical data into this non-expiring stream, Luis wants to first validate current data correctness, since malformed data in a non-expiring index cannot rely on the same "wait for expiration" mitigation used for the 30-day stream — deleting individual documents is trivial (by ID), but he was unsure how difficult it would be to delete a broader set of malformed entries, likely requiring Monit team involvement.

### Missing CPU count and memory reporting
While reviewing the overloading dashboard with corrected data, gaps in specific site data (e.g., RAL) were traced to the script's current behavior of skipping insertion entirely when CPU count cannot be determined for a pilot — a deliberate choice (rather than inserting possibly-wrong values) that Luis had made in response to an earlier weird-value issue. It also emerged that some entries lack memory usage/request data — RAL, MIT, and reportedly many US Tier-2 sites — and were being skipped as well, which was surprising given RAL's importance as a Tier-1. Antonio noted CPU should not be skipped if only memory is missing, since CPU is the primary metric of interest for now; both Luis and Marco agreed. The underlying cause of missing memory reporting is not understood; Antonio speculated it could relate to translation between the pilot/HTCondor environment and the remote ARC-CE/batch-system stack (e.g., Slurm vs. Condor on the remote end) or to versioning differences, but this remains unconfirmed and was flagged for future investigation rather than immediate action.

### Concern about historical data-format consistency
Marco raised a concern about the planned backfill of his long-running (~1.5 year) manually-collected dataset into the new non-expiring index: over that period, the data format changed at least once (e.g., the "overloaded" field moved from a Boolean representation to a percentage/string one), and other undetected inconsistencies may exist. Because the long-term index has no expiration, any such inconsistency would persist indefinitely rather than aging out, unlike the current dashboard issue. If found, Antonio noted this would require reviewing the calculation and re-inserting corrected data. Luis agreed to check for this before the production backfill.

### Overloading/efficiency dashboard review
Antonio shared an updated version of the dashboard with the variable time-window option removed and a fixed ~12-hour window across all plots (noting 24 hours could make even more sense). With corrected data, no extreme/out-of-range values were observed, and a clear separation between overloaded-true and overloaded-false efficiency trends was visible, which Antonio considered a meaningful improvement. Remaining fluctuations were attributed either to natural variability in the mix of workflows being run, or to specific known effects — e.g., a wider gap at one site was linked to long-running pilots submitted around the time of an earlier Fermilab issue, where jobs continued running for several days after new pilot submission had stopped.

### Factory operations
- **Nanjing Normal University**: still pending SAM test fixes on the site side; not blocked on Submission Infrastructure.
- **Rome (Tier-2)**: continues to work in ITB but not in production; the issue is understood to be in the site's local batch system, and the team is waiting on the site admin, with Luis offering to look for more grid-manager logs to assist.
- **Bristol**: per an item Antonio raised via Mattermost, the entry is being moved from Tier-2 to Tier-3 classification; from the factory side this mainly requires changing the entry name and the CMS site class.
- **Condor-CE site-token migration**: an upcoming task to change the authentication method for Condor-CE entries from grid proxy to site tokens, affecting more than 100 entries; these will need to be tested and validated in ITB before being flipped to site tokens in production.
- **"Copy fail" vulnerability**: all factory machines are already patched; Luis is unsure which other (non-factory) machines can be safely rebooted and asked to be informed if action is needed there.

### GPU/MIG status
No progress since Tuesday. The RAL GPU entries remain blocked by a failing "obtainer" validation, pending the site admin. Thomas (Finland) referred the team to a contact (Andrea Bocchi) who has been experimenting with AMD GPUs, but there has been no follow-up; Antonio noted the team's interest is in resource interaction/scheduling/discovery rather than code performance, and that this AMD testing appears to use local (non-grid) machine access rather than the grid-based access the team is interested in. Luis noted the CERN Tier-2 also has a MIG-enabled entry that could be used for testing, since the RAL entry currently cannot be used. Antonio suggested comparing Condor discovery tool output between MIG and non-MIG (full GPU) sites, noting the device-name attribute already reveals when a MIG instance (rather than a full GPU) is received, and other differences may be discoverable.

### CHEP rehearsals and posters
Next week involves CHEP-related rehearsals for TikToks and posters; drafts and materials need to progress, though placeholders for pending plots/information are acceptable at this stage. Antonio expressed particular concern about the GPU-related contribution, viewing it as the least advanced and most open-ended, still in a preliminary information-gathering phase rather than based on direct experimentation by the team.

### Fermilab outage follow-up
Hyunwoo reported that power from the utility company to Fermilab is fully restored with no ongoing issues, though the company is still working to re-establish one of the affected towers (one gate remains closed for now). He shared efficiency plots showing degraded efficiency following the original power outage and the subsequent "copy fail" patch/reboot cycle, plus a separate efficiency drop (to roughly 70-80%) beginning the day before the meeting. Antonio recapped a Monday discussion with Dave Mason attributing this more recent drop to a period of high memory-per-core job requests depleting available pilot memory, leaving CPU cores idle despite being technically free (since no further payload could be matched without memory). Hyunwoo's "idle CPU by cause" plot supported this explanation. It was clarified during the discussion that Hyunwoo had already identified and reported this same explanation to Dave Mason over the preceding weekend, meaning Antonio's recap (sourced from Dave Mason) was actually a return of Hyunwoo's own earlier analysis.

## Open Questions

- Will the currently-collected pilot monitoring data (and Marco's ~1.5-year historical dataset) prove fully consistent once combined in the non-expiring long-term index, or will latent format changes (e.g., the earlier Boolean-vs-percentage "overloaded" field) require correction?
- What is the root cause of missing memory-usage/request reporting at sites such as RAL, MIT, and several US Tier-2 sites — is it related to translation between the pilot/condor environment and the remote ARC-CE/batch-system stack, or to pilot/software versioning?
- Will the AMD GPU experimentation that Andrea Bocchi has reportedly been doing (via local, non-grid access) provide anything relevant to the team's grid-based resource-discovery/scheduling interests, pending follow-up?
- What differences, if any, will appear in the Condor discovery tool's output between the MIG-enabled CERN Tier-2 entry and non-MIG GPU sites?

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[Pilot Jobs]] · [[GPU]] · [[Heterogeneous Computing]] · [[Monitoring]] · [[OpenSearch]] · [[Monit]] · [[Factory Operations]] · [[Factory Configuration]] · [[CMS]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-07 17.35.53 Submission Infrastructure Weekly Meeting`)
