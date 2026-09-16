---
type: meeting
date: 2026-04-16
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Luis Simas
  - Florian Von Cube
topics:
  - HTCondor collector duty-cycle monitoring (CERN vs Fermilab)
  - IO/static slot utilization
  - overflow via pilots vs. job routing
  - glide-in overload-enabled parameter fix (factory entries)
  - GPU partitioning (`-divide` flag / GPU Discovery Tool, MIG)
  - factory operations status
  - dynamic resources / BSC (no update)
---

# Submission Infrastructure Weekly Meeting

## Summary

This was a CMS-week week, so there was no general computing meeting, and the Monday meetings had been virtual with nothing pending to report. Antonio gave a short infrastructure status update: the pools (roughly 500,000 slots total) are healthy, the proportion of slots taken by 4-core jobs has increased (reducing single-core slot counts and overall slot totals, continuing a discussion from the previous week with Luis), and the collector duty cycle has gone back down, though a systematic gap between the main (CERN) and backup (Fermilab) collectors remains unexplained. The bulk of the meeting was a discussion, following an earlier conversation with Stefano, about whether "overflow via pilots" (dedicated front-end overflow groups) is still needed now that overflow via job routing exists; monitoring showed poor utilization for the remaining US overflow group, and Antonio proposed asking Stefano to agree to disabling it, contingent on confirming CRAB's site configuration doesn't depend on it. Luis gave a brief factory-operations update: two entries are still under test with site admins, and a fix for inconsistent `glide-in overload-enabled` settings across CMS entries has been made but not yet deployed; the related monitoring bug is still not resolved. Antonio had no BSC update this week due to focus on CHEP contributions. The meeting closed with a technical discussion between Marco and Florian on next steps for GPU partitioning: using the GPU Discovery Tool's `-divide` flag to make HTCondor advertise one physical GPU as multiple slots (memory-constrained, not truly hardware-partitioned), the GlideinWMS-side changes likely needed to pass this through, monitoring implications, and plans to test at KIT and compare against a site referred to in the transcript as "peak"/"pick" (unclear, possibly PIC).

## Decisions / Conclusions

- Overflow (jobs waiting too long at a Tier-1 spilling over to run at neighboring Tier-1s or other sites) remains a needed feature, particularly for analysis jobs pending in Tier-1 queues, since Tier-1s hold much of the data these jobs require.
- Overflow via dedicated pilot groups is no longer enabled for the UK and Italy Tier-1 regions (confirmed by Florian). Only the US overflow group in the front end remains active.
- Monitoring of the US overflow group's slot utilization showed it frequently drops below 50%, at times appearing to approach the plot's minimum, indicating this mechanism is inefficient.
- Antonio and Marco agreed overflow via job routing (the schedd routing table enlarging/correcting the user's overly restrictive "desired sites" expression) is the cleaner mechanism, since non-universal ("overflow") pilots are inherently less efficient to schedule and a dedicated overflow group adds complexity to the front-end configuration (another group negotiating for pilots).
- IO/static slot usage has been increasing recently — e.g., at Fermilab IO slots account for roughly half of total available slots — but this was judged not currently a problem, since the jobs using them are numerous but short; Antonio noted such jobs could become disruptive if they fragment many pilots simultaneously, but no action was taken.
- The collector duty cycle is currently under control (it rose during a recent period of more single-core-job slot updates, but has since gone back down); a systematic gap between the CERN (main) and Fermilab (backup) collector duty cycles persists, which Antonio flagged as worth re-examining but did not resolve during the meeting.
- Regarding GPU partitioning: Florian clarified that the `-divide` flag on the HTCondor GPU Discovery Tool does not perform true hardware partitioning — it advertises the same physical GPU device multiple times and prevents oversubscription of the GPU memory that jobs have requested, but does not enforce that jobs stay within their requested memory (jobs exceeding their request could still interfere with each other). Antonio characterized this as effectively turning the GPU into a partitionable slot with GPU memory as the constrained/controlled resource, analogous to CPU overloading.
- The team agreed the existing "GPU pool size per resource provider" monitoring panel (based on total slot GPU counts) will become misleading once the `-divide` flag is used, since it will count the same physical GPU multiple times; total GPU memory (and memory fragmentation across processes) was proposed as the more meaningful metric to track going forward, though this has not yet been implemented.
- Factory-entry overloading-parameter inconsistencies were identified and fixed by Luis (with Marco): several entries had overloading disabled but did not explicitly set the `glide-in overload-enabled` parameter to false (suspected to be interfering with monitoring), and some GPU entries were incorrectly configured with overloading enabled. The fix has been committed but still needs to be deployed.
- The overload-enabled monitoring bug (from the previous week's discussion) is still not resolved: the aggregation query still mixes two different attribute types across separate indices. Antonio and Luis expect this to resolve once all pilots in the pool have refreshed with the corrected configuration, which will take on the order of several days given the pool's long-lived pilots; Luis also noted the query's time-range handling likely contributes to inconsistent results in the meantime.

## Action Items

- [ ] Propose to Stefano disabling the US overflow (pilot) group in the front end, given overflow-via-routing appears sufficient and overflow-via-pilots shows poor utilization — Antonio Perez-Calero Yzquierdo
- [ ] Check whether CRAB's site configuration / job-routing expressions properly cover the US case before removing the US overflow group (CRAB's current configuration doesn't list US sites explicitly and appears to rely on this overflow mechanism) — Marco Mascheroni
- [ ] Deploy the committed overloading-parameter fixes to factory entries — Luis Simas
- [ ] Look into enabling the GPU `-divide` attribute in the factory configuration / GlideinWMS, "sooner rather than later" — Marco Mascheroni
- [ ] Investigate where the GPU Discovery `-extra` parameter (referenced around line 925 of the glidein startup script) is consumed, to determine what GlideinWMS-side change is needed to pass the divide argument through — Marco Mascheroni
- [ ] Test GPU partitioning behavior against KIT's MIG-based GPU setup, and also test/compare at the site referred to in the transcript as "peak"/"pick" (unclear which site this refers to) — Antonio Perez-Calero Yzquierdo

## Discussion

### News / CMS week
CMS week was taking place, so there was no general computing meeting; the Monday meetings had also been virtual, with nothing pending from them. Tier-0 jobs are still running; Antonio described the LHC as being in a kind of impasse with some parameter adjustments, but nothing new to report from checking during the week.

### Infrastructure status: pool size and collector duty cycle
Antonio reported the pools (SanD++ plus global, as referenced) hold nearly 500,000 slots, and that the number of slots has gone back down, continuing last week's discussion with Luis: the proportion of slots taken as 4-core slots has increased, which reduces the total number of single-core slots and, in practice, the total slot count overall (the relevant plot includes static, dynamic, and partitionable slots, as discussed the previous week). As slot counts went down, the rate of updates reaching the collector, and the collector's duty cycle, also went down.

Antonio described the collector duty cycle as the percentage of time the collector spends processing incoming slot updates and replying to queries (e.g., from negotiators); 100% represents saturation, at which point the collector becomes non-responsive — effectively a measure of stress on the collector. He noted a systematic, persistent gap between the duty cycle of the main (CERN) collector and the backup (Fermilab) collector, both of which receive slot updates. He attributed part of the difference to negotiator queries (an "ad server"-style query from negotiators to the CERN collector) and recalled that non-essential/monitoring queries are meant to be diverted to the Fermilab collector specifically to reduce load on the main one. He said he was surprised to see a consistent gap remain, having expected the diversion of non-essential queries to Fermilab to roughly compensate for the extra negotiator load on CERN, and noted this is a metric the team used to monitor closely during a past scalability test focused on collector scalability. He characterized the current gap as nothing to worry about (load levels are low) but worth re-examining.

Antonio also reviewed IO-slot utilization: most of the time IO slots appear to be in excess, but recently this has been increasing — e.g., at Fermilab, IO slots account for roughly half of the total available slots. In response to Marco's question about Caltech, Antonio confirmed Caltech has an unfavorable ratio of IO/merge cores to total cores, which Marco had noted as a site worth continuing to check, along with Vanderbilt (also noted as having a high proportion of IO slots) and Fermilab. Antonio judged this is not currently a problem: the jobs involved are numerous but generally short, though he noted such jobs could become disruptive if they end up fragmenting many pilots simultaneously. Antonio said the general monitoring plots for scheduling efficiency show the same effect (from the collector/slot-count changes described above) but otherwise look fine.

### Overflow via pilots vs. overflow via job routing
Antonio described an interesting discussion with Stefano about "stateless attraction" / overflow via pilots. Overflow itself — allowing jobs waiting too long at a Tier-1 to run at neighboring Tier-1s or other sites — is needed, particularly for analysis jobs pending in Tier-1 queues, since Tier-1s hold much of the data such jobs require. What is less clear is whether overflow via dedicated pilot groups is still needed. Historically there was overflow for several Tier-1 countries/regions into Tier-2s; Florian confirmed this is no longer enabled for UK and Italy. There remains an active "overflow" group in the front end for the US. Florian and Marco clarified this group had been disabled and was re-enabled roughly 2–3 weeks prior (a separate, specific case discussed at that time); the "normal" (routing-based) overflow mechanism, by contrast, has always been enabled.

Antonio explained that overflow via job routing works by correcting an overly restrictive "desired sites" expression a user submitted — e.g., if a user requested to run only at Fermilab or only at PIC and isn't getting matched, the routing table adds other nearby sites (other US sites, or Madrid/Santander in the PIC case) to the desired-sites attribute. He views this as cleaner than overflow via pilots, since it corrects the same overly restrictive user decision without requiring "non-universal" pilots, which represent a potential source of inefficiency (Marco added that such pilots can fill up without enough matching jobs, leaving them poorly utilized).

Reviewing monitoring, Antonio and Marco looked at slot utilization for the US "overflow" group in the global pool and found it frequently below 50%, at times appearing to approach the plot's displayed minimum (the plot is cut off near its floor, so the true minimum utilization is unclear). Antonio proposed using this as supporting evidence to show Stefano that the US overflow-via-pilots group should be removed in favor of relying on overflow via routing, citing both the inefficiency of the pilots and the reduced front-end configuration complexity (one fewer group negotiating for pilots). Marco agreed he is in favor of removing it, subject to Stefano's agreement, but flagged that CRAB's current site configuration does not explicitly list US sites and appears to rely on this overflow mechanism for the US case — this needs to be checked before removal. Marco separately looked up a related GitHub issue number that Stefano had referenced (confirmed as issue #95).

### Factory operations (Luis)
Two entries remain under test with site admins, carried over from the previous week, with little to update — discussions with the site admins are ongoing. Following a discussion from an earlier "chat checkpoint" meeting about overloading parameters, the overloading parameters were updated for all CMS entries. Several entries had overloading disabled but did not explicitly set the `glide-in overload-enabled` parameter to false, which was suspected of interfering with monitoring; some GPU entries were also found to be incorrectly configured with overloading enabled. These issues were fixed after discussion with Marco, but the fix still needs to be deployed.

The related monitoring is still not working: Antonio noted the aggregation query mixes two different attribute types across separate indices, and checking the last 24 hours still showed nothing working. Luis suggested the query's time-range handling also contributes, since data will remain inconsistent until all pilots refresh. Antonio agreed the pool has long-lived pilots, so achieving full consistency will take on the order of several days; the team will check again once that has happened.

### Dynamic resources / HPCs
Antonio had nothing new to report this week — no testing done on BSC, as his time was spent on CHEP contribution work instead.

### Monitoring note
Antonio noted the overloading tag has been fixed at the source (factory entries) and this is hoped to eventually resolve the corresponding display issue in Monit, though it is not visible yet.

### GPU partitioning follow-up (Marco and Florian)
Marco asked Florian to recap a discussion from the previous morning about GPU partitioning and next steps. Florian summarized the conclusion: as an immediate, simple first step, pass a "divide" attribute in the factory configuration through to the HTCondor GPU Discovery Tool, so HTCondor advertises a single physical GPU device as multiple ("quote-unquote") instances — not true hardware instances, but multiple advertised GPUs — while relying on user jobs not interfering with each other. This was described as the cleaner of two very simple approaches currently available. After experimenting with this, the plan is to talk to KIT about how to interact with their GPU nodes, where MIG (multi-instance GPU) partitioning is activated at the site.

Marco raised where the `-divide` attribute should be enabled; Florian thought it belongs in the factory configuration, but Marco noted GlideinWMS is what actually runs the GPU discovery and passes parameters to the GPU Discovery Tool, so a GlideinWMS-side change may be needed. Florian agreed this shouldn't be a large change (passing one additional argument). Marco took this as likely his action item.

Florian clarified the mechanics: the GPU Discovery Tool's `-divide` option does not truly partition the GPU. HTCondor advertises the same GPU device multiple times and prevents oversubscription of the GPU memory that jobs request, but it does not enforce that a job stays within its requested memory — a misbehaving job using more memory than requested could still interfere with or crash other jobs sharing the device. Antonio related this to the earlier team discussion of MPS: logically, the GPU becomes a partitionable slot where GPU memory is the resource being partitioned and controlled, similar in spirit (though not in implementation) to condor overloading.

Antonio raised a further question: what happens if a `-divide`d pilot lands on a GPU that has already been hardware-partitioned by the site itself — could the pilot incorrectly assume access to the full device rather than its assigned partition? Florian said this depends entirely on how the site implements its partitioning; if a site properly partitions via MIG, the pilot should be confined to its granted memory envelope, and anything done within that envelope (e.g., self-inflicted oversubscription) is on CMS's own pilot, the same way a CPU pilot is confined within a worker node. Florian argued this scenario is not worth focusing on yet, since no site currently hands CMS pre-subdivided GPU devices; Antonio agreed this needs to be understood eventually but accepted starting with the simpler case first, framing the initial phase as exploratory — gather information on what happens, then move into a phase of gathering performance metrics, which will likely require extending monitoring/dashboards to track new variables as they are found.

Florian noted a concrete monitoring implication: the current "GPU pool size per resource provider" panel, based on total slot GPU counts, will be thrown off by the `-divide` approach, since the same physical GPU would be counted multiple times. Antonio agreed and proposed instead tracking total GPU memory, which should stay constant while being subdivided/used across multiple processes, potentially allowing the team to look at GPU memory fragmentation as a way to observe what's happening.

On concrete next steps, Marco said he would look into enabling the `-divide` flag "sooner rather than later." Luis asked whether this is set in the glidein startup script; Marco confirmed it is in the condor_startup script that writes the condor_config file used by the condor `startd` (Antonio noted this is the same mechanism he has been using to manipulate startd attributes for his BSC dynamic-resource testing). Marco found a related "GPU Discovery extra" parameter around line 925 of the script but was not yet sure where it is consumed, and said he would look into it. Antonio noted a peak in GPU pool size visible in Grafana was from a manual test Marco had run the previous day with Florian and Luis, unrelated to a real production change.

On where to test, Antonio suggested testing both where the team knows it should work and at other sites to confirm the capability holds more broadly, mentioning KIT specifically for the MIG-interaction test, and also a site referred to in the transcript as "peak"/"pick" (transcription unclear) where CMS reportedly has GPU access at the grid level. Florian agreed using two different sites for comparison is a good idea.

## Open Questions

- Why does a systematic duty-cycle gap persist between the CERN (main) and Fermilab (backup) collectors, and are non-essential/monitoring queries still being consistently diverted to Fermilab as originally intended?
- Do we still need overflow via pilots for the US at all, given overflow via job routing appears to cover the same need? (Contingent on Stefano's agreement and on confirming CRAB's configuration doesn't depend on the pilot-based mechanism.)
- Will the overload-enabled monitoring/aggregation issue resolve automatically once all pilots refresh with the corrected configuration, or does the query's time-range handling also need to be addressed?
- What happens when a `-divide`d GPU pilot lands on a GPU that has already been hardware-partitioned by the site (e.g., via MIG) — could it incorrectly assume access to the full device?
- Where exactly should the `-divide` attribute be configured (factory vs. GlideinWMS), and what GlideinWMS-side change, if any, is required to pass it through to the GPU Discovery Tool?
- What monitoring/dashboard changes will be needed to properly track GPU sharing once the `-divide` approach is tested (e.g., total memory and fragmentation instead of raw GPU counts)?

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[Pilot Jobs]] · [[GPU]] · [[Heterogeneous Computing]] · [[Monitoring]] · [[Factory Operations]] · [[CMS]] · [[CRAB]] · [[Dynamic Resource Provisioning]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-16 17.05.49 Submission Infrastructure Weekly Meeting`)
