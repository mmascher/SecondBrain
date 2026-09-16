---
type: meeting
date: 2026-03-11
participants:
  - Marco Mascheroni
  - Kenyi Hurtado Anampa
topics:
  - DIRAC integration strategies
  - PanDA/DIRAC comparison
  - workflow management system evolution
  - GlideinWMS value proposition
---

# New WM Dev Team Weekly Meeting

## Summary

Marco Mascheroni and Kenyi Hurtado Anampa reviewed a document Kenyi had written evaluating strategies for integrating [[DIRAC]] with [[glideinWMS]]/[[HTCondor]], as a parallel effort to an earlier PanDA integration analysis. They walked through DIRAC's architecture (transformation agent, workflow task agent, request task agent, JobDB/TaskDB), compared four candidate integration strategies, and converged on a preferred strategy and a preliminary technical opinion to bring to an upcoming Level-1 presentation on evaluating alternative workload-management systems for CMS.

## Decisions / Conclusions

- Strategy 1 (directly modifying DIRAC core) was concluded to be a no-go: it requires core changes to a codebase CMS does not own, which would be hard to get upstreamed/maintained.
- Kenyi's preferred DIRAC strategy is Strategy 3: an external CMS adapter split into components, keeping DIRAC's workflow task agent only as a thin plugin that submits pilots to Condor SKD (Schedd) using glideinWMS-compatible ClassAds, with a separate custom component tracking job status (read from Condor and/or a dedicated job database) and a separate submission component. This gives CMS more ownership/freedom, at higher (but still lower-than-PanDA-equivalent) development effort.
- Strategy 4 (the hybrid approach worked out with Federico, the DIRAC developer) keeps more of DIRAC's workflow task agent, submitting pilots to Condor SKD directly from it and adding one component to update job status in the transformation database. It is simpler/lower effort but depends on the workflow task agent, which does not exist in DiracX — considered its main disadvantage.
- DiracX does not yet implement the workflow/pilot-submission functionality analyzed in DIRAC; any DIRAC-based strategy would need to be re-evaluated once DiracX supports it. The working assumption discussed was: if an integration approach works with DIRAC, it should be portable to DiracX once DiracX reaches parity, since CMS cannot make DiracX progress before the presentation.
- Marco's conclusion for the presentation: given a stated priority of "cleanest architecture" (to minimize long-term technical debt and ease onboarding/feature development), DIRAC's Strategy 3 offers a cleaner architecture with less development effort than the equivalent PanDA strategy (PanDA Strategy 3, characterized by Kenyi as higher effort). This was framed as Marco's personal conclusion/opinion based on Kenyi's analysis, not a formal team decision.
- The group agreed the DIRAC transformation database + workflow task agent are architecturally analogous to CMS's Request Manager + microservices Work Queue (WMCore's central "brain" component), reducing the need to reinvent that layer.
- Marco's earlier workflow-orchestrator proof of concept (querying the Request Manager and submitting a scheduler-universe Condor job running a "microagent" that tracks file-based progress in a local SQLite database) was noted as conceptually similar to the custom-middleware layer in DIRAC Strategy 3, and to PanDA Strategy 1.
- One acknowledged open risk/caveat for DIRAC versus PanDA: PanDA has proven production scale, while DIRAC's scale at CMS's required volume is still unknown ("an incognita"). Marco noted the actual scaling concern is about job-granularity database load rather than Condor itself, since Condor scales at the request/pilot level.
- The metrics/evaluation table structure used for the PanDA comparison should be reused for the DIRAC comparison, and the same conclusion structure should apply to both.
- Kenyi does not plan to include a direct architecture-comparison diagram sourced from a 2017/2018 DIRAC paper in the presentation slides (though it can stay referenced in the document); Marco considered the diagram misleading (e.g., inconsistent treatment of HTCondor/Condor-C dependencies across experiments such as ALICE).
- Kenyi does not plan to present a direct PanDA-vs-glideinWMS or DIRAC-vs-glideinWMS comparison, since that is expected to draw a separate line of questioning about the value/effort of glideinWMS itself.

## Action Items

- [ ] Prepare a backup slide (not necessarily presented) on the value/effort of GlideinWMS and Condor's matchmaking/global-pool capabilities, anticipating Level-1 questions — Marco Mascheroni
- [ ] Add the referenced DIRAC/pilot-systems comparison paper (believed to be by Andrew McNab, ~2017-2018) to the document's reference links — Kenyi Hurtado Anampa
- [ ] Identify which database table (JobDB or TaskDB) stores DIRAC site definitions — Kenyi Hurtado Anampa
- [ ] Produce a comparison table covering all four DIRAC strategies (including the two without diagrams), noting why the first two were discarded — Kenyi Hurtado Anampa
- [ ] Structure the presentation as: PanDA integration-strategy slides, DIRAC integration-strategy slides, and a shared conclusions slide covering both — Kenyi Hurtado Anampa
- [ ] Coordinate with Andrea Piccinelli and Kevin Lannon on how much system-architecture content to cover in the presentation, to avoid duplicating material — Kenyi Hurtado Anampa
- [ ] Prepare/circulate a summary slide of the DIRAC/PanDA conclusions for Marco and others to comment on before the presentation — Kenyi Hurtado Anampa

## Discussion

### DIRAC architecture overview

Kenyi explained that DIRAC separates data management and job generation into two agents (unlike PanDA's JEDI/harvester combination): the **workflow task agent** (also referred to as workflow test agent) reads job/resource needs from the transformation database and handles job generation, resource provisioning, and pilot submission; the **request task agent** handles data movement (e.g., staging input files). The **transformation agent**, which Kenyi compared to PanDA's JEDI, is the "brain" that defines workflows as transformations — object definitions similar in spirit to a Condor DAGMan structure, supporting dependencies between jobs (Job A/B/C). Transformations are divided into tasks recorded in a transformation database, which the workflow task agent reads to generate and submit jobs. Marco noted this database does not itself hold CPU/memory needs; those come from user-defined "categories" (analogous to CMS request-manager job categories) associated with each workflow type.

Marco and Kenyi agreed that replacing the transformation agent would be equivalent in scope to replacing PanDA's JEDI — effectively a full re-implementation, not a targeted change. Kenyi's analysis therefore focused on the workflow task agent, mirroring the scope of the earlier PanDA analysis, and only considered changes needed at that level.

### Discussion of the DIRAC/pilot-systems comparison diagram

Marco raised strong objections to a diagram from a referenced DIRAC paper (~2017-2018, believed authored by Andrew McNab) comparing pilot-system architectures across experiments (including ALICE), arguing it inconsistently depicted dependence on HTCondor/Condor-C across systems and appeared designed to make DIRAC look architecturally simpler than it is. Kenyi agreed the diagram was likely oversimplified and explained that DIRAC's apparent point was that it does not depend on external third-party schedulers/provisioning systems in the way glideinWMS/Condor-based systems do (though DIRAC does use the Condor grid universe in some cases). Both agreed not to include this diagram in the presentation slides, though it may remain referenced in the underlying document.

### Candidate DIRAC integration strategies

Kenyi described four strategies evaluated in the document, following the same framing requested by Kevin Lannon for the PanDA analysis (direct modification vs. external components):

- **Strategy 1 — direct DIRAC core modification.** No diagram was made. Concluded as not recommended: requires core DIRAC changes CMS does not own, making propagation/maintenance difficult.
- **Strategy 2 — external adapter layer.** A single external CMS adapter layer. Considered not the best option either; related open comments existed around the job-database design (previously discussed separately between Marco and Kenyi).
- **Strategy 3 — external adapter split into components (preferred by Kenyi).** The workflow task agent is kept only as a plugin for submitting pilots to Condor SKD using glideinWMS-compatible classads. CMS-built components track job status (reading from Condor directly and/or a job database) and handle submission (analogous to a Harvester Condor plugin). Marco compared this to his own proof-of-concept "job updater"/SQLite tracking approach. Open implementation questions raised included whether job status should be read from Condor on the fly or cached, and how to handle Condor request failures/retries and Condor downtime. This strategy gives more ownership and a cleaner architecture but requires more development effort than the hybrid Strategy 4 (though still less effort than the equivalent PanDA strategy per Kenyi's assessment).
- **Strategy 4 — hybrid approach (developed with Federico, the DIRAC developer).** Retains the workflow task agent submitting pilots directly to Condor SKD; CMS adds only one component to update job status in the transformation database. Lower effort but relies on the workflow task agent, which does not exist in DiracX, and requires closer coordination with the DIRAC team — its main disadvantage per Kenyi.

Marco asked whether DIRAC site definitions (CE name, core/memory sizing per pilot) live in the JobDB/TaskDB schema shown, since he recalled a flat text file listing sites from prior experience; Kenyi believed the definitions come from what the transformation database generates but was not certain of the exact table and took an action item to confirm.

### DiracX vs. DIRAC

Marco raised that the workflow task agent functionality analyzed does not yet exist in DiracX, so the same evaluation would need to be redone once DiracX implements it. Kenyi noted Gavin's guidance was that CMS cannot make DiracX progress before the presentation, so the working assumption is that a strategy shown to work with DIRAC should also be achievable with DiracX, without knowing DiracX's exact future shape. Marco observed that CMS's timeline differs from LHCb's DiracX timeline, creating a practical dependency mismatch: CMS needs a decision by a certain date but currently only has DIRAC (not DiracX) available to evaluate against.

### Comparison with the earlier PanDA analysis and Marco's proof-of-concept

Marco connected the DIRAC Strategy 3 architecture to the microservices-based proof of concept he, Andrea Piccinelli, and Brian Bockelman had been designing, later implemented with AI-agent assistance per Dima Kovalskyi's suggestion. Marco's prototype used a central workflow orchestrator querying the Request Manager (intended eventually to query the Work Queue) and performing splitting, then submitting a scheduler-universe Condor job running a "microagent" per work element that tracks progress and saves results in a local SQLite database (file-based, discarded once the request completes) — enabling file-based recovery. Marco noted this resembled Dima's DAGMan-based variant of the same proof of concept, and that this general pattern (custom middleware between a central request source and Condor) would map most closely to PanDA Strategy 1.

Kenyi noted that, unlike the DIRAC Strategy 3 middleware (medium effort, per his assessment), the equivalent PanDA strategy (PanDA Strategy 3) has more components in its custom middleware and was assessed as higher effort, though it also offers a clean architecture.

### GlideinWMS value proposition and matchmaking

Marco and Kenyi discussed how to address anticipated Level-1 questions about the value of continuing to use glideinWMS/Condor matchmaking on top of either PanDA or DIRAC. Marco argued Condor's global-pool matchmaking (including GPU-aware matchmaking, which he believes neither PanDA nor DIRAC currently supports with comparable granularity) is glideinWMS's true unique value, having evolved over roughly 40 years, and that this value only holds if other experiments (e.g., ATLAS, LHCb) also recognize and adopt Condor-based matchmaking rather than CMS being the sole user long-term. Marco considered this a personal, unresolved opinion, not something to put directly in the slides — the team agreed only to prepare it as a backup/anticipatory slide.

### DUNE and community interest in DIRAC

Kenyi noted DUNE has been considering DIRAC as part of a broader interest in adopting it, partly because DUNE's current workflow system (Justin, developed largely by one person and using AAA-based remote access, which does not scale to CMS's needs) is expected to be replaced. If CMS adopts DIRAC and implements glideinWMS as a pilot-submission option within it, DUNE would likely be able to pick that option up, which Kenyi suggested is useful context for Level-1 (community expansion / funding justification for glideinWMS work) without going into detail. Marco suggested trying to talk to DUNE developers, referencing Andrew McNab; Kenyi had not spoken with them directly but had heard secondhand (via Kevin Lannon) that some contact may already exist, possibly through CMS staff at Fermilab.

## Open Questions

- Which exact table (JobDB or TaskDB) stores DIRAC site definitions?
- How should job status be tracked in DIRAC Strategy 3 — read live from Condor, cached, or via a dedicated job database — and how should Condor request failures/retries and downtime be handled?
- Will DIRAC Strategy 3-style core changes to the workflow task agent be needed, and if so, how significant are they?
- How will any DIRAC-based integration strategy need to be re-evaluated once DiracX implements the equivalent workflow/pilot-submission functionality?
- Should the DIRAC and PanDA analyses be presented as one combined presentation or two separate presentations, and how should content be divided with Andrea Piccinelli and Kevin Lannon's architecture material?
- Is DIRAC's scalability at CMS's required job volume viable, given PanDA's proven scale versus DIRAC's unknown scale in this context?

## Related

[[DIRAC]] · [[DIRACX]] · [[glideinWMS]] · [[HTCondor]] · [[Workload Management]] · [[CMS]] · [[Work Queue]] · [[WMCore]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-11 14.13.35 New WM Dev team weekly meeting`)
