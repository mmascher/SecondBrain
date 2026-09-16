---
type: meeting
date: 2026-04-21
participants:
  - Alan Malta Rodrigues
  - Andrea Piccinelli
  - Marco Mascheroni
  - Kenyi Hurtado Anampa
topics:
  - DIRAC/glideinWMS integration strategies
  - DIRAC transformation system architecture
  - workflow task agent
  - microagent comparison
---

# New WM Dev Team Weekly Meeting

## Summary

Alan Malta Rodrigues, Kenyi Hurtado Anampa, and (more briefly) Marco Mascheroni and Andrea Piccinelli reviewed a shared document on candidate strategies for integrating [[glideinWMS]] with [[DIRAC]]/[[DIRACX]]. With Strategies 1 and 2 already removed from the document (per earlier evaluation), the group focused on Strategy 3 versus Strategy 4, walking through [[DIRAC]]'s transformation-system architecture (transformation database, workflow task agent, request task agent) to understand where a glideinWMS integration would intercept the system. Marco left partway through due to another commitment, and Alan proposed continuing offline via further reading, with a possible follow-up discussion next week.

## Decisions / Conclusions

- No new strategy decision was made in this meeting. Kenyi restated his existing preference for Strategy 3 over Strategy 4, citing lower long-term maintenance effort and not significantly higher short-term development effort compared to Strategy 4.
- Strategy 4 was noted as the approach originally suggested by Federico (the DIRAC developer, not present): it is one of the easiest ways to integrate glideinWMS with DIRAC, but requires changes to DIRAC core components, making the changes less independent and potentially leading to higher long-term maintenance.
- Strategy 3 avoids modifying the DIRAC transformation database or the workflow task agent directly. Instead, it separates the work into two components — one that reads/tracks work before materialization (a new "queue service" backed by a separate job database, e.g. a small SQL/MySQL database) and one that performs the actual materialization/submission of jobs. Kenyi's rationale: if something goes wrong at submission time (e.g. HTCondor issues), jobs still accumulate correctly in the job database rather than breaking the translation of jobs from the workflow task agent into the queue.
- Kenyi deliberately avoided adding glideinWMS-specific logic directly into the DIRAC workflow task agent (a "short-circuit" approach Alan raised as an alternative) because the workflow task agent's future shape in DiracX is uncertain, and because this approach aims to touch as little of the existing DIRAC code as possible, keeping CMS-specific logic in a separate custom middleware component instead.
- Kenyi noted that Strategy 3's custom middleware architecturally resembles the microagent approach discussed elsewhere in the team's work, raising the possibility that this middleware could eventually be replaced by (or converge with) a microagent-based implementation. Alan suggested an alternative framing: implementing this as a new DIRAC system rather than an external custom middleware layer. Neither was decided; both were raised as open possibilities.
- Kenyi reiterated that the documented strategies are suggestions, not final: if a better approach emerges from group discussion (including from the microagent work), new strategies could still be proposed.

## Action Items

- [ ] Do further reading on the glideinWMS/DIRAC integration document and, if useful material is produced, share it with the group in advance of further discussion — Alan Malta Rodrigues

## Discussion

### DIRAC transformation-system architecture

Kenyi and Alan walked through the relevant parts of DIRAC's architecture using a shared diagram:
- **Transformations** define workflows (input/output dependencies), which Kenyi compared conceptually to what [[HTCondor]] provides via DAG-like structures.
- A **transformation agent** produces tasks from transformations based on configurable plugin criteria (e.g. different resource-requirement plugins per production job type, such as dedicated resources versus HPC resources).
- Two agents read from these tasks: the **request task agent**, which handles input data, and the **workflow task agent**, which reads both the logical-jobs table and the plugin-based resource-requirements table from the transformation database and injects the resulting logical jobs into DIRAC's WMS (which then creates pilot jobs). Alan noted this workflow task agent currently only supports assigning a job to run at a single site, whereas glideinWMS would need the flexibility to allow a job to run at any of several sites (e.g. sites A–E) — proposed as one possible reason a separate "enrichment" step is needed in the new queue service.
- Both the request task agent and workflow task agent write into shared tables of the same transformation database; there is no separate job-tracking database for materialized jobs unless one is added (as Strategy 3 proposes).
- Alan compared this architecture to WMAgent: communication happens largely through shared database state, with agents polling for new data to act on across different DB tables.

### Where Strategy 3 intercepts the system

Kenyi described intercepting output at the workflow task agent: rather than sending jobs to DIRAC's own WMS, a CMS-specific component reads the same two transformation-database tables (logical jobs and resource requirements) and materializes glideinWMS/[[HTCondor]]-compatible jobs itself, via the proposed queue service and job database.

### Data management interaction (Marco's question)

Marco asked where the DIRAC transformation/workload system interacts with data management (e.g. where queries determine data location so jobs can be routed accordingly). Kenyi and Alan agreed this logic lives in the transformation database itself: the request task agent handles input data and records this in the transformation database, and the transformation system separately talks to DIRAC's request management system and a storage/data management system. Alan reasoned through an example (a re-record workflow): a data-placement transformation would need to query [[Rucio]] (when used as the data-management backend) to determine where data ended up before the next transformation step (e.g. reconstruction) could use it.

### glideinWMS requirements on the integration

Alan asked what requirements glideinWMS imposes for smooth adoption into this ecosystem. Marco's preliminary answer: jobs need to be defined in terms of glideinWMS-style resource parameters (desired CPUs, memory, and similar sizing information); this was described as the main constraint, with further thought needed.

### Next steps

Given Marco's early departure, Alan proposed reviewing the document further individually, taking notes, and reconvening — possibly the following week — to continue with follow-up questions. Alan noted a fuller discussion would benefit from a better shared understanding of how data flows through DIRAC, and that this would likely require input from Federico.

## Open Questions

- What exactly does the "enrichment" performed in the proposed new queue service consist of (e.g. is it limited to enabling multi-site flexibility for a job, or does it cover more)?
- Could the transformation database itself be extended to track materialized jobs/retries/failures (as Federico suggested might be possible), or is a separate job database needed? Kenyi noted this was not discussed with Federico in enough detail to know if it would account for cases like retries.
- Should Strategy 3's custom middleware eventually be implemented as a microagent-based component, as a new dedicated DIRAC system, or remain a separate custom layer?
- What full set of requirements does glideinWMS impose on job/resource definitions for smooth integration into this system?

## Related

[[DIRAC]] · [[DIRACX]] · [[glideinWMS]] · [[HTCondor]] · [[Rucio]] · [[Workload Management]] · [[Work Queue]] · [[CMS]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-21 16.42.45 New WM Dev team weekly meeting`)
