---
type: meeting
date: 2026-07-30
participants:
  - Marco Mascheroni
  - Luis Simas
  - Stephan Lammel
topics:
  - CRAB schedd overload / production drain
  - group surplus configuration
---

# Submission Infrastructure Weekly Meeting (2026-07-30, early segment)

## Summary

This is a short transcript covering the opening minutes of the 2026-07-30 Submission Infrastructure Weekly Meeting, before a gap in recording (a separate, later transcript from the same day, already captured in [[2026-07-30-Submission-Infrastructure-Weekly-Meeting|the continued meeting note]], picks up a few minutes later). The group discussed a message — attributed to Stephan Lammel, transcribed inconsistently as "Stephanus"/"Stefan" — reporting that [[CRAB]] schedds were overloaded and not recovering, and discussed possible mitigations, including capping the number of jobs and disabling the "group surplus" [[HTCondor]] negotiator configuration.

## Decisions / Conclusions

- Marco Mascheroni and Luis Simas agreed, as an immediate mitigation, that the "group surplus" configuration should be disabled to reduce load and let the overloaded CRAB schedds recover. (The later, continued meeting note for this same day records this as an established decision, consistent with this discussion.)

## Action Items

None identified.

## Discussion

### CRAB schedd overload and production drain

- Luis raised a message (in the SI Mattermost channel) reporting that CRAB was having problems; Marco confirmed he had seen it and agreed the situation was bad.
- Marco proposed putting a hard cap on the overall number of jobs — i.e., not replacing completed jobs with new ones — as a way to let the system "breathe."
- Marco raised disabling the "group surplus" configuration as a possible mitigation; Luis agreed this could work, and Marco confirmed: "disable the group surplus."
- When Stephan joined the discussion, Marco summarized that the issue was Stephan's message about needing to cap CRAB jobs because CRAB schedds were "not coping and not recovering."
- Stephan explained the CRAB schedds got overloaded due to a production "train" (Marco referred to it as a production "drain," transcript unclear whether these refer to the same event) that day.
- Marco expressed confusion/surprise that this could happen, arguing there should already be a limit on the number of running jobs per schedd, and that CRAB should instead receive submission refusals, or have jobs held/queued, rather than the schedds becoming overloaded.
- Luis suggested that the configured limits might simply be set too high, since they are now being hit "on average" (exact meaning unclear in the transcript).
- The transcript ends mid-sentence, with Marco noting that production was "coming back," before cutting off.

## Open Questions

- Why CRAB schedds do not already enforce a hard limit on running jobs sufficient to prevent overload during a production drain/train event (i.e., why submission refusal or queuing did not kick in as expected).
- Whether the existing job/limit configuration on CRAB schedds is set too high, as suggested by Luis.

## Related

[[CRAB]] · [[HTCondor]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-30 16.05.42 Submission Infrastructure Weekly Meeting`)
