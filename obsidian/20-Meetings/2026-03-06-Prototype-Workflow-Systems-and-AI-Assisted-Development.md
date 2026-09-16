---
type: meeting
date: 2026-03-06
participants:
  - Dmytro Kovalskyi
  - Marco Mascheroni
  - Muhammad Hassan Ahmed
  - Hasan Ozturk
topics:
  - Dima's prototype workflow management system (WMAgent alternative)
  - Marco's microagent prototype
  - Condor/DAGMan design choices for a future CMS WMS
  - AI-assisted development workflows (Claude Code, Cursor, Copilot)
  - CMS common submission-infrastructure strategy (PanDA/DIRAC)
  - WMAgent/WMCore development process and accountability
---

# Prototype Workflow Systems and AI-Assisted Development Discussion

## Summary

This was an informal call, largely a two-way demo and discussion between Dmytro Kovalskyi ("Dima") and Marco Mascheroni, with Muhammad Hassan Ahmed asking clarifying questions throughout and Hasan Ozturk joining later. Dima demonstrated a prototype workflow management system he has been building (with heavy use of Claude Code) as a possible future replacement for WMAgent, walking through its web front end, its round-based adaptive processing model built on HTCondor/DAGMan, and its current limitations (local-pool-only reliability, in-progress global-pool submission, no stage-out policy yet). Marco described his own parallel prototype, the "microagent" approach, which submits all jobs for a work element via a single Condor submission and tracks job state by parsing the Condor log rather than duplicating tracking in a database. The two disagreed on a key design question: Dima wants to work directly with Condor/DAGMan's native (spool-based) recovery and structural information, arguing effort should go into "fixing DAGMan" rather than building workarounds; Marco is wary of DAGMan's in-place rebuild/recovery behavior, citing bad experience with CRAB, and prefers his microagent's log-parsing approach. The group also compared experiences using AI coding assistants (Claude Code vs. Cursor vs. GitHub Copilot/VS Code) and discussed the wider, partly political context of CMS's effort to decide on a common submission-infrastructure strategy (possible convergence with PanDA and/or DIRAC), including who is or isn't accountable for delivering a replacement system, and CompOps' relationship with WMCore development.

## Decisions / Conclusions

- No architecture decision was made. Dima and Marco continue to pursue two different prototypes/approaches in parallel (Dima's Condor/DAGMan-centric system vs. Marco's microagent), and both said they are comfortable with this ("anyone can pick it up... steal pieces you like and build your own system").
- Dima reported he validated his prototype's physics output against centrally-produced samples for the same workflow and found it matched.
- In Dima's system, only the local pool (a large VM he runs) is currently reliable; submission to the global pool is still being debugged.
- Dima's design deliberately avoids using WMCore/WMAgent runtime code for job execution; the executable is CMSSW itself, wrapped by a bash script whose design was informed by looking at what WMAgent and CRAB do, but reimplemented independently.
- Dima's system currently implements three stages/rounds of processing and does not yet implement merging policy, proper stage-out, or registration in Rucio ("Rush", as heard)/DBS — these are described as the next steps before the prototype is "close to production."
- Marco's microagent prototype currently implements request pickup (from Request Manager, filtering StepChain requests with status "acquired"), per-job pset splitting, single-Condor-submit job submission, and a log-parsing monitor that writes job/file tracking information to a small local database for the lifetime of the work element (dropped once information is in DBS/Rucio). Merge logic is not yet implemented, pending a decision on merge policy.
- Both explicitly rely on HTCondor/DAGMan (or plain Condor submission) for job tracking rather than re-implementing job tracking in their own systems.

## Action Items

- [ ] Try installing "OpenClaw" (name as heard, unclear/possibly a different tool) over the weekend to explore AI-agent automation, e.g. for automating repetitive summer-student application emails — Muhammad Hassan Ahmed
- [ ] Share the name of the CMSSW/EDM monitoring tool (called before executing CMSSW) that Dima could plug into his prototype's performance monitoring — Marco Mascheroni

## Discussion

### Dima's prototype workflow management system

Dima walked through a web front end he built to control the system, noting he built it partly because he finds command-line-only operation inconvenient for demoing/explaining. Currently the system only takes requests from Request Manager (ReqMgr), reading the workflow's JSON and its cached pset config from ReqMgr rather than reimplementing that layer, since "it already works." In the future it is intended to also update workflow status back in Request Manager, positioning it as a potential replacement for WMAgent.

Per request, the interface lets Dima choose an execution mode — CMSSW (real, heavy jobs), synthetic (fast, for testing DAGMan and infrastructure), or a simulator (in between) — and a processing fraction (e.g. running 1% of events, so a 5,000-event job processes only 50). Job parameters (events per job, etc.) are pulled automatically from Request Manager unless overridden. A pool can also be specified; currently only the local pool (his own large VM) is reliable, and global-pool submission is still being debugged, partly to avoid the long queuing/priority delays of production/high-priority queues while iterating.

The implementation ("the log with comments and important changes") is roughly 4,000 lines; Dima said the specification/planning material is much larger. The executable submitted to Condor is CMSSW itself; a bash script handles the surrounding logic, which Dima said was designed by looking at what WMAgent and CRAB do, without reusing WMCore runtime code.

### Round-based adaptive processing model

Work is organized into "work units," each defined as a merge block — enough jobs to produce a reasonable merged output. Processing proceeds in rounds: round 0 starts with a single work unit at the highest possible priority, acting as a pilot/tuning run to measure performance (CPU efficiency, memory usage) as quickly as possible. After each round, the system adjusts parameters for the next round — e.g. the number of work units per round (10 by default, but adaptively reduced, e.g. to 7, to target a specific merged output size such as 3-4 GB), memory requested per job (observed changing across rounds, e.g. from 9 GB to 5.6 GB and then adjusting upward again), and grouping of jobs to balance output size, while trying to keep CPU efficiency stable. Each round must complete before the next starts, and workflow priority can also be adjusted between rounds.

The DAG structure per round includes a landing job (decides which site to run on), parallel processing jobs, and a final merge job. In the demoed run, each round had roughly 101 nodes. Dima said the system aims to stabilize (parameters converge) after a few rounds and noted it should be able to run a very large workflow either as one dataset produced at 100% or as many datasets produced in parallel at partial completion (e.g. 100 datasets at 10% each) — a mode he said matches what physics users want.

Muhammad Hassan Ahmed asked whether jobs are pre-created and held (as in the current WMAgent, which creates thousands of job records in the agent and holds them until submission); Dima said no — there is no such persistent job store, and the number of concurrently active DAGs on a scheduler is capped (currently designed for a single schedd, as a prototype) to avoid overloading the scheduler. He confirmed this cap could scale with multiple schedulers.

On reboot resilience: the DAG itself persists on disk (nothing is lost structurally), but jobs that were running at the time of a reboot are lost and must be resubmitted/retried by the recovery logic.

### Recovery, retries, and stage-out

Dima described a post-job step (still running on the schedd) responsible for most recovery: it analyzes internal error codes (from the post job's own analysis, not raw CMS run/system error codes) to decide whether to retry or give up, and only escalates to workflow management when failures span multiple sites or are massive. He said plain Condor job retries alone "make no sense" without this kind of logic layered on top, though Condor's ability to target a different site/machine on retry (via job requirements, as Marco pointed out) is something he relies on.

Stage-out is not yet finalized; output is currently being copied to what Dima described as his private/user area (he said he was not sure of the exact destination). Marco suggested following the "store temp" pattern used by CRAB/WMAgent (writing to a site's LFN-based temp area at the site where the job runs) rather than a personal user area; Dima agreed this was a good idea, noting he thought he was putting it under his own user area rather than a temp area.

### Design disagreement: Condor/DAGMan spool access vs. microagent log parsing

Marco questioned why Dima's system needs to access the Condor spool directory directly. Dima explained that to get full per-step performance information (memory usage, etc.) for adaptive tuning, he needs structured data — effectively JSON-like dictionaries — which ClassAds alone don't provide well ("just class ads are not good enough... it's a weird thing"). He said this requirement is much easier to satisfy running directly on the schedd machine than remotely, since remote access is limited to what can be submitted/retrieved via the submit interface; he avoided running directly on a production submit host mainly due to security concerns, calling his current approach "the hard way."

Dima's fundamental design choice is to let DAGMan rebuild the DAG/recovery information in place. Marco said he is "not a fan" of that approach, citing bad past experience with CRAB's similar in-place DAG rebuilding, and described his own alternative, which he called the "microagent": a process running on the scheduler that performs its own splitting, submits all jobs for a work element via a single Condor submission (enabling `condor watch queue` to show the whole submission at once), and is monitored by a separate process that parses the Condor log file to populate a small local database tracking job/file state. Marco emphasized that job tracking itself is still done entirely by Condor — his database exists only to track files/recovery state for the lifetime of the work element, and is dropped once the relevant information is registered in DBS/Rucio.

Dima pushed back, arguing "why don't we fix DAGMan" instead of building workaround layers, saying that is where effort should go if the team has to deal with something. Marco cited additional DAGMan limitations he dislikes, e.g. that a single JDL submission (which Condor already supports and which allows scaling submission with late materialization) is not available in the same way through DAGMan. Dima reiterated he specifically wants a design centered on work groups (produced by merging) and rounds, allowing either single-dataset or many-parallel-dataset (e.g. 100 datasets at 10% each) production, and said he doesn't want to "release and forget" jobs.

Marco separately walked through his microagent prototype on screen: it pulls acquired StepChain requests from Request Manager, retrieves psets from the ReqMgr config cache, and submits a microagent process per work element that performs splitting (producing per-job, per-step input and pset modifications) and a single Condor submission for the whole work element. A separate monitoring process parses the Condor log file (tracking job submission/termination events) into a small database that exists only for the lifetime of the work element, since once the work element finishes, all relevant information is already in DBS and Rucio. Marco said he has not yet implemented merging because he has not settled on a merge policy — he considered a WMAgent-like approach of triggering a merge job once a site/tier's unmerged output reaches a size threshold (e.g. 20 GB), but had also heard that ATLAS instead moves small files to a merge destination and merges them there, and did not want to pick an arbitrary policy.

Muhammad Hassan Ahmed noted that this database-based scaling approach (Dima relying on reading information from the Condor spool) might not scale well at high job counts (e.g. 50,000 jobs in a pool). Dima responded that how much information is actually needed from the spool is an open question, and that DAGMan's post-job layer already absorbs most recovery decisions without him needing to query much.

### Site targeting during testing

Both Dima and Marco said they currently target a specific site during testing (rather than submitting broadly or via production/high-priority queues) to avoid long queuing delays and to make it easier to debug stage-out issues without having to check output at many sites (Dima mentioned not wanting to have to check output at Nebraska, for example). Marco noted he instead targets all sites in his own testing and said this approach works for him.

### AI-assisted development workflow comparison

Dima described his workflow with Claude Code as spec/planning-driven: he maintains planning documents (saved in the GitHub repository, distinct from the "official" specification documents that drive constraints) that describe current priorities and tasks, reserves a section of the planning document that only he edits and that Claude never touches, and manages Claude "exactly as I manage people... students and postdocs" — assigning tasks, specifying what needs to be done, and checking in on progress rather than closely directing each step. He said he is spending a large amount of time on writing specs, and that pushing more work into upfront planning lets Claude do "bigger chunks of stuff on its own without doing stupid things." He described the tool as still "fairly stupid" in places and prone to occasional mistakes, especially when instructions are insufficiently clarified, but said it is "way better than I can do myself."

Marco described his own experience using Cursor (with the Composer 1.5 model) as more directive — telling it what to do, then checking and running the result — and said he felt this might be the wrong tool or model for the kind of higher-level, spec-driven workflow Dima described; he said he would try Claude Code (the CLI) after seeing Dima's demo. Marco also said he loses track of specification/planning markdown files in Cursor in a way that doesn't happen for Dima.

Hasan Ozturk described obtaining GitHub (Copilot) Pro for free via a student/CERN-account application (approved after about two days), which through Copilot in VS Code gives access to the same underlying models available via Claude/ChatGPT (e.g. Claude Opus and Sonnet), and said the VS Code Copilot interface felt similar to Cursor's. Dima and Muhammad Hassan Ahmed noted that the surrounding tool/orchestration layer (how the assistant manages context, memory, and multi-step work) differs meaningfully between Copilot and tools like Cursor, Claude Code, or Codex, and that VS Code now also supports running Claude Code or Codex agents within the same interface, allowing easy switching between them (e.g. when running out of tokens on one). Marco said this "orchestration" idea (keeping consistent context/memory of prior inputs across a session) is the part he feels he is currently missing in his own workflow.

Dima separately mentioned that he is currently using Claude to fix a bug in WMS monitoring ("blade in WMS monitoring", as heard — exact meaning/term unclear).

Hasan Ozturk raised wanting to try installing an AI-agent tool referred to as "OpenClaw" (name as heard; the exact tool is unclear from the transcript) to automate a repetitive task — replying to a high volume of summer-student application emails with a standard task/response — but said he had not found the time and was hesitant to give an AI agent access to his CERN email account for security reasons. Dima cautioned that such agents need careful control over what information/access they are given, and suggested using an isolated account plus external monitoring/tunneling scripts as a safeguard against unwanted actions. Muhammad Hassan Ahmed said he would try installing it over the weekend. The topic was raised as a possible demo/topic for the upcoming workshop if someone gets it working. Dima and Marco both said the upcoming workshop is intended in part to let the team share experience on how each of them is using these AI tools so others can learn and start using them (Marco confirmed he will be at CERN the following week).

### CMS common submission-infrastructure strategy and organizational context

Marco and Dima discussed the broader, ongoing effort (outside this specific prototype work) around whether CMS should adopt a shared/community workload-management solution with other experiments, rather than continuing to maintain its own stack. Marco said the stated driver is that USCMS does not want to be the only experiment maintaining this kind of system, and wants to build something usable by or shared with other communities; he said there is a document prepared by Kenji outlining three possible strategies, and that he has been pushing for the "cleanest" of the three, though the counterargument raised by others is that the cleanest strategy requires development effort CMS does not have.

Marco summarized PandA's architecture at a high level, as he understands it: a component analogous to McM, a task-management layer called JEDI (which Marco compared to WorkQueue/Request Manager), jobs stored in a large Oracle database, a PanDA Server that decides what to schedule, and a Harvester component that sends PanDA pilots to queues, with PanDA pilots then talking back to the PanDA Server to get jobs — which Marco said is architecturally similar to CMS's current model. He said one idea being floated is to run PanDA pilots inside glideinWMS pilots submitted via HTCondor (i.e., stacking PanDA, glideinWMS, and Condor), which he characterized as a potential architectural "nightmare," and which he has used as an argument for choosing a cleaner strategy from Kenji's document.

Marco also noted that Valentin reportedly spent about three to four weeks trying to install DIRAC and could not get it running, let alone operating it, which Marco offered as evidence for how difficult the DIRAC path can be in practice.

Marco shared, asking the others to keep it private, his understanding of individual positions: Alan Todd (heard as "Alan Todor"), Andrea, and Kenji are described as favoring the common/shared solution; Valentin is described as sharing Marco's skepticism that this leads to unnecessary complexity if not carefully managed; Duong (connected to the call) was described as caring more about having a sustainable, changeable development framework than about which specific external system is chosen.

Dima was skeptical of the "we don't have development effort" argument, pointing to AI-assisted development as changing what's realistically achievable, and questioned who is actually accountable for delivering a replacement system: he noted Andrea does not have a permanent position and will likely eventually leave, and that Kevin (described as CMS's relevant senior figure, currently a department chair and very busy) has delegated related work to Alan but has not, to Dima's knowledge, publicly committed to delivering anything. Dima said he does not know who is "driving" the community-solution push or why, and that he is not closely engaged with the relevant US-based politics because he is based at CERN.

Both agreed the current situation gives CompOps more freedom to make changes than in the past (partly attributed to the ongoing code freeze), contrasted with a past example where a relatively small change proposed by Antonio (related to CVMFS fallback for a list of CMSSW releases) reportedly took about two months to get through review under the previous dynamic. Dima cited Unified (built historically by Jean-Roch, referred to as "Jean Rock") as a precedent for this kind of "layer on top of something that isn't doing great" approach, noting Jean-Roch had tried to get changes into WMCore directly, found it not worth the effort, and built Unified instead — which Dima said remains core to CMS computing operations today, despite never having had its underlying approach formally adopted.

Dima argued that if the goal of any new development effort is simply to "keep people" employed, that is the wrong basis for defining a project; he suggested there is plenty of genuinely hard work needed elsewhere that current AI tools cannot easily do, citing CMSSW algorithmic optimization as an example (referencing Andrea Bocci's point that CMS is roughly a factor of 10 away from the compute budget needed for HLT in Run 4) as work requiring developers who understand the underlying algorithms, which he said AI-based coding tools cannot substitute for.

Muhammad Hassan Ahmed and Hasan Ozturk both commented on their own past experience with the current system: Hasan Ozturk described his past time on it as personally difficult ("traumatic"), both due to the codebase and to dealing with people, and said he does not want to spend more time on it. Muhammad Hassan Ahmed agreed getting consensus among people was harder than dealing with the code itself, and said things have become somewhat easier since the code freeze, since issues can now at least be fixed directly rather than living with them for months.

## Open Questions

- How should adaptive-tuning performance data best be extracted from Condor/DAGMan (spool access vs. some other structured mechanism), especially if remote/non-local submission needs to be supported?
- What merge policy should Marco's microagent adopt (size-threshold trigger vs. an ATLAS-style small-file consolidation approach)?
- How will Dima's prototype's stage-out and registration in Rucio/DBS be implemented, and when will global-pool submission be reliable enough to move past the local pool?
- Will the disagreement between "fix DAGMan directly" (Dima) and a microagent/log-parsing approach (Marco) be resolved, or will both approaches continue to be developed in parallel?
- Who, organizationally, is accountable for delivering a CMS workload-management replacement, and under what strategy (of the three in Kenji's document) will CMS proceed regarding PanDA/DIRAC convergence?
- Will anyone get an "OpenClaw"-style AI agent working in time to demo at the upcoming workshop?

## Related

[[CMS]] · [[WMAgent]] · [[WMCore]] · [[HTCondor]] · [[DAGMan]] · [[CRAB]] · [[DIRAC]] · [[Rucio]] · [[Workload Management]] · [[Submission Infrastructure]] · [[Pilot Jobs]] · [[glideinWMS]] · [[CERN]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-06 17.18.35 Dmytro Kovalskyi's Personal Meeting Room`)
