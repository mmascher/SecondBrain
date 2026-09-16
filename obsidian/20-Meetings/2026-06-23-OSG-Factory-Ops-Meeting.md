---
type: meeting
date: 2026-06-23
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Luís Simas
  - Hyunwoo Kim
topics:
  - Wisconsin/Tiger cooling failure and network incident
  - CMS offline/computing face-to-face management meeting readout
  - Phase 2 HL-LHC CPU efficiency and high-memory jobs
  - Run 3 completion and Tier-0 prompt reconstruction
  - P5/HLT farm resource relocation
  - Condor CE site-token migration at CERN
  - MIT Tier 2 site-token mapping issue
  - Pilot submission rate tuning
  - Historical AlmaLinux 9 / OpenSSL HTCondor auth issue
---

# OSG Factory Ops Meeting

## Summary

Jeff Dost opened with an update on a cooling failure at Wisconsin the previous week that made the Tiger factory unavailable for a period; recovery is mostly complete aside from some residual network issues, and a specific classad anomaly (an empty, rather than missing, glidein Condor token path) is still not fully explained. Marco Mascheroni reported back from a CMS offline/computing face-to-face management meeting, covering a Submission Infrastructure (SI) status presentation, a possible reorganization of the dynamic resource provisioning coordination area, CPU-efficiency concerns tied to Phase 2 of the HL-LHC, the end of Run 3 (with Tier-0 prompt reconstruction continuing for a couple more months), a fair-share reversion, and a resource relocation involving the P5/HLT farm. Luís Simas reported that the Condor CE site-token migration is effectively concluded for the CERN factory (pending a short validation period before publishing to the Git repository), but that MIT reported reduced usage and idle cores after a related change, traced to only one of three factories still being able to submit pilots to two of MIT's CEs — believed to be a token-subject-to-local-user mapping issue on MIT's side, still pending. The group also discussed slow pilot submission rates as a possible general problem (using MIT and the CERN Tier 2 as examples) and revisited a historical AlmaLinux 9 / OpenSSL issue that had broken HTCondor authentication between factories and the CA.

## Decisions / Conclusions

- The Wisconsin cooling failure made the Tiger factory unavailable for a period; most things have recovered, though some network weirdness remains. The only front end noticeably affected was the UCSD CMS front end (also hosted on Tiger); the OSG pool, also on Tiger, was less noticeably affected because it restarts frequently.
- During the incident, a glidein Condor token variable on the factory side (expected to hold the path to a token sent from the front end) was observed as an empty string rather than missing. Jeff Dost believes the front end was unable to refresh and send ID tokens to the factory, but the root cause is unconfirmed and tied to unexplained Tiger networking problems; it will be hard to diagnose further unless it recurs.
- Jeff Dost understands a temporary patch was applied on the Tiger Kubernetes side to restore networking for the factory, though he does not fully understand the underlying fix, which was handled behind the scenes on the Tiger cluster.
- At the CMS offline/computing face-to-face management meeting, a possible reorganization was discussed in which the dynamic resource provisioning area (which helps set up and connect European HPC resources via glideinWMS "in a vacuum," and also covers management of the CERN HLT farm using the same strategy) could shift from being a level-2 area to a level-1 area, potentially becoming a sub-area of Submission Infrastructure, since Daniele (the current level-2 lead for that area) is moving to a level-1 role. No clear decision was reached on this reorganization.
- CPU efficiency and high-memory jobs were discussed as a concern for Phase 2 of the HL-LHC: more high-memory jobs are expected, without a corresponding increase in high-memory-capable resources or workforce.
- Run 3 (LHC) is over; CMS will continue processing data for a couple of months via Tier-0 prompt reconstruction jobs.
- The Tier 0 fair share, previously increased temporarily to handle an emergency, has been reverted back to the default shares.
- A site relocation is underway: the resources associated with the CH5 site are being physically moved to P2 and will be hosted by ALICE, requiring a new site configuration and wrapper. The current HLT farm is expected to become "P5," with a new HLT commissioning resource used when there is no data taking. (The transcript's description of this resource shift was not fully clear; the general gist — a physical relocation of CERN HLT-related resources and a change in which site name/role applies — is preserved here with that caveat.)
- The Condor CE site-token migration is essentially concluded on the CERN factory: Luís Simas fixed a wrong "security class" value on the Tier 0 front end (which had caused pilot requests to fail, though the factory itself never actually submitted), updated the front-end configuration, validated the change on one CERN factory entry, then flipped the remaining entries. This is applied locally on the CERN factory only and has not yet been published to the Git repository; Luís wants to leave it unpublished for one to two days to confirm stability.
- Separately, an incorrectly configured ID token on the CERN Tier 0 front end (which had prevented it from requesting pilots from the Fermilab factory) is also now fixed.
- After the site-token changes, the Tier 2 site admin at MIT (Max) reported lower usage and many idle cores. Investigation showed that for two of MIT's CEs, the Tiger and CERN factories were no longer able to submit pilots, leaving only the Fermilab factory contributing. The site admin found that the likely cause is an error in how MIT's Condor CE maps the token subject to local users; this is still pending resolution on MIT's side (a ticket is open).
- Marco Mascheroni instructed Hyunwoo Kim to wait and not touch the Fermilab factory until the MIT mapping issue is fixed, since it is currently the only factory still able to submit pilots to MIT. Jeff Dost agreed with holding off.
- Luís Simas noted that during the CERN incident (from the wrong security-class value), it took roughly eight-plus hours to regain full capacity at the CERN Tier 2 after the pool deflated.
- Regarding a historical MIT issue Hyunwoo Kim found in old logs (involving delegating job GSI credentials), Marco Mascheroni clarified it was unrelated and was actually the earlier OpenSSL/proxy issue: when AlmaLinux 9 updated OpenSSL to a newer major version (the exact version was uncertain in discussion, tentatively around 3.x), a change in OpenSSL broke HTCondor authentication between the factory and the CA. The fix was an HTCondor flag to disable proxy delegation, avoiding the problematic part of OpenSSL. Marco described it as "not a fun week."

## Action Items

- [ ] Publish the CERN factory site-token configuration to the Git repository, after a one-to-two-day local validation period — Luís Simas
- [ ] Hold off updating the Fermilab factory's auth method / MIT entries until the MIT token-mapping issue is resolved; revert the CERN/Tiger-related change for the affected MIT entry if the site admin doesn't fix it soon — Luís Simas
- [ ] Hold off making Fermilab factory auth-method changes for MIT entries until given the OK — Hyunwoo Kim
- [ ] Add a note/reminder to check back next week on the MIT token-mapping issue — Jeff Dost

## Discussion

### Wisconsin/Tiger cooling failure and network incident

Jeff Dost reported another cooling failure at Wisconsin the previous week that made the Tiger factory unavailable for a period. Most things have since recovered aside from some residual network weirdness. The UCSD CMS front end, also hosted on Tiger, was the only front end noticeably affected; the OSG pool (also on Tiger) likely wasn't noticed as affected because it restarts frequently anyway. Jeff continued a discussion with Marco Mambelli about a specific anomaly: a glidein Condor token variable expected to hold the path to a token sent from the front end to the factory was present but held an empty string rather than being missing. Marco Mambelli is reportedly looking at adding protections for this scenario, but reproduction is difficult since the cause is believed tied to the still-unexplained Tiger networking issue. Jeff's best guess is that the front end was unable to refresh and send ID tokens to the factory during the incident. He understands a temporary patch was applied on the Tiger Kubernetes side to fix the networking for the factory, but does not fully understand the underlying long-term fix, which appears to have been handled behind the scenes on the Tiger cluster.

### CMS offline/computing face-to-face management meeting readout

Marco Mascheroni reported on a CMS offline/computing face-to-face management meeting from the previous week, which included a presentation on Submission Infrastructure (SI) manpower, status, needs, and future plans (a link was shared in the meeting chat). Separately from that presentation, he raised a possible reorganization: the dynamic resource provisioning area — which covers helping most European HPC sites connect to the CMS pool (typically via glideinWMS "in a vacuum") and also covers managing the CERN HLT farm with the same strategy — might shift from being a level-2 to a level-1 coordination area, potentially becoming a sub-area of Submission Infrastructure, since Daniele (currently level-2 lead for that area) is moving into a level-1 role. No clear decision was reached on this.

Marco also relayed discussion of CPU efficiency and the expectation of more high-memory jobs for Phase 2 of the HL-LHC, without a corresponding increase in high-memory-capable resources — flagged as worth keeping in mind. He noted Run 3 is now over, though CMS will continue processing data via Tier-0 prompt reconstruction jobs for a couple more months.

On more routine items, Marco reported the Tier 0 fair share (previously increased temporarily during an emergency) has been reverted back to the default shares. He also described a resource relocation: the CH5 site's resources are being physically moved to P2 and will be hosted by ALICE, requiring a new site configuration and wrapper; the current HLT farm is expected to become "P5," with a new HLT commissioning resource used when there is no data taking. This portion of the transcript was difficult to follow precisely, so the details are preserved here with that caveat.

### Condor CE site-token migration and CERN/MIT issues

Luís Simas reported that last week's Tier 2 CH CERN entries issue — caused by a wrong "security class" value on the Tier 0 front end, which stopped pilot requests (though the factory itself never actually submitted) — is now fixed. He updated the front-end configuration, validated the site-token change on one CERN factory entry, then flipped the rest. This is applied locally on the CERN factory only and has not yet been published to the Git repository; he wants to leave it that way for one to two days to confirm everything is running fine. With that, he considers the CERN move to site tokens effectively concluded. Separately, an incorrectly configured ID token on the CERN Tier 0 front end (which had prevented it from requesting pilots from the Fermilab factory, discussed the previous week) is also now fixed.

One consequence of the site-token change: the MIT Tier 2 site admin (Max) reported lower usage and a lot of idle cores. Investigation found that for two of MIT's CEs, the Tiger and CERN factories were no longer able to submit pilots after the change, leaving the Fermilab factory as the sole contributor to that site. The site admin opened a ticket and identified a likely cause: an error in how MIT's Condor CE maps the token subject to local users. This remains pending. Marco Mascheroni told Hyunwoo Kim to hold off touching the Fermilab factory until this is resolved, since it is currently the only factory able to submit to MIT; Jeff Dost agreed. Luís noted he would revert the change for the specific affected MIT entry if the site admin doesn't fix the issue soon, and that the factories would need to be re-synced and tested together with Hyunwoo afterward.

Luís also noted that during the CERN incident, it took roughly eight-plus hours to regain full capacity at the CERN Tier 2 after the pool deflated, which he connected to the broader submission-rate discussion.

### Pilot submission rate tuning

Marco Mascheroni raised that the Fermilab factory alone is not filling MIT fast enough. He explained that per-entry submission speed in the factory XML is controlled by two parameters: how many jobs are submitted per `condor_submit` call, and how long the factory sleeps between successive `condor_submit` calls. He recalled increasing the submission rate for MIT roughly three months ago, but believes this may have only been applied to one of MIT's CEs, leaving the other two with older, slower rates. Jeff Dost recalled a related complaint from the MIT admin (Max) roughly six months ago about the site not being filled, though he was unsure whether that was linked to the proxy-versus-site-token issue.

Marco proposed re-evaluating submission rates more generally, potentially via a script that checks each site's size (e.g., entries above a 5–10K job threshold) and derives appropriate rate parameters, possibly with a target such as filling a site within six hours. Jeff Dost questioned how to determine a site's true size without already filling it, and suggested checking historical data (e.g., in MONIT/Elasticsearch) as one option, though he noted this may not tell the full story. He distinguished this from the MIT problem specifically — MIT's issue is about the pool never reaching capacity at all, not about the time it takes to fill an already-reachable capacity, which he considered a different question. As a possible signature of under-filling a site, Jeff suggested checking the ratio of running-to-idle jobs: a persistently very low idle count relative to running (pilots transitioning to running almost immediately) could indicate the site isn't actually being filled to capacity, which matched the pattern seen at MIT. Marco agreed this was worth investigating further, suggesting a possible follow-up discussion in the next meeting and floating the idea of a quick one-off script (potentially with Luís) to check submission-rate signatures like this while the MIT/CERN cases are still fresh. This remained a proposal; no firm commitment or owner was agreed for the script itself.

### Auth method changes at Fermilab and historical OpenSSL issue

Hyunwoo Kim asked whether he should proceed with previously discussed auth method changes for the Fermilab factory (updating remaining MIT entries to the newer auth method). Marco Mascheroni said to hold off, since the Fermilab factory is currently the only one able to submit to MIT, until the MIT mapping issue is better understood; Jeff Dost agreed, noting the other two factories already use the correct auth method, so there is enough redundancy for other sites even with a few Fermilab entries left on the older method. Jeff said he would add a note to check back on this next week.

Separately, Hyunwoo Kim, while reviewing old logs, found a historical MIT-related issue whose noted solution involved delegating job GSI credentials. Marco Mascheroni clarified this was unrelated and referred to an earlier, separate issue: when AlmaLinux 9 updated OpenSSL to a newer major version (uncertain exact version, discussed tentatively as around 3.x), the change broke HTCondor authentication between the factory and the CA. The fix at the time was an HTCondor flag to disable proxy delegation, avoiding the problematic part of OpenSSL. Marco described that week as disruptive ("everything broke that week").

## Open Questions

- What exactly caused the Tiger networking issue that led to the empty glidein Condor token classad, and how to reproduce or protect against it — unresolved; Marco Mambelli is investigating possible protections.
- The precise details of the CH5/P2/P5/HLT resource relocation were not fully clear from the discussion.
- Whether the dynamic resource provisioning area will actually be reorganized into a level-1 sub-area of Submission Infrastructure — no decision reached.
- The root cause and fix timeline for MIT's Condor CE token-subject-to-local-user mapping issue — pending on MIT's side.
- How to reliably estimate a site's true capacity/size in order to calibrate pilot submission rates, and what general rule(s) to use (e.g., target fill time) — open, proposed for further discussion in a future meeting.
- The exact OpenSSL version involved in the AlmaLinux 9 HTCondor authentication break was not confirmed in the discussion.

## Related

[[OSG]] · [[CMS]] · [[HTCondor]] · [[glideinWMS]] · [[Kubernetes]] · [[CERN]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Submission Infrastructure]] · [[Dynamic Resource Provisioning]] · [[AlmaLinux]]

## Source

meeting_saved_closed_caption.txt (from `2026-06-23 17.10.54 OSG Factory Ops Meeting`)
