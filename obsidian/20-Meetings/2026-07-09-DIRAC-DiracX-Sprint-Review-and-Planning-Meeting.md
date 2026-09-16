---
type: meeting
date: 2026-07-09
participants:
  - Andrei Tsaregorodtsev (CNRS)
  - Simon Fayer
  - Bertrand Rigaud
  - Loris Van Katwijk
  - Ryunosuke O'Neil
  - Marco Mascheroni
  - Mazen Ezzeddine
  - Daniela Bauer
  - Jorge Lisa
  - Héloïse Joffe
  - Francesco Brivio
  - David Lange
  - Vijay
topics:
  - DIRAC/DiracX sprint review (pull requests and issues)
  - Database schema migration tooling (Alembic) and ADR process
  - Replacing MinIO with SeaweedFS
  - DiracX transformation-system sandbox default fix
  - Sprint velocity and retrospective
  - HTCondor gap/blahp vs. pilot-submission overlap
  - Next-sprint backlog refinement and availability planning
---

# DIRAC/DiracX Sprint Review and Planning Meeting

## Summary

This was a end-of-sprint review, retrospective, and next-sprint planning meeting for the DIRAC/DiracX development team. Most of the meeting was led by a speaker whose Zoom label appears in the transcript only as "[EP 2/R-014]" (which reads as a room/location label rather than a person's name); this speaker's identity could not be reliably determined from the transcript and they are not listed as a named participant above, though they conducted most of the sprint review, retrospective, and planning-poker facilitation. The team went issue-by-issue through the sprint board, covering documentation-style migration, Python-version cleanup, a long-standing TaskQueue priority bug, DiracX entry-point rewrites, OpenSearch "global topics" indexing, a large database-related pull request being deferred to a future minor release, replacing MinIO with SeaweedFS, a misrouted pull request between the DIRAC and DiracX repositories, and a DiracX transformation-system sandbox default fix nearing merge. A significant discussion concerned introducing Alembic for relational-database schema migrations and writing an Architecture Decision Record (ADR) before implementing DB migration tooling. Marco Mascheroni reported on a separate small meeting with HTCondor developers exploring whether HTCondor's "gap"/"blahp" concepts overlap with DIRAC's pilot-submission model, concluding there is no clear advantage over the current approach. The meeting closed with a sprint retrospective, a planning-poker sizing exercise for a small issue, an explanation of the backlog/sprint self-assignment process, and a round-table availability poll for the next two-week sprint.

## Decisions / Conclusions

- The docstring-convention migration (from the existing/no convention to Google style, an issue originally from Janusz) will be split into one pull request converting existing style and multiple follow-up per-directory pull requests adding missing documentation, rather than one large pull request. The original large pull request was closed for being too large. This work was moved to the next sprint.
- Simon Fayer's Python-version data-usage cleanup will be split into two pull requests: one adding the new utility (rebased and ready for review/merge) and a second, likely further split, pull request applying it across the codebase.
- The long-standing TaskQueue priorities bug fix has a ready pull request, but per Federico it needs to be tested in a production-like environment before the issue can be closed; targeted for closure next sprint.
- For the DiracX entry-points rewrite: the "charts" pull request was reviewed and merged; a second pull request in DiracX is ready to merge but is currently blocked by an unrelated failing CI.
- For "global topics" OpenSearch indexing: the DIRAC-side pull requests were merged. The DiracX-side pull request is waiting on new factory-settings work introduced during the sprint (attributed in the transcript to "PSOP"); moved to the next sprint since the person involved may be on holiday.
- A large, mostly single-author pull request involving database schema changes was marked for a future minor release (referred to as "9.2") rather than the current sprint/release, and was removed from the current sprint's plan; the group discussed but did not fully resolve how this affects near-term planning.
- Extended Resource Status System (RSS) work for a specific policy was implemented, but no review comments had been received from the relevant reviewers as of this meeting.
- For the database-migration-tooling issue (raised by "Skela" and discussed with Christophe): the underlying issue was re-scoped after the team determined the original description didn't match the implementation, the database schema needs to change, and this was judged a good opportunity to introduce **Alembic** for DB migrations. A draft pull request was opened but will be excluded from the current milestone until the team has a documented understanding of how the migration approach will work. A previous attempt (by Jorge) to introduce a migration tool had raised unresolved design questions, which is why the team decided an ADR should be written and discussed before implementation proceeds. New sub-issues were created to work toward the ADR, set up Alembic, and add CI checks that fail a pull request changing the DB schema without an accompanying migration; this issue set was not yet fully created as of the meeting.
- Regarding database migration approach generally: the group noted that adding a column in MySQL can be done as a simple online migration, but agreed to start with the most basic migration approach first rather than immediately adopting more advanced "online schema change" tooling. There was a preference expressed for keeping schema-migration SQL isolated (e.g., in dedicated files) rather than embedding SQL statements inside Python modules, based on past experience that this is hard to track. The team has no practical experience with Alembic yet; it was described as a long-standing, well-known tool in this space, and the team intends to consult Rucio (which reportedly already uses a similar migration approach and has been a source of advice for the team before) and to justify the tool choice explicitly in the ADR before adopting it.
- For MinIO → SeaweedFS: the group discovered that Bertrand Rigaud's pull request and a duplicate pull request from "Chris" addressed the same underlying fix; the team decided to use Chris's pull request instead, and Bertrand Rigaud's pull request will be closed (with a cross-reference added to the issue).
- Loris Van Katwijk's pull request was closed because the underlying GitHub issue had been filed against the wrong repository (it targeted DiracX/"Euratex" instead of DIRAC). The facilitator transferred the issue to the DIRAC repository and indicated Loris could reuse most of the existing work when redoing the pull request against the correct repository.
- The DiracX transformation-system sandbox default fix (Ryunosuke O'Neil's pull request) has had review comments addressed and is considered ready to merge pending one final review pass, assuming no failing tests.
- Regarding HTCondor's "gap"/"blahp" concepts vs. the pilot-submission model: following a separate meeting with HTCondor developers (referred to as Alexander and Jamie), Marco Mascheroni reported that, per the HTCondor developer ("Jamie"), there is no clear advantage to using blahp/gahp directly compared to the current approach of using the ARC client and the Condor client, since a client interacting with gahp/blahp would still need to implement job tracking, status retrieval, and stdout/stderr retrieval itself. The advantage of the current Condor-scheduler-based approach is a single interface/client handling multiple CE types, with Condor's own scheduler process managing submission, status tracking, and output retrieval. Marco Mascheroni proposed organizing a broader follow-up meeting (with more participants) to explore the idea further only if there is team interest; otherwise the idea will not be pursued further.
- On DIRAC/DiracX version compatibility: there is currently no need to pin a specific DiracX version against a given DIRAC version, since the DiracX RSS service is not yet mandatory in production. In a future phase (RSS "phase two"), a minimum DiracX version will be required for full RSS functionality, but sites without it will still be able to run DIRAC, simply without that newer functionality. This is not seen as a blocking issue for the current pilot phase.
- A small planning-poker exercise was run on an issue about renaming/moving an internal repository (a Boto/S3-client-like library used by DiracX, and planned for use by WMCore/"WorkCo" as well, described as recently renamed) after a dependency change (from one HTTPX-based version to another). The group's estimate converged on 1 story point (trivial), with one dissenting vote of 2.

## Action Items

- [ ] Split the docstring-convention pull request into a conversion PR plus multiple per-directory documentation PRs, and comment on the issue to record this plan
- [ ] Review Simon Fayer's Python-version-cleanup pull request (the first, utility-only PR)
- [ ] Certify the workload-time-left-for-HTCondor-at-CERN pull request
- [ ] Determine who will open the pull request for the DiracX hackathon "30-job executor" issue, and follow up with Ryan on outstanding questions — Benedict, Andrea, Camille
- [ ] Test the TaskQueue-priorities fix in a production-like environment before closing the issue next sprint
- [ ] Investigate and resolve the unrelated failing CI blocking the DiracX entry-points pull request
- [ ] Finish creating the remaining sub-issues toward the DB-migration ADR, Alembic setup, and CI schema-migration check
- [ ] Close the Bertrand Rigaud SeaweedFS pull request and link/reference Chris's pull request on the issue instead — Bertrand Rigaud
- [ ] Redo the pull request against the DIRAC repository (reusing existing work), to be reviewed afterward — Loris Van Katwijk
- [ ] Perform one final review pass on the DiracX sandbox-default-fix pull request before merging
- [ ] Talk to Alexander about which backlog issues to pick up next sprint — Marco Mascheroni

## Discussion

### Sprint review highlights
The team worked through the sprint board issue-by-issue. Notable items beyond those already captured as decisions:
- A request (attributed to the facilitator) to make sure a change works in LHCb-derived production still needs follow-up.
- The DiracX hackathon issue about a "30-job executor" was worked on by Benedict, Andrea, and Camille; it remained unclear who would submit the pull request, and there were outstanding questions for Ryan.
- In the RSS/policy area, functionality was extended so that a related manual "extension decision" step should no longer be necessary, but no confirmation had come back from the team that would validate this.

### Database schema migration and ADR process
The team agreed that before adopting a migration tool (currently expected to be Alembic) for relational schema changes in the newer ("Alamic"-managed) components, an ADR should be written to document and justify the approach, informed by a prior unsuccessful attempt (by Jorge) that raised unresolved design questions. Points raised during the discussion:
- Legacy DIRAC currently requires operators to manually run SQL commands against the database when a schema changes with a new release — a process the team wants to avoid repeating.
- The team wants schema migrations to work as "online migrations" where possible (e.g., adding a MySQL column), and agreed to start with the simplest approach rather than immediately building or adopting more sophisticated "online schema change" tooling.
- A past internal lesson learned was that embedding SQL statements directly inside Python modules is hard to track and maintain; the group expressed a preference for keeping migration-related SQL in isolated files.
- The team has no direct experience with Alembic; it was described as a long-established tool in this space, and the team plans to ask Rucio (an existing source of advice) about their experience before finalizing the approach in the ADR.

### HTCondor gap/blahp vs. pilot-submission model
Marco Mascheroni described a separate meeting he had with HTCondor developers (Alexander and Jamie) exploring the overlap between DIRAC's pilot-submission concept and HTCondor's "gap" (a resource/computing-element abstraction similar to a computing-resources section) and "blahp" (an interface to batch systems) concepts, both tied specifically to HTCondor. According to the HTCondor developer's ("Jamie's") assessment, relayed by Marco Mascheroni, there is no clear benefit to using blahp/gahp directly over using the ARC client plus the Condor client, because a client built on gahp/blahp would still need to implement job submission, status tracking, and stdout/stderr retrieval itself — work that Condor's own scheduler already handles when using the current single-interface approach across CE types. A related but distinct point was raised about a potential duplication between "pilot CE" functionality and an "internalized pool," which the group agreed would need separate discussion at another time. Marco Mascheroni proposed that, if there's broader interest, a follow-up meeting with more participants could be organized to explore the idea further; otherwise, it will not be pursued.

### Sprint metrics and round-table status
The facilitator reported the sprint had an expected/planned 5 story points and an expected velocity of 11.8 points (based on team capacity, accounting for reduced headcount during the hackathon), against an actual velocity of 6.3 points, which was characterized as "not bad." The facilitator noted the team may be systematically overestimating velocity because several of the facilitator's own long-running issues/pull requests (carrying larger story-point estimates, some pre-dating the sprint) keep rolling from sprint to sprint without resolving; this is expected to correct itself once those are finished. Round-table area updates: DIRAC — mostly RSS service work; CTA integration — nothing to report; matchmaking proof of concept — the matchmaking logic has been implemented in Python and the team can now move on to benchmarking; DIRAC maintenance — ongoing security and bug-fix work.

### Sprint retrospective
- What slowed the sprint down: issues/pull requests being filed against the wrong repository (DIRAC vs. DiracX) because the two systems are closely interconnected in the team's thinking; this happened to the facilitator (an issue meant for DIRAC was filed against DiracX) and separately to Héloïse Joffe on a REST-related issue. The team agreed to be more careful to target the correct repository going forward.
- What helped: hackathon-related practice was useful for bringing in outside expert counterparts (referenced as "Brian" in the transcript, unclear attribution).
- Risk for the next sprint: the facilitator will be on holiday, which is expected to reduce how quickly pull requests get reviewed; this was described as a known/planned risk rather than a surprise.

### Backlog process and next-sprint planning
The facilitator explained the team's backlog/planning-poker workflow: the backlog currently holds roughly 166 issues, many of which are blocked pending other work. During review meetings the team works through some issues via planning poker; once story points are assigned, issues move to the prioritized backlog. If an issue needs further refinement and the team can't converge on a solution live, it is moved to a design-discussion track to be resolved separately. From the end of this meeting until the next day ("tomorrow night"), team members can self-assign any issue from the prioritized backlog for the upcoming two-week sprint, based on their own availability and the story-point estimate, and then set it to the current sprint.

### Next-sprint availability poll
The team did a round-table poll of expected availability (as a rough percentage of working time) for the next two-week sprint: Loris Van Katwijk (~40%), Jorge Lisa (~50%), Ryunosuke O'Neil (~15–20%), Héloïse Joffe (~0%, on leave for the two weeks, present only the following day), Mazen Ezzeddine (~10%), Andrei Tsaregorodtsev (~10%), Simon Fayer (~0%, rounding down from a small remaining task), Daniela Bauer (~0%), Vijay (~20%), Marco Mascheroni (~10%, still to be coordinated with Alexander on specific tasks), Francesco Brivio (~0%, still new to the area), and David Lange (~0%). Other availability figures mentioned in the transcript (e.g., for "Federico" and other participants) were too unclear or ambiguously attributed to record reliably.

## Open Questions

- Who will submit the pull request for the DiracX hackathon "30-job executor" issue, and what questions remain for Ryan?
- Is the large, DB-related pull request deferred to "9.2" fully scoped, and what is its path back into a future sprint?
- Will Rucio's experience with schema-migration tooling (and Alembic specifically) confirm it as the right choice before the ADR is finalized?
- Is there sufficient team interest to justify a broader follow-up meeting on the HTCondor gap/blahp vs. pilot-submission overlap?
- Will the CI failure blocking the DiracX entry-points pull request be resolved, and is it definitely unrelated to that pull request's own changes?

## Related

[[DIRAC]] · [[DIRACX]] · [[HTCondor]] · [[Pilot Jobs]] · [[Workload Management]] · [[OpenSearch]] · [[Rucio]] · [[WMCore]] · [[CERN]] · [[CNRS]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-09 10.04.06 BiLD`)
