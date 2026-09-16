---
type: meeting
date: 2026-07-09
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Luis Simas
  - Hyunwoo Kim
  - Francesco Brivio
topics:
  - BSC ticket and misconception about site whitelisting in submission infrastructure
  - DIRAC team's pilot-submission tooling (InterSeed CE) and discussion of harmonizing pilot submission via HTCondor across CMS/ATLAS/LHCb
  - Fermilab frontend pilots retried with expired tokens
  - Fermilab grid-proxy certificate validity and proxy-to-token migration deadline
  - HTCondor SCHEDD authentication vulnerability and planned upgrade
  - global-pool front-end self-signed certificate expiration and related Apache/Puppet gaps
  - Condor-CE grid-proxy-to-site-token migration epic across 20+ sites
  - network/port documentation for HPC sites with restricted connectivity
  - Grafana/SI alert cleanup and move to percentage-based thresholds
  - Francesco Brivio joining to collaborate on DiracX integration of the global pool
---

# Submission Infrastructure Weekly Meeting

## Summary

The meeting opened with Antonio recapping a ticket involving BSC (labeled as a Tier-3 extension of a Tier-1), where he had pushed back on the idea, discussed with "Kir," that submission infrastructure should handle site whitelisting directly. Antonio reiterated that this is not how the system works: a component in WMAgent produces the full ClassAd for jobs, and matching happens based on that, with the ClassAd decided somewhere along the WM chain; if a substantial change to slot size is genuinely needed, it must go through the proper mechanism, discussed at WLCG (transcribed as "WCG") with the sites, rather than being solved inside submission infrastructure.

Marco reported on a meeting with HTCondor developers, also attended by Alexander (from the DIRAC development team) and Jamie, about a tool the DIRAC team is developing/using ("InterSeed CE" — transcription uncertain) to submit pilots to CEs. Following a suggestion from Marco during the previous week's hackathon, Alexander and Jamie discussed how CMS does pilot submission with HTCondor. Marco is trying to convince the DIRAC team to adopt HTCondor for pilot submission as well, to harmonize the approach across CMS, ATLAS, LHCb, and potentially ALICE, but stressed this is a "nice to have," not something he is pushing hard, and it would be fine if DIRAC decides not to adopt it. Antonio noted this could benefit DIRAC because it currently appears to lack full support for multi-core and GPU pilots, features already available via glideinWMS/HTCondor. Marco clarified the discussion is specifically about the pilot-submission interface layer (equivalent to `arc submit`, `condor submit`, or SSH+`sbatch` for Slurm) rather than about glideinWMS's factory-side scheduling logic; DIRAC currently uses three different interfaces for these three use cases, while CMS does all three via `condor submit` on the factory. DIRAC had also considered working directly at the GAHP protocol level, but Jamie discouraged this as too low-level.

On infrastructure status, Antonio reported no notable news beyond the items already on the agenda; the pool was considered to be in a correct state.

Luis gave an update on the Fermilab frontend pilots-with-expired-tokens issue previously raised by Florian. His understanding is that the affected pilots were all requested by the Fermilab frontend with a valid token, started, and successfully ran a number of payload jobs. At some point the factory tried to remove those jobs, but for an unknown reason the removal request did not complete, and the factory kept retrying the removal; eventually the token used for those retries expired, so the CE was receiving removal requests carrying an expired token. Luis resolved the immediate problem by removing the jobs directly on the factory side, since the corresponding jobs at the CE were already long gone. The root cause of why the original removal did not complete is not understood. Florian reported still seeing some related requests; Luis planned to restart the factory and check again afterward.

On the Fermilab grid-proxy front-end certificate, Antonio noted there is a certificate valid until March next year (2027) that will not be renewed; it serves as a backup (not the main certificate), but the team does not want to run without a backup. The broader goal discussed is to eliminate proxy certificates from pilot submission in favor of tokens by March 2027, which is why there is currently a lot of activity around completing the tokens transition. Luis said he was still catching up on this topic and had understood from the factory ops meeting that the certificate's client EKU was not relevant for CEs; Hyunwoo clarified that what he had said in the factory ops meeting was incorrect, and that the EKU is in fact relevant. After this clarification, Luis confirmed the team has until March 2027.

Antonio relayed a notice from the HTCondor team about a vulnerability in the SCHEDD, fixed by removing a specific authentication method from the SCHEDD configuration (a pre-release security version is already available as an alternative to removing the authentication method). Marco confirmed WMAgent uses this authentication method locally (not remotely), so it is relevant to check across the team's schedds. Marco and Luis agreed to meet Monday morning to plan the upgrade. Marco noted the upgrade approach depends on scope: a minor version bump could be applied directly, but moving to a new major version would require going through ITB first due to possible breaking changes; the team is unsure whether ITB (possibly HTCondor 25) and production (possibly HTCondor 24) are currently on different versions and needs to check. Antonio suggested that, since this is a minor version fixing a bug, it might be possible to skip formal ITB validation and instead upgrade one or two actively used production machines first, observe them, and then continue with the rest to speed up the process; Marco agreed this could be worth investigating for a minor-version case, while noting it is generally good practice to keep production and ITB on the same version. Antonio further explained the vulnerability: a user authorized to submit jobs to a given SCHEDD (access point) could potentially escalate privileges within that SCHEDD. In CMS's case, schedds are not directly open to arbitrary users — only a restricted set of people/processes (running DAG/central agents) submit via `condor_submit` — but CMS Connect is a more exposed case, requiring coordination with Benedetto (name as heard; transcription uncertain) and CMS Connect/"MLT". Luis asked whether Condor-CEs are also affected (confirmed yes) and whether site admins should be told, e.g. at the Monday facilities meeting; Antonio said no — the HTCondor team is already communicating the issue directly to institutions (Antonio had forwarded it to the Condor admin at PIC), site Condor admins are assumed to already be on that distribution list, and a wider CMS-side announcement would likely go against the limited-disclosure period the HTCondor team requested (public announcement expected in a couple of weeks).

Separately, a self-signed certificate on the global-pool front end (used only for monitoring, via an HTTPS endpoint reachable from worker nodes) had expired, triggering a CERN security notice based on automated scanning; the self-signing itself was not the flagged problem, only the expiration. Luis renewed the certificate (still self-signed) but found along the way that this Apache server runs largely on default configuration and is not managed via Puppet, despite being a publicly exposed endpoint; he opened a Jira ticket describing the situation and possible next steps, and agreed to add a reference/guide link to it. Related to this, a monitoring node had Puppet disabled and was temporarily removed from the network by CERN configuration (since re-enabled); this was due to a local monitoring-script change bypassing SSL verification (to tolerate the self-signed certificate) that Puppet would otherwise override — Florian had disabled Puppet specifically because of this. Luis committed the bypass as a temporary fix with a note to remove it once a proper SSL certificate exists. With the certificate now renewed, the team no longer needs to keep Puppet disabled on those machines.

On factory operations, Luis has created an epic with one ticket per site for migrating Condor-CE entries from grid-proxy to site-token authentication, covering more than 20 sites (mostly ARC-CEs), identified via `condor_status` on the factory as configured to use grid proxy; three Tier-1 sites are in the list and are not expected to have problems with site tokens, but will need to be tested. Luis plans to start this work after finishing the ongoing alerts cleanup. Per Marco's earlier suggestion, this work will be announced to CRAB and production teams beforehand since it could disrupt ITB (although usage there is believed to be low); separately, Antonio from Tier Zero asked the team to hold off on production changes for about two weeks until the ongoing heavy-ion run finishes, out of concern about accidentally breaking site configuration and losing processing capacity at large sites, even though Luis considers the change itself low risk. Antonio suggested starting with sites not involved in Tier-0 production (the Tier-1s and a few large US Tier-2s) in the meantime, which Luis agreed made sense, also because those sites may be slower to respond/act.

On dynamic resources, Luis is compiling (a request originating from Stefano) a list of machines and ports in submission infrastructure that need to be reachable from worker nodes, to document connectivity requirements for sites that want to restrict outbound connectivity — relevant in particular for some HPC sites. Antonio suggested the list needs context beyond the central machinery (the "major part"): the list of SCHEDDs also matters, and some of those may need special treatment depending on whether they serve production or analysis jobs and whether they are in the US or Europe, since some HPCs only run production jobs or only trust connections from specific ranges (e.g. CERN IPs). Marco proposed preparing two port-range sets: a "complete" set needed for full, error-free functionality, and a "minimal" set for sites imposing restrictions. Luis agreed this made sense but raised a concern about the failure mode if an HPC restricted access to a SCHEDD the pilot still needed — he was unsure exactly how that would manifest and how it would be troubleshot, though he agreed most site admins would likely just allow everything, and the two-list approach fits the base case (Stefano's goal being primarily to document readiness for CMS jobs). Antonio noted this connectivity negotiation is also a "political" trust question, citing VSC as historically very restrictive (no external connectivity accepted) and Cineca as an example that accepted connections specifically because the submitting machines were based at CERN. Antonio emphasized that HPC sites generally operate as isolated "islands" outside the grid mindset and are not used to trusting an external, real-time submitting/manipulating partner, so the minimal list represents the baseline ask for CMS to be able to work with such sites at all. Luis noted the connectivity in question is outbound only, which he expects to be easier to negotiate than inbound; Antonio agreed this can help, while maintaining that these sites' security models are still generally very restrictive.

On alerts, Luis reported deleting all factory-related Grafana alerts, which are not used. For SI (Sensu?) alerts, he is reviewing thresholds and messages; his current focus is the idle-cores-in-the-global-pool alert, which he proposed changing from a hard-coded threshold (currently around 10,000–12,000 idle cores) to a percentage-based threshold (e.g. 10%). Antonio and Marco both agreed this is desirable; Antonio recalled that there had been some earlier issue or limitation preventing a percentage-based approach, but was confident this is the preferred direction now. Luis plans to share results next week so thresholds can be tuned based on feedback, and noted that "GNI Alerts" (as transcribed) still need attention but have not yet been reviewed.

Francesco Brivio joined the meeting as a guest, invited by Marco (who was hosting him in person at the Milano-Bicocca office) because Francesco will collaborate on the DiracX integration of the global pool. Francesco said the discussion was still mostly new to him and that he would follow future meetings to catch up.

## Decisions / Conclusions

- Submission infrastructure does not perform site whitelisting; the full job ClassAd is produced within the WMAgent/WM chain, and matching is done against it. Any substantial change to slot size must go through the proper mechanism (discussion at WLCG with the sites), not be resolved within submission infrastructure.
- HTCondor adoption for DIRAC pilot submission is a proposed harmonization goal across CMS/ATLAS/LHCb (and potentially ALICE), not a requirement; the team is comfortable if DIRAC does not adopt it.
- Working directly at the GAHP protocol level (considered by the DIRAC team) was discouraged by Jamie (HTCondor developer) as too low-level.
- The team has until March 2027 to eliminate proxy certificates from pilot submission in favor of tokens, aligned with the expiration of the Fermilab backup grid-proxy certificate; the certificate's client EKU is relevant for CEs (correcting an earlier, incorrect statement Hyunwoo had made in the factory ops meeting).
- WMAgent uses the HTCondor authentication method affected by the SCHEDD vulnerability locally, so a fix/upgrade is needed; the remote variant of this authentication method is not used.
- CMS's schedds are not broadly exposed to the SCHEDD-privilege-escalation vulnerability since only a restricted set of processes submit directly; CMS Connect is a more exposed access point and requires coordination with Benedetto (name as heard) and the CMS Connect/MLT side. Condor-CEs are also affected by the vulnerability.
- The team will not make a wider (e.g. facilities-meeting) announcement about the SCHEDD vulnerability, since the HTCondor team is already notifying institutions/site Condor admins directly and a broader announcement would work against the intended limited-disclosure window.
- The global-pool front-end monitoring certificate issue was caused by expiration, not by being self-signed; renewing it (still self-signed) resolves the immediate CERN security notice. The underlying Apache server is not Puppet-managed and runs largely on default configuration despite being publicly exposed — flagged for follow-up via a new Jira ticket.
- The SSL-verification-bypass workaround on the affected monitoring node, and the associated Puppet-disable done by Florian, are no longer needed now that the certificate has been properly renewed.
- Condor-CE grid-proxy-to-site-token migration will start with sites not involved in Tier-0 production (Tier-1s and a few large US Tier-2s); other Tier-0-relevant production changes will be held for about two weeks until the current heavy-ion run finishes, per a request from Antonio (Tier Zero); the migration work will be announced to CRAB and production teams beforehand due to possible ITB disruption.
- For the HPC connectivity documentation, the team will prepare two port/machine lists: a "complete" set for full functionality and a "minimal" set for sites that need to restrict connectivity, pushing for the complete/open set as the default ask.
- Moving the idle-cores-in-global-pool alert from a hard-coded threshold to a percentage-based threshold is the agreed direction; exact percentage to be tuned after initial results are shared.

## Action Items

- [ ] Restart the factory and check whether Fermilab-frontend pilot requests with expired tokens are still occurring — Luis Simas
- [ ] Meet Monday morning to plan the HTCondor SCHEDD-vulnerability upgrade across global pool schedds and factory, including checking current ITB vs. production HTCondor versions — Marco Mascheroni, Luis Simas
- [ ] Coordinate with Benedetto (CMS Connect/MLT) regarding the SCHEDD vulnerability
- [ ] Add a reference/guide link to the Jira ticket documenting the global-pool front-end certificate/Apache-configuration issue — Luis Simas
- [ ] Start the Condor-CE grid-proxy-to-site-token migration after finishing the alerts cleanup, beginning with non-Tier-0-production sites, and announce the work to CRAB and production teams beforehand — Luis Simas
- [ ] Prepare "complete" and "minimal" port/machine connectivity lists for the HPC network-documentation effort — Luis Simas
- [ ] Share results of the percentage-based idle-cores alert changes next week for threshold tuning — Luis Simas

## Discussion

See Summary above for full discussion detail on each topic.

## Open Questions

- Why did the factory originally receive job-removal requests from the Fermilab frontend that failed to complete, leading to the expired-token retry issue (no known failover event was identified around that time)?
- How would a connectivity failure manifest and be troubleshot if an HPC site restricted access to a SCHEDD that a pilot still needed to reach?
- What exactly do the "GNI Alerts" (as transcribed) refer to, and what fixes do they need? Not yet reviewed by Luis.

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[DIRAC]] · [[DIRACX]] · [[Pilot Jobs]] · [[Factory Operations]] · [[Factory Configuration]] · [[WLCG]] · [[HPC]] · [[GPU]] · [[Monitoring]] · [[CMS]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-09 17.18.17 Submission Infrastructure Weekly Meeting`)
