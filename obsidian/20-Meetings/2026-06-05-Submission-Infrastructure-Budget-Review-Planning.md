---
type: meeting
date: 2026-06-05
participants:
  - Scarlet Norberg
  - Duong Nguyen
  - Marco Mascheroni
topics:
  - USCMS budget review preparation
  - Submission infrastructure staffing and effort levels
  - Factory operator funding risk (Jeff Dost)
  - Scale testing results (jobs, cores, scheduler memory)
  - DIRAC/DIRACX scale-test implications
  - Budget review slide planning
---

# Submission Infrastructure Budget Review Planning

## Summary

Scarlet Norberg and Duong Nguyen met with Marco Mascheroni to prepare for a USCMS budget review scheduled for around July 28th (less than two months out). The meeting covered a review of current submission-infrastructure effort/staffing, a report on this year's scale testing (jobs/cores capacity, scheduler memory constraints, idle-job scaling, and the "Uber pilots" factory test mechanism), the implications of the upcoming DIRAC/DIRACX transition for future scale testing, a precautionary discussion of staffing risk if factory operator Jeff Dost's funding were lost, and an agreement on how Marco should structure forward-looking material (past-year accomplishments and next-year plans) for the budget review document.

## Decisions / Conclusions

- Marco Mascheroni's assessment is that the current level of effort is sufficient to keep submission infrastructure running and evolving. He described the current effort as: ~0.5 FTE for factory operations at CERN (Luís Simas, referred to as "Lewis" in the transcript), Jeff Dost's OSG-side factory work, one FTE currently being replaced (Florian, the main front-end operator, who is leaving — referred to variously as "Florence"/"Floridian" in the transcript), and Marco himself at 50% operations (factory + global pool operations, plus some management) and 25% on new-WM development (in the area led by Kevin Lannon).
- This year's overall-pool scale test confirmed the system can handle 800,000 running jobs (~3 million cores, using an average of ~8 cores/job), consistent with results already demonstrated a couple of years earlier.
- The central manager is a single point that cannot scale horizontally and remains the critical constraint; schedulers scale horizontally but are deliberately not scaled out indefinitely (some vertical scaling is preferred to limit hardware cost).
- The main scaling constraint is memory: ~2MB per running job.
- New this year: idle-job scaling was tested (requested by Tier0). Idle jobs are inexpensive — millions of idle jobs can be held in a single scheduler's queue — and this was confirmed to be well above what Tier0 required. Condor's late-materialization feature (queuing jobs without materializing them in scheduler memory/disk) reduces resource consumption further.
- The factory-side scale test used an "Uber pilots" mechanism, where one pilot spawns multiple partitionable slots, allowing the full chain (central manager, schedulers, factory) to be scale-tested using real grid worker nodes without wasting resources.
- In an earlier, separate evaluation (with Andrea) of CMS's revamped workflow-management options (Panda, DiracX, and the CMS-led revamp/microagent prototype), Marco estimated the current hardware (2TB RAM across schedulers) could support ~500,000 running jobs (2 million cores) with the microagent-based approach running on schedulers, or up to ~800,000 running jobs (3 million cores) without that added overhead — consistent with the pool-wide scale-test figure. Slides for this evaluation are linked in a recent quarterly report.
- Marco stated that, assuming only failed hardware is replaced (no additional hardware purchased), the current infrastructure should be adequate for the High-Luminosity LHC era.
- DiracX's transformation system (the component that would functionally replace the CMS workflow agent) has not been written yet; Marco could not say what scale testing DiracX itself will require, since this depends on whether DIRAC-side processes will need to run on the schedulers and how aggressively DiracX queries/submits compared to the current system.
- On the hypothetical scenario of losing Jeff Dost (raised as a precautionary, not actual, concern — see Open Questions): for CMS, the impact would be comparatively contained since the Fermilab and CERN(-managed) factories would remain, but operations would be strained, with Marco and the CERN operator absorbing more work and losing time for other tasks; the group agreed the main loss would be expertise in testing new glideinWMS releases and debugging factory issues. There are three factories in total — one in Kubernetes/OSG infrastructure ("Tiger," managed by Jeff Dost), one at Fermilab (backup infrastructure, managed by Hyunwoo Kim, referred to as "Hanbu"/"Han Woo" in the transcript), and one managed by Marco — with shared access across all three but dedicated ownership. It was unclear who would take over running the OSG-side (Tiger) factory if Jeff Dost left.
- Duong Nguyen raised a knowledge-concentration risk; Marco agreed that, unlike the pool (where Antonio also has deep knowledge), factory expertise would then be concentrated in Marco alone.
- Marco's stated broader concern is less about a specific funding loss and more about the standard ~2-year CERN operator-rotation model: a strong operator's departure could be followed by a less experienced replacement, causing a dip in quality — a general risk independent of any specific funding scenario.
- For the budget review document, the group agreed on a two-slide structure: one slide/section summarizing what was accomplished in submission infrastructure over the past year, and one forward-looking slide/section on plans for the next year (with the understanding that priorities may shift, as they already have relative to last year's stated plan). Marco stated that for next year, the new WM (DIRAC/DIRACX integration) will be the key focus area for submission infrastructure.

## Action Items

- [ ] Review this year's write-up/document, and prepare the forward-looking budget-review material — a slide/section on what submission infrastructure accomplished in the past year and one on plans for next year (highlighting, per Duong Nguyen's suggestion, increased effort on the interaction between the new WM and submission infrastructure) — and send it to Scarlet Norberg and Duong Nguyen within about two weeks — Marco Mascheroni

## Discussion

### Effort and staffing review

Scarlet Norberg opened the review by asking how the past year went and whether effort had been sufficient. Marco described submission infrastructure as a well-consolidated, solid area, and detailed the current effort breakdown (see Decisions above). He noted CMS is also separately involved with OSG factory effort via Jeff Dost.

### Scale testing

Scarlet asked about progress on stress-testing the system to confirm it can handle the rate needed for the High-Luminosity LHC era — something she and Duong ("Zhuang" in the transcript) had been asking about for a couple of years, noting earlier conversations had focused on getting management buy-in and then figuring out an approach. Marco reported the pool-wide scale test results and the new idle-job/late-materialization testing (see Decisions). He also referenced an earlier, separate evaluation of CMS's revamped workflow-management proposal (done with Andrea, covering Panda, DiracX, and the CMS-led/microagent option), whose slides are linked from a recent quarterly report.

### DIRAC/DIRACX and future scale testing

Duong Nguyen asked whether the DiracX prototype expected in the next few months (installation/testbed work) would be full-scale tested against the factory. Marco said he was not comfortable committing to that, since DiracX's transformation system does not exist yet — only the older DIRAC version has one. He explained his mental model of DIRAC as having two main blocks: a workload manager (equivalent to Condor/glideinWMS) and a transformation system (equivalent to the CMS agent). Independent of which system runs in front (agent, DiracX, or a new microagent-based solution), submission and per-job resource usage figures (2MB/running job, 800,000 running jobs) should still apply, unless DIRAC needs to run additional processes on the schedulers, which is not yet known. Marco proposed, as an idea rather than a firm plan, designing scale tests independent of whatever orchestration layer sits in front — e.g., measuring how many Condor queue queries and how many `condor_submit` operations the infrastructure can sustain (noting 1 million idle/dematerialized jobs is a very different test than 1 million individual submissions) — to establish limits that don't depend on the specific system. Scarlet noted this could be testing to plan for next year, without committing to it.

### Staffing/funding risk scenario (Jeff Dost)

Scarlet raised, as a hypothetical planning exercise ahead of the budget review, what would happen if Jeff Dost's funding were lost. She explained this is prompted by some funding (e.g. IrisHEP-related) that is ending or rippling to other funding sources in the next couple of years, as multi-year grant cycles come to an end — she was explicit that nothing is confirmed or imminent, and that USCMS is simply starting to ask these questions in preparation for the budget review, so it can advocate for effort and plan for both negative (funding loss) and positive (additional FTE) scenarios. Marco described Jeff Dost's deep experience running the OSG factory and testing/finding bugs in new glideinWMS releases, and discussed the impact of losing him (see Decisions). Duong Nguyen asked about knowledge concentration risk and how the team could recover in a worst-case scenario; Marco reiterated the loss of factory expertise and raised the operator-rotation risk as his broader concern.

### Presentation logistics and next-year planning for the budget review

Duong Nguyen asked Marco to review the document reflecting what was accomplished this year (noting some planned bullets from last year's document were not completed, replaced instead by other priorities — Marco confirmed this is normal, as priorities shift) and to think about content for next year. Duong framed the purpose of these slides as convincing stakeholders that submission infrastructure has significant ongoing activity and needs at least maintained, ideally increased, effort — specifically suggesting more effort be highlighted around understanding the interaction between the new WM and submission infrastructure. Marco agreed and confirmed the new WM (DIRAC/DIRACX integration) will be the key focus for next year.

Separately, Marco mentioned that Luís Simas ("Luis") is presenting at next week's Wednesday general/OSG meeting on pilot-monitoring overload work and on finalizing last year's submission-infrastructure work; Marco is working with Luís on that talk but may not be able to attend live himself, since he has a conflicting talk at the Throughput Computing Week event in Madison the same week. Marco described Luís as the new factory operator (started in March) who is already doing a good job, and wanted to give him the opportunity to present.

## Open Questions

- What scale testing, if any, DiracX itself will require — depends on whether DIRAC-side processes will need to run on the schedulers and how aggressively DiracX will query/submit compared to the current system; explicitly unresolved and described by Marco as still "brainstorming."
- Whether IrisHEP or other funding sources tied to current submission-infrastructure staffing (the scenario behind the Jeff Dost discussion) will actually be renewed or pivot — not known; Scarlet said these questions are only starting to be asked ahead of the budget review.
- Who would take over running the OSG-side (Tiger) factory if Jeff Dost left — raised by Marco, not resolved.

## Related

[[CMS]] · [[OSG]] · [[HTCondor]] · [[glideinWMS]] · [[DIRAC]] · [[DIRACX]] · [[Kubernetes]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Workload Management]] · [[Jeff Dost]] · [[Luís Simas]] · [[Hyunwoo Kim]] · [[Florian Von Cube]]

## Source

meeting_saved_closed_caption.txt (from `2026-06-05 15.23.10 Scarlet Rachel Norberg's Personal Meeting Room`)
