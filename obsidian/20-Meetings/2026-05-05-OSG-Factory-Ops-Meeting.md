---
type: meeting
date: 2026-05-05
participants:
  - Jeff Dost
  - Marco Mascheroni
  - Hyunwoo Kim
  - Luís Simas
topics:
  - Kernel privilege-escalation vulnerability ("CopyFail") response and patching
  - Condor CE auth method migration to site token
  - glideinWMS ARM architecture-requirement patch status
  - Docker/Kubernetes container escalation risk
  - Pilot-efficiency monitoring for CHEP
---

# OSG Factory Ops Meeting

## Summary

The meeting focused on the previous week's response to a kernel privilege-escalation vulnerability, transcribed as "CopyFail" (exact name/CVE unclear from the transcript), which affected execute points (EPs) and required patching. Hyunwoo Kim reported that Fermilab patched and rebooted all its machines in response to both this vulnerability and an unrelated power outage. Jeff Dost described how OSG responded operationally (temporarily shutting off the OSpool glidein pool, then cautiously re-enabling it) and raised concerns about CMS management's risk posture, leading to an extended discussion with Marco Mascheroni about attack scenarios, the role of Singularity/containers, and unresolved questions about Docker/Kubernetes escalation risk. Luís Simas reported no progress on the Condor CE site-token migration, as CHEP-related pilot-efficiency monitoring work took priority. Marco reported he still needs to implement changes to his glideinWMS ARM architecture-requirement patch, based on a suggestion from Jamie, and plans to discuss it with Marco Mambelli the next day.

## Decisions / Conclusions

- Fermilab patched and rebooted all of its machines in response to the CopyFail vulnerability (in addition to responding to a separate power outage the same week). No ongoing concerns were reported.
- OSG's initial response to the vulnerability was to shut off the entire OSpool glidein pool (on Thursday), primarily to ensure APs were patched; the pool was cautiously and gradually re-enabled, reaching full scale again by Friday.
- OSG decided against running an automated validation/mitigation-check script across sites, because Brian Bauman raised concern that it could trigger false positives and make sites think OSG was attempting to exploit the vulnerability against them.
- CMS's operating assumption is that patching vulnerable sites is ultimately the site's own responsibility, though Jeff expressed personal reservations about relying on this given the potential impact of a compromised EP (credential theft, glidein code modification, exposure of user-job data).
- For CMS's CE/collector ("central") machines, the decision was to wait for the official AlmaLinux 9 patch and install it rather than run any interim mitigation, since only already-privileged operators have access to those machines.
- CMS decided to patch the worker nodes for the CopyFail vulnerability (confirmed explicitly for Fermilab in response to a direct question).
- Per information from Todd Tenenbaum (HTCondor team), a process running inside Singularity cannot use this particular escalation mechanism to break out, because Singularity ships its own set of UIDs. This protection does not apply to an arbitrary job submitted directly to a site's batch system outside of the OSG-managed glidein.
- CMS runs its pilot/job workloads in containers (Singularity), which Marco noted is a mitigating factor for this particular escalation path.
- The Condor CE site-token auth-method migration plan (agreed previously) remains: first verify via the ITB setup that site tokens still work at the sites CMS believes they should, then update the relevant entries. This work has been deprioritized behind CHEP-related work and has not yet started.

## Action Items

- [ ] Implement the suggested changes (from Jamie) to the glideinWMS patch addressing the ARM/architecture-requirement issue, and discuss it with Marco Mambelli and other glideinWMS developers, aiming to finish by the next day so a release candidate can proceed — Marco Mascheroni

## Discussion

### CopyFail vulnerability response and risk discussion

Jeff described the timeline and reasoning behind OSG's response: upon discovering the vulnerability, the pool was shut down (Thursday) primarily to ensure APs were patched, and to allow time to consider the implications of sites that remained vulnerable. One idea considered was running an automated check to detect whether a site had applied the patch or mitigation, potentially as part of a validation script; this was dropped after Brian Bauman raised concern that it might be mistaken by sites as an actual exploitation attempt. Instead, OSG proceeded cautiously, gradually re-enabling the pool, reaching full scale by Friday.

Jeff raised his personal concern about relying on sites' own responsibility to patch: any unprivileged job submitted to a site's batch system (not just glideins) could exploit the vulnerability to get root on an EP before it is patched or mitigated, potentially stealing pilot credentials, modifying glidein behavior while it continues to accept user jobs, or exposing user-job data/credentials to the attacker.

Marco initially argued he was less worried about EPs specifically, since the credentials shipped with the pilot are limited (read/write access to data), so a malicious actor's main leverage would be filling disks or denial-of-service against the collector, rather than broader compromise. Marco also noted that exploiting this would require an attacker who already has a legitimate CMS credential and access to a worker node — i.e., someone already inside the CMS community.

Jeff pointed out a scenario Marco had not considered: an attacker need not come through CMS's own pool at all — a different user with independent access to a site's batch system could exploit the vulnerability directly, without needing any CMS credential or expertise in glideinWMS/HTCondor. Jeff also noted that, in an AI-agent era, an attacker no longer needs deep personal expertise in the exploited systems. Marco agreed this was a use case he had not considered, and distinguished CE/collector ("central") machines — where only already-privileged operators have access, making them comparatively safer — from worker nodes, which he acknowledged are more exposed.

Jeff stated that, ideally, EPs that are not yet patched should be avoided entirely, but noted that reliably detecting this is difficult — which he described as the reason OSG "gave up" on the validation-script approach.

Marco asked whether running workloads in containers changes this risk. Jeff said it does not help if the attacker already has root on the EP: with root, an attacker can manipulate or restart the container, or modify and restart the container image — "nothing is safe" once root is obtained on the host.

### Docker/Kubernetes escalation risk (open/unresolved)

Jeff noted he has not yet learned whether a bad actor running inside a Docker container under Kubernetes can escalate to the underlying bare-metal machine using this vulnerability, and has not seen updates from anyone on this. Marco asked whether this would behave the same way as Singularity. Jeff said not necessarily — Singularity's protection in this case stems from it shipping its own set UID mechanism, whereas Docker/Kubernetes routinely mounts external paths (e.g., for PVCs) into containers, which could present other avenues. Marco noted Docker also performs user ID remapping, but Jeff said this could still be exploited, and that if the base container image's OS kernel is itself vulnerable, the vulnerability already exists inside the container regardless of UID remapping.

### Fermilab status (Hyunwoo Kim)

Hyunwoo reported dealing with two outages the previous week: a power outage and the CopyFail vulnerability. Fermilab patched and rebooted all machines in response; no ongoing concerns remain. Hyunwoo was on vacation from Tuesday afternoon onward, making it a slow week otherwise. He also noted there had been some internal confusion about how serious the vulnerability was and whether a full patch-and-reboot was warranted, since some had characterized it as relevant only to end users who already have access to a machine; most of Fermilab's machines are servers rather than EPs. Jeff pointed out that EPs are an exception to that reasoning, since submitted jobs count as a vector too — something he suggested some people may not be considering.

### Condor CE auth method migration to site token

Hyunwoo, noting he may have missed part of Luís's earlier report, asked for clarification on the current plan, recalling that two weeks prior the plan had sounded straightforward: go through entries with a proxy-based auth-method attribute and update them to site tokens. Jeff clarified that CMS wants to first verify via the ITB setup that site tokens still work after such a change, to confirm token authentication actually works at the sites they expect it to, before making changes — Luís confirmed this was correct. Luís reiterated he has not yet started this work because pilot-efficiency monitoring for CHEP has taken priority.

### CHEP-related work status

Luís reported no updates on the auth-method work, as his time has gone toward pilot-efficiency monitoring for CHEP, which he said is reaching better shape — it can now identify the impact of overloading on efficiency.

### glideinWMS patch / release status

Marco said he still needs to finish a patch for glideinWMS related to the architecture-requirement issue discussed the previous week (affecting ARM pilots), and had received a suggestion from Jamie on how to improve the patch, which he still needs to implement. He plans to discuss it with Marco Mambelli and other glideinWMS developers the next day, aiming to get it done so a release candidate can proceed. Jeff noted he had checked that morning and believes the release is waiting on some last-minute items.

## Open Questions

- Whether a bad actor running inside a Docker container under Kubernetes can escalate to the bare-metal host via this vulnerability (or a related mechanism).
- Whether there is a reliable way to detect EPs that have not yet been patched or mitigated, given that an automated validation-script approach was rejected over false-positive concerns.
- Whether/how user-job credentials could be exposed to an attacker via a compromised glidein.
- When the next glideinWMS release candidate (incorporating Marco's architecture-requirement fix) will be available.

## Related

[[OSG]] · [[CMS]] · [[CERN]] · [[HTCondor]] · [[glideinWMS]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Kubernetes]] · [[Docker]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-05 17.08.47 OSG Factory Ops Meeting`)
