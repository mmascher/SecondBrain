---
type: meeting
date: 2026-08-13
participants:
  - Marco Mascheroni
  - Luis Simas
  - Hyunwoo Kim
topics:
  - Fermilab backup collector crashing (HTCondor bug investigation)
  - WMAgent schedd flocking failure to Tier-0 pool
  - Tier-0 collector incident (hypervisor hardware failure, firewalld)
  - schedd (SCADI) security updates and ownership/responsibility
  - Front-end certificate renewal failure
  - Site tokens migration (Factory CEs)
  - Condor 24 → 25 upgrade planning
  - glideinWMS frontend testing on ITB dev
  - New operator (Pablo) onboarding
---

# Submission Infrastructure Weekly Meeting (2026-08-13)

## Summary

This is a "summer mode" roundtable-style Submission Infrastructure weekly meeting (no fixed agenda, per Marco). The transcript begins mid-discussion, already analyzing a monitoring failure against the Fermilab backup collector. The group first worked through whether an HTCondor collector crash at Fermilab was fixed by a manual HTCondor upgrade or by switching monitoring queries to the primary collector — the two changes happened close together in time, so the group agreed a clean test (switching monitoring back to the secondary collector) is needed to know for sure. Marco then raised a separate incident: WMAgent schedds failing to flock to the Tier-0/CERN collector, which was traced to schedds ("SCADI") that had lost their connection, most likely following a Tier-0 collector restart. The rest of the meeting was a roundtable: Hyunwoo on the Condor 24→25 upgrade plan; Marco on glideinWMS frontend testing in ITB dev; and a long update from Luis covering schedd security updates and team responsibility boundaries, a full recap of last week's Tier-0 collector incident (hypervisor hardware failure and a stray firewalld rule), the front-end certificate renewal failure, site-tokens migration progress on the Factory, and onboarding plans for the new operator, Pablo, starting September 1st.

## Decisions / Conclusions

- Restarting a schedd ("SCADI") is not a risky/disruptive operation: WMAgent automatically retries jobs that were running on a restarted schedd, so no downtime results. No approval is needed to restart a SCADI, though other teams should be notified so they understand any resulting failures.
- Responsibility split (as articulated by Marco): SI is responsible for schedd connectivity/flocking issues and can restart SCADIs freely. Upgrading the Condor version on schedds shared with other teams (P&R for CRAB/WMAgent schedds, Tier-0 for Tier-0 schedds) requires coordination — those teams need time to test and give a "green light" before SI proceeds, which is the main source of delay. Stefano (P&R) currently prefers to do CRAB schedd upgrades himself; SI is willing to help but defers to P&R's testing timeline.
- The most likely root cause of the "14 SCADIs not flocking" issue was the Tier-0 collector restart from the incident described below — the timing of the disconnections matched the collector restart.
- Root cause of the Tier-0 collector incident (previous week): the physical hypervisor hosting the Tier-0 collector VM had a hardware failure (believed to be ECC memory corruption), causing CPUs on the VM to stall; the hypervisor eventually crashed and rebooted, taking the VM with it. On reboot, a `firewalld` rule that had been applied manually on the machine (not persisted via Puppet) came back and started blocking connections. Fix: disable and stop the `firewalld` service.
- `firewalld` does not appear to be installed via Puppet and is not present on other machines (e.g. Factory machines); its origin on this machine is unknown. It is not believed to be an AlmaLinux 9 default.
- The extra "CMS Pilot2/hostname"-style Subject Alternative Name (SAN) entry in the front-end certificate Puppet configuration is believed unnecessary: the front-end certificate itself is no longer used to authenticate anything (this changed once everything migrated to tokens); today only the CMS Pilot certificate is used, for CE authentication. The suspected fix for the renewal failure is to remove that extra SAN from the Puppet config (untested as of the meeting).
- Global pool collector load from the (much heavier) single monitoring query to the secondary/backup collector was, contrary to expectation, not a major driver of duty cycle; Luis and Marco's shared hypothesis (based on prior discussion with Jimmy, not independently verified) is that many small/frequent queries (e.g. from a front end) are more expensive than one large query, because HTCondor forks a process per query except for small/limited (e.g. `-limit 10`) queries that can run in-process.

## Action Items

- [ ] Test some queries against the secondary (Fermilab backup) collector, then switch WMAgent monitoring back to it on Monday to determine whether the HTCondor 25.0.13 upgrade actually fixed the crashing, and report results either way — Luis Simas
- [ ] Ping P&R (Gregor) again about validating the pending schedd security updates — Luis Simas
- [ ] Check with Antonio on the status of the Tier-0 schedd Condor upgrade (and whether Antonio has moved to CMS monitoring work) — Luis Simas
- [ ] Check newly created Frontier machines for whether `firewalld` is present by default; if so, add Puppet code to disable it; if not, leave as is — Luis Simas
- [ ] Add a monitoring alert for the collector not responding, similar to the existing schedd-not-responding alert — Luis Simas
- [ ] Build a list of all schedds (including those SI doesn't directly manage, e.g. CMS Connect, institutional schedds) that still need Condor version updates, using the list of schedd versions connected to the collector — Luis Simas
- [ ] Back up existing front-end/pilot certificates, then test the suspected certificate-renewal fix (removing the extra SAN from Puppet) starting in ITB, expected to start the day after the meeting — Luis Simas
- [ ] Find the old TWiki page (originally by James Letts) documenting the manual front-end certificate renewal process — Marco Mascheroni
- [ ] Follow up on whether WMAgent/Tier-0 schedds are flocking correctly to the CERN collector (check was in progress during the meeting but didn't complete in time) — Marco Mascheroni
- [ ] Disable the Sentry/site entries for the Taiwan Tier-3 site once its CE migration from ARC CE to HTCondor-CE is complete — Luis Simas

## Discussion

### Fermilab backup collector crash investigation

- Luis's monitoring script had been failing to query the Fermilab collector for an unknown reason (connection closed without explanation). Hyunwoo separately found that a Condor collector process on that machine (the backup/secondary collector) was repeatedly crashing every few minutes.
- Luis's hypothesis: the monitoring script's query is heavy (it queries all startds — thousands of pilots), HTCondor forks a process per query, and that process crashed, closing the socket from the collector side and producing the "connection closed" error the script saw. This wasn't independently confirmed (no information in the stack trace).
- Hyunwoo reported the crash to the HTCondor mailing list; Greg (HTCondor dev) responded that this was a known bug fixed in HTCondor 25.0.13. The machine was on 25.0.12 at the time; Hyunwoo manually downloaded and installed the 25.0.13 RPMs.
- Timing complication: the crashing had already stopped once the team switched monitoring queries over to the primary collector, before the 25.0.13 upgrade was applied — meaning Hyunwoo's original statement ("I upgraded and the error stopped") was premature, since the switch to the primary collector could also explain it. Both changes happened around the same time, so it's possible both are "true" (the switch masked the issue, and the upgrade also fixed it). Luis confirmed that a previously-failing query against the Fermilab collector now succeeds even without reverting to the secondary collector, which is consistent with the upgrade being an actual fix, but this is not yet a clean test.
- Agreed real test: switch monitoring back to the secondary (backup) collector — now running 25.0.13 — to see whether crashing resumes. Luis planned to do this test on Monday rather than immediately (meeting was on a Friday), citing a self-imposed caution about not making changes on Fridays for something that risks failing over a weekend, even though this is "just monitoring" and considered lower risk/easily reversible.
- Side observation: Luis found the primary collector's duty cycle did not spike much from taking on the heavy monitoring query (a surprise), which fed into the forking/duty-cycle discussion above.

### WMAgent schedd flocking failure to Tier-0

- Marco relayed a report from Gregor: some jobs targeting CERN as the desired site were failing to run. Root cause: WMAgent uses two pools (global pool and Tier-0/CERN pool) with separate primary collectors (global pool collector: VOCMS 14100; Tier-0 collector: VOCMS 0824). A schedd reaches the other pool's collector via HTCondor's flocking mechanism (schedd configured to flock to a second collector). Flocking from the affected schedd to the Tier-0/CERN collector had failed, so its jobs weren't visible there and couldn't run.
- Fix: Luis restarted the affected schedds ("SCADI"), which reconnected. All schedds affected by this issue (reported as "14 SCADIs" since "the incident last week", referring to the Tier-0 collector incident below) were restarted and reconnected, except one: a QA schedd for P&R, which has expired tokens (forwarded to Marco by email; not urgent).
- Marco confirmed this was not caused by an expired ID token — restarting the schedd was sufficient. He noted the currently deployed Condor version is old, which is one reason he hasn't reported this recurring issue upstream to the Condor developers (they would likely just recommend upgrading), along with the fact that it's a rare, hard-to-reproduce ("once a year") occurrence that has been costly to debug previously (Marco spent time in Condor logs about a year ago when it first occurred). The group agreed to upgrade to a newer Condor version and, if the issue recurs on the new version, to report it upstream (to "Jaime"/Condor devs) with more confidence, since a version bump will rule out a known/older-version cause.

### schedd (SCADI) security updates and team responsibility

- Security updates for SCADIs are pending; P&R (Gregor) asked for a few more days to validate. Plan: ping them again to move forward. Applies to P&R-managed and Tier-0 schedds as well — Luis argued all SCADIs should be updated regardless of how heavily they're used, since they are "as exposed as any other SCADI."
- Discussion clarified team responsibility boundaries (see Decisions above): SI owns schedd connectivity issues (e.g. flocking, restarts) and does not need permission to restart a SCADI; Condor version upgrades on schedds shared with P&R/Tier-0 require coordination and sign-off from those teams due to risk of breaking WMAgent/Condor. Antonio currently manages Tier-0 Condor upgrades, but his continued involvement is uncertain given a "long shutdown"/possible move to CMS monitoring — to be checked. The VO Card (VOC) team may also be involved in managing some schedulers per the VOCMS profile.
- Status of SCADIs not managed by SI (e.g. CMS Connect, institutional schedds at MIT/Wisconsin) is unclear; Marco had heard CMS Connect was updated but had no information on institutional schedds. Plan to build a full list of schedds needing updates, using the list of schedd versions visible to the collector.
- A related but separate open issue was raised: a "crab issue" from a few weeks ago where a schedd machine died from memory exhaustion, with unclear responsibility for whether WMAgent or CRAB processes were the cause. Marco does not have a clean ownership answer for this today and hopes an eventual merge of the WMAgent/CRAB teams under the next-generation WM will produce clearer separation of responsibility.

### Tier-0 collector incident recap (previous week)

- See root cause and fix in Decisions above (hypervisor hardware failure → VM reboot → un-persisted manual firewalld rule blocked connections → firewalld disabled/stopped).
- The global pool collector's central manager had the same latent risk (firewalld service present but only "stopped", not "disabled" — meaning a reboot would have re-triggered the same failure there too); Luis has since set it to "disabled" to prevent recurrence.
- Luis plans to check whether firewalld is present by default on newly built Frontier machines, and if so add explicit Puppet code to disable it; if not, no action needed.
- Luis plans to add a "collector not responding" monitoring alert, analogous to the existing schedd-not-responding alert, noting the underlying data is likely already available.

### Front-end certificate renewal failure

- Automatic renewal of the front-end certificate is failing again — the same failure mode as roughly a year ago, first flagged by Florian a few weeks prior to this meeting, and confirmed by Luis to still be failing. The certificate expires in about one month from the meeting date (deadline in the first week of September); an expiry-warning email had also been received.
- Suspected cause: cert-manager is now enforcing a restriction on a Subject Alternative Name (SAN) prefix that it previously tolerated. The front-end certificate's Puppet configuration currently defines two SANs — the plain hostname, and a second one prefixed similarly to the CMS Pilot certificate's subject (e.g. "CMS Pilot2/hostname"). Luis's working theory, confirmed by Marco, is that the front-end certificate no longer needs that second SAN, since the front-end certificate itself isn't used to authenticate anything anymore (only the CMS Pilot certificate is, for CE/central manager authentication) — historically the front-end cert authenticated to the Factory, but that's no longer the case.
- Plan: remove the extra SAN from the Puppet config and test renewal, starting in ITB, because this is considered a risky change; existing valid certificates will be backed up first. All production front ends are expected to have the same issue and same fix, except ITB-dev, which doesn't use the automated proxy renewal (Marco manually copied the proxy there rather than the host certificate, meaning its cron-based renewal doesn't currently work either — noted as something to revisit).
- Marco is trying to relocate an old TWiki page (originally written by James Letts) describing the historical manual certificate renewal process, in case the automated fix isn't found quickly.
- Longer-term direction (not a near-term plan): Marco hopes this will be the last certificate renewal needed, anticipating the front end will move to token-only authentication within about a year, removing the need for these certificates entirely. The Tier-0 front end is technically already able to drop certificate-based auth today, but there is no ITB-equivalent pool for the Tier-0 front end to test this safely, and Marco prefers to prioritize the near-term certificate renewal over rushing this migration before the September deadline.

### Site tokens migration (Factory)

- 17 of 22 CEs have been migrated to site tokens so far (Luis), better progress than expected. 5 sites remain, 3 of which already have GGUS tickets open; some sites haven't yet responded, some are in downtime (making it impossible to tell if the CE works), and some are out of downtime but still not working. Luis expects this "long tail" to take a few more weeks.
- One notable case: a Taiwan Tier-3 site is in CMS's "candidate" site state (not yet fully validated/accepted into CMS), but CMS uses its resources anyway per Andrea, who said this is not a concern. Its CE is an ARC CE that has had persistent, unresolved issues for months; the site has decided to migrate to HTCondor-CE instead in the coming weeks/months. Once that migration completes, Luis plans to disable the site's Sentry/related grid-proxy entries, since the ARC CE will be decommissioned.

### Condor 24 → 25 upgrade and ITB dev frontend testing

- Hyunwoo noted most WMAgent machines are still running Condor 24. Marco said the upgrade to 25 is planned as the first task for the new operator (Pablo), starting September 1st — partly because it's a good way for him to get familiar with the team's systems (Puppet, etc.).
- Marco has been testing a newer glideinWMS frontend package on ITB-dev (explicitly not ITB proper, to avoid breaking the test pool other people rely on). He upgraded from the 3.10-series to a newer version, opened a couple of pull requests fixing issues found along the way (an unclear error for an expired proxy, unreadable stack traces), before going on vacation. Task is not yet complete: while testing, the new frontend appeared unable to find all resources when querying the scheduler via the Factory; Marco paused this investigation to work on other things and has not yet resumed it.

### New operator (Pablo) onboarding

- Pablo starts September 1st; hired under the same arrangement as Luis (not a CERN-affiliated hire), with no quota/logistics issues expected so far. Logistics (desk, laptop) still to be arranged with Stefano.
- Marco plans to travel to CERN for in-person onboarding around the week of a computing-related conference/workshop (referred to as "Flight and Computing Week", tentatively the week of the 21st — Marco and Luis were not fully certain of the exact week during the discussion), mirroring the onboarding pattern used for Luis (an in-person week plus Zoom sessions, with day-to-day teaching handled at the time by a previous team member, "Viva", over about a month).
- Since Florian (who previously did more of this kind of day-to-day/CERN-administrative mentoring) has left, Luis offered to help train Pablo on SCADI operations and CERN administrative basics, given he is on-site; Marco welcomed this. Marco noted the front-end/Factory-ops side of the role tends to involve more day-to-day operational load (many site administrators to deal with) than the WMAgent/project side, which is currently quieter due to a WMAgent feature freeze.
- Marco briefly checked in with Luis on how the role has been going and whether he has requests, but the transcript cuts off before Luis's answer is captured.

## Open Questions

- Whether the HTCondor 25.0.13 upgrade on the Fermilab backup collector actually fixed the crashing, independent of the earlier switch to the primary collector — pending the Monday test.
- Where the `firewalld` service/rule on the Tier-0 collector machine originated, and whether it's needed at all (CERN IT security stance on this is unknown).
- Whether Antonio remains responsible for Tier-0 schedd Condor upgrades, or has moved to CMS monitoring work.
- Whether removing the extra SAN from the front-end certificate Puppet configuration actually resolves the renewal failure (untested as of the meeting).
- Update status of SCADIs not managed by SI (CMS Connect confirmed updated; MIT/Wisconsin institutional schedds unknown).
- Who is responsible when a shared schedd machine fails due to memory pressure from a mix of WMAgent and CRAB processes.

## Related

[[HTCondor]] · [[WMAgent]] · [[CRAB]] · [[glideinWMS]] · [[Factory]] · [[Factory Operations]] · [[Submission Infrastructure]] · [[CERN]] · [[CMS]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-08-13 16.44.52 Submission Infrastructure Weekly Meeting`)
