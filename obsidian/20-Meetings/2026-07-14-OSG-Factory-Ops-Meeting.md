---
type: meeting
date: 2026-07-14
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Hyunwoo Kim
topics:
  - DIRAC/DIRACX InterSeed meeting recap
  - HTCondor/glideinWMS security patching (Condor 25.0.12, glideinWMS 3.11.4)
  - Fermilab factory configuration migration (site tokens vs. grid proxy)
  - Expired-token pilot cleanup issue at KIT
  - Glidein retirement-time spread and the Fermilab 5-day dip pattern
  - Grid-proxy to site-token migration status
---

# OSG Factory Ops Meeting

## Summary

Marco Mascheroni recapped the DIRAC/DIRACX "InterSeed" meeting held the same day (see [[2026-07-14-DiracX-InterSeed-and-HTCondor-Access-Point-Discussion]]), noting it was aimed at connecting Condor developers with DIRAC developers, particularly around DIRAC's from-scratch rewrite of the component equivalent to the glideinWMS factory, and discussed the potential for LHCb to adopt HTCondor for pilot submission. Jeff Dost and Hyunwoo Kim gave status updates on the HTCondor/glideinWMS security-patch rollout, confirming Fermilab and OSG pool factories are upgraded. Hyunwoo Kim reported he was now able to update the Fermilab factory configuration (auth method / site token changes) after Luís Simas reverted a related change at another site. The group briefly discussed an open bug involving both X.509 and site tokens present in the same frontend group, an unresolved token-expiry issue that left stale pilots at KIT, and spent significant time discussing a recurring 5-day periodic dip in Fermilab glidein activity, its likely cause (synchronized worker-node reboots), and a proposed factory-side fix (querying HTCondor for concentrated retirement times and spreading them out) that Luís Simas is expected to raise at the glideinWMS development meeting.

## Decisions / Conclusions

- The Fermilab factory has been upgraded to glideinWMS 3.11.4 and Condor 25.0.12 with no issues encountered; Hyunwoo Kim confirmed CMS servers he manages at Fermilab are already on Condor 25.x.
- Condor 25.0.12 contains the relevant security fixes; there is no intention to move back to 24.x.
- The HTCondor security vulnerability is considered most critical for user-facing access points (e.g. CMS Connect), not factories, since factories don't grant user logins — but the team is treating the patch cycle as a good opportunity to update other components (including WMAgent) regardless of strict necessity.
- The OSG pool's Condor has reportedly already been patched (Jeff Dost's understanding, not independently confirmed in this meeting).
- Hyunwoo Kim was previously blocked from updating the Fermilab factory XML configuration (auth method / site token changes) per instruction from Marco Mascheroni and Luís Simas. That blocker was cleared after Luís reverted a related change at another site (TTUS/MIT, reverted back to grid proxy), and Hyunwoo applied the Fermilab configuration update the day before this meeting.
- For the KIT (CAIT/KIT) expired-token pilot issue: the factory had an old token and could not remove stale pilots that were not connected to the collector or the CE. The team ran `condor_rm` (referred to as "condor sex"/force removal) on their side, but the pilots also need to be removed on the site side. Jeff Dost noted `condor_rm`/force-remove only clears state on the factory side and does not affect the actual remote job state.
- The Fermilab CMS worker-node reboots (attributed to periodic security updates) cause a large batch of glideins to start simultaneously, producing a recurring ~5-day periodic dip in scheduling efficiency at retirement time (glidein max lifetime in the factory is 5 days). This is understood to be non-critical/expected, not an operational problem, but it repeatedly draws attention from site admins/users (e.g. raised again at a Fermilab operations meeting) and consumes time to keep re-explaining.
- Marco Mascheroni stated that when `GLIDEIN_Retire_Time` (wall time) is explicitly set, the separate retirement "time spread" setting is ignored — contrary to Jeff Dost's prior understanding that spread was always an additive random component on top of wall time. This point was raised by Marco as new information from a conversation with Luís Simas; it was not independently verified in this meeting.
- Luís Simas's current work priorities are: cleaning up pool-side Grafana alerts (too many low-value alerts firing, including into Marco's spam folder), migrating grid proxy to site tokens (Condor CE sites are already done; remaining focus is on ARC sites), and — after alert cleanup — extending similar alerting cleanup to the factory-side Grafana dashboard (currently CMS-only).

## Action Items

- [ ] Investigate why the stale/expired-token pilots at KIT were not removed automatically, and check logs / obtain the glidein name(s) from the site admin if possible — Marco Mascheroni
- [ ] Attend the glideinWMS development meeting (the next day) to propose and discuss the idea of making the factory spread out glidein retirement times when it detects a concentration of pilots ending at the same time — Luís Simas (per Marco Mascheroni, tentative/expected, not firmly confirmed by Luís in this meeting)
- [ ] Try to join tomorrow's meeting to check for news on the X.509/site-token-in-same-frontend-group bug reported by Nick (Fermilab) — Jeff Dost (conditional: "if I can")

## Discussion

### DIRAC/DIRACX InterSeed meeting recap

Marco Mascheroni described the earlier same-day meeting as primarily intended to bring together some DIRAC developers and Condor developers (Todd and Jamie attended on the Condor side). Todd highlighted the HTCondor features currently used for submitting pilots. Marco noted DIRAC is being rewritten from scratch, including a new "InterSeed" component that performs the same function as the glideinWMS factory, and he saw this as an opportunity to bring the two communities together. Jeff Dost speculated this could go both ways — CMS potentially adopting DIRACX ideas for workflow management, and DIRAC potentially adopting glideinWMS ideas for the factory/pilot-submission side.

Marco noted that ATLAS already uses HTCondor within Harvester to submit pilots (with a local scheduler, for ARC and Condor sites specifically); Jeff was not previously aware of this, calling Harvester "a black box" to him. Marco suggested that if more experiments adopt Condor for pilot submission, this increases pressure on WLCG to invest more effort supporting it, and mentioned the existing WLCG "ETF" (experiment test framework) same-style tests that can already submit a pilot via Condor as one avenue that could potentially be extended.

Marco clarified he deliberately did not invite ATLAS representatives to this meeting — he had invited LHCb people, with the explicit goal of "selling Condor to LHCb," and did not want to create confusion by mixing in a different customer (ATLAS) at this stage. He also could not invite ALICE because they were occupied helping with the WLCG technical roadmap document Marco is writing. Luís Simas was also invited but did not attend, as he was at CERN attending a talk by Bjarne Stroustrup (the C++ inventor).

### Security patching status

Jeff Dost reported that Hyunwoo (referred to as "Hun"/"Hanwu" in the transcript, i.e. Hyunwoo Kim) had already upgraded the Fermilab factory to glideinWMS 3.11.4 and Condor 25.0.12 without issues. Marco asked whether 25.0.12 was the version containing the security fixes; Hyunwoo confirmed yes, and that CMS servers he manages at Fermilab are already on Condor 25.x, with no path or need to go back to 24.x.

Jeff reiterated that the Condor security vulnerability primarily matters for user-facing access points (like CMS Connect), since factories don't provide user SSH/login access. Marco noted that even where not strictly at risk, upgrading now is a useful opportunity to also update related components such as WMAgent, "to get the update out of the way." Jeff mentioned Jamie had previously told him not to worry about factories specifically for this vulnerability, and separately noted his understanding that the OSG pool's Condor is already patched.

### Fermilab factory configuration migration

Hyunwoo Kim explained he had been told by Marco and Luís not to update the Fermilab factory XML configuration (auth method / site token settings) until a blocking issue was resolved. He noted Luís had recently reverted a related change (TTUS/MIT back to grid proxy) via a commit Jeff could point to, which Jeff confirmed was the only blocker. With that resolved, Hyunwoo updated the Fermilab configuration the day before this meeting.

### Open bug: X.509 and site token in same frontend group

Jeff Dost raised a bug that came up at last week's stakeholder meeting, involving both X.509 and site token being present in the same frontend group — reportedly reported by Nick from Fermilab. Marco had not attended that meeting and will also be unable to attend tomorrow's related meeting due to a scheduling conflict; Jeff said he would try to join if possible to check for updates. Hyunwoo Kim relayed that Nick said (as of "yesterday") he is working with Namrata (name possibly mis-transcribed as "Namrasa") on that issue.

### KIT expired-token pilot cleanup

Marco Mascheroni reported ongoing debugging by Luís Simas related to expired tokens at KIT ("CAIT"/KIT — Florian, the previous operator, is now the KIT admin). Some pilots remained registered despite having an old/expired token on the factory side, and the factory could not remove them because of the expired token. On the CMS/factory side, they ran a force-remove (`condor_rm`, transcribed as "condor sex") to clear the pilots. Marco noted he still needs to check why these pilots were not removed automatically. Jeff Dost cautioned this may be hard to diagnose if the pilots are old enough that logs are no longer available, and explained that force-remove only clears the factory's own bookkeeping — it does not affect whether the pilot is actually still running or registered on the remote/site side, so the site also needs to clean them up independently.

Marco clarified the pilots were not merely still running at the site — they were not connected to the collector and not visible at the CE either. Jeff noted OSG has occasionally seen a similarly rare and unexplained case: pilots that the factory has no record of, but that remain running at the site and continue serving (and outliving their intended lifetime as) real user jobs. He said this has happened before but they never got to the bottom of the root cause, and suggested that if the site admin can be asked for the glidein name, checking logs might help understand the current KIT case (assuming the site hasn't already cleaned them up).

### Fermilab glidein retirement-time spread and the 5-day dip pattern

Marco Mascheroni relayed a conversation with Luís Simas about a periodic ~5-day dip pattern in Fermilab pilot/scheduling activity, caused (per Marco and Jeff's shared understanding) by synchronized worker-node reboots (likely due to periodic security updates) that vacate a large batch of glideins simultaneously; those glideins then get resubmitted together and hit their 5-day retirement/max-lifetime limit together, causing scheduling efficiency to visibly dip in a repeating pattern.

Hyunwoo Kim examined a Grafana plot (via screen share) showing Fermilab glidein counts, confirming a clear 5-day repeating pattern where roughly 20% of ~400 (or, at another point discussed, roughly 10K out of ~50K) glideins stop accepting new jobs for several hours at a time near retirement, and noted this had also been raised independently by Dave Mason at a Fermilab operations meeting the day before. Marco stated this is not actually an operational problem, but that it keeps being raised by users/admins because Fermilab is the largest site the team operates, making the pattern more visible there than elsewhere; he expressed a desire to reduce the pattern's visibility so it stops being repeatedly flagged. In discussing which other sites might show a similar pattern, the group speculated CERN, the Italian Tier-1, MIT (T2), and Caltech as candidates for whole-node sites where this effect could also appear after a mass reboot, though this was not confirmed via the plot for any site other than Fermilab. Jeff also raised whether the pattern could instead relate to a factory-side maximum glideins-submitted-per-cycle limit, but the group did not reach a conclusion on this; Hyunwoo also asked why only ~20% (not closer to 100%) of glideins showed the effect if the triggering reboot event affected the whole cluster, which the group did not resolve — Jeff suggested it may reflect that only a subset of glideins are submitted/running in sync from any single triggering event, with the rest submitted more gradually as the factory fills up site capacity over subsequent cycles, but this remained speculative.

Marco proposed, based on a discussion with Luís Simas, that the fix under consideration is on the factory's submission side: rather than unconditionally setting a fixed wall time and spread, the factory could query HTCondor for the existing queued/running pilots' retirement times, detect when there's a concentration ending at the same time, and only then apply spread to new submissions — while leaving glideins alone (e.g. running for their normal ~5 days) when no such concentration exists. He emphasized that this would not change when glideins are submitted, only the wall-time value assigned at submission, and that no existing running glideins would be affected — only new submissions from that point on. Jeff Dost worked through his understanding of how HTCondor's `GLIDEIN_Retire_Time` and spread settings interact and raised uncertainty about the mechanism (how a factory-side decision would need to be "communicated" to individual glideins); Marco maintained this would happen entirely at the factory's `condor_q` / submission-decision stage, not via any runtime communication to already-running glideins. Marco said Luís is interested in this idea and is expected to join the glideinWMS development meeting the next day to propose and discuss the technical details, which were not worked out in this meeting. Jeff noted a related concern: if more spread is introduced into the factory's submission decisions, sites might complain about slower time-to-fill after a large vacate event — though Marco clarified only the assigned wall time (not the submission timing/rate) would change. Jeff said he wants to better understand the actual solution once Luís proposes it.

### Luís Simas's current priorities

Marco Mascheroni reported Luís's recent focus has been cleaning up pool-side Grafana alerts (too many low-value alerts firing, some ending up in Marco's spam folder), with a plan to next apply similar cleanup to the factory-side Grafana dashboard (currently CMS-only). His other ongoing priority is migrating grid-proxy authentication to site tokens; this work is complete for Condor CE sites and now focused on the remaining ARC sites.

## Open Questions

- Root cause of the KIT stale-pilot issue: why the expired-token pilots were not removed automatically, and whether they were ever connected to the collector/CE (per Marco, they were not) — unresolved at meeting time.
- The rare OSG-side phenomenon Jeff Dost described, where pilots keep running and serving jobs at a site past their lifetime with no record at the factory — never fully understood, per Jeff Dost.
- Why only ~20% of Fermilab's glideins show the periodic retirement dip rather than a larger share, if triggered by a cluster-wide reboot event — not resolved in this meeting; competing explanations (partial/staggered initial submission vs. a factory submission-rate cap) were raised but not confirmed.
- Whether Jeff Dost's prior understanding of how `GLIDEIN_Retire_Time` and the retirement time-spread setting interact (spread as an always-additive random offset) is correct, given Marco's claim that spread is ignored once wall time is explicitly set — not independently verified in this meeting.
- Whether other large/whole-node sites (CERN, Italian Tier-1, MIT, Caltech) show a similar periodic retirement-dip pattern — raised as speculation, not confirmed via data in this meeting.

## Related

[[OSG]] · [[HTCondor]] · [[glideinWMS]] · [[DIRAC]] · [[DIRACX]] · [[Factory Operations]] · [[Pilot Jobs]] · [[CMS]] · [[CERN]] · [[WLCG]] · [[Factory Configuration]] · [[2026-07-14-DiracX-InterSeed-and-HTCondor-Access-Point-Discussion]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-14 17.05.59 OSG Factory Ops Meeting`)
