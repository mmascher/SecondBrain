---
type: meeting
date: 2026-07-30
participants:
  - Marco Mascheroni
  - Stephan Lammel
  - Luis Simas
  - Hyunwoo Kim
topics:
  - CAP/production drain incident (HammerCloud)
  - glideinWMS 3.11.4 testing on ITB dev
  - Factory tarball / Alma10 default Condor version handling
  - WMAgent machine upgrades and Condor 25 testing
  - robot certificate / grid-mapfile issue for WMAgent
  - Bastion service (P&R)
  - schedd (SCADI) updates and site tokens rollout
  - global pool query load from ITB dev front end
---

# Submission Infrastructure Weekly Meeting (2026-07-30, continued)

## Summary

This transcript continues a Submission Infrastructure Weekly Meeting already in progress (it opens mid-conversation about a HammerCloud-driven production drain, and Marco Mascheroni rejoins after a computer crash). The group discussed a recent CAP/production drain incident tied to HammerCloud evaluations, then did a roundtable of updates: Marco on glideinWMS 3.11.4 testing and Factory tarball handling for Alma 10 worker nodes; Hyunwoo Kim on WMAgent machine upgrades, Condor 25 testing, and a robot-certificate/grid-mapfile issue at a Tier-1 (Fermilab); Marco and Stephan Lammel on the production Bastion service; Luis Simas on schedd (SCADI) patch rollout and the site-tokens migration for CEs; and Marco on an ITB dev front end issue that was significantly increasing query load on the global pool collector.

## Decisions / Conclusions

- The high-priority "surplus" configuration should be disabled; per Marco, this is something the team does only under exceptional circumstances, and the group can remove it for good rather than keep re-enabling it.
- Stephan confirmed the new robot certificate DN had been added to the grid-mapfile (done the prior Friday, propagated by Saturday); the fix is believed to be in place and ready to be retested.
- Marco identified that his own use of the global pool (instead of a dedicated pool) for ITB dev testing was set up that way for unclear/legacy reasons, and that enabling the ITB front end significantly increased query load (duty cycle) on the collector; he plans to investigate the front end's query behavior and open a ticket.

## Action Items

- [ ] Work with Gregor to confirm the P&R test machine intended for the Bastion service is ready, then configure it (via Puppet, matching the production system config) and enable the additional Puppet config — Marco Mascheroni / P&R team (Gregor)
- [ ] Ping Gregor (back from vacation Tuesday) to retest WMAgent/robot-certificate access to the storage elements now that the grid-mapfile entry has been added — Hyunwoo Kim
- [ ] Double-check how the `MetricLID` (or similarly named) attribute identifying where a CMS job ran is populated (SCADI/collector mechanism), and follow up with Marco Mambelli, before answering Stefano Belforte's question on the Mattermost channel — Marco Mascheroni
- [ ] Open a ticket about the increased number of queries from the ITB dev front end hitting the global pool collector — Marco Mascheroni
- [ ] Continue investigating and opening tickets for CEs where pilots fail to run with site tokens — Luis Simas
- [ ] Ping the Fermilab PNR team (on the existing Mattermost thread with Kiril and Gregor) about SCADI test results before upgrading the remaining production SCADIs — Luis Simas
- [ ] Push the remaining opportunistic Tier-3 site to the OSG Factory repository once its site-token setup is verified working, and notify Marco to update the Fermilab factory — Luis Simas

## Discussion

### CAP / production drain incident (HammerCloud)

- Stephan explained that a site is marked "bad" by HammerCloud evaluation; if a site stays in a bad state for roughly two to three days, production puts it into drain state.
- [[CAP]] (a data-processing/CMS component referenced by Stephan) has a related but different policy: it requires something like two HammerCloud evaluations within the last five days before acting, so CAP effectively switches state about a day after production does.
- In this specific incident, CAP kicked in and grabbed slots after production had already drained, and the underlying issue reportedly persisted for about three and a half days without being noticed, apparently because people were on vacation.

### glideinWMS 3.11.4 testing (Marco)

- Marco has been testing 3.11.4 on ITB dev and found several minor bugs, for which he opened tickets in the relevant repositories and provided fixes.
- Most issues traced back to the ITB dev setup and the refactoring of credential handling in 3.11, which appears to have dropped some protections/error messaging present in 3.10 — e.g., a proxy not readable by the front-end user producing an unclear error, and an "auth method mismatch between factory and front end" error that was actually caused by an expired proxy. Marco improved the corresponding error messages.

### Factory tarball / default Condor version handling for Alma 10 (Marco)

- On the OSG Factory, Marco worked on tarball management because some OSG worker nodes now run Alma 10.
- There is no single HTCondor version that spans EL7 through EL10 (Alma 10), so a single default tarball version can't cover all worker node OS versions.
- Marco changed the mechanism so that when the front end doesn't specify a Condor version, a **list** of default Condor versions can be configured instead of a single default.
- Hyunwoo asked whether the corresponding config (`glideinWMS.xml`-style / "Tyro"/"turbo" config, name unclear in transcript) needs a similar update on the CMS/Fermilab factory side; Marco said not yet, since this was specifically an OSG-side change, but expects it will be needed later when Alma 10 support is required more broadly, and confirmed he and Hyunwoo would coordinate on that update together.

### Hyunwoo's updates: memory usage, WMAgent machines, Condor 25, robot certificate

- Hyunwoo noted some production workflows at the Fermilab Tier-1 were using more memory than expected, resulting in very low core efficiency (idle cores while high-memory jobs run); Marco confirmed seeing this and attributed the dip to high-memory production jobs, noting the scale (~10,000 cores affected).
- Both attributed part of the current load to ongoing CRAB/HammerCloud "emergency" activity pushing more credentials/jobs in; resolution timing was unclear.
- Of six WMAgent machines, two are currently active. Hyunwoo upgraded the four idle machines to version 1.2.5 (as stated; exact version numbering unclear), while the two active machines remain on 24.0.22 (the latest at time of recording).
- The WMAgent operator (Gregor) found a failure when a "Derbian" (unclear term — possibly a transcription of another name) agent ran under Condor 25; it was determined the failure was not actually caused by Condor 25 itself.
- Separately, Gregor's team has been testing a transition from Alan Rodriguez's personal certificate to a robot certificate for WMAgent, but hit an error and reverted to the personal certificate for now. Discussion between Hyunwoo, Alan, and Stephan determined the robot certificate's DN was missing from the grid-mapfile of the relevant storage elements (mentioned: EOS CMS). Stephan said he added the DN a few days prior (Friday, propagating by Saturday) and the fix should now be testable; Gregor is on vacation until Tuesday and will need to be pinged to retest.
- Hyunwoo also relayed that, per the operator, aside from this specific error, the WMAgent code is generally expected to be ready for Condor 25, including its new Python bindings.

### Bastion service (P&R)

- Marco and Stephan discussed resuming work on the production Bastion service and its validation, following up on a message from Stephan about the P&R team being ready to resume this work.
- Stephan confirmed the intent is still to use the previously identified bastion machine for production; once a test machine is available, it will be configured accordingly ("combustion"/Puppet config, term partly unclear).
- Management of the production Bastion service is expected to move to Facility and (Services and Site Support), currently managed by Stephan.
- Prior test machines used for this (on the CAP side, previously managed by Vijay, and on the PNR/WMAgent side, previously managed by Alan) were both shut down some weeks ago, so there is currently no active reference/comparison machine.
- Stephan believes the relevant Puppet manifests already exist; setting up a new machine and enabling the existing Puppet config/manifest should, in principle, be sufficient to reproduce the production configuration.
- Marco summarized the resulting action item as: work with Gregor to confirm a test machine is ready and identified for this purpose, then configure and enable it per Stephan's description.

### Schedd (SCADI) updates and site tokens (Luis)

- Luis updated one PNR-associated schedd ("SCADI") to the patched version 24.0.22 early in the week; the remaining schedds are on hold pending test confirmation from PNR before further upgrades proceed.
- Luis asked how to coordinate with the PNR team; Marco suggested using the existing Mattermost thread involving Kiril and Gregor. Marco also noted he will be on vacation starting the following Monday, and pointed to the COMPOPS meeting (Mondays at 5) as an alternative place to get updates in his absence.
- On the site-tokens migration: more than half of the ARC CEs are already using site tokens. Luis characterized these as the "easy" cases (tests passing cleanly) and is now working through sites where tests are failing and pilots can't run with site tokens yet, opening tickets one by one; he expects this to take a while.
- One remaining site (an opportunistic Tier-3) is pending push to the OSG Factory repository, held back until Luis confirms it's working; CERN and another site ("Tiger", name possibly a transcription artifact) have been working well so far.

### Global pool query load from ITB dev front end (Marco)

- Marco noted the ITB dev testing setup uses the global pool (rather than a separate test pool), which he said was inherited/unclear in origin.
- While running 3.11.4 tests, the ITB dev front end was found to be hammering the global pool collector with a much higher number of queries than expected — roughly a 4x increase (from about 80 queries per 12 minutes to around 320), pushing the collector's duty cycle up to roughly 0.8, close to the ceiling of 1.
- Marco noted the combined effect of increased CRAB (single-core) job load plus the ITB front end being enabled pushed the duty cycle close to 1, though it remained manageable on the day observed.
- Marco recalled having previously worked on tickets to reduce this kind of query volume and suspects something regressed; he plans to investigate and open a new ticket.
- Marco flagged this is something to be careful about going forward, since he had not realized the front end was this heavy on the collector, and suggested production's front end may operate at a lower duty cycle than what was observed here.

## Open Questions

- What the mechanism is that populates the `MetricLID`-type attribute used to identify where a CMS job ran (Marco needs to verify against the SCADI configuration/collector code and consult Marco Mambelli).
- Why the ITB dev front end's query volume against the global pool increased so significantly, and whether a prior fix for this regressed.
- Whether the WMAgent robot-certificate/grid-mapfile fix actually resolves the failure once Gregor retests it.
- Timeline for resolving the ongoing CRAB/HammerCloud-related emergency activity contributing to load at the Fermilab Tier-1.

## Related

[[glideinWMS]] · [[HTCondor]] · [[CRAB]] · [[WMAgent]] · [[Submission Infrastructure]] · [[Factory Operations]] · [[CAP]] · [[OSG]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-30 16.09.22 Submission Infrastructure Weekly Meeting`)
