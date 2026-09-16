---
type: meeting
date: 2026-09-09
participants:
  - Alexandre Boyer
  - Marco Mascheroni
  - Héloïse Joffe
  - Loris Van Katwijk
  - Jorge Lisa
  - Janusz
  - Todor
topics:
  - DIRAC/DiracX sprint review (pull requests and issues)
  - JobDB job-parameters-to-OpenSearch migration and MySQL removal
  - ARC/DiracX compatibility grid (needs design)
  - Kanban board terminology (needs triage vs. needs design)
  - GitHub auto-draft behavior on requested changes
  - DIRAC space-token occupancy cache removal and pull-request merge ordering
  - Security-related "prepared statement parameter" fix
  - DRSS configurable thresholds pull request
  - Global OpenSearch index prefix consistency between DIRAC and DiracX
  - GitHub "stacked pull requests" and forks
  - DIRAC task-run Helm chart pull request and CI image refresh
  - Matching logic with Redis and Lua scripts
  - Pull-request review ordering (Héloïse Joffe / Loris Van Katwijk)
  - Pilot manager service completion and Jorge Lisa's availability
  - ADR progress and roadmap/repository-map for onboarding
---

# DIRAC/DiracX Sprint Review Meeting

## Summary

This was a mid-sprint pull-request and issue review for the DIRAC/DiracX development team, led by Alexandre Boyer, who went through the sprint board item by item. Most of the technical responses came from a speaker captured in the transcript only under the Zoom label `[EP 2/R-014]`; as in other meetings in this series, this label reads as a room/endpoint identifier rather than a confirmed individual. Within this meeting it was addressed directly as "Federico" several times (including a closing remark that "Federico will host the meeting" next week), but at one point Alexandre Boyer also addressed the same speaker as "Raj" when discussing one of their pull requests — consistent with other meetings in this corpus where the same label has been addressed by different names (e.g. "Alexander," "Christophe"/"Chris"). Given this inconsistency, the speaker's identity is not treated as confirmed here and is not listed as a named participant, though they are referred to below by the names used in the transcript, in quotes.

The board review covered: a long-running pull request removing the JobDB job-parameters MySQL table (job parameters having been migrated to OpenSearch since DIRAC v9.0), which surfaced a broader open question about an ARC/DiracX compatibility grid; a pull request from Andre (absent) approved but not yet merged pending CI; a pull request from "Raj"/`[EP 2/R-014]` that had automatically reverted to draft status after requested changes; a DIRAC pull request removing space-token-occupancy-cache methods, with a discussion of merge ordering relative to a linked pull request; a security-related "prepared statement parameter" fix needing a reviewer; a DRSS configurable-thresholds pull request; DIRAC web-app report-request companion pull requests; a DiracX email-notification issue; an open question/review in progress on a global-OpenSearch-index-prefix pull request; an issue Valentin is working on with no visible progress since the last review comments; and Marco Mascheroni's DIRAC "task run" Helm chart pull request, confirmed ready to merge. The team also discussed Jan's in-progress work on matching logic using Redis and Lua scripts, and Janusz's docstring-related pull requests (this portion of the transcript is largely unusable — see note below). Alexandre Boyer laid out a review plan for pending pull requests from Héloïse Joffe and Loris Van Katwijk, and Jorge Lisa agreed to pick up the pilot-manager-service task, starting next sprint given his limited current availability. The meeting closed with status checks on Architecture Decision Records (ADRs) and a still-pending roadmap/repository-map for onboarding, before a final technical detour about Zoom's transcript/caption feature (not meeting content, omitted here).

**Transcript quality note:** the segment involving Janusz (roughly 10:23–10:29) is transcribed almost entirely as isolated, disconnected words or phrases (including several in Polish), likely due to a poor audio connection. This portion is not reliably interpretable and is only loosely summarized below.

## Decisions / Conclusions

- The ARC/DiracX compatibility issue (removing the JobDB job-parameters MySQL table from DiracX would create incompatibilities between ARC v9.0 and DiracX, since DiracX does not have the MySQL part) will be moved to "needs design" status, since the current issue description is not considered actionable. An issue already exists for this; it needs design before the JobDB-removal work can proceed on the DiracX side.
- Kanban terminology clarified (for Marco Mascheroni): "needs triage" means no one has looked at the issue yet; "needs design" means the issue has been looked at, but the description isn't accurate/complete and design work is needed before implementation can start.
- GitHub behavior clarified: when someone requests changes on a pull request, an automated process converts it back to draft status; the author (or a maintainer) has to manually mark it "ready for review" again afterward. Alexandre Boyer did this for the pull request in question.
- Merge ordering for the DIRAC space-token-occupancy-cache work: the integration pull request (referred to as "149.0"/"#87") must be merged first; only afterward can the linked V9.0 pull request (a smaller, technical follow-up needed to sort out compatibility with the first one) be merged.
- GitHub's "stacked pull requests" feature was discussed and concluded not to be usable for this team's workflow, because it currently does not work with forked repositories, and the team's contributors all work from forks.
- Review plan agreed for two pending pull requests: `[EP 2/R-014]` ("Federico") will review Héloïse Joffe's pull request first (a read-path change replacing "degraded" status handling with "active"/"banned" states, touching an FTS-related file), and only then Loris Van Katwijk's pull request, since Loris's work depends on reusing utilities from Héloïse's changes and will need to be rebased on top of it once it is merged.
- One older board item was removed from the board because it is already covered by an associated issue.
- Marco Mascheroni's DIRAC "task run" Helm chart pull request was confirmed ready: tested locally, chart bumped, and all relevant CI checks passing (an initially-concerning failing check turned out to belong to the unrelated DiracX pipeline, which was expected).
- Jorge Lisa will be assigned the pilot-manager-service pull request/task starting next sprint rather than the current one, since he currently has only about 10% availability this sprint due to additional work following his contract renewal (based in Valencia); he expects more availability next sprint and may look at the issue in the meantime.
- The team leaned toward waiting for Christophe before running backlog refinement, since several of his open issues lack sufficient descriptions and need clarification directly from him; this was not stated as a firm final decision.
- No new updates on the previously-requested Mermaid roadmap diagram or a repository/purpose map for onboarding new contributors; both remain in the backlog, and Alexandre Boyer said he still hasn't found time for them, hoping to have them ready for the DIRAC user workshop.
- No concrete timeline was given for the ADRs; work is reportedly ongoing by two contributors in their free time (unnamed in the transcript beyond "the two"), described only as more than a matter of days.

## Action Items

- [ ] Finish/merge the JobDB job-parameters-removal pull request, pending resolution of the ARC/DiracX compatibility issue — `[EP 2/R-014]` ("Federico")
- [ ] Move the ARC/DiracX compatibility issue to "needs design" on the board — Alexandre Boyer
- [ ] Merge the integration ("149.0"/"#87") pull request first, then the linked V9.0 space-token-occupancy-cache pull request — `[EP 2/R-014]`
- [ ] Review Héloïse Joffe's pull request first, then Loris Van Katwijk's — `[EP 2/R-014]`
- [ ] Rebase pull request on top of Héloïse Joffe's work and reuse her utilities, once her pull request is merged — Loris Van Katwijk
- [ ] Push current progress on the Redis/Lua-script matching-logic work by the end of the week; if unfinished, Alexandre Boyer will take over — Jan
- [ ] Look at the replacement of Next.js next week — Héloïse Joffe
- [ ] Pick up the pilot-manager-service pull request/task next sprint — Jorge Lisa
- [ ] Restart CI after the task-run Helm chart merge so new images are produced for testing (e.g. the "run demo") — Alexandre Boyer

## Discussion

### JobDB job parameters and ARC/DiracX compatibility
`[EP 2/R-014]` ("Federico") has been working on finishing a long-running pull request (started roughly a year earlier) that removes the JobDB job-parameters MySQL table, following a years-earlier migration of job-parameters content to OpenSearch, completed as of DIRAC v9.0. Removing the equivalent from DiracX raised a compatibility concern: DiracX does not currently have the MySQL part removed by this change, so ARC v9.0 would remain compatible while future DiracX versions might not be, once this change lands there too — creating the need for a documented compatibility grid between ARC and DiracX/ArcX versions. An issue already existed for this; Alexandre Boyer proposed moving it to "needs design" since its current description isn't actionable.

### Pull request review status and ordering
- A pull request from Andre (absent from the meeting) was approved by `[EP 2/R-014]` but not yet merged, pending integration and (per the transcript, unclear word, possibly "nightly") test results; Andre is reportedly aware of this dependency.
- A pull request attributed to "Raj" had automatically reverted to draft after requested changes were made on it; Alexandre Boyer explained GitHub's automated draft-on-requested-changes behavior and manually restored it to "ready for review."
- For the DIRAC space-token-occupancy-cache pull request, `[EP 2/R-014]` clarified the merge order needed across two linked pull requests (integration first, then the V9.0 technical follow-up).
- A "prepared statement parameter" pull request from Simon, described as a security-related fix, was flagged by `[EP 2/R-014]` as needing review (suggested reviewers: Christophe or Andre); no reviewer confirmed taking it on during the meeting.
- A DRSS pull request adding configurable thresholds (autonomous thresholds and fractions), updated per a request from Bert Chu, was reported by `[EP 2/R-014]` as ready to go; Alexandre Boyer said he had started but not finished reviewing it, and asked whether it had been tested in certification or the HLT rack — `[EP 2/R-014]` said it had not necessarily been certification-tested.
- DIRAC web-app "report requests" pull requests (versions 145/146) were noted as companions to the corresponding DIRAC pull requests.
- On the DiracX side, Francisco (absent) reportedly did not receive an email notification about a pull request because he was not individually a recipient; `[EP 2/R-014]` had added the team (rather than him individually) to the recipient list. Christophe is reviewing a related pull request, with an open question noted but not detailed.
- An issue Valentin is working on shows no new changes since Alexandre Boyer's last review comments were posted.
- A pull request concerning the global OpenSearch index prefix is close to ready; Alexandre Boyer noted the global prefix is currently not treated the same way in DiracX as it is in DIRAC, which needs to be checked/fixed.

### GitHub stacked pull requests and rebase workflow
During a discussion of Janusz's pull requests (transcript largely unreliable in this segment), Alexandre Boyer noted GitHub's newer "stacked pull request" feature does not work with forked repositories, and since the team works entirely from forks, it cannot currently be used to manage dependent pull requests. His stated review plan instead: review the first (base) pull request; if there are no comments, review the second; if that one is also correct, merge the second and close the base one.

### DIRAC task-run Helm chart pull request
Marco Mascheroni reported his pull request was ready: tested locally, chart bumped, tests now passing. Alexandre Boyer initially flagged a failing check, which turned out to belong to the unrelated DiracX pipeline (expected) rather than the DIRAC repository. Marco Mascheroni asked about linking the related DiracX chart issue to this pull request; Alexandre Boyer confirmed this is possible but noted a GitHub quirk — linking a pull request to an issue causes the issue to auto-close when the pull request is merged, and he was not aware of a way to change this behavior. Once merged, Alexandre Boyer said restarting CI should produce new images usable for testing (e.g. for a "run demo").

### Matching logic (Redis/Lua)
Jan reported still being in testing for the matching-logic work using Redis and Lua scripts, expecting to be done by the end of the week. Alexandre Boyer said Jan could push whatever progress exists even if unfinished, and he would take over from there if needed.

### Héloïse Joffe's and Loris Van Katwijk's pull requests
Alexandre Boyer described Héloïse Joffe's pending pull request as changing the "reading part" of some status logic — replacing "degraded" (and related) status values with simpler "active"/"banned" states. He flagged a concern about a possibly-related FTS file that used the old status values, and wanted `[EP 2/R-014]` to double-check for any issues before proceeding; `[EP 2/R-014]` agreed to look at both this and Loris Van Katwijk's pull request, in that order, since Loris's pull request needs to reuse utilities introduced in Héloïse's work and will require a rebase once it merges.

### Pilot manager service and Jorge Lisa's availability
`[EP 2/R-014]` noted the pilot manager service for "Birak"/"Birak" (unclear in transcript, likely referring to DIRAC/DiracX) is nearly finished, with only a few remaining items, including a pull request `[EP 2/R-014]` started but hasn't had time to finish. Jorge Lisa, recently returned from vacation, volunteered to take a look but reported only about 10% availability this sprint due to additional work in Valencia following his contract renewal, with more availability expected next sprint. Alexandre Boyer opted to assign the task for next sprint rather than the current one, while noting Jorge Lisa could look at the issue in the meantime if time allows.

### Refinement, ADRs, and roadmap/onboarding map
Alexandre Boyer suggested the team might need to wait for Christophe before running backlog refinement, since a number of his open issues lack descriptions and require his clarification. Marco Mascheroni asked for an ADR update; `[EP 2/R-014]` explained the delay is because the (unnamed) people working on it are doing so only when they have free time together, and it's taking a while; no concrete timeline (beyond "not just days") was given. `[EP 2/R-014]` also asked about two previously-requested items: a new Mermaid diagram roadmap, and a map of repositories and their purposes for onboarding newcomers to the community. Alexandre Boyer confirmed no progress on either — both remain a backlog issue he hasn't found time for — but said he hopes to have them ready in time for the DIRAC user workshop.

## Open Questions

- Is there a way to prevent GitHub from automatically closing a linked issue when the referencing pull request is merged? Raised by Alexandre Boyer; no known solution mentioned.
- Who, if anyone, will review the security-related "prepared statement parameter" pull request from Simon? No reviewer confirmed during the meeting.
- What exactly needs to change so DiracX's global OpenSearch index prefix is treated the same way as DIRAC's?
- Will refinement proceed without Christophe, or will the team wait for him? Leaning toward waiting, not firmly decided.
- What is the concrete timeline for the ADR work? Only described in relative terms ("not just days").

## Related

[[DIRAC]] · [[DIRACX]] · [[GitHub]] · [[OpenSearch]] · [[Redis]] · [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-09 10.03.05 BiLD`)
