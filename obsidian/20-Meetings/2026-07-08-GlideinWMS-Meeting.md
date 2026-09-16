---
type: meeting
date: 2026-07-08
participants:
  - Marco Mascheroni
  - Jeff Dost
  - Jason C Patton
  - Ken Herner
  - Shreyas Bhat
  - Gideon Appia
topics:
  - Summer project: Prometheus/Grafana instrumentation for GlideinWMS factory observability
  - Known bugs in 3.10/3.11 (custom-logging reconfig, ID-token generation, credential submission failures, factory monitoring SDK)
  - Custom-script timeout change (10 minutes)
  - GlideinWMS release/versioning roadmap (3.10, 3.11, 3.12)
  - Security hardening (GitHub Actions permissions, Singularity-invocation sanitizer fix)
  - On-demand CVMFS (CFS) provisioning and Glidein startup refactor
  - Password-protected SSH credential support
  - Pool index credential-syntax deprecation discussion
  - Python version roadmap (dropping SL7/Python 3.6, considering Python 3.12)
  - Front-end high-availability (HA) behavior
  - DiracX / CMS transformation-system integration update
  - Data-aware matchmaking (Fermilab retreat follow-up)
---

# GlideinWMS Meeting

## Summary

This was the periodic GlideinWMS stakeholders meeting. As in other transcripts from this recording setup, one recurring speaker appears only under the Zoom label "[WH8XE- Quarium]"; this label likely represents a room or shared endpoint used by the meeting's host/facilitator rather than a single named individual, so no name is attributed to this speaker below beyond noting their role as the meeting's presenter. Gideon Appia, a summer student (described as a rising junior at Grambling State University, per the transcript's "Granblade State University"), gave a project update on instrumenting GlideinWMS factory operations with Prometheus and Grafana; he said his mentors are "Marco and Namrata" (likely Marco Mascheroni and Namratha Urs, though this is not confirmed by direct participation of a "Namrata"/Namratha Urs in this transcript). The facilitator then covered known bugs, a recent behavior change (custom-script timeouts), the release/versioning roadmap, recent security hardening, 3.11 migration notes, in-progress feature work (on-demand CVMFS provisioning, password-protected SSH credentials), and two open questions for stakeholders (deprecating the "pool index" credential syntax, and moving to Python 3.12). The meeting closed with a round table: Jason C Patton (LIGO) asked about front-end high-availability behavior; Ken Herner asked about Superfacility API/HPC integration testing; and Marco Mascheroni gave updates on a conversation with DiracX developers about integrating HTCondor/GlideinWMS into the CMS DIRAC-based workflow system, and on his assignment (from a recent Fermilab retreat) to work on data-aware matchmaking.

## Decisions / Conclusions

- The double-reconfig bug affecting custom Glidein logging (requiring `reconfig` to be run twice when custom logging is first enabled) has already been fixed in code but not yet included in a release.
- In 3.10, if the front end's signing key is missing or corrupted, ID tokens cannot be generated, but the front end keeps running and only prints a warning; this is suspected to be the cause of a prior incident (referred to in the transcript as the "OG"/"OSG" Kubernetes network/auditor problem — network issues on the OSG-factory Kubernetes cluster are believed to have prevented ID tokens or associated data from reaching the factory). In 3.11, this same condition instead raises an error — described as the intended, desired behavior. There is currently no plan to back-port this error behavior to 3.10.
- Production versions now enforce a 10-minute timeout on custom scripts, implemented via a watchdog process that runs in parallel to the custom script and kills it if it exceeds the timeout; VOs needing longer custom-script runtimes must set the plugin custom-script timeout variable accordingly. Seeing a `sleep` process running alongside a custom script (visible via `ps`) is expected/normal and not a concern.
- A security fix restricting GitHub Actions permissions for GlideinWMS CI has already been applied, in response to reports of GitHub repositories being compromised via automated scripts/actions; CI workflows no longer have write access to modify code.
- A security fix has been merged (patch available on GitHub, to be included in the next release) for an unsanitized variable used when invoking Singularity, which could otherwise have allowed code injection.
- Running a 3.11 front end requires a 3.11 factory; factories remain compatible with both 3.10 and 3.11 front ends. Front ends being updated to 3.11 must replace `proxy` with `credential` in the security-section configuration for the plugin; a warning message has been added to `reconfig` to flag this.
- 3.11.5 (next development release) is planned to include MyCFS/on-demand-CVMFS provisioning support (already under review and "almost merged") and password-protected SSH-key credential support for remote-cluster submission (used by default with password-protected keys); this work also expanded the test environment to cover passcode-protected credential submissions.
- The Glidein startup process has been refactored to support full on-demand CVMFS provisioning: a new utility, `cvmfsexec` (transcribed as "CFS exec"), must be the parent process of everything using the CVMFS mount. This produced a second, rearranged "Glidein tab" version with an external part that runs first and an internal part spawned after `cvmfsexec` is invoked; this variant is only used when on-demand CVMFS provisioning is enabled via the feature flag added in the previous version. Both the old and new startup paths will be supported side by side.
- Regarding a change of authentication method (X.509 proxy → site token, or similar) at CERN this month: Marco Mascheroni reported that after removing an unused X.509 proxy credential and running `reconfig`, the previously failing submission to some site(s) started working, though the root cause (why having multiple/unused credentials configured caused the problem) could not be reproduced or fully explained.
- Regarding a related factory-monitoring issue (the "stern" factory monitoring / status XML not reporting existing pilots after an entry's auth method is updated), Marco Mascheroni confirmed this appears to occur only when the authentication method is changed, that the status XML recovers and ramps back up after a period, and that CMS considers this low priority and something the team is willing to live with; a ticket has been filed to track it as a known issue.
- CMS (Marco Mascheroni) and LIGO (Jason C Patton) both confirmed they no longer use, or are unfamiliar with, the "pool index" credential-collection syntax (a shorthand for referencing multiple same-type credential files, e.g. `proxy0002`, `proxy0004`, etc., via a suffix/range syntax in a single configuration line, historically used for X.509 proxy rotation and analysis/production fair-share splitting). Both indicated it would be fine to deprecate/remove it. The presenter plans to send an email to the stakeholders list for final confirmation before deciding, and separately noted uncertainty about whether the feature was correctly ported during the credential-handling refactor, and whether it currently works consistently for token-based credentials (it was originally designed for X.509 only).
- No SL7/Python 3.6 users were reported among stakeholders present (Jason C Patton for LIGO/OSG and Marco Mascheroni for CMS both confirmed no SL7 usage); dropping Python 3.6/SL7 support in the next major series is planned, pending a confirmation email to the full stakeholders list.

## Action Items

- [ ] Send an email to the stakeholders list to confirm whether the "pool index" credential-collection syntax is used anywhere before deciding to deprecate/remove it
- [ ] Send an email to the stakeholders list to confirm that no one is running GlideinWMS 3.10 factories on SL7/Python 3.6, ahead of dropping that support
- [ ] Send a separate email opening discussion on moving the 3.11/3.12 series reference/minimum Python version to 3.12
- [ ] Follow up on what LIGO specifically needs regarding front-end high availability, beyond the existing HA-style behavior — Jason C Patton
- [ ] Prepare material on data-aware matchmaking (the topic assigned at the recent Fermilab retreat) and discuss it, possibly at a future GlideinWMS meeting — Marco Mascheroni

## Discussion

### Summer project: Prometheus/Grafana factory observability (Gideon Appia)
Gideon Appia, a summer student, is working on improving observability of GlideinWMS factory operations via Prometheus instrumentation, mentored by "Marco and Namrata." Motivation: factory statistics currently rely on ground/relational databases plus XML and JSON files, which limits integration with modern observability platforms. The project investigates exposing factory metrics via Prometheus using OpenTelemetry principles, and integrating with Grafana for visualization through Fermilab's existing landscape monitoring infrastructure. Progress so far: a containerized GlideinWMS environment (factory, front end, CE) was set up; the factory/front-end/CE architecture and codebase were studied; a local Prometheus development environment was built (a Python test app instrumented with the Prometheus client library, plus a local Prometheus server); and integration of Prometheus into the factory itself is in progress. Remaining goals: finish factory instrumentation (targeted for later that week) and integrate Grafana for visualization.

### Known bugs and investigations
- Custom Glidein logging double-reconfig bug: fixed in code, not yet released.
- 3.10 ID-token generation failure on missing/corrupted signing key: front end silently continues with only a warning (suspected cause of a prior OSG-factory Kubernetes network incident); 3.11 raises an error instead, which is considered the desired behavior going forward.
- 3.11 credential submission investigation: the 3.11 front end at Fermilab, configured with both X.509 and site-token ("cytokine"/SciToken) credentials, was not submitting to some site(s); removing an unused X.509 proxy credential and running `reconfig` resolved it. The team could not reproduce the issue or fully explain why the extra/unused credential caused a problem, and it remains under investigation ("temporary freezing" was mentioned as a related symptom, without further detail in the transcript).
- Factory ("stern") monitoring/status-XML issue: after an entry's auth method is updated, existing pilots stop being reported for a period before recovering. Marco Mascheroni noted this appears tied specifically to auth-method changes, self-recovers, and is considered low priority; a ticket exists to track it.

### Release/versioning roadmap
Current development series: 3.10.18 and 3.11.4 released so far (as stated: "produced 3.10, 3.11.4 currently"). Next expected releases: 3.10.19 and 3.11.5. Depending on how adoption of the 3.11 front end progresses, the plan is to promote 3.11.5 to become 3.12.0. Reported adoption status among those present: the OSG front end ("USG"/OSG Match) and the Fermilab 3.11.4 front end are running 3.11.4; CMS is still on 3.10; LIGO is still on 3.10. Marco Mascheroni said CMS plans to test 3.11 in the ITB (integration test bed) environment but has no firm timeline yet, as another ITB change is queued ahead of it. Current development focus is on hardening the 3.11 series for wider adoption and prioritizing closing GitHub issues, alongside adding new features. Planned 3.11 features include full CFS-exec (on-demand CVMFS) support, controlling SSH jobs inside containers, and expanded HPC-site submission support. Stakeholders migrating to 3.11 were invited to reach out for live support during the transition.

### Security hardening
- GitHub Actions CI permissions were restricted (CI can no longer modify/write code) in response to reports of compromised GitHub Actions/automated scripts affecting other repositories.
- A variable used when invoking Singularity was found to be unsanitized, creating a potential code-injection path; a patch is available on GitHub and will be included in the next release.

### On-demand CVMFS (CFS) provisioning and Glidein startup refactor
To support full on-demand CVMFS provisioning, the Glidein startup sequence was refactored around a new `cvmfsexec`-based utility that must be the parent process of anything using the CVMFS mount. This produced a second variant of the Glidein startup ("tarball"/tab) — used only when on-demand CVMFS provisioning is enabled via a feature flag introduced in the previous release — with an external part running first, and an internal part spawned after `cvmfsexec` is invoked. Both the legacy and new startup variants will be supported, selectable via the feature flag.

### Pool index credential syntax (stakeholder question)
The presenter asked whether anyone still uses "pool index," a credential-specification feature allowing a single configuration line to reference multiple credential files of the same type via a numeric suffix/range syntax (e.g., referencing `...0002`, `...0004`, `...0005`, `...0006`), historically useful for X.509 proxy rotation and for splitting fair-share allocation between analysis and production pools by mapping to different users. Marco Mascheroni recalled CMS used this in the past (before he joined the project) to split fair share between an analysis pool and a production pool, but CMS has since moved to doing this centrally via Condor Negotiators instead, which he described as a better approach; CMS no longer needs the feature and is fine removing it. Jason C Patton confirmed LIGO does not use it and did not find it in the OSG pool configuration either. There is uncertainty about whether the feature was correctly carried through the recent credential-handling refactor and whether it works consistently with token-based credentials (it was originally designed for X.509). The presenter plans to email the full stakeholders list before finalizing the decision to deprecate/remove it, and separately planned to check with Fermilab about front-end usage.

### Python version roadmap
Currently, the 3.10 series references/defaults to Python 3.9 but also supports Python 3.6 on SL7, as well as Python 3.9–3.12 on Alma 8/9. The 3.11 series has the same Python 3.9 reference but supports Python 3.9–3.12 on Alma 8/10. Once 3.10 enters maintenance mode, the plan is to drop Python 3.6/SL7 support going forward (bug-fix-only releases, no new features expected for 3.10). No stakeholders present reported running 3.10 factories on SL7/Python 3.6; a confirmation email will still be sent to the full list. Separately, the presenter raised moving the 3.11/3.12 series' reference (and possibly minimum-supported) Python version to 3.12, since Python 3.9 is becoming deprecated by linters/formatters, and 3.12 is available upstream, on Alma, and is the EL10 default. Options discussed included continuing to rely on the OS/system Python (with multiple Python versions coexisting per-RPM) versus providing a virtual environment with a newer Python version bundled with the service. Marco Mascheroni (CERN, currently on system Python 3.9.25) said he was open to either approach, with a slight preference for a bundled virtual environment. Jeff Dost (OSG, also on 3.9.25) said he had no strong preference on Python version as long as GlideinWMS handles any virtual-environment setup itself with no extra manual steps required, since the factory container is scoped around whatever Python the factory needs. The presenter noted OSG is separately discussing upgrading some containers to EL10, and that moving the GlideinWMS reference platform to Python 3.12 already required some code changes during testing (not fully behavior-identical to 3.9), so a similar platform move could surface further issues. A separate email will be sent to continue this discussion.

### Front-end high availability (Jason C Patton / LIGO)
Jason C Patton relayed a question from LIGO (also raised by Brian Bockelman) about front-end HA: whether, with two front ends running, one does all the work and the other takes over automatically if it notices the first is down, and whether this works "out of the box." The presenter and Marco Mascheroni described the existing behavior: a named front end (e.g., "Fermilab front end") queries the factory collector for a ClassAd with a given name/cell; if it doesn't find that ClassAd (i.e., the primary front end has gone down), it starts advertising and effectively takes over — described as largely automatic and stateless, since front-end status/communication is tracked in Condor. Starting a second front end with the same name was noted to have caused problems in the past (the two front ends overwriting each other's ClassAds on the factory); Marco Mascheroni suggested this overwriting behavior might potentially be turned into a usable feature rather than treated purely as a bug, but said this needs to be double-checked. Jeff Dost noted CMS already uses an HA mode for the collectors and believed something similar exists for the front end (e.g., the Fermilab front end acting as backup for Tier 0). Jason C Patton said the exact implementation detail doesn't matter to LIGO as long as two front ends can run with at most degraded (not full) service loss if one goes down; he will follow up on LIGO's specific needs if the existing behavior doesn't already cover them.

### Round table
- Jeff Dost (OSG): nothing further to report beyond what was already discussed earlier in the meeting.
- Jason C Patton (LIGO): raised the front-end HA question (above); no other feature requests to report.
- Ken Herner: asked about progress integrating with the Superfacility API for HPC submission. The presenter confirmed a working prototype already exists, submitting clients via the Superfacility API for a specific proposal/CD, with production integration still to follow.
- Shreyas Bhat: nothing further to report.
- Marco Mascheroni (CMS):
  - Reported a conversation (at an event the transcript renders as "Rakuten," likely a mistranscribed event name — possibly a workshop or conference) with a DIRAC/DiracX developer about integrating HTCondor and GlideinWMS as the execution layer under DiracX (the CMS-facing rewrite of the DIRAC workload-management system). The DiracX team reportedly has a clear picture of where the HTCondor/GlideinWMS integration point needs to be, but there is schedule uncertainty: the team recently shifted focus to prioritize the "transformation system" (the part of DIRAC handling the sequence of workflow steps — generation, simulation, reconstruction, registration, stage-in/stage-out, etc.) specifically to accommodate CMS's needs, ahead of finishing the rewrite of the legacy DIRAC workload-management component that would interface with Condor/GlideinWMS. Since this transformation-system work is new, CMS was able to help clarify requirements early. Next step: the DiracX team will circulate a design document (referred to by an acronym Marco Mascheroni could not recall, described as an "ADR"-style document) with technical details, to be followed later by a more detailed technical specification (database structure, component interactions, etc.). It is understood that DiracX jobs will ultimately be submitted to Condor, and Condor matchmaking is expected to work the same way it does today; in the meantime, CMS continues to use the current legacy DIRAC-based workload management (i.e., what CMS does today with GlideinWMS is unaffected for now). Marco Mascheroni noted the separation of roles (comparable to today's separation between WMAgent/WMCore and GlideinWMS/Condor) looks straightforward in principle, but "the devil is in the details," to be clarified once the design document is available.
  - Reported that, following working-group assignments made at a recent Fermilab retreat, he was assigned the topic of data-aware matchmaking and has begun working on it, though he had nothing concrete to report yet. He suggested it may be useful to have a discussion with an expert, possibly at a future GlideinWMS meeting, where he could present his current thinking for discussion.

## Open Questions

- Why did the presence of an unused/removed X.509 proxy credential at Fermilab's 3.11 front end cause submission failures to some sites when combined with site-token credentials, and why could this not be reproduced?
- What exactly caused the OSG-factory Kubernetes network/auditor incident, and is the 3.10 ID-token-generation silent-warning behavior confirmed as the root cause?
- Does anyone (including Fermilab front ends specifically) still use the "pool index" credential syntax, and does it currently work correctly for token-based credentials?
- Should the reference/minimum Python version for the 3.11/3.12 series move to 3.12, and if so, via system Python or a bundled virtual environment?
- What are LIGO's specific unmet requirements for front-end high availability, if any, beyond the existing automatic-takeover behavior?
- Could the "two front ends with the same name overwrite each other's factory ClassAds" behavior be turned into an intentional, supported feature?
- What will the DiracX "ADR"-style design document specify regarding the HTCondor/GlideinWMS integration point, and on what timeline?

## Related

[[glideinWMS]] · [[HTCondor]] · [[Prometheus]] · [[Grafana]] · [[CVMFS]] · [[SciTokens]] · [[DIRAC]] · [[DIRACX]] · [[WMAgent]] · [[WMCore]] · [[Factory Configuration]] · [[Factory Operations]] · [[CMS]] · [[CERN]] · [[OSG]] · [[Pilot Jobs]] · [[HPC]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-08 17.09.33 GlideinWMS Meeting`)
