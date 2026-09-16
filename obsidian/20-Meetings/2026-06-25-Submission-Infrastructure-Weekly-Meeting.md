---
type: meeting
date: 2026-06-25
participants:
  - Marco Mascheroni
  - Luis Simas
  - Hyunwoo Kim
topics:
  - CERN Tier 2 site-token migration and GPU entry split
  - Factory version upgrade to 3.11.4 (ITB tested, production planned)
  - Front-end version gap across CMS/OSG factories and plan to catch up
  - MIT site-token blocker for front-end upgrade
  - Third ("Fnal") negotiator to isolate Fermilab Tier 1 production-job matching
  - ITB test-job submission walkthrough
  - Brainstorming meeting with Jamie (memory-aware scheduling, pilot lifetime extension, CRAB submission-point load balancing)
  - CRAB overflow concurrency limits and TierZero-requested revert
---

# Submission Infrastructure Weekly Meeting

## Summary

Antonio was traveling and did not join; the meeting was held as a quick round table between Marco, Luis, and Hyunwoo.

Luis reported that the CERN Tier 2 entries were migrated to site tokens on the OSG factory, and that the front-end security class fix behind this has been validated as working. He also split off a dedicated GPU entry for the CERN Tier 2 with separate CPU/memory profiles, and confirmed CRAB jobs are already running through it. A related ticket from Ben Jones (in the CMS "computing tools" category, about analysis-infrastructure/GPU support) was handed off to Luis to reply to and close. Luis also reported the ITB factory was upgraded to glideinWMS 3.11.4 with no issues; Marco said production deployment could proceed but wanted to first cross-check with Jeff on a task/ticket referred to in the transcript as sounding like "Deus G532311" (unclear transcription) before rolling it out, likely early the following week rather than on a Friday.

Hyunwoo raised the growing version gap: production factories are on 3.11.3, the OSG factories are believed to be on 3.11.4, CMS front ends are still on the 3.10.x line, and OSG front ends have moved to 3.11.4. He asked what the plan is to catch up the CMS front ends. Marco noted this is now more feasible since the grid-proxy-to-site-token migration is largely done, and that both proxy and site token should be supported together in some 3.x version per a comment from Marco Mambelli at another meeting, but said he has been reluctant to touch the front end given the team is currently without a dedicated factory operator. Hyunwoo pushed back that the new operator hire is still months away, and the three of them agreed to attempt the front-end upgrade themselves, starting with ITB.

Luis identified the MIT site as the blocker for the front-end upgrade: it currently doesn't work with site tokens. The group agreed this is a soft block — if the MIT site admin doesn't fix it within about a week, the team will revert that site specifically back to grid-proxy-only so the rest of the front-end upgrade can proceed; at that point only Syracuse (name uncertain in transcript, referred to as "Arxys") and MIT would remain on grid proxy. Luis added that Jeff had described the 3.10-to-3.11 front-end upgrade as non-trivial due to required configuration changes, and asked whether this applies to the CERN front ends. Marco said it likely does — possibly requiring a custom credential-handling plugin, or at minimum configuration changes to use available defaults — and that the upgrade should not be expected to be transparent.

Hyunwoo then gave a detailed technical update on his plan (first reported previously) to prevent CRAB/CMS Connect user (analysis) jobs from being scheduled at the Fermilab Tier 1. His current plan is to test this in the ITB pool: stop the negotiator on the CERN-side ITB machine and start a negotiator on the Fermilab backup machine's collector, then modify the negotiator configuration to launch a third child negotiator (referred to as "negotiator Fnal") alongside the existing two (Tier 1 and US), which will exclusively match production user jobs against the Fermilab Tier 1; all other matching remains with the existing two negotiators. He plans to start this testing sometime the following week in ITB, and if successful, continue testing there and upgrade the Fermilab backup front end to 3.11.4. Marco confirmed the approach made sense, clarifying this means adding a job constraint (not currently used in production, where only a slot constraint is used) restricting the new negotiator to production jobs only; Hyunwoo confirmed. Marco separately noted the team conceptually needs three negotiators — Tier 1, US, and one covering the rest (European Tier 2s/Tier 3s) — and Hyunwoo clarified terminology: these are "child" negotiators under a main negotiator.

To prepare for ITB testing, Hyunwoo shared his screen and, with Marco's guidance, walked through submitting test jobs on host `0811` (under `/data/srv`), using Marco's existing test scripts (`multicore.jdl`, a `sleep` job, and a script exporting a target site before `condor_submit`). Marco explained how to select desired sites, and confirmed there is no restriction preventing Hyunwoo from setting the job's accounting group to `production.cms` (as opposed to an `analysis.<username>` group) in order to test whether the planned third negotiator correctly accepts production-owned jobs and rejects others.

Marco gave an update on a brainstorming meeting he had with Jamie the previous day, following up on topics from the earlier face-to-face management meeting. Discussion points included: memory requirements for CMS workflows likely increasing, and the possibility of more sophisticated memory-aware scheduling using average rather than peak memory — Jamie, who has expertise in container memory management and cgroup enforcement, suggested he be involved in this area (the transcript is unclear on the exact framing beyond this); extending pilot lifetime so a pilot nearing retirement could request a time extension to keep running jobs rather than retire, which Marco noted would require site-level work outside the team's control; and ideas about better spreading CRAB job submission across multiple access points/remote condor submit requests, since CRAB currently uses a single submit point with a "locator" function that selects a scheduler based on attributes (memory, running jobs, and data transfer — using the lowest of the three to weight scheduler selection) to pick the least busy scheduler at submit time. Marco asked Jamie whether this locator mechanism could be generalized; Jamie mentioned that at CHTC, users are manually assigned to specific access points, and Marco thought something similar could be worth exploring for CMS in the future. These were characterized as forward-looking brainstorming ideas rather than concrete plans.

Finally, Marco described a concurrency-limit change made this week to CRAB overflow (the mechanism where jobs queued too long at a site are allowed to run elsewhere and read data remotely): the negotiator now caps the number of concurrently running overflow jobs at 2000, via separate concurrency limits for Tier 2 CRAB-overflow and Tier 1 CRAB-overflow. He confirmed this has been verified as working. He noted the TierZero team has since asked for "the quota" to be reverted to its previous value (the transcript does not make fully explicit whether this refers to the overflow concurrency limit just described or another quota), and said he would take care of it.

## Decisions / Conclusions

- CERN Tier 2 entries have been migrated to site tokens on the OSG factory; the front-end security class fix behind this is validated as working.
- A separate GPU entry with distinct CPU/memory profiles was split out for the CERN Tier 2; CRAB jobs are confirmed running through it.
- ITB factory upgrade to glideinWMS 3.11.4 is complete and stable; the group agreed to proceed toward a production deployment, pending a cross-check with Jeff.
- The team agreed to attempt the CMS front-end version upgrade (currently 3.10.x) themselves rather than wait for a new factory operator (still months from being hired), starting with ITB.
- If the MIT site admin does not fix site-token support within about a week, the team will revert that site specifically to grid-proxy-only so the broader front-end upgrade is not blocked.
- Agreed technical approach for isolating Fermilab Tier 1 from analysis jobs: add a third ("Fnal") child negotiator, tested first via negotiator failover to the Fermilab backup machine in ITB, using a job constraint that accepts production jobs only; if ITB testing succeeds, the Fermilab backup front end will be upgraded to 3.11.4.
- The CRAB-overflow concurrency-limit change (capping overflow jobs at 2000 for Tier 1 and Tier 2) is implemented and verified working.

## Action Items

- [ ] Reply to and close the Ben Jones ticket (CMS "computing tools" category, analysis-infrastructure/GPU support) — Luis Simas
- [ ] Start testing the third ("Fnal") negotiator / job-constraint configuration in the ITB pool, including submitting test jobs with production vs. analysis accounting groups — Hyunwoo Kim
- [ ] If ITB testing of the third negotiator succeeds, upgrade the Fermilab backup front end to 3.11.4 — Hyunwoo Kim
- [ ] Revert "the quota" (per the TierZero team's request, following this week's CRAB-overflow concurrency-limit change) back to its previous value — Marco Mascheroni

## Discussion

### CERN Tier 2 site-token migration and GPU entry split
Luis confirmed the CERN Tier 2 entries were pushed to site tokens on the OSG factory, and that the front-end security class fix required for this has been validated. He also split off a dedicated GPU entry for the same site to allow different CPU/memory profiles, and reported CRAB jobs already running there successfully.

### Factory version upgrade
The ITB factory was upgraded to glideinWMS 3.11.4 with no issues observed. Marco was open to deploying this to production but wanted to first confirm with Jeff whether a specific task (transcribed unclearly, sounding like "Deus G532311") had been completed, suggesting deployment early the following week given it was already Thursday night.

### Front-end version gap and upgrade plan
Hyunwoo noted the version mismatch across components: production factories on 3.11.3, OSG factories believed to be on 3.11.4, CMS front ends still on 3.10.x, and OSG front ends on 3.11.4. Marco explained his hesitation to touch the front end has been the lack of a dedicated factory operator, making him want to minimize changes, but noted the underlying auth migration to site tokens (with some remaining proxy-only sites) makes the front-end upgrade more feasible now; Marco Mambelli reportedly said both proxy and site token should be supported together starting at some 3.x version. Given the new operator hire is still months away, the group agreed to attempt the upgrade themselves, starting with ITB.

### MIT site-token blocker
Luis identified MIT as currently not working with site tokens, which softly blocks the front-end version upgrade. The group agreed that if MIT's site admin doesn't resolve this within about a week, the team will revert MIT specifically to grid-proxy-only so the rest of the front-end upgrade can proceed; at that point Syracuse (transcribed as "Arxys" — uncertain) and MIT would be the only sites remaining on grid proxy. Separately, Luis relayed that Jeff described the underlying 3.10-to-3.11 upgrade as non-trivial due to required configuration changes; Marco said this likely applies to the CERN front ends too, possibly requiring a custom credential-handling plugin or configuration changes to use available defaults, and that the upgrade should not be expected to be fully transparent.

### Third negotiator for Fermilab Tier 1 production-only matching
Hyunwoo described his concrete testing plan to prevent CRAB/CMS Connect analysis jobs from matching the Fermilab Tier 1. He will fail the negotiator over from the CERN ITB machine to a Fermilab backup machine acting as collector, then configure a third child negotiator ("negotiator Fnal") to exclusively handle matching between production user jobs and the Fermilab Tier 1, leaving the existing Tier 1 and US child negotiators to handle everything else. Testing is planned to start the following week in the ITB pool; if successful, Hyunwoo will continue testing there and upgrade the Fermilab backup front end to 3.11.4. Marco confirmed the approach, clarifying that it involves a job constraint (production jobs are not currently filtered by job constraint in production — only a slot constraint is used) restricted to production jobs only. Marco also reiterated the team conceptually needs three negotiators (Tier 1, US, and one for remaining European Tier 2s/Tier 3s); Hyunwoo clarified these are "child" negotiators operating under a main negotiator.

### ITB test-job submission walkthrough
Hyunwoo shared his screen to confirm he knew how to submit test jobs in the ITB pool. Marco walked him through using existing test scripts and JDL files (`multicore.jdl`, a sleep job) in `/data/srv` on host `0811`, setting a target site via an environment variable before `condor_submit`, and confirmed there is no restriction preventing Hyunwoo from setting the job's accounting group to `production.cms` (versus an `analysis.<username>` group), which will let him verify the new negotiator accepts production-owned jobs and rejects others.

### Brainstorming meeting with Jamie
Marco summarized a brainstorming meeting with Jamie the previous day, following up on the earlier face-to-face management meeting:
- **Memory-aware scheduling**: CMS workflow memory requirements are likely to increase; discussed a more sophisticated scheduling approach using average rather than peak memory. Jamie, who has expertise in container memory management and cgroup enforcement, suggested involvement in this area (the transcript is unclear on the precise framing).
- **Pilot lifetime extension**: idea of a pilot nearing the end of its lifetime requesting a time extension to keep running jobs instead of entering retirement, which could affect efficiency. Marco noted this would require site-level work and is not something the team itself can act on.
- **CRAB submission-point load balancing**: discussed spreading CRAB submissions over multiple access points/remote condor submit requests, since CRAB currently has a single submit point with a "locator" function that selects a scheduler based on the lowest of three attributes (memory, running jobs, data transfer) to weight scheduler selection and pick the least busy one. Marco and Jamie discussed whether this could be generalized; Jamie noted CHTC manually assigns individual users to specific access points, which Marco thought could be worth exploring for CMS's future.
These were discussed as forward-looking, exploratory ideas rather than agreed plans.

### CRAB overflow concurrency limits
Marco described this week's change implementing concurrency limits in the negotiator to cap CRAB-overflow jobs (jobs that, after queuing too long at a site, are allowed to run elsewhere and read data remotely) at 2000 concurrently running jobs, via separate limits for Tier 2 CRAB-overflow and Tier 1 CRAB-overflow. He confirmed this was verified as working. He noted the TierZero team has since requested reverting "the quota" to its previous value; Marco committed to handling this, though the transcript does not make fully explicit whether this refers to the overflow concurrency limit itself or a different quota.

## Open Questions

- What exactly is the task/ticket Marco referred to (transcribed unclearly, sounding like "Deus G532311") that needs to be confirmed with Jeff before the production factory 3.11.4 deployment?
- Is the site remaining on grid proxy alongside MIT actually Syracuse, or a different site (transcribed as "Arxys")?
- Which "quota" did the TierZero team ask to have reverted — the CRAB-overflow concurrency limit discussed this week, or a different quota?

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[CRAB]] · [[Factory Operations]] · [[Factory Configuration]] · [[Pilot Jobs]] · [[CMS]] · [[Site Token Migration]]

## Source

meeting_saved_closed_caption.txt (from `2026-06-25 17.02.40 Submission Infrastructure Weekly Meeting`)
