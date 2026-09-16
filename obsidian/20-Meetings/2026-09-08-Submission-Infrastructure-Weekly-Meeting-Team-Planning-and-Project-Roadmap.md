---
type: meeting
date: 2026-09-08
participants:
  - Marco Mascheroni
  - Antonio Perez-Calero Yzquierdo
topics:
  - mini-workshop for the WM team on Submission Infrastructure internals
  - CMS's position relative to DIRAC's own HTCondor-based matchmaking work
  - team task planning for Luis and Pablo
  - Factory-to-Kubernetes migration idea
  - renewable/extendable pilots at Fermilab
  - long-term monitoring and ITB dev environment
  - Archie integration and AI tooling
  - new Workload Management (WM) prototype status
  - Marco's potential move to the SI/WM Level 2 position
  - DM team succession candidates
  - PIC Tier-1 funding shortfall
---

# Submission Infrastructure Weekly Meeting — Team Planning and Project Roadmap

## Summary

Marco Mascheroni and Antonio Perez-Calero Yzquierdo held a wide-ranging planning discussion covering: a mini-workshop Marco is organizing for the WM (Workload Management) team to explain [[Submission Infrastructure]] (SI) internals; CMS's stance on DIRAC's own HTCondor-style matchmaking development; how to divide upcoming project work between Luis and Pablo now that the team is fully staffed; several candidate SI projects (Factory-to-[[Kubernetes]] migration, renewable/extendable pilots at Fermilab, reviving the ITB dev setup, long-term monitoring, [[Archie]]/AI integration); the status of Marco's new-WM prototype work, which is blocked on a DIRAC-side design document; Marco's consideration of moving into the SI/WM Level 2 role pending approval from Tulika; informal discussion of possible succession candidates for DM-related Level 2 work; and PIC's Tier-1 funding shortfall as motivation for opportunistic/free-resource work.

## Decisions / Conclusions

- CMS/SI will not adopt DIRAC's own HTCondor matchmaking implementation (observed in a DIRAC team presentation reusing CMS terminology). The group's shared understanding: SI's core responsibility is resource acquisition and matchmaking, which stays with [[HTCondor]]/[[glideinWMS]]; CMS is not interested in DIRAC's internal job-scheduling reimplementation, only in areas of genuine overlap (e.g. GPU handling).
- Pablo is recognized as the new main operator of the system, taking over core day-to-day operational tasks (deployments, debugging, testing new versions) that Luis had been doing; Luis, despite having joined only in March, is regarded as an already-senior/highly knowledgeable team member and will be given more freedom to work on forward-looking projects rather than routine operations.
- Two project ideas were identified as most promising for Luis to work on next: migrating the [[Factory]] to [[Kubernetes]], and exploring [[Archie]] integration (expanding the Condor monitoring data source Archie uses from job ClassAds to other SI components) together with AI tooling.
- Rationale for Factory-to-Kubernetes migration: part of the factory infrastructure (the OSG factory) already runs on the Tiger Kubernetes cluster, and another on the Glass Kubernetes cluster; moving the rest would consolidate on one technology, avoid the Puppet-based configuration burden (referencing the ~1 year it took to migrate Puppet profiles to Alma9), and align SI with the common infrastructure used by other CMS services being deployed on Kubernetes.
- The Fermilab renewable/extendable pilot idea (raised previously by Antonio after CHEP, and discussed with Jamie, who indicated this needs to be done site-by-side) is judged a good starting point: Fermilab is a large, whole-node site with Hyun Hu as a core SI team member with local knowledge; Antonio noted the main justification should be enabling longer-running jobs (current pilot/drain-based fragmentation is estimated ~95% efficient already, so scheduling-efficiency gains from renewable pilots alone would likely be small — one or two percentage points at most).
- Long-term monitoring (previously assigned to Florian roughly two years ago and never completed) and reviving the ITB dev deployment are identified as training/objective tasks, likely for Pablo (with Luis's assistance), to be incorporated into Pablo's probation-period objectives by adapting the same induction/objectives document previously used for Luis.
- New-WM prototype work (Marco's proof of concept: direct job submission from a DIRAC server to HTCondor) is currently paused, pending the DIRAC team's ADR (architecture decision record) describing the transformation system that SI will need to interface with.
- Francesco Brivio is expected to work with Marco on integrating the new WM with the SI layer; Marco characterized the Condor-submission part as comparatively straightforward, with the harder part being workload splitting/requirement estimation, which may require an iterative loop between job submission, monitoring results, and adjusting workflow parameters.

## Action Items

- [ ] Try to schedule the mini-workshop for the WM team during CERN computing week, preferring Tuesday afternoon (Wednesday morning as fallback) — Marco Mascheroni
- [ ] Ask Pablo whether he submitted a request to attend Condor Week — Marco Mascheroni
- [ ] Organize milestones and priorities across the open projects (Factory-to-Kubernetes, renewable/extendable pilots, ITB dev deployment, long-term monitoring, Archie integration) — Marco Mascheroni and Antonio Perez-Calero Yzquierdo
- [ ] Request that SI team members be added to the Archie users list — Marco Mascheroni / Antonio Perez-Calero Yzquierdo
- [ ] Adapt Luis's induction/objectives document to define Pablo's probation-period objectives, including long-term monitoring and ITB dev deployment — Antonio Perez-Calero Yzquierdo

## Discussion

- The mini-workshop originated from Alan, after the WM team's discussions with the DIRAC team at CERN surfaced how little the WM group knows about SI/glideinWMS details; Marco intends to run it as an informal whiteboard/blackboard session rather than a slide-based presentation.
- Antonio observed that CMS's work has historically been well factorized from other WLCG/DIRAC efforts, which has helped the team focus, though it also means other groups (and even parts of CMS) often treat SI as a "black box."
- On GPUs/heterogeneous computing: Antonio noted, from reviewing conference material, that CMS/SI is already ahead of some other groups' current GPU work.
- Archie is currently understood to be mostly focused on operations and job debugging via Condor job information (ClassAds); expanding its monitoring data source to cover other SI components was raised as a natural next step. Marco separately raised the idea of storing meeting summaries (not full transcripts) in a repository to make them available to AI coding/writing assistants.
- On defragmentation: Antonio cautioned that if pilots are made effectively infinite in lifetime, a "defrag daemon" would eventually be needed to drain/select machines to make room for larger jobs, which is conceptually a similar problem to what renewable pilots aim to solve; the primary motivation for either approach should be enabling jobs that need to run longer than the current drain-based fragmentation allows, not incremental scheduling-efficiency gains.
- Regarding project timelines shown by Liz at a recent computing-week general meeting (covering Analysis Facilities, DM, and WM project timelines): Marco and Antonio recognized the WM timeline's origin but were unclear which team is behind the Analysis Facilities timeline, and Antonio noted he had not been involved in preparing the computing-week agenda.
- Marco reported he has proposed moving into the SI/WM Level 2 position; this requires approval from Tulika (his funding-line manager) and subsequently from the level-one coordinators (Stefan and Daniele). He sent an email to Tulika (drafted with input from James) the previous Friday and was still awaiting her reply as of this meeting. Marco stated he expects to remain roughly 75% dedicated to SI operations/development regardless of the outcome, continuing informal glideinWMS/CRAB development work he has already been doing.
- Regarding succession for DM-related Level 2 work: no decision was made. Eric Bandering was mentioned as a name that has circulated; Diego and Dasan currently do DM development work. This was discussed informally and remains unresolved.
- Antonio mentioned that PIC's Tier-1 project has only had roughly one-third of its requested funding allocated, which motivates pursuing opportunistic/free compute resources (referenced in the context of ongoing BSC-related work) as an offset, since such resources still require effort even if free in CPU/electricity terms.

## Open Questions

- Whether renewable/extendable pilots and/or smarter defragmentation would provide meaningful efficiency gains beyond enabling longer-running jobs — not resolved; Antonio's view is that the efficiency upside alone is likely small given current ~95% pilot efficiency.
- Which team is responsible for the "Analysis Facilities" project timeline shown at the computing-week general meeting.
- Who will take on DM-related Level 2 responsibilities going forward — discussed informally without conclusion.
- Outcome of Marco's request to Tulika regarding the SI/WM Level 2 move — pending at the time of this meeting.

## Related

[[Submission Infrastructure]] · [[HTCondor]] · [[glideinWMS]] · [[DIRAC]] · [[Kubernetes]] · [[Factory]] · [[Factory Operations]] · [[Workload Management]] · [[WMAgent]] · [[CRAB]] · [[CMS]] · [[CERN]] · [[GPU]] · [[Heterogeneous Computing]] · [[Archie]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-08 11.27.06 Submission Infrastructure Weekly Meeting`)
