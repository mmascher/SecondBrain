---
type: meeting
date: 2026-07-21
participants:
  - Marco Mascheroni
  - Luís Simas
  - Hyunwoo Kim
topics:
  - Condor CE site-token auth_method migration
  - Factory low-pilot-count alert
  - WM Agent HTCondor 24/25 compatibility
  - glideinWMS 3.11.4 testing
  - Distance-based matchmaking proposal
  - Training session follow-up
---

# OSG Factory Ops Meeting

## Summary

Luís Simas reported progress on migrating Condor CE factory entries to site-token authentication and on a new factory-level alert for sites providing low pilot capacity. Hyunwoo Kim raised a blocker upgrading WM Agent machines to HTCondor 25, since WM Agent packages do not yet work on that series; the group discussed mitigations while staying on the latest HTCondor 24 release. Marco Mascheroni gave an early, still-in-design overview of a proposal for distance-based matchmaking in glideinWMS, inspired by the Justin/DUNE tool's use of Rucio storage-element distances, which he plans to discuss further with Jamie. The group also agreed to resume a previously paused training.

## Decisions / Conclusions

- Of roughly 50 Condor CE factory entries identified for migration to site-token authentication, 15 (including RAL's entries and some Tier-2s) have successfully run test jobs with site tokens in ITB; Luís Simas will move these into production one by one.
- Two Tier-1 entries (Poland and Russia) accept the site token but their jobs remain pending rather than failing outright; the group agreed to give them more time before taking further action.
- A new factory-specific alert has been added: it compares a site's average number of running cores over the last 7 days against its current running cores, and fires when the site is providing under 30% of that trailing average. It is currently implemented as an email notification (described as a "soft" alert) because there is not yet a better mechanism for a non-noisy, tolerant alert. It already proved useful, catching a number of alerting sites the previous week.
- Because WM Agent packages do not yet work with HTCondor 25, the two currently active WM Agent machines (of six total, four of which are idle) remain on HTCondor 24 and have been upgraded to the latest 24.x release, 24.022 (confirmed released that day, July 21), which addresses a recent known vulnerability.
- HTCondor stated (per Hyunwoo Kim) that even after HTCondor 24 reaches end of life — not precisely dated on their website but expected around October/November 2026 — serious bug fixes will still be backported to 24, even though new features will not.
- Luís Simas and Marco Mascheroni agreed to resume the previously paused training, tentatively starting Tuesday afternoon (July 22), with Luís to ping Marco to settle on an exact time.

## Action Items

- [ ] Continue moving the 15 ITB-verified site-token entries into production one by one — Luís Simas
- [ ] Open tickets / follow up with site admins for the remaining ~25 sites (~30 entries, including Finland, the Rome Tier-2, and some Tier-3s) that still need the site-token migration — Luís Simas
- [ ] Talk to Katie (from RAL) about how RAL's Condor CEs are configured and working correctly in production with site tokens, to understand who to contact regarding the mapping setup on the EGI side — Luís Simas
- [ ] Look into whether a package/RPM could be distributed via EGI repositories to handle the site-token-to-Unix-user mapping, similar to how it is done via OSG repositories, instead of requiring per-site tickets — Luís Simas
- [ ] Discuss the distance-based matchmaking proposal with Jamie at tomorrow's meeting (Tuesday, 6 PM) — Marco Mascheroni
- [ ] Ping Marco Mascheroni to arrange a time to resume the training this week — Luís Simas

## Discussion

### Site-token authentication migration

Luís Simas is migrating Condor CE factory entries from the previous authentication method to site tokens. Of roughly 50 entries needing migration, 15 have successfully run test jobs against ITB using site tokens — including RAL's entries and some Tier-2s — and Luís began moving these into production one by one. Two Tier-1 entries (Poland and Russia) accept the token without rejecting it, but their jobs remain pending rather than completing; the group agreed to wait longer before investigating further. The remaining roughly 30 entries, spread across more than 20 (Luís said around 25) sites — including Finland, the Rome Tier-2, and some Tier-3s — will require tickets to individual site admins.

Marco Mascheroni raised uncertainty about how site-token-to-Unix-user mapping is managed outside OSG. For OSG sites, all relevant CEs are Condor CEs (no ARC CEs), and the mapping is handled via an RPM that site admins install from the same OSG repositories used for glideinWMS and HTCondor. For EGI-flavor sites, which use different repositories, it is unclear who manages this mapping, particularly for ARC CEs. Marco was unsure whether opening tickets individually with ~20 site admins was the right approach, versus reaching out more broadly (e.g. by email) to establish the best way to proceed. As an interim step, Luís agreed to talk to Katie (from RAL) about how RAL's CEs are working correctly in production, since she may know who else to contact. Luís also proposed, as an ideal longer-term solution, distributing a package via EGI repositories that site admins could install directly (paralleling the OSG RPM approach), which would avoid needing to open per-site tickets; Marco agreed this would be preferable to having ~20 sites each tweak their configuration individually. Luís said he would look into this.

### Factory low-pilot-count alert

Luís Simas added a new factory-specific alert that compares a site's average running cores over the trailing 7 days to its current running cores, firing when the site is providing under 30% of that average. It is currently sent as an email notification rather than a harder alert, since there isn't yet a better mechanism to express this "soft tolerance" without being noisy. The alert was exercised the previous week when a number of sites triggered it, which Luís considered a good validation of its behavior.

### WM Agent / HTCondor 24 vs. 25

Hyunwoo Kim reported that of six WM Agent machines, two are currently active (used by Gregor and colleagues, including Kirill; Muhammad has since left) and four are idle, which is considered normal. Hyunwoo wants to upgrade the WM Agent machines to HTCondor 25, but the WM Agent code does not currently work with it — Hyunwoo believes this is related to significant changes HTCondor made to its Python bindings in the 25 series. The two active machines instead remain on HTCondor 24, upgraded to the latest release, 24.022, which Marco confirmed had been released that same day (July 21) and which addresses a recently known vulnerability.

Hyunwoo noted that Gregor appears to be the only person with practical WM Agent knowledge and cannot dedicate 100% of his time to it, which limits how quickly HTCondor-25 compatibility can be fixed; the other two names Hyunwoo has seen in related email threads appear to be very new. Hyunwoo referenced a comment from the previous week (attributed to Antonio, though Marco was not fully certain that reflected exactly what Antonio meant) that if compatibility work does not progress, the group may need to ask the HTCondor team to extend the support lifetime of the 24 series. Per Hyunwoo, HTCondor has not published an exact end-of-life date for 24 but it is expected around October/November 2026, and HTCondor has stated that serious bug fixes (though not new features) will continue to be backported to 24 after that point. Marco said he did not think this needed to be a major concern given the remaining runway, and planned to raise the topic at an upcoming CMS meeting, though the transcript is unclear about which specific meeting (Marco referred to both a management meeting and "the weekly general CMS meeting" while correcting himself) and also intends to bring it up with Jamie the next day.

### glideinWMS 3.11.4 testing

Hyunwoo Kim reported that the Fermilab factory is running glideinWMS 3.11.4, and that he updated a configuration file together with Luís Simas involving some recent method changes (the transcript is unclear on the exact details of this update). Separately, Marco Mascheroni said he started working that morning on resurrecting the ITB Dev deployment to test 3.11.4, but ran into a problem attempting to clone something needed for the test; the transcript does not make clear what specifically failed.

### Distance-based matchmaking proposal

Marco Mascheroni gave an early overview of a proposal he volunteered to work on following an action item from the Fermilab workflow-management retreat in May: matchmaking based on distance in glideinWMS. This was inspired by the Justin tool, used by the DUNE experiment, which performs distance-based matchmaking using Rucio's concept of distance between pairs of storage elements (RSEs).

As currently envisioned, jobs defined in the scheduler specify one or more input LFNs; Marco assumes WM Agent or an equivalent component would populate a list of RSEs where the corresponding data is available. Initially, matchmaking would continue to use the current desired-sites requirement (i.e., a job runs at the site holding the data); the proposal would later also allow jobs to run at "close" sites and read the data remotely. Marco is not satisfied with the current sketch for implementing this as a HTCondor requirement/constraint — as designed, it would require the pilot to specify each site-distance pair as a separate class-ad constraint — and plans to discuss whether there is a better way to express this with Jamie the next day (Tuesday, 6 PM). Marco described the work as still in the design/definition phase and declined to go into further detail at this meeting. Hyunwoo Kim expressed interest and said he would try to join the discussion with Jamie, noting the usual meeting time does not always work for him.

### Training

Marco Mascheroni and Luís Simas noted they had forgotten to resume a previously started training. Since Luís currently has less on his plate (alerts work is cleaned up) and there is no general meeting the next day, they agreed to try resuming it Tuesday afternoon, with Luís to ping Marco to settle on the exact time.

## Open Questions

- Whether opening individual tickets with ~20–25 different EGI/Tier-2/Tier-3 site admins is the right approach for the remaining Condor CE site-token migrations, versus a more centralized approach.
- Who manages the site-token-to-Unix-user mapping on EGI-flavor sites (as opposed to the OSG RPM-based approach), particularly for ARC CEs.
- Whether a distributable package/RPM for EGI repositories is feasible for the site-token mapping.
- Why the two pending Tier-1 entries (Poland, Russia) accept the site token but leave jobs pending.
- What exactly is breaking WM Agent under HTCondor 25 (suspected to be related to Python-binding changes) and when this will be fixed.
- Which specific meeting Marco Mascheroni intended to raise the HTCondor 24/25 WM Agent issue at.
- What caused the clone failure Marco Mascheroni hit while trying to resurrect the ITB Dev deployment for 3.11.4 testing.
- How the distance-based matchmaking requirement should best be expressed/implemented in HTCondor, pending discussion with Jamie.

## Related

[[OSG]] · [[CMS]] · [[HTCondor]] · [[glideinWMS]] · [[WMAgent]] · [[Rucio]] · [[Factory Operations]] · [[Factory Configuration]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-21 17.06.44 OSG Factory Ops Meeting`)
