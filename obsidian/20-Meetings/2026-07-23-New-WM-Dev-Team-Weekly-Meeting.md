---
type: meeting
date: 2026-07-23
participants:
  - Andrea Piccinelli
  - Alan Malta Rodrigues
  - Marco Mascheroni
  - Daniele Spiga
  - Liz Sexton-Kennedy
  - Kevin Lannon
  - Todor
topics:
  - CI/CD commit-message linting issue (dirac-cwl)
  - GitHub Copilot usage and AI coding assistants
  - DIRAC/DiracX ADR (Architectural Design Review) status and timeline
  - CMS offline week (September) and workload-management roadmap
  - interseed project and HTCondor-C / ARC / Lund plus SH backend
  - LHCb analysis production system and feasibility for CMS
  - CWL (Common Workflow Language) as a possible unifying workflow description
  - MCM (McM) history and goals for a unified Monte Carlo request system
---

# New WM Dev Team Weekly Meeting

## Summary

The meeting opened with an informal exchange about a CI failure in dirac-cwl: a commit message Marco Mascheroni prepared with GitHub Copilot exceeded a 78-character limit enforced by a commit-message-length test, which then caused failures to surface in unrelated pull requests; Alan Malta Rodrigues noted Copilot's PR description and its own review of the pull request both missed the issue. This led to a broader, informal discussion of AI coding assistants (GitHub Copilot's monthly "premium request" credit quotas, the CERN academic/educational licensing benefit for Copilot, and which underlying models are used) that was not treated as project business.

Andrea Piccinelli then ran through a short list of organizational items: a reminder about the weekly DWX call on Thursdays at 10am, an unconfirmed note about a possible new person joining, and a summary of the prior DIRAC/DiracX sprint-review meeting (noted separately in the corpus) — the team is largely waiting on reviews from people currently on vacation, and story-point-based velocity again came in lower than expected, which Andrea attributed more to how the DIRAC team assigns story points than to individual capability. Andrea suggested this, together with the broader question of planning around the DIRAC production/transformation system roadmap, would be worth raising once the DIRAC team (specifically Federico) returns from vacation, tentatively expected around the end of July/beginning of August, though Alan Malta Rodrigues thought more likely mid-to-end of August.

Daniele Spiga (joining to listen/follow along) asked about the realistic timeline for the DIRAC team's Architectural Design Reviews (ADRs). Alan Malta Rodrigues reported the DIRAC team said they have 6 ADRs in progress (one complete, one halfway done), and estimated release sometime between mid-August and early September, noting these are published as GitHub pull requests open for community feedback before being finalized — not immediately final documents. Marco Mascheroni suggested the October HSF/WLCG-related user workshop would likely be the point where most ADR-related discussion converges, since most relevant people would be present in person.

Marco Mascheroni then gave an update on the "interseed" project, which originated from discussions at a recent hackathon. He explained HTCondor's two operating modes (vanilla Condor with access point/central manager/execute point, versus Condor-G/glideinWMS-style pilot submission to compute elements). The interseed project is a library that an unspecified "X team" (DIRAC-related) is developing to talk to compute elements (Condor-C, ARC, "Lund plus SH" which he described as also being Condor) to submit jobs, check status, cancel jobs, and retrieve output — functionality that Marco noted overlaps significantly with what HTCondor already provides. The idea discussed at the hackathon was to bring HTCondor developers and interested DIRAC developers together to explore using HTCondor as the backend implementation for interseed; for CMS/glideinWMS, adopting the same approach would align with what ATLAS already does. Marco also mentioned separate, still-unformed ideas about evolving the glideinWMS frontend, to be shared with the group later. An HTCondor workshop in Lyon in October was mentioned as a relevant venue (about 2 hours' drive from Geneva). Alan Malta Rodrigues commented favorably on the general idea of factoring out the code that interacts with compute elements (and, similarly, storage elements) into its own well-tested, versioned package, noting this has long been an annoyance in WMCore/CRAB.

The remainder of the meeting was a detailed discussion of LHCb's "analysis production" system and its potential relevance to CMS, prompted by a discussion Alan Malta Rodrigues and Camille (Brown University) had with Chris(topher) Burr and Ryan. Alan described analysis production as a GitLab-merge-request-based system for preparing user workflows, running a small validation sample, checking exit status, and gathering resource-usage information, with DIRAC/DiracX as the backend — all payloads ultimately execute through DIRAC. Depending on requester trust, configuration, and outcome, workflows can be fully automated or require approval from a physics/analysis group (POG/PAG). Alan reported that Chris considered it "not feasible" to directly copy LHCb's GitLab-based setup to another experiment, because it relies heavily on LHCb-specific machinery (e.g., a tool called "lbmcsubmit" that maps user configuration into LHCb-specific objects, ultimately converted to CWL). Camille is looking into whether the DIRAC instance set up by Valentin (used previously for a DIRAC evaluation of running CMS payloads) could be used to test running CMS jobs/workflows through this kind of pipeline.

Liz Sexton-Kennedy questioned the purpose and scope, asking whether the goal was for CMS to have its own equivalent Git-based front end with CMS-specific generator fragments while reusing CMS's DIRAC instance as backend. She explained that the current McM (Monte Carlo Management) system for CMS was originally designed to be lightweight (she and Fabio were among its original designers, in 2012, before PPD split from offline/computing), but became increasingly heavyweight and gated by PAG sign-off; the intent was never for it to require this for all cases. She described a target architecture in which small-scale requests (illustratively, up to ~10,000 events) could be validated purely for computational soundness and executed automatically, while larger requests (millions to billions of events) would still require increasing levels of physics-coordination approval, similar to how LHCb's analysis production system separates computational validation from physics/scientific approval. Marco Mascheroni asked why a separate system would be needed for user (CRAB-based) versus central-production Monte Carlo; the discussion clarified that the goal is not two separate systems but a single, unified lightweight system usable by both individual users and central production, with heavier Monte Carlo requests "promoted" to central-operator oversight as needed — unifying what McM and CRAB currently do separately.

Discussion also covered CWL's role: Alan Malta Rodrigues noted CRAB uses a config object from WMCore, and that mapping the most common CRAB/WMAgent configuration fields to a CWL description would be a useful contribution. He confirmed CWL integration into DIRAC is ongoing but noted it is not yet clear whether CWL is actually what gets injected into the DIRAC backend today (an open point to be clarified). Liz Sexton-Kennedy asked whether legacy DIRAC (or DIRAC/DiracX as a hybrid) accepts CWL as backend input; Andrea Piccinelli clarified legacy DIRAC uses a different format (JDL), so mapping a CMS/WMAgent object to a format that is being phased out would not make sense — but mapping to CWL could make sense and could also be a positive contribution toward LHCb's own stated goal of migrating to DiracX. Kevin Lannon argued for a bottom-up approach: rather than starting from a full DIRAC/CWL proof of concept (he noted one exists marrying CWL with legacy DIRAC), the more valuable near-term step would be getting worker-node-level execution instructions expressed in CWL and successfully running a CMSSW job with everything it needs. Todor began describing a prior proof of concept that took the opposite, top-down approach, but the transcript ends before he finishes this point.

## Decisions / Conclusions

- The dirac-cwl CI failure was traced to a commit-message-length test (78-character limit) tripped by a Copilot-generated commit message from Marco Mascheroni; this was treated as resolved/understood, not requiring further action discussed in the meeting.
- The team's general view (Marco Mascheroni, Liz Sexton-Kennedy) is that CMS should aim for one unified, lightweight Monte Carlo request/workflow system usable by both individual users (currently served by CRAB) and central production (currently served by McM), rather than separate systems — with heavier requests promoted to central-operator/physics-coordination oversight as needed, rather than gating everything upfront as McM currently does.
- Legacy DIRAC uses JDL, not CWL, as its backend format; mapping CMS workflow objects to JDL was judged not worthwhile since legacy DIRAC is being phased out. Mapping to CWL was judged the more sensible target, and DIRAC's CWL integration is reported to be ongoing (though it remains unclear whether CWL is actually what is injected into the DIRAC backend today).
- Directly replicating LHCb's GitLab-based analysis production setup for CMS was assessed by Chris Burr (LHCb) as not feasible, because it depends heavily on LHCb-specific machinery for converting user configuration into LHCb objects/CWL.

## Action Items

- [ ] Marco Mascheroni to further develop and share his ideas for evolving the glideinWMS frontend with the group.
- [ ] Raise the DIRAC production/transformation-system roadmap and story-point/velocity concerns with Federico (and possibly Chris/Christoph) once he is back from vacation — Andrea Piccinelli.

## Discussion

- GitHub Copilot: Marco Mascheroni described using the CERN academic/educational Copilot benefit (apply via GitHub with CERN documentation) which provides a coupon for two years and 1,500 "premium request" credits per month, resetting monthly; a pull request was estimated to use around 500 credits. This was informal/off-topic conversation, not a project decision.
- Six DIRAC ADRs are reportedly in progress (one complete, one halfway done); it is unclear whether the DIRAC team intends to release them all together, though Alan Malta Rodrigues believes the production/transformation-system ADR is likely to be released together with related ones.
- ADRs are released as GitHub pull requests open for community feedback for some period before being finalized as the agreed architecture.
- Interseed: a library reportedly being developed to let DIRAC-side tooling talk to compute elements (Condor-C, ARC, and a system Marco referred to as "Lund plus SH," which he said is also Condor-based) for job submission, status, cancellation, and output retrieval. Marco assessed this functionality as largely overlapping with existing HTCondor capability, and floated the idea (raised originally at a hackathon) of using HTCondor as interseed's backend implementation, which would align CMS's approach with ATLAS's existing use of the same pattern.
- Alan Malta Rodrigues sees value, independent of the interseed/HTCondor outcome, in factoring the code that talks to compute elements (and storage elements) out of WMCore/CRAB into its own well-tested, versioned package — something he described as a long-standing pain point.
- LHCb's analysis production system: GitLab-merge-request-based front end; DIRAC/DiracX backend; validates a small sample of a workflow, checks exit status, and gathers resource-usage information before routing the workflow along different paths depending on requester trust, configuration, and scale (fully automated vs. requiring POG/PAG approval).
- Chris Burr reportedly described analysis production as the "fourth generation" of this kind of LHCb system, and indicated it is not yet settled how much of its functionality will persist as a standalone system in Run 4 versus being absorbed into the production and transformation systems.
- Liz Sexton-Kennedy explained the history and original intent of McM (she and Fabio were among the original designers in 2012), and argued it became more heavyweight than intended because it never had a lightweight/self-service path built in from the start.
- Kevin Lannon advocated a bottom-up approach to CWL adoption: start by expressing worker-node-level job instructions in CWL and get a working CMSSW job running end-to-end, rather than beginning from a full high-level DIRAC/CWL proof of concept.
- Todor began describing a proof of concept he worked on that took a top-down approach (starting from higher-level description rather than the worker node), as a contrast to Kevin's bottom-up suggestion; the transcript ends before he completes this point.
- Camille (Brown University) is exploring, together with Alan Malta Rodrigues, whether the DIRAC instance previously set up by Valentin (used earlier for a DIRAC evaluation running CMS payloads) can be used to test an analysis-production-style workflow against CMS jobs.

## Open Questions

- Whether the DIRAC instance's CWL integration is actually what gets injected into the DIRAC backend today, or whether the analysis-production CWL-conversion pipeline is separate from what DIRAC executes — flagged by Alan Malta Rodrigues as needing to be figured out.
- Whether Camille's feasibility testing should be run against Valentin's legacy DIRAC instance, DiracX, or both — Liz Sexton-Kennedy leaned toward starting with Valentin's DIRAC setup but this was not settled.
- Exact timeline for the DIRAC team's ADR releases and for the team members (Federico, Alexander) returning from vacation remains uncertain (estimates ranged from end of July/beginning of August to end of August).
- Whether/how much of LHCb's analysis production functionality will remain a standalone system versus being absorbed into the production/transformation systems in Run 4 is, per Chris Burr, still undecided.

## Related

[[CMS]] · [[DIRAC]] · [[DIRACX]] · [[HTCondor]] · [[glideinWMS]] · [[WMCore]] · [[CRAB]] · [[Workload Management]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-23 15.34.20 New WM Dev team weekly meeting`)
