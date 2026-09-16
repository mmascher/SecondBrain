---
type: meeting
date: 2026-07-16
participants:
  - Andrei Tsaregorodtsev (CNRS)
  - Jorge Lisa
  - Loris Van Katwijk
  - Marco Mascheroni
  - martynia
  - Francesco Brivio
topics:
  - DIRAC/DiracX backlog grooming and planning poker
  - Documentation of the DIRAC/DiracX repository structure
  - Removing Boto from DIRAC repositories (S3-like sandbox storage)
  - Making the Redis parameter mandatory for DiracX tasks
  - Renaming the DiracX "tasks run" command/script
  - Job-attribute-overwrite bug potentially related to Rucio
---

# DIRAC/DiracX Backlog Grooming and Planning Poker Session

## Summary

This was a [[DIRAC]]/[[DIRACX]] backlog grooming meeting in which the team went issue-by-issue through several backlog tickets, discussed their scope, and estimated them using a planning-poker-style voting round (referred to in the transcript, likely due to transcription error, as a "round of pocket language"). As in other meetings in this series, most of the facilitation was done by a speaker captured only under the Zoom label `[EP 2/R-014]`, which reads as a room/endpoint label rather than an individual; their identity could not be reliably determined from this transcript. Andrei Tsaregorodtsev addressed this facilitator directly as "Alexander" at the start of the meeting, but this attribution is not treated as confirmed here since the label could represent more than one person. Topics covered: documentation of the link between DIRAC and DiracX repositories, removing the `Boto` library from remaining DIRAC repositories, making a `Redis` parameter mandatory for DiracX tasks, renaming the DiracX "tasks run" command, and a reported bug where job-attribute-setting functionality is silently disabled under certain conditions. Marco Mascheroni, participating as a newcomer to the DIRAC/DiracX codebase, asked clarifying questions about how to vote and about what specific commands/tools do, which shaped some of the estimation discussion.

## Decisions / Conclusions

- For the documentation task (explaining the repository structure and the role of a component that links DIRAC and DiracX, transcribed unclearly as "direct comments"/"direct commons"): the group agreed this explanation, or at least a link to it, should be included in the repository/documentation area newcomers reach early (discussed in relation to a "Getting Started" section on the DiracGrid.org documentation site), since the component is described as basic and relevant to both DIRAC and DiracX. It was also agreed that although the task itself is well described, a complete newcomer likely should not pick it up without at least some existing knowledge of the current architecture, given expected unknowns. No explicit final point estimate for this task was clearly stated in the transcript despite a poker round being conducted (votes called out included 1, 2, 2, 3, 3, without a stated majority afterward).
- For removing `Boto` from the remaining DIRAC repositories (identified as `Dirac` and `DiracOS2`): the group's estimate converged on a majority of **3 story points**. It was confirmed that DiracX had already replaced `Boto` with an internally developed, lighter-weight library (its exact name is unclear in the transcript) to interact with the S3-like storage used for job sandboxes, and that the same replacement should now be applied to the remaining DIRAC repositories. The change was described as close to a mechanical drop-in replacement, except for one function that performs a direct file download, which is not available in the replacement library and requires refactoring to instead sign a URL and issue a GET request against it. Marco Mascheroni initially voted 5, citing the ramp-up needed as a newcomer (installing DIRAC, learning the sandbox-handling code, no prior experience with `Boto` or the replacement library); after the facilitator pointed out that changes can be validated via CI without running tests locally, Marco revised his estimate downward, and the group settled on 3.
- For making the `Redis` parameter mandatory for DiracX tasks: the group's estimate converged on a majority of **2 story points**. The conclusion was that `Redis` should no longer be treated as optional (`None`)/should become a mandatory parameter, and that conditional checks in the code handling a `None` Redis value should be removed as dead code. It was noted there might be additional test-mocking code exercising the `None` case that would also need updating, though this was not confirmed.
- For renaming the DiracX "tasks run" script/command to "Dirac Tasks" (the original name was judged poorly chosen): the group agreed this requires a multi-step, backward-compatible rollout rather than a single change, because the DiracX CI uses the DiracX Helm chart to run its tests, and the Helm chart in turn uses the DiracX command being renamed — a circular dependency that would break CI if changed in one step. The agreed sequence: (1) add the new command name in DiracX while keeping the old name working as well, (2) update the Helm chart to support both names, (3) once merged and tagged, switch the chart to use the new name, and (4) drop the old name in a subsequent DiracX release. Francesco Brivio summarized this as "3 steps," which the facilitator confirmed. The facilitator proposed a point estimate of **2**, and Marco Mascheroni agreed.
- Process clarification: issues estimated during this grooming session go into the backlog but are not automatically part of the current sprint. Once an issue has a story-point estimate, it appears in the "prioritized backlog" rather than the current sprint board, from which team members can later pick it up for a future sprint.

## Action Items

None identified.

## Discussion

### Documentation of the DIRAC/DiracX repository link
The group discussed a documentation backlog item concerning the overall repository structure, in particular a component (unclear in the transcript, called "direct comments" or "direct commons") described as making "the link" between DIRAC and DiracX and relevant to both. There was discussion of where such documentation belongs given it spans both projects, with a preference toward surfacing it early for newcomers (e.g., near or referenced from a "Getting Started" page on the DiracGrid.org site). A specific repository on DiracGrid.org was mentioned in connection with this. The group discussed whether a newcomer could take this task and concluded that, despite the documentation area being generally well described, someone with at least some familiarity with the current architecture should probably take it, since unknowns could come up.

### Removing Boto from remaining DIRAC repositories
For context, DiracX previously used `Boto` to interact with the S3-like storage backing job sandboxes. `Boto` was considered heavy and included many unneeded features, so the team developed a lighter-weight internal library and replaced `Boto` with it inside DiracX. The remaining work is to apply the same replacement in the `Dirac` and `DiracOS2` repositories. The change is largely mechanical — finding references to `Boto` and replacing them with the equivalent calls in the new library — except for a direct-file-download function that has no equivalent in the new library; that case requires signing a URL and then issuing a separate GET request, which was described as "almost mechanical" rather than purely mechanical since it needs some refactoring. There was some back-and-forth about whether an S3 storage-element implementation elsewhere in the codebase still depends on this direct-download behavior from `Boto`, or whether it already relies on signed URLs; this was not conclusively resolved in the discussion. martynia asked whether existing tests would need to be modified; the facilitator did not believe so, since this is considered internal/implementation-level code, but acknowledged uncertainty.

### Making the Redis parameter mandatory for DiracX tasks
The task concerns DiracX tasks that use `Redis`. Currently the `Redis` parameter can apparently be `None`/optional; the team's understanding is that it should instead be a mandatory parameter, since `Redis` is now always expected to be present. The task was described as simple: remove the `None` default and any conditional code branches that handle a missing/`None` Redis value, since they would become dead code. martynia questioned the removal of the `None`-handling condition; the facilitator clarified that the condition is only being removed because `Redis` is no longer expected to ever be `None` in practice.

### Renaming the DiracX "tasks run" command
The backlog item concerns a script/command currently named in a way referencing "ZRAX"/DiracX tasks (transcription unclear), which the group agreed should be renamed to something like "Dirac Tasks" since the current name is not accurate — the command is an internal framework process that picks up items from the message queue (backed by `Redis`) and executes them; it is not a user-facing command. Marco Mascheroni, who had previously looked for documentation on this command without success (having assumed it was a user command), asked the facilitator to explain what it does; the facilitator confirmed it runs as part of the infrastructure and pointed to existing documentation under the Administrator Guide, in a "how-to tasks" section. The rename itself was said to require three small, low-risk, one-line-style pull requests across DiracX and the associated Helm chart repository, without deep knowledge of the Helm charts being strictly necessary, since a given DiracX version is tied to a specific Helm chart version/tag.

### Backlog/sprint process
In response to a question from Marco Mascheroni (addressed to "Alexa," likely the same unidentified facilitator), it was clarified that items being triaged/estimated in this meeting go into the backlog rather than being automatically scheduled into the current sprint; once story-pointed, they move into a "prioritized backlog" view from which they can be picked up in a future sprint.

### Reported bug: job attributes silently overwritten
Near the end of the meeting, a backlog item was introduced (addressed to someone named "Ryan," who is not otherwise identified by a speaker label in this transcript) described as related to [[Rucio]] (name uncertain in the transcript, transcribed as "Rakuten"). The reported behavior: in one of the "governance" examples, the function responsible for setting job attributes is being completely overwritten to do nothing, so operations on job attributes silently have no effect if a certain component (transcribed unclearly, possibly "Goblins"/"Dublins") gets loaded. It was suggested that something in how a component referred to as "Pixie" sets up the default environment is pulling in this unwanted component. Creating a separate environment for the problematic component was mentioned as something that appears to work around the issue, and the behavior was said to be reproducible. This portion of the transcript is heavily garbled and several terms could not be reliably identified; no clear decision or assignment was captured for this item.

## Open Questions

- Whether an existing S3 storage-element implementation still relies on `Boto`'s direct-download functionality, or already uses signed URLs — not resolved in the discussion.
- Whether additional test-mocking code needs to change as part of making the `Redis` parameter mandatory.
- What the confirmed root cause and fix are for the job-attribute-overwrite bug discussed at the end of the meeting; the relevant portion of the transcript is unclear and several technical terms could not be reliably transcribed.
- No explicit final point estimate was captured for the documentation task, despite a poker round being conducted.

## Related

[[DIRAC]] · [[DIRACX]] · [[Rucio]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-16 10.23.46 BiLD`)
