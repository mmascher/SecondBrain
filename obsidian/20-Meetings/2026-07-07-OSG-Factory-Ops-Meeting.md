---
type: meeting
date: 2026-07-07
participants:
  - Jeff Dost
  - Hyunwoo Kim
  - Marco Mascheroni
  - Luís Simas
topics:
  - glideinWMS 3.11.4 front-end credential-shipping bug (site token / grid proxy)
  - Fermilab non-CMS front-end and factory upgrade holdoff
  - ARC CE X509 requirements
  - MIT Condor CE site-token migration
  - Fermilab certificate authority provider change
---

# OSG Factory Ops Meeting

## Summary

The meeting opened with Hyunwoo Kim relaying a bug report, via Nick Peregano (who manages the Fermilab non-CMS/"Fermi grid" front end), affecting glideinWMS front end 3.11.4: when a group in `frontend.xml` is configured with both a grid proxy and a site token credential, only one of the two is now shipped to factories, whereas previously both were sent. The group discussed the scope of this bug — including whether CMS's own front-end groups (which also combine both credential types in single groups, e.g. `main` and `main_arc`, for historical reasons) are similarly exposed — and the ongoing need for X509/grid-proxy support at ARC CEs and a few other sites (RAL, MIT). The group concluded that front ends should hold off upgrading to the 3.11 series until the bug is fixed upstream. Hyunwoo also gave a Fermilab-side update on factory upgrade sequencing, and Luís Simas reported on the MIT Condor CE site-token migration status and on Fermilab's upcoming change of certificate authority provider, which the group determined should not affect glideinWMS proxy-based credentials.

## Decisions / Conclusions

- Front ends should hold off upgrading to the glideinWMS 3.11 series (specifically 3.11.4) until the group learns more about, and glideinWMS developers fix, the credential-shipping bug where only one of two credentials (grid proxy / site token) configured in the same front-end group is sent to factories. Jeff Dost proposed this and Marco Mascheroni agreed it was a good plan.
- CMS's front-end configuration also combines both grid proxy and site token in single groups (a `main` group and a `main_arc` group), for reasons Marco Mascheroni described as "probably historical" and said should eventually be cleaned up. This means CMS is not clearly sidestepping the bug by virtue of its group structure.
- The bug affects only the site-token/grid-proxy dual-credential case within a single group, not a bug specific to having multiple groups in a front end.
- Upgrading the glideinWMS *factory* package itself (as opposed to the front end) is considered low-risk/minimal-change; the credential-shipping bug is a front-end-side issue, not a factory-side one.
- The group agreed Hyunwoo Kim should wait a staggered period after the OSG factory (already on 3.11.4) before upgrading the Fermilab factory to the same version, so that any additional issues can first be caught on the OSG factory.
- For the MIT Condor CE site-token migration: two of MIT's three CEs currently do not work with site tokens (only the third, already updated to a newer HTCondor CE package, accepts site tokens). The site admin is aware and plans to update the other two to AlmaLinux 9 with newer packages, but this was expected to take weeks. The group decided to roll back auth_method to grid proxy/X509 for those two CEs in the factory config now, rather than block the broader `auth_method` config merge on MIT's readiness; Luís Simas will make this change without waiting for the site admin's reply, since having all three CEs operational is preferable regardless.
- Once MIT is fully migrated to site tokens, the earlier-held-off `auth_method` config change can be merged for all factories at once, rather than merging per-factory piecemeal (Jeff Dost's stated preference, to avoid one factory lagging behind on unrelated config changes).
- MIT being left on grid proxy for now does not block any other migration work, since many ARC CEs still require grid proxy/X509 regardless.
- Fermilab's planned change of certificate authority provider (expected within the next couple of weeks, i.e. in July) — where the new provider no longer issues client certificates — is understood to be a different issue from the earlier "host certificate used as client certificate" problem (related to a browser/CA ecosystem decision, referenced as a "Google" decision, from several months prior) that had affected some OSG services (e.g., CE advertisement to the OSG collector). The CA change should not affect X509 grid proxies used by the Fermilab front end, since proxies are generated from personal/service certificates via a different mechanism than direct host-certificate authentication. The CERN CE log-shipping mechanism was confirmed to use rsync with a secret, not host-cert authentication, so it is also unaffected. Conclusion: there is no pressure from the CA change to migrate to site tokens on that front.
- When an entry has `enabled = false`, it should not appear in the Factory Collector at all (confirmed by Marco Mascheroni). A discrepancy between Hyunwoo Kim's count of `auth_method = grid_proxy` lines in a Fermilab factory config scan (~20-30 lines, roughly two-thirds disabled) and Luís Simas's `condor_status`-based count on the production factory (20+ enabled sites, mostly ARC) was attributed to the Fermilab factory config not having all the same entries enabled as e.g. the CERN factory.

## Action Items

- [ ] Roll back `auth_method` to grid proxy/X509 for two of MIT's three Condor CEs in the factory config, then commit so Hyunwoo Kim can merge that part of the config — Luís Simas
- [ ] Determine how many sites served by the Fermilab front end still require grid proxy/X509 (not currently known precisely) — Hyunwoo Kim
- [ ] Check whether CMS ARC sites use a single front-end group containing both grid proxy and site token credentials (confirmed during the meeting: yes, for both `main` and `main_arc` groups) — Marco Mascheroni
- [ ] Bring up the 3.11.4 credential-shipping bug at the stakeholder meeting the following day — Jeff Dost / Marco Mascheroni
- [ ] Share a previous summary of the host-certificate/client-certificate issue from months ago with Luís Simas — Hyunwoo Kim
- [ ] Continue testing remaining grid-proxy sites with site tokens (sites already mapped out) — Luís Simas

## Discussion

### glideinWMS 3.11.4 credential-shipping bug

Hyunwoo Kim reported that Nick Peregano, who manages the Fermilab non-CMS ("Fermi grid") front end, recently upgraded one of the Fermilab front ends to glideinWMS 3.11.4 and encountered difficulties. Nick discovered that in `frontend.xml`, for groups configured with both a grid proxy and a site token credential, only the first credential is now shipped to factories — previously both were sent. Nick reported this bug, and the group understood it was being worked on (Hyunwoo referred to the party informed as "Workli" in the transcript; the exact recipient/team is unclear). Jeff Dost noted this was the first he'd heard of the issue.

Jeff asked whether the bug was specifically about combining two credential types in one group, or a more general issue with multiple groups in a front end; Marco Mascheroni clarified it is about having two credentials in one group. Hyunwoo proposed, as a possible workaround until a fix is released, duplicating affected groups in the front-end XML (e.g., splitting a `main` group into a `main` group with grid proxy and a `main_token` group with site token) — this was discussed as an idea but not adopted as a plan; the group instead decided to wait for the upstream fix.

Hyunwoo cautioned that the bug report currently comes from a single source (Nick, who said he discussed it with Marco Mambelli) and it is not confirmed whether glideinWMS developers have officially reproduced it in 3.11.4.

### Scope: which sites/VOs still require X509

Jeff Dost asked about the scope of remaining X509/grid-proxy requirements. Marco Mascheroni and Luís Simas noted RAL and MIT sites connected to the Fermilab factory require grid proxy, though there are other Tier sites globally with the same requirement. Luís Simas said a `condor_status` scan of the production factory that day found 20+ sites configured with `auth_method = grid_proxy`, mostly ARC CEs. Hyunwoo Kim's own scan of a Fermilab factory config had shown roughly 20-30 lines with `auth_method = grid_proxy`, about two-thirds of them disabled, with only a few RAL sites and MIT enabled; Jeff Dost explained the discrepancy was likely due to the Fermilab factory not having all the same entries enabled that other factories (e.g., CERN's) do, since disabled entries should not appear in the Factory Collector at all.

Jeff Dost realized during the discussion that ARC CEs still require X509 for many VOs, and that the group had "been ignoring ARC" in prior conversations about site-token migration — raising the concern that some OSG-pool ARC entries might already be broken if X509 handling had been assumed unnecessary. He noted that unlike Condor CEs (which previously had a fallback: continue without proxy if not configured), ARC/front-end auth in the 3.11 series requires separate explicit entries per auth method (`X509` vs. `psiToken`/site token), with no automatic fallback.

Marco Mascheroni confirmed that CMS currently has a `main` front-end group containing both grid proxy and site token, and a `main_arc` group also containing both, which Marco attributed to historical reasons and suggested should be cleaned up. This means the CMS front end may be similarly exposed to the credential-shipping bug rather than sidestepping it via group separation, contrary to an earlier hypothesis that OS Pool might already avoid the bug due to its group structure.

Jeff Dost recalled that the original motivation for investigating site-token fallback behavior was that when Fermilab moved their front end to the 3.11 series, sites expected to require X509 (and previously covered by fallback) stopped working, prompting fixes; he suggested this same risk applies broadly and the group should not assume which sites are truly using site tokens vs. X509 without verification, similar to the earlier verification round Luís Simas did for Condor CEs.

### Fermilab factory/front-end upgrade sequencing

Hyunwoo Kim clarified he has been holding off on two separate items at Fermilab: (1) merging Luís Simas's recent `auth_method = site token` config changes, which the group had previously told him to hold off on pending the MIT status, and (2) upgrading the Fermilab factory's glideinWMS package to 3.11.4 (the factory is currently on 3.11.3). Jeff Dost clarified that the credential-shipping bug originates on the front-end side, not the factory side, so there is no blocker to upgrading the factory package itself; upgrading the factory is expected to involve minimal changes. Hyunwoo suggested waiting a period between the OSG factory upgrade (already on 3.11.4 for a while) and the Fermilab factory upgrade, so any issues can first surface on the OSG factory; Jeff agreed this was a good idea.

### MIT Condor CE site-token status

Luís Simas reported MIT has three Condor CEs; only one (already updated to a newer HTCondor CE package) accepts site tokens, while the other two do not and still require grid proxy. The site admin is aware and plans to update the remaining two to AlmaLinux 9 with newer packages, but this was expected to take weeks according to the admin. Luís had also tested switching between grid proxy and site tokens on these CEs via the CERN factory and found the site admin's earlier claim (that all three CEs could be consolidated to accept cores in a single CE) did not hold in practice; he had a follow-up ticket outstanding.

The group agreed the pragmatic path is to roll back `auth_method` to grid proxy/X509 for the two non-working MIT CEs in the factory config, allowing Hyunwoo Kim to merge that part of the config independently of MIT's full readiness. Once MIT is fully ready for site tokens, all factories would receive that update together in one merge, consistent with Jeff Dost's general preference against having one factory wait to merge a change that others have already received. Luís confirmed he would proceed with the rollback without waiting for the site admin's reply, since restoring all three CEs to operational status is beneficial regardless of the site admin's longer-term plan, and MIT remaining on grid proxy does not block other work (many ARC sites are in the same state).

### Fermilab certificate authority provider change

Luís Simas raised a concern, originally heard the prior week both in this meeting series and in a glideinWMS developers meeting, that Fermilab will change its certificate authority provider within the next couple of weeks (in July), and the new provider does not issue client certificates. Luís was concerned this could mean the Fermilab front end could no longer obtain a valid grid proxy.

Hyunwoo Kim and Jeff Dost clarified this is likely unrelated to the front end's use of X509 grid proxies. They distinguished it from an earlier, separate issue from several months prior — a decision by a certificate/browser ecosystem party (referred to in the transcript as "Google") affecting a bit/flag in certificates used to mark them as valid for server vs. client authentication — which had caused problems where OSG services were using host certificates directly as client certificates (as opposed to generating an X509 proxy from a personal/service certificate, which is what front ends use). That earlier issue had affected some OSG services, including (per Jeff Dost) the mechanism CEs use to advertise themselves to the OSG collector, motivating a broader move away from "auto-conf"-style host-cert usage; OSG software was reportedly working on a solution for that specific problem after Jeff pushed back on it.

Jeff Dost confirmed CERN's log-shipping mechanism from factories uses rsync with a secret rather than host-cert authentication, and Marco Mascheroni noted most current mechanisms use tokens in some form. The group concluded the CA provider change should not affect X509 proxies or glideinWMS credentials, and therefore creates no additional pressure to migrate to site tokens. Hyunwoo offered to locate and share his earlier written summary of the related host-cert/client-cert issue with Luís.

Separately, Luís Simas noted he has already mapped out all remaining sites still using grid proxy (as opposed to site tokens) and will begin testing them with site tokens.

## Open Questions

- Who exactly received Nick Peregano's bug report (transcribed as "Workli") and whether glideinWMS developers have officially reproduced the 3.11.4 credential-shipping bug.
- How many sites served by the Fermilab (non-CMS) front end still require X509/grid proxy — Hyunwoo Kim did not have a precise answer and said he would need to find out.
- Whether the root cause of MIT's two non-working CEs is confirmed to be an old HTCondor CE package version, as the site admin concluded — Luís Simas was not certain the site admin's diagnosis was correct, and did not have information on exactly how old the package version was.

## Related

[[OSG]] · [[CMS]] · [[glideinWMS]] · [[HTCondor]] · [[Factory Operations]] · [[Factory Configuration]] · [[Pilot Jobs]] · [[CERN]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-07 17.08.03 OSG Factory Ops Meeting`)
