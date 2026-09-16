---
type: meeting
date: 2026-03-26
participants:
  - Marco Mascheroni
  - Luís Simas
topics:
  - glideinWMS entry troubleshooting
  - pilot logs
  - site tokens vs grid proxy authentication
  - WLCG token migration
---

# GlideinWMS Entry Troubleshooting and Site Token Migration (Mentoring Session)

## Summary

This was a one-on-one mentoring/working session between Marco Mascheroni and Luís Simas, focused on Luís's work testing a new glideinWMS entry for the Rome (Italy) Tier-2/CE site. Marco walked Luís through debugging a "pilots running but jobs idle" symptom using `condor_status`, `condor_q`/`entry_q`, and factory pilot logs, then explained the glideinWMS process architecture (condor_master, condor_startd, condor_starter, grid managers) and the difference between grid-proxy (X509/GSI) and site-token (JWT) authentication to compute elements. The session ended with a discussion about pushing site-token adoption for the Rome CE and coordinating with WLCG on the broader token migration.

## Decisions / Conclusions

- The group agreed to push for site-token adoption on the Rome CE rather than defaulting back to grid proxy, on Marco's recommendation that "it's time to migrate everything to site token."
- Rather than editing the existing entry's auth method in place, a new entry (e.g. suffixed `_site_token`) should be created so the grid-proxy and site-token entries can be tested side by side.
- Luís will tell the Rome site admin that two types of pilots (grid proxy and site token) may be arriving, since the admin is concurrently reconfiguring the CE and unrelated simultaneous changes have previously made it hard to isolate the cause of issues (as happened with the Finnish/LUMI-C site).
- The proxy credential is still sent alongside the site token for Condor CEs even when authentication is actually performed via the site token; this was a deliberate fallback kept from when the token transition began, and the proxy may still serve an accounting purpose.

## Action Items

- [ ] Create a new entry for the Rome CE to test site-token authentication side by side with the existing grid-proxy entry, and replicate the "pilots running, jobs idle" issue — Luís Simas
- [ ] Inform the Rome site admin that two pilot types (grid proxy and site token) are being tested — Luís Simas
- [ ] Write a documentation guide on how to add a new glideinWMS entry and how to troubleshoot common issues (e.g. pilots running but no jobs), based on this session's transcript and comments — Luís Simas
- [ ] Send Luís the details of the 2pm meeting with Florian (and possibly Antonio) on GPU partitioning — Marco Mascheroni

## Discussion

### Debugging the Rome entry: pilots running, jobs idle

Luís reported pilots showing as running in Grafana monitoring for the Rome ITB entry (scheduler VOCMS0811) since the previous day, but with no jobs actually running — a symptom he found confusing. Marco walked through diagnosing this directly against HTCondor rather than relying on monitoring:

- `condor_status` on the factory/collector lists connected pilots (execution points); it can be filtered with `-constraint 'GlideinEntryName == "<name>"'`.
- `condor_status -long -limit 1` shows all classad attributes for a pilot/slot.
- `entry_q` is described as a wrapper around `condor_q`/`condor_status` scoped to a given entry.
- `condor_q -g -all` queries all schedulers globally (there are multiple schedulers for scalability) and all users' jobs, showing the pilot's cluster ID in the first column.
- Once a pilot's cluster ID is known, its factory-side pilot logs can be inspected after the pilot exits (not while still running).

Marco noted a common false alarm: a pilot can start when jobs are queued, but by the time it starts running those jobs may already be gone, so the pilot appears idle after connecting. In this session, resubmitting a fresh batch of test pilots reproduced running pilots and running jobs, resolving the immediate confusion. Marco commented that submitting on the order of 100 test jobs for testing/retesting is fine, but not thousands.

Earlier in the debugging, Luís's initial pilots for the Rome entry were idle in the factory while using site tokens; logs pointed to "compute resource being down," similar to an earlier issue seen at the Finnish site (Lumi-C) with site tokens. Switching to grid proxy (matching what all of Rome's production entries currently use) got them further, and after the site admin made configuration changes (seen referenced in an INDIGO ticket), the pilots started reaching the CE and going idle there instead, then eventually ran successfully.

### Reading factory pilot logs

Marco showed the structure of factory-side logs, organized per front end and per entry, containing one subdirectory/file set per pilot cluster ID:
- `glidein_startup` logs record the sequence of validation steps ("activations"), e.g. Frontier/Squid validation (`test_squid.sh`), CVMFS-type checks, etc. A failed validation (e.g. failing `test_squid.sh`) causes the pilot to exit before starting Condor.
- When a validation fails, the pilot gives up and waits (Marco recalled roughly 20 minutes) before another pilot is tried, rather than retrying immediately — a deliberate throttle intended to prevent "black holes" (a site pulling down pilots repeatedly with no useful outcome).
- After successful validation, the log shows Condor starting up in the background; `condor_status` can then be used to confirm the pilot registered with the pool.
- The standard error log contains base64-encoded snippets of the `condor_master`, `condor_startd`, and `condor_starter` logs, extractable with commands like `cat master.log | base64 -d` (approximate usage shown live); `grep -v "configuration problem"` was suggested to filter out a long-standing, unresolved harmless warning.
- An XML summary is appended by `glidein_startup` at the end of pilot execution for convenience; Marco believes it used to be consumed by some downstream tool (possibly under "support"), but is unsure whether anything still consumes it today.

### GlideinWMS/HTCondor process architecture

Marco explained the on-worker-node process hierarchy: `condor_master` and `condor_startd` are always present once a pilot starts, while a `condor_starter` process is spawned only when a job is actually matched and started — one starter per running job. This means a startd can be healthy and registered while a starter-level failure still prevents user jobs from running, which can look like "pilots fine, zero jobs" in monitoring (0% pilots failing to start, 0% validation failures, 100% pilot run, 0 user jobs).

Each pilot registers two slots with the collector: a regular job slot and a dedicated high-I/O slot reserved for merge jobs (which are disk-heavy, low-CPU jobs that combine outputs from multiple jobs). Only one high-I/O slot is created per pilot to avoid wasting CPU allocation or creating disk contention from running multiple merge jobs concurrently on the same node.

On the factory/scheduler side, `ps` shows one Condor Master, `condor_schedd`, and per-scheduler grid-manager processes — separate grid-manager processes for CondorCE and for ARC CEs — running under HTCondor's grid universe (as opposed to the vanilla universe used for regular jobs). The grid managers watch the queue, connect to the relevant compute element, authenticate (via proxy and/or site token), and submit the pilot job to the CE.

### Recurring starter-level failure on the ITB frontend

Marco described a previously-diagnosed incident (discussed internally a couple of weeks earlier) in which the ITB frontend appeared to work correctly for weeks — pilots connected, validations passed — but jobs were actually failing at the starter step due to a misconfiguration in the backup ITB front end for Fermilab (managed by an external contact, "Yahoo" in the transcript — possibly a mis-transcribed name). Marco had rolled the ITB frontend back from version 3.10.3 (believed broken) to the older 3.10.17, expecting it to work, but did not realize the backup front end was also affected, so the failure went undetected for some time. The root cause was described as a value defined without its variable being set, in the backup front end configuration. Marco noted he still doesn't fully know why this recurring issue exists.

### Grid proxy vs. site token authentication

Using a live example from a submitted pilot job's classads, Marco explained:
- Grid proxy is an X509 certificate (with GSI/VOMS-style extensions encoding CMS role/capabilities, e.g. role "pilot") created by the frontend and passed to the factory (encrypted, via the collector). It is what the factory presents to the compute element for authentication under the `grid_proxy` auth method.
- Site tokens are JWT tokens (viewable via jwt.io) stored in a `SciToken`-style classad (referred to as "site token" in this environment) on the pilot job; used for authentication under the `auth_method = scitoken` (site token) setting. It is the factory itself — not the pilot initialization script — that uses the token/proxy to authenticate to the CE.
- Both a proxy and a site token are currently attached to Condor CE jobs. This dates back to the original transition to Condor CEs, when the team wanted to attempt site-token auth with a proxy fallback if the token failed. The proxy is believed to still be needed/used for accounting purposes even though authentication itself now goes through the site token.
- Luís clarified there is no separate standalone "proxy service" — the term refers only to the X509 proxy file itself, generated and passed along by the frontend.

### WLCG-coordinated token migration

Marco explained that CMS is one of several experiments sending pilot jobs to WLCG (Worldwide LHC Computing Grid) sites, and that WLCG is the ultimate body deciding what authentication methods sites must support — a site can decline to drop grid-proxy support, and WLCG's coordination determines whether that is acceptable. Marco referenced a WLCG migration timeline with milestones (M1–M9, referencing GSI, ARC, and WMAgent/CRAB jobs), including one milestone (around March, referred to as M5) marking "end of HTCondor support for GSI," after which he said only site tokens could be used, "with a caveat" he did not elaborate on in this session. Marco was uncertain whether the currently-cited timeline was still current, and was not sure whether pushing site-token migration is a hard WLCG deadline or a proactive CMS choice; he suggested checking with Stefan (referred to as "Stefan Amerio" and separately transcribed as "Nccu," likely a mistranscription) or a WLCG contact named Martin to clarify.

### Monitoring gaps

Luís noted that an earlier validation failure for the Rome entry did not show up in the Grafana pilot-efficiency monitoring; Marco suggested this was likely because the `analyze_entry` tool itself was broken at the time. Marco reiterated a general preference for going directly to logs when debugging, treating monitoring as useful mainly for alerting, and said monitoring gaps like this "we'll fix." Luís separately asked whether an exporter exists for this data; this was not resolved in the meeting.

### Documentation and other notes

Luís plans to turn this session (transcript plus Marco's live comments) into documentation covering how to add a new entry and how to troubleshoot common symptoms (e.g., pilots running but no jobs). Marco encouraged this, noting the value of documentation for future AI-assisted support tooling ("Archie"). Separately, Luís mentioned he keeps informal personal notes ("private post-mortems") on issues he investigates (e.g. Frontier-related breakages); the group does not currently have a formal post-mortem process, and Marco agreed this might be worth doing more formally.

Briefly mentioned in passing: a 2pm meeting with Florian (and possibly Antonio) on GPU partitioning that Luís expressed interest in joining; the CMS week around April 13th (Marco does not plan to attend most of it, being a non-physicist, but may attend a computing-focused session); and a visit from "Dave," tentatively placed around the week of April 21st (dates were uncertain in the discussion).

## Open Questions

- Why does the Condor site-token authentication fail for the Rome CE (and previously for the Finnish/LUMI-C site) on first attempt? To be investigated by replicating with a dedicated `_site_token` test entry.
- Is the push toward site-token migration driven by a firm WLCG deadline/policy, or is it a proactive choice by CMS ahead of any deadline? To be clarified with Stefan or a WLCG contact ("Martin").
- Is the XML summary file produced by `glidein_startup` still consumed by any downstream tool?
- Why does the long-standing "configuration problem" warning in pilot logs exist, and should it finally be fixed?
- Is there an exporter for pilot/validation monitoring data that could address the observed Grafana gap?

## Related

[[glideinWMS]] · [[HTCondor]] · [[WLCG]] · [[CMS]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Frontier]] · [[CRAB]] · [[WMAgent]] · [[Monitoring]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-26 10.05.57 Submission Infrastructure Weekly Meeting`)
