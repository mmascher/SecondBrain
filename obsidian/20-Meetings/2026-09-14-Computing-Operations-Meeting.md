---
type: meeting
date: 2026-09-14
participants:
  - Kirill Ivanov
  - Marco Mascheroni
  - Liz Sexton-Kennedy
  - Ajit Mohapatra
topics:
  - HTCondor 24/25 upgrade testing
  - WMAgent certificate handling
  - ReqMgr2 / WMStats access issue
  - GPU workflow at NERSC
---

# Computing Operations Meeting

## Summary

The available portion of this meeting covered three separate operational topics: ongoing testing of the [[HTCondor]] 24-to-25 upgrade against [[WMAgent]] and its uncertain relationship to X.509 certificate handling, an access problem with [[ReqMgr2]] / [[WMStats]] reported by Ajit Mohapatra, and a GPU test workflow at [[NERSC]] that had been stuck for about a week to ten days. The transcript begins mid-conversation and ends mid-sentence, so it does not cover the full meeting.

## Decisions / Conclusions

- No firm conclusion was reached on the cause of the HTCondor 24/25 upgrade issue. It initially appeared to correlate with WMAgent 0.8 (new certificates) on Condor 25, but recent communication with Hyun Woo suggested the issue may instead be related to a "condor user" configuration, unrelated to certificates. Further investigation was described as still needed.

## Action Items

- [ ] Create tickets to coordinate an automated way to update their submission agents ahead of the current HTCondor version's end of life — Kirill Ivanov
- [ ] Test the Condor 25 / WMAgent issue by replicating it with a direct `condor_submit` (instead of the full agent); offered privately by Marco Mascheroni and accepted by the Fermilab team ([354/1-016])
- [ ] Follow up offline on the ReqMgr2 / WMStats access problem — Ajit Mohapatra

## Discussion

### HTCondor 24 → 25 upgrade and WMAgent certificate handling

Kirill Ivanov noted pressure to update their submission agents (transcribed as "firm agents") because of an upcoming HTCondor end-of-life, and that an automated update process is needed; tickets will be created to coordinate this. The exact end-of-life date for the previous version was not known precisely — Marco Mascheroni estimated "probably end of October" — which a Fermilab-side participant ([354/1-016]) said meant the update should happen as soon as possible.

Liz Sexton-Kennedy noted this coincides with the release of Condor version 26, and raised a concern originating from the facility-ops meeting: it had not been confirmed there that the issue was understood, and there was concern that it might involve X.509 certificate handling between the schedd (transcribed as "SCED") and the worker node — which would be a problem if Condor changed that behavior.

The Fermilab-side participant explained that they are currently testing at Fermilab: Condor 24 and Condor 25 are each being tested against WMAgent 0.3 (old certificates) and WMAgent 0.8 (new certificates). Initially the issue was observed only with WMAgent 0.8 on Condor 25, which suggested a certificate-related cause. However, based on recent email exchanges with Hyun Woo, the issue was reported to involve a "condor user" and may be unrelated to certificates after all, leaving the root cause unclear and requiring more investigation.

Marco Mascheroni offered to help test the issue directly via `condor_submit` — replicating what the agent does internally — rather than running the full WMAgent, and asked to be contacted privately.

### ReqMgr2 / WMStats access issue

Ajit Mohapatra reported being unable to access ReqMgr2 and WMStats on cmsweb (hostname unclear in the transcript), receiving what appeared to be an authorization error, and said this happened from both Firefox and Chrome and from both Linux and Mac. He noted the services appeared to be working for other people. A Fermilab-side participant ([354/1-016]) was not aware of a general issue, though another unidentified participant indicated they were having a similar problem. Ajit said he would follow up offline. The Fermilab-side participant noted that a ticket can be opened for this kind of issue and that they would help.

### GPU test workflow stuck at NERSC

Ajit Mohapatra relayed that a colleague, Harris, had asked for help tracking down why a test workflow (relval-based) intended to run on GPUs at NERSC had been injected into ReqMgr2 but had not run for about a week to ten days. Because Ajit could not himself access ReqMgr2/WMStats to debug this, he had suggested Harris contact "PNR" (unclear reference in the transcript) for help, but was unsure whether she had done so. He asked whether someone else could reach out to her. The Fermilab-side participant again pointed to opening a ticket as a way to get help tracking the issue.

## Open Questions

- Whether the HTCondor 24/25 upgrade issue observed with WMAgent 0.8 is actually related to X.509 certificate handling, or is a separate "condor user"-related issue as suggested by Hyun Woo.
- The cause of the authorization/access error Ajit Mohapatra (and at least one other participant) experienced with ReqMgr2 and WMStats.
- Whether Harris's stuck GPU relval workflow at NERSC has since been followed up on with the appropriate support contact.

## Related

[[HTCondor]] · [[WMAgent]] · [[ReqMgr2]] · [[WMStats]] · [[NERSC]] · [[GPU]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-14 17.15.32 Computing Operations Meeting`)
