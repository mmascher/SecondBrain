---
type: meeting
date: 2026-08-13
participants:
  - npigoux
  - Alan Malta Rodrigues
  - Marco Mascheroni
  - Héloïse Joffe
topics:
  - DIRAC/DiracX in-progress pull request review
  - CI failure blocking a pull request, caused by an unrelated prior commit
  - Workflow for pull requests depending on other unmerged pull requests; GitHub "stacked pull requests" feature
  - Documentation update for the "direct task submit" command (three-phase ticket)
  - S3 "direct download" method in DIRAC — open question on reuse vs. new implementation
  - Start of a backlog triage / planning-poker session (transcript ends abruptly)
---

# DIRAC/DiracX In-Progress Review and Backlog Triage Meeting

## Summary

npigoux led this DIRAC/DiracX status meeting, going through a list of in-progress tickets/pull requests one by one and checking for comments or blockers, similar in structure to other meetings in this series. As in prior meetings, part of the discussion involved a speaker captured only under the Zoom label `[EP 2/R-014]`, addressed during the meeting as "Christophe"/"Chris"; consistent with earlier notes in this corpus, this label reads as a room/endpoint identifier rather than a confirmed individual, so it is not listed as a named participant above. Alan Malta Rodrigues raised a CI failure blocking one pull request and a question about the expected workflow when a pull request depends on another unmerged pull request, which led to a discussion of GitHub's newly added "stacked pull requests" feature. Marco Mascheroni reviewed a documentation pull request (adding the "direct task submit" command to the docs) and had it assigned to Chris for review. npigoux raised an open question about whether an existing "direct download" method in DIRAC (used for S3-based storage) should continue to be reused or needs a new implementation. Héloïse Joffe gave a brief status update on a pull request nearing readiness for review. Near the end, npigoux said Alexander had asked him to run a short backlog triage/planning-poker session; the group began discussing the first item (related to S3-type staging and CTA during some activity), but the transcript ends abruptly mid-sentence before any estimate or outcome was recorded.

## Decisions / Conclusions

- The Copilot-suggested documentation addition for a pull request was agreed to be committed: the docs should note that the "direct task submit" command can also be called directly, not only via the existing "call" command. The distinction discussed: "call" is a live/interactive execution, while "submit" is a scheduled execution carried out through a worker. Chris was assigned as reviewer. Marco Mascheroni noted this is phase one of a three-phase ticket: phase one is this documentation update, phase two is updating the Helm charts, and phase three is removing backward-compatible support for the old command.
- On the pull request blocked by an unrelated CI failure: the proposed fix discussed was to "relax" something in the repository configuration and then re-trigger the tests, after which the pull request should be able to proceed. No owner was confirmed for making this fix; Alan Malta Rodrigues noted a follow-up note had been left for "Ryan and Alexandri" (spelling per transcript) a few weeks earlier, and npigoux stated he did not know exactly how to fix it.
- On the pull request with a dependency on another unmerged pull request (raised on behalf of Valentin, who could not connect to the meeting but relayed context via Mattermost, mostly through Federico): the pull request needs to use a different error exception that is being provided by Alexander in a separate, not-yet-merged pull request. The understanding reached was that the expected workflow is to wait for the other pull request to be merged, then update/rebase on top of it. Chris mentioned that GitHub recently added a "stacked pull requests" feature allowing pull requests with dependencies on other pull requests to be reviewed and tested together; he had not tried it yet but had heard positive reports. Alan Malta Rodrigues concluded the team should look into this feature to see if it helps manage this kind of situation. This was left as a proposal to investigate, not a decision to adopt it.
- Chris indicated he needed to check the status of, and finish, an item related to a "global OpenSearch prefix" (transcribed as "global open source prefix"), noting that the related "factory settings" had already been merged and that he still needed to add something following that merge.

## Action Items

- [ ] Commit the Copilot-suggested documentation change adding the "direct task submit" command, and assign Chris as reviewer — Marco Mascheroni / npigoux
- [ ] Fix the failing client tests so the pull request is ready for review — Héloïse Joffe
- [ ] Check the status of, and finish, the "global OpenSearch prefix" work now that the related factory settings have merged — Chris (`[EP 2/R-014]`)

## Discussion

### CI failure blocking a pull request
Alan Malta Rodrigues reported an unrelated CI problem blocking a pull request, caused by a commit that had been merged earlier and is breaking tests for this unrelated request. A follow-up note on this had been left for "Ryan and Alexandri" a few weeks prior, but it was unclear who would actually fix it. The suggested remediation was to relax something in the repository and re-trigger the tests. npigoux acknowledged he did not know how to fix it himself.

### Pull request dependency workflow / stacked pull requests
Alan Malta Rodrigues, relaying a question via a message from Valentin (who could not join the call), asked whether the DIRAC team has an established practice for handling a pull request that depends on another, not-yet-merged pull request — in this case, one needing a different error exception being introduced by Alexander in a separate pull request. The understanding was that the correct approach is to wait for the dependency to merge and then rebase. Chris mentioned GitHub's newly introduced "stacked pull requests" feature, which allows dependent pull requests to be reviewed and tested together; he had not used it yet but had heard it works well. Alan Malta Rodrigues suggested the team look into this feature.

### Andre/Andrea item
A separate in-progress item (associated with "Andre," not present in the meeting) was noted by Chris as waiting for a second review; apart from that, no other issues were reported for it.

### Global OpenSearch prefix
npigoux asked Chris for a status update on an item described as a "global open source prefix" (likely referring to a global prefix for OpenSearch, a topic that has recurred in other meetings in this series). Chris said he had not checked on it recently, noted that related "factory settings" had already been merged, and that he still needed to add something following that merge.

### Documentation update for "direct task submit"
Marco Mascheroni reviewed an open pull request with one outstanding comment from Copilot, suggesting that the documentation should also mention that "direct task submit" can be called directly, since currently only the "call" command is documented. Marco explained the underlying distinction — "call" is live/interactive execution, while "submit" is scheduled execution carried out through a worker — and concluded the suggestion made sense as a documentation-only addition. The group agreed to commit the suggestion and assign Chris as reviewer. Marco noted this pull request is phase one of a three-phase ticket, with phase two being a Helm chart update and phase three being removal of backward-compatible support for the old command.

### S3 "direct download" method in DIRAC
npigoux raised a question (heavily unclear in the transcript, referencing an item transcribed as "Robertoesta") about an S3-related file download used in DIRAC storage, asking whether the team should keep relying on the existing "direct download" method in DIRAC or whether it needs to be implemented elsewhere/differently. Chris responded that if it is used, it needs to be implemented. The exchange was brief and the underlying technical details are unclear in the transcript.

### Héloïse Joffe's pull request
Héloïse Joffe reported her pull request should be ready for review soon; she still needs to fix failing client tests.

### Start of backlog triage / planning poker (incomplete)
npigoux said Alexander had asked him to run a small planning-poker-style triage session on some backlog tickets. The group began with a first item, described very unclearly in the transcript as involving S3-type ("your root [bucket?]") staging and CTA (possibly CERN Tape Archive) during some activity referred to as "RNS activity" (unclear). Chris indicated he had already commented on this item. The transcript ends abruptly mid-sentence ("So what should I note...") before any estimate, conclusion, or further detail was captured.

## Open Questions

- Who will fix the CI issue blocking the pull request (caused by an earlier, unrelated merged commit)? No owner was confirmed.
- Will GitHub's "stacked pull requests" feature actually help the team manage pull requests with cross-dependencies, as hoped? Not yet tried by the team as of this meeting.
- Should the existing "direct download" method in DIRAC (used for S3-based storage) continue to be reused, or does a new implementation need to be added elsewhere? The transcript is unclear on the specifics of this item.
- What was the outcome of the planning-poker/triage session on the S3/CTA-related staging item raised at the end of the meeting? The transcript cuts off before this was resolved.

## Related

[[DIRAC]] · [[DIRACX]] · [[GitHub]]

## Source

meeting_saved_closed_caption.txt (from `2026-08-13 10.16.37 BiLD`)
