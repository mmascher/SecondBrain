---
type: meeting
date: 2026-09-09
participants:
  - Marco Mascheroni
  - Pablo Izquierdo Gonzalez
  - Jaime Frey
  - Hyunwoo Kim
  - Stephan Lammel
topics:
  - data-aware matchmaking (Rucio distance in HTCondor matchmaking)
  - immortal pilots
  - HTCondor 24 end-of-support and WMAgent compatibility
  - job startup/shutdown overlap and job bundling for CPU efficiency
---

# CMS Submission Infrastructure Meeting — Data-Aware Matchmaking, Immortal Pilots, Condor 24

## Summary

Marco Mascheroni led a discussion with Jaime Frey (HTCondor team), Hyunwoo Kim (Fermilab), Stephan Lammel, and Pablo Izquierdo Gonzalez, covering four topics: (1) refining the data-aware matchmaking idea (continuing from an earlier design discussion, see [[2026-07-08-Data-Aware-Matchmaking-Design-Discussion]]) and brainstorming ClassAd mechanics with Jaime; (2) "immortal pilots" — removing pilot wall-time limits and relying on glideinWMS draining, with Fermilab identified as a candidate site to prototype; (3) HTCondor 24 end-of-support and its impact on WMAgent, which is not yet compatible with Condor 25; and (4) CPU efficiency ideas raised in a separate CMS offline/computing meeting, around overlapping job startup/shutdown and bundling multiple payload jobs into a single HTCondor job.

## Decisions / Conclusions

- No new final decisions on the data-aware matchmaking design were reached; the exact ClassAd mechanism (per-site explicit distance clauses vs. a lookup/dictionary-based approach) remains unresolved. Jaime Frey said HTCondor's current ClassAd language does not have a construct for compactly expressing "iterate over a list and check each value is within a threshold," and this would require new functionality; he will discuss with his team.
- For immortal pilots, the working approach discussed was to not set a wall-time limit in the factory (making pilots effectively immortal from the start) and rely on glideinWMS's existing draining feature for sites to retire pilots, rather than a fixed lifetime. Hyunwoo Kim proposed testing this via a limited test entry in the production Fermilab factory (one pilot, so as not to consume the ITB's limited job pressure) rather than in ITB. Hyunwoo and Marco agreed to have a separate technical follow-up meeting on implementation details.
- HTCondor plans (as stated by Jaime Frey): version 26.0 is expected this month, after which no further releases (including security patches, under normal policy) will be made for the 24.0/24.x series; general end-of-support for 24 was stated as October (Jaime initially said September, then corrected to October). A new security vulnerability announced the day before the meeting is being patched for 24.0/24.x as an exception. Exceptions to extend support past October are possible but not guaranteed, and likelihood depends on factors such as requested duration and effort shown toward migrating; such decisions are made above Jaime's level.
- Agreed division of work on the Condor 24/WMAgent issue: Hyunwoo will first contact Gregor (who ran the earlier WMAgent/Condor 25 compatibility tests) to relay Jaime's suggested workaround (see below) and ask him to test it, aiming to hear back in one to two weeks. Only after that will the group pursue a second, parallel track of requesting a prolonged Condor 24 support window through CMS higher-level management (not a developer-to-developer request), since Stephan Lammel and Marco agreed an official request needs to come from CMS management to HTCondor management, not from Hyunwoo or Marco directly.
- Stephan Lammel's position: rather than requesting an extended-support exception, the underlying WMAgent/Condor 25 compatibility issue should be understood and fixed, since otherwise WMAgent risks being stuck on old Condor releases for years. Stephan proposed documenting the issue and opening a ticket.
- Jaime Frey clarified that WMAgent nodes at Fermilab run HTCondor daemons (schedd, using FS authentication) plus the Python bindings; since daemons are involved (not just bindings), simply continuing to run old bindings against newer daemons is not automatically safe in the way it would be for bindings-only usage, though HTCondor does attempt to preserve over-the-wire compatibility across releases. As a practical workaround, Jaime suggested installing the Condor 24 Python bindings in an isolated user-level environment (e.g., PyPI/Python virtual environment under the user's home directory, not at the system level) so WMAgent can keep using the 24 bindings while the system-level Condor package is upgraded to 25; this is preferable to trying to break the RPM dependency between the Condor and Condor-Python packages, which Jaime said is not possible directly.
- On job startup/shutdown overlap ("overlaying" job wind-down with the next job's wind-up): Jaime noted HTCondor had support for this roughly 15 years ago, but it was rarely used and added complexity to how HTCondor manages job sequencing, so it isn't something to build on directly today.
- Instead, HTCondor's current direction for reducing per-job overhead is bundling multiple payload jobs into a single HTCondor job (e.g., a "quadruple" job packing 4-5 user jobs), so the container/image bootstrap (CVMFS, singularity) cost is paid once per bundle rather than once per job; this was discussed favorably by both Jaime and Stephan, including a potential added benefit of increased shared-memory reuse across bundled jobs' shared libraries.
- Jaime described a related, early-stage HTCondor concept ("late materialization"-style bundling): sending a group of jobs (e.g., 10) from the same cluster to an execute point together so that per-job overhead (starter activation, file transfer, network requests) is amortized across the group, while jobs remain fully independent/separate ClassAd jobs. Jaime was explicit that this is only in early concept phase, not implemented.
- Separately, and further along: HTCondor's planned "Common Input Transfers" feature (targeted for release in HTCondor 26.0) will transfer a tarball that is common across many jobs from the same cluster going to the same execution point only once over the network, then extract it once per job into each job's own scratch directory — while jobs remain fully independent. Jaime confirmed this is actively implemented and planned for 26.0.
- Jaime said HTCondor has no current plans to implement a shared/common scratch area across multiple bundled jobs on the same machine (so a second job could detect and reuse files already unpacked by a first job), though this has been requested by other user groups and HTCondor has been thinking about how such a mechanism might work (e.g., an environment-variable-exposed shared scratch directory, bind-mounted into each job's singularity container).
- Next step agreed for the HTCondor bundling/Common Input Transfers work: Jaime will follow up by email describing what HTCondor currently plans to support, and the CMS side (Marco et al.) will reply describing how useful it would be and what additional behavior would make it more useful, as an iterative written exchange rather than further immediate meeting time.

## Action Items

- [ ] Mull over whether a new ClassAd/HTCondor language feature (e.g., a lookup-based way to express per-site distance requirements more compactly) could be added, and discuss with HTCondor team members — Jaime Frey
- [ ] Contact Gregor to relay Jaime Frey's suggested workaround (isolated Python-bindings environment for Condor 24) for the WMAgent/Condor 25 compatibility issue and ask him to test it; aim to hear back in 1–2 weeks — Hyunwoo Kim
- [ ] Schedule a separate technical meeting with Marco Mascheroni to discuss immortal-pilot implementation details — Hyunwoo Kim
- [ ] Check with Steve(n) (Fermilab team) about why the glideinWMS draining feature was not used as an alternative during a prior episode when Farooq pushed for longer (four-day/one-week) pilot lifetimes — Hyunwoo Kim
- [ ] Check in with Cole Balig (HTCondor's Fermilab ambassador) and the HTCondor team for any existing knowledge about the WMAgent/Condor 25 compatibility errors reported on the regular Fermilab/Condor call — Jaime Frey
- [ ] Send email to Dima Anderson (CompOps Level 2) once more is known, to inform them of the Condor 24 end-of-support situation — Marco Mascheroni (contingent on hearing back from Gregor first, per Hyunwoo's suggested sequencing)
- [ ] Follow up by email describing HTCondor's current/planned support for job bundling and Common Input Transfers (targeted for 26.0); CMS side to reply on usefulness and desired refinements — Jaime Frey

## Discussion

### Data-aware matchmaking (continued)

Marco recapped the concept: jobs currently use data locality (running where the needed data is present), with uncontrolled remote reads via XRootD occurring sometimes; the goal is to make remote reads more controlled. He referenced learning about "Justin" (another workflow management system using glideinWMS and Condor, encountered at the Scientific Workflow Management retreat at Fermilab) which uses [[Rucio]]'s built-in per-RSE "distance" metric — an administrator-assigned, non-commutative number between pairs of storage elements — as the basis for similar matching decisions.

Marco's proposal: run at the local/desired sites first; after a defined wait (e.g., 8 hours), also allow jobs to run at sites within an acceptable Rucio distance of the data. He sketched an example with a "required minimum data distance" ClassAd and per-site distance values a pilot would publish (looked up from a Rucio-derived cache, e.g. hosted via CVMFS), illustrating the requirements expression as a `stringListMember` check against desired sites, OR (after 8 hours) a distance-threshold check. Marco's concern was that expressing this per-site (potentially 100+ clauses for ~50+ RSEs) in ClassAds is unwieldy, and he asked whether HTCondor could support a more compact lookup/dictionary-style construct instead of many explicit per-site clauses.

Jaime Frey said he had been considering whether the current ClassAd language supports this kind of "iterate over a list and check each is within a threshold" pattern in one statement, and concluded it likely does not exist today — it would be new functionality. He said he might be able to design something usable in other similar scenarios too, and needs to discuss with other team members about the best way to do it.

### Immortal pilots

Marco described the idea (attributed in part to a colleague, Luis, who suggested calling it "immortal pilots"): pilots that run beyond the current 48-hour/5-day wall-time limits. No specific implementation was settled; Marco's working idea was to remove the wall-time limit in the factory entirely and rely on glideinWMS's draining feature for sites to retire pilots when needed.

Fermilab was raised as a candidate site to explore this, being a large, whole-node site with fragmentation toward the end of pilot lifetimes; Marco estimated the resulting inefficiency is on the order of 1-2%, but noted it came up in the context of a recent CMS efficiency-focused meeting.

Jaime noted implementation would differ depending on whether the target is a Slurm or Condor cluster: Slurm typically enforces a default max runtime (jobs exceeding it get killed and must restart) unless a longer one is explicitly requested, whereas Condor normally has no notion of a max runtime — a pilot can run indefinitely, subject to the pool's policy, and if interrupted/rescheduled by Condor itself it may simply resume. He cautioned that site administrators might be confused or annoyed by a pilot job that appears to run forever and keeps getting rerun, and recommended a site-by-site conversation with administrators.

Two complications were raised:
- **ID token expiration**: the ID token used by a pilot to authenticate to the central manager might expire over a long-running pilot's lifetime. Jaime explained the token is only needed to (re-)establish a Condor security session — used continuously only if the connection drops or the central manager restarts, at which point the pilot must reconnect using the ID token. He noted a long-standing, unimplemented feature request from the glideinWMS side to let a factory push a refresh token into a queued job's CE sandbox, which could help. Jaime also flagged that queue times can compound this, and that there is a (to-be-confirmed) glideinWMS/CE policy that a pilot job is only allowed to run once — if interrupted and Condor tries to rerun it, the CE may refuse.
- **Defragmentation**: pilot expiration/retirement is currently also used to defragment whole nodes; removing wall-time limits could reduce this defragmentation effect, though Marco was uncertain of the actual impact given the site mostly runs single-core jobs on a whole-node cluster. Jaime confirmed Condor supports *partial* defragmentation (a defragging threshold, e.g. half of CPUs/memory reclaimed, rather than requiring all jobs off a node).

Hyunwoo Kim said he and Marco had already discussed this the previous day, confirmed the approach seems implementable via parameter adjustments, and proposed testing in a **production** Fermilab factory test entry limited to one pilot (rather than ITB, which lacks sufficient job pressure to observe real behavior) to observe what happens when pilots do not retire. He requested a follow-up technical meeting with Marco.

Marco raised whether there's value in a mechanism where the batch-system job itself requests renewal (e.g., relevant for refresh-token-based credential renewal, but not clearly useful for lifetime extension itself). He also recalled that a colleague, Farooq, previously pushed for longer pilot lifetimes (one week, later four days), and that glideinWMS's draining feature was reportedly not a viable option for that case at the time, for reasons Marco could not recall — flagged as something to check with the Fermilab team (Steve, likely to remember, per Hyunwoo).

### HTCondor 24 end-of-support and WMAgent compatibility

Hyunwoo raised that most Fermilab machines have been upgraded to Condor 25, but WMAgent machines have not, because the WMAgent code is not yet compatible with Condor 25 — WMAgent developers have been pushed on this without success so far, and Fermilab's WMAgent nodes will need to remain on Condor 24 for a while.

Jaime confirmed HTCondor's plan: version 26.0 is expected this month (September), after which the project will not make further 24.0/24.x releases under its standard support policy; general end-of-support was stated as October (after initially saying September and then correcting to October). A new security vulnerability disclosed the day before this meeting is being patched for 24.0/24.x as it predates the cutoff; after October, new vulnerabilities discovered would normally not get a 24.x patch, though exceptions are possible for especially severe cases — with likelihood depending on factors outside Jaime's control (decided at a higher level in the HTCondor project, considering requested extension length and effort shown toward resolving the underlying compatibility problem).

The group discussed why WMAgent isn't compatible with Condor 25: WMAgent development is currently in a low-effort "freeze" state, making it hard to find effort to fix Condor-related issues in the agent. No ticket number for the specific error exists yet (confirmed by Hyunwoo); the error was previously mentioned by Hyunwoo/Gregor on a Fermilab/Condor call but not formally documented.

Stephan Lammel argued for fixing the underlying compatibility issue rather than requesting extended Condor 24 support, since the same problem would likely recur with the next Condor version too, risking WMAgent being stuck on old releases indefinitely; he proposed documenting the issue and opening a ticket. Marco agreed and proposed a two-track approach: (1) get more technical detail on the actual error so it can potentially be fixed, with Jaime available to help; (2) separately, since Condor 24 support ends in October/November, ask CMS higher-level management (not Hyunwoo or Marco individually) to make an official developer-to-developer-avoiding request to HTCondor's management for extended support, framed as a bridge (e.g., 3-6 months) while the underlying issue is fixed — not a multi-year extension, and not guaranteed to be granted.

Jaime asked clarifying technical questions: whether the WMAgent Condor 25 issue involves the Python bindings, HTCondor daemons, or both. Marco explained the Fermilab WMAgent machines run HTCondor daemons (schedd) authenticating via FS authentication, and also use the Python bindings. Jaime noted that if it were bindings-only, continuing to use 24.0 bindings against newer daemons would likely be fine, since HTCondor tries to maintain over-the-wire compatibility across release series and vulnerabilities typically affect daemons rather than client bindings — but since daemons are involved too, this is trickier. Hyunwoo asked whether the Condor and Condor-Python RPM dependency could be broken to allow Condor 25 (daemons) with Condor 24 Python bindings; Jaime said this isn't directly possible via the RPM dependency, but suggested installing the Condor 24 bindings in an isolated Python environment (PyPI/virtualenv, user-level rather than system-level) and pointing WMAgent code at that installation instead of the system bindings — Hyunwoo considered this "a good plan" for the interim and will contact Gregor to relay it and ask him to test it.

The group agreed Hyunwoo will first pursue the Gregor/technical-workaround track (aiming for feedback in 1-2 weeks) before initiating the higher-management extended-support request track. This concern was noted as currently specific to Fermilab's WMAgent machines (not yet confirmed as affecting CERN agents similarly). Jaime will separately check with Cole Balig (HTCondor's Fermilab ambassador) and the wider HTCondor team for any existing awareness of this issue from the regular Fermilab/Condor call.

### CPU efficiency: overlapping job phases and job bundling

Marco introduced a topic that had come up in a separate general CMS offline/computing meeting earlier that day: allowing a new job to start (or its execution phase to begin) while the previous job is still finishing its shutdown/stage-out, or overlapping a job's own bootstrapping (unpacking images/grid packs) with useful work.

Stephan Lammel characterized the underlying problem: CPU is not being consumed efficiently during each job's startup and shutdown phases. Startup involves instantiating the singularity container from a CVMFS image (fetching it if the CVMFS cache is empty), extracting the job tarball, and starting CMSSW (loading shared libraries from CVMFS) — this can take about 2 minutes before the first event is processed. Shutdown (writing statistics, tying up output, transferring to local storage) takes roughly 45 seconds to a minute. For a 15-20 minute job, this end-of-job overhead alone is roughly a 15% effect.

The idea discussed at the CMS meeting was to overlay the startup of the next job with the shutdown of the previous one: the job would report to the batch system (global pool / negotiator, clarified by Marco and Jaime as distinct from a site's local batch system) when its startup phase is complete and execution has begun, allowing the slot to be considered available for the next job's startup even before the current job's shutdown finishes. Stephan noted this would need support on the (global pool) batch-system side, and suggested it could also be used for other purposes, e.g., pre-filling the CVMFS cache before executable startup, or having a job pre-fetch its input data (in a "data lake" scenario) into a local cache ahead of time so reads become local rather than remote.

Jaime recalled HTCondor had implemented something along these lines roughly 15 years ago, but it saw little use (despite some demand) and added complexity to how HTCondor manages sequences of jobs — implying it isn't a good basis to build on today.

Jaime's suggested alternative direction, HTCondor's current recommendation for reducing per-job overhead, is **bundling** multiple payload jobs (e.g., 4-5) into a single HTCondor job in the global pool, so per-job overhead (CVMFS/container loading) is paid once per bundle. Stephan responded positively, noting bundling (e.g., a "quadruple" single-core job) could also increase shared-memory reuse of shared libraries across the bundled jobs, and suggested a similar mechanism could support additional job states (e.g., a staging state for tape data, followed by a run/transfer state).

Marco characterized this as effectively moving the responsibility for packing multiple CMSSW executions into a single Condor job envelope up into WMAgent. Discussion then covered two related, distinct HTCondor mechanisms Jaime described:

1. An early-concept idea (not yet implemented) of sending a group of jobs (e.g., 10) from the same cluster together to an execute point so that per-job overhead (starter activation, file transfer, network round-trips to the access point) is amortized across the group, while the jobs remain fully independent/separate. Jaime was explicit this is still only in the early concept phase.
2. **Common Input Transfers** — actively implemented and planned for release in **HTCondor 26.0**: for many jobs of the same cluster going to the same execution point, a tarball common across them is transferred over the network only once, then extracted once per job into each job's own scratch directory. Jobs remain fully independent Condor jobs; only the network transfer is deduplicated.

Marco asked about a related idea of a shared scratch area across bundled jobs on the same machine (e.g., so a second job could detect that a first job already unpacked something and skip redoing it). Jaime said HTCondor has no plans to implement this currently, but it has been requested by other user groups and the team has thought about possible approaches, such as exposing a shared scratch directory via an environment variable, bind-mounted into each job's singularity container. Stephan noted this would likely need an overlay filesystem approach in practice, since unpacking/write operations into a shared area typically need to happen once and then be layered per job; he confirmed CMS already uses singularity everywhere, so bind-mounting would not be an issue technically. In the same exchange, Stephan clarified that the CMS singularity/glideinWMS wrapper currently fetches the user's job tarball from the scheduler for each job; with job bundling (e.g., a "quadruple" job), the tarball would only need to be fetched once and then unwound per sub-job into the shared working area.

Marco asked how CMS should proceed on this line of work; Jaime proposed sending a written summary by email of what HTCondor currently plans to support (bundling / Common Input Transfers), with CMS then replying on how useful it is and what further changes would make it more useful, as an ongoing written exchange rather than requiring further meeting time on this specific topic. Marco agreed this was a good way to proceed.

## Open Questions

- What the exact ClassAd mechanism should be for data-aware matchmaking (explicit per-site clauses vs. a new lookup/dictionary-style HTCondor language construct) — unresolved; Jaime needs to discuss internally.
- Whether removing pilot wall-time limits (immortal pilots) will meaningfully affect whole-node defragmentation at Fermilab in practice — not yet tested.
- Why glideinWMS draining was reportedly not a viable option during the earlier (Farooq-era) push for longer pilot lifetimes — to be checked with the Fermilab team (possibly Steve).
- What the specific technical error is that prevents WMAgent from working with Condor 25 — not yet documented in a ticket; needs further investigation before a fix or a targeted extended-support request can be pursued.
- Whether higher-level CMS management would successfully obtain an extended Condor 24 support window from HTCondor management, and for how long — undetermined; described by both Marco and Jaime as not guaranteed and dependent on factors (effort shown, requested duration) not yet known.
- Whether the WMAgent/Condor 25 compatibility issue also affects the CERN WMAgent machines, not just Fermilab's — not yet examined.
- How useful HTCondor's planned bundling/Common Input Transfers features will be for CMS's actual workflows, and what refinements CMS would want — to be worked out via the proposed follow-up email exchange with Jaime.

## Related

[[2026-07-08-Data-Aware-Matchmaking-Design-Discussion]] · [[HTCondor]] · [[glideinWMS]] · [[Rucio]] · [[Pilot Jobs]] · [[Workload Management]] · [[WMAgent]] · [[CMS]] · [[CVMFS]] · [[XRootD]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-09 18.00.52 CMS Submission Infrastructure meeting`)
