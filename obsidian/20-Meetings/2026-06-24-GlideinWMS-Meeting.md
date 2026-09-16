---
type: meeting
date: 2026-06-24
participants:
  - Marco Mascheroni
  - Namratha Urs
topics:
  - GlideinWMS 3.11 to production (3.12) promotion planning
  - Site-token vs. grid-proxy authentication migration (CERN, IN2P3, MIT, Fermilab)
  - Factory support for combined site-token + grid-proxy configuration
  - CVMFS mount-list eval() security advisory (PR #678)
  - Decision engine issue #206
  - GlideinWMS issue #679 (X509 proxy verification script error)
  - Glidein log access for factory ops
---

# GlideinWMS Meeting

## Summary

This was a GlideinWMS development/status meeting. Note: the transcript (auto-generated closed captions) is heavily garbled for one recurring speaker, whose Zoom label appears only as "[WH8XE- Quarium]"; this speaker was addressed once by Namratha Urs as "Peter," but the identification is uncertain and is not otherwise confirmed in the transcript, so this person is not listed as a named participant below. The bulk of the discussion concerned the migration from grid-proxy to site-token authentication ahead of promoting GlideinWMS 3.11 to production (as 3.12): several sites (IN2P3, MIT) were reported to have authentication or mapping problems after factories switched to token-only submission, and Marco Mascheroni described a still-unpushed local change enabling site-token authentication for the CERN factory. The group also discussed whether a factory configuration could be made to send both a grid proxy and a site token to a site simultaneously, to smooth the 3.10/3.11 transition, and agreed on tests to verify this. A security advisory was reported: an unsanitized variable (the list of CVMFS repositories to mount) is used in an `eval` in a script, creating a potential code-injection path; a patch has already been merged into master (PR #678). Namratha Urs gave a round-table update on her investigation into GlideinWMS issue #679, a factory-ops-reported X509 proxy verification script error that she has not yet been able to reproduce.

## Decisions / Conclusions

- In GlideinWMS 3.11, a site's factory-configuration authentication method supports only one credential type at a time (grid proxy or site token, not both); this differs from 3.10, which — per the discussion — allowed sending both via workarounds/tweaks in the 3.10 front end. This behavior change is understood to be the source of recent site breakages after factories were flipped to token-only.
- CERN's factory has been switched to site-token authentication as a local (uncommitted) change; it was previously kept on grid-proxy because of a front-end/factory security-class mismatch bug, which has since been fixed and verified locally. Marco Mascheroni will coordinate with Luis (factory ops) to push this change.
- IN2P3 (CNRS) was reported to have CMS jobs landing in an unmapped/opportunistic queue rather than running, apparently because two front ends are sending tokens to it and the site is not mapping the site token correctly; the IN2P3 factory entry had reportedly not yet been switched to site-token authentication at the time of this report. MIT was separately reported to authenticate successfully via site token but not map correctly.
- Fermilab's factory is being deliberately kept on proxy authentication for now due to unresolved issues.
- A security vulnerability was confirmed: a variable holding the list of CVMFS repositories to mount is not sanitized before being used in an `eval` in a script, which could allow a job that tampers with its CVMFS mount-list to trigger code injection. A fix has already been merged into master and is available via PR #678 (replace the Singularity-wrapper script with the patched version, then perform a factory upgrade/dispatch). This affects both 3.10 and 3.11 factories.

## Action Items

- [ ] Coordinate with Luis (factory ops) to push the CERN site-token authentication configuration change — Marco Mascheroni
- [ ] Verify whether a factory configuration listing both grid proxy and site token as authentication methods causes both credentials to be sent to the site — Marco Mascheroni
- [ ] Test the old (3.10) ITB front end against the combined proxy+token factory configuration, and consider also upgrading ITB to the new (3.11) front end to test that combination — Marco Mascheroni
- [ ] Spin up a 3.11 GlideinWMS factory/front-end testbed and connect the existing 3.10 front-end testbed container to the new 3.11 factory, to test authentication-configuration compatibility across front-end versions, and report results back to Marco Mascheroni — Namratha Urs
- [ ] Apply the PR #678 patch (replace the Singularity-wrapper script) to the 3.10 and 3.11 factories and perform a factory upgrade/dispatch — Marco Mascheroni
- [ ] Continue investigating GlideinWMS issue #679 (X509 proxy verification script error) and attempt to reproduce it, including trying scenarios such as the front end failing to deliver an updated token while the factory keeps submitting, or removing/deleting the front end's SSH key (used to sign ID tokens shared with the collector) while the front end is running — Namratha Urs
- [ ] Follow up with Jeff for glidein logs relevant to issue #679 (already contacted via Slack; no response yet as of this meeting) — Namratha Urs

## Discussion

### Release planning (opening remarks)
The meeting opened with a brief discussion about upcoming release planning — identifying which features should be included before closing out a release — but the transcript for this segment is too garbled to reliably reconstruct specifics (references to release/version numbers were unclear).

### Site-token vs. grid-proxy authentication migration
A factory-side change recently flipped several factory entries from proxy-only to site-token-only authentication (moving away from a long-standing legacy configuration). This surfaced several site-specific issues:
- IN2P3 (CNRS): CMS jobs were reported going into an unmapped/opportunistic queue — submitted but not running well — apparently because two front ends were sending tokens and the site was not mapping the site token correctly. There was some back-and-forth about whether the IN2P3 (OSG factory) entry had actually been switched to site token yet; it was noted that if a group ("GP49," per the transcript) falls back to the 3.11 configuration, it would not be able to submit to CERN, which would be a problem — though Marco Mascheroni clarified CERN had already been switched to site token that week.
- MIT: authentication succeeded but the site token was apparently not being mapped correctly.
- CERN: kept on grid-proxy for a period specifically because of a known bug where the front-end and factory security classes did not match after an earlier attempt to switch to site-token authentication; this bug has since been fixed and verified in a local test, but the change has not yet been committed/pushed to the shared factory configuration.
- Fermilab: deliberately still kept on proxy authentication due to separate, unresolved issues.

The recurring speaker (unidentified) explained that GlideinWMS 3.11's factory configuration only sends one authentication method per site (proxy or token, not both) — unlike 3.10, where a proxy-based site could still receive tokens due to tweaks/workarounds in the 3.10 front end that made token support effectively an add-on. Because of this, upgrading a site's factory entry to the new syntax without adjusting for both credential types risks breaking sites that were relying on the older mixed behavior.

### Testing combined site-token + grid-proxy configuration
It was proposed that the factory configuration could specify both a site token and a grid proxy for a given site (e.g., `site token, proxy`) so that the factory sends both, giving old and new front ends compatible credentials during the transition. Marco Mascheroni agreed to verify this. Namratha Urs volunteered to build a testbed: spin up a GlideinWMS 3.11 factory/front-end setup (via testbed compose, using the upcoming-series RPM) and connect it to her existing 3.10 front-end testbed container, to check whether the two syntaxes (new combined-config style vs. older 3.10-style) are compatible with both factory versions. It was noted there may be some tweaking needed to find a configuration that satisfies both the old and new front end simultaneously, and that this was not yet confirmed to work.

### Security advisory: CVMFS mount-list eval() vulnerability
A variable containing the list of CVMFS repositories to mount is not sanitized before being passed into an `eval` in a script. A job that tampers with its own CVMFS-repo mount list could potentially trigger code injection as a result. The fix has already been merged into master; it can be applied to existing 3.10 and 3.11 factories by replacing the affected Singularity-wrapper script with the patched version from PR #678 and performing a factory upgrade/dispatch. The attack was described as unlikely but possible. Marco Mascheroni acknowledged the issue and indicated he would look at patching the Fermilab factories.

### Decision engine issue #206
The recurring (unidentified) speaker reported that a fix for decision-engine issue #206 is still not ready; the code fix is reportedly done, but supporting evidence/verification still needs to be built. This was deprioritized behind other current work.

### Round table
- Marco Mascheroni: nothing to report.
- Namratha Urs: has been investigating GlideinWMS issue #679, an error reported by factory ops from the X509 proxy verification script. She has not yet been able to reproduce the error and has been reviewing the codebase for clues. She reached out to Jeff via Slack the previous day asking for glidein logs but had not yet received a response. The recurring speaker noted the issue occurred while there were intermittent (not total) network problems affecting the Kubernetes cluster running the OSG factory, and speculated the front end's ID token (used by glideins to connect back, generated by the front end signing with an SSH key shared with the collector) may not have been available/valid at the relevant moment. Suggested reproduction attempts included: forcing the front end to fail to deliver an updated token while the factory continues submitting jobs, or deleting the front end's SSH key file while the front end is running (which reconfig is known to check for and fail on if missing). Namratha noted the `check_proxy` script logs an "ID token found and continuing" message at the end of a successful run, and she wanted to see whether that message appeared in the logs from the incident Jeff reported, as a clue to what happened. It was suggested that if the issue cannot be reproduced after further effort, the team might instead harden the relevant code defensively and monitor for recurrence, since the triggering network conditions were unusual.
- Separately, the recurring speaker mentioned having previously asked Jeff (a couple of weeks earlier) whether GlideinWMS logs could be published to a web server; Jeff was not sure this was possible but had offered to give a few key people direct login access to view logs themselves, to avoid needing to file a ticket every time a log needs to be checked.

## Open Questions

- Has the IN2P3 factory entry actually been switched to site-token authentication, and if so, why is CMS job mapping still failing there?
- Why is MIT's site token authenticating successfully but not mapping correctly?
- Can a factory configuration specifying both grid proxy and site token actually deliver both credentials to a site, and is there a syntax that works consistently across both 3.10 and 3.11 front ends?
- What exactly caused the GlideinWMS issue #679 X509 proxy verification error, and can it be reproduced?
- Will Jeff be able to share relevant glidein logs (or provide direct log access) for investigating issue #679?

## Related

[[glideinWMS]] · [[HTCondor]] · [[SciTokens]] · [[CVMFS]] · [[Factory Configuration]] · [[Factory Operations]] · [[CMS]] · [[CERN]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-06-24 17.04.47 GlideinWMS Meeting`)
