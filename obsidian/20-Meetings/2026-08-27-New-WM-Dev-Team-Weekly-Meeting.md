---
type: meeting
date: 2026-08-27
participants:
  - Andrea Piccinelli
  - Valentin Kuznetsov
  - Kevin Lannon
  - Marco Mascheroni
topics:
  - Roundtable news and vacation schedule
  - Requirements meeting planning and McM (Monte Carlo Management) involvement
  - Andrea Piccinelli's transition out of the convener role
  - Proposal for a centralized WM documentation/recipe repository
  - Upcoming workshop registration and call for contributions
---

# New WM Dev Team Weekly Meeting

## Summary

The transcript captures only the opening roundtable/news portion of this weekly meeting; it ends mid-sentence partway through a reminder about an upcoming workshop, so later agenda items (if any) are not recorded.

A meeting lead (much of this segment's content is attributed to a room/connection label, `[EP 40/R-C10]`, rather than to a named individual, though context indicates at least part of it was spoken by Andrea Piccinelli) opened with roundtable news: upcoming vacation/travel overlapping with the "Iraq" workshop (transcription unclear — possibly a mistranscribed workshop name) and the CMS Offline and Computing week, mentioned by Valentin Kuznetsov as affecting his availability. For the requirements meeting, the group noted the agenda is very full and that someone from McM (Monte Carlo Management) should be invited to discuss McM-related topics; a job-splitting session was mentioned as scheduled for Wednesday morning. A reminder was given that a discussion involving Federico (subject unclear in the transcript) and a chat about DAS/DBS with Diego were planned for roughly two weeks out, with plans to eventually present that work at the CMS Offline and Computing week.

This was announced as Andrea Piccinelli's last meeting as convener after two years in the role; Andrea thanked the group and the collaborators worked with over that time. Kevin Lannon thanked Andrea on behalf of the group for their contributions over the past two years.

Andrea then raised a proposal (flagged as something they had meant to bring up the previous week as well): to create a single shared place to store procedures, deployment scripts, and other WM-related material as it is developed — including short-lived items — modeled on the existing CI/CD pipeline, templates, and GitLab-based setup used for "Dublin core" (transcription unclear). Examples mentioned as candidate content included Marco's HTCondor proof-of-concept work, a "balancing" deployment item, and an investigation by Vijay (transcription of the specific tool/topic, rendered as "cwlet," is unclear). The intent described was a lightweight, low-friction shared space — not a tightly governed system, but also not an unstructured dumping ground — with merge-request-based contribution access, that could also be used to bring in existing baseline documentation and support interaction with the DIRAC group and other teams. The proposal received supportive responses: a speaker (room label) called it "a good plan," particularly useful for keeping documentation up to date when interacting with other groups, and suggested starting by setting up a basic landing area/structure rather than a full systematic effort, since sufficient effort for the latter is not currently available. Marco Mascheroni supported the idea as a way to consolidate currently scattered recipes in one place, and suggested a two-step approach: first centralize the fragmented documentation as-is, then evolve it into a more structured form that better tells the story of the work.

The meeting lead then moved to a next agenda item, noting there was no particular additional news beyond a reminder about an upcoming workshop: registration would remain open until the end of September, some people had already registered, and Federigo (or Federico — spelling unclear) had noted that anyone wanting to propose a contribution/presentation should let the organizers know so a time slot can be arranged. The lead suggested the team should think about what to propose to present and discuss there. The transcript ends at this point, mid-sentence.

## Decisions / Conclusions

- The group responded favorably, without recorded objection, to the proposal to set up a single shared place (modeled on the existing GitLab/CI-CD-based setup used elsewhere) for WM-related procedures, deployment scripts, and documentation, with a lightweight/low-friction structure and merge-request-based contributions. The transcript indicates an intent to begin at least with a basic landing structure, given limited available effort for a fully systematic effort at this time; it is not clear from the transcript that a formal decision with an owner or timeline was made.

## Action Items

None identified.

## Discussion

- Requirements meeting: the agenda was described as very full; there was a wish to bring in someone from McM to discuss McM-related topics, and a job-splitting session was mentioned as planned for Wednesday morning.
- A reminder was given of a planned discussion involving Federico (topic unclear in the transcript) and a chat about DAS/DBS with Diego, expected roughly two weeks out, with the intent to eventually present related work at the CMS Offline and Computing week.
- Andrea Piccinelli's departure from the convener role after two years was announced, with acknowledgements to collaborators; Kevin Lannon thanked Andrea on behalf of the group.
- Proposed centralized WM documentation/recipe repository: modeled on an existing GitLab CI/CD pipeline and template setup ("Dublin core" — transcription unclear); intended to hold procedures, deployment scripts, and other material including short-lived items; candidate content mentioned included Marco's HTCondor proof-of-concept, a "balancing" deployment item, and an investigation by Vijay (specific subject unclear, transcribed as "cwlet"); intended to be lightweight and not overly strict, but also not an unstructured dump; access via merge requests.
- Marco Mascheroni proposed a two-phase approach: first consolidate scattered recipes/documentation in one place, then later restructure it into a more coherent, structured form.
- Workshop reminder: registrations open until end of September; a call for proposed contributions/presentations was relayed (attributed to Federigo/Federico), with a suggestion that the team think about what to propose to present.

## Open Questions

- What the team wants to propose to present/discuss at the upcoming workshop was raised as something to think about, but not resolved in the recorded portion of the meeting.
- The transcript ends mid-sentence; any further agenda items, decisions, or conclusions from the remainder of the meeting are not available.

## Related

[[CMS]] · [[Workload Management]] · [[HTCondor]] · [[CI/CD]] · [[DIRAC]]

## Source

meeting_saved_closed_caption.txt (from `2026-08-27 15.16.31 New WM Dev team weekly meeting`)
