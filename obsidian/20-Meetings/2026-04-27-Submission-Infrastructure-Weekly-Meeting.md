---
type: meeting
date: 2026-04-27
participants:
  - Marco Mascheroni
  - Luis Simas
topics:
  - Condor CE authentication migration to site tokens
  - Pilot efficiency monitoring (OpenSearch) — CPU count fallbacks, timestamp field
  - Factory-operations ticket status (Rome/New Rome entry, Tier-3 China site, Tier-1 GPU entries)
  - GPU partitioning (NVIDIA MIG) at a new Tier-1 site
  - HTCondor / GlideinWMS versions on the factories
---

# Submission Infrastructure Weekly Meeting

## Summary

This was primarily a working session between Marco and Luis (Antonio and others were not present). After a brief check-in on workload and priorities, most of the meeting covered three technical threads: (1) migrating Condor compute-element (CE) entries to site-token authentication, following a request from Jeff at last week's factory-operations meeting — Luis had found more entries than expected still advertising non-site-token authentication methods, and he and Marco discussed why (front-end/factory/CE authentication-method negotiation) and agreed on a test-in-ITB-first approach; (2) Luis's pilot efficiency monitoring work (feeding OpenSearch for CHEP-related plots — referred to in parts of the transcript as "chat," apparently a mis-transcription of "CHEP"), including a long discussion with Marco about how to reliably determine per-pilot CPU count (including whole-node entries) and an open question about correctly timestamping pilot records; and (3) a review of open factory-operations tickets, including a new Tier-1 site with GPU (NVIDIA MIG) entries that will likely become an early test case for GPU partitioning. The meeting closed with a quick check of HTCondor/GlideinWMS versions running in ITB and production.

## Decisions / Conclusions

- Marco explained that Condor CE authentication is negotiated between the factory and the compute element: the front end sends both grid-proxy and site-token credentials to the factory, and the CE picks whichever method(s) it advertises support for. Marco's working theory for why many CMS entries still show non-site-token methods is that authentication may already effectively be happening via site token even though the front-end/factory configuration hasn't been updated — this needs to be verified rather than assumed.
- Agreed approach for the site-token migration: first identify all Condor entries whose auth method is not site token, change them in ITB, and verify authentication (e.g. via `condor_ping` and by forcing `SEC_CLIENT_AUTHENTICATION_METHODS` to site token) before touching production. Testing should be done submitting through the front end (not just the factory) since front-end/factory communication is also part of the change.
- Marco recommended running the test-submission script *before* making the site-token changes, so any already-broken entries are identified independently of the migration (avoiding confusion between pre-existing breakage and breakage caused by the change).
- Decision on pilot efficiency monitoring data model: only raw values (durations, CPU-seconds) are pushed to OpenSearch — efficiency itself is not pre-computed at collection time. This follows Antonio's earlier guidance that per-site efficiency must be computed from summed raw values, not by averaging per-pilot efficiencies ("averages of averages").
- Observed efficiency values slightly above 1 (e.g. 1.05–1.12) in Luis's early (pre-change) version of the script were judged expected/fine by Marco: this can happen due to overloading, where extra pilots beyond the nominally required count get scheduled and pick up otherwise-idle CPU cycles (e.g. from other VOs' pilots), especially at CMS-only sites. Marco said this would only be a concern if values were much larger (e.g. 4x).
- For CPU count per pilot: the `RequestCpus`/`CPUs` classad from the job-terminated event is usable when present, and this is the same source Marco's older script used from the collector-side query (not from log parsing). ARC entries currently have no CPU classad at all in the job-terminated event; some Condor CE entries are also missing it, and these appear (not fully confirmed) to be whole-node entries.
- Decision: do not default `RequestCpus` to 1 as a stand-in for "whole node," since some real single-core-pilot entries exist (e.g. Syracuse, and the Mexican Tier-1) — defaulting to 1 would misclassify them and produce wrong CPU counts.
- Decision: whole-node status per entry should instead be determined by querying the factory collector for the glidein CPU classad (referred to in the transcript as "gliding CPUs," exact classad name not confirmed) rather than inferring it from job-log data, and by falling back to the CE's `DetectedCpus` (total node cores, from the CE-side collector) when the entry is confirmed whole-node.
- Decision: this factory-collector lookup should be done once per script run (not per event), cached to a file, and reused; if the query fails on a given run, the script should keep using the previously cached values and continue collecting data for all other entries rather than skipping collection — judged an acceptable degradation since the query is not expected to fail often, and a single missed refresh (e.g. right after a new whole-node entry is added) self-corrects on the next successful run.
- Decision: no additional fallback (e.g. parsing glidein stdout/stderr, as `efficiency.py` previously attempted) will be built for cases where CPU count is otherwise unavailable. Marco was firmly against this approach, citing past experience that pulling from multiple unsynchronized sources becomes unreliable ("a spider... taking information from different places, and then they are not synchronized, and it's a mess").
- Checked example CE versions live: Fermilab (ARC) reports HTCondor 25.0.7; Caltech reports 10.0.9, a notably old (~2022) version. Marco concluded outdated CE software is the likely reason some entries lack the needed classad(s), and does not plan to build fallbacks for this — if data is missing due to an old CE, the plan is to open a ticket asking the site to update, escalating if needed.
- Whether to also store a pre-computed "efficiency" field in OpenSearch (in addition to raw values), purely for convenience in ad hoc Grafana/OpenSearch Discover queries, was discussed but not decided — Marco is inclined to include it despite Antonio's stated preference against, but explicitly left the decision to Luis.
- Reaffirmed from an earlier "CHEP touchpoint" meeting (with Antonio): the pilot efficiency monitoring effort is not a hard dependency for producing the CHEP plots, since it was agreed the plots can be produced without it. Marco confirmed this work currently has no hard deadline.
- On the Tier-1 GPU/MIG entries: Marco's working hypothesis is that the site's batch system enforces at most one GPU pilot per node (via `RequestGPUs=1` sent to the CE), with other pilots on the same node being regular non-GPU pilots. This needs confirmation with the site admin — specifically whether the site's notion of "one GPU" means one physical device or one MIG partition, since the latter could allow multiple GPU pilots to land on the same node while each pilot's `CUDA_VISIBLE_DEVICES` is set to "all," which would be a problem.
- The version-number suffix seen after some HTCondor/GlideinWMS RPM versions (e.g. a trailing dash-number) was clarified by Marco as an RPM build/spec-file metadata increment (e.g. from a dependency change), not a functional/code difference — safe to ignore.

## Action Items

- [ ] Identify all Condor CE entries with an authentication method other than site token, build a script to test them, validate in ITB, then update production entries — Luis Simas
- [ ] Write a script (evolving the current manual JDL test) to submit test pilots per entry/site via environment-variable + `condor_submit` substitution, and log results to a file for tracking, running it before the site-token changes to catch pre-existing broken entries — Luis Simas
- [ ] Test forcing `SEC_CLIENT_AUTHENTICATION_METHODS` to site token (e.g. via `condor_ping`) in ITB as part of validating the migration — Luis Simas
- [ ] Restore/extend the CPU-count query in the pilot efficiency monitoring script: query the factory collector once per run for whole-node status (and CE `DetectedCpus` where applicable), cache results to a file, and fall back to the cached value if the query fails — Luis Simas
- [ ] Investigate indexing/querying pilot records in OpenSearch/Grafana by the pilot termination time rather than the OpenSearch ingestion time — Luis Simas
- [ ] Check with the site admin of the new Tier-1 GPU (MIG) site what "one GPU" means from the batch system's perspective (physical device vs. MIG partition) — mentioned as a near-future step, no owner explicitly stated
- [ ] Mention to Antonio the need to possibly reschedule tomorrow's 15:00 CHEP working meeting, since Marco cannot attend — Marco Mascheroni

## Discussion

### Workload and priorities
Luis raised wanting clear deadlines across his parallel work streams so he doesn't unintentionally drop something with no stated deadline. Marco acknowledged this is a general difficulty for him too — undated work tends not to get done. Marco confirmed the pilot efficiency monitoring work currently has no hard deadline (a "nice to have," not least because of open risks around whether the desired OpenSearch queries/timestamps will work as hoped), so Luis will continue working on it alongside his other tasks as before.

### Condor CE site-token migration
Following a request from Jeff at the previous week's factory-operations meeting, Luis is working out which Condor CE entries need to move to site-token authentication. Using `yq` to query the factory's entry configuration files, he found a CMS/enabled/production entry count with authentication methods other than site token that was larger than he expected, and wanted Marco's read on whether that count was reasonable.

Marco explained that for Condor CEs (as opposed to ARC), authentication is negotiated: the grid-manager process and the CE exchange their available authentication methods, and the intersection is used. The front end sends both grid-proxy and site-token credentials to the factory; if a CE advertises only site token, that's what gets used regardless of what the factory/front-end XML nominally lists. Marco's hypothesis is therefore that most of these entries are probably already authenticating via site token in practice, and the large count mostly reflects that the front-end/factory configuration itself has lagged behind — but this needs to be verified in ITB rather than assumed.

Agreed plan: identify entries needing a config change, change them in ITB, and verify. Verification should include forcing `SEC_CLIENT_AUTHENTICATION_METHODS` to site token (e.g. via `condor_ping`) and submitting real test pilots through the front end (since front-end/factory communication is also part of what changes), catching any front-end/factory communication issues that a bare `condor_ping` might miss. Marco suggested running the pilot-submission tests *before* applying the site-token changes, so any entries that are already broken are identified independently of the migration, rather than after the change when it would be unclear whether a failure is caused by the site-token change or a pre-existing issue.

Luis is using a JDL test file (originally shown to him by a colleague, Vive) for manually triggering test pilots per site, and plans to turn this into a script using environment-variable substitution in `condor_submit`, with results logged to a file to track entries over time. Luis reported he had summarized this plan today in an email to Marco, Jeff, and a third recipient referred to in the transcript as "Yonhu" (name transcription unclear).

### Pilot efficiency monitoring (OpenSearch)
Luis walked through the current state of the pilot efficiency monitoring script, part of the "submission infrastructure monitoring" GitLab repository, running on the (single) production monitoring machine and currently sending data to a test OpenSearch index. For each pilot it collects: the pilot job ID, CPU count, summed user+system CPU time (total CPU time used), and total pilot duration (termination time minus execution/start time); from duration and CPU count it derives the total available CPU-seconds. Per earlier guidance from Antonio (to avoid "averages of averages"), only these raw values are pushed — efficiency itself will be computed at query time in OpenSearch, not pre-aggregated at collection time.

Luis's earlier (pre-change) version of the script did compute efficiency directly and surfaced some values slightly above 1 (e.g. 1.05, 1.10, 1.12). Marco explained this is expected and not concerning: it can happen due to overloading, where extra pilots beyond the nominally required number are scheduled and end up picking up otherwise-idle CPU cycles (e.g. left over from other VOs, or other CMS pilots not fully using their allocation), especially at CMS-only sites. He said this would only be a red flag if values were much higher (e.g. around 4x).

Marco raised that having a precomputed "efficiency" field, even if unused for the main plots, would make ad hoc filtering easier (e.g. finding all pilots at or below 50% efficiency directly in OpenSearch Discover, similar to what he can already do today in Grafana without recomputation). Luis noted this would require recalculating at query time and that he discussed with Carlos last week that it should be possible to do a proper aggregation via an OpenSearch query, but hasn't verified it yet. Marco proposed that, worst case, a separate long-term index doing daily per-site aggregation on the monitoring machine could be built later. Whether to add a precomputed efficiency field was left to Luis to decide, with Marco explicitly not wanting to push him against Antonio's stated preference.

Luis flagged an open issue with timestamps: pilots can terminate significantly before the corresponding record is pushed to OpenSearch (including cases of backfilling from historical data), so ideally records should be indexed by their actual termination time, not by the time they were submitted to OpenSearch. He plans to check whether this field can be used directly for the OpenSearch timestamp/index time and in Grafana queries. Marco noted Carlos is doing something similar for user-job Condor history data pulled from the CMS schedulers (not the submission-infrastructure/factory-operations schedulers), indexing by event fields rather than query time, and believes this is achievable.

### CPU count sourcing and whole-node entries
The main topic Luis wanted Marco's help with was determining CPU count per pilot, especially for whole-node entries. Marco's earlier (older) script sourced CPU count from a collector-side query (not from parsing logs), and explicitly skipped whole-node entries because they lack this information; this was recently improved so that the number of cores is now available in some pilots' activity logs (though not all).

Luis found the `CPUs` classad (used by the older approach) is not present at all in job-terminated events for ARC entries, and is missing for some Condor entries too — the latter appearing (not confirmed exhaustively) to correlate with whole-node configuration. As a fallback for non-whole-node entries, the job-terminated event's `RequestCpus` classad (and `RemoteUserCpu`/related usage fields) is available and usable.

For whole-node entries, `RequestCpus` is often present but incorrectly set to 1 (a known quirk), so it cannot be used as a general fallback — doing so risked misclassifying genuinely single-core-pilot sites (Marco noted, while checking live, that Syracuse and the Mexican Tier-1 run single-core pilots) as whole-node, or vice versa. Marco suggested `DetectedCpus`, a classad available from the CE-side or factory collector giving the node's total core count, as usable once an entry is confirmed to be whole-node. To determine whole-node status itself, Luis found a "gliding CPUs" classad (exact name/spec unconfirmed) visible via the factory collector that reliably indicates which entries run whole-node pilots.

Agreed approach: query the factory collector once per script run (not per event) for whole-node status per entry, and use `DetectedCpus` as the CPU-count source for confirmed whole-node entries; cache this mapping to a file. If the once-per-run query fails (e.g. because the collector is busy, such as during reconfiguration), the script should reuse the previously cached values rather than skip data collection for all entries — data for a newly added/changed entry might be missed for one cycle, but this self-corrects on the next successful run, which was judged an acceptable risk.

Marco was firm that no further fallback chain should be built for cases still missing CPU data (e.g. parsing glidein stdout/stderr, an approach previously attempted in `efficiency.py`), calling this an unreliable pattern of pulling unsynchronized data from multiple sources. Investigating live, the group found that CEs with very old HTCondor versions (Caltech: 10.0.9, vs. Fermilab: 25.0.7) likely lack the classad(s) this depends on; Marco's conclusion was to treat this as the site's responsibility (open a ticket asking them to update their CE) rather than building more fallbacks.

### Factory-operations tickets
- A CE referred to as "Rome"/"New Rome" (site name unclear from the transcript) is still failing to submit to the site's batch system; Luis pinged the site admin again and the team is still waiting on a response.
- A Tier-3 site in China: the GlideinWMS-side setup is complete and Luis was preparing to push the entry to production, but he noticed no evidence of SAM tests being configured for it. After checking with a colleague referred to as "Noi" (responsible for facilities and site support), it turned out the site's local site configuration is not properly set up at all. Luis still needs to adjust the GlideinWMS entry naming (described as straightforward) but the site itself is not yet ready on the facilities/site-config side.
- A Tier-1 site referred to as "Raw" (likely RAL; transcription unclear) has 5 new GPU entries, tied to a ticket originally opened at the end of last year about a nested-container/Singularity issue on Docker-based worker nodes. A workaround (disabling PID namespaces in Singularity via a GlideinWMS option) had previously been set up by a colleague (Vive); the current blocker is that a validation step is failing to find "apptainer"/Singularity in the environment, with no action item yet on Marco/Luis's side. Once resolved, the team plans to use these entries to test GPU partitioning.

### GPU partitioning (NVIDIA MIG) at the new Tier-1 site
The new Tier-1 GPU entries use NVIDIA GPUs partitioned via MIG at the site (not whole-node; worker nodes have 16 cores). MIG partitioning is configured by the site admin, and a pilot landing on such a node sees multiple GPU devices already split by the site. As observed in the logs so far, each pilot currently gets `CUDA_VISIBLE_DEVICES` set to "all," i.e. visibility into every GPU slot on the node. Luis raised a concern (not yet observed, but considered plausible) that if two pilots landed on the same node simultaneously, both could see all GPUs, which would be problematic.

Marco's hypothesis is that the site requests one GPU per pilot to its batch system, and the batch system itself guarantees that at most one GPU pilot runs per node at a time (other pilots on that node being regular, non-GPU pilots) — but this depends on what the site's batch system means by "one GPU": one physical device, or one MIG partition. If it means one MIG partition, multiple GPU pilots could still land on the same node, which would conflict with the "sees all GPUs" behavior. This needs to be confirmed with the site admin.

Marco suggested this ticket is a good opportunity for Luis to build experience with GPU partitioning; Luis agreed MIG is likely the easiest case to start with, and asked to be given Marco's existing GPU test-job submission script when he needs it (not immediately) rather than now.

### Team/logistics notes
- Marco will be unable to attend tomorrow's 15:00 CHEP working meeting due to a personal commitment, and will raise with Antonio whether it should be moved (with only Luis and Antonio otherwise attending).
- Florian's last day working with the team was the previous Friday; he is moving back to Germany, and is expected to be at CHEP, where Antonio will be able to give him a proper farewell.

### HTCondor / GlideinWMS versions
Checked live: production factories run HTCondor 24.0.14 and GlideinWMS 3.11.3; ITB runs HTCondor 25.0.7 and GlideinWMS 3.11.3 (same GlideinWMS version, newer HTCondor). Marco noted production should move to HTCondor 25 "sooner rather than later." The dash-suffixed build numbers sometimes seen after these versions were clarified as RPM-level metadata increments (e.g. from a spec-file dependency bump) rather than functional changes, and can be ignored. Separately, Marco mentioned needing to revive an ITB-dev instance for upcoming testing, and no longer thinks Luis needs his own ITB-dev instance (previously suggested) given his current familiarity with the system, though he may ask for help with specific tests; Luis said he'd be open to it as a learning experience.

## Open Questions

- Is the large number of CMS Condor entries still configured with a non-site-token auth method actually causing any authentication problem, or is authentication already effectively happening via site token in practice (front end sending both credentials, CE picking site token)?
- Can OpenSearch aggregation queries correctly compute site-level pilot efficiency (sum of usage over sum of available time) without falling into "averages of averages," and can this be done from Grafana directly, or will a separate pre-aggregated (e.g. daily per-site) index be needed?
- Should a precomputed "efficiency" field be stored in OpenSearch for convenience, given Antonio's preference against pre-aggregating it? Left to Luis to decide.
- Can pilot records be timestamped/indexed by their actual termination time rather than OpenSearch ingestion time, in both storage and Grafana queries?
- Exactly what classad reliably indicates "whole node" status per entry via the factory collector (referred to in the transcript as "gliding CPUs"), and is `DetectedCpus` consistently available as a fallback?
- For sites with outdated CE software lacking needed classads (e.g. Caltech's ARC CE), will opening a ticket be sufficient to get them updated, or will escalation be needed?
- For the new Tier-1 MIG-based GPU entries: does the site's batch system treat "one GPU" as one physical device or one MIG partition, and could multiple GPU pilots land on the same node while each sees all GPU slots?

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[Pilot Jobs]] · [[GPU]] · [[Heterogeneous Computing]] · [[Monitoring]] · [[Factory Operations]] · [[Factory Configuration]] · [[CMS]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-27 14.14.15 Submission Infrastructure Weekly Meeting`)
