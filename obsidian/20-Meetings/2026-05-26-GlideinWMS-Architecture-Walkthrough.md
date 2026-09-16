---
type: meeting
date: 2026-05-26
participants:
  - Marco Mascheroni
  - Luis Simas
topics:
  - GlideinWMS two-stage matchmaking (Frontend-to-entry and Condor negotiator-to-pilot)
  - start expression (pilot resource envelope and site/GPU requirements)
  - glidein token-based authentication and token issuance (IAM)
  - proposal to use Vault for refresh-token storage
  - glidein startup script internals (script/binary downloads, node validation, postmortem, cleanup)
  - glidein work directory / temporary directory logic
  - HTTP-based script distribution and Squid caching
  - comparison of CMS Frontier/Oracle conditions data vs LHCB's CVMFS-based approach
  - ATLAS reportedly moving some caching from Squid to Varnish
  - Factory Ops meeting hand-off
---

# GlideinWMS Architecture Walkthrough: Matchmaking, Token Authentication, and Glidein Startup Script

## Summary

This session was a training/walkthrough meeting in which Marco went through GlideinWMS architecture slides with Luis, apparently as part of an ongoing onboarding series (the group noted the slide deck had 34 slides and expected to finish the remaining material "tomorrow probably or Thursday"). No operational status items (factory tickets, GPU status, monitoring, etc.) were covered in this session.

Marco explained that GlideinWMS involves two distinct matchmaking steps. The first happens in the Frontend, matching idle user jobs against the static entries defined in the factory's XML configuration (which the Frontend reads via Condor ClassAds/`condor_status`); combined with the live count of running pilots, Frontend logic determines how many additional pilots to request. Marco noted that in practice the details of this algorithm rarely matter because the team normally has "infinite pressure" — enough demand to always want to fill all sites — with GPU jobs as an exception, since GPU pilots are only requested when GPU jobs are actually queued. The second matchmaking happens later, inside the Condor negotiator, once a pilot has traveled through the factory, the CE, and the site batch system and started on a worker node: this determines whether any queued job actually matches that specific live pilot. Luis confirmed there is no guarantee that the job which triggered a pilot request will end up matching that pilot — the two are independent — and Marco noted the Frontend performs correction over time (e.g., withdrawing idle pilot requests if pressure disappears, to avoid starting pilots that would sit idle and eventually starve).

The "start expression" was discussed as the mechanism controlling the second (negotiator-level) matchmaking: it is a Condor requirements expression, configurable per Frontend group, that defines the pilot's resource "envelope" (e.g., 8 cores, 16 GB RAM, running for up to two days) against which individual user jobs (e.g., a single-core job requesting 2 GB RAM and 8 hours) are matched. It also encodes other requirements such as desired site and whether a GPU is needed.

On authentication, Luis asked how the glidein proxy/token — which is owned by the Frontend and simply passed through and used by the factory to authenticate to the CE — stays valid and who issues it. Marco explained the token is issued by an IAM-like service (referred to in the transcript as "AIM"), an instance run at CERN by CERN IT, with the underlying software originally developed by an Italian high-energy-physics institution (Marco referred to it as "INFM," which appears to be a mis-transcription — the intended institution was not confirmed in the transcript). The Frontend uses a registered client to obtain a token with the correct capabilities and refreshes it against the same service; currently this works by curling the token and storing it in a local file. Marco raised that there has been ongoing discussion (not yet acted upon) about moving to Vault, storing a Vault access token in the Frontend instead of the powerful long-lived credential itself, so that the underlying credential lives only in Vault — a more security-conscious pattern he has seen elsewhere. Luis asked whether this would extend to the factory too (since the factory also holds the token), suggesting Vault could let the factory only read tokens rather than hold them. Marco replied this was intended only for the Frontend, since the factory is deliberately "agnostic"/a "dumb client" — it doesn't know about VOs or requesters, it just receives a token and submits — and giving it direct Vault interaction would go against that model, though he noted "in principle" things could change in the future (jokingly floating a full rewrite of GlideinWMS, even "in Go," given how cheap writing code has become with AI agents).

The group then walked through the glidein startup script: `glidein_startup.sh` is the only script pushed directly to the worker node; everything else is downloaded from the factory and the Frontend at runtime, with different scripts fetched depending on VO (e.g., CMS pilot vs. generic glidein) plus common factory-ops parameters. Condor binaries are also downloaded (rather than relying on a site-admin-installed version) so the team controls exactly which Condor version runs. This is followed by node validation, writing a `condor_config` file, running the pilot (which can run for up to two days processing user jobs), collecting postmortem information (also done on failure), and final cleanup. Luis clarified that while Condor itself handles the actual shipping of stdout/stderr logs, collecting/interpreting that "postmortem" information (start/end of jobs, whether execution went as expected) is done by glidein scripts, and is written at the end even for successful pilots.

Discussion of the pilot's working/temporary directory (`GLIDEIN_WORK_DIR` or similar entry setting) clarified that despite the slides describing the pilot as creating a temp directory in the current working directory (CWD), the actual location depends on entry configuration and can instead be `$condor_scratchdir`, `$OSG_WORKER_NODE_TMP`, or `$TMP` (an "auto" option exists but is not used). Marco confirmed `$condor_scratchdir` is a Condor/CE- or batch-system-specific variable, more likely available for an HTCondor-CE or HTCondor batch system than for an ARC-CE running Slurm, though he was not fully certain which layer (CE vs. batch system) it comes from. Luis confirmed from experience that only these two variants (`condor_scratchdir` and `TMP`-like variables) are commonly seen in practice. Within this work directory, a unique per-glidein subdirectory (`glidein_<unique ID>`) is created; the parent variable's value (e.g., `condor_scratchdir`) is shared across all glideins/pilots running under the same StartD on a worker node — Luis had initially assumed this value was per-pilot and was corrected.

On file distribution, Marco noted files are downloaded via HTTP (this was previously seen to matter when the Frontend machine was removed from LANDB), and that a Squid cache can optionally be used for this traffic, though GlideinWMS itself is low-volume and squids are not typically configured for it. This led to a broader comparison with CMS's use of Frontier/Squid for conditions/calibration data (configured via `siteconf.xml` in CVMFS) versus LHCB, which — per Marco's understanding — does not run a Frontier-equivalent conditions database at all and instead publishes calibration data directly into CVMFS, reusing the same underlying Squid caching technology. Luis noted an operational point: CVMFS Stratum backends are not his responsibility, but the Frontier backend is, so pushing more traffic onto CVMFS would not directly affect his workload. Marco speculated (without a confirmed answer) about the relative advantages of CMS's Oracle/Frontier approach (possibly offering more structure/history) versus LHCB's simpler CVMFS-only approach (no separate backend service to maintain), noting CMS has a large body of legacy CMSSW code tied to Frontier access, and that he did not know who actually writes the calibration data into the Frontier/Oracle database (guessing it may involve Tier-0 or HLT/P5-level calibration jobs, and suggesting Antonio Linares or Antonio Perez-Calero Yzquierdo might know more). Neither the size of the Oracle database nor the reason for the architectural difference was established; this was an open, informal comparison rather than a firm conclusion. As an aside, Luis mentioned — without being certain — that ATLAS is reportedly moving away from Squid to Varnish for some (non-CVMFS) caching use cases, while continuing to use Squid for CVMFS itself; Marco speculated this might relate to LHCB/ATLAS/CMS differences in calibration-data volume or complexity, but treated this as unconfirmed guesswork. The group also briefly noted experiment size differences (ATLAS and CMS being larger, general-purpose detectors; LHCb and ALICE being smaller/more specialized) as unverified general background.

The meeting ended early because Marco had another meeting at 16:00. Luis agreed to attend the Factory Ops meeting in Marco's place and report that Marco could not join; Marco said he would separately let Jeff know directly, noting he did not believe he had much to report for factory ops that day.

## Decisions / Conclusions

- No formal decisions were made in this session; it was primarily an explanatory/training walkthrough of existing GlideinWMS architecture rather than a discussion of open operational issues.
- Clarified (not new information, but confirmed during discussion): there is no guarantee that the job which triggers a pilot request will be the one matched to that pilot, since Frontend-to-entry matchmaking and Condor negotiator-to-pilot matchmaking are independent steps.
- Clarified: the `$condor_scratchdir`-style work-directory variable has the same value across all glideins running under the same StartD on a given worker node; a unique per-glidein subdirectory is created within it.

## Action Items

- [ ] Attend the Factory Ops meeting and report on the architecture discussion in Marco's place — Luis Simas
- [ ] Let Jeff know directly that he could not attend the Factory Ops meeting — Marco Mascheroni

## Discussion

### Two-stage matchmaking
The Frontend performs a first matchmaking between idle user jobs and static factory entries (read via Condor ClassAds), combined with live pilot counts, to decide how many pilots to request; this rarely needs close attention because demand normally exceeds capacity ("infinite pressure"), except for GPU jobs, which only trigger GPU pilot requests when GPU jobs are actually queued. A second matchmaking occurs later in the Condor negotiator, once a pilot is running on a worker node, to match queued jobs against that specific live pilot. The two matchmaking steps are independent, so a job that triggered a pilot request has no guarantee of running on that pilot; the Frontend corrects for changing pressure by withdrawing idle pilot requests when appropriate to avoid starting pilots that would starve.

### Start expression
The start expression is a Condor requirements expression, set in the Frontend configuration, that defines a pilot's resource envelope (CPU count, memory, walltime) and other requirements (desired site, GPU need). It is propagated from the Frontend down to the entry (the "study"/StartD) as a requirement, and individual user jobs are matched against it as long as they fit within the pilot's envelope.

### Token authentication
The glidein proxy/token is owned and issued to the Frontend; the factory only receives and uses it to authenticate against the CE, without direct involvement in its issuance. Tokens are issued by an IAM-like service (transcribed as "AIM") run at CERN by CERN IT; Marco described the underlying software as originally developed by an Italian HEP institution (transcribed as "INFM" — not confirmed). The Frontend uses a registered client to obtain and refresh tokens; currently the token is curled and stored in a local file. Marco raised a longstanding, undecided idea of moving to Vault, so the Frontend would hold only a Vault access token rather than the more powerful credential directly. Luis suggested this could extend to the factory (read-only token access via Vault), but Marco noted this would conflict with the factory's intentionally "agnostic"/dumb-client design, which has no awareness of VOs or requesters — though he acknowledged this could change in the future.

### Glidein startup script
Only `glidein_startup.sh` is pushed to the worker node; all other scripts and Condor binaries are downloaded at runtime from the factory and Frontend (varying by VO, e.g. CMS pilot vs. generic glidein, plus common factory-ops parameters). Condor binaries are downloaded rather than relying on site-installed versions to guarantee a known/controlled version. The flow then proceeds through node validation, writing `condor_config`, running the pilot (up to two days, executing user jobs), collecting postmortem information (including on failure), and cleanup. Postmortem information (start/end of each job, execution outcome) is collected and written by glidein scripts even for successful pilots, distinct from Condor's own stdout/stderr log shipping.

### Work directory / temporary directory logic
Despite slide material describing the glidein as creating its temp directory in CWD, the actual location is configurable per entry and can be `$condor_scratchdir`, `$OSG_WORKER_NODE_TMP`, or `$TMP` (an unused "auto" option also exists). `$condor_scratchdir` is Condor/CE-specific and more likely relevant to an HTCondor-CE or HTCondor batch system than an ARC-CE on Slurm, though the exact layer (CE vs. batch system) that defines it was not fully certain to Marco. In practice, Luis has only seen `condor_scratchdir` and `TMP`-style variables used. The value of this variable is shared across all glideins under the same StartD on a worker node; a unique per-glidein subdirectory (`glidein_<unique ID>`) is created within it.

### File distribution and Squid caching
Scripts are downloaded via HTTP; this became relevant previously when the Frontend machine was removed from LANDB. A Squid cache can optionally be used for glidein file downloads, but this traffic is low-volume and squids are typically not configured for it in practice.

### CMS Frontier/CVMFS vs. LHCB conditions-data architecture
CMS conditions/calibration data is served to jobs via Frontier and Squid caches (configured through `siteconf.xml` in CVMFS), whereas LHCB reportedly has no Frontier-equivalent conditions database and instead publishes calibration data directly into CVMFS, reusing the same Squid-based caching technology. Luis is responsible for the Frontier backend but not the CVMFS Stratum backends. Marco speculated about tradeoffs (CMS's Oracle/Frontier approach possibly offering richer structure/history vs. LHCB's simpler single-backend approach) but did not reach a conclusion, and noted CMS has substantial legacy CMSSW code tied to Frontier access that would need rework to switch approaches. Who writes calibration data into the Frontier/Oracle database was not established; Marco guessed it may involve Tier-0 or HLT/P5-level calibration jobs and suggested Antonio Linares or Antonio Perez-Calero Yzquierdo might know more.

### ATLAS caching direction (unconfirmed)
Luis mentioned, without certainty, that ATLAS is reportedly moving some (non-CVMFS) caching from Squid to Varnish while continuing to use Squid for CVMFS. Neither participant was certain of the reasons; Marco speculated this could relate to differences in calibration-data volume/complexity between experiments.

### Factory Ops meeting hand-off
Marco needed to leave for another meeting at 16:00 and would not attend the Factory Ops meeting. Luis agreed to attend and report on the architecture discussion; Marco said he would separately inform Jeff directly, noting he likely did not have much to report for factory ops.

## Open Questions

- What is the correct/confirmed name of the token-issuing service and its developing institution (transcribed unclearly as "AIM" and "INFM")?
- Should the Frontend (and potentially the factory) move to storing credentials via Vault rather than a locally curled token file, and if so, how would this interact with the factory's agnostic/dumb-client design?
- Which layer (CE vs. remote batch system) actually defines `$condor_scratchdir`, and is it truly absent for ARC-CE/Slurm sites?
- Who writes calibration/conditions data into the CMS Frontier/Oracle database, and how large is that database?
- Why do CMS/ATLAS use a Frontier+Oracle-backed conditions system while LHCB reportedly stores calibration data directly in CVMFS — is this driven by data volume, structural complexity, or historical/staffing reasons?
- Is ATLAS actually moving from Squid to Varnish for some caching use cases (excluding CVMFS), and why?

## Related

[[glideinWMS]] · [[HTCondor]] · [[Submission Infrastructure]] · [[CMS]] · [[GPU]] · [[CVMFS]] · [[Frontier]] · [[Factory Operations]] · [[Factory Configuration]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-26 15.31.44 Submission Infrastructure Weekly Meeting`)
