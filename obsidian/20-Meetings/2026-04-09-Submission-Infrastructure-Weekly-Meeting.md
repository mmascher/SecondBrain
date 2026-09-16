---
type: meeting
date: 2026-04-09
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Florian Von Cube
  - Luis Simas
  - Stephan Lammel
topics:
  - CPU efficiency discussion (CMS computing meeting)
  - user resource request (Jira ticket, KaFq/LXBatch)
  - front-end total-slot limit increase
  - HTCondor collector duty-cycle / single-core job storms
  - GlideinWMS pilot-validation monitoring bug
  - Lumi HPC entry moved to production
  - Chinese Tier-3 site onboarding
  - BSC dynamic resources
  - glide-in overload-enabled type/monitoring fix
  - CHEP 2026 speaker nominations
---

# Submission Infrastructure Weekly Meeting

## Summary

Antonio opened with news from the general CMS computing meeting: CPU efficiency remains a "hot topic" at CMS, with Antonio and Marco agreeing that CMS's official explanation (increased analysis-job share) is only half the story, since organized production workloads are also inefficient; Marco was skeptical that "organizing" more analysis would help without some automatic enforcement (e.g. killing low-efficiency jobs), and Antonio linked this to a related storage-allocation/data-placement problem (data sitting at Tier-1s but jobs running at Tier-2s, forcing remote reads and lowering efficiency). A user request for extra computing resources (Jira ticket) was discussed; the request's scope was unclear, and Stephan suggested the user likely belongs on the CERN "KaFq"/LXBatch batch queue rather than the CMS pool, since the activity sounds related to calibration work with an existing privileged queue. The bulk of the meeting was a detailed walkthrough (led by Antonio and Marco) of why the front-end's total-slot limit (200,000, throttling at 220,000) was being hit — driven by "single-core job storms" fragmenting the pool — and a decision to raise that limit substantially. Luis gave a short factory-operations update (two new entries in troubleshooting/testing, a GlideinWMS monitoring bug fix merged upstream, the Lumi HPC entry now in production, and continued onboarding of a Chinese Tier-3 site). Florian reported on an investigation into the "glide-in overload-enabled" monitoring/type-casting bug, concluding a proper fix requires changing the front-end knob from an expression to a string type and explicitly setting it to `false` on all entries that don't use overloading. The meeting closed with CHEP 2026 speaker-nomination logistics for two accepted talks.

## Decisions / Conclusions

- The front-end total-slot limit (the sum of partitionable, dynamic, and static slots, currently throttling glidein requests starting at 200,000 and stopping entirely at 220,000) will be raised substantially — Antonio and Marco converged on raising it toward the range of 500,000–1,000,000, reasoning that pushing it far enough away means the team can "forget about it" for years while relying on other signals (collector duty cycle, alerts) to detect real problems. No single final number was explicitly confirmed in the transcript beyond this range.
- The front end's slot limit was confirmed to count the total sum of partitionable, dynamic, and static (not just dynamic/pilot) slots — this was previously unclear to Antonio, who had assumed it was based on pilot/partitionable count only.
- The recent front-end slow-down and a couple of production schedd "out of memory" errors are believed to be related, both driven by an increase in single-core jobs fragmenting the pool into many more (smaller) slots, which increases the collector's update rate and duty cycle, and which in turn causes the front end to throttle new glidein requests as a protective measure for the central manager/collector.
- Static IO slots were confirmed to have low update rates (they only report on activity change, e.g. job start, not periodically) and were judged not to meaningfully contribute to the current duty-cycle increase; no immediate change to IO slot allocation was decided, though Antonio suggested a possible future refinement (only adding IO slots to a fraction of pilots, similar to overloading) if IO slots later prove to be a problem.
- Team agreed that any operational configuration change (e.g. changing front-end/collector limits) must be documented in Jira ("CMS 12"/JIRA), per an existing team decision that Marco acknowledged he had not followed this time; communication about the recent slot-limit issue had been fragmented across five different channels (private chat, internal channel, public channel), which Florian said caused him to lose track and give up following it. Marco will open a Jira ticket to document this change.
- Regarding the "glide-in overload-enabled" monitoring bug: casting the ClassAd expression to a proper type at the monitoring/data-acquisition layer is not feasible (the relevant code path is generic and wrapped in multiple nested loops in the monitoring script), and cannot be fixed on the Grafana side either. The agreed path is to fix it at the source: change the front end's `glide-in overload-enabled` attribute from an expression/ClassAd type to a string type, and then explicitly set that knob to string `false` on every factory entry that does not use overloading (rather than leaving it unset, which currently causes the "dice throw" logic to run without applying the corresponding CPU/memory multiplier). Florian will change the type in the front end and Capitan; Marco and Luis will make the corresponding changes across factory entries.
- The Lumi HPC entry has been validated over several weeks and moved into production.
- The Chinese Tier-3 site (university name not recalled by Luis) remains in a long-standing onboarding ticket; the site admin had to rebuild the cluster essentially from scratch while setting up HTCondor, and the team continues to work through problems and point him to documentation.

## Action Items

- [ ] Change the `glide-in overload-enabled` front-end attribute type from expression to string — Florian Von Cube (planned for "first thing tomorrow" / Friday)
- [ ] Set the overloading multiplier limits/changes in Capitan to match — Florian Von Cube
- [ ] Update all factory entries to explicitly set the overload-enabled knob to string `false` where overloading is not used, and make the corresponding factory-side changes — Marco Mascheroni and Luis Simas (to be discussed/coordinated in their meeting the next morning)
- [ ] Open a Jira (CMS 12) ticket documenting the front-end slot-limit change — Marco Mascheroni
- [ ] Update the GlideinWMS factories once the fixed release (pilot-validation-failure monitoring bug) reaches production, following the normal release-candidate → testing → production repository cycle (no rush to push a release candidate directly to production for this) — Luis Simas / Marco Mascheroni
- [ ] Decide who nominates whom for the two CHEP 2026 talk slots (both currently unassigned), taking into account that Antonio may already be presenting/convening in the same Monday track-4 session, and that it is not yet certain whether Marco will attend CHEP in Thailand — Antonio Perez-Calero Yzquierdo and Marco Mascheroni

## Discussion

### CPU efficiency and CMS computing meeting news
Antonio reported that yesterday's general CMS computing meeting again discussed low CPU efficiency across CMS (particularly at Tier-2 sites and CERN), following questions from the Computing Resource Scrutiny Group. CMS's official answer attributed the drop partly to increased analysis-job share (lower efficiency than production), but Antonio characterized this as "only a half truth" since organized production workloads are also not very efficient. There was discussion of poorly-defined private Monte Carlo production resource requests (e.g. users mistakenly requesting multicore jobs just to get more memory). Marco noted the CSFG recommendation was to move analysis toward more organized submission, but was skeptical this alone would help, since even organized/production workloads underperform; he suggested that without some automatic enforcement (e.g. killing jobs running below ~50% efficiency), the efficiency problem "will always bite us." Antonio connected this to a separate, related issue being discussed by Dima and Stefano regarding data placement: reduced storage means some datasets are only available at Tier-1s while jobs must run at Tier-2s, forcing remote reads and further lowering efficiency. Antonio noted the team has been compensating indirectly by pushing more overloading/packing into pilots, and floated the idea of eventually needing a higher overload fraction (e.g. 50% instead of 25%) and of producing the team's own efficiency metric to be more proactive — this was raised as an idea, not a decision.

### User resource request (Jira ticket)
Marco raised a Jira ticket from a user requesting more resources, related to running a physics analysis (systematic uncertainty calculations). Antonio noted the request was unclear about which resources/pool the user meant (LXBatch vs. the CMS pool), and that the discussion had drifted into evaluating the physics validity of the request rather than the technical resource question. Stephan identified this as likely related to calibration/systematic-uncertainty computing needs and suggested the user should simply use the existing CERN batch queue ("KaFq"/LXBatch), since the relevant group already has a privileged queue/share for this activity (their foot sensor/cup-tube calibration work) rather than needing grid access; he noted this is outside of Submission Infrastructure's scope. Antonio confirmed the team had offered to help test via the grid/pilots if the user could provide a representative test payload, and that this offer stands; the team remains subscribed to the ticket/thread in case grid access is later needed (e.g. via CMS Connect high-priority accounting groups).

### Front-end total-slot limit and single-core job storms
Antonio and Marco reviewed two related issues from the past week: front-end throttling of new glidein requests, and a couple of production schedd errors ("running out of memory"), both attributed to a high number of running jobs/slots. Marco noted that since IO (static) slots were added, the pool's total slot count (partitionable + dynamic + static) had grown; in a prior scale test the pool successfully ran 800,000 jobs, so the current 200,000/220,000 front-end limit (unchanged for roughly 10+ years) was judged too conservative and a candidate for increase, e.g. toward 1 million.

Antonio explained the mechanism using pool-fragmentation plots: the global pool's partitionable slots fragment dynamically to match the mix of job core-counts being requested. When many single-core jobs enter the queues ("single-core job storms" — described as effectively random events from the infrastructure's point of view), the pool fragments into a much larger number of smaller slots for a similar total CPU count. This increases the total slot count, which the front end monitors; if it approaches the limit, the front end stops requesting new glideins (protecting the collector/central manager) — this is one effect. The second, related effect is that more slots means a higher rate of ClassAd updates reaching the collector, raising the collector's duty cycle; if the collector reaches 100% duty cycle, it can no longer keep the pool state current, degrading matchmaking and general responsiveness. The current slot-limit exists specifically to protect the collector from this saturation.

Reviewing monitoring plots live, Antonio and Marco found the collector duty cycle had only risen from about 0.5 to under 0.7 despite an increase of roughly 80,000 single-core jobs/slots (from about 120,000 to 200,000 total slots), concluding there is still meaningful headroom (up to 1.0/saturation) before the collector becomes a real bottleneck. Marco noted the team previously used to hit collector saturation during single-core storms but "nowadays we can swallow them easily." Both agreed to raise the front-end limit to let the pool grow, while continuing to monitor the collector duty cycle as the real protective signal going forward. Marco noted that unlike the schedd layer (which can scale horizontally by adding more schedds), the collector is a single global component that could in principle be partitioned if it became a persistent problem, though the team currently prefers keeping one global collector with full pool visibility.

Static/IO slots were separately discussed: Marco noted they only send updates when they change activity (e.g. job starts), not periodically, so their contribution to the collector's update rate is low; this was judged not currently a problem, though Antonio suggested that if it ever became one, IO slots could be restricted to only a fraction of pilots (similar to how CPU overloading is applied to only a fraction of pilots) as a possible future refinement — not adopted as a current action.

Florian noted the recent troubleshooting communication for this issue was spread across five different channels (private chat, an internal channel, and a public channel), causing him to lose track and give up following it; Marco acknowledged moving the discussion between channels, including an accidental post to the wrong (public) channel. Antonio stated that while informal/quick communication channels are fine for discussion, any actual operational change (e.g. settings changes) must be documented in Jira ("CMS 12"), reiterating an existing team decision; Marco agreed this was on him this time and said he would open a Jira ticket for this change.

Luis asked why this slot limit hadn't been hit before; Antonio's fragmentation-plot walkthrough (above) was the response, and Luis noted he had previously only been thinking about pool size in terms of pilot count, not fragmentation into dynamic/static slots.

### Factory operations (Luis)
Two new entries are in production and currently being troubleshot/tested (pilots are running in the pool). A GlideinWMS bug affecting visibility of pilot-validation failures in monitoring has been fixed upstream (PR merged); the team is waiting for the next GlideinWMS release. Marco explained the release will likely appear as a release candidate next week, following the usual multi-candidate early cycle before the RPM moves to the testing then production repository; per Marco, the team should wait for this normal release cycle rather than push a release candidate directly to production, since ITB is normally updated first for issues like this.

The Lumi HPC entry: after several weeks of validation of slots and related issues, all resources are now considered fine and the entry has moved into production. Luis added the site admin (Thomas) is still troubleshooting some things and currently running smaller-slot pilots (via a "forkar" pilot, name as heard) to debug, before moving to 8-core pilots; jobs are running successfully there.

The Chinese Tier-3 site (a long-standing ticket) required the site admin to rebuild the cluster essentially from scratch while setting up HTCondor; the team continues fixing problems incrementally and pointing him to documentation.

### Dynamic resources and HPCs / HLT / B.5
Antonio had no update on BSC (manual-glidein-with-split-starter testing) due to the Easter holiday and vacation; he had tested it roughly a week and a half prior but had not progressed further. No change of status was reported for HLT (currently in data-taking) or the B.5 pool, which remains stable at roughly 11,000 (units as heard, likely "cores").

### Glide-in overload-enabled monitoring/type bug
Florian investigated fixing the "glide-in overload-enabled" flag issue affecting Grafana monitoring, exploring three options discussed the previous day: fixing it on the factory/front-end side, on the monitoring data-acquisition side, or on Grafana's side (ruled out as infeasible). He found that while the underlying ClassAd could in principle be cast/converted at query time, the monitoring script's relevant code path is generic and deeply nested (wrapped in loops "five times"), making a targeted fix there non-trivial; an attempted quick fix did not work.

Marco proposed the cleaner fix: change the front-end's `glide-in overload-enabled` attribute type from an expression to a string. Florian noted this then raises the previously-discussed issue: if the type is a fixed string, the factory (not the expression) must be the one to "throw the dice" to decide whether to apply overloading, based on the front end's true/force setting plus separate CPU/memory overload multipliers (1.25, i.e. 25% overloading). The problem is that entries which don't use overloading at all would still have the dice thrown (since the multiplier isn't set for them), meaning the dice-throw logic runs without ever applying an actual multiplier. Antonio proposed resolving this by having such entries always resolve the dice-throw to `false` (i.e., a "fraction to overload" of zero) rather than skipping the logic. Marco proposed implementing this by explicitly setting the overload-enabled knob to string `false` on all such entries at the factory level, overriding whatever the front end provides — agreed as the way forward, despite Marco's reservation about having to touch "all the entries."

Florian confirmed the monitoring side works fine as long as the field is consistently one type (string), but noted the OpenSearch index will only fully re-cast to the new type once it regenerates with new incoming documents, likely not until next month; there is a risk of gaps in overload-status data ("Chap"/CHEP dashboard, as referenced) until then. Florian suggested cross-checking with Carlos once the change is made. The team agreed to first make the front-end/factory side consistent, then address the monitoring/OpenSearch side separately.

Florian will change the front-end type (also needs to be applied in Capitan, which currently has local changes blocking a direct push) and planned to do this "first thing tomorrow." Marco noted the worst case of a temporary inconsistency is simply not applying overloading for a couple of days, which is tolerable. Marco and Luis will make the corresponding factory-entry changes, planned for discussion in their meeting the next morning; Marco also mentioned he and Luis may use time next week (when Marco is at CERN) to focus specifically on the overloading monitoring fix.

### CHEP 2026 speaker nominations
Antonio confirmed CMS Submission Infrastructure has two accepted posters (Antonio nominated himself for one — GlideinWMS/factory scalability poster — and Marco for the other) and two accepted talks, both scheduled in the same Monday track-4 session ("CMS collaboration: advanced support for resources" and "advanced scheduling strategies for improved CPU efficiency"). Antonio noted he is also a convener for track 4 and may end up convening that same session, which combined with presenting could mean he is both convener and speaker twice if Marco does not attend. Both talks still need a nominated speaker (and full author list) in the conference tool before CMS-level propagation. Antonio expressed a preference for nominating one talk to each of them rather than both to himself, citing a concern that nominating the same person to too many contributions could draw pushback from Level 1s or the conference committee; he suggested deciding this after clarifying whether Marco will actually attend CHEP in Thailand, given hybrid/remote attendance is expected to not be permitted. No final nomination decision was made; it remains open, to be discussed further. Separately, Florian confirmed he will not attend CHEP due to starting a new position; Antonio noted his own attendance is not 100% guaranteed and contingent on world events (a reference to the Middle East situation affecting flight corridors was made). Marco noted he has three events available to him but was asked to pick two, and chose to prioritize the other two given uncertainty around this trip.

## Open Questions

- What is the final new value for the front-end total-slot limit (a range of roughly 500,000–1,000,000 was discussed, but no single number was confirmed)?
- Will raising the slot limit require any change to IO/static slot allocation policy (e.g. only adding IO slots for a fraction of pilots) if they later prove to add meaningful load?
- Will the OpenSearch index re-cast (and associated risk of a monitoring data gap) be an acceptable tradeoff, and can it be triggered manually with Carlos's help?
- Who will be nominated as speaker for each of the two CHEP 2026 talks, and will Marco be attending CHEP in Thailand?
- Will Antonio's planned attendance at CHEP be affected by world events impacting flight routes?

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[Monitoring]] · [[CMS]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Dynamic Resource Provisioning]] · [[HPC]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-09 17.02.59 Submission Infrastructure Weekly Meeting`)
