---
type: meeting
date: 2026-04-21
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Luís Simas
  - Hyunwoo Kim
topics:
  - CMS entry GLIDEIN_Overload_Enabled configuration fix
  - Condor CE auth method migration to site token
  - glideinWMS 3.11.4 testing / ITB factory upgrade
  - Factory ops poster planning
---

# OSG Factory Ops Meeting

## Summary

The group reviewed and merged Luís Simas's pull request fixing inconsistent `GLIDEIN_Overload_Enabled` values across CMS entries, which had already been running in CERN production since the previous Friday. The group then discussed migrating Condor CE entries from grid-proxy to site-token authentication (`auth_method`), agreeing to start testing this in ITB next week, beginning with CMS-scoped entries with grid type Condor. Marco Mascheroni reported no progress on glideinWMS 3.11.4 release-candidate testing; Jeff Dost said he would consider upgrading the ITB (OSG) factory to 3.11.4 given interest in related autoconf fixes. The meeting closed with a brief note that the factory-ops poster still needs to be worked on.

## Decisions / Conclusions

- Jeff Dost merged Luís Simas's pull request fixing `GLIDEIN_Overload_Enabled` across CMS entries into the OSG factory repository during the meeting, trusting Luís's PR description and the fact that it had already been running in CERN production (merged there the previous Friday) with converging correct values in the collector. The remaining outliers reporting `true`/undefined were attributed to pilots with unusually long wall times (5–7 days).
- The standardized representation for `GLIDEIN_Overload_Enabled` is a double-quoted, uppercase string (e.g. `"True"`), rather than a lowercase boolean or a bare/unquoted value, or a percentage string when overload is partially enabled.
- Fixing this configuration is what caused a previously empty monitoring plot (unresolved for a couple of months, per Hyunwoo Kim) to have stopped populating; merging the fix should repopulate it again.
- For Condor CE entries, `auth_method` should eventually be changed to site token everywhere, but this had been deliberately held off for CMS entries because CMS wasn't ready; it had already been enabled for a handful of non-CMS OSG entries following earlier confirmation from Marco Mascheroni and Vaiva that it was fine to do so there. ARC entries are treated as a separate, more delicate case and are out of scope for this work.
- The reason for holding off on CMS entries: the CMS front end had for a long time been sending both site token and X509 proxy credentials, which could mask sites where site-token authentication doesn't actually work; flipping to site-token-only could break those sites if this occurred.
- The site-token migration work for now is scoped only to entries where CMS is present in the VO list; Jeff Dost had already made a pass on non-CMS entries, which may explain why Hyunwoo Kim was seeing it work for only some entries on the Fermilab front end.
- CMS front ends should hold off upgrading to HTCondor 3.11.4 until that version is actually available, since it contains fixes Jeff Dost is uncertain apply to the non-CMS Fermilab front end; an ITB test is wanted first.

## Action Items

- [ ] Get-pull and reconfigure the Fermilab OSG factory to pick up the merged `GLIDEIN_Overload_Enabled` fix, once ready — Hyunwoo Kim
- [ ] Update the Fermilab monitoring script, which currently checks for both lowercase and uppercase boolean representations of `GLIDEIN_Overload_Enabled`, to match the new standardized string format — Hyunwoo Kim
- [ ] Test, starting in ITB, whether all CMS-scoped grid-type-Condor entries work correctly when `auth_method` is set to site token, starting before next Tuesday's meeting — Luís Simas
- [ ] Record and report back next week on entries where it is unclear whether flipping `auth_method` to site token is safe (e.g. entries with additional attributes like project ID, or that may affect other VOs even if CMS doesn't use them) rather than changing those directly — Luís Simas
- [ ] Communicate with Hyunwoo Kim (via what was referred to in the transcript as "CMS talk" — exact channel/tool unclear) before/when making the site-token changes in production — Marco Mascheroni / Luís Simas
- [ ] Monitor OSG factories after the `GLIDEIN_Overload_Enabled` merge and report back to Marco Mascheroni via Slack if issues arise — Jeff Dost
- [ ] Prepare a first draft of the factory-ops poster and share it with Marco Mascheroni, ideally by email, before the end of the week — Jeff Dost
- [ ] Hold a dedicated meeting to discuss the factory-ops poster, tentatively next Tuesday before or after the regular call — Marco Mascheroni, Jeff Dost

## Discussion

### CMS entry `GLIDEIN_Overload_Enabled` fix

Luís Simas explained that inconsistent values of `GLIDEIN_Overload_Enabled` had been observed across collectors: some entries were missing the parameter entirely, and others had it set to `true` instead of a percentage, because they had been configured before glideinWMS supported percentage-based overload. Luís used a script to make the change and, per Marco Mascheroni, also to sort all entry attributes; each commit in the PR represented an iteration between Marco and Luís to refine the change. The fix had already been merged and running in CERN production since the previous Friday, and several days of results showed the collector converging on correct values, with remaining `true`/undefined outliers attributed to pilots with long wall times (5–7 days).

Jeff Dost noted that once merged into the shared repository, OSG factories automatically reconfigure via an existing script that checks the master branch of the repo; the Fermilab factory would likely require Hyunwoo Kim to manually `git pull` and reconfigure, which Hyunwoo confirmed. Marco raised urgency tied to needing plots derived from these entries for CHEP, preferring the fix land sooner rather than later, and separately proposed cleaning up idle pilots after the merge to speed convergence across factories; Jeff agreed this could be done on all factories once the fix was in.

Hyunwoo Kim asked about the exact string format chosen for `true` (lowercase vs. double-quoted uppercase); Marco and Luís confirmed the uppercase, double-quoted string. Hyunwoo noted he had observed this inconsistency himself weeks earlier and needs to update his own monitoring script (described as using a "constrained list encoder sales command" — likely a mis-transcription) to match the new standard. Separately, Hyunwoo asked whether this fix was related to a monitoring plot that had been empty for a couple of months; Marco confirmed it was, and that the plot should repopulate once the fix propagates.

### Condor CE auth method migration (site token)

Hyunwoo Kim relayed a report from a Fermilab colleague testing HTCondor 3.11.4 on a Fermilab grid front end: some Condor CE sites have stopped accepting X509 proxies, but some factory entries are still configured to send them. Jeff Dost confirmed this is a known, pending update needed across all Condor CE entries: `auth_method` needs to change to site token. This had been intentionally deferred for CMS entries because CMS wasn't ready, though Marco Mascheroni and Vaiva had previously confirmed it was fine to do for non-CMS OSG entries, and Jeff had already flipped a handful of those. ARC entries are treated as a separate, more careful case, not part of this effort.

Jeff explained the specific risk for CMS entries: the CMS front end has historically sent both site token and X509 proxy for Condor CE authentication, so a site could appear to work while its site-token support is actually broken; switching over could then surface previously-hidden breakage. Given confidence that site token is working correctly, the group agreed to run a similar validation process to the overload-enabled fix, starting with testing in ITB.

Luís Simas agreed to start this work before next Tuesday's meeting, though full completion was not expected by then, given he is occupied with training (with "Dave") earlier in the week. The number of entries involved was estimated as "a couple of hundred," likely more than 100 but under 600 (fewer than the overload-enabled change, since ARC entries are excluded). Jeff noted that editing entries is not the hard part — the more time-consuming part is identifying which entries are safe to flip, given only Condor grid-type and grid-proxy-only entries should generally be changed. Entries currently disabled (`enabled: false`) are lower priority but harmless to update anyway, since they are occasionally re-enabled later. Entries with additional complicating attributes (e.g. one already known to have a project-ID-related, currently-broken case affecting OSG) should be recorded rather than changed outright, since they might affect other VOs even where CMS doesn't use the entry; Luís was asked to report these back next week rather than resolve them unilaterally. Jeff confirmed this work is scoped only to entries where CMS is in the VO list.

### glideinWMS 3.11.4 status

Jeff Dost asked about testing progress on the glideinWMS 3.11.4 release candidate. Marco Mascheroni reported no progress since last check, though he believed it is available in one of the OSG testing/development repositories. Given interest in related autoconf fixes, Jeff considered upgrading the ITB (OSG) factory to 3.11.4; Marco agreed this made sense. Separately, in connection with the auth-method discussion, Jeff and Marco agreed CMS front ends should hold off upgrading to 3.11.4 until it's actually released, given uncertainty about whether its fixes affect the non-CMS Fermilab front end, and given Marco still wants to test in ITB first.

### Factory-ops poster

Marco Mascheroni raised that the factory-ops poster needs to get going. Jeff Dost said he had intended to work on it over the weekend but was still recovering from a back issue; he committed to producing a first draft to share with Marco, ideally by email, before the end of the week (excluding the coming weekend, since he'll be out the following Monday). They agreed to hold a dedicated discussion, tentatively next Tuesday before or after the regular call.

## Open Questions

- Whether other, not-yet-identified Condor CE entries exist (beyond the known project-ID case) where flipping `auth_method` to site token could unexpectedly affect other VOs.
- The exact final count of Condor CE entries requiring the `auth_method` change.
- When CMS front ends will be ready to upgrade to HTCondor 3.11.4, pending its release and ITB testing.

## Related

[[OSG]] · [[CMS]] · [[HTCondor]] · [[glideinWMS]] · [[Factory Operations]] · [[Factory Configuration]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-21 17.02.47 OSG Factory Ops Meeting`)
