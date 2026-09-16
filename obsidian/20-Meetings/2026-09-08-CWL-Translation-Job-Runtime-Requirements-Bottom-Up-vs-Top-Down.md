---
type: meeting
date: 2026-09-08
participants:
  - Marco Mascheroni
  - Todor
  - Alan Malta Rodrigues
  - Vijay Chakravarty
  - Francesco Brivio
  - Camille Mauceri
topics:
  - CWL (Common Workflow Language) as the target workflow description for Run 4
  - Bottom-up vs top-down approach to CWL design
  - Job runtime requirements (runtime executable, job/particular file, PSet configuration)
  - Todor's prior "CMS Dirac Works" proof of concept
  - Translation adapter between Request Manager / CRAB / Tier0 / MCM and CWL
  - CRAB client-to-server parameter mapping
---

# CWL Translation Approach: Job Runtime Requirements and Bottom-Up vs Top-Down Design

## Summary

Marco Mascheroni called this dedicated meeting (separate from the regular Thursday WM Dev team meeting) to give technical feedback on the CWL (Common Workflow Language) work Alan Malta Rodrigues and Vijay Chakravarty have been doing, since he felt there was not enough time to go into technical depth on Thursdays. Camille Mauceri is doing similar exploratory work for CRAB. Before the main group joined, Marco and Todor had an informal pre-discussion in which Todor argued that Alan and Vijay's work was repeating a top-down proof of concept ("CMS Dirac Works") he had already built and documented in a report roughly six months earlier, and that his findings and the code (uploaded to GitHub) had not been consulted.

In the main meeting, Marco raised his central concern: Alan and Vijay's CWL work appeared to start top-down from what WM Agent already does (the job's sandbox, job package, scheduler inputs), whereas he advocated a bottom-up approach — starting from what a single job atomically needs to run (e.g. for Monte Carlo), and describing that single job's steps explicitly in CWL, rather than treating a whole multi-step workflow as an opaque WM Agent job wrapper invoked from CWL. Alan explained that the CWL work so far had gone through two stages: first, mapping a Request Manager JSON workflow description to a CWL workflow document; second (once Vijay started implementing), experimenting with actually executing a CMS run job through CWL command-line tools, partly by studying how LHCb's system does this. Alan characterized the current stage as building familiarity with CWL rather than converging on a final design.

Todor summarized his own earlier proof of concept, which followed a similar path but was built against (legacy) Dirac rather than DiracX, and did not include a CWL translation layer, since Dirac's own CWL/transformation tooling was immature at the time. His central argument was that there is no reliable one-to-one parameter mapping between two independently designed workflow-management systems (abstraction-layer mismatch), and that forcing such a mapping requires a canonical/translation layer that itself becomes a scalability bottleneck — a path he warned risks re-treading the same problems (e.g. reinventing a WMBS-like bookkeeping system) that CMS's current system already solved. Alan acknowledged Todor's report as useful context but noted two key differences: it targeted Dirac (not DiracX, which has no production transformation system yet) and did not address CWL translation specifically.

The group converged on three pieces of information a CMS job needs at runtime, independent of which workload-management system provides them: (1) the runtime/CMSSW software executable, which is already resolvable via CVMFS; (2) a "job particular" file (currently a pickle) that defines the boundary of data (event/Lumi range) a specific job must process; and (3) the PSet configuration for the job (currently packaged as a pickle for fast unwrapping at runtime — roughly 30 seconds faster than an equivalent JSON export, which Todor said he had discussed previously with a colleague referred to as "Mati"/"Matty"). Alan pushed back on framing this in WMCore-specific terms ("pickle file," "Dublin Core"-style artifacts) and argued for describing the underlying information requirements (events, Lumis, files — a "bag of jobs" model) independent of file format or system.

Discussion also covered the broader translation-adapter architecture: the long-term goal is a single CWL description accepted directly by a future (DiracX-based) server, regardless of whether the request originates from MCM, CRAB, or Tier0, via a pluggable/removable translation adapter, while initially keeping Request Manager and CRAB server largely as-is. Francesco Brivio asked whether one common adapter or separate adapters per client (MCM, CRAB, Tier0) would be needed; Alan leaned toward possibly two separate translation components since the underlying workflow-description formats differ substantially (Request Manager: JSON key/value document; CRAB: a WMCore Python configuration object). For CRAB specifically, Alan noted an existing hard requirement from the CRAB/distributed-analysis requirements document: there must be a long-enough overlap period running both the old and new systems in parallel so users have time to migrate — meaning a CRAB-side translation adapter is considered a must, whereas it is unclear whether Tier0 or a future MCM would need any translation layer at all.

Marco proposed, as a concrete next step, starting from an example Request Manager JSON request (e.g. a StepChain with six steps) and translating it into a CWL document that explicitly reflects each of the six steps, rather than hiding them inside an opaque WM Agent job-wrapper execution. He illustrated this with his own earlier proof of concept, in which a JSON file described per-step job parameters (Lumi section, event range, outputs) fed into a PSet-tweaking tool (an EDM PSet tool provided by the CMSSW core software team), followed by `cmsRun`, previously orchestrated by a bash script that the group agreed should be replaced with a CWL description. In response to a question from Vijay about whether each job needs its own CWL, Marco clarified that a single parameterized CWL document should suffice, with per-job differences expressed as CWL parameters/arguments, not separate CWL files. Marco explicitly rejected one of two directions Vijay proposed (executing the existing WM Agent job wrapper from within CWL, "like WMCore does"); the group agreed to instead describe the job's steps natively and directly in CWL. Alan suggested a concrete achievable next step: expressing, in CWL, the bootstrap of the CMSSW environment on the worker node (`scram` setup) and the PSet-tweaking step (based on Marco's proof of concept), potentially followed by `cmsRun` chaining, stage-out, and logging.

Camille reported she has not yet looked deeply into the CRAB side of this work, given the dependency on the (not-yet-existing) transformation system, but plans to look at how CRAB client parameters map to CRAB server database columns as a baseline for understanding what information is needed for CWL translation. Marco showed a module that performs this client-parameter-to-database-column mapping; Alan asked whether it is an exhaustive mapping, and Marco confirmed the CRAB client raises an error/rejects unknown parameters rather than silently dropping them.

At the end of the meeting, there was a brief, inconclusive discussion about whether to hold the regular WM Dev team meeting the next day (2026-09-09), since Alan and Andrea (both usually involved in running it) would be unavailable; the transcript is unclear about the final outcome of this discussion. It was noted that the regular Thursday meeting slot would not run that week because Thursday is a CERN holiday.

## Decisions / Conclusions

- The group agreed that executing the existing WM Agent job wrapper from inside CWL ("like WMCore does") is not the desired direction; instead, the job's steps should be described natively and directly in CWL, built up from what a single job needs.
- The group converged on three runtime requirements a CMS job needs, independent of the workload-management system: (1) the runtime/CMSSW software executable, already resolvable via CVMFS; (2) a "job particular" file defining the data boundary (event/Lumi range) for that specific job; (3) the PSet configuration for the job. Todor argued that if all three become independently configurable, sandbox transfer and separate upstream bookkeeping become unnecessary.
- For CRAB, an existing hard requirement (from the CRAB/distributed-analysis requirements document) is that the old and new systems must run in parallel for a long enough overlap period so users have time to migrate their workflows — making a CRAB-side translation adapter a must-have. It is not yet clear whether Tier0 or a future MCM would need any translation adapter at all.
- The CRAB client is confirmed to validate configuration parameters against the client-to-server-database mapping and raise an error on unrecognized parameters, rather than silently dropping them.
- A single, parameterized CWL document is expected to suffice per workflow/step-chain type; per-job differences (e.g. event ranges, Lumi sections) should be expressed as CWL parameters/arguments rather than generating a distinct CWL file per job.
- Todor's "CMS Dirac Works" proof of concept was judged relevant background but not directly transferable: it targeted legacy Dirac (not DiracX, which has no production transformation system yet) and did not include a CWL translation layer, unlike the current work.

## Action Items

- [ ] Share the meeting recording and AI-generated summary with the group, particularly Vijay Chakravarty — Marco Mascheroni
- [ ] Follow up privately with Camille Mauceri to share the CRAB job-parameter details discussed during the meeting — Marco Mascheroni
- [ ] Look into how CRAB client parameters map to CRAB server database columns, as a baseline for understanding CRAB-side information needs for CWL translation — Camille Mauceri

## Discussion

### Todor's prior proof of concept and its relevance

- Before the main meeting, Todor told Marco he believed Alan and Vijay's current work repeats what he had already implemented and documented roughly six months earlier in a project called "CMS Dirac Works," including flattened workflows, interfaces to extract data from Request Manager, and a tested workflow mechanism, and that his report on the associated limitations had not been engaged with.
- In the main meeting, Alan noted two critical differences between Todor's prior work and the current effort: (1) Todor's investigation was based on legacy Dirac, not DiracX, and CMS does not yet have a production transformation system in DiracX; (2) Todor's investigation did not include a CWL description/translation step, which is central to the current work.
- Todor maintained that the underlying abstractions (and the runtime constraints on CMS jobs) would not differ meaningfully between Dirac and DiracX, and that the core lesson — no reliable one-to-one parameter mapping is possible between differently-abstracted systems — still applies. He argued that building a canonical/translation layer to bridge the two systems creates a scalability bottleneck and risks re-treading paths (e.g. reinventing WMBS-like bookkeeping) that CMS's current system has already worked through.
- Marco and Alan viewed Todor's report as reinforcing the decision to design the new system rather than copy Dirac's model, while noting that new architectural decisions (via ADRs) will provide an opportunity to address the gaps Todor identified.

### Bottom-up vs top-down framing

- Marco's concern: current CWL work (as he understood it) starts from WM Agent's existing job-level artifacts (sandbox, job package, scheduler inputs) — a top-down approach. He advocated instead starting from the atomic unit of what a single job (e.g. Monte Carlo) needs to run, and reflecting each job step explicitly in the CWL, rather than treating the whole multi-step workflow as a single opaque WM Agent execution.
- Alan clarified the project's history: the original goal (discussed with Vijay) was mapping a Request Manager JSON workflow description to a CWL workflow class; a second, exploratory goal (once Vijay began implementing) was to actually get a CMS run job executing via CWL command-line tools, partly informed by looking at how LHCb does this. Alan described the team as still in a knowledge-building/exploration phase, not converging on a final design.
- Marco proposed concretely starting from a Request Manager request JSON with a multi-step StepChain (e.g. six steps) and producing a CWL document that explicitly reflects each step, so that reading the CWL alone shows that `cmsRun` (and PSet tweaking) is executed multiple times with different parameters.
- Alan agreed the job-level approach is a sound starting point given there is no finalized transformation system yet, and separately observed that the current CWL execution work only handles a single `cmsRun` step, disregarding chaining; he suggested that describing the chaining of multiple steps in CWL would also be valuable, without specifying which should come first.

### Job runtime constraints (the "three things")

- Todor described three components he says must be exposed as configuration in order to run a job without needing a bespoke sandbox and without re-implementing upstream bookkeeping: the runtime/CMSSW executable (already available via CVMFS), the job's PSet configuration (the CMS run job template, currently packaged as a pickle for fast unwrapping — approximately 30 seconds faster at job start than an equivalent JSON export, a tradeoff he said is negligible against multi-hour job runtimes), and the "job particular" file, which defines the specific event/Lumi boundary that job instance must process (as opposed to the full pre-split workflow representation that is otherwise sent with the job sandbox today).
- Alan agreed with the underlying point but pushed to reframe it away from WMCore-specific terminology ("pickle file," Dublin Core-style artifacts) toward the generic information a job needs (events, Lumis, files) at each layer — describing this as effectively a "bag of jobs" model, independent of the specific system providing it.
- Marco separately asked whether Monte Carlo jobs (which do not consume input data) need this same data-distribution/bookkeeping step; Todor was not fully certain of the historical reasoning for Monte Carlo specifically and suggested checking with Alan, though he noted a first task in a task chain starts from generators while subsequent tasks consume the previous task's data tier.
- Marco and Alan agreed there should not be a foreseeable blocker on the DiracX side to providing this minimal per-job payload (events, Lumis, files) directly, since this is viewed as baseline functionality any workload-management system needs, though this was described as "hard to say for sure right now."

### Translation adapter architecture

- Marco reiterated the ultimate long-term goal (previously discussed) of a system where a future server accepts a single CWL description of a workflow originating from MCM, CRAB, Tier0, or any other system, reached incrementally — e.g., initially keeping Request Manager as-is and adding a translation/adapter layer that converts its JSON into CWL.
- Francesco Brivio asked whether three separate adapters (one each for Tier0, CRAB, MCM/Request Manager) or a single adapter querying all three would be needed. Marco suggested a single adapter that queries all three inputs might be feasible, though the underlying translation code implemented in each client could differ (e.g., a client posting CWL instead of the current Request Manager JSON to a future server, replacing today's post to the CRAB/Request Manager REST interface).
- Alan raised an open question about how central production would handle the transition: whether an adapter is needed, and whether both systems (old and new) would need to run in parallel with replication between them, is not yet clear. For CRAB, however, Alan cited an existing hard requirement from the CRAB/distributed-analysis requirements document that a long overlap between old and new systems is mandatory so users have time to migrate — making a CRAB adapter a firm requirement, unlike Tier0, which might end up needing no translation at all, or MCM, which might eventually emit CWL directly.
- Marco floated an alternative option for CRAB: keep the current CRAB client/server as-is (maintained as long as needed) while introducing a new client that submits directly to the new system, letting both coexist since the underlying request content should be equivalent.
- Francesco questioned whether a single common translation library (usable by CRAB, MCM, etc.) or separate, system-specific translators made more sense, noting that if each client (CRAB client, MCM) implements its own translation to CWL internally, a shared common translator may not add value. Alan leaned toward the workflow descriptions being different enough between CRAB (a WMCore Python configuration object) and central production (a JSON key/value document) that two separate translation components might be more appropriate, though he agreed a unified description should be the goal for the target system itself. Marco maintained his opinion that a common description should ultimately be the goal, noting CRAB can be thought of as a simplified case of the same workflow model (a single-step execution vs. WM Agent's multi-step chaining).
- Marco suggested that comparing CRAB's server-side database columns (what the CRAB client configuration object is ultimately persisted as) against the Request Manager JSON structure could be a useful additional angle for identifying shared underlying concepts between CRAB and central production.

### CWL granularity and example templates

- Alan shared a link (in the meeting chat) to a repository of CWL "executor" templates, illustrating the intended granularity for CWL workflows: each executor (e.g. a CMSSW-run executor) ultimately generates a bash script to run on the worker node. Alan said he expects some of these types of templates will remain relevant conceptually in Run 4, though many current implementation details (associated with legacy Dublin Core-based artifacts) are hoped to be eliminated.
- Vijay asked whether each job would need a distinct CWL document; Marco clarified that the differences between jobs (event ranges, Lumi sections, etc.) should be expressed as CWL parameters/arguments to a shared, parameterized CWL document rather than generating a separate CWL per job.
- Marco showed his own earlier proof-of-concept artifacts: a JSON file describing per-step job parameters (Lumi block, event ranges, and outputs) for each step of a multi-step job, fed to an EDM PSet-tweaking tool provided by the CMSSW core software team, and previously orchestrated with a bash `for` loop that the group agreed should be replaced by a CWL description.
- Vijay stated he saw two possible directions for his own next steps: (1) running a job starting from the WM Agent job sandbox (i.e., invoking the existing job wrapper via CWL), or (2) converting the PSet-tweaking logic from Marco's proof of concept into CWL. Marco explicitly said direction (1) is not the desired approach, and that the goal is to start fresh, describing the job's steps natively in CWL.
- Alan suggested, as an achievable next milestone, expressing in CWL the bootstrap of the CMSSW runtime environment on the worker node (`scram` project setup), applying job-specific PSet tweaks (per Marco's proof of concept), and chaining into `cmsRun`, with stage-out and logging strategy as further steps beyond that.

### CRAB-side exploration

- Camille reported limited progress so far on the CRAB side, citing the difficulty of scoping this work without a finalized transformation system, but said she plans to look into how CRAB client configuration parameters are mapped to database columns on the CRAB server, following up on a module Marco showed during the meeting.
- Alan asked whether this client-to-database mapping is exhaustive — i.e., whether any configuration attribute not covered by the mapping would be dropped when persisted to the central database. Marco clarified the CRAB client instead raises an error and rejects unrecognized parameters, rather than silently dropping them.
- Alan suggested this parameter mapping is a good baseline for Camille to correlate CRAB configuration parameters against the Request Manager JSON structure, to identify where the two systems represent similar information under different names.
- Marco reiterated his view that the ultimate goal should be one CWL description usable for both CRAB and central production, while acknowledging the central-production case is more complex due to having multiple steps.

## Open Questions

- What exact form the future translation-adapter architecture will take, and whether one common adapter (querying MCM, CRAB, and Tier0) or separate per-client adapters will be used — not resolved; views differed between Marco (leaning toward a shared/common description) and Alan (leaning toward likely two separate translation components given differing underlying formats).
- Whether central production will need a translation adapter running in parallel with replication between old and new systems, or some other transition mechanism — explicitly described by Alan as unclear.
- Whether Tier0 will need any translation layer at all, and whether a future version of MCM could emit CWL directly — both open, per Alan.
- Whether standard/vanilla CWL is sufficient for CMS's needs (e.g., handling multiple pileup inputs) or whether CMS-specific CWL extensions will be required — Alan stated he did not know and considered this worth investigating.
- Why the current data-distribution/bookkeeping mechanism historically applies to Monte Carlo workflows (which do not consume external input data) — Todor was uncertain and suggested checking with Alan.
- Whether the WM Dev team meeting originally being considered for 2026-09-09 would go ahead, given Alan's and Andrea's unavailability — the transcript does not clearly resolve this.

## Related

[[CMS]] · [[DIRAC]] · [[DIRACX]] · [[CWL]] · [[WMAgent]] · [[WMCore]] · [[CRAB]] · [[CVMFS]] · [[Workload Management]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-08 13.37.38 New WM Dev team weekly meeting`)
