---
type: meeting
date: 2026-05-08
participants:
  - Alan Malta Rodrigues
  - Marco Mascheroni
  - Andrea Piccinelli
topics:
  - microagent architecture
  - Global Workflow Orchestrator design
  - HTCondor access point terminology
  - workflow vs workload management
  - MCP protocol integration
  - retreat presentation planning
---

# New WM Dev Team Weekly Meeting

## Summary

Alan Malta Rodrigues, Marco Mascheroni, and Andrea Piccinelli reviewed a diagram Alan is preparing for an upcoming retreat presentation, walking through the proposed future system architecture: a web service handling Tier-0 requests and a related service for user/Monte Carlo/data-reprocessing requests, communicating with a [[Global Workflow Orchestrator]] that breaks incoming requests into smaller units of work and coordinates data-management decisions with a [[Data Broker]]. Much of the discussion centered on the "microagent" concept — a per-work-unit component intended to replace a single monolithic orchestrating service — and how it relates to [[HTCondor]] access points and [[glideinWMS]]-managed resources. The group also discussed whether and how to integrate the Model Context Protocol (MCP) into the future system, without reaching a firm conclusion, and briefly discussed retreat logistics before the transcript cuts off mid-sentence.

## Decisions / Conclusions

- The future system's [[Global Workflow Orchestrator]] is intended to be a stateless component with no database of its own (Marco's stated design intent); any state needed about in-progress work can be queried from the scheduler rather than persisted by the orchestrator itself.
- The "microagent" is a per-work-unit entity: there is a one-to-one mapping between a microagent and the work queue unit it handles (a microagent is *created to deal with* a unit, it does not *become* the unit). Each microagent is expected to maintain its own small local database (referred to during the discussion as a "micro DB" / possibly SQLite — the transcript is unclear on the exact term).
- The strict 1:1 relationship between a data chunk and a microagent was explicitly flagged as something the group may not want to lock in as a hard constraint: while likely best for scalability, it introduces per-microagent scheduling and teardown overhead, which could be costly at large scale (e.g. millions of data chunks).
- The [[Global Workflow Orchestrator]] is understood to be the component responsible for deciding when to instantiate, reuse, and schedule microagents.
- Terminology clarification: an "access point" (the new name for what used to informally be called by a HTCondor submit-node identifier) is a host plus the [[HTCondor]] schedd service running on it. A microagent is scheduled to run on an access point, and a single access point can host several microagents (the origin of the "micro" naming). The access point connects to an execution point pool managed by the submission infrastructure and [[glideinWMS]], which matches available pool resources against the materialized grid jobs created by the microagent.
- Regarding MCP: Marco argued that the core system only needs to expose a queryable API (status, REST interface, etc.); an MCP server that queries that API can be a fully separate, standalone component and does not need to be part of the core proposal. Alan argued that MCP-style request handling should be considered a core capability (accepting and understanding MCP-style requests, and exposing extensible "actions" that MCP requests can trigger), while agreeing the actual queries/integrations (e.g. to Elasticsearch, Oracle, or a condor scheduler running microagents) would be implemented by/for the MCP server layer. This was not resolved into a single agreed design.

## Action Items

- [ ] Share the (first) retreat slide deck with the team by Monday morning — Alan Malta Rodrigues
- [ ] Review Alan's retreat slide deck — Andrea Piccinelli

## Discussion

### Future system architecture (diagram walkthrough)

Alan walked through a diagram of the proposed future system, describing (at a level that deliberately left out lower-level details):
- A web service handling Tier-0 requests, and a differently-flavored web service handling user, Monte Carlo simulation, and data-reprocessing requests. Both persist incoming request documents.
- A communication link (communication model not yet decided) between the [[Global Workflow Orchestrator]] and this request-handling layer, used to digest requests, determine their data dependencies, and make data-management decisions together with the [[Data Broker]].
- At this same stage, incoming requests start being broken into more granular units (the granularity size was explicitly left undecided) as part of partitioning the overall workload to enable concurrent execution of the resulting work units.

Marco noted this was presented as a proposal, not a final design, and that open discussion/alternative ideas were welcome. He also raised the meta-question of what the presentation's goal should be: summarizing what was already worked out, versus opening discussion on what to do next.

### The microagent concept

Andrea framed the microagent as a new paradigm relative to existing systems: rather than one global service tracking and monitoring all workflows or work units (which creates fault-tolerance and resilience drawbacks from having a single service track everything), the functionality needed to run a workflow is packaged into a smaller entity that runs wherever needed and oversees only its own specific work unit. In this model, the orchestrator's remaining job is to receive data and take decisions.

Alan and Marco clarified the relationship between microagents and work units: a microagent is created to handle a given work queue unit (described as similar to a JSON document), with a one-to-one mapping between microagent and unit — though Alan suggested this 1:1 relationship might not need to be a hard constraint going forward, given the scheduling/teardown overhead of running many microagents at scale.

Andrea noted that each microagent is expected to have its own local (small/lightweight) database, which is not currently shown in the diagram.

### HTCondor access point and glideinWMS terminology

Alan worked through the terminology with Marco to confirm his understanding: "access point" refers to the host plus the [[HTCondor]] schedd service (not just the service itself), a microagent is scheduled onto an access point, an access point can host multiple microagents, and the access point connects to an execution point pool managed by the submission infrastructure and [[glideinWMS]], which manages available pool resources against grid jobs materialized by microagents.

### Workflow management vs. workload management, and work queue elements

Alan raised a distinction between workflow management and workload management layers that he has become more aware of over roughly the last year, referencing the 2018 review's resource-management layer and past conversations with Doug Tang at Notre Dame. He connected this to the ability to break one workflow into smaller "work queue elements" that can be scheduled across different agents/systems/microagents, describing this as a genuine benefit of the proposed system worth highlighting.

Andrea noted that during the week, Tommaso Bocali reacted positively to the microagent idea and suggested investigating it further; if other experiments give similar feedback, the concept could potentially be explored for [[DIRAC]] as well. Alan suggested that workflow management (as distinct from workload management) could also be an interesting topic to present, at least in the HEP context, noting that different systems may share similar modes of operation and challenges at the workflow layer, and that even without full convergence, sharing common libraries could improve portability between systems. This was raised as a proposal/idea, not agreed as a plan.

### MCP (Model Context Protocol) integration

Andrea raised whether MCP protocols could be integrated into the microagent, in the context of the retreat covering AI-related work. Alan described MCP as a client-server protocol used by agentic AI systems to communicate with external systems — conceptually similar to a REST API — where a system integrates an MCP server exposed on a host/port, and MCP clients can then send it requests. Andrea gave an example use case: AI tools for operators that can read what is happening inside a microagent. Alan elaborated with an example: an operator sends a request for an aggregated summary of a given workflow, and an AI fetches and aggregates logs from data management, job failures, and the workload management system before returning a summary.

Marco questioned whether anything MCP-specific needs to be built at all: if the core system provides APIs to programmatically query status, an MCP server could be a fully separate system that is not part of this proposal. He expressed skepticism about a general push to add AI capabilities ("I know everybody needs to do AI now because it's cool"). Alan responded that MCP-style request handling should be a core capability, since it enables understanding/serving MCP-style requests via an extensible set of triggerable "actions." Marco reiterated a preference for keeping any actual MCP server component separate/standalone, querying the core system's exposed APIs (which could point at Elasticsearch, an Oracle database, or a condor scheduler running microagents) rather than being embedded into the core, but the discussion did not reach a firm conclusion.

### Retreat logistics

Alan mentioned he had not yet received feedback on his first slide deck and planned to share it with the team by Monday morning, expecting feedback over the weekend. He noted he is still working on a second contribution/slide deck and invited Andrea and Marco to help present or discuss that material. Alan confirmed he and Marco are both traveling to the US for the retreat the following week. Andrea began to mention that Friday during the retreat there would be presentations from DIRAC and (the transcript cuts off before the sentence is completed).

## Open Questions

- What communication model will be used between the request-handling web services and the [[Global Workflow Orchestrator]]?
- What granularity size should be used when partitioning incoming requests into smaller work units?
- Should the 1:1 mapping between a data chunk/work unit and a microagent remain a strict design constraint, or should more flexible mappings be allowed to reduce per-microagent overhead at large scale?
- Should MCP-style capability be built into the core system, or should any MCP server remain a fully separate/standalone component that simply queries the core's exposed APIs? No agreement was reached.
- What was the full agenda for Friday's retreat sessions (the transcript cuts off after "presentations from DIRAC and...")?

## Related

[[Global Workflow Orchestrator]] · [[Data Broker]] · [[Work Queue]] · [[HTCondor]] · [[glideinWMS]] · [[Workload Management]] · [[DIRAC]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-08 17.27.10 New WM Dev team weekly meeting`)
