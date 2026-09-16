---
type: meeting
date: 2026-09-04
participants:
  - Marco Mascheroni
  - Alan Malta Rodrigues
topics:
  - Level 2 coordinator nomination for GlideinWMS / Submission Infrastructure
  - Conditions preparation workshop — Tier 0-like workflow requirements
  - HLT / CERN pool resource provisioning for the prompt calibration loop
  - HTCondor quotas, priority, and global share enforcement
  - Fallback submission options (DIRAC/DIRACX vs. direct HTCondor access)
  - CWL architecture (job / workflow / transformation layers) and a possible Request Manager adapter
---

# Conditions Workshop, HLT Provisioning, and CWL Discussion

## Summary

A 1:1 between Marco Mascheroni and Alan Malta Rodrigues. The meeting covered three main threads: (1) an open, undecided discussion about who might nominate themselves for a Level 2 coordinator position for [[GlideinWMS]] / [[Submission Infrastructure]] following a recent stepping-down from that role; (2) preparation for an upcoming conditions preparation workshop, where Alan and Andrea are giving a talk on Tier 0-like workflow requirements, including detailed discussion of how HLT/CERN-pool resources are provisioned and prioritized for the prompt calibration loop (PCL), and what fallback submission options exist if the group does not adopt [[DIRAC]]/[[DIRACX]]; and (3) a technical discussion of [[CWL]] architecture — distinguishing job-level, workflow-level, and transformation-level CWL documents — and whether a temporary adapter should be built to convert Request Manager JSON workflows into CWL.

## Decisions / Conclusions

- Cloud HLT resources were previously used opportunistically during interfill periods (an experiment run when Diego Gomez was involved, which produced a paper), but this was discontinued: dynamically spinning up/rebooting HLT nodes when not in use by the online system required ongoing operational effort that was judged not worth it, and nobody was willing to keep maintaining it.
- On HTCondor scheduling in the shared CERN/Tier-0 pool: provisioning speed is not the concern — the Tier 0 activity (including PCL jobs, given the highest priority) is matched first as soon as resources are available (matchmaking/priority), not through faster resource provisioning. The negotiator continuously enforces the current quota rather than averaging usage over time, and global share/fair-share is enforced at the pool level.
- Agreed fallback for the calibration group's workflows if they do not want to use [[DIRAC]]/[[DIRACX]]: rather than the group standing up and operating its own independent HTCondor pool/negotiator directly on HLT machines (which would remove those resources from CMS's shared accounting and control), the fallback should be direct `condor_submit` access via CMS's own Submission Infrastructure-provided schedulers ("manually launched glideins") connected to CMS's existing resource shares — preserving CMS's control over quotas. [[CMS Connect]] was noted as an existing, under-used way for users to get this kind of direct HTCondor access.
- On a possible adapter converting Request Manager JSON workflows into [[CWL]]: both agreed that if such an adapter is built, it must be a small, isolated, removable "edge service" component (fetching documents and rewriting them into CWL) rather than a compatibility layer woven into the rest of the system — motivated by the shared concern that "temporary" adapters tend to become permanent. The long-term objective remains storing CWL natively in the database. Central production might eventually be able to drop the Request Manager JSON representation entirely, but for analysis ([[CRAB]]) both systems will likely need to run in parallel, since CRAB's server already has its own REST interface backed by a database queried by the task worker.
- Approved: Alan will add a link to CMS's HTCondor fair-share/quota documentation (which includes a summary table and supports fair share at the Tier level) to the workshop slide.
- The conditions-preparation-workshop planning document was deliberately split by quarter into separate documents rather than kept as one large running document, based on past experience (the old approach, used for ~2 years of weekly stakeholder meetings, grew to ~30 pages and became hard to navigate, especially for people who hadn't attended the meetings).

## Action Items

- [ ] Collect information from Thomas (surname/transcription unclear — "Thomas, his light") on whether prompt-calibration-loop workflows are single-core or multi-core and their GPU requirements, and add it to the workshop slides — Alan
- [ ] Add a link to the HTCondor fair-share/quota documentation to the workshop slide — Alan
- [ ] Send Alan the HTCondor fair-share/quota documentation link — Marco

## Discussion

### Level 2 coordinator nomination
Following a recent stepping-down from a coordination role, Marco raised whether to nominate himself for a Level 2 position covering this area of computing; Alan encouraged him to do so and said either of them "would be the best call" for it. Marco said that before nominating himself he needs USCMS approval, since his effort is split across percentages in different areas and USCMS (via the Level 1 leads — Stefan was mentioned as being in USCMS) would need to formally acknowledge a shift of his effort toward Submission Infrastructure. Alan said he is undecided about nominating himself, citing a need to prioritize his experiment responsibilities, though he noted the role would likely help his CV. Other potential candidates discussed: Eric Vandering (Alan thought he "would be nice"), Valentin (reportedly nominated previously, before a discussion about splitting the organizations came up — Alan wasn't sure if that nomination still stands), and Antonio (uncertain whether he is still active enough in this area; Alan noted Antonio seems to have "ramped down" his involvement compared to previous years). No decision was reached; both said they would be comfortable if both were nominated.

### Conditions preparation workshop
Alan and Andrea have been invited to give a talk at the conditions preparation workshop (described as happening the following week, on a Wednesday). They had previously met with a contact named Dan and exchanged follow-up emails on requirements for Tier 0-like workflows. Alan relayed concerns raised by a workshop contact — transcribed as "Keys" (name unclear), described as one of the coordinators/conveners of the prompt calibration workflow area — about using [[GlideinWMS]] for these workflows: latency is a bigger concern for Tier-0-like/PCL workflows than for central production (which is throughput-oriented), because a workflow expected to complete within roughly an hour needs to do so reliably, and there are downstream dependencies in the chain. The contact's concerns centered on (a) the complexity potentially imposed by using GlideinWMS-provisioned resources, and (b) how access to HLT machines is provided today, including whether the group would need a different setup (e.g. direct HTCondor submission) instead. Alan noted the calibration group's plan appears to be considering whether to adopt DIRAC/DIRACX for these workflows and needs to know the associated timeline if so; in the meantime their current fallback plan is more of a lightweight, direct approach. Alan also noted their workflows have real data/task dependencies (not just job submission), meaning they would likely need some workflow-management layer regardless of the submission mechanism used.

### HLT/CERN pool resource provisioning
Marco confirmed the prompt calibration loop (referred to elsewhere as "Alcarico"/PCL) already runs on the Tier-0 WMAgent (transcribed as "double M agent" / "double Magence" — likely [[WMAgent]]) today, though Alan and Marco use different names for it. The CERN resource pool (distinct from the "global pool") was described as containing resources associated with the Tier-2 CERN site, resources associated with the Tier-0 CERN site (transcribed indistinctly, e.g. "Tier 2 CHR" / "tier zero CHR" — likely referring to CMS site-naming conventions such as T2_CH_CERN / T0_CH_CERN, though the exact names are not clearly transcribed), and HLT resources — all ultimately drawn from the same underlying worker nodes. Only the "cloud HLT" portion is ever available to this pool; the online/data-taking HLT farm itself cannot be used since it is needed during data taking. Marginal opportunistic use during interfill periods (when the beam is down) was judged not worth the operational effort (see Decisions above).

Within the Tier-0 pool, quotas exist for all activities but Tier 0 has priority, and PCL jobs are given the highest priority within Tier 0, matched to resources first as soon as they're available. Since preemption is not used, and many jobs rotate through in practice, Alan noted this is not expected to be a major issue in practice, though a large, high-priority PCL workflow could in principle temporarily take over the resources allocated to Tier 0. Marco noted that whether this matters in practice depends on job core count: 8-core jobs are the hardest to find a slot for (so ramp-up could be slower for those), whereas single-core jobs — like analysis jobs, which rotate quickly — will generally find a slot quickly. It is not confirmed whether PCL/calibration jobs are single- or multi-core (open question; Alan to check with Thomas). Alan also asked whether PCL/multi-harvesting workflows would need GPUs; Marco raised the question in the context of possible future changes to HLT, and Alan's assessment (unconfirmed) is that these workflows are mostly data-intensive (plenty of input data, very little output) and likely would not need GPUs.

### CWL architecture
Marco and Alan discussed the emerging [[CWL]] (Common Workflow Language) design for describing CMS workflows, identifying three layers: a job-level CWL document describing a single job, a workflow-level CWL document describing the overall workflow (which embeds job CWL), and — per Alan — a third, "transformation" layer, where a transformation is one task within a workflow (a processing task, or a data task such as replication, deletion, or movement), also to be described as a CWL document. Alan expects the Request Manager will need an adapter/converter for a while to translate the existing Request Manager JSON workflow description into a CWL-based description; see the agreed constraint on this under Decisions above. Marco described the current CRAB/central-production architecture as comparable: a Request Manager plus (for CRAB) a REST-interface "CRAB server" backed by a database queried by the task worker. The long-term goal remains storing CWL directly in CMS's own database, with an adapter needed at minimum as a phase-out/transition mechanism for the wider CMS collaboration.

Separately, work exploring CWL (with "b-j" — name as transcribed, elsewhere also referred to as "VJ"/"V-Jay"; exact name unclear — and Camille) was mentioned; Alan said this person is expected to confirm their continued commitment to this exploration either that evening or by the following Monday. Alan advocated taking "baby steps" in this exploration given how broad the possible scope is, with each step incrementally reducing reliance on what Alan referred to as "Dublin Core" (this term is unclear in the transcript — Alan, a long-time contributor to CMS's workload-management core software, may have intended [[WMCore]]; preserved here as transcribed since the intended term is not unambiguous).

## Open Questions

- Whether prompt-calibration-loop (PCL) workflows are single-core or multi-core, and whether they will need GPUs — unresolved; Alan to check with Thomas.
- Whether future changes to HLT infrastructure will need to support GPU workloads.
- Whether Marco will obtain the USCMS approval needed to formally nominate himself for the Level 2 coordinator position, given his effort is split across percentages in different areas.
- Whether Alan will nominate himself for the same position — he remains undecided, citing competing experiment priorities.
- Whether Valentin, Eric Vandering, or Antonio will also be candidates for the Level 2 position.
- Whether the calibration group will adopt DIRAC/DIRACX for their Tier 0-like workflows, and on what timeline.
- Whether "b-j"/"VJ" will confirm continued commitment to the CWL exploration work with Camille.

## Related

[[GlideinWMS]] · [[HTCondor]] · [[DIRAC]] · [[DIRACX]] · [[CWL]] · [[WMAgent]] · [[CRAB]] · [[WMCore]] · [[CMS Connect]] · [[Submission Infrastructure]] · [[CMS]] · [[CERN]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-04 09.11.26 Marco Mascheroni's Personal Meeting Room`)
