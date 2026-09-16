---
type: meeting
date: 2026-04-14
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Hyunwoo Kim
topics:
  - GitHub access for OSG factory repo
  - CMS entry overloading configuration fix
  - glideinWMS 3.11.4 / ITB Dev revival
  - HTCondor front-end upgrade at Fermilab
  - Factory repo cleanup
---

# OSG Factory Ops Meeting

## Summary

A short meeting. Marco Mascheroni gave a quick update before leaving early (he was helping a colleague, Luis, move apartments), covering a CMS entry-overloading configuration fix and a GitHub access request. Hyunwoo Kim gave an update on the Fermilab front-end's HTCondor 3.11 upgrade status. The group also discussed plans to test glideinWMS 3.11.4, the status of two autoconf bug fixes Jeff Dost had reported, and cleanup of unused items in the OSG factory repository. Jeff Dost mentioned he had been working reduced hours this week due to a back injury.

## Decisions / Conclusions

- The entry-overloading configuration fix is not a functional change: many entries were simply missing the overloading parameter entirely, which was causing monitoring problems.
- Jeff Dost confirmed it is fine to remove `get_tarballs.py` from the factory tools, since it appears to be a leftover from earlier prototyping and is no longer used.
- The Condor 10 series can be removed from the CMS entry configuration, since CMS no longer uses it. Jeff Dost noted this is separate from whether the Condor 10 series can be removed from the OSG factory more broadly, which he was unsure about.

## Action Items

- [ ] Grant Marco Mascheroni collaborator/GitHub access needed to open PRs in the OSG factory repository (possibly via adding him to an OSG GitHub group) — Jeff Dost
- [ ] Revive the ITB Dev setup to test glideinWMS 3.11.4 without risking the main ITB environment — Marco Mascheroni
- [ ] Investigate the still-unknown front-end bug (possibly CMS-specific) using the revived ITB Dev setup — Marco Mascheroni
- [ ] Test the second autoconf fix (untested as of Friday) before/during the 3.11.4 release candidate testing — Marco Mascheroni
- [ ] Remove `get_tarballs.py` from the factory tools — Marco Mascheroni
- [ ] Remove the Condor 10 series from the CMS entry configuration — Marco Mascheroni

## Discussion

### CMS entry overloading fix and GitHub access

Marco Mascheroni had made fixes to entry configurations related to overloading for CMS entries and wanted to open a PR in the OSG factory repository for code review, but lacked collaborator access on GitHub. Jeff Dost said he would look into granting access, possibly by adding Marco to an OSG GitHub group. Two new entries had also been deployed to production the previous week, with Marco working with site admins on new entries generally.

### Fermilab front-end HTCondor 3.11 upgrade

Hyunwoo Kim reported that Nick had upgraded HTCondor on Fermilab's backup front-end machine, but testing would require a failover to that machine to confirm nothing is broken; this failover was expected soon. Jeff Dost noted that Nick could reach out via the OSG Slack if he needed help debugging, since the Fermilab front-end connects to the OSG factory (the "tiger factory" as referenced in the transcript).

### glideinWMS 3.11.4 and ITB Dev

Marco Mascheroni said "Mark" (transcript unclear on exact name/role) was expected to cut a 3.11.4 release candidate on Friday, though Marco had not cross-checked whether that happened. Marco's goal for the week was to revive the ITB Dev setup (separate from the main ITB, which is used for testing new entries and other activities) so that testing 3.11.4 would not risk breaking the environment used for other testing — this had happened before, when ITB was broken for a couple of weeks and had to be rolled back.

A bug that Florian had tested and logged (referenced by ticket number, not stated in the transcript) had already been hot-patched on the CMS front-end; Marco suggested it makes sense for Hyunwoo Kim's side to simply wait for 3.11.4 rather than hot-patching, since the fix should be included there. A second, still-unidentified bug — possibly specific to the CMS setup — remains to be investigated once ITB Dev is revived.

### Autoconf bug fixes

Jeff Dost asked about two autoconf bugs he had previously reported, and whether fixes for both would make it into 3.11.4. Marco Mascheroni said one fix was tested carefully and confirmed working. The other fix existed but had not been tested because it was completed late on a Friday, so it did not make the release candidate in time. Per "Mark," the untested fix could still be added and tested during release-candidate testing, since it is a standalone script; if it turns out broken, it would be fixed in a subsequent release candidate rather than needing to be re-added from scratch.

### Factory repository cleanup

Marco Mascheroni raised two cleanup items:
- An apparently-unused `get_tarballs.py` script in the factory tools, which Jeff Dost believed was left over from earlier prototyping work and approved removing.
- The Condor 10 series, which Jeff Dost confirmed is no longer used by CMS and can be removed from the CMS entry configuration; he was uncertain whether it could also be removed more broadly from the OSG factory.

There was also a brief, unclear exchange about a related file that could "no longer be found," possibly tied to an older OS version (transcribed as "Jacintos 7," likely a mis-transcription — possibly CentOS 7) in connection with a move to a newer OS. The transcript is too garbled to reliably determine what was decided here.

## Open Questions

- Whether the still-unidentified front-end bug Marco Mascheroni plans to investigate is specific to the CMS configuration.
- Whether the Condor 10 series can be removed from the OSG factory more broadly (beyond the CMS-specific configuration).
- The exact nature of the additional file/config item discussed at the end of the meeting regarding an older OS version — the transcript is unclear.

## Related

[[OSG]] · [[CMS]] · [[HTCondor]] · [[glideinWMS]] · [[Factory Operations]] · [[Factory Configuration]] · [[GitHub]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-14 17.06.39 OSG Factory Ops Meeting`)
