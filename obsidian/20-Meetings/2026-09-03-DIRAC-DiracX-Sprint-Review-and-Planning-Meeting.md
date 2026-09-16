---
type: meeting
date: 2026-09-03
participants:
  - Andrei Tsaregorodtsev (CNRS)
  - Marco Mascheroni
  - Janusz
  - Loris Van Katwijk
  - Héloïse Joffe
  - Mazen Ezzeddine
  - Hideki MIYAKE
  - Todor
  - Dhiraj kalita
topics:
  - DIRAC/DiracX sprint review (pull requests and issues)
  - Crypto dependency version issue affecting tests
  - 404-page fix
  - OpenSearch multi-document upserts and "global prefix" indexing
  - Docstring convention / REST-regression pull request (Janusz)
  - Security-advisory handling process
  - Resource Status System (RSS) progress
  - Sprint velocity and retrospective
  - Job attributes vs. job parameters architecture (MySQL vs. OpenSearch)
  - Local development environment and OpenSearch requirement
  - DiracX InterSeed evaluation
  - Next-sprint planning, meeting-time change, and availability poll
---

# DIRAC/DiracX Sprint Review and Planning Meeting

## Summary

This was an end-of-sprint review, retrospective, and next-sprint planning meeting for the DIRAC/DiracX development team, structurally similar to other recurring sprint meetings in this series. As in other meetings in this series, most of the dialogue in the transcript is attributed to a speaker label "[EP 2/R-014]", which appears to be a room/device label rather than an individual; this facilitator's identity could not be reliably determined and they are not listed as a named participant, though they drove the sprint-board review, retrospective, and planning. The transcript quality is poor in places — several exchanges (particularly ones attributed to Janusz) are transcribed as isolated, apparently unrelated single words, and are treated here as unreliable rather than interpreted.

The team went issue-by-issue through the sprint board, covering: a buggy version of a crypto dependency affecting unit tests (to be pinned/fixed the same day); a fix for a broken 404 page; OpenSearch multi-document upsert support (in progress, assigned to Valentin(e), who went on a week's vacation starting the day of the meeting); a "global prefix" convention for OpenSearch indexes needing a small fix for consistency between DIRAC and DiracX; a multi-phase command/chart pull request from Marco Mascheroni moved to the next sprint; a docstring-convention/REST-regression pull request from Janusz, with a plan to split the work into an "ignore" pull request followed by a docstring pull request; and the team's process for handling security advisories (private forks, restricted disclosure, and known drawbacks such as no CI on private-fork pull requests). Loris Van Katwijk and Héloïse Joffe gave status updates on RSS-related work. The facilitator then reported the sprint's velocity/availability metrics and a per-area summary of sprint accomplishments (DIRAC bug fixes, chart/OpenTelemetry fixes, documentation-link fixes, a matchmaking proof-of-concept prototype, and general DIRAC maintenance), followed by a retrospective and a discussion of moving the following week's meeting to accommodate holidays.

A substantial technical discussion, prompted by Marco Mascheroni, covered the architectural distinction between job attributes (stored in MySQL, schema-defined, needed before a job starts) and job parameters (stored in OpenSearch, dynamic/schema-less key-value pairs uploaded by the job once it starts running, originally introduced to enable fast searching that MySQL key-value lookups could not support efficiently). This connected to a separate discussion about whether the local development environment ("run local"/"local start") should be able to run OpenSearch, given that a dummy job executor (built during a hackathon) currently fails locally because it depends on OpenSearch to update job status — the facilitator preferred to wait for a clearer use case, partly because a fix to remove that OpenSearch dependency was believed to exist already but may not have been merged. The meeting closed with round-table reporting on next-sprint availability, including a status update from Dhiraj kalita on drafting an ADR for an analytics-related workload, and a note that Alexander (from an organization transcribed as "Newton") will spend part of the next several months evaluating DiracX's "InterSeed" concept.

## Decisions / Conclusions

- A buggy version of a crypto library dependency was affecting unit tests for everyone; an issue had reportedly been opened upstream, and if it isn't picked up promptly the team will just pin/fix the version themselves — this was to be done the same day (not later than today).
- Marco Mascheroni's item on multiple pull requests for a "time management" feature was not finished this sprint; he plans to split the work into several single-change pull requests to keep review manageable, and the item moves to the next sprint.
- The broken 404 page (ticket attributed to "Uraj"; spelling uncertain) is fixed — the fix used an existing environment variable rather than the originally anticipated path rewrite, and 404-page assets are now displaying correctly.
- A request/execute "agent process pool" issue (the transcript is unclear on the exact name) is not specific to LHCb but most likely only affects LHCb in practice; plan is to test first, then fix.
- OpenSearch multi-document upsert support is in progress (Valentin(e)); reviewed the day before the meeting but needs further changes. Valentin(e) started a week's vacation the day of this meeting (per Marco Mascheroni), so the item moves forward accordingly.
- A "global prefix" concept for OpenSearch indexes, already implemented for DIRAC, was reviewed for DiracX and needs one minor fix so that DIRAC and DiracX use the same prefix convention (an extra underscore had reportedly been added between the global prefix and the index prefix on the DiracX side); considered an easy fix.
- Marco Mascheroni's multi-phase pull request (Phase 1: new command, Phase 2: chart changes, reviewed; Phase 3: also opened) is moved to the next sprint — Phase 3 must wait until the Phase 2 chart changes are merged, and Marco Mascheroni still needs to address review comments (including a typo) and test the charts.
- For Janusz's docstring/REST-regression work: the facilitator assessed that a GitHub feature Janusz wanted to use "a few weeks" old would not work for this case, and instead proposed a two-step plan — open a pull request that adds an "ignore" entry, then a follow-up pull request built on top of it that adds the missing docstring and removes the ignore. Janusz agreed to try this approach.
- Security advisories are not discussed in this (public) meeting. The team's process: a private fork is created for a reported security issue, fixes are developed as pull requests within that private fork (which notably has no CI), and the fork is eventually merged back into the main repository once ready; disclosure happens only once the fix is finalized, communicated via the team's mailing list or, sometimes, a more restricted group. The facilitator noted they find this process nerve-wracking given the lack of CI on private-fork pull requests, and that a previous, separate, more restricted repository was used for security tracking a few years ago before adopting GitHub's built-in security-advisory system.
- An item attributed to someone referred to as "Meta" (name/identity unclear from the transcript) was set aside because that person is on holiday, reportedly through the end of the month, returning in October (confirmed by Loris Van Katwijk).
- Héloïse Joffe reported her RSS-related work is essentially finished, having corrected an issue raised the day before; the facilitator will do one more review pass. Loris Van Katwijk's related RSS work will depend on functions Héloïse Joffe wrote, and the facilitator will review Loris Van Katwijk's work afterward.
- Sprint metrics were reported as velocity of 13 and availability of 7.8, described as "not so far from the expected one" (the transcript is unclear on whether "13" was the expected or actual velocity).
- Sprint accomplishments reported by the facilitator: a fix for a 500 error on the jobs-metadata endpoint; a fix for an issue in the OIDC token endpoint; a "renewal" script fix; reference-chart fixes and a fix for an OpenTelemetry issue; charts made more configurable; documentation-link fixes. Nothing to report for CTA integration this sprint. For the matchmaking proof of concept: the Python prototype and a log-testing framework are done, and the next step is implementing what was transcribed as a "Redis clustering" solution (exact term uncertain). DIRAC maintenance saw a number of bug fixes and performance-related improvements.
- Retrospective: less availability than expected during the sprint was attributed to unspecified "preparations" and other work, without further detail captured in the transcript. A risk flagged for the next sprint is reduced availability due to upcoming holidays for some team members, plus an unspecified reference to "the electric[al]" (unclear). The team discussed moving next week's regular Thursday meeting to Wednesday (tentatively around 9–10, exact time ambiguous in the transcript) to avoid a conflict with a "team operations" meeting at 11 and to work around the holiday; this was tentatively agreed and expected to also work for most CMS-side participants.
- For next-sprint goals: continue cleaning up existing issues, though the team feels it is "reaching the end of the easy issues to solve" in the DIRAC repository, with many remaining issues being harder to pick up. The team wants to write Architecture Decision Records (ADRs), hopefully for the transformation system and possibly for something referred to as "CWA" (unclear). A roadmap draft is to be published soon; a previous roadmap document was removed because it was outdated (it assumed the transformation system would be done first), and a new roadmap draft is being prepared.
- For RSS: the goal for next sprint is to finish "phase two" (described as the integration phase), if possible.
- For matchmaking: the goal is to finish an item referred to as "properties" (unclear). The team confirmed there is an informal, not-yet-documented sequence of further phases (7, 8, 9, 10) expected as integration work continues.
- A service (the transcript is unclear on which one, transcribed ambiguously as existing "in graphics") was confirmed to exist and was merged a few weeks prior, but is not yet installed in the DIRAC certification instance; getting it into certification will likely require using a "dev" image there.
- A task that had not gone through the normal refinement process (because it was done by "Robin") was discussed; whoever is assigned it can direct questions to the facilitator. The facilitator committed to ensuring someone is assigned to this task for the next sprint.
- RSS completion also depends on "Condor"/an unclear name and on Stella, who was not present; the facilitator will follow up with them directly.
- Marco Mascheroni raised whether he could open GitHub issues for developer-experience improvements, specifically: allowing `local start` to run an OpenSearch server, because a "dummy job executor" (built during a hackathon and already merged) fails under `local start` since it depends on OpenSearch to update job status. The facilitator confirmed this is the right process (open an issue/discuss) but noted it depends on the size of the change.
- On why OpenSearch is needed for this case: submitting a job causes the dummy job executor to update job status, which in turn also updates OpenSearch. The facilitator recalled that during the hackathon this was a known issue with an available fix (attributed to Benedict) to avoid using OpenSearch in this path, but that fix may not have made it into the merged code because a different pull request (Andrea's) was merged instead. The facilitator will check the relevant executor code (referred to as the "ninja executor"; exact name uncertain) to confirm whether it still sets job status via OpenSearch.
- Job attributes vs. job parameters: job attributes are stored in MySQL, are schema-defined, and are largely (though not entirely) assigned at job submission time — some attributes, like job status, do change during the job's lifetime. Job parameters are stored in OpenSearch as dynamic, schema-less key-value pairs uploaded by the worker node once a job starts running; they were moved off MySQL originally because MySQL-based key-value search was reported as very slow without proper indexing, and OpenSearch enabled fast search (e.g., searching quickly by job owner) as well as building dashboards/visualizations. Andrei Tsaregorodtsev summarized: job attributes are parameters every job is expected to have; job parameters are dynamic, arbitrary key-value pairs that may or may not be present, and are not necessarily known in advance.
- The facilitator agreed to double-check whether the "set job status" functionality could have its dependency on job parameters (and therefore OpenSearch) removed, since status conceptually belongs to job attributes rather than job parameters.
- On adding OpenSearch to the local dev environment: unlike MySQL (for which SQLite can be substituted in a lightweight dev setup), there is no lightweight local equivalent for OpenSearch. Ideas discussed (not decided) included a `local start --with-opensearch` flag that would either start an OpenSearch Docker container or detect and use a locally installed OpenSearch binary via environment variables. The facilitator's conclusion was to wait for an actual concrete use case before implementing this, partly because the plan to remove the job-parameter/OpenSearch dependency from the job-status path would reduce the need. It was also noted that developers can already point `local start` at an existing local OpenSearch installation via environment variables.
- Valentin(e)'s availability for next sprint was set to 0% due to vacation.
- Alexander (affiliation transcribed as "Newton"; spelling/affiliation uncertain) is going to work on evaluating whether DiracX's "InterSeed" concept could be used in something referred to as "the vertex" (unclear), over the next roughly six months. Their availability was discussed in light of upcoming research/thesis-report deadlines, converging on roughly 30%, with a specific upcoming week unavailable due to the start of official research documentation.
- Dhiraj kalita reported he is in the early stages of drafting an ADR related to analytics work; he plans to circulate a first draft (to the facilitator and to Todor, among others) by Monday for comments, ahead of an upcoming "workshop" (transcribed elsewhere in the corpus as involving DIRAC; here transcribed ambiguously as "Iraq worship" — likely a mis-transcription of "DIRAC workshop").
- Next-sprint availability poll (approximate, as reported): facilitator ~30%; Loris Van Katwijk ~20%; Héloïse Joffe ~30%; Mazen Ezzeddine ~10%; Andrei Tsaregorodtsev ~10%; Todor ~10%; Dhiraj kalita low/unclear; Alexander ~30%; Marco Mascheroni ~10% (potentially ~20% if his proposed OpenSearch/local-dev work is picked up); Hideki MIYAKE reported low availability without a clear percentage; Benedict had no confirmed availability (expected back from school the following week, no clearance yet); several other reported percentages (e.g., for "Federico" and "Janusz") were too unclear in the transcript to record reliably.

## Action Items

- [ ] Pin/fix the buggy crypto dependency version affecting unit tests (same day as the meeting)
- [ ] Open a pull request adding an "ignore" entry, followed by a second pull request adding the missing docstring and removing the ignore — Janusz
- [ ] Perform one final review pass on Héloïse Joffe's RSS-related work
- [ ] Review Loris Van Katwijk's RSS-related work after it is submitted
- [ ] Address outstanding review comments (including a typo) and test the charts on the multi-phase command/chart pull request — Marco Mascheroni
- [ ] Ensure someone is assigned to the task originally done by Robin for the next sprint
- [ ] Follow up with Stella (and/or "Condor"/unclear name) about finishing RSS-related work
- [ ] Open a GitHub issue/pull request for allowing `local start` to run with OpenSearch, and check whether the "ninja executor" (name uncertain) still requires OpenSearch to set job status
- [ ] Double-check whether the "set job status" function's dependency on job parameters (OpenSearch) can be removed
- [ ] Publish a draft of the new project roadmap
- [ ] Circulate a first draft ADR on analytics work for comments (to the facilitator, Todor, and others) by Monday — Dhiraj kalita

## Discussion

### Job attributes vs. job parameters
Prompted by Marco Mascheroni's questions about DIRAC's architecture, the group clarified the distinction between job attributes and job parameters. Job attributes live in MySQL, are schema-defined, and are largely fixed at submission time, though some (such as job status) change during the job's lifetime. Job parameters live in OpenSearch, are schema-less dynamic key-value pairs uploaded once a job starts running on a worker node, and were moved to OpenSearch originally to support fast search (e.g., by job owner) and visualization/dashboarding, since equivalent key-value search in MySQL was reported to perform very poorly without proper indexing. Andrei Tsaregorodtsev summarized the conceptual distinction: attributes are parameters every job is expected to have, while parameters are arbitrary and not guaranteed to exist for a given job. The facilitator agreed some metadata (notably job status) currently exists in both places and should really only live in job attributes; a prior, partially-completed effort to remove such duplication was referenced.

### Local development environment and OpenSearch
Marco Mascheroni raised that the hackathon-built "dummy job executor," now merged, fails under the local development environment (`local start`) because it depends on OpenSearch to update job status, and OpenSearch is not available locally. He asked about the right process for proposing developer-experience work like this (open a GitHub issue first). The facilitator recalled a hackathon-era fix (attributed to Benedict) to avoid this OpenSearch dependency that may not have survived a later merge of a different pull request (Andrea's), and committed to checking. Options discussed for adding local OpenSearch support (a `--with-opensearch` flag on `local start`, using a Docker container, or detecting a locally installed OpenSearch binary via environment variables) were not adopted; the facilitator preferred to wait for a clearer use case, especially since removing the OpenSearch dependency from the job-status path might make the local-OpenSearch feature unnecessary.

### Security advisory handling
The facilitator described, at a general level, how the team handles reported security issues: a private fork is created, fixes are developed there as pull requests (without CI, which was flagged as a source of concern), and the fork is merged back into the main repository once ready, with disclosure following via the mailing list or a more restricted group only after the fix lands. This was explicitly kept out of the public meeting's agenda for specifics. The team previously used a separate, more restricted repository for tracking such issues before moving to GitHub's built-in security-advisory workflow.

### Meeting schedule change
Due to upcoming holidays affecting attendance the following Thursday, the group discussed and tentatively agreed to move the next occurrence of this meeting to Wednesday (time was discussed as around 9–10, with some confusion in the transcript about the exact hour relative to a "team operations" meeting at 11); this was expected to also suit most CMS-side participants.

## Open Questions

- Was the reported crypto-library issue picked up upstream, or did the team need to pin the version themselves?
- Will the fix removing OpenSearch dependency from the "set job status" path be found/restored, and does it still apply after subsequent merges?
- What exactly is the item referred to as "CWA" that may also get an ADR?
- What is the unclear reference to "the electric[al]" as a risk for the next sprint?
- Was the exact time for the rescheduled (Wednesday) meeting finalized?
- What is the "vertex" system that Alexander will investigate for possible InterSeed use, and what would adopting InterSeed there involve?

## Related

[[DIRAC]] · [[DIRACX]] · [[OpenSearch]] · [[Workload Management]] · [[CNRS]] · [[CMS]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-03 10.10.59 BiLD`)
