---
type: meeting
date: 2026-07-16
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Luis Simas
  - Hyunwoo Kim
topics:
  - CPU inefficiency table / terminology alignment with Computing Operations
  - HTCondor SCEDD vulnerability upgrade rollout (WMAgent, CRAB, CMS Connect, MIT)
  - WM code-freeze sustainability concerns
  - Machine/host inventory for Submission Infrastructure
  - DIRAC / HTCondor developers pilot-submission discussion
  - Pool status and CERN worker-node reboots
  - Puppet certificate expiration on the global pool front end
  - Factory operations tickets (draining-state cleanup, IPv6)
  - Pilot retire-time spread / whole-node pilot lifetime clustering at Fermilab
  - HLT machines move to P2
  - Monitoring alert cleanup and alarm ownership/routing
  - glideinWMS package auto-update exclusion on legacy front end
  - Summer meeting schedule
---

# Submission Infrastructure Weekly Meeting (2026-07-16)

## Summary

Antonio Perez-Calero Yzquierdo, Marco Mascheroni, Luis Simas, and Hyunwoo Kim covered the usual round of Monday-meeting news, infrastructure status, and factory operations. Main threads: a renewed Computing Operations effort (led by Kirill) to quantify CPU inefficiency, which the group felt needs closer SI involvement to avoid terminology confusion; the slow, partial rollout of an HTCondor SCEDD vulnerability fix across WMAgent, CRAB, CMS Connect, and MIT, complicated by the ongoing WM code freeze; a long technical discussion of `glidein` pilot lifetime parameters (retire time, retire time spread, max wall time) triggered by Fermilab's very synchronized pilot-retirement pattern on whole-node jobs; monitoring/alerting cleanup, including a discussion about which alarms SI should own versus route elsewhere; and a Puppet certificate/package-update issue on the legacy global-pool front end. The meeting closed with a discussion of the reduced-activity summer schedule.

## Decisions / Conclusions

- The existing "payload monitors" panel in the Submission Infrastructure Grafana dashboard (showing job-type split, idle/killed jobs, average memory requested per job, etc.) already covers the pool-usage-by-group tracking Luis had raised; no new dashboard is needed for this.
- Re-confirmed an earlier agreement that fine-grained (day-to-day) alarms on the split of pool usage between production/analysis/Tier‑0 are not worth having, since usage naturally fluctuates and the group mainly cares about the time-integrated split; complaints from affected groups are considered a sufficient practical signal if the split goes seriously wrong.
- The Puppet certificate issue on the global pool front end is resolved: Puppet is now running continuously (all the time) on all machines, so the automatic certificate renewal should prevent a recurrence. Luis suspects the original cause was that Puppet had previously been disabled, which let the agent's client certificate expire without being renewed.
- On the legacy/volunteer central-manager machine (which also runs a glideinWMS front end): the group will not upgrade its glideinWMS version until "Florian's replacement" is available, since it is currently unmaintained/non-critical and working. The recurring auto-update-failure alert for it will instead be fixed by adding the missing `glideinWMS` HTTPD package (and any other missing glideinWMS packages) to the DNF auto-update exclude list, and separately noting it for addition to the DNF version-lock list later.
- No SI weekly meeting is expected during weeks when both Antonio and Marco are unavailable: Marco is on vacation Aug 3–7 and Aug 17–21; Antonio is attending a conference in Spain the following week and then on vacation for roughly 3–4 weeks starting in early August, returning the last week of August. Outside of those specific weeks, the group will decide on shorter/adapted meetings on a rolling basis.

## Action Items

- [ ] Try setting the `glidein` retire-time-spread parameter for Fermilab only (parameters are configurable per site) and observe the effect on the whole-node pilot lifetime clustering — Marco Mascheroni
- [ ] Open a (low-priority) ticket/GitHub issue with the glideinWMS developers proposing support for a variable/configurable max wall time, so pilots don't all retire at the same fixed lifetime — Marco Mascheroni (to be discussed together with Antonio Perez-Calero Yzquierdo)
- [ ] Create the composite "core matchmaking" / insufficient-active-SCD alarm(s) (initially owned/received by SI, not yet routed elsewhere); observe how they behave before deciding whether to hand them off to PNR/CRAB — Luis Simas
- [ ] Figure out the emailing/routing setup for these alarms once the corresponding "soft" (downstream) alarms also exist — Luis Simas
- [ ] Add the missing glideinWMS HTTPD package to the DNF auto-update exclude list on the legacy central-manager/front-end machine, and leave a note in the version-lock file to add it there too later — Luis Simas
- [ ] Retest IPv6 for pilots at the Indian site once its network downtime is over (currently disabled there) — Luis Simas
- [ ] Raise the lack of replies to the Condor SCEDD-vulnerability upgrade request (CRAB dev agents, CMS Connect, MIT, Benedict) at the Monday Computing Operations meeting — Marco Mascheroni

## Discussion

### CPU inefficiency table and terminology (Computing Operations)

- Antonio reported that Kirill (Computing Operations) presented a table breaking down elements contributing to CPU inefficiency, reviving a push on this long-standing problem (efficiencies reportedly sometimes below 50%).
- The presentation used the term "scheduling efficiency" in a way inconsistent with SI's existing use of the term, and Antonio felt the discussion touched on subtleties (e.g., 32-core/32-thread job usage) that weren't fully resolved; it was described as an initial presentation, postponed for further discussion since the Monday meeting doesn't allow enough time for technical depth.
- Marco raised a related point from Stefano Belforte about the "hold time" attribute used in monitoring: when a job restarts (e.g., after a Condor restart), only the last hold-time value is counted rather than the sum of all restarts, distorting inefficiency figures. Antonio confirmed this was part of the same discussion; Stefano intends to redo the calculation and make the formula/definition for each field fully explicit, partly to help onboard new people who otherwise have to rediscover these subtleties.
- Open sub-question raised in the discussion: whether "bad put" (wasted resources from a job being repeatedly put on hold and retried) should count as "inefficiency" in the same sense as idle CPU time — not resolved.
- Both Antonio and Marco agreed SI needs to stay involved in this discussion and help re-converge on shared terminology, given SI's own deep involvement in the inefficiency/pilot-overloading problem.

### DIRAC / HTCondor developers discussion on pilot submission to CEs

- Marco organized a discussion between DIRAC developers and Condor developers about using Condor's capabilities to submit pilot jobs to CEs (as an alternative/addition to glideinWMS). Antonio could not attend but read the minutes and found it a useful starting point for recognizing both community needs and Condor's capabilities; terminology alignment came up here too.
- Marco clarified this is not a top CMS priority currently (focus remains on the transformation system), but he wanted to "plant a seed" for a capability CMS may need later, and to potentially align with DIRAC's approach the way SI already collaborates on ETF (experiment test framework) tests.
- Antonio noted a possible secondary benefit for SI: if DIRAC integrates with Condor-G (or similar) to submit pilots to resources other than via glideinWMS, this could function as a backup submission path in case of future issues with glideinWMS.

### HTCondor SCEDD vulnerability upgrade rollout

- Following up on the previous week's discussion of an HTCondor vulnerability affecting SCEDDs, Marco reported he had sent an announcement requesting upgrades but had not received replies from Benedict, PNR, or others; Antonio confirmed he saw the email but no reply.
- The plan discussed (worked out with Luis) was to move to Condor version 24.0.21 — described as the version immediately prior to the one containing the fix, so the eventual jump to the fix would be a small, easy version bump. CRAB was reported as already upgraded.
- Hyunwoo separately reported status for the six Fermilab WMAgent machines: after coordinating with the WMAgent operators (Gregor and team), four machines were upgraded to Condor 25.0.12. One of the five originally attempted at 25.0.12 hit an unspecified issue (referred to in the transcript as breaking something — the exact affected component is unclear) and was downgraded back to 24.0.22. Current status: four machines on 25.0.12, two on 24.0.22 — both versions considered to resolve the vulnerability. It's unclear from the transcript whether this version numbering is fully consistent with the 24.0.21 plan discussed earlier with Marco; the note preserves both as stated.
- Hyunwoo asked the WMAgent operators to investigate what's needed to move the remaining machines to Condor 25.

### WM code-freeze sustainability concern

- Marco raised a concern that upgrading Condor could introduce breaking changes to WMAgent, and that the WMAgent codebase is under a code freeze (developers reassigned to the future WM system) with reduced in-house expertise to fix issues if something breaks — calling a multi-year freeze without addressing this "not scalable" and something that needs to be raised with management.
- Antonio confirmed the code freeze's purpose (letting developers focus on the future WM system) and agreed operations/PNR can still make code changes if something breaks, but the people with deep expertise are focused elsewhere. He suggested, as an idea rather than a settled plan, that SI could push the Condor team to continue providing bug-fix releases on the 24.x branch for an extended period to ease the transition, potentially as part of SI's existing collaboration with the Condor team.
- Both agreed this specific sustainability issue is bigger than this meeting and not something to resolve here.

### Machine inventory and Tier-0 pool share

- SI compiled a list of hosts in Submission Infrastructure accessed by jobs on worker nodes and remote sites, and passed it to Stefan/facilities (presented there). Antonio noted the list used actual hostnames, which tend to go stale relatively quickly, and suggested it might be better to include aliases, or a reference to SI's own dynamically-maintained node list, as a future improvement — for at least the central manager and factory, aliases should still be included per Marco.
- Tier-0 jobs are still consuming a fraction of the pool but were reported as being in their last days of doing so; after that, production and analysis regain full access to the pools.

### Infrastructure status

- Combined average pool size was on the lower side (~410,000 CPU cores) but scheduling efficiency was very high/good.
- Reduced capacity was attributed mainly to CERN rebooting worker nodes to apply vulnerability patches (affecting both the Tier-0 and shared partitions); Antonio believes this is now essentially done, based on the pool regaining (and briefly exceeding) its normal share once CERN's drain/intervention ended, since SI is typically fast to reclaim resources after an intervention. Similar reboot-related interventions were reported at Nebraska, MIT, Purdue ("Peak"?), and Fermilab (mentioned on Monday), possibly causing continued fluctuations.

### Puppet certificate expiration on the global pool front end

- An alarm fired for the global pool front end: the Puppet agent's client certificate (used to authenticate to the Puppet server, distinct from the front end's own operational certificate) had expired. Luis manually renewed it.
- Luis suspects the root cause was Puppet having been previously disabled, preventing automatic certificate renewal. Downtime was brief (minutes to a couple of hours) before Luis noticed and fixed it via the alarm.

### Factory operations tickets

- Desy: a recurring issue where their node-reboot automation doesn't clean up the machine/job-features draining-state file before rebooting, so nodes come back still marked as draining and pilots immediately retire. Desy is aware and needs to fix it on their side.
- Indian site: IPv6 is currently disabled for pilots there (site-specific configuration); the site is ready to retest but currently has a network downtime, so testing is on hold.

### Pilot retire-time spread and lifetime clustering at Fermilab

- Luis had observed a very clear pattern at Fermilab: pilots retire (and new ones are submitted) in near-synchronization roughly every 5 days. This doesn't cause problems by itself, but risks a fast pool drop if pilot submission has issues at the moment retirement is due.
- Following up on a prior discussion with Marco about the glideinWMS "retire time spread" configuration parameter, Luis confirmed via the glideinWMS code (documentation was ambiguous/confusing on this point) that the spread is applied when `GLIDEIN_Max_Walltime` is used, and — importantly — the spread only ever shortens a pilot's lifetime relative to the max wall time, never extends it, so the hard cap (agreed with the resource provider) is preserved.
- The group revisited how retire time, retire time spread, and max job wall time interact: setting all three explicitly can produce an inconsistent combination, so effectively one of the parameters gets overridden/ignored depending on what's set (previously a source of confusion for the team).
- Marco argued that for Fermilab's whole-node jobs specifically, retire-time spread would likely not help: the spread only affects when the pilot stops *accepting* new jobs, not the pilot's actual end time, and whole-node pilots run enough jobs that some will always run until the true max wall time — so pilots stay synchronized regardless of the spread setting. This effect is much less pronounced on non-whole-node sites, where pilots typically run only 1-2 sequential jobs and naturally get spread out as each job finishes at a different time.
- Antonio added a second contributing factor: at a fully-dedicated resource like Fermilab, SI acquires/fills the pool quickly (no competition with other users), so pilots start together and therefore also tend to finish together; at shared sites, slower/staggered resource acquisition naturally desynchronizes pilots. Deliberately slowing pilot acquisition/submission was raised as a theoretical way to desynchronize pilots, but rejected as undesirable since it would also slow recovery of full capacity after downtimes.
- Hyunwoo asked whether the retire-time/spread/max-walltime parameters are uniform across all glideins or configurable per site; confirmed they are set per site (whole-node handling, e.g., at Fermilab, differs from other sites).
- Antonio characterized the observed effect (efficiency dropping to about 85% for a brief period at retirement time) as real but not severe, within an otherwise excellent, flat efficiency profile — questioning whether more invasive fixes were worth the effort, but was open to a low-effort fix. Marco agreed to test retire-time spread for Fermilab only despite expecting it won't fully solve the whole-node case, and separately proposed raising the idea of a variable/configurable max wall time with the glideinWMS developers as a longer-term fix, so not every pilot has the exact same fixed lifetime.

### HLT machines move to P2

- The move of HLT machines to the P2 site (raised in Monday facilities/computing-ops meetings, reported via Viva as VOC) is not yet ready; Antonio understood this could take until August, since the relevant team (name unclear in the transcript, heard as "Senati"/"Sunite") is not fully available due to vacations. The move is more involved than simply relocating hardware and bringing it back up.

### Monitoring/alerting cleanup and alarm ownership

- Luis reported the Grafana alert cleanup is now mostly complete: some alerts were merged, some deleted, and the remaining ones are all meaningful again — team should not ignore alerts going forward.
- Two remaining alert topics to align on:
  - **Production-jobs pressure in the global pool** (tracking idle-job pressure). Antonio gave historical context: SI previously pushed back on WM/Computing Operations after episodes (roughly a year-plus ago) where a broken WM-chain component silently starved the pool of work, often unnoticed over a weekend for 48–72+ hours, discovered only because SI noticed the downstream symptoms (pilot pressure/pool size dropping) without being able to fix the upstream cause. This led to an agreement that SI would build alarms on upstream symptoms visible to SI (e.g., insufficient active/healthy SCDs, "core matchmaking" status) but route/forward them to the responsible teams (WM/PNR/Computing Operations) rather than treat them as SI's own alarms to fix.
  - Luis raised a competing view: since he lacks the detailed knowledge PNR/CRAB have about their own services (e.g., which SCDs are draining), he leans toward SI focusing on downstream alerts it fully owns and understands, while questioning why SI is responsible for building the best alert for someone else's system when that team has the same Grafana data access. Antonio's counter was that SI's responsibility here is more a matter of applied pressure/accountability (detecting and forcing attention to a real recurring problem) than technical necessity.
  - Marco's position: he's fine with SI keeping a broader set of "soft" diagnostic alarms (e.g., core matchmaking) as long as they aren't emailed to SI — he only wants a single clear "hard" alarm/email when the pool is actually deflating, which he can then use as the trigger to go look at the supporting diagnostic pages; noisy alarms sent to the wrong people (or too many people) risk being ignored. Antonio agreed with this framing.
  - Resolved path forward: Luis will build the upstream alarms, keep them under SI's ownership for now (not necessarily emailing SI), observe how they behave, and revisit with the relevant teams later whether to hand off ownership.

### glideinWMS package auto-update failures on legacy front end

- Luis had been tracking down a set of alerts (Puppet-disabled, distro-sync failing) on front-end machines and traced most to a failing auto-update of a glideinWMS package. He asked which glideinWMS version the legacy/volunteer central-manager+front-end machine should run, since Puppet had a different version pinned than what was actually running; Marco confirmed the running version should be treated as correct and the machine should not be touched/upgraded until "Florian's replacement" exists.
- The mechanism: a DNF cron job auto-updates packages, and it fails whenever it hits an un-excluded, unlocked package that would break a dependency of a version-locked package (`glideinWMS-httpd`/`glideinWMS.xml`-related package). Version-locked packages are excluded from the failing chain; the `httpd` package is missing from both the version-lock list and the auto-update exclude list, causing the recurring alert.
- Agreed fix: add the missing package to the DNF auto-update exclude list (a low-risk config change, doesn't touch the running front end or version), and leave a note to also add it to the version-lock list later rather than making that change immediately. Marco noted version lock (originally added by Nikos, whom he had previously been skeptical of) is in this case actually what's preventing a broader unwanted cascade of package updates.

### Summer meeting schedule

- Antonio: traveling to a conference in Spain the following week (so may be unavailable Thursday); then on vacation roughly 3–4 weeks starting shortly after, into early August, returning the last week of August (reachable for emergencies only).
- Marco: on vacation Aug 3–7 and Aug 17–21; available the other week(s) in between to run the meeting if others are around.
- Hyunwoo confirmed the assumption that the meeting is skipped specifically when both Antonio and Marco are unavailable, i.e., the weeks of Aug 3–7 and Aug 17–21; the rest of the summer will be handled adaptively as people's availability varies.

## Open Questions

- Whether setting `glidein` retire-time spread for Fermilab specifically will meaningfully reduce pilot-retirement synchronization, given whole-node jobs tend to run until the true max wall time regardless.
- Whether/how to formally reconcile the "scheduling efficiency" and CPU-inefficiency terminology between SI, Computing Operations, and the DIRAC/Condor developer discussions.
- Whether "bad put" (repeated job hold/retry) should be counted as inefficiency alongside idle CPU time.
- Whether Condor developers would be willing to extend bug-fix support on the 24.x branch to ease the WM code-freeze transition — raised as an idea, not yet pursued.
- Exact cause and affected component of the issue Han Vu reportedly saw when testing Condor 25.0.12 on a Fermilab WMAgent machine (transcription unclear).
- Final ownership/routing of the new upstream ("core matchmaking" / insufficient-SCD) alarms once they and the corresponding downstream ("soft") alarms exist.
- Timeline for the HLT machines' move to P2 (currently expected around August, pending Senati/Sunite-team availability — exact team name unclear in the transcript).

## Related

[[HTCondor]] · [[glideinWMS]] · [[WMAgent]] · [[DIRAC]] · [[CRAB]] · [[Submission Infrastructure]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Puppet]] · [[CMS]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-16 16.04.49 Submission Infrastructure Weekly Meeting`)
