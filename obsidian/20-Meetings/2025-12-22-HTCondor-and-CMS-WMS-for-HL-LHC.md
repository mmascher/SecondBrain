---
type: meeting
date: 2025-12-22
participants:
  - Brian Bockelman
  - Kevin Lannon
  - Andrea Piccinelli
  - Marco Mascheroni
topics:
  - CMS WMS for HL-LHC architecture
  - data-aware matchmaking
  - workflow representation
  - cross-experiment collaboration
---

# HTCondor and CMS WMS for HL-LHC

## Summary

The group explored a proposed [[CMS]] workload-management architecture built around a global work queue, microagents, late-bound data-aware matchmaking, and feedback from the access-point layer. They compared potential overlap with [[DIRAC]], PanDA, [[Rucio]], and DUNE approaches, and identified follow-up design exercises rather than adopting a final architecture.

## Decisions / Conclusions

- No final architecture decision was recorded.
- The current design direction was to keep workflow generation focused on workflow readiness, progress, priority, and low-frequency policy rather than detailed, high-frequency resource targeting.
- The proposed model seeks to defer data-locality resolution until matchmaking time, rather than translating a data requirement into a static site whitelist before jobs enter the pool.
- A Tier 0 feeder was described as feeding a local work queue rather than creating a work-queue element; the transcript notes this understanding was still to be verified.

## Action Items

- [ ] Verify the Tier 0 workflow path with Tier 0 operators — Marco Mascheroni

## Discussion

### Proposed architecture and boundaries

Brian Bockelman described a migration-oriented alternative to replacing everything at once: retain and shrink working logic where possible, while reimplementing only the components that remain specific to CMS. The discussed design comprised a global work queue, a workflow generator, microagents, an access-point/global-pool layer, and a data placement manager (DPM). Replacing CouchDB was explicitly advocated, but no implementation plan was agreed.

The group considered whether a similar exercise should start from [[DIRAC]]. DIRAC was described as having workflow concepts that might eliminate the need for a CMS global work queue, while CMS-specific workflow-generation and data-policy logic could still remain. PanDA was discussed as lacking a workflow system on its own, with ATLAS-specific JEDI and IDDS cited as related layers.

### Data-aware matchmaking and feedback

The proposed DPM would make placement and replication decisions and provide feedback at workflow or work-queue-element granularity. The workflow generator would check whether required data is on disk and apply slow policy choices, but should avoid detailed knowledge of individual resources. The microagent would express workflow input-data requirements to the pool rather than command individual jobs to run at named sites.

Participants discussed using [[HTCondor]] job-set functionality or an equivalent shared attribute so locality can be resolved at matchmaking time. This would allow a change to apply to a group of jobs without editing thousands of materialized jobs and could support policies such as remote reads or removing failing sites. The transcript presents this as a proposal, not an implemented design.

### Workflow chains and adaptive execution

TaskChain and StepChain semantics were discussed. Andrea Piccinelli described the current understanding as one work-queue element for all steps in a StepChain, versus a one-to-one task/work-queue relationship for TaskChain with the agent connecting tasks. The group proposed that a workflow generator or another service could group steps with compatible requirements, and defer that grouping decision later.

They also discussed potential support for partial jobs, adaptive splitting, sample jobs, and feedback that could adjust data location or memory requirements. These were described as unrealized opportunities, not commitments.

### Collaboration and validation exercises

The group saw possible shared layers or interfaces with DUNE and other experiments: Condor/glidein infrastructure, a standard way to update workflow attributes in the access point, [[Common Workflow Language]], and potentially [[Rucio]]. They noted that direct job callbacks in a DUNE-style late-binding approach can make offline operation difficult, which is important for [[HPC]] integration.

Marco Mascheroni proposed tracing a concrete AOD-on-tape to NanoAOD use case through recall, processing, merge, movement, and DBS interactions. Brian Bockelman suggested simulation, AOD reprocessing, and Tier 0 as three cases that would cover much of the relevant space. A broader conversation with DIRAC, PanDA, CMS, DUNE, Rubin, FCC, and workload-management communities was proposed for the new year.

## Open Questions

- Which proposed components can be provided by DIRAC, PanDA, Condor, Rucio, or a shared interface rather than built as CMS-specific services?
- Should locality resolution be implemented in the access-point layer or periodically by microagents querying the DPM?
- What should the exact workflow and work-queue-element representation be for TaskChain and StepChain?
- Can the Tier 0 feeder be handled by the workflow generator without special changes?
- Which shared interfaces or projects have sufficient cross-experiment interest to pursue?

## Related

[[CMS]] · [[HTCondor]] · [[Workload Management]] · [[Work Queue]] · [[Global Workflow Orchestrator]] · [[Data Broker]] · [[Rucio]] · [[DIRAC]] · [[Common Workflow Language]] · [[HPC]]

## Source

meeting_saved_closed_caption.txt (from `2025-12-22 16.03.56 HTCondor and CMS WMS for HL-LHC`)
