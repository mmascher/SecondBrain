---
type: meeting
date: 2026-07-24
participants:
  - Marco Mascheroni
  - Luis Simas
topics:
  - glideinWMS Factory architecture
  - entry group internals
  - proxy and token encryption
  - HTCondor security patching status
---

# GlideinWMS Factory Architecture Walkthrough

## Summary

Marco Mascheroni walked Luis Simas through the internal architecture of the [[glideinWMS]] Factory: how entry-group monitoring XML files are generated, how entry attributes are structured and overridden, and how proxies and tokens are encrypted between the front end and the Factory. The meeting closed with a short, separate discussion on the status of an [[HTCondor]] security-related update across CMS Connect, production, and [[CRAB]] systems.

## Decisions / Conclusions

- CRAB was confirmed to already be running a patched HTCondor schedd version (25.0.12), so no further action was needed for CRAB with respect to the update in question.
- No decision was made on whether/when to push the pending update to the remaining unpatched systems (CMS Connect and the system associated with Carl Vuosalo); this remained open.

## Action Items

None identified.

## Discussion

### Entry-group monitoring files

The Factory's per-entry monitoring XML files are static files generated during `reconfig`. Each file name includes a short timestamp component so that a fresh copy is produced whenever files might be served through a Squid cache, avoiding stale reads. Marco noted he was unsure how much Squid caching is actually used for these downloads today, though the mechanism supports it.

### Factory and entry-group processes

- The **glidein Factory** process starts the entry-group processes and aggregates their monitoring output.
- Each **entry group** process serves multiple entries. It runs a continuous loop: advertise entry attributes to the collector, read/retrieve requests, submit pilots via **Condor-G**, monitor pilot status (also via Condor-G), then advertise and resubmit as needed.
- Monitoring information is stored both in internal log files and published for web access; each entry group produces one XML file per entry, and an aggregate file combines them (the transcript's rendering of this aggregate filename was unclear and is not repeated here as a reliable name).
- Everything advertised to the collector is ClassAd-based, and access control is implemented at the collector.
- The frontend queries the collector to select relevant entries; entries are visible via a `condor_status` query on the entries advertised by the entry group.
- One entry can serve multiple front ends, in which case it holds a proxy per front end.
- A "cloud entry" was mentioned as an opportunistic entry type with comparatively few configured attributes.

### Entry attributes

- Attribute fields come from the entry's XML configuration. Required fields include the entry name, hostname, grid type, gatekeeper, and submit attributes; the attribute name must be unique (the site name does not need to be).
- Container/job-wrapper execution previously used a "jail"-type mechanism; the group now uses [[Singularity]] instead.
- Optional attributes (e.g., a CMS site attribute) exist for matchmaking; Marco noted the CMS `Infosys`-related attribute is believed to no longer be used.
- Front-end attributes can override Factory entry attributes as defaults, unless the Factory marks a given parameter as **constant**, in which case it cannot be overridden by the front end.
- Marco described the mechanism controlling whether an attribute can be published/overridden (a combination of "publish" and "const" flags producing different effective behaviors on the glidein startup command line) as confusing and something he has never fully liked. He said the team has long intended to improve this but never prioritized it over more visible/impactful work. This is an opinion, not a decision to redesign it.

### Matchmaking behavior and over-provisioning

- The front end requests pilots per **site**, not per individual entry; it determines which entries (CEs) belong to a requested site and sends a request to all of them.
- For each job, the front-end matchmaking logic checks entry-by-entry whether the job's requested site matches the entry's site, incrementing a request counter on each match; since one job can match multiple entries for the same site, this behaves as a form of over-provisioning.
- The Factory looks at idle counts and submits (or removes) glideins to close the gap between requested and idle pilots.
- Marco's assessment (an opinion/observation, not a settled conclusion) was that this over-provisioning is likely unintentional but harmless and possibly beneficial in practice, because the system normally runs in a saturation/constant-pressure mode with already-overqueued schedulers, so the extra pilots do not cause a practical problem and nobody has complained.

### Proxy and token security

- Proxies (and, similarly, tokens/site tokens) are delivered from the front end to the Factory as encrypted ClassAd attributes.
- The Factory generates a public/private key pair and publishes the public key via its ClassAd; the front end encrypts the proxy or token using that public key, and the Factory decrypts it with its private key.
- In response to Luis's question about the reasoning, Marco confirmed the assumption is that the collector itself is not a trusted/secure location — any client can read what is advertised there — so sensitive data (proxies, tokens) must be encrypted before being placed on the collector.
- Historically, each front end mapped to a separate user identity on the Factory (a front-end-to-UID mapping). Marco and Luis confirmed this is no longer the case: front ends are now consolidated under a shared Factory identity (referred to as "gfactory").
- Marco raised, without resolving, a security implication of this consolidation: if a front end were compromised and could manipulate its ClassAd, it might be able to make the Factory act on its behalf in ways that expose or affect other VOs. This was left as a raised concern rather than a conclusion.

### HTCondor security update status (brief, separate topic)

- Luis raised, as an aside, that certain systems ("SCADs"/schedds, per the transcript) needed an update following a security incident.
- Marco said he had messaged the people responsible for CMS Connect and for another affected system (associated with Carl Vuosalo, correcting an earlier mix-up over the name) the previous day but had not received a response.
- Marco proposed the question of whether to proceed and update all affected systems regardless, accepting the risk of breakage. Luis confirmed they have the technical ability to do so, but noted the group would need to check how versions are deployed/locked for the VOCMS-managed production instance before doing so (the exact deployment/config-management mechanism mentioned was unclear in the transcript).
- Luis distinguished a security **incident** (something actually exploited) from a **vulnerability** (a latent risk), implying the current situation had not yet been confirmed as an active exploitation.
- Luis looked up the relevant email and confirmed CRAB's schedd was already running version 25.0.12, which is the patched version, leading Marco to conclude CRAB did not need further action.

## Open Questions

- Whether and when to proceed with updating the remaining unpatched systems (CMS Connect and the Carl Vuosalo-associated system) given no response from the responsible people.
- How versions are deployed/locked for the VOCMS-managed production instance, and whether that constrains an immediate update.
- Whether the shared Factory identity model ("gfactory") for front ends poses a realistic cross-VO security exposure if a front end were compromised.

## Related

[[glideinWMS]] · [[HTCondor]] · [[Submission Infrastructure]] · [[Factory Operations]] · [[CRAB]] · [[Singularity]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-24 15.25.48 Submission Infrastructure Weekly Meeting`)
