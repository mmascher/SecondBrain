---
type: meeting
date: 2026-06-24
participants:
  - Valentin Y Kuznetsov
  - Marco Mascheroni
topics:
  - DiracX / DIRAC architecture and dependencies
  - DiracX demo and local development experience
  - Integration-testing requirements (need for a dedicated site)
  - Long-term WMS integration plugin idea
  - Upcoming DiracX hackathon
  - Kubernetes deployment experience with DiracX
---

# DiracX Evaluation and WMS Integration Planning

## Summary

Valentin Y Kuznetsov and Marco Mascheroni discussed Valentin's hands-on experience evaluating DiracX/DIRAC ahead of an upcoming hackathon. Valentin explained that DiracX currently does nothing on its own — it is a wrapper that must be configured to point at a running (legacy) DIRAC backend via a central YAML configuration file, and that installing DiracX with tools like Pixi only sets up services, not a working system. He described DiracX's components as far more interdependent in practice ("like a snowball") than the documentation's claim of a "pluggable" architecture suggests, and reported difficulty understanding the system's demo, its errors, and its required Docker-based setup. The two discussed what would be needed for CMS to run real integration tests (a dedicated, DIRAC-compliant site), compared this to CMS's existing GlideinWMS pilot-submission model (direct submission to Condor CE / ARC CE), and discussed Marco's longer-term idea of eventually writing a plugin so that DiracX submits directly to CMS's own systems instead of through DIRAC. Valentin also described his limited-value experience standing up DiracX on Kubernetes, given the lack of full Kubernetes/Helm support and differences from CMS's own Kubernetes environment. The meeting closed with logistics (hackathon recording, September Computing/Offline Week, a DIRAC workshop in Prague) and a private exchange in which Marco shared his personal view that building the DiracX integration will require significantly more effort than the one-month proof-of-concept prototypes he and a colleague ("Dima") had each already built independently.

## Decisions / Conclusions

- DiracX cannot currently function independently: it requires a working legacy DIRAC deployment (databases, job manager, computing-element registration, etc.) and a central configuration file that points to DIRAC's old (non-HTTP) protocol services. Without a DIRAC server in place, DiracX "will do nothing."
- The DIRAC/DiracX configuration file (a custom format in DIRAC, YAML in DiracX) is the central binding mechanism used by every service to locate and communicate with every other service, including authorization/permission levels (e.g., a "job administrator" level in a hierarchical authorization tree).
- Despite DiracX being described by its developers as a pluggable/decoupled system, Valentin's experience is that it is effectively monolithic in practice: standing up even one component (e.g., a transformation service) pulls in Docker, the configuration server, and other dependent services, rather than allowing isolated development/testing (he contrasted this with being able to run just the DiracX DB in isolation for DB-layer development).
- Running the DiracX demo requires Docker/containers; Valentin was able to run it but could not determine what functionality it actually exercises, and observed unexplained job-scheduling errors in it.
- CMS will need its own dedicated site for integration testing: simply asking an existing site (e.g., an Italian site) to accept jobs will not work, because the site must pass authentication and be registered/visible in the DIRAC/DiracX configuration server. This site would need to be DIRAC-compliant (not simply an existing HTCondor/GlideinWMS site).
- Valentin's local Kubernetes setup for DiracX has limited value so far: DiracX/DIRAC does not yet fully embrace Kubernetes (its Helm charts did not work directly as claimed for him), and CMS's own Kubernetes environment differs from what DIRAC participants use.
- There is no written schema for the JSON payloads exchanged between DiracX services (similar in spirit to how WMCore's WMTask/WMWorkflow runtime objects were handled, since Python code just passes dictionaries); without knowing these object structures, developing new components is effectively blocked.

## Action Items

- [ ] Use the hackathon to determine what functionality the local DiracX demo actually supports (e.g., job submission, monitoring, retrieving results) — Marco Mascheroni (per Valentin's suggestion)
- [ ] Share honest feedback/rating on the DiracX system after the hackathon, at least privately if not otherwise — Marco Mascheroni (requested by Valentin)

## Discussion

### DiracX architecture and dependency chain
Valentin walked through how DiracX depends entirely on DIRAC today: DiracX's configuration contains a pointer to a DIRAC configuration file, which in turn tells each service which protocol and host to use for every other service. He showed his own DIRAC configuration (on his VM) as an example, noting DIRAC still uses its old (non-HTTP) protocol. He argued that without a running DIRAC server and its associated sites/computing-elements set up hierarchically, there is no way to test end-to-end communication for a new service (e.g., a GlideinWMS-based service registered in the DIRAC/DiracX system) beyond local unit-style testing.

### Coupling and "pluggable" claims
Valentin said DIRAC/DiracX documentation describes minimal required components for installation, but that using the system for anything real (e.g., submitting a job) reveals a chain of further dependencies (e.g., job metrics requiring metrics storage). He characterized this as a system that claims to be pluggable but in reality has extensive hidden interconnections that make it difficult to work with until that knowledge is acquired. He distinguished this from what he considers a genuinely decoupled service, using the DiracX DB as a counterexample of something that could in principle be run and tested in isolation.

### Demo and development experience
Valentin expressed dislike for the number of abstraction layers involved (Pixi, containers, Docker) compared to running Python directly, drawing an analogy to a video Marco had previously shared of a framework developer (Flask) criticizing similar layering (e.g., SQLAlchemy). He acknowledged the layering is likely necessary for deployment across heterogeneous sites/OS versions, but said it adds significant friction for development. He noted the demo starts Docker and deploys multiple containers requiring many configuration parameters, and that a single missing parameter can break the whole setup. He said things become easier once the system and its configuration are already known, but that starting from scratch is difficult.

### Long-term WMS integration idea
Marco described a longer-term (not immediate) idea: rather than going through DIRAC's job-poller/agent mechanism, develop a plugin so that DiracX submits jobs directly to CMS's own submission system instead of to DIRAC. Valentin agreed this is achievable down the road via DiracX's plugin/configuration mechanism, but noted several open questions would need to be answered first, including how the manager component balances and recognizes new plugins and routes job submission to them.

### Need for a dedicated integration-testing site
Valentin reiterated a point raised in a separate prior meeting: proper integration testing requires a dedicated site that is DIRAC-compliant (registered, authenticated, and visible in the DIRAC/DiracX configuration server) — an arbitrary existing HTCondor/GlideinWMS site cannot simply be pointed at. Marco said this concerns him less, since the logistics are similar to what CMS already does for GlideinWMS site onboarding. Marco described how GlideinWMS currently works for comparison: pilot jobs are submitted directly to computing elements (Condor CE and ARC CE) using their native clients, carrying the input files and instructions needed to set up and run on the worker node and connect back to the server; there is effectively a catalog of known sites. Valentin agreed the logistics are comparable but noted the key open question is what DIRAC does differently at the point where GlideinWMS would use Condor directly.

### Kubernetes experience
Valentin has a personal Kubernetes setup for DIRAC/DiracX but sees limited value in it so far, since DiracX does not yet fully embrace Kubernetes (its Helm charts, despite being advertised as usable, did not work directly for him), and CMS's Kubernetes environment differs from the environment DIRAC participants use. He considers the main complication to be that CMS needs to build its own supporting infrastructure before development can proceed effectively; once infrastructure exists, he expects iterative Python-level development/debugging to become feasible.

### Hackathon logistics
Valentin will not be attending the hackathon in person. Organizers reportedly said sessions will not be recorded; Valentin suggested someone might informally record audio. Marco suggested this may simply be impractical given the room/breakout-group format involving multiple projects beyond CMS, but said a CMS-only small-group session might be recordable.

### Proof-of-concept comparison (shared privately)
In a portion of the conversation Marco flagged as private, he described spending about a month building a "microagents" proof-of-concept of his own (using `request.json` and a roughly 100-line script that runs the appropriate `cmsRun` steps in sequence) as an alternative to going through DIRAC/DiracX. He noted that a colleague ("Dima") had independently built a similar full-workflow prototype in about the same timeframe. Marco's personal view, shared privately with Valentin, was that pursuing the DiracX integration will require substantially more effort (multiple people over roughly a year, in his own rough estimate) than the redundant one-month prototypes already produced independently, and that he is not yet able to judge the DiracX system itself (not having worked on it) but can already judge the level of effort involved. He said the team would nonetheless proceed with what has been asked of them.

### Personal/organizational context
Valentin is currently half-time at Cornell CHESS, working on infrastructure for X-ray beamline experiments, and half-time on CMS spread across multiple projects. He plans to attend the September Computing/Offline Week (profiling week) and separately a DIRAC workshop in Prague, where he is scheduled to give a talk. Marco also plans to attend the Computing/Offline Week.

## Open Questions

- What exact functionality (job submission, monitoring, retrieving results) does the local DiracX demo actually support?
- Does DiracX offer any standalone deployment path that does not require a full configuration server and its dependent databases/services? Valentin's understanding is that it does not, but this remains unconfirmed.
- What does DIRAC/DiracX actually do differently from GlideinWMS at the computing-element submission step (Condor CE / ARC CE)?
- How would a future CMS-developed submission plugin be recognized, balanced against other plugins, and routed to during job submission within DiracX?
- What caused the scheduling errors Valentin observed while running the DiracX demo?

## Related

[[DIRACX]] · [[DIRAC]] · [[glideinWMS]] · [[HTCondor]] · [[Kubernetes]] · [[WMCore]] · [[CMS]] · [[Workload Management]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-06-24 22.29.01 Valentin Y Kuznetsov's Personal Meeting Room`)
