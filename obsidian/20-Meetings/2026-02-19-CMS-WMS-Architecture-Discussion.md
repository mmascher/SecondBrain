---
type: meeting
date: 2026-02-19
participants:
  - Brian Bockelman
  - Marco Mascheroni
  - Andrea Piccinelli
topics:
  - CMS WMS architecture
  - microagent prototype
  - Global Work Queue modernisation
  - Dagman alternatives
---

# CMS WMS Architecture Discussion

## Summary

The group refined a proposed incremental architecture for a future [[CMS]] workload-management system. They emphasized demonstrating a microagent proof of concept, retaining conceptual continuity with the [[Global Work Queue]], separating data-progress tracking from job tracking, and comparing a microagent approach with possible Dagman-based alternatives.

## Decisions / Conclusions

- No final architecture decision was recorded.
- The group’s proposed migration strategy is incremental replacement of components, avoiding parallel production systems where possible.
- A microagent proof of concept beginning with merge logic was considered the most useful near-term demonstration.
- The proposed microagent should track work/data completion rather than duplicate batch-system job tracking.
- The Global Work Queue name and API boundary should be retained conceptually even if its implementation is replaced.

## Action Items

- [ ] Continue the microagent proof of concept, starting with merge logic — Marco Mascheroni
- [ ] Update the architecture diagram to distinguish Tier 0 from production/private-analysis instances and add the Global Work Queue — Andrea Piccinelli
- [ ] Invite Dima to the next architecture discussion — Andrea Piccinelli

## Discussion

### Incremental modernisation and proof of concept

Brian Bockelman argued that replacing components one at a time reduces migration risk and avoids operating two workflow systems in parallel. The key architectural change was identified as the microagent; the workflow optimizer was viewed as another microservice rather than a conceptual leap. Marco’s prototype could already submit a simple range of jobs, but merge logic was identified as the first place requiring microagent decisions.

The group discussed relying on scheduler logs for job state and tracking data/work completion instead of creating a second job-tracking database. This was presented as a way to make the CMS layer smaller and simpler while retaining reliability goals.

### Architecture document and system boundaries

Andrea was refining an architecture document and diagram covering use cases, interfaces, and services. The participants wanted the diagram to show a unified system with separate Tier 0 and production/private-analysis instances, rather than the current separation. They also discussed a sufficiently abstract data-management service that could handle more than one use case.

The Global Work Queue was proposed as the stable conceptual boundary. The group discussed hiding database implementation behind its API so that CouchDB could later be replaced by a managed CERN database solution without requiring a whole-system rewrite. This was a design direction, not a selected database technology.

### Alternatives and shared workflow technology

The group discussed Dima’s alternative, more top-down proposal to use Condor itself for workflow management. Brian suggested presenting both directions initially and deciding after a short evaluation period. They identified known Dagman concerns around changing merge topology and process management, and discussed possible variants such as a microagent generating a DAG or an embedded Dagman interface.

[[Common Workflow Language]] was mentioned as a possible workflow description, but Brian cautioned that workflow-language popularity changes over time. No commitment to adopt CWL, Dagman changes, or an alternative was made.

## Open Questions

- Can a minimal microagent demonstrate merge handling and recovery before the March discussion?
- What Dagman changes, if any, would make a Condor-centric alternative viable?
- Which components should remain unchanged for an initial end-to-end demonstration, and which can be replaced later?
- How can the microagent and Dima’s alternative be evaluated with a coherent technical narrative?

## Related

[[CMS]] · [[Workload Management]] · [[Global Work Queue]] · [[HTCondor]] · [[DAGMan]] · [[Microservices]] · [[Common Workflow Language]] · [[CouchDB]]

## Source

meeting_saved_closed_caption.txt (from `2026-02-19 15.07.57 Sala riunioni personale di Andrea Piccinelli`)
