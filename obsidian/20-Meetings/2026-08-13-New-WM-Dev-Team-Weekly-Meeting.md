---
type: meeting
date: 2026-08-13
participants:
  - Liz Sexton-Kennedy
  - Marco Mascheroni
  - Valentin Kuznetsov
  - Kevin Lannon
  - Eric Vaandering
topics:
  - CMS computing roadmap / work-package timeline
  - European site-admin workshop representation
  - HTCondor support for multiple workflow languages (CWL, Snakemake)
  - DiracX architecture sketch review
  - CRIC usage and information-source rationalization
  - GitHub stacked pull requests / PR review process
  - ADR timeline
  - CMS job wrapper (JIRA CMS-414)
  - Monte Carlo luminosity sections and DBS scaling
  - DIRAC VM testbed for analysis productions
---

# New WM Dev Team Weekly Meeting

## Summary

This was a weekly WM (Workload Management) Dev team meeting. Much of the meeting was led by a speaker captured only under the Zoom label `[EP 40/R-C10]`; this label is not a reliably identified individual and may represent a room or conference endpoint, so it is not listed as a named participant above, even though this label appears to have chaired/driven most of the agenda. Named participants who spoke substantively were Liz Sexton-Kennedy, Marco Mascheroni, Valentin Kuznetsov, Kevin Lannon, and Eric Vaandering. The meeting covered the upcoming CMS computing roadmap presentation, representation at a European site-administrator workshop, HTCondor's plans to support multiple workflow languages (CWL, Snakemake), a review of a DiracX architecture sketch/diagram, a detailed discussion of CRIC usage and the need to rationalize information sources for workload management, GitHub's new "stacked pull requests" feature, the DIRAC ADR timeline, the CMS job wrapper ticket (CMS-414), a long discussion of Monte Carlo luminosity sections and their implications for DBS scaling, and an update on attempts to use a DIRAC VM as a testbed for analysis productions. Several parts of the transcript are heavily garbled (disfluent, fragmented speech), and names of some participants and topics could not be reliably determined; this is flagged inline where relevant.

## Decisions / Conclusions

- CMS does not plan to duplicate compute-element information in CRIC: this information is already maintained in the submission infrastructure factories, and past experience with duplicated information maintained in two places was cited as a reason to avoid duplicating it in CRIC as well.
- CMS is understood to be the only LHC experiment that uses CRIC's bridge to the HR database to automate user administration/IAM (avoiding the need for secretaries to manually add/configure users). This is expected to be at least partly consolidated with the "Glance" system in the future; work on this consolidation (e-group management) is understood to already be ongoing with ICMS and the CRIC team, though the exact status is unclear ("I'm not sure that the work [is] going on, but there should be work going on").
- The group agreed on the general principle that information sources used by the workload management system should be rationalized and consolidated toward common solutions shared across experiments, rather than each experiment maintaining its own scattered sources (dashboards, REST APIs, config files). Liz Sexton-Kennedy noted she had written this down as a guiding note.
- Persistent/static data (e.g. a maintained site list) was concluded not to be needed in the WM system; the preference expressed was for dynamic, on-demand queries (e.g. "which sites currently provide GPUs," which sites hold a given dataset) with local caching in WM-side services, rather than maintaining separate static lists.
- Running analysis productions directly on the existing DIRAC VM was concluded not to be practical: Chris (from the DIRAC side) was clear that the VM is heavily tied to LHCb's specific DIRAC release, making it very challenging/implausible to run CMS analysis productions on it directly with that flavor of DIRAC.
- On Monte Carlo luminosity sections: no conclusion was reached, but there was broad agreement (Liz Sexton-Kennedy, Kevin Lannon) that Monte Carlo and real-data use cases should be treated differently going forward, since luminosity accounting (one of the two identified reasons for storing Lumi sections in DBS) has no meaning for Monte Carlo data, and that this topic needs further discussion with the generators group.

## Action Items

- [ ] Forward the email/answer regarding HTCondor's plans to support multiple workflow languages (Snakemake, CWL, and reportedly one more) to Liz Sexton-Kennedy — Marco Mascheroni
- [ ] Attach a draft CMS computing roadmap/timeline to the shared planning document for comment — Liz Sexton-Kennedy
- [ ] Discuss issue-prioritization alignment with Federico, in person, in September (before the ADRs/OIC) — no single owner stated
- [ ] Meet with Marco Mascheroni to clarify the plan for the HTCondor-interface prototype built during the earlier hackathon work, and produce a document on findings/possible direction for an analysis-production testbed — owner unclear in transcript (referred to variously as "Camille"/"Kami")

## Discussion

### CMS computing roadmap
Liz Sexton-Kennedy is preparing a high-level roadmap/timeline covering all of CMS computing, to be presented in about two weeks in a weekly-meeting format; this WM group is one of several "work packages" (others mentioned include infrastructure and data management). She described it as a first-draft guess based on when things are needed, not on available manpower, compiled by attending various teams' meetings and likely incomplete. She plans to present it as a timeline slide per area and asked to attach her draft to the shared planning document once ready, which she agreed to do.

### European workshop representation
The group briefly discussed representation at an upcoming European workshop (referred to as being "in France"; the exact name is unclear in the transcript) described as oriented toward site administrators, including basic tutorials. Marco Mascheroni confirmed he is attending, along with Luis from factory operations/submission infrastructure, and encouraged others in the group to attend if their schedules allow, noting it is a valuable, detail-oriented learning opportunity.

### HTCondor support for multiple workflow languages (CWL)
Liz Sexton-Kennedy said Brian (transcribed as "Boggleman," likely a mis-transcription of a name) had wanted to discuss CWL/HTCondor plans with her, since there may have been a misunderstanding about what HTCondor is planning for CWL support, but he has been too busy to connect. From a related meeting, the understanding was that HTCondor is aiming to support multiple workflow languages, including Snakemake, CWL, and one additional one not clearly captured. Marco Mascheroni confirmed he had seen an email response (from a contact transcribed as "Cole") corroborating that HTCondor plans to support multiple workflow languages, and agreed to forward it to Liz.

### DiracX architecture sketch review
The `[EP 40/R-C10]` speaker reported difficulty following the architecture sketch/diagrams produced a few weeks earlier, saying they were complex and did not have the expected focus, and asked (directed mainly at "Stefan," who is not identifiable as a distinct speaker label in this transcript) about a roadmap for further brainstorming on the sketch. Liz Sexton-Kennedy explained that the diagram shows relatively little detail about DIRAC because CMS has not yet seen DIRAC's ADRs (Architecture Decision Records); without those documents, no details of the DIRAC-side design can be assumed. Colored pieces in the diagram were described as CMS-side components that might persist into the new system (e.g., a possible Tier-0 request interface, though polling for files at Tier-0 was raised as a possible simpler alternative depending on how robust CRIC-provided information turns out to be); white-colored boxes were said to represent DIRAC. There was discussion of better color-coding the diagram to distinguish DIRAC components, other offline-data-management/computing components, and components external to offline computing.

### CRIC usage
Triggered by discussion of where DBS, Rucio, and CRIC fit as data/information systems, Liz Sexton-Kennedy asked how DIRAC uses CRIC differently from CMS. The `[EP 40/R-C10]` speaker explained CRIC is used by DIRAC for compute-element information, which CMS instead maintains in the submission infrastructure factories, so duplicating it in CRIC is not seen as worthwhile for CMS. Marco Mascheroni added, based on a conversation with Federico, that other VOs (non-WLCG) supported by DIRAC have had a hard time using CRIC (a WLCG project) for this, and likely store compute-element information elsewhere (e.g. a configuration file), similar to CMS's own approach. Liz also asked about CRIC's role in user identification; the `[EP 40/R-C10]` speaker explained CRIC bridges to the HR database and from there into IAM, and that CMS is the only LHC experiment that manages users this way (rather than administering users directly in IAM), a design decision attributed to "Paul and I," intended to automate user management without needing secretaries. Liz noted this overlaps with duplication already being addressed via the Glance system and e-group management consolidation with ICMS and the CRIC team.

### Information-source rationalization
The `[EP 40/R-C10]` speaker argued the key question is not what information is convenient for WM to pull from CRIC, but what resource and user information WM actually needs, and from what appropriate source — currently scattered across systems, dashboards, and REST APIs in CMS. They argued against maintaining static structures like a site list in WM, preferring dynamic queries (e.g., querying which sites hold a dataset, or which sites currently provide GPUs) with local caching services in the WM domain, potentially also tracking availability trends (e.g., over the last week vs. current day). They also distinguished static/rarely-changing information from dynamic information (e.g., sites/storage elements disabled by Hammer Cloud tests, or network issues). Marco Mascheroni added that the glideinWMS factory currently exposes information about compute-element queues and pilot size, and suggested this area should move toward a common, shared solution across experiments (potentially DIRAC- or CRIC-based, as used by ATLAS) rather than each experiment maintaining its own. Liz Sexton-Kennedy confirmed she had already noted the need to rationalize information sources and move toward common solutions where possible.

### Value of a published schema/interface document
Valentin Kuznetsov argued there is significant value in publishing a white paper or schema document describing data formats (e.g. for authentication or job description) that other players/experiments can implement against, rather than assuming voluntary compliance with an unpublished convention. He framed this as necessary groundwork for achieving generalization/common solutions across experiments, comparing it to a published standard that generic parsers could then be written against. The `[EP 40/R-C10]` speaker agreed this is a useful discussion to revisit once the architecture documents and roadmap are further along.

### GitHub stacked pull requests / PR review process
The `[EP 40/R-C10]` speaker relayed (crediting Valentin for raising it, and Chris for the underlying info) that GitHub has released a feature supporting "stacked pull requests" — reviewing/validating pull requests with cross-dependencies across multiple PRs. Neither Chris nor the `[EP 40/R-C10]` speaker had explored the details yet, but it was suggested this could become the recommended approach for handling cross-dependent code changes in the future. For now, per guidance relayed from Pedro via Mattermost, a PR needing a change from another not-yet-merged PR should wait for that PR to be merged before making the relevant updates. Valentin Kuznetsov confirmed this understanding and noted that when developers are unaware of such a blocking dependency, it can stall development for an unpredictable period and affect deliverables.

### Sprint status
The current sprint is mid-sprint and ends the following Thursday. The `[EP 40/R-C10]` speaker noted development had been slow, attributing it partly to the sprint starting around when people went on vacation, and mentioned their own work has been waiting on input from another side for some weeks; they suggested looking at the backlog for other issues to pick up in the meantime.

### Issue prioritization with Federico
The group noted they should not forget to discuss, with Federico in September, how issues are prioritized into the backlog on the DIRAC side, in order to align priorities. Liz Sexton-Kennedy agreed this needs to happen in person, ideally before the ADRs/OIC discussions.

### ADR timeline
Liz Sexton-Kennedy asked for a reminder of the ADR (Architecture Decision Record) timeline; the `[EP 40/R-C10]` speaker said the last update they had heard was that ADRs were expected by end of August, and confirmed they had not yet been released as of this meeting. Nomination for new conveners was also noted as open until mid-September.

### CMS job wrapper (CMS-414)
The `[EP 40/R-C10]` speaker noted Stefan had raised CMS job wrapper ticket CMS-414 as an important topic, suggesting the team could learn from job-wrapper capabilities in the ARC and PanDA workload management systems. No concrete follow-up was agreed beyond noting it as a topic to revisit once the ADRs and roadmap are available.

### Monte Carlo luminosity sections and DBS
The `[EP 40/R-C10]` speaker raised the proposal (discussed in another context, "Single Lumi per file" for Monte Carlo) to reduce Monte Carlo files to a single luminosity section per file rather than closing/opening a new luminosity section every N events, and asked whether this poses a blocker for workload management, CMSSW, or DBS. Marco Mascheroni suggested this is really a question for the DBS experts (Todd or Valentin), asking whether it would affect DBS at scale. The `[EP 40/R-C10]` speaker clarified their understanding that no information would be dropped, but that GEN files would be produced with far fewer luminosity sections per file (e.g., one, growing to something like ten once merged), reducing scale relative to today's files with up to a million luminosity sections, while still keeping at least one Lumi per file.

Liz Sexton-Kennedy said this needs discussion with the generators group, since it is unclear what "run" and "Lumi" conceptually mean for Monte Carlo, and referenced a past "lessons learned" issue where certain B-physics samples with filter efficiencies of 10⁻⁹ could not be produced, related to how Lumi information was gathered into datasets historically. She noted that where metadata is stored should depend on how it will be used.

Kevin Lannon agreed with focusing on use cases, distinguishing between runtime/processing-level metadata (which doesn't necessarily need a database) and information that needs to be tracked in a system like DBS. He identified two use cases historically served by Lumi sections in DBS: (1) luminosity accounting without reading the actual data — which has no meaning for Monte Carlo, since there is no luminosity to account for — and (2) locating a specific event by run/Lumi section — which he argued should be scrutinized given the potential cost of dramatically increasing DBS's scale, questioning whether individual Monte Carlo event lookup is actually needed. Liz Sexton-Kennedy and Kevin Lannon agreed that, unlike real data (where an individual event may be a meaningful outlier worth locating), Monte Carlo events are statistical/stochastic and not individually interesting in the same way.

Marco Mascheroni raised a third use case: job splitting for analysis workflows that read Monte Carlo data from DBS, asking whether any needed information would be lost by this change; he believed probably not. Liz Sexton-Kennedy said splitting should ideally be done at the file level; Eric Vaandering noted that some workflows can't process a whole file, which is where this becomes relevant. Kevin Lannon distinguished this from the real-data case: for real data, Lumi-section-level splitting is required because 0%/100% of every Lumi section must be processed and accounted for, whereas Monte Carlo could instead be split at the event level, which the framework is believed to support (though the group was not fully certain — CMSSW/ROOT event-entry-number lookup was discussed as likely supported, since ROOT indexes files for order-1 lookups, while run/event-number based lookup would require additional metadata). Kevin Lannon suggested it may be preferable to track Monte Carlo splitting in terms of event/entry numbers rather than continuing to force artificial, sometimes very small, Lumi sections into Monte Carlo files. The `[EP 40/R-C10]` speaker noted this could imply the data bookkeeping system may eventually need to track event ranges, which it currently does not (today only an event count is stored, without a first/last event range).

Liz Sexton-Kennedy added historical context: object-level (file-level) EDM metadata placement was introduced by the framework around 2018, well after DBS; separately, the generators group's own cross-section database (which is now part of DAS rather than DBS) was introduced during Run 2 and was a painful addition, illustrating that much of the current design reflects historical timing rather than a clean design. The `[EP 40/R-C10]` speaker suggested raising this topic, with the goal of identifying the right people to involve, at an upcoming "final booking week" (unclear reference in transcript).

### DIRAC VM testbed for analysis productions
The `[EP 40/R-C10]` speaker and Alan discussed, together with Chris (from the DIRAC side, referred to as "Chris Berg"), whether the existing DIRAC VM could serve as a testbed for analysis productions. Chris indicated this is impractical because the VM is heavily tied to LHCb's specific DIRAC release. The group is now discussing alternative directions, including producing a document on findings and possible feasible directions to bring to a wider decision-making discussion. One possible direction raised was to build on earlier hackathon work (attributed to a person referred to as "Camille"/"Kami," name unclear in the transcript, together with the `[EP 40/R-C10]` speaker) that prototyped submitting jobs through an HTCondor interface, executing a "dummy task." The idea discussed was to prepare a CMS-like task that could be submitted through this prototype interface to produce a small number of events as a proof of concept. A meeting with Marco Mascheroni was planned for the next day to better understand the existing plan for this prototype.

## Open Questions

- What is the alternative source of resource and user information that the workload management system should use going forward, given the plan to move away from relying on CRIC for this? Not resolved; framed as needing to be answered from the WM system's actual needs rather than from what CRIC happens to provide.
- Will GitHub's "stacked pull requests" feature actually help manage cross-dependent PRs? Not yet explored in detail by anyone in the group.
- How should "run" and "Lumi" be conceptually defined for Monte Carlo data, and what is the right cadence/granularity for storing related metadata? Flagged as needing discussion with the generators group.
- Is individual Monte Carlo event lookup (via DBS Lumi-section information) actually needed, given its potential cost to DBS scale? Raised by Kevin Lannon as an open question.
- Does the CMSSW/ROOT framework fully support event-range-based (rather than Lumi-section-based) splitting and processing for Monte Carlo, and would this require new metadata beyond what ROOT can already provide from file indices?
- What is a feasible alternative direction for an analysis-production testbed, given that direct use of the LHCb-flavored DIRAC VM is not practical?

## Related

[[DIRAC]] · [[DIRACX]] · [[CRIC]] · [[DBS]] · [[Rucio]] · [[HTCondor]] · [[glideinWMS]] · [[Workload Management]] · [[Submission Infrastructure]] · [[CMS]] · [[WLCG]] · [[CWL]] · [[CMSSW]]

## Source

meeting_saved_closed_caption.txt (from `2026-08-13 15.10.28 New WM Dev team weekly meeting`)
