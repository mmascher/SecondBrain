---
type: meeting
date: 2026-05-19
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Luís Simas
  - Hyunwoo Kim
topics:
  - Wisconsin power outage impacting OSG Tiger/NRP factories
  - CERN VOFrontend firewall/Puppet incident and HA failover behavior
  - Condor CE site-token auth migration
  - glideinWMS 3.11 stakeholder update
  - DIRAC/DIRACX integration retreat and July hackathon
  - CHEP poster
---

# OSG Factory Ops Meeting

## Summary

The transcript begins mid-discussion (the recording appears to start partway into Jeff Dost's report), already describing recovery from a power outage at Wisconsin that had taken down the Tiger cluster's Ceph storage and disrupted Kubernetes-backed services, requiring a manual restart of the Tiger factory and, separately, the redundant NRP factory. Luís Simas then reported a CERN incident where a Puppet-managed firewall rule blocked pilot access to the VOFrontend, shrinking the global pool by about 35% over the weekend; the group discussed in detail why the Fermilab backup front end's automatic failover did not trigger. The rest of the meeting covered Condor CE site-token migration progress, a stakeholder update on glideinWMS 3.11 adoption blockers, Marco Mascheroni's report from a cross-experiment workflow-management retreat involving DIRAC/DIRACX, and routine items (a planned factory reboot, and CHEP poster logistics).

## Decisions / Conclusions

- The OSG Tiger and NRP (redundant) factories have both recovered and are back to normal after the Wisconsin power outage; Jeff Dost is still working through roughly 45 affected hosted CEs.
- The CERN incident was caused by a CERN Puppet automation that drops a firewall rule for port 80 on the VOFrontend VM if Puppet hasn't run for 30 days; this blocked new pilots from downloading configuration files from the front end. It was resolved by re-enabling Puppet and waiting for the firewall rule to be reapplied.
- The global HTCondor pool shrank by about 35% during the CERN incident (per a monitoring plot referenced in the meeting), but Marco Mascheroni noted the actual capacity loss was likely smaller than 35%, since only new-pilot validation was affected — already-running pilots (with lifetimes up to 5 days) kept working normally.
- The Fermilab backup front end's automatic failover did not trigger during the CERN incident because the CERN front end process itself remained up and continued sending monitoring classads/pilot requests through the factory collector. The failure occurred only at the final step (pilots downloading files from the front end), which is not what the failover check monitors.
- The failover mechanism works as follows: the front end and factory communicate via a condor collector on the factory ("factory collector"); the front end submits pilot requests and monitoring classads to it. If the backup front end sees no requests/monitoring classads from the CERN front end on that collector, it begins submitting on its own.
- Jeff Dost concluded that this kind of failure (a single firewall rule blocking file downloads while the front end process stays up) would be very hard to distinguish automatically from a partial/site-specific issue, and that HA "could never really work" for this kind of web-server-level failure in the current design.
- No factory-ops operator was actively monitoring over the incident weekend: Florian (referred to in the transcript as "Floria"/"Floren," almost certainly [[Florian Von Cube]]) had finished his contract and was traveling, and Luís Simas was on holiday. Despite this, only one site/ticket was reported as noticing impact.
- The previously-reported slot-overload monitoring plot issue is now fixed; it had been waiting on old OpenSearch data at CERN to expire before the query could run again.
- Fermilab's non-CMS VOs (served by a separate, non-CMS front end) are interested in upgrading to glideinWMS/HTCondor 3.11 but are blocked because that version changed semantics: it no longer automatically falls back to X509 proxy when site-token auth isn't configured. Since these VOs share sites with CMS, CMS-scoped Condor CE entries must first be migrated to site-token `auth_method` before the non-CMS front end can safely upgrade.

## Action Items

- [ ] Add a note documenting the Wisconsin power outage / Tiger and NRP factory incident — Jeff Dost
- [ ] Continue the Condor CE `auth_method` migration to site tokens; expects most of it done this week — Luís Simas
- [ ] Reboot the factory to update Condor — Hyunwoo Kim (planned for the day after the meeting)

## Discussion

### Wisconsin power outage (Tiger / NRP factories)

Jeff Dost described recovering from a power outage in Wisconsin that took down nodes backing part of the Tiger cluster's Ceph storage, which in turn disrupted Kubernetes-dependent services. He had to manually restart the Tiger factory even though, as far as he understood, it uses a different (NVMe-backed) Ceph filesystem than the one that went down — he speculated the factory's reconfig process may have failed to talk to the CE collector during the outage, leaving it in a bad state until restarted. The separate, supposedly redundant NRP factory also locked up, for a reason Jeff did not understand, but was likewise recovered. He noted CERN/Kubernetes has multiple physically separate Ceph filesystems, and while only one was directly affected, enough Kubernetes components depended on it to cause broader problems. Jeff was still working through about 45 affected hosted CEs at the time of the meeting. He and Marco Mascheroni briefly speculated whether increased glidein "churn" from the outage could have caused increased load on the factory (contributing to the NRP factory's separate lockup), but agreed this was likely coincidental rather than a confirmed causal link.

### CERN VOFrontend firewall incident and HA failover

Luís Simas reported that on Saturday night, a CERN Puppet automation dropped a firewall rule allowing traffic to port 80 on the CERN VOFrontend (this automation drops the rule if Puppet hasn't run on the VM for 30 days). As a result, new pilots could not download configuration files from the front end and failed validation. The fix was to re-enable Puppet and wait for the firewall rule to be reapplied. The global pool shrank by about 35% (per a linked plot) before recovering.

Jeff Dost initially wondered if this was related to the Wisconsin power outage, given the similar timing, but agreed with Marco it was a coincidence. The group then discussed at length why the Fermilab backup front end did not automatically fail over: Marco explained the front end and factory communicate via a condor collector ("factory collector"), with the front end submitting pilot requests and monitoring classads to it; the backup only takes over if it sees no such activity from the primary. Since the CERN front end process was still running and only the final pilot file-download step was broken, no failover condition was ever detected. Hyunwoo Kim asked whether, hypothetically, someone could have manually stopped the CERN front end to force a failover; Marco noted nobody was watching at the time since Florian ("Floria"/"Floren" in the transcript) had finished his contract and was traveling, and Luís was on holiday — though he also noted that, despite this, essentially nobody else noticed or complained, and only one site's ticket referenced the issue. Jeff Dost pointed out that existing pilots would have kept recycling/retrying without necessarily showing up as a visible capacity drop unless someone checked glidein logs directly. Marco added that because validation failure (not the older, already-running glideins) was the only thing affected, and pilots can run up to 5 days, actual lost capacity was probably less than the 35% pool-size drop suggested.

Luís asked whether a check for this specific failure mode (front end up but file downloads failing) could be added to the failover logic. Jeff Dost said this would be hard to implement reliably, since it's difficult to automatically distinguish a total outage from a partial, site-specific issue; he concluded that HA "could never really work" for this type of web-server-level failure. Hyunwoo Kim separately noted, based on prior observation, that even when failover does trigger, there is roughly a 30-minute gap before it takes effect.

### Site tokens and GGUS tickets

Luís Simas reported higher GGUS ticket activity this week, including some older tickets now being resolved by site admins. He is continuing the migration of Condor CE `auth_method` to site tokens and expects most of it done this week. In response to Jeff Dost's question, Luís clarified this work is currently unrelated to any production issues — it is only being tested in ITB so far, to confirm CEs work correctly with site tokens before wider rollout.

### glideinWMS 3.11 stakeholder update

Jeff Dost relayed from last Wednesday's glideinWMS stakeholder call that Fermilab VOs using the separate non-CMS front end are interested in moving to 3.11, but are blocked because they share sites with CMS and 3.11 no longer automatically falls back to X509 proxy authentication when site tokens aren't configured — so CMS-scoped Condor CE entries need to be migrated to site tokens first. Hyunwoo Kim reported that a colleague (Nick) had upgraded one of the two Fermilab general-purpose-cluster front ends to test this, ran it for a couple of days, but then failed back to the original front end, which is still running an older (10.x) HTCondor version. Luís asked for clarification on the dependency; Jeff explained that pre-3.11, HTCondor CE automatically fell back to X509 if site token wasn't set up, and that behavior no longer applies in 3.11, making the site-token migration a prerequisite for the upgrade.

### DIRAC/DIRACX integration retreat

Marco Mascheroni reported attending a cross-experiment workflow-management retreat the previous week, with participants from DUNE, DES ("five"/possibly mis-transcribed), IceCube, and other experiments around Fermilab that use glideinWMS or similar tools. The DIRAC technical lead and other DIRAC team members presented; Marco described it as more of a workshop with multiple presentations and discussions than a decision-making session about whether to adopt DIRAC. The shared understanding among participants is to keep glideinWMS and adopt DIRAC's transformation system — the part responsible for linking payloads together, merging, and constructing the overall workflow. The next step is a hackathon in early July, which Marco and others from CMS plan to attend, aimed at working out how to integrate DIRAC and glideinWMS in practice.

### Other items

Hyunwoo Kim noted he needs to reboot the factory the next day to update Condor. Marco Mascheroni mentioned he is unsure whether the CHEP poster has been submitted; Florian is now understood to be in charge of it and expected to print and bring it. Neither Marco, Jeff, nor (per Jeff's assumption) Luís or Hyunwoo plan to attend CHEP in person (Bangkok, Thailand, the following week).

## Open Questions

- Why the Tiger factory's reconfig process failed to talk to the CE collector during the Wisconsin outage, given it uses a separate, seemingly unaffected Ceph filesystem — not fully understood by Jeff Dost.
- Why the redundant NRP factory separately locked up during the same period — not understood by Jeff Dost; a possible link to increased glidein churn/load was raised but not confirmed.
- The exact final capacity loss caused by the CERN firewall incident (estimated to be less than the 35% pool-size drop, but not precisely quantified).
- Whether any specific issue caused Nick's 3.11 test front end at Fermilab to be rolled back to the original version — not detailed in the meeting.

## Related

[[OSG]] · [[CMS]] · [[HTCondor]] · [[glideinWMS]] · [[Kubernetes]] · [[CERN]] · [[DIRAC]] · [[DIRACX]] · [[Factory Operations]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-19 17.07.07 OSG Factory Ops Meeting`)
