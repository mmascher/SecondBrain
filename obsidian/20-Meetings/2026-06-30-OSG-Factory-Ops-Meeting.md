---
type: meeting
date: 2026-06-30
participants:
  - Marco Mascheroni
  - Luís Simas
  - Hyunwoo Kim
topics:
  - MIT Tier 2 auth-method rollback and AlmaLinux 9 host update
  - CERN cooling issues
  - CERN GPU entry split
  - GlideinWMS 3.11.4 upgrade rollout
  - Negotiator failover testing at Fermilab
  - GlideinWMS site-token/proxy auth-method behavior and monitoring
  - Fermilab proxy certificate authority deprecation
---

# OSG Factory Ops Meeting

## Summary

Marco Mascheroni and Luís Simas were both at CERN and had already been syncing daily, so this was a brief check-in; Hyunwoo Kim joined for the factory-ops portion. Luís reported that the CERN entries/site-token changes are running fine, and that he is waiting on Max (MIT admin) regarding an Alma9 host update for the MIT Tier 2 and had rolled back the MIT entries' auth method to grid proxy to keep more than one factory able to submit there while that is sorted out. Marco noted cooling issues at CERN (per an email from Stefan) may explain reduced CERN resource availability, and mentioned a prior CERN GPU entry split (8-core/8GB entry split into two) to better match worker-node sizes. The group confirmed the ITB factory is validated on GlideinWMS 3.11.4 and agreed to install 3.11.4 on the CERN ("SEM"/"Sern") factory next, while leaving the Fermilab factory unchanged for now. Hyunwoo summarized his negotiator-failover testing on ITB, confirming pilots flow correctly through the chain and that swapping between the ITB and Fermilab-backup Condor negotiators works, though launching an additional negotiator instance did not work yet and needs troubleshooting. The group then had an extended discussion, prompted by an issue Luís opened against glideinWMS, about how the `auth_method` setting behaves per entry, whether an entry can list both grid proxy and site token (apparently broken in 3.11.4), what gets written into the pilot submission JDL, and why CERN entries no longer show a proxy in `condor_q` after switching to site token — this was left as something to investigate further rather than resolved live. Marco also recalled a discussion that a certificate authority change used by FNAL to generate proxies might force a migration away from proxy auth within roughly a year, though the timeline was uncertain.

## Decisions / Conclusions

- The CERN entries/site-token change (pushed by Luís) is confirmed running fine.
- Luís rolled back the MIT Tier 2 entries' auth method to grid proxy (from site token) so that more than one factory can submit to the site while the Alma9 host-update work with Max (MIT admin) is pending; the site-token change is being kept local to the specific factory where Luís is coordinating directly with the site admin.
- It was decided not to update the Fermilab factory's auth-method configuration until the fix/testing situation is resolved, since the Fermilab factory still uses the working grid-proxy auth method.
- The ITB factory is confirmed updated and validated on GlideinWMS 3.11.4, including an end-to-end pilot test.
- The group agreed ("green light") to install GlideinWMS 3.11.4 on the CERN factory next (referred to in discussion as "SEM"/"Sern" Factory), keeping the Fermilab factory as-is for now. Luís expected this could go into production "probably tomorrow."
- Hyunwoo confirmed the negotiator-failover test chain works: pilots submitted through the ITB front end/factory reach the Fermilab CE and get matched; swapping between the Sun/ITB Condor negotiator and the Fermilab backup negotiator also works and jobs still get matched. Launching an additional (second) negotiator instance did not work and requires further troubleshooting.
- The alert that had been firing was explained by this negotiator-swap testing activity (Marco and Luís had been reviewing alerts and noted this correlation); no separate incident.
- Luís confirmed all CERN entries had their auth method changed (to site token).
- Regarding the GlideinWMS behavior: as of the 3.11 factory package release, the `auth_method` specified for an entry is expected to match what each CE actually requires. Listing two auth methods (e.g., grid proxy and site token) via comma-separation in a single entry's `auth_method` was tested by "Nick" and found not to work; Marco Mambelli acknowledged this as a bug in 3.11.4 (reported in a prior GlideinWMS meeting, referenced as "last Wednesday"). The group agreed to limit their working assumption to one auth method per entry for now.
- Condor CE can be configured on the site side to accept both grid proxy and site token, falling back to proxy if site token doesn't work — this differs from ARC CE behavior (not discussed in detail).
- Marco observed via `condor_q` that CERN entries with `auth_method` set to site token show `SendCredential`/proxy-related fields as undefined (no proxy sent), whereas before the removal of a former GlideinWMS 3.10 workaround ("continue if no proxy" hack), the factory would continue submitting with the site-token credential even without a proxy present. Since that hack has been removed, Marco's conclusion is that sites now effectively need to migrate to site token for auth methods that rely on it.
- If an entry XML has `auth_method` set to a given value (e.g., site token) but the site's CE requires proxy, the entry should instead be configured with grid proxy as its `auth_method`.
- Hyunwoo confirmed understanding: as long as there remains a mixture of auth methods across factory entry XML files (currently site token for roughly 90%+ of entries, with a few remaining on grid proxy, e.g., at a site referred to as "RCE"), the front end must keep both grid-proxy and site-token credentials configured in each relevant group section. X509/proxy credentials can only be removed from the front-end configuration once no factory entry XML still uses grid proxy.
- Luís will further investigate offline why some CERN/backup entries in `condor_q` show duplicate ("2") credential-related class ads or unexpected combinations, and will check ARC entries' auth method as well as the age/status of some older-looking pilots submitted via the backup negotiator, before proceeding to upgrade the production (CERN) factory.

## Action Items

- [ ] Let Max know that the MIT entries' auth method was rolled back to grid proxy, and re-switch to site token once Max is ready to test the Alma9 host update — Luís Simas
- [ ] Reply/follow up with Max on the Gigus/Alma9 host update for MIT Tier 2 — Luís Simas
- [ ] Install GlideinWMS 3.11.4 on the CERN factory (production) — Luís Simas
- [ ] Troubleshoot launching an additional (second) negotiator instance for the Fermilab failover setup — Hyunwoo Kim
- [ ] Send Luís the full `condor_q` command used to inspect site-token/proxy class ads — Marco Mascheroni
- [ ] Investigate, before upgrading the production factory: why some entries show duplicate/unexpected credential class ads in `condor_q`, check ARC entries' auth method, and check the age/status (e.g., held) of older pilots submitted via the backup negotiator — Luís Simas

## Discussion

### MIT Tier 2 status and auth-method rollback

Luís reported that the CERN entries/site-token push is running fine. Separately, for the MIT Tier 2, he messaged Max (MIT admin) about updating the CE host to AlmaLinux 9 via Gigus; this may take a while, and Luís told Max that if it takes much longer they could roll back changes and test elsewhere (e.g., "in DB"). He noted a capacity change at MIT: pilot count there had grown from roughly 9,000 at the start of the show to roughly 15,000, though it was unclear whether Max had rearranged worker nodes. Luís is waiting on Max's reply.

Marco recalled a prior discussion about increasing submission rates for MIT's other CEs (having previously increased limits for one CE roughly three months earlier), but noted they want to double-check with the site admin first and avoid updating the Fermilab factory configuration until a fix is in place, since Fermilab's factory still uses the working grid-proxy auth method. Luís clarified he had not yet increased the submission rate for those entries; instead, his plan was to roll back the auth-method change so more than one factory can submit to the site, keeping the site-token change local to the factory where he coordinates directly with the site admin. Marco suggested letting Max know about the rollback and switching back to site token once Max is ready to test; Luís agreed to wait for Max's reply before deciding further. Marco did not consider this an emergency, noting the site is currently filled.

### CERN cooling and GPU entry split

Marco mentioned an email from Stefan about cooling issues at CERN resources, noting this may explain any observed CERN resource contraction; Luís had seen the email but not yet observed an effect on pool size. Marco also referenced a previously-discussed GPU entry split at CERN: an existing 8-core/8GB GPU entry was split into two entries to better match worker-node sizes and allow users to use more memory.

### GlideinWMS 3.11.4 rollout

Marco asked about the status of the GlideinWMS 3.11.4 upgrade for the ITB factory. Luís confirmed the ITB factory is updated and validated, including an end-to-end pilot test, and said they are now waiting to update production. Marco checked live and confirmed 3.11.4 is already installed on the Tiger factory, and proposed installing it on the CERN factory as well, giving a "green light" to proceed to production; the Fermilab factory should be left as-is for now. Luís expected this could go to production "probably tomorrow."

### Negotiator failover testing at Fermilab (ITB)

Hyunwoo summarized testing of an idea to control failover at the negotiator level for Fermilab. Using instructions on submitting jobs, he confirmed pilots submitted through the ITB front end/factory reached the Fermilab CE and were matched. He then swapped the negotiator between the ITB ("Sun") central/schedd manager and the Fermilab backup central manager and submitted another job to confirm the negotiator also works when running on the Fermilab machine — this worked. He attempted to launch an additional (second) negotiator instance dedicated to Fermilab, but this did not work and requires further troubleshooting. Marco noted this activity likely explained an alert that had been firing, which he and Luís had noticed while reviewing and triaging alerts generally (described as too noisy, with more triage work still needed).

### GlideinWMS auth-method behavior, JDL contents, and monitoring

Prompted by a GlideinWMS issue Luís had opened (relevant given the ongoing shift of Fermilab entries to site tokens), the group discussed that when an entry's auth method is changed, the entry stops reporting in the RRD/monitoring XML (referred to as the "SCADI.xml" file in the transcript); Marco agreed this is expected behavior rather than a bug, since monitoring tracks active front-end credentials, and switching credentials means the prior credential's activity is no longer tracked.

Hyunwoo then asked to confirm his understanding of the implications of the MIT rollback: current practice is to set `auth_method` in each entry XML to either grid proxy or site token, while keeping both grid-proxy and site-token credentials defined in the relevant front-end group sections. Marco confirmed. Hyunwoo asked whether an entry can specify both by listing both methods (e.g., comma-separated); Marco noted 3.11.4 is supposed to support this and said he wanted to test it, but Hyunwoo noted "Nick" had already tested this and found it did not work, and that Marco Mambelli acknowledged this as a bug in 3.11.4 during a prior GlideinWMS meeting ("last Wednesday"). The group agreed to assume, for now, that only one auth method should be listed per entry.

Hyunwoo confirmed with an example (Tier 1 US) that an entry's auth method should reflect what that site's CE actually requires (e.g., site token for the Tier 1 US Fermilab CE), and that for sites requiring grid proxy, the entry should be configured accordingly. He then asked whether a CE could be configured to accept both. Marco distinguished Condor CE from ARC CE: Condor CE sites can be configured to accept both, falling back to proxy if site token doesn't work, though Marco was unsure exactly what the factory puts into the submission JDL in that case and wanted to check.

Marco then investigated live via `condor_q`, inspecting class ads for site-token file and proxy-related attributes across submitted pilots. He found that for CERN entries with `auth_method` set to site token, the proxy-related field showed as undefined (no proxy sent) — in contrast to prior (3.10-era) behavior where a proxy would still be attached due to a former workaround. Marco explained that GlideinWMS writes a JDL file during reconfig that is used for `condor_submit`, and what's included depends on the configured auth method; in 3.10 there was a hack ("continue if no proxy," his recollection of the name) that allowed the factory to continue and submit successfully using only the site-token credential even without a proxy present, as a temporary measure while factory ops were not yet ready to fully migrate to site tokens. Since that hack has since been removed from the code, Marco's conclusion is that sites now need to actually migrate to site token where applicable — noting this has been effectively a deliberate, if gradual, push toward site-token adoption across sites over roughly two years.

While inspecting further, Marco and Luís noticed some entries (including some CERN/backup-related ones, and some inspected for ARC) showing what appeared to be duplicate ("2") credential-related class ads or other combinations that weren't immediately understood, and also noted some pilots submitted via the backup negotiator that might be old or held. Luís said this shouldn't be investigated live by the three of them right now, but felt it should be understood before upgrading the production (CERN) factory; he asked Marco to share the full `condor_q` command used. Both agreed to check this offline, including ARC entries' auth-method configuration and the age/status of the older-looking pilots.

Hyunwoo, needing to leave the call, asked a final clarifying question: given the current mixture of auth methods across factory entries (site token for roughly 90%+, grid proxy for a remaining few, e.g., at a site referred to as "RCE"), should the front end continue to carry both grid-proxy and site-token credentials in each relevant group section? Marco confirmed yes. Hyunwoo further confirmed that X509/proxy credentials could only be removed from the front-end configuration once no entry in any factory XML still used grid proxy; Marco agreed.

### Fermilab proxy deprecation

Marco recalled a discussion (attributing more detailed knowledge to someone referred to as "Steve" — the transcript is unclear whether this refers to Stephan Lammel, who appears elsewhere in project meetings) that a certificate authority used by FNAL to issue proxies was changing in a way that, in roughly one year, would prevent generating proxies for the Fermilab front end — intended as a forcing function to migrate to site tokens. Marco was not certain whether that timeline had since been extended, and suggested that even after such a migration, proxy-based credentials could potentially be left configured in the front end for sites where proxy still works.

## Open Questions

- Whether Max's AlmaLinux 9 host update for the MIT Tier 2 CE is related to the observed capacity increase (roughly 9,000 to 15,000 pilots) — unclear, pending Max's reply.
- Whether/when to increase submission rates for MIT's remaining CEs — pending resolution of the auth-method/host-update situation.
- Why some entries (including CERN/backup-related and ARC entries) show duplicate or unexpected credential-related class ads in `condor_q` — to be investigated offline before the production CERN factory upgrade.
- Why some pilots submitted via the Fermilab backup negotiator appeared possibly old or held — to be checked offline.
- How to launch an additional (second) dedicated negotiator instance for Fermilab failover — currently not working, needs troubleshooting.
- Whether the roughly one-year timeline for the FNAL proxy-issuing certificate authority change (forcing migration away from proxy) still holds, or has been extended — uncertain; noted that Steve (likely Stephan Lammel) would know more.

## Related

[[OSG]] · [[glideinWMS]] · [[HTCondor]] · [[CERN]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Submission Infrastructure]] · [[AlmaLinux]]

## Source

meeting_saved_closed_caption.txt (from `2026-06-30 17.04.16 OSG Factory Ops Meeting`)
