---
type: meeting
date: 2026-03-10
participants:
  - Marco Mascheroni
  - Kenyi Hurtado Anampa
topics:
  - GlideinWMS integration with PanDA
  - GlideinWMS integration with DIRAC
  - offline computing week presentation prep
  - job bookkeeping duplication
  - strategy comparison tables
  - resource provisioning ownership vs maintenance
  - community-building considerations
---

# GlideinWMS Integration with PanDA/DIRAC — Slide Prep Discussion

## Summary

Marco Mascheroni and Kenyi Hurtado Anampa met one-on-one to prepare slide content ahead of presentations the following week at CERN offline computing week (Marco noted he had been assigned multiple slide decks by Andrea). The discussion focused on framing principles and comparison tables for evaluating candidate strategies to integrate GlideinWMS with PanDA and DIRAC as part of exploring alternatives/evolutions to the current WMAgent-based submission infrastructure. Much of the meeting was Kenyi thinking out loud while building a PanDA strategy-comparison table live, with Marco challenging and refining the dimensions (ownership, maintenance, complexity to evolve, ease of onboarding new developers, resource definition, brokerage intent, job execution/scheduling, job bookkeeping). They also discussed a current-system pain point (job bookkeeping duplicated across multiple databases), an idea (attributed to Kevin) about collaborating with HTCondor developers on data-locality-aware matchmaking, and broader political/funding considerations about whether a CMS-led solution needs to demonstrate it can serve a wider community.

## Decisions / Conclusions

- For the effort estimates requested by Stefan Lammel and Daniele, Kenyi decided not to commit to FTE numbers (citing insufficient information, especially for DIRAC) and will instead present effort as low/medium/high, split into short-term (development, testing, deployment) versus medium-/long-term categories.
- No strategy (1, 2, or 3, in Kenyi's PanDA framing) was decided on for the presentation. Kenyi's working conclusion is to propose starting with Strategy 2 as a conservative, reusable stepping stone toward an eventual Strategy 3, rather than committing immediately to the more complex Strategy 3 or settling for Strategy 1.
- The group agreed that ATLAS's use of GlideinWMS under "Strategy 1" is convenient for ATLAS specifically because GlideinWMS is maintained by CMS/OSG and requires no deployment effort on ATLAS's side, but is not equally attractive for CMS long-term since it would require CMS to maintain both a GlideinWMS layer and a PanDA layer. This point was agreed as worth including in the slides, framed informatively rather than as a criticism of ATLAS.
- Marco and Kenyi agreed to meet again the next day (starting around 30 minutes earlier than this meeting, keeping the same one-hour slot) so Kenyi can walk Marco through the DIRAC strategy document in more detail.

## Action Items

- [ ] Meet again the next day (~30 min earlier than today's start, same 1-hour slot) to review the DIRAC strategies document together — Marco Mascheroni, Kenyi Hurtado Anampa
- [ ] Re-read own earlier DIRAC notes (covering four candidate strategies) to refresh before the follow-up meeting — Kenyi Hurtado Anampa
- [ ] Build a strategy-comparison table for DIRAC similar to the one drafted for PanDA — Kenyi Hurtado Anampa
- [ ] Add a job-bookkeeping row/consideration to the comparison table(s), reflecting the current system's duplicated job-tracking databases — Kenyi Hurtado Anampa
- [ ] Add a "resource definition" row to the PanDA comparison table (where/how sites and CEs are defined, e.g. equivalent of the factory XML) — Kenyi Hurtado Anampa
- [ ] Add an "ease of onboarding new developers" row/dimension to the comparison table — Kenyi Hurtado Anampa
- [ ] Add a slide/point noting that ATLAS gets GlideinWMS "for free" (maintained by CMS/OSG) under Strategy 1, which is convenient for ATLAS but implies double maintenance for CMS long-term — Kenyi Hurtado Anampa
- [ ] Ask Andrea whether framing the CMS-led option around "building a community" (i.e., making it usable by other experiments) is the right message for the conclusions — Marco Mascheroni
- [ ] Discuss conclusions with Andrea on Thursday — Kenyi Hurtado Anampa

## Discussion

### Presentation prep context
Marco noted Andrea had assigned him three slide decks plus one to prepare jointly with the team, on top of a tight travel schedule to CERN, calling the workload "a little bit crazy." He described the current meeting as an opportunity to work through disagreements internally ("stones in my shoe") before offline computing week next week, rather than raising them for the first time in the larger meeting.

### Guiding principle: avoid stacking systems
Marco articulated a principle he wanted reflected in the slides: integrating GlideinWMS with PanDA or DIRAC by simply layering one system on top of another is achievable in the short term, but leads to having to maintain two systems long-term, with associated ongoing effort.

### What CMS wants from PanDA/DIRAC
Marco's view: the main value CMS wants from PanDA or DIRAC is their data/request management capability (queuing requests, staging data from tape, etc.), since GlideinWMS itself does not do this. Kenyi agreed but noted that since this specific talk is scoped to GlideinWMS integration, his report focused mainly on resource provisioning (what GlideinWMS actually does), touching data management only where it intersects resource provisioning (e.g., worker nodes acquiring input files or staging out outputs). Broader WMS topics (the "big picture," including for PanDA and DIRAC) were described as being covered separately, in Alan's work.

Kenyi noted that job generation/request handling would be handled by PanDA or DIRAC in either integration approach, which he said answers a question Daniele had raised the day before ("what do we gain?").

### Job bookkeeping duplication in the current system
Marco described the current system's job-tracking data as duplicated across multiple places: HTCondor's own job queue, the WMAgent's SQL database, a CouchDB copy, WMStats-specific tables derived from CouchDB (described as relying on old technology), and MONIT — effectively three or four separate "tables" of the same jobs.

Marco's stated principle: any new system should avoid replicating job bookkeeping already handled well by Condor, PanDA, or DIRAC. He argued jobs are inherently temporary (needed only to process inputs and produce outputs), so the durable bookkeeping should be based on files/data rather than jobs; recovery (the current system's ACDC-equivalent) should likewise be driven by identifying missing/incomplete data rather than by job state, and each target system would likely implement its own recovery mechanism.

Kenyi's counterpoint: some notion of a "logical job" is still needed — the job as originally intended/submitted, as distinct from its (possibly multiple) actual execution attempts. For example, a Condor job retried three times produces three actual Condor job records that all correspond to one logical job; the system needs to account for this retry relationship (e.g., "these 300 jobs belong to the same logical job in this workflow"). Marco and Kenyi agreed this concept maps to the current system's WorkQueueElement (WQE) — a logical unit of work that can be split into, and mapped from, multiple actual worker jobs. They also discussed that a PilotJob can run many worker jobs, and that this "job layering" (logical job → worker job → pilot job) may differ by strategy.

Kenyi noted the current system already has two retry layers: WMAgent-level (with an ACDC server that regenerates jobs to reproduce missing data, based on the data gap rather than the specific failed job) and Condor-level retries. Marco noted Condor itself supports job retries (e.g., via expressions to retry on a different site/node), something he has used in his own proof-of-concept work.

### Comparison table for PanDA strategies
Kenyi worked live on a comparison table for the (previously defined, not re-explained in this meeting) Strategy 1/2/3 spectrum for PanDA integration, with Marco providing feedback on the dimensions:

- **Maintenance**: ongoing cost of running/supporting the approach.
- **Ownership**: not a cost but "the freedom of doing changes," i.e., how much control CMS has over its own codebase versus having to get changes approved/merged by another community's developers (e.g., ATLAS validating PanDA changes before hitting merge).
- **Complexity to evolve** (tentative name, discussed as possibly renamed, e.g. "layer complexity"): related to but not strictly identical to ownership — how hard it is to propagate a change through the layered architecture. Kenyi's initial view was that for PanDA (Strategy 1) low ownership correlates directly with high complexity to evolve, but he was less sure this holds for DIRAC, where medium development effort might still yield low long-term maintenance/complexity — a potential advantage over PanDA that Kenyi said needs to be double-checked. Marco initially suggested the two columns should be perfectly correlated but agreed to keep them separate given Kenyi's uncertainty about DIRAC.
- **Resource definition**: where sites/CEs are defined (Marco specifically asked for this, drawing an analogy to the factory XML). Discussed conclusion: factory entries would remain defined via the GlideinWMS factory in all strategies, but Strategies 1 and 2 would additionally require a mapping/duplication with PanDA queues, which Strategy 3 would not need.
- **Brokerage intent**: for Strategies 1/2 (PanDA-based), this refers to a first-level site filtering step requiring a mapping between ATLAS-style PanDA queues and GlideinWMS factory entries. Kenyi described needing "logical queues" in the PanDA brokerage plus a CMS-specific plugin (e.g., an initial filter sending work broadly to all Tier-2 sites), distinct from the ATLAS-specific brokerage/data-locality plugins that CMS would not reuse and would need to develop itself. A second-level filter (incorporating data-locality considerations) would then happen at the Harvester layer, which materializes the final, smaller set of desired sites injected into Condor (e.g., an initial logical list of ~20 sites narrowed to 5 actual desired sites). Strategy 3 would not have this Harvester layer and may not need a distinct "brokerage intent" step at all, or would need something analogous to WorkQueue's existing resource-control updater component (which periodically checks idle/running job counts per site) — Marco noted he has never liked that component, though acknowledged some form of it needs to be preserved, particularly since Monte Carlo job metadata is highly predictable (only the Lumi/event range changes between jobs), which he thought could support pushing all work upfront with late materialization; he was less sure this applies to data-processing workflows, which are less predictable and which he said he had not thought through as much.
- **Job execution / scheduling**: job execution refers to the actual job wrapper/environment code; scheduling refers to enforcing quotas and deciding which jobs to start. Both were noted as CMS-specific work needed under any strategy ("we need to prepare everything ourselves here").
- **Job bookkeeping**: discussed per strategy. Under Strategy 1, PanDA pilots are kept in full. Under an intermediate strategy, PanDA pilots are not actually run, but the pilot-job bookkeeping database is still needed. Kenyi noted that even under Strategy 3, part of PanDA's JEDI component (which handles logical job/job-intent tracking) would likely still need to be adapted or reused.

Marco pushed back that, based on the table as drafted, the intermediate Strategy 2 appeared to combine the downsides of both other strategies ("gets the worst of the two") without a clear offsetting benefit over Strategy 1, and said he did not particularly like either Strategy 1 or 2, seeing Strategy 3 as the more clearly viable direction to explore further.

Kenyi's response/argument for Strategy 2: it should be framed as a conservative starting point that can migrate to Strategy 3 later if Strategy 1 surfaces too many maintenance or complexity problems, since much of the development work done for Strategy 2 would be reusable rather than thrown away when moving to Strategy 3.

### Ease of onboarding new developers
Marco proposed adding a dimension (possibly folded into "complexity to evolve") capturing that lower complexity means new developers can ramp up faster — a real pain point in the current system, where he said a new developer can take months to become productive. Kenyi agreed this should be framed as helping not just current-developer maintenance load but also onboarding of future developers, and that Strategies 1/2 would score "high" on this friction (harder to onboard) while Strategy 3 would score "low" (easier).

### ATLAS precedent and PanDA-pilot mechanics
Marco observed that ATLAS/PanDA developers favor an approach equivalent to Strategy 1 because it is convenient for them: GlideinWMS is fully maintained by CMS/OSG, so ATLAS gets it "for free" without deploying anything themselves, whereas for CMS the same approach would mean maintaining both the GlideinWMS layer and the PanDA layer long-term. He suggested that if this were a genuinely shared/common solution, ATLAS developers might eventually contribute to GlideinWMS development themselves.

Kenyi clarified a further difference: in ATLAS's actual setup, PanDA pilots submit to fixed GlideinWMS factory entries tied to a fixed group of sites — there is no per-workflow site-selection decision made at the GlideinWMS/matchmaking layer itself, unlike CMS's current setup which relies on multiple queues and GlideinWMS reading class ads to decide where to provision. He also noted it is inherently simpler for ATLAS because the PanDA pilot already runs only ATLAS workloads, whereas for CMS an extra adaptation layer would be needed between the PanDA pilot and actual CMS workloads. Marco agreed this was a useful point to note ("the first part is all ATLAS, while for us it would be first part, then ATLAS, then CMS — a bit more complicated") and said he would use it when responding to future comparisons to ATLAS's experience.

### Main resource-provisioning concern
Marco reiterated his primary concern for any strategy: avoiding duplication of resource-provisioning/matchmaking logic (which the Condor negotiator already performs) and avoiding duplication of job bookkeeping across systems.

### HTCondor collaboration idea (data-locality matchmaking)
Kenyi raised, as something he recalled hearing Kevin discuss with others (not something the team is actively researching), an idea for evolving beyond the current "desired sites" mechanism: instead of editing a fixed desired-site list, inject available-data/block information as class ads into the Condor collector, so that HTCondor matchmaking expressions could dynamically determine whether a given site has the data needed for a given workflow, removing the need to manually/periodically update a static desired-site class. This would require an additional external component to inject such class ads and would likely need a feature request or discussion with HTCondor developers. Marco raised a concern about the potential size of the list of data blocks available at a site making this impractical unless injection were scoped/controlled (e.g., limited to blocks already known to Rucio/managed there). Marco suggested next week is not a good time to raise this with HTCondor developers, but that Kenyi could join the CMS/HTCondor bi-weekly meeting to discuss it there. Kenyi emphasized this idea goes beyond the scope of the current GlideinWMS integration talk and into longer-term evolving needs of whichever system (PanDA or DIRAC) is eventually adopted, and that its feasibility for PanDA/DIRAC specifically is unknown.

### State of evaluation and proof-of-concept work
Marco noted that nobody on the team has actually deployed PanDA yet — Alan has studied deployment more closely but has not deployed it himself — so a firm strategy recommendation isn't yet possible ("the evil is in the details"); the team has deliberately avoided placing heavy demands on PanDA/DIRAC developers' time given no long-term commitment has been made to either tool. Marco said he is currently running a scale test of his own GlideinWMS/HTCondor-based proof of concept, and that Dima has separately done his own proof of concept; Marco described this as a valuable, non-redundant experimentation phase across candidate tools, with no commitment yet to any one approach, and uncertainty about whether a CMS-led solution will ultimately be chosen.

### Broader/political framing: building vs. joining a community
Kenyi said he wished the broader effort (referred to as "the 11 [sic, unclear] ones") had been more explicit about the non-technical goals behind choosing an option — specifically, his understanding from conversations (not from a specific document) that whatever CMS adopts cannot serve CMS needs alone; it needs to have relevance to a broader scope/community. Marco agreed this is related to, but a slightly different point from, USCMS not wanting to pursue this work alone. Kenyi framed it as two paths: either CMS joins an existing community (PanDA/DIRAC), or CMS builds a new community around a CMS-led/GlideinWMS-based solution by explicitly designing it to be applicable to other experiments; he said joining an existing community is easier than building one, which is part of why the PanDA/DIRAC explorations are happening. He argued that convincing the experiment/funding agencies to adopt a CMS-built solution would require demonstrating it can build such a community — without that, he expects the outcome will default to PanDA or DIRAC. Marco asked who besides Kevin Kenyi had discussed the community-building idea with; Kenyi said that would be more a question for Andrea. They agreed Marco would raise it with Andrea, and that Kenyi and Andrea would separately discuss conclusions on Thursday.

## Open Questions

- Which strategy (1, 2, or 3) should be recommended for PanDA integration — not resolved; Marco leans toward exploring Strategy 3 further and dislikes both 1 and 2 as currently tabulated, while Kenyi's working proposal is to start with Strategy 2 as a stepping stone.
- How technically feasible is the proposed HTCondor-collaboration idea (injecting data-locality class ads into the collector for dynamic matchmaking), and would it need to be pursued as a formal feature request to HTCondor developers?
- How comparable/applicable are the PanDA and DIRAC strategy options, given DIRAC feedback so far has come only from a DIRAC developer (Federico) and not from CMS people, while PanDA feedback has come only from CMS people and not from ATLAS?
- Is "building a community" (making a CMS-led solution usable by other experiments) the right framing to include in the conclusions? Flagged as a question for Andrea.
- Will a CMS-led solution ultimately be selected, given political/funding considerations noted by Marco (USCMS not wanting to work in isolation)?
- How would data processing (as opposed to Monte Carlo production) fit the "push everything with late materialization" idea discussed for brokerage intent, given its less predictable metadata? Marco noted he had not thought this through.

## Related

[[glideinWMS]] · [[HTCondor]] · [[PanDA]] · [[DIRAC]] · [[WMAgent]] · [[Work Queue]] · [[CMS]] · [[ATLAS]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-10 14.43.43 New WM Dev team weekly meeting`)
