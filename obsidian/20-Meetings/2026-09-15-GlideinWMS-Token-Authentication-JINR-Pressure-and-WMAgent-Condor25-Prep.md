---
type: meeting
date: 2026-09-15
participants:
  - Marco Mascheroni
  - Pablo Izquierdo Gonzalez
  - Gregor
topics:
  - glideinWMS front end / factory authentication: token-based auth replacing X.509 proxies
  - Factory collector and custom ClassAds as the front end/factory communication mechanism
  - JINR ("Jinner"/Russian site) resource-usage drop investigation
  - WMAgent created/idle job limits and the "Condor jobs fraction" configuration
  - HTCondor 25 rejecting submissions from the OS user "condor"
  - WMAgent architecture recap (access point, components, per-site agents)
  - Hands-on Puppet/Condor 25 upgrade attempt on a schedd (VOCMS 0259)
---

# GlideinWMS Token Authentication, JINR Pressure Investigation, and WMAgent Condor 25 Prep

## Summary

This Submission Infrastructure weekly session combined continued onboarding of Pablo Izquierdo Gonzalez with a live troubleshooting/planning segment involving Gregor (from the PNR/P&R team), followed by more hands-on training.

Pablo had been reviewing an older glideinWMS front-end presentation and asked Marco Mascheroni to confirm which parts were outdated. Marco confirmed that the described X.509 proxy-based mutual authentication between front end and factory is no longer used; the infrastructure now uses token-based authentication throughout. Marco also walked through how the factory and front end actually communicate: the factory runs its own HTCondor collector (described as an in-memory database of ClassAds), and both the factory and front end publish custom ClassAds to it; the front end queries (polls) this collector to retrieve information from the factory, rather than the factory pushing to the front end. Pablo separately asked about a "second proxy" for glidein submission mentioned in the old material; Marco said that's also no longer accurate — three separate tokens are now used: one for front end-to-factory authentication, one for the factory's glidein/pilot submission to sites, and one for worker-node-to-collector authentication (to the global pool collector, VOCMS 14100).

Gregor then joined to raise three items. First, a WMAgent test/QA agent (VOCMS 0259, described as a former "revel"/production agent now repurposed for lower-priority testing) is being used to test HTCondor 24 vs. 25 (with old vs. new certificates) at Fermilab; Gregor proposed also testing at CERN, and Marco agreed, suggesting they target the latest stable 25.0.x series. Second, Gregor reported that CMS appears to be using roughly half as many cores as before at JINR ("Jinner," a Russian site) — a drop first noticed around six months prior. Gregor recalled a JINR-side scheduling-priority change from roughly a year earlier (jobs with priority above 85K not scheduled there), but noted running-job levels had stayed steady for six months after that change, so a causal link was unclear. Marco investigated live using Submission Infrastructure slot-monitoring and factory-monitoring pages/queries, and concluded that the front end was not requesting many idle pilots for JINR because the pool of idle CMS jobs actually targeting JINR was very low (on the order of resulting in the front end's demand-based logic requesting close to zero idle pilots there) — i.e., low job "pressure" from the CMS side, rather than a reduction in resources offered by the site. Third, Gregor asked about limits on the number of jobs a WMAgent can create/run, referencing a "Condor jobs fraction" configuration value (e.g. 0.3 on scheduler 0253) that appeared to cap created jobs around 30,000 (idle or running) in a low-efficiency agent, even when Gregor tried adding more jobs after raising the fraction from 0.2 to 0.3. Marco checked the schedd's HTCondor configuration and found no scheduler-side setting that would explain a 30,000-job cap, concluding the limit likely originates in WMAgent's own logic tied to the "Condor jobs fraction" value rather than in HTCondor itself; Marco also confirmed there is no SI/global-pool-layer mechanism limiting what fraction of jobs can be routed to a given site.

Gregor's last topic was a WMAgent submission error under HTCondor 25 ("fail to create new user record for condor"). Marco interpreted this as HTCondor now rejecting job submissions made under the OS user literally named `condor` (a privileged/reserved account), which is what happens by default when `condor_submit` is invoked directly as that user rather than as a designated service account. The affected Fermilab agents run as `cmsdataops`, while CERN agents run as `cmst1`; both would need to avoid submitting as the `condor` OS user. Gregor and Marco agreed this is managed on the WMCore/agent-deployment side (how the agent container is started, e.g. via a CMS Kubernetes startup script) rather than something HTCondor manages directly, though Marco characterized the rejection itself as HTCondor-enforced behavior. Gregor described the near-term plan: cut a new WMAgent patch release (0.9) today with the latest changes, have the PNR/P&R team deploy it to the CERN test agent (VOCMS 0259) so Condor 25 can be installed there, and run parallel comparison tests at Fermilab. Marco asked Gregor to use the public SI Mattermost channel going forward instead of private conversations, so the wider team stays informed.

After Gregor left, Pablo asked clarifying questions about WMAgent's architecture: it runs on (rather than being) the access point, as a set of components under a `WMCoreD` daemon running inside a Docker container, one of which submits jobs to Condor. There is one production WMAgent per access point; CRAB (analysis jobs) and Tier-0 (which runs a modified WMAgent) are separate cases. Gregor's team (PNR) is responsible for the production WMAgents.

The remainder of the session was hands-on: Marco and Pablo attempted to add HTCondor 25 as an installable option via Puppet on a schedd (initially unclear whether it was 0253 or 0259; they confirmed it was 0259, running the QA/master Puppet environment branch, distinct from production). They found the existing Puppet-managed yum repository configuration only defined a Condor 24 repository entry (with an embedded username/password for that repo) and no 25 entry; they were unable to complete adding the 25 repository during the session, running into Puppet/git-access friction (Marco noted he had not personally done a Puppet checkout/update in roughly two years) and uncertainty about credentials for the Condor 25 repository. They also identified they should target installing Condor 25.0.13 (the long-term-support/stable series) rather than 25.0.14 (a security-patched version not yet available on the public repository), since this exercise was about validating the 24→25 upgrade path rather than the security fix itself. Marco explained the team's standard production-upgrade process: validate the new version on the ITB (integration test bed) first, then install it directly on the production host — there is no side-by-side run of two versions, unlike the machine-replication approach Pablo was used to at his previous Tier-2. Marco also flagged that updating the production central manager (VOCMS 14100) to Condor 25 is the next step after the schedd, noting the ITB central manager is already on 25.

## Decisions / Conclusions

- The old glideinWMS front-end/factory presentation Pablo reviewed is outdated on authentication: X.509 proxy-based mutual authentication is no longer used. Token-based authentication is used throughout, via three separate tokens: front end-to-factory, factory glidein/pilot submission to sites, and worker-node-to-collector (global pool collector, VOCMS 14100).
- The factory runs its own HTCondor collector; both factory and front end publish custom ClassAds to it, and the front end queries this collector to obtain information from the factory (pull model, not push).
- JINR's apparent resource-usage drop was attributed (with reasonable but not fully certain confidence) to low job "pressure" from the CMS side — too few idle jobs targeting JINR for the front end to request more idle pilots there — rather than a reduction in resources offered by the site itself.
- No HTCondor scheduler-side configuration was found that would explain a ~30,000-job creation/idle cap on the low-efficiency WMAgent; the cap is suspected to originate in WMAgent's own logic tied to its "Condor jobs fraction" configuration value, not in HTCondor.
- There is no Submission-Infrastructure/global-pool-layer mechanism that limits what fraction of jobs can be routed to a given site.
- The WMAgent submission error under Condor 25 ("fail to create new user record for condor") is understood as HTCondor now rejecting submissions made under the OS user literally named `condor` (a privileged account); the fix is to ensure agents submit under their designated service accounts (`cmst1` at CERN, `cmsdataops` at Fermilab) rather than as `condor`. This OS-user configuration is managed on the WMCore/agent-deployment side, not by HTCondor.
- For the Condor 25 upgrade test on the schedd, the target is 25.0.13 (stable/LTS series), not the newer 25.0.14 security-patched release, since the latter is not yet available via the public repository and this test concerns the 24→25 upgrade path, not the security fix.
- Standard production HTCondor upgrade process: validate on ITB first, then install the new version directly on the production host (no parallel dual-version run).

## Action Items

- [ ] Cut a new WMAgent patch release (0.9) with the latest changes — Gregor
- [ ] Deploy the new WMAgent release to the CERN test agent (VOCMS 0259) so Condor 25 can be installed there — PNR/P&R team (Gregor)
- [ ] Run comparison tests of Condor 24 vs. 25 at Fermilab in parallel with the CERN test — Gregor
- [ ] Use the public SI Mattermost channel (instead of private messages) to communicate progress on the WMAgent/Condor 25 work — Gregor
- [ ] Ask around the PNR team about testing the actual maximum job-submission threshold achievable at JINR — Gregor
- [ ] Investigate/test whether more idle jobs can be generated targeting JINR to increase pilot request pressure — Marco Mascheroni
- [ ] Try to catch live (or check logs/config) why the WMAgent cannot submit more than ~30,000 jobs, and report back — Pablo Izquierdo Gonzalez
- [ ] Get Puppet access and understand how the team's Puppet repositories are organized, talking to Luis Simas (once back) and/or pinging Florian on the public SI Mattermost channel if needed — Pablo Izquierdo Gonzalez
- [ ] Add a Condor 25 yum repository entry to the Puppet configuration for the test schedd (VOCMS 0259) this week — Pablo Izquierdo Gonzalez
- [ ] Attend today's factory ops meeting — Pablo Izquierdo Gonzalez

## Discussion

### Authentication: tokens replacing X.509 proxies
Pablo, reviewing an older glideinWMS front-end presentation, asked Marco to confirm which details were outdated. Marco confirmed that mutual X.509-proxy authentication between front end and factory has been replaced by token-based authentication. The old material's mention of a "second proxy" for glidein submission is similarly outdated: three tokens are now used — front end-to-factory, factory-to-site glidein submission, and worker-node-to-collector (targeting the global pool collector, VOCMS 14100).

### Factory collector and ClassAd-based communication
Pablo asked about a diagram element showing "the factory collector puts special attributes on the class ad," which he found confusing since he hadn't previously understood the factory to run its own collector. Marco explained the factory runs its own HTCondor collector (an in-memory ClassAd store), on which both the factory and the front end publish custom ClassAds in order to communicate; the front end queries this collector to retrieve the factory's information (entries/queues per site), rather than the factory pushing data to the front end.

### JINR resource-usage drop
Gregor reported that CMS appears to be using about half as many cores as before at JINR, first noticed roughly six months ago. He recalled a JINR-side scheduling change from about a year prior limiting jobs with priority above 85K from being scheduled there, but noted running-job counts had stayed steady for six months after that change, making a causal link to the recent drop unclear. Marco investigated live via SI slot-monitoring and factory-monitoring pages: the front end's idle-pilot request for JINR was going to (or near) zero, and a check of idle jobs queued against JINR as a desired site showed a low count — not enough, in Marco's assessment, to generate sufficient pilot-request pressure to fill JINR's capacity. Marco and Gregor agreed the likely explanation is that CMS-side job "pressure" toward JINR is currently too low, rather than the site providing fewer resources.

### WMAgent created-job limits and "Condor jobs fraction"
Gregor asked whether WMAgent job-creation counts can be manipulated: in a low-efficiency agent, jobs were capped around 20,000–30,000 via a "Condor jobs fraction" parameter (schedd 0253, set to 0.3, up from an earlier 0.2), which Gregor connected to a 100,000-jobs-per-user HTCondor limit (0.3 × 100K ≈ 30K). When Gregor previously tried adding more jobs after raising the fraction, no additional jobs (not even idle ones) were created. Marco reviewed HTCondor scheduler configuration (`MAX_JOBS_PER_OWNER`, per-submission limits, etc.) and found nothing that would explain a hard 30,000 cap, tentatively concluding the limit is more likely enforced within WMAgent's own logic tied to the "Condor jobs fraction" value. Marco suggested Gregor retry with a schedd using a higher fraction (e.g. scheduler 255 at 0.75, implying ~75,000 jobs) and check WMAgent logs for possible file-descriptor-related errors. Separately, Gregor confirmed there is no SI-layer mechanism (e.g., a config file) that limits what fraction of jobs is routed to a given site; Marco confirmed the same.

### Condor 25 and the "condor" user submission error
Gregor shared an error ("fail to create new user record for condor") seen when testing WMAgent submission under Condor 25/25-related changes, using the CMST1 user (their 0.8 agent still authenticates via robot certificates rather than tokens). Marco's interpretation: HTCondor now rejects `condor_submit`-equivalent calls made under the OS user literally named `condor`, since that username is privileged/reserved. Fermilab agents run as `cmsdataops`; CERN agents run as `cmst1`. Gregor asked whether this is purely a WMCore/agent concern or also involves an HTCondor-side change; Marco's read was that the rejection is HTCondor-enforced, but which OS user the agent submits as is controlled by how the agent container is started (a CMS Kubernetes startup script), which is a WMCore/deployment-side concern, not something HTCondor manages. Gregor outlined the near-term plan: release WMAgent 0.9 today, have PNR/P&R deploy it to VOCMS 0259 (CERN test agent) to allow installing Condor 25 there, and run parallel Fermilab tests to compare CERN and Fermilab behavior. Marco asked Gregor to report progress via the public SI Mattermost channel.

### WMAgent architecture recap
Following Gregor's departure, Pablo asked Marco to clarify WMAgent's role: it runs on the access point (rather than being a separate machine/entity), inside a Docker container managed by a `WMCoreD` daemon that runs multiple components, one of which is responsible for submitting jobs to Condor. There is one production WMAgent per access point; CRAB (analysis jobs) is a separate, unrelated system, and Tier-0 runs a modified version of WMAgent for its own production processing. Gregor's team is the PNR (production) team.

### Hands-on Puppet / Condor 25 upgrade attempt
Marco and Pablo worked through applying a Condor 25 upgrade via Puppet to a test schedd, initially unsure whether the relevant host was 0253 or 0259 (confirmed to be 0259, running the QA/master Puppet branch). They found the DOCMS host group's existing yum repository definition only configured a Condor 24 repository (with an embedded username/password), and no equivalent Condor 25 entry; Pablo suggested the Condor 25 repository would need similar credentials, possibly obtainable from the Condor developers. They distinguished this repository (managed by Submission Infrastructure) from a separate, unrelated repository used by the site-support team to generate yum/repo files. Marco had difficulty with git/Puppet commands during the session, noting he had not personally done a Puppet checkout/update in roughly two years, since operators have typically handled this. They identified the correct target as Condor 25.0.13 (the long-term-support/stable series), rather than 25.0.14 (a newer security-patched release not yet available via the public repository) — the schedd upgrade exercise concerns the 24→25 transition, not the security fix. The session ended without successfully completing the repository addition. Marco explained the team's standard upgrade process going forward: validate a new version on ITB first, then install it directly on the production host (no side-by-side dual-version run, unlike Pablo's prior Tier-2 experience of replicating machines). Marco noted the next step after this schedd work is to also update the production central manager (VOCMS 14100) to Condor 25, mentioning the ITB central manager is already running 25.

### Onboarding approach
Marco reflected that this session mixed deeper technical/incident-style discussion with the usual structured training, and suggested this back-and-forth is a reasonable strategy going forward.

## Open Questions

- Whether JINR's year-old scheduling-priority change (jobs above 85K priority not scheduled) is actually related to the six-months-ago drop in running jobs there — the six months of unchanged running-job levels after that change makes the link unclear.
- Why WMAgent could not submit more than ~30,000 jobs even when Gregor attempted to add more (including idle jobs) — not resolved; Pablo was asked to try to observe this live.
- Whether raising the "Condor jobs fraction" value (as apparently done on scheduler 255, at 0.75) would allow more jobs to be created.
- Whether the Condor 25 "condor" user submission error also involves any change on the HTCondor side beyond the privileged-username rejection, versus being purely a WMCore/deployment-side configuration issue.
- Which Puppet class/repository manages the Condor package on the production central manager (VOCMS 14100), and how the Condor 25 yum repository should be added there.
- Where to obtain valid credentials for the official Condor 25 yum repository (parallel to those already present for the Condor 24 repository).

## Related

[[glideinWMS]] · [[Frontend]] · [[Factory]] · [[HTCondor]] · [[WMAgent]] · [[WMCore]] · [[Pilot Jobs]] · [[CMS]] · [[Puppet]] · [[Submission Infrastructure]] · [[Factory Operations]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-15 13.37.47 Submission Infrastructure Weekly Meeting`)
