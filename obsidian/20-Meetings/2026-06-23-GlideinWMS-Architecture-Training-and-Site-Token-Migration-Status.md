---
type: meeting
date: 2026-06-23
participants:
  - Marco Mascheroni
  - Luis Simas
topics:
  - Site token migration status (CERN Tier 0, MIT, Syracuse/OSG Tier 3)
  - glideinWMS architecture training (continuation)
  - Factory/Frontend/entry group internals
  - ID token / site token credential flow
  - Match expression and start expression configuration
  - Factory unexpected restart (unresolved)
  - Puppet/RPM deployment of factory HTCondor config
---

# GlideinWMS Architecture Training and Site Token Migration Status

## Summary

This session opened with a short operational status update between Marco Mascheroni and Luis Simas on the ongoing Condor CE site-token migration, before continuing a longer-running glideinWMS architecture training/tutorial (a continuation of an earlier walkthrough, picking back up at the point they had previously stopped, mid-discussion of Squid plugins). The bulk of the meeting was Marco walking Luis through the glideinWMS architecture slide deck — factory, frontend, entry groups, the factory collector, class ads, credential/token flow, and the two-stage matchmaking (match expression and start expression) — with Luis asking clarifying questions and cross-checking some details against the actual deployment (Puppet, RPM packaging, GitLab-hosted frontend configs). The meeting ended with Luis outlining his plan to validate the site-token migration across all glideinWMS entries before a separate Factory Ops meeting scheduled shortly afterward.

## Decisions / Conclusions

- Wait at least one more day before publishing the CERN Tier 0 site-token changes further (to the component Marco referred to as "Tiger" — likely OSG Topology, but the transcript is unclear on the exact name).
- Do not touch/change the Fermilab factory until the MIT site issue is resolved; also avoid changing submission rates there for now.
- Submit-rate changes will be discussed separately in the meeting with Jeff Dost, since it may also be relevant to Luis.
- The established, conservative process for rolling out site-token (and similar) changes across the three glideinWMS factories is: make the change first in the CERN factory only (kept local), validate it, commit it so OSG picks it up, re-check, and only then apply it to the Fermilab factory — Fermilab is always updated last. This process was reaffirmed as "usually the process we do."
- The frontend configuration should not be updated for a while, to avoid confounding the ongoing site-token validation work (a drop in CPU cores could otherwise be hard to attribute).
- The CERN entries for the site-token migration are already fully done; this is local to the CERN factory only and does not affect the Fermilab ("Tiger") factory.
- The group agreed to continue the glideinWMS training in a future session, likely Thursday or Friday, resuming at the "glidein internals" section (last covered roughly three weeks prior).

## Action Items

- [ ] Check why the (CERN?) factory process was found running since ~2pm without having been intentionally restarted — Luis Simas
- [ ] Send an email to the Syracuse (OSG Tier 3) site admin regarding the site-token migration, since that site has not yet responded — Marco Mascheroni
- [ ] Go over all glideinWMS entries to identify which ones stopped working around June 9, using a more thorough test than the earlier ITB test (which was not very useful since even known-working entries never completed) — Luis Simas
- [ ] Do this entry-by-entry site-token review/validation before the Factory Ops meeting taking place shortly after this one — Luis Simas

## Discussion

### Site token migration status
Luis reported that pilots are starting to run following the site-token changes for the CERN Tier 0. He wants to wait at least one more day before publishing the changes further. Marco raised that the Fermilab factory should not be touched until the MIT site issue is understood; Luis confirmed the MIT site admins now understand the issue conceptually but said it will take some time to fix (referencing a message from "Max").

Luis explained his validation approach so far: he first tested using `condor_ping` with the production token in ITB, then tried a real test job, but found the ITB tests were not reliable — even entries known to be working never completed, making it hard to trust the results. Given that the MIT site did not behave as expected despite earlier testing, Luis decided he needs to systematically go over all entries to see which ones stopped working since June 9, rather than relying on the ITB test alone. He noted that problems on some entries could otherwise go unnoticed if another resource silently compensates for the lost capacity, only becoming visible (as a drop in CPU cores) if that other resource is also changed later.

All CERN entries have already had the site-token change applied; this is local to the CERN factory and does not affect the Fermilab ("Tiger") factory. Luis reaffirmed the team's usual conservative rollout process across the three factories: change and validate in the CERN factory first (kept local), commit so OSG's topology/config picks it up, re-check, and only then apply the change to the Fermilab factory, which is always updated last. He plans to do this review before the Factory Ops meeting occurring shortly after this session.

Separately, Syracuse (an OSG Tier 3 site) has not yet responded regarding the site-token migration; Marco said he had already spoken with the site admin informally and needs to follow up with an email.

### glideinWMS architecture training (continuation)
Marco and Luis resumed a glideinWMS architecture training session, picking up roughly where a previous session had left off (a tangent about Squid plugins). Marco walked through the architecture slides, covering:

- **Glidein concept**: a properly configured execute node submitted as a grid job; glideinWMS automates pilot submission. The system is composed of three logical pieces: the glidein itself (which sets up and starts HTCondor on the worker node), the factory, and the frontend.
- **Validation plugins**: standard plugins perform basic grid-node validation (token/certificate checks, disk space, etc.); optional VO plugins can check anything else — e.g., the CMS frontend checks CMSSW and Squid availability. Factory administrators can also supply plugins (e.g., an OS-verification plugin Marco mentioned is now part of the default set).
- **Factory**: holds per-site submission details in an XML configuration file; only trusted/tested sites are included, entered by adding a config-site entry with support contact info and attributes. These are manually maintained and (per Marco) never actually cross-checked against external databases like GOCDB or OSG topology, though Marco suggested this might be worth doing at some point. Luis noted CRIC is more like a frontend than an actual data source, aggregating from GOCDB/topology; both agreed the factory is purely a "waiter" — it does not decide how many/which glideins to submit, only the frontend does, based on demand.
- **Frontend/factory communication**: happens via ClassAds through the factory collector. When the factory starts, it reads the XML and publishes one "glidein resource" ClassAd per site; the frontend publishes a "glide client" ClassAd with its request, most importantly `request_idle`, i.e. how many idle glideins it wants in the factory queue at a given site.
- **Factory internals**: the factory is a Python process that spawns multiple sub-processes ("entry groups") for load balancing; each entry group handles a subset of entries and runs the factory cycle (submit, check the collector, verify errors, etc.) for each. Luis asked whether the number of parallel workers/sub-processes is configurable; Marco located a configuration option (apparently controlling something like the number of parallel workers) but was not certain of the exact details of how work is split between them. Luis suggested this parallelism exists mainly because Python needs multiple processes to manage work in parallel effectively.
- **Submission mechanism**: the factory submits via Condor-G to the CE. The factory does not support process-based tracking per se; it operates per-entry, submitting and then monitoring each entry's glidein progress.
- **Authentication**: previously proxy-based (deprecated), now uses ID tokens for frontend-to-factory authentication, plus an additional security-class-ad check on the factory side so it only accepts requests matching what it expects. For factory-to-CE authentication, a site token is used instead. The frontend owns the glidein/site-token proxy and must keep it valid at all times via a cron job (a mechanism the team wants to replace, hopefully once migrated to HTCondor 3.11.4). The cron job authenticates to "CMS auth" using stored credentials, obtains and decodes a token, and installs it for use. Each VO used to be mapped to a different Unix account on the factory, but this is no longer the case — all VOs now use the same Unix account.
- **Token audience (proposed change, not yet done)**: Marco noted the team would like to change the site-token audience from a wildcard to a per-CE hostname, so that if one site's CE is compromised, only that site is affected rather than all sites sharing the token.
- **Token expiry**: site tokens are configured to expire after three days, specifically to cover weekends, since the CMS hub does not have 24/7 coverage — this gives admins until Monday to fix an issue that arises on a Friday.
- **Match expression / start expression (two-stage matchmaking, revisited)**: the frontend can (and should) provide a VO-specific validation script and a "start expression." The match expression (used for the first, frontend-to-entry matchmaking) is defined by the frontend admin, not the user, and is implemented as a Python function (wrapped in a module, since it grew too complex to remain a single boolean expression) comparing job attributes (from the job ClassAd) against entry attributes — e.g., requested memory vs. per-slot memory, OS/architecture, expected runtime, desired sites. This is deployed via a config file hosted in the `frontend-configs` GitLab repository, with Puppet believed to manage a symlink to it (Luis recalled recent related changes). The start expression (used for the second, negotiator-level matchmaking) is conceptually similar but is a Condor ClassAd expression rather than Python, configured per frontend group (no single shared file); it is passed from the frontend to the factory to the CE/worker node as a parameter, and the glidein startup script appends it to the StartD's start expression. Validation scripts referenced at this point include a microarchitecture check, a Squid check (exporting info from site configuration), a Dirac benchmark run (requested by "the team"), and CVMFS-related checks.
- **Local deployment inspection**: While cross-checking where various Condor configuration snippets on the factory host come from, Luis found several locally-managed config files/RPMs on the CERN factory (e.g. `GWMSlocal.config`, a "batch gap" file, "99 local tweaks", and other local-config files), some possibly deployed via Puppet and some via RPM (checked using `rpm -qf`/`rpm -ql`). Neither participant was fully sure which of these are actively used, deployed via Puppet vs. packaged directly, or where all of them originate (Marco suspected some come from CMS-provided configuration). Marco suggested doing a dedicated review/cleanup exercise at some point to understand and straighten these out, but this was not scheduled as a concrete task.
- **Unexpected factory process state**: while looking at process details on screen, Luis noticed the (CERN) factory appeared to have been running since around 2pm despite not having been intentionally restarted that afternoon (it had reportedly been started that morning). Marco confirmed he had not restarted it either. Luis said he would look into why it restarted.
- **VO frontend role**: the frontend monitors the user Condor pool, does matchmaking, and requests glideins; it is described as the "brain" of a glideinWMS-based pool, acting as a site-level negotiator. There are two matchmaking cycles: the frontend-level cycle (deciding whether to request more glideins) and the Condor central-manager negotiator cycle (matching queued jobs to already-running glideins/pilots on worker nodes).
- **Relationship to higher-level matchmaking**: Luis asked whether jobs entering the vanilla Condor schedd already have a specific desired site attached. Marco clarified there is no single desired site at that point in general; higher-level systems (WMAgent, CRAB, Tier-0) perform their own, data-driven matchmaking/site selection before jobs reach this level — e.g. CRAB does data-locality-based matchmaking, and jobs may require data retrieval from tape before running. Marco noted glideinWMS deliberately does not deal with data itself, to avoid scope creep, and that this class of decision-making is intended to move into DIRACX in the future, at which point WMAgent, CRAB, and Tier-0 would rely on it rather than implementing their own site-selection logic. Tier-0 currently does comparatively little site selection ("run a good site, that's it").
- **"Constant pressure" principle**: glideinWMS's request model is not imperative ("submit exactly N glideins now") but is based on constant pressure — the frontend continuously requests a certain number of idle glideins, and factory/frontend interact indirectly through a polling loop rather than a single request/response call. Luis characterized this as more declarative (frontend expresses a desired state; factory works to realize it), which Marco agreed with. Marco noted (as an aside, not confirmed in detail) that other systems like PanDA or DIRAC may not use this same constant-pressure model, instead requesting a specific number of pilots directly.

The group did not reach the "glidein internals" section of the deck in this session and agreed to continue in a future session, likely Thursday or Friday.

## Open Questions

- Which system Marco referred to when saying he wanted to wait before publishing CERN Tier 0 site-token changes further (transcribed as "Tiger," possibly a mis-transcription of OSG Topology or a similar system) — not clarified in the transcript.
- Why the CERN factory process appeared to have restarted around 2pm that afternoon without either Marco or Luis having done so intentionally.
- How exactly work is split between the factory's parallel entry-group worker sub-processes (Marco was not certain of the details).
- Which locally-managed HTCondor configuration files/RPMs on the factory (`GWMSlocal.config`, "batch gap," "99 local tweaks," etc.) are actually in use, how they are deployed (Puppet vs. RPM), and which originate from CMS-provided configuration versus local additions.
- Whether it would be worth periodically comparing factory site-configuration entries against external databases (GOCDB, OSG topology) — raised as a possible idea, not decided.

## Related

[[glideinWMS]] · [[HTCondor]] · [[Factory]] · [[Factory Configuration]] · [[Factory Operations]] · [[Pilot Jobs]] · [[CMS]] · [[OSG]] · [[CERN]] · [[DIRACX]] · [[WMAgent]] · [[CRAB]]

## Source

meeting_saved_closed_caption.txt (from `2026-06-23 15.55.40 Submission Infrastructure Weekly Meeting`)
