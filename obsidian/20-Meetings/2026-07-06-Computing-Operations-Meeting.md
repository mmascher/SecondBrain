---
type: meeting
date: 2026-07-06
participants:
  - Dmytro Kovalskyi
  - Sitian Qian
  - Ajit Mohapatra
  - Marco Mascheroni
topics:
  - workflow CPU efficiency vs. PPD-reported efficiency
  - controlled special agent throttling for low-efficiency workflows
  - PPD LHE-saving policy for Monte Carlo campaigns
  - new low-pileup campaigns
  - pileup ratio rule / disk retention handshake
  - high-pileup sample specs
  - HPC resources status (Bridges2, Anvil, NERSC)
  - Submission Infrastructure report (high-priority group, CRAB overflow concurrency limit)
  - 32-core job site assignment / desired site list
---

# Computing Operations Meeting

## Summary

The transcript is a partial excerpt of a recurring CMS Computing Operations meeting, starting mid-discussion. Most of the meeting is chaired by an unidentified speaker (Zoom label `[354/1-016]`, possibly a phone/room bridge representing one or more participants; not confidently attributable to a single named person). The group continued a prior discussion on how to investigate low CPU efficiency in workflows, agreeing that Submission Infrastructure (SI) should mainly cross-check its efficiency observations against numbers already reported by PPD rather than independently digging into root causes, and revisited the existing practice of throttling known low-efficiency workflows through a "controlled special agent." Sitian Qian gave a PPD contribution report covering delayed-workflow cleanup, a move toward not saving certain event files by default for Monte Carlo campaigns, new low-pileup campaigns, and a proposal to make the pileup-disk-retention rule stricter to reduce case-by-case handshakes with P&R. Ajit Mohapatra gave an HPC status update (Bridges2 and Anvil as the only currently contributing resources, NERSC allocation exhausted). Marco Mascheroni gave the Submission Infrastructure report (high-priority group changes, a new CRAB overflow concurrency limit per Tier-1, and pool status: ~487,000 CPU cores at 97% scheduling efficiency), which led into an extended discussion about why 32-core jobs sometimes idle because their WMCore-assigned desired site list only includes sites without matching multicore slots, and whether the site list should be extended/handled more dynamically (similar to CRAB's overflow mechanism) rather than being a static, manually curated list.

## Decisions / Conclusions

- Reaffirmed action item from a previous meeting: SI's role is primarily to verify that its own observed workflow efficiency is consistent with what PPD has already reported/measured, not to independently investigate root causes of inefficiency (PPD and CMS overall lack the manpower for deep per-workflow investigation).
- Existing practice: workflows identified as low-efficiency are routed through a "controlled special agent" that limits how many can run concurrently, creating back-pressure intended to push workflow owners to investigate. Dmytro Kovalskyi noted this throttling likely only accounts for a small part of the overall efficiency gap (an observed ~45% efficiency / roughly factor-of-two loss), meaning some additional cause is likely contributing.
- PPD (Sitian Qian) stated they are moving forward with a policy of not saving a certain event-file type by default for all Monte Carlo campaigns (the transcript is unclear on the exact term, transcribed as "LD"/"LHE thing" — possibly LHE/Les Houches Event files). The principle of not saving by default was stated as settled; analysis teams that need these files must explicitly tell PPD in advance or they will not be kept. How this applies to a category referred to in the transcript as "highways" (unclear, possibly "high-pileup" campaigns) was still being debated.
- A historical hard-coded list in Unified marking sites offering more than 16 cores (which included PIC — transcribed as "pick" — because it offered whole-node slots) has since been removed.
- Clarified technical point: HTCondor matchmaking already considers core-count requirements; if a job's desired site list includes all sites, HTCondor will only match it to sites that actually have 32-core slots available. The current idling problem for some 32-core jobs is therefore attributed to WMCore/Unified assigning a desired site list restricted to sites where the required input data is staged, some of which lack 32-core (whole-node) slots — not to a HTCondor-level restriction.
- No final decision was reached on how to dynamically extend/adjust desired site lists for multicore jobs; the group agreed this needs further discussion, and that HTCondor/CRAB-style matchmaking logic (e.g., the job router / `condor_qedit`-based extension CRAB already uses for overflow) should not be reimplemented inside Unified.

## Action Items

- [ ] Create a Jira issue describing how PPD wants requests exceeding the pileup ratio rule to be handled, so P&R can follow up offline — Sitian Qian
- [ ] Converge on exact resource specs (memory, core/"store" counts) for the new nominal-pilot high-pileup sample requests this week, then submit them — Sitian Qian / PPD
- [ ] Double-check whether 32-core jobs failing to match sites is caused by fragmentation of large pilots or by job priority being too low to grab new pilots — Marco Mascheroni
- [ ] Follow up offline (Marco Mascheroni and the computing-coordination side) on the right technical approach for more dynamic desired-site-list assignment for multicore jobs, and check whether an existing Jira ticket already covers this
- [ ] For next week/Thursday, compile a comparison of SI-observed efficiency vs. PPD-reported validation efficiency for a set of sizable, high-impact workflows (selected by absolute wasted CPU/CPU-hours, not simply lowest efficiency percentage, since ranking by efficiency alone would surface only small/low-impact jobs)

## Discussion

### Workflow CPU efficiency vs. PPD numbers
The group discussed how to investigate workflows with low CPU efficiency. One proposed method: take an example job from a high-impact (largest absolute wasted-CPU) low-efficiency workflow, and use timestamps in its log file to break down time spent in startup, CMSSW execution, and stage-out. This alone cannot distinguish whether time attributed to CMSSW came from remote vs. local reading or from job-internal inefficiency, but comparing several jobs' read-source information could help disentangle this. It was suggested the P&R team would need to do this deeper log analysis.

Dmytro Kovalskyi reiterated the agreed approach from a previous discussion: first check whether SI's observed efficiency for a workflow is consistent with what PPD has already reported (PPD already measures efficiency and, in some cases, has already approved running a workflow despite acknowledging it is inefficient). If SI's numbers match PPD's, that is considered sufficient — deeper investigation is a matter of policy/manpower CMS does not currently have. The existing lever available is the "controlled special agent," which throttles low-efficiency workflows to create back-pressure on workflow owners. It was noted this throttling mechanism likely explains only a small part of the overall efficiency shortfall (~45%, roughly a factor of two), implying something else is also contributing.

A practical obstacle was raised: PPD's validation efficiency numbers are not currently available in Grafana and would need to be extracted from McM (transcribed variously as "MCM"/"MCC") and integrated into the dashboard — described as not very hard technically, but not guaranteed to happen soon given competing backlog (notably finalizing the new Unified dashboard and other WM work). As an interim step, Dmytro suggested manually comparing a handful of requests to sanity-check that nothing is fundamentally wrong. It was agreed that for the next discussion (Thursday), rather than ranking by lowest efficiency percentage (which would surface small/low-impact jobs), workflows should be selected using a size/CPU-hours threshold so the comparison focuses on sizable workflows with real impact (absolute wasted CPU hours).

### PPD contribution report (Sitian Qian)
- The list of "delayed" workflows was reported as mostly workflows actually sitting in validation, not truly delayed; PPD thanked SI/P&R for keeping the list clean and for actively following up on "three queues" related to Monte Carlo samples.
- PPD is moving forward with a policy of not saving a certain file type by default for all Monte Carlo campaigns (transcribed as "LD," likely LHE, though this is uncertain). Analysis teams that want these files retained must proactively tell PPD, or they will not be kept. How this applies to a campaign category transcribed as "highways" (possibly high-pileup campaigns) was still being worked out.
- PPD plans to open new campaigns, including a dedicated low-pileup campaign (in two parts: one complementing an existing tool, another designed for 2026 running), with a pilot/test expected within a day or so.
- PPD raised the idea of making the pileup-disk-retention policy (currently: a request cannot exceed roughly twice the on-disk pileup dataset size before requiring a case-by-case discussion) stricter, to reduce the frequency of handshake discussions with P&R. Sitian asked whether P&R could provide historical data on how often/by how much requests exceed this threshold to help inform a better rule. The `[354/1-016]` speaker noted SI could provide historical monitoring of how often the limit is bypassed (estimated at roughly every 3 months or less often) but that deeper analysis would require more effort.
- Sitian gave randomized parameter-scan workflows as an example that doesn't fit the current per-request rule well: technically one big workflow, but actually composed of many small sub-workflows.
- The `[354/1-016]` speaker suggested that comparing campaign JSON fields (fractional-on-disk flag, event/sample sizes) against McM event counts could provide a relatively easy automated check; Sitian agreed this is doable and noted PPD already has some scheduled checks, though a known loophole exists — a processor can request an extension of an existing request to effectively bypass the rule, which would be hard (but not impossible) to detect automatically.
- On high-pileup samples (transcribed as "high pilot"): PPD asked the requesting analysis team for exact resource specs (memory, core/"store" counts) to avoid resource-mismatch problems recurring, and expects to converge on these numbers within the week before submitting a new set of requests. PPD asked that the existing high-pileup sample requests be finalized soon, since they are valuable input for a group referred to as the "PF"/particle-flow-related algorithm study group (exact name unclear in the transcript). Sitian also gave a general reminder that other pending workflows exist and PPD will try to flag which ones are genuinely urgent (needed within a day or two).

### HPC report (Ajit Mohapatra)
Only two HPC resources are currently contributing: Bridges2 and Anvil. A third resource had not been receiving allocation for roughly the past two to three weeks; a ticket was filed but has not yet received a response, though some resources appeared starting around July 4th (visible in the reported plot). Bridges2/Anvil has a scheduled maintenance downtime the following day, with most nodes reserved for it, causing an expected temporary drop in available resources; it is expected to recover once maintenance completes. The other four HPC sites, including NERSC, are reported as effectively done/exhausted for their current allocations, with no news yet on a supplemental allocation for NERSC.

### Submission Infrastructure report (Marco Mascheroni)
Marco reported a personal issue prevented a wiki update this cycle (no action item, informational only) and mentioned a prior cooling issue with no action taken. Three users were added to a high-priority group; this required some manual babysitting of jobs in the system but was completed successfully. SI also enabled a concurrency limit for CRAB overflow: when CRAB jobs are rerouted to sites outside their original desired site list after sitting idle too long (e.g., jobs needing to read MiniAOD remotely at Tier-1s that instead run at other sites), a limit now caps how many such jobs can run concurrently per Tier-1, to avoid excessive remote-reading load on any single Tier-1. Pool status: approximately 487,000 CPU cores in the global HTCondor pool, with 97% scheduling efficiency.

### 32-core job site assignment
Following up on an earlier discussion from a computing coordination meeting, the group discussed how 32-core jobs get assigned to sites. Current understanding: job-to-site assignment (the desired site list) is controlled by Unified/WMCore, and HTCondor's matchmaking operates within that list. The `[354/1-016]` speaker asked whether, mid/long-term, jobs could instead be submitted to the global HTCondor pool and matched automatically to sites with sufficient cores, rather than relying on a curated whitelist.

Marco clarified that HTCondor's matchmaking already accounts for this: if all sites were included in a job's desired site list, HTCondor would only match it to sites that actually have 32-core slots — this is technically already possible on the HTCondor side. CRAB already does something similar for its overflow mechanism, dynamically extending the desired site list for idle jobs via HTCondor's job router (effectively a periodic `condor_qedit`-style update), rather than a purely static list.

Dmytro questioned why any manual list management should be needed at all — if a job needs 32 cores it should simply match whatever site has them — and initially worried this could indicate fragmentation of large pilots preventing 32-core matches, or an unnecessary restriction somewhere in submission infrastructure. It was clarified that in the specific case under discussion, the affected jobs had their input data staged only at sites lacking 32-core (whole-node) slots, so their desired site list was correctly restricted to those sites by WMCore — meaning the jobs were idling due to data locality, not a HTCondor-level problem. It was recalled that a previous hard-coded workaround in Unified (treating sites offering more than 16 cores as viable, which included PIC for its whole-node slots) has since been removed.

The group agreed Unified's assignment logic likely needs to be more dynamic at assignment time to avoid assigning jobs to sites where they cannot actually run, while being careful not to duplicate HTCondor's own matchmaking logic inside Unified. It was noted that for MC (non-data) workflows this input-placement constraint doesn't apply, and that making remote reading the default could sidestep the issue in some cases. No conclusion was reached; the group agreed to discuss the correct technical approach with Marco offline, and asked whether an existing Jira ticket already tracks this.

## Open Questions

- What accounts for the majority of the observed overall efficiency shortfall (~45%, roughly a factor of two) if throttling of already-known low-efficiency workflows via the controlled special agent is only a small contributor?
- Is the idling of some 32-core jobs caused by pilot fragmentation, insufficient job priority to grab newly available 32-core pilots, or purely by restrictive desired site lists driven by data placement? (Marco to check.)
- Is there an existing Jira ticket covering dynamic desired-site-list assignment for multicore jobs?
- How can the pileup-ratio disk-retention rule be redesigned (or made stricter) to reduce case-by-case handshake overhead between PPD and P&R, including handling edge cases like randomized parameter-scan workflows composed of many small sub-workflows?
- How exactly should the "no [LHE?] saved by default" policy apply to the campaign category referred to in the transcript as "highways" (unclear term, possibly high-pileup campaigns)?

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[CRAB]] · [[WMCore]] · [[CMS]] · [[Monitoring]] · [[Pilot Jobs]] · [[HPC]] · [[PPD]] · [[McM]] · [[Unified]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-06 17.33.27 Computing Operations Meeting`)
