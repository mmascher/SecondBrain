---
type: meeting
date: 2026-09-09
participants:
  - Marco Mascheroni
  - Jason C Patton
  - Mats Rynge
  - Vito Di Benedetto
  - Namratha Urs
topics:
  - Release roadmap (3.10.19, 3.11.5, OSG 26 plan to drop 3.10)
  - Known bugs (front-end signing key, credential matching across trust domains, factory monitoring pilot count)
  - Custom-script default timeout reverted
  - Security fixes (logging tokens, OSG Security-reported code-execution issue)
  - glidein_config comments and batched constant updates
  - Encrypted/RSA credential support for Bosco
  - Pilot efficiency and overloading (CMS Grafana dashboard)
  - Python version roadmap (3.9 to 3.12)
  - Decision Engine release plan and OSG 26 compatibility
  - HPC/edge-services work (Superfacility API, IRI API, NERSC, ALCF, Oak Ridge)
  - Factory containerization (CMS)
  - cgroups enforcement for pilots
  - Redmine migration
---

# GlideinWMS Meeting

## Summary

This was the periodic GlideinWMS stakeholders meeting. As in other transcripts from this recording setup, the meeting's presenter/facilitator speaks only under the Zoom label "[WH8XE- Quarium]", which likely represents a room or shared endpoint rather than a single named individual; no personal name is attributed to this speaker below. The facilitator covered known bugs, a policy change (custom-script timeout default), the 3.10/3.11 release roadmap and the plan to include only 3.11 in OSG 26, a large set of 3.11.5 feature/fix highlights, Python version plans, and HPC/edge-services work (Superfacility API, IRI API) for NERSC, ALCF and Oak Ridge. Marco Mascheroni gave a developer spotlight on pilot-efficiency work and the overloading strategy, including a new CMS Grafana dashboard. The meeting closed with a round table: Jason C Patton (LIGO), Mats Rynge, Vito Di Benedetto (HEPCloud), and Marco Mascheroni (CMS/Factory Ops) gave updates, followed by an update from a participant referred to as "Steve" (surname unclear, heard as "Toon"), whose comments were nonetheless recorded under the room label rather than a personal name.

## Decisions / Conclusions

- The double-recall/double-reconfig bug affecting custom Glidein logging has been fixed, targeted for the 3.10.19 candidate release expected later the same day.
- In 3.10, if a front end's signing key is removed or corrupted while the front end is running, the front end keeps making (failing) requests instead of failing cleanly; this is suspected to be what happened during a prior Kubernetes cluster outage. This is considered a rare occurrence and will **not** be changed in 3.10, since 3.11 already handles this correctly.
- A new issue was identified: after the entry "out method" changed from grid proxy to site token, 3.11 factory monitoring fails to report pre-existing pilots carried over from a 3.10 factory in the count, even though the pilots are running correctly. This is considered a one-off affecting only that specific 3.10-factory/3.11 combination and will **not** be addressed.
- The default 10-minute timeout for custom scripts (introduced in 3.10.18/3.11.4) caused problems on sites where scripts run slowly. The timeout capability will remain configurable, but the **default will revert to no timeout**. The team will continue monitoring script execution length to keep identifying inefficient scripts.
- `glidein_config` now supports comments: a line starting with `#` followed by a space is treated as a comment; `#` not followed by a space is not treated as a comment (so it can still be used as part of a key).
- A security issue reported by OSG Security — a check in the Glidein configuration handling that could have allowed arbitrary code execution by someone with access to the factory configuration — has been fixed.
- 3.10.19 is expected later the day of the meeting; 3.11.5 is planned for later in September, with the group's next full meeting in November.
- For OSG 26, only the GlideinWMS 3.11 series will be included (3.10 will not be in OSG 26); 3.10 remains the last version with an SS7/SL7 build. Python 3.9–3.12 continue to be supported/tested on Alma 8/9; Alma 10 requires the 3.11 series. Once outstanding issues from wider 3.11 adoption are resolved, 3.11 will be renamed 3.12 for OSG 26.
- OSG 24 and OSG 25 will continue to carry both the 3.10 (current stable) and 3.11 (upcoming) series.
- All known factories (including CERN's) have migrated to GlideinWMS 3.11; a 3.11 front end requires a 3.11 factory, while 3.11 factories remain compatible with 3.10 front ends.
- When migrating a front end from 3.10 to 3.11, the `proxy` plugin setting (e.g. `proxy_all`) must be manually replaced with the credential-based equivalent; a warning is shown during config/upgrade, but the change itself must be done manually. The rest of the configuration is expected to carry over automatically.
- The Decision Engine plan is to get Decision Engine 2.1 into OSG by the end of the month, targeting OSG 24/25, ahead of eventually reaching OSG 26; the currently deployed Decision Engine version in OSG 24/25 is 2.0.6, which took about two years to land. Part of the motivation for the GlideinWMS credential-handling refactor was to allow the same credential-handling code to be reused by the Decision Engine.
- The GlideinWMS team has an ongoing summer project (started over the summer) to add support for the Superfacility API, an "IRI" API, and possibly Globus Compute, targeted for around the end of October; this will run within the factory and, while mainly driven by AmSC-related use cases, will be available to all factory users.
- Since HTCondor has not committed to a timeline for native Superfacility API (SF API) support (potentially "end of year or later"), GlideinWMS is implementing SF API support directly in the factory without requiring HTCondor changes, similar in approach to what HTCondor itself would have done. This work (referred to as Douglas's work) currently exists as a PR.
- The planned first use case for the IRI/SF API work is NERSC, which currently is accessed via Bosco (SSH-based submission, requiring exemptions); after that, the same approach is planned for Argonne (ALCF) and then Oak Ridge (OLCF), assuming the API is consistent across facilities. A durable solution for "edge services" at sites like ALCF (which lacks network connectivity for worker nodes) remains an open problem blocking a sustainable production workflow there.
- Plan features after the current release cycle: continued work on the HPC APIs (Superfacility/IRI) and enabling Condor SSH jobs that can run containers.

## Action Items

- [ ] Complete full on-demand CVMFS provisioning for the 3.11.5 release — Namratha Urs
- [ ] Complete the Puppet setup for Decision Engine so the front-end/Decision Engine path separation is consistent — Vito Di Benedetto
- [ ] Work on containerizing the CMS factory (following the OSG factory's existing Kubernetes deployment) — Marco Mascheroni / CMS Factory Ops

## Discussion

### Team, external contributions, and Redmine
The current team was introduced as the presenter, Marco Mascheroni, Namrata (Namratha Urs), and Shreyas. The presenter thanked outside contributors, including a contributor heard as "Mans" (elsewhere transcribed as "Mads" — the transcript is unclear which is correct) for a PR improving `glidein_config` and for a security report that helped further harden the Glidein. Regarding legacy issue tracking, GlideinWMS still has material in Redmine at Fermilab, whose Redmine support is described as dwindling; most of that material is considered obsolete but is kept for project history, and the plan is to move it into a separate GitHub project within the team's GitHub space.

### Known bugs and monitoring
- Custom Glidein logging double-recall bug: fixed, targeted for 3.10.19.
- 3.10 front-end signing-key removal/corruption while running: front end keeps making (failing) requests rather than stopping cleanly; suspected cause of a prior incident during a Kubernetes cluster outage. Considered rare; will not be changed in 3.10 since 3.11 handles it correctly.
- Front-end credential matching across multiple trust domains: an active bug being troubleshot, affecting selection of the correct credential when multiple sites/domains and credentials are involved.
- 3.11 factory monitoring undercounting pre-existing 3.10 pilots after the entry "out method" changed from grid proxy to site token: pilots keep running correctly, but monitoring loses track of the count. Considered a one-off tied to this specific configuration; thanks were given to Namratha Urs for investigating. Will not be addressed further.
- ID-token related issue raised by Mats Rynge (see Round table) is believed to already be addressed by merged fixes, pending confirmation via further testing.

### Custom-script timeout policy change
3.10.18 and 3.11.4 introduced a default 10-minute timeout for all custom scripts (both those shipped by default with the front end/factory and user-added scripts). This caused problems on sites where such scripts run slowly. The timeout setting will remain available/configurable, but the **default will revert to no timeout**. The team is monitoring script execution length and using that data to help improve some scripts that were found to be inefficient.

### Release roadmap and 3.11.5 highlights
3.10.19 is expected later the same day as the meeting; 3.11.5 is planned for later in the month (toward the end of October/beginning of November). Reported/planned 3.11.5 content included:
- More robust `check_proxy`, improved default selection (and fallback) of Condor tarballs, improved credential mapping defaults.
- `glidein_config` "multi"/batched constant updates: constants shared across custom scripts used to be added to the shared config file one at a time (each involving a lock/copy of the file), which was slow and risked partial writes; a PR from the external contributor mentioned above, further optimized by the team, batches these writes and significantly speeds this up.
- Fixes to the arch requirement for pilot support, and to variables visible in the Glidein environment (e.g. bind paths, IDtoken files).
- `glidein_config` now supports comments (see Decisions).
- GitHub Actions updated to keep CI functioning.
- Fix for the logging-token issue noted as a known issue for 3.10.18.
- A security fix (reported by OSG Security) for a check in the Glidein configuration that could otherwise have permitted arbitrary code execution by someone with factory-configuration access.
- Consideration of adding Prometheus monitoring in 3.10.19 was dropped for that release; it may appear in a possible 3.10.20 or go directly into the 3.11 series instead.
- Documentation for 3.11 lives in a separate "dev docs" location, distinct from the regular docs/PRD documentation path.
- Framework support for encrypted credentials, implemented for RSA keys (heard as "Lsa key"): previously, signed/encrypted key pairs required a separate tool to strip the signature before use; now outside/signed keys can be used directly. This is particularly useful for Bosco users, since the Condor tooling used to set up Bosco (remote-cluster submission via Condor) creates an encrypted/signed key by default.
- `get_request_credentials` snapshot support, enabling targeted, dynamic request credentials.
- Improved generator context validation: generators such as the ID-token and site-token generators were meant to raise configuration-time errors but sometimes only failed at runtime (one also had a bug in its check); these have been fixed.
- Compatibility fix for a Python `cryptography` library type/naming change, to remain compatible with the older version that ships by default in Alma Linux RPMs.
- Fix to `populate_group_security` not parsing/stripping correctly at the end of a string.
- Fix to the ID-token generator, which had a bug both in configuration and in the per-site auto-matching fallback (a misspelled fallback variable introduced in an earlier PR) used to automatically generate a per-site ID token.
- The overloading-enable fix mentioned by Marco Mascheroni (see Developer spotlight/Round table).
- The factory's ScheddStatus XML has been improved and now works correctly with 3.11.
- An unclear feature referred to in the transcript as "eventually support" is not working correctly in 3.11; the team will probably drop support for it since no one appears to be using it.
- Remaining open items before 3.11.5: full on-demand CVMFS provisioning (Namratha Urs completing this) and a refactor of plugin startup.

### 3.11 migration notes
3.11 factories are compatible with 3.10 front ends, but a 3.11 front end requires a 3.11 factory. All known factories, including CERN's, have migrated to 3.11. When migrating a front end from 3.10 to 3.11, the `proxy` plugin configuration (e.g. `proxy_all`) must be manually replaced with the credential-based equivalent; a warning appears during config/upgrade, but this step is manual. Feedback on the 3.11 front end is especially welcome as wider adoption surfaces new, previously untested use cases; thanks were given to CMS for testing and contributing fixes.

### Developer spotlight: pilot efficiency and overloading (Marco Mascheroni)
Marco Mascheroni presented a summary covering several past quarters of work in three areas:
- **Pilot efficiency and overloading**: monitoring and enabling overloading-percentage reporting, plus bug fixes found in the development version.
- **Factory resource configuration**: made OSG AutoConf more robust to missing/inconsistent resources; fixed the GPU count reported for whole-node GPU entries; added handling for ARM resources; improved the default Condor-tarball selection and its fallback.
- **Operational improvements**: installing 3.11 on the CMS ITB dev environment surfaced new corner cases in the development version, leading to improved diagnostics and additional fixes.

On pilot efficiency specifically: previously CMS only had a per-job "payload efficiency" metric, computed via Condor from job CPU-time data, with no independent metric for overall pilot efficiency (which also reflects GlideinWMS/scheduling overhead and whether overloading is active). Missing information in the HTCondor log — including per-pilot overloading on/off status — previously made this impossible to measure continuously; it was only checked via spot checks. Efficiency is computed as: CPU time (in seconds) used by a process, divided by (wall time × available CPUs). Adding this information to the HTCondor log enabled continuous monitoring and produced a new **CMS pilot efficiency Grafana dashboard** (external to the GlideinWMS codebase). The dashboard compares overloaded vs. non-overloaded pilot efficiency for Tier-1 sites overall and for Fermilab specifically; Fermilab was highlighted because it runs whole-node allocations with enforced cgroups boundaries, so there is confidence that pilots are not "borrowing" extra cores. The data shows overall pilot efficiency improved by roughly 10% with the overloading strategy, both at Fermilab and across Tier-1s overall — providing an independent, continuous way to demonstrate the benefit of overloading (more efficient resource use and more produced events). Overloading was described again briefly (pushing extra jobs/cores into the same pilot slot); an "IO slots" feature was also mentioned as previously introduced, though the presented plots focused on overloading.

### Python version roadmap
GlideinWMS 3.10 will not be part of OSG 26; only 3.11 will (as noted in Decisions). 3.10 remains the last version with an SS7 build (no known users currently); 3.9–3.12 are supported/tested on Alma 8/9, and Alma 10 requires the 3.11 series. The facilitator raised whether to move the 3.11 series to reference Python 3.12 rather than 3.9, noting Python 3.9 support from libraries is winding down even though RHEL still supports it, and that 3.12 is already upstream/default on EL10. This applies only to the Python version used to run the factory and front end themselves — operators can otherwise choose their own Python. Separately, embedded Python interpreters invoked by `glidein_startup.sh` and VO custom scripts running inside the pilot need to remain compatible much further back (as far back as Python 2.7), since GlideinWMS cannot control what is available on the worker node; GlideinWMS looks for Python 3 first and falls back to Python 2 if needed. No explicit final decision on moving the 3.11 reference Python to 3.12 was recorded in the transcript; it was raised as an open question for feedback.

### OSG 26 release policy and Decision Engine backward compatibility
A stakeholder confirmed with the facilitator that GlideinWMS 3.10 will not be in OSG 26 going forward (only 3.11). This was flagged as creating a backward-compatibility concern for the Decision Engine, which currently still depends on some 3.10-era behavior. The plan discussed is to get Decision Engine 2.1 into OSG by the end of the month, targeting OSG 24/25, with the goal of eventually having 2.1 available for OSG 26 as well; the current OSG 24/25 Decision Engine version (2.0.6) took about two years to reach release. Part of the motivation for the GlideinWMS credential-handling refactor was explicitly to allow the same credential-handling code to be shared with the Decision Engine, avoiding duplicated work.

### HPC/edge-services work (Superfacility API, IRI, NERSC, ALCF, Oak Ridge)
US CMS (via a conversation the facilitator had with "Nick from CMS") is involved in projects pledging to use more HPC resources, including submission to NERSC and other DOE Leadership Computing Facility (LCF) sites, in the context of what the transcript refers to as "American Science Cloud" (the exact name/acronym is unclear in the transcript). GlideinWMS has plans and a timeline to support submission to these sites. A key open problem is that some sites, such as ALCF, lack network connectivity for their worker nodes, complicating access to CVMFS, Condor, and other services; ALCF does not currently have a persistent "edge"/gateway service to rely on (a temporary one was set up for a demo roughly six years ago).

Since HTCondor gave no committed timeline for native Superfacility API support, GlideinWMS is implementing SF API support in the factory directly (a PR already exists), in an approach similar to what HTCondor itself would have done. The plan is to first use this for NERSC, which has network connectivity and is currently accessed via Bosco (SSH-based submission requiring exemptions), then extend the same approach to Argonne (ALCF) and then Oak Ridge (OLCF), assuming the same API works across facilities. A durable edge-services solution at ALCF/OLCF remains necessary for a sustainable production workflow (as opposed to filesystem-transfer-based prototypes already tried in past "pledge run" style efforts). It was suggested that having a concrete AmSC-related user (e.g., a mention that DUNE is expected to start using this around 2027, in connection with CMS being described as an AmSC infrastructure partner) could help build momentum for edge services at Argonne. There is reportedly an advocate for this work within an "AmSC architecture team" (name heard as "Eustace Spokas", spelling uncertain), who is pushing for HTCondor to be included in that architecture.

### Round table
- **Jason C Patton (LIGO)**: nothing to report this month; LIGO's front end remains on GlideinWMS 3.10.
- **Mats Rynge**: raised an ID-token issue under discussion over the preceding days; a workaround exists, but he felt it needs to be looked at seriously since it could affect other VOs. The facilitator responded that they have been testing this and it appears to work correctly with fixes already merged. Mats also said his group is waiting for the upcoming release, in particular for the `glidein_config` multi/batched-constant-update feature discussed earlier.
- **Vito Di Benedetto (HEPCloud)**: the Decision Engine factory is still on GlideinWMS 3.11.4, with some patches possibly to be addressed in 3.11.5. He is testing Decision Engine 2.0.6, focused on separating directory/path locations between the front end (referred to as "GWMSLib") and the corresponding Decision Engine paths (the transcript is unclear on the exact details here); no blockers so far, but the Puppet setup to make this consistent still needs to be completed.
- **Marco Mascheroni (CMS/Factory Ops)**:
  - CMS is planning to work on containerizing the CMS factory, similar to the OSG factory's existing Kubernetes deployment; he does not expect this to affect GlideinWMS development unless the deployment architecture changes (e.g. running Condor in a separate container), which is still being explored.
  - In response, the facilitator suggested — as was previously done for front-end containerization — splitting out the web server into its own container, since the RPM packages are already separate and this allows Glideins to keep downloading files from the web server even while the factory itself is down (e.g. during updates); currently, the OSG deployment installs everything in a single container.
  - CMS is also working on deploying the new (3.11-series) front end; the factory side is already on 3.11, but the front-end is still on 3.10 in production. Testing this week surfaced a bug where overloading was not applied under the new front-end/factory communication protocol — the overloading logic exists on the factory, but has not been implemented for the new protocol.
  - A likely future focus is enforcing cgroups for pilots, to ensure jobs running inside a pilot do not exceed the resource (e.g. memory) boundaries assigned to that pilot — particularly relevant with overloading. The facilitator agreed this should be tested, noting enforcement would go through Condor configuration.
- A participant referred to (and addressed) as "Steve" (surname unclear, heard as "Toon") then gave an update, though the transcript continues to label this speech under the room label rather than a personal name: the OSG global pool is described as stable and not being stretched, with interest in the ongoing HPC/IRI work; it was noted that such HPC demos require dedicated FTE effort to make progress (CMS funded earlier demos), and that renewed outreach to the Argonne (ALCF) team is overdue (it has been over a year since the last conversation), with the observation that "a lot has moved" there recently (software now exists where previously there was only paperwork). It was suggested that if both CMS and DUNE push Argonne for edge services, that could generate real movement.

## Open Questions

- Should the 3.11/3.12 series move its reference/minimum Python version from 3.9 to 3.12?
- Will HTCondor commit to a timeline for native Superfacility API support, or will GlideinWMS's own SF API implementation in the factory remain the long-term approach?
- What durable "edge services" solution can be established at ALCF (and later Oak Ridge) to support a sustainable production workflow, given the lack of worker-node network connectivity?
- Will pushing from CMS and DUNE toward Argonne (ALCF) produce movement on edge services?
- Will Decision Engine 2.1 land in OSG on the timeline discussed (end of the month, then OSG 24/25, eventually OSG 26)?

## Related

[[glideinWMS]] · [[HTCondor]] · [[CMS]] · [[OSG]] · [[CERN]] · [[Factory]] · [[Factory Operations]] · [[Factory Configuration]] · [[Pilot Jobs]] · [[HPC]] · [[Kubernetes]] · [[DIRAC]]

## Source

GlideinWMS Meeting transcript_2026-09-09_17.54.47.txt (from `2026-09-09 17.09.26 GlideinWMS Meeting`)
