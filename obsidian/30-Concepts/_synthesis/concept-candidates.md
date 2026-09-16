# Concept Candidates — Knowledge Synthesis Discovery

Discovery pass date: 2026-09-16
Scope: `obsidian/20-Meetings/` (123 Markdown meeting notes, 2025-12-11 through
2026-09-16), read in full. Deeper sources under `40-References/`,
`60-Presentations/`, `70-Proceedings/`, and `80-Code-Index.md` were consulted
only by directory listing / title, not opened in full, except where noted.
This is a **discovery checkpoint**, not synthesized knowledge. No files under
`obsidian/30-Concepts/` were created or modified.

## Method

The meeting corpus was read by four parallel research passes grouped by
recurring theme (visible from meeting titles and a wikilink-frequency scan
of all `[[...]]` links in `20-Meetings/*.md`):

- **DiracX / future-WMS thread** (21 meetings, Dec 2025–Sep 2026)
- **GlideinWMS / OSG Factory Ops / pilot lifecycle / site-token migration**
  (31 meetings, Feb–Sep 2026)
- **HTCondor fundamentals / CPU efficiency / matchmaking / CWL prototypes**
  (16 meetings, Mar–Sep 2026)
- **Weekly SI / New WM Dev Team / organizational meetings** (52 meetings,
  Dec 2025–Sep 2026)

Wikilink frequency across the corpus (top entities): `[[HTCondor]]` 133,
`[[glideinWMS]]` 121, `[[CMS]]` 104, `[[Submission Infrastructure]]` 86,
`[[DIRAC]]` 75, `[[Pilot Jobs]]` 65, `[[DIRACX]]` 61, `[[Factory Operations]]`
58, `[[CRAB]]` 50, `[[Workload Management]]` 47, `[[Rucio]]` 41. Per
`SYNTHESIS.md` principle 2, frequency alone did **not** determine candidacy —
it was used only to prioritize where to look.

Seven candidates are proposed below. Several frequently-mentioned topics
were deliberately **not** proposed as standalone candidates; see
"Considered and not proposed" at the end, with rationale.

---

## Candidate 1: CMS's Adoption of DiracX as the Future Workload Management System

**Status:** approved
**Readiness:** ready for synthesis, with the explicit caveat that the subject
is an active, fast-moving transition as of the corpus end date (2026-09-16).
The note must clearly separate "decided" from "still being designed."

### Why durable

This is the single largest and most consequential architectural thread in
the entire corpus (21+ dedicated meetings plus mentions across nearly every
New WM Dev Team and SI weekly meeting from March 2026 onward). It represents
a top-level, collaboration-level decision (presented at the March 2026 CMS
collaboration meeting) with a defined rationale, a new team structure built
around it, and a growing set of concrete integration/architecture questions.
It meets several of the SYNTHESIS.md bars simultaneously: multi-meeting
evidence, an important architectural role, an established organizational
decision, and recurring unresolved design questions.

### Current understanding vs. history (must be preserved, not collapsed)

- **Dec 2025–Feb 2026**: CMS was still exploring a **CMS-built** HL-LHC WMS
  (global work queue, "microagents") as one option; DIRAC was only a
  reference point for reusable ideas, not a chosen direction
  (`2025-12-22-HTCondor-and-CMS-WMS-for-HL-LHC.md`,
  `2026-02-19-CMS-WMS-Architecture-Discussion.md`).
- **~Early May 2026**: The decision to adopt DIRAC/DiracX had *already been
  made* (per Stephan Lammel, presented ~3 weeks earlier at the March CMS
  collaboration meeting); the CMS-native option's "reservation" was released
  (`2026-05-29-Submission-Infrastructure-Candidate-Interview-and-DIRAC-Decision-Debrief.md`).
  A **communication gap** is explicitly documented: this was not yet common
  knowledge among CMS computing colleagues weeks later, surfacing at CHEP
  corridor conversations, which prompted Stephan Lammel to start a standing
  status page (same source; corroborated by
  `2026-09-08-Submission-Infrastructure-Weekly-Meeting-Team-Planning-and-Project-Roadmap.md`
  team-roadmap discussion naming DiracX integration the top SI priority).
- **June 2026**: Hands-on evaluation (Valentin Kuznetsov) shows DiracX
  cannot yet run standalone — it wraps a running legacy DIRAC backend
  (`2026-06-24-DiracX-Evaluation-and-WMS-Integration-Planning.md`).
- **July 2026**: A DIRAC/DiracX hackathon marks the start of active CMS
  engagement; a dedicated **New WM Dev Team** (distinct from the existing
  Submission Infrastructure team) begins weekly meetings, sprint cadence
  with the upstream DIRAC/DiracX team, and architecture-decision-record
  (ADR) tracking (`2026-07-08-DiracX-InterSeed-HTCondor-GAHP-BLAHP-Discussion.md`
  through `2026-07-23-DIRAC-DiracX-Sprint-Review-and-Retrospective-Meeting.md`).
- **Aug–Sep 2026**: First working DiracX→HTCondor submission prototype
  (`2026-08-14-DiracX-Interim-HTCondor-Job-Submission-Walkthrough.md`);
  Kubernetes deployment and sandbox-upload work against a "Test18" prototype
  (`2026-09-01-DiracX-Proof-of-Concept-Update-and-DMWM-Convenership-Discussion.md`,
  `2026-09-15-Test18-DiracX-CMS-Prototype-Sandbox-Upload-Walkthrough.md`);
  six upstream DIRAC/DiracX ADRs repeatedly announced as imminent and
  repeatedly slipping (July→mid-Aug→end-Aug→mid-Sep, still not landed by
  `2026-09-16-WM-Retreat-and-DIRAC-Session-Planning.md`), with CMS
  explicitly deferring "serious designing" until they land.
- Separately, `2026-09-09-Conditions-Preparation-Workshop-2026-Validation-Tier0-and-Future-WMS.md`
  documents that WMAgent/"WM4" was reviewed 2024–2025, judged not
  sustainable for Phase 2, and has been **frozen since September 2025**,
  with DiracX-based replacement targeted for Tier0+MC+reprocessing+CRAB, an
  earliest-usable-system estimate of mid-2027, and a CSA 2028 checkpoint.
  This is an important independent corroboration of the transition's stated
  urgency and should be checked against `60-Presentations/WM_Conditions_Workshop_2026.pdf`
  during synthesis (not opened during this discovery pass).

### DIRAC vs. DiracX (must be preserved as a distinct sub-point)

DiracX is described as a from-scratch **re-engineering**, not a port, of
DIRAC (fstagni, `2026-07-14-DiracX-InterSeed-and-HTCondor-Access-Point-Discussion.md`).
DIRAC is the established, multi-VO system historically used heavily by
LHCb; it built its own pilot ecosystem separate from HTCondor roughly 20
years ago. DIRAC/DiracX developers attend CMS meetings as representatives
of the whole DIRAC consortium, not of LHCb. CMS's sudden, large manpower
contribution is noted as disproportionate relative to other VOs
(`2026-07-30-WM-Dev-Team-Weekly-DiracX-DIRAC-Deployment-and-Integration-Strategy.md`,
Liz Sexton-Kennedy).

### Integration points (candidate relationships — see Relationships below)

- InterCEde and HTCondor pilot submission: InterCEde was proposed as the DIRAC-to-CE interface, with an approach advocated to reuse HTCondor for pilot submission to CEs, rather than building a separate submission mechanism. This is distinct from user-job submission, where DIRACX is expected to submit jobs via condor_submit to SI Access Points. The InterCEde/HTCondor pilot-submission idea was discussed in 2026-07-08, 2026-07-14, 2026-07-30, and 2026-09-03, but appears to have been dropped rather than remaining an active architecture question.
- **glideinWMS/pilots**: the team explicitly converged on *not* adding
  direct links between glideinWMS/HTCondor and DiracX components beyond
  HTCondor access points, preserving modularity
  (`2026-07-15-New-WM-Dev-Team-Weekly-Meeting-DiracX-Architecture-Deep-Dive.md`).
  Where CMS "job materialization" (turning DiracX task-DB rows into
  HTCondor jobs) should live — core DIRAC feature, DiracX plugin, or
  standalone glideinWMS-side component — is explicitly unresolved
  (same source).
- **Rucio**: data-management operations route through DIRAC's Request
  (Management) System as the bridge to Rucio; where output registration to
  Rucio/DBS happens (worker-node vs. centralized) is an unresolved "hot
  topic" flagged from a hackathon, with Valentin Kuznetsov warning against
  uncontrolled worker-node calls (citing a past DAS-like incident)
  (`2026-07-15`). `2026-07-17-Rucio-Caching-Meta-Job-Terminology-and-ADR-Recap.md`
  documents a DIRAC-side terminology effort distinguishing "direct task"
  vs. "meta job," not yet finalized.

### Disagreements / open questions (preserve, do not resolve)

- **Integration-test strategy**: explicit, named disagreement at
  `2026-07-30` — Valentin Kuznetsov wants DIRAC+DiracX connected now for
  fast feedback; Alan Malta Rodrigues/Andrea Piccinelli/Marco Mascheroni
  lean toward building DiracX-only components first to avoid throwaway work
  on DIRAC pieces slated for ADR-driven replacement. The meeting ends with
  the participants stating they are "not on the same page."
- Job-materialization placement (three options, unresolved).
- CWL vs. HTCondor JDL/ClassAd translation responsibility — see Candidate 6.
- Storage: SeaweedFS/Helm chart incompatibility with CMS's Kubernetes setup
  forced a fork (`2026-08-27-New-WM-Dev-Team-Weekly-Meeting-DiracX-Storage-Helm-Charts-and-Token-Support.md`);
  a live disagreement about whether DIRAC's general-purpose flexibility
  (supporting many optional backends for other VOs) is worth the added
  burden for CMS (Kevin Lannon argues yes).
- No mechanism observed yet in the DIRAC framework for secrets management
  (flagged gap, `2026-07-15`).

### Sources

- `2025-12-22-HTCondor-and-CMS-WMS-for-HL-LHC.md`
- `2026-02-19-CMS-WMS-Architecture-Discussion.md`
- `2026-05-29-Submission-Infrastructure-Candidate-Interview-and-DIRAC-Decision-Debrief.md`
- `2026-06-24-DiracX-Evaluation-and-WMS-Integration-Planning.md`
- `2026-07-08-DiracX-InterSeed-HTCondor-GAHP-BLAHP-Discussion.md`
- `2026-07-09-DIRAC-DiracX-Sprint-Review-and-Planning-Meeting.md`
- `2026-07-14-DiracX-InterSeed-and-HTCondor-Access-Point-Discussion.md`
- `2026-07-15-New-WM-Dev-Team-Weekly-Meeting-DiracX-Architecture-Deep-Dive.md`
- `2026-07-16-DIRAC-DiracX-Backlog-Grooming-and-Estimation-Meeting.md`
- `2026-07-16-WM-Dev-Team-Weekly-DiracX-Ticket-Prioritization-and-ADR-Review-Planning.md`
- `2026-07-17-Rucio-Caching-Meta-Job-Terminology-and-ADR-Recap.md`
- `2026-07-23-DIRAC-DiracX-Sprint-Review-and-Retrospective-Meeting.md`
- `2026-07-30-WM-Dev-Team-Weekly-DiracX-DIRAC-Deployment-and-Integration-Strategy.md`
- `2026-08-13-DIRAC-DiracX-In-Progress-Review-and-Backlog-Triage-Meeting.md`
- `2026-08-14-DiracX-Interim-HTCondor-Job-Submission-Walkthrough.md`
- `2026-08-27-New-WM-Dev-Team-Weekly-Meeting-DiracX-Storage-Helm-Charts-and-Token-Support.md`
- `2026-09-01-DiracX-Proof-of-Concept-Update-and-DMWM-Convenership-Discussion.md`
- `2026-09-03-DIRAC-DiracX-Sprint-Review-and-Planning-Meeting.md`
- `2026-09-09-DIRAC-DiracX-Sprint-Review-Meeting.md`
- `2026-09-09-Conditions-Preparation-Workshop-2026-Validation-Tier0-and-Future-WMS.md`
- `2026-09-15-Test18-DiracX-CMS-Prototype-Sandbox-Upload-Walkthrough.md`
- `2026-09-16-WM-Retreat-and-DIRAC-Session-Planning.md`
- Corroborating (org-level) : `2026-07-13-New-WM-Dev-Team-Weekly-Meeting-Effort-Roundtable-and-Use-Case-Boundaries.md`,
  `2026-09-08-Submission-Infrastructure-Weekly-Meeting-Team-Planning-and-Project-Roadmap.md`
- Not yet inspected, likely relevant: `60-Presentations/20251216 New CMS WM_ Discussion with HTCondor.pdf`,
  `60-Presentations/Exploring Collaboration Between HTCondor and DiracX-4.pdf`,
  `60-Presentations/20260610_Evolving_the_CMS_Submission_Infrastructure.pdf`,
  `60-Presentations/WM_Conditions_Workshop_2026.pdf`

### Relationships

- Depends on / motivates **Candidate 5** (Submission Infrastructure team
  structure — the "New WM Dev Team" exists because of this transition).
- Explicitly designed to *keep* **Candidate 2** (glideinWMS Factory/Frontend)
  as the execution/pilot layer underneath DiracX (see Candidate 2's own
  sources, e.g. `2026-07-08-GlideinWMS-Meeting.md` era discussion).
- Shares an unresolved design tension with **Candidate 6** (CWL prototype):
  both concern how CMS's job/workflow definitions map onto DiracX/DIRAC
  abstractions.

---

## Candidate 2: GlideinWMS Pilot-Based Resource Provisioning (Factory/Frontend Architecture and Pilot Lifecycle)

**Status:** approved
**Readiness:** ready for synthesis — this is the most stable, best-corroborated
architectural concept in the corpus, repeatedly re-explained consistently
across independent training/walkthrough sessions over seven months.

### Why durable

Highest-frequency technical entities in the corpus (`glideinWMS` 121,
`Pilot Jobs` 65, `Factory Operations` 58, `Factory` 23) backed by no fewer
than six dedicated architecture/lifecycle walkthrough meetings plus 20+
weekly "OSG Factory Ops" operational meetings. This is CMS's established,
in-production resource-provisioning mechanism, explicitly slated to
*remain* the execution/pilot layer even as the WMS above it changes
(Candidate 1).

### Current understanding

Three logical components: **glidein/pilot** (a job that, once landed on a
worker node, starts `condor_startd`/`condor_master`, joining the HTCondor
pool), the **Factory** (holds per-site "entries," is VO-agnostic/"dumb," a
"waiter" that does not decide glidein volume), and the **Frontend**
(performs matchmaking against user jobs/VO credentials, one per experiment,
the "brain"). CMS operates 3 of 4 known factories (Fermilab: Tier-1-only,
reliability-motivated; "Tiger"/OSG: CMS + other VOs, run by Jeff Dost;
CERN: all CMS sites, run by Luis Simas) — Factories are explicitly shared
across VOs while Frontends are one-per-experiment
(`2026-09-07-GlideinWMS-Factory-and-Frontend-Architecture-Follow-up.md`).
Communication is **pull-based**: the Frontend polls a Factory-run HTCondor
collector roughly every 10 minutes; there is no push
(`2026-06-23-GlideinWMS-Architecture-Training-and-Site-Token-Migration-Status.md`,
`2026-09-15-GlideinWMS-Token-Authentication-JINR-Pressure-and-WMAgent-Condor25-Prep.md`).
Matchmaking happens in two independent stages — Frontend↔entries, then
Condor negotiator↔pilot — so there is no guarantee a specific job's demand
signal lands on the specific pilot it triggered
(`2026-05-26-GlideinWMS-Architecture-Walkthrough.md`).

The full pilot lifecycle (submission via Condor-G → CE queueing →
`glidein_startup.sh` validation/download → `condor_startd` registration →
negotiator match → job execution → retirement at `GLIDEIN_ToRetire`/death
at `GLIDEIN_ToDie`) is documented in detail across
`2026-05-26-GlideinWMS-Architecture-Walkthrough.md`,
`2026-05-27-GlideinWMS-Pilot-Lifecycle-Walkthrough.md`, and restated for a
new hire in `2026-09-04-GlideinWMS-and-HTCondor-Architecture-Walkthrough.md`.

### Evolution / correction across sources

Terminology and diagrams were repeatedly found to be outdated or
inconsistent when re-explained to new operators: an older
pilot-contains-execution-point diagram had the containment backwards
(corrected `2026-09-08-GlideinWMS-Frontend-Training-Terminology-and-Infrastructure-Walkthrough.md`);
old proxy-based mutual-auth diagrams were declared fully obsolete, replaced
by a three-token model (`2026-09-15-GlideinWMS-Token-Authentication-JINR-Pressure-and-WMAgent-Condor25-Prep.md`
— see Candidate 3). This pattern of repeated re-explanation itself signals
this is durable, foundational knowledge that the team must actively
maintain and re-teach, not settled-and-static trivia.

### Disagreements / open questions

- Jeff Dost vs. Marco Mascheroni on whether "spread" and "retire-time"
  interact additively — unresolved (`2026-07-14-OSG-Factory-Ops-Meeting.md`).
- Whether over-provisioning from multi-entry site matching is a bug or a
  benefit — unresolved, treated as an open opinion
  (`2026-07-24-GlideinWMS-Factory-Architecture-Walkthrough.md`).
- "Immortal pilots" (removing wall-time limits, relying on draining
  instead) proposed as an efficiency experiment with three named
  "showstopper" concerns (fragmentation, credential expiration, accounting
  gaps) — no decision to implement
  (`2026-09-15-OSG-Factory-Ops-Meeting.md`; also touches Candidate 4).

### Sources

- `2026-02-17-OSG-Factory-Ops-Meeting.md` through `2026-09-15-OSG-Factory-Ops-Meeting.md`
  (20 OSG Factory Ops meetings — operational corroboration, not individually
  enumerated here; see the GlideinWMS digest pass for the full list)
- `2026-03-10-GlideinWMS-Integration-PanDA-DIRAC-Slide-Prep.md`
- `2026-04-01-GlideinWMS-Meeting.md`, `2026-04-22-GlideinWMS-Meeting.md`,
  `2026-06-24-GlideinWMS-Meeting.md`, `2026-07-08-GlideinWMS-Meeting.md`,
  `2026-07-29-GlideinWMS-Meeting.md`, `2026-09-09-GlideinWMS-Meeting.md`
- `2026-05-26-GlideinWMS-Architecture-Walkthrough.md`
- `2026-05-27-GlideinWMS-Pilot-Lifecycle-Walkthrough.md`
- `2026-06-23-GlideinWMS-Architecture-Training-and-Site-Token-Migration-Status.md`
- `2026-07-24-GlideinWMS-Factory-Architecture-Walkthrough.md`
- `2026-09-04-GlideinWMS-and-HTCondor-Architecture-Walkthrough.md`
- `2026-09-07-GlideinWMS-Factory-and-Frontend-Architecture-Follow-up.md`
- `2026-09-08-GlideinWMS-Frontend-Training-Terminology-and-Infrastructure-Walkthrough.md`
- `2026-03-04-CMS-Computing-Model-Submission-Infrastructure-Onboarding.md`
  (frames the pilot model as "pull/late-binding" vs. "push/vacuum" at the
  computing-model level — links to Candidate 5)
- Not yet inspected, likely relevant: `60-Presentations/Exploiting Kubernetes to Simplify the Deployment and Management of the Multi-purpose CMS Pilot Job Factory-6.pdf`,
  `60-Presentations/Improving GlideinWMS Factory Compute Resource Configuration with Automation Tools.pdf`

### Relationships

- The execution layer that **Candidate 1** (DiracX) is explicitly designed
  to sit on top of, not replace.
- Carries **Candidate 3** (site/token migration) as an operational
  workstream against this same architecture.
- The "overload"/oversubscription mechanism inside this architecture is a
  concrete lever discussed under **Candidate 4** (CPU efficiency).

---

## Candidate 3: Site/Token Authentication Migration for Pilot Submission (SciTokens)

**Status:** approved
**Readiness:** ready for synthesis — has a clear, well-evidenced start,
middle (with named regressions), and a near-complete end state as of the
latest meetings.

### Why durable

A discrete, multi-month infrastructure migration with a defined technical
driver, tracked consistently across ~15 meetings from March through
September 2026, with concrete before/after states, named regressions and
fixes, and an explicit "this is now the baseline" teaching moment at the
end. This is an established operational/security change to core
infrastructure, not a passing mention.

### Current understanding and evolution

Migration from grid-proxy (X.509/GSI) to site-token (JWT/SciToken)
authentication for pilot submission to Compute Elements. Drivers: a
WLCG-coordinated milestone timeline (M1–M9, referenced with explicit
uncertainty about currency — `2026-03-26-1005-GlideinWMS-Entry-Troubleshooting-and-Site-Token-Migration.md`);
HTCondor 3.11's removal of an old "continue if no proxy" fallback,
forcing real token support (`2026-06-30-OSG-Factory-Ops-Meeting.md`); and a
since-deprioritized FNAL CA change once believed to force the timeline
within a year, later clarified as unrelated
(`2026-06-30-OSG-Factory-Ops-Meeting.md`, `2026-07-07-OSG-Factory-Ops-Meeting.md`).

Timeline: inventory of proxy-only entries requested April 2026
(`2026-04-01-GlideinWMS-Meeting.md`); deliberate CMS holdoff on
Condor-CE entries pending non-CMS rollout (`2026-04-21`, `2026-04-28`
OSG Factory Ops meetings); a HTCondor 3.11 regression removing 3.10's
dual-credential workaround caused breakage at MIT and IN2P3
(`2026-06-23-OSG-Factory-Ops-Meeting.md`, `2026-06-24-GlideinWMS-Meeting.md`);
a 3.11.4 front-end credential-shipping bug (only one of two credentials
sent per group) caused a hold on upgrades and a rollback to grid-proxy for
two of three MIT CEs (`2026-07-07-OSG-Factory-Ops-Meeting.md`); Condor-CE
site-token work declared "complete" with focus shifting to ARC/EGI sites
(no OSG-style RPM equivalent, mapping unclear) by mid-July
(`2026-07-14-OSG-Factory-Ops-Meeting.md`, `2026-07-21`, `2026-07-28`); by
early September all known factories including CERN had migrated to 3.11,
though the CMS Frontend itself was still on 3.10 in production, and the
overload/oversubscription logic was found broken under the new 3.11
protocol (`2026-09-09-GlideinWMS-Meeting.md`); by mid-September the
three-token model (Frontend↔Factory, Factory↔site, worker-node↔collector)
is taught to a new operator as the current, normalized baseline, with
proxy-based auth framed as purely historical
(`2026-09-15-GlideinWMS-Token-Authentication-JINR-Pressure-and-WMAgent-Condor25-Prep.md`).

A separate, concurrently-tracked effort — **WMAgent Condor25
compatibility testing** — surfaced in the same September meeting: HTCondor
now rejects `condor_submit` run as the reserved OS user `condor`, requiring
WMAgent to submit as `cmst1`/`cmsdataops` instead; a WMAgent 0.9 patch and
parallel Condor 24-vs-25 comparison tests were planned. This is related but
distinct from the site-token migration itself and should not be merged
into it without preserving that distinction.

### Disagreements / open questions

- No outright disagreement documented, but repeated technical surprises
  (3.11 regressions) suggest the migration was executed more cautiously
  than originally planned, and EGI/ARC-site mapping remained an open gap
  as of late July 2026.
- JINR's low core utilization was initially suspected to be
  migration-related but was determined to be a demand-side (Frontend
  "pressure") issue, not an authentication problem
  (`2026-09-15-GlideinWMS-Token-Authentication-JINR-Pressure-and-WMAgent-Condor25-Prep.md`)
  — this distinction should be preserved rather than conflated.

### Sources

- `2026-03-26-1005-GlideinWMS-Entry-Troubleshooting-and-Site-Token-Migration.md`
- `2026-04-01-GlideinWMS-Meeting.md`
- `2026-04-21-OSG-Factory-Ops-Meeting.md`, `2026-04-28-OSG-Factory-Ops-Meeting.md`
- `2026-05-19-OSG-Factory-Ops-Meeting.md`, `2026-05-27...` (LPC/Syracuse status,
  via GlideinWMS Pilot Lifecycle Walkthrough meeting)
- `2026-06-23-GlideinWMS-Architecture-Training-and-Site-Token-Migration-Status.md`,
  `2026-06-23-OSG-Factory-Ops-Meeting.md`
- `2026-06-24-GlideinWMS-Meeting.md`
- `2026-06-30-OSG-Factory-Ops-Meeting.md`
- `2026-07-07-OSG-Factory-Ops-Meeting.md`
- `2026-07-14-OSG-Factory-Ops-Meeting.md`, `2026-07-21-OSG-Factory-Ops-Meeting.md`,
  `2026-07-28-OSG-Factory-Ops-Meeting.md`
- `2026-09-09-GlideinWMS-Meeting.md`
- `2026-09-15-GlideinWMS-Token-Authentication-JINR-Pressure-and-WMAgent-Condor25-Prep.md`
- Not yet inspected, likely relevant: `60-Presentations/20220401 Token Migration - Submission Infrastructure.pdf`,
  `20-Meetings/CMS Token Transition.pdf`

### Relationships

- An operational workstream layered on **Candidate 2**'s architecture.
- Loosely time-correlated with, but causally independent of, the staffing
  changes in **Candidate 5**.

---

## Candidate 4: CMS CPU / Resource Efficiency as a Recurring Cross-Team Problem

**Status:** approved
**Readiness:** ready for synthesis as an *open, unresolved* problem —
the note should present current understanding and explicitly state that no
CMS-wide efficiency metric or resolution exists yet, per SYNTHESIS.md's
instruction to state when evidence is insufficient rather than manufacture
a resolution.

### Why durable

A recurring, escalating operational and strategic concern with
independent evidence lines converging in September 2026: a scrutiny-group
compliance requirement, a live site-debugging case study, a CMS-wide
cross-team strategy meeting, and a purpose-built monitoring effort. This
reflects an established organizational problem with real operational
consequences (external LHCC/WLCG scrutiny), not a one-off technical
complaint.

### Current understanding

- **PnR "bad put" study** (`2026-08-12-PnR-Failed-Job-CPU-Waste-Bad-Put-Discussion.md`):
  a WLCG scrutiny group now requires experiments, not just sites, to
  self-report failed-job resource waste. Marco Mascheroni proposes "bad
  put" (wasted wall time, not CPU%) as the more correct metric, split into
  Condor-restart bad put vs. WMAgent-retry bad put.
- **CNAF live debugging** (`2026-09-02-HTCondor-Shadowing-Session-CNAF-Efficiency-Debugging.md`):
  CNAF showing ~40% idle cores against a Tier-1-wide 93% efficiency (target
  96–98%); "pilot retiring" (near-end-of-life pilots refusing new work,
  tied to ~2-day wall-time job requests) identified as a leading suspect;
  memory exhaustion ruled out.
- **CMS-wide strategy meeting** (`2026-09-09-CMS-OC-Weekly-Meeting-CPU-Efficiency-Strategy.md`,
  chaired by Stephan Lammel): explicitly **no agreed efficiency metric
  exists** (raw utilization vs. CPU-cycle/instruction throughput vs.
  events/cycle debated). Candidate causes discussed: job startup/shutdown
  overhead (~15% of a 15–20 min job), remote I/O vs. data pre-placement
  trade-offs, poor resource-requirement characterization (jobs requesting
  ~2x actual memory), low-efficiency analysis/user jobs (~30% of
  resources), and CPU-model heterogeneity. No decision reached; deferred to
  smaller working groups.
- **Monitoring precedent**: pilot-monitoring dashboards
  (`2026-05-29-Pilot-Monitoring-and-Efficiency-Presentation-Prep.md`) had
  already found site-reported efficiency (70%) diverging from
  payload-level efficiency (46%), attributed to the overload/oversubscription
  compensation mechanism inside glideinWMS (Candidate 2) — this is the
  clearest concrete link between the efficiency problem and the
  oversubscription lever.
- **Concrete technical response**: same day as the CMS-OC strategy meeting,
  Marco raised HTCondor 26.0's "Common Input Transfers" job-bundling
  feature with HTCondor developer Jaime Frey as a candidate mitigation
  (`2026-09-09-CMS-Submission-Infrastructure-Meeting-Data-Aware-Matchmaking-Immortal-Pilots-Condor24.md`).

### Disagreements / open questions

- No agreed CMS-wide efficiency metric (explicit, `2026-09-09-CMS-OC-Weekly-Meeting-CPU-Efficiency-Strategy.md`).
- Whether to raise per-pilot memory (Stephan Lammel's proposal) or increase
  pilot/slot size (Antonio Pérez-Calero Yzquierdo's proposal) is disputed
  and unresolved in the same meeting.
- GPU/heterogeneous resources are acknowledged as a coming additional
  dimension to this problem ("soon — GPU," James Letts) but not yet
  addressed — see "Considered and not proposed" below regarding GPU
  MIG/MPS.

### Sources

- `2026-05-29-Pilot-Monitoring-and-Efficiency-Presentation-Prep.md`
- `2026-08-12-PnR-Failed-Job-CPU-Waste-Bad-Put-Discussion.md`
- `2026-09-02-HTCondor-Shadowing-Session-CNAF-Efficiency-Debugging.md`
- `2026-09-09-CMS-OC-Weekly-Meeting-CPU-Efficiency-Strategy.md`
- `2026-09-09-CMS-Submission-Infrastructure-Meeting-Data-Aware-Matchmaking-Immortal-Pilots-Condor24.md`
- Corroborating (overload mechanism origin): `2026-04-10-Overload-Enabled-Fix-Planning-and-Condor-Overview-Training.md`
- Not yet inspected, likely relevant: `20-Meetings/20260525_CHEP26_CMS_SI_Efficiency.pdf`,
  `60-Presentations/Memory Utilisation and Unused Cores.pdf`

### Relationships

- Consumes the oversubscription/"overload" mechanism from **Candidate 2**.
- Shares a meeting and a proposal-stage overlap with **Candidate 6**
  (data-aware matchmaking) and the "Immortal Pilots" proposal, but these
  are distinct proposed mitigations, not the same concept — do not merge.

---

## Candidate 5: Submission Infrastructure — Scope, Computing-Model Role, and Team Structure

**Status:** approved
**Readiness:** ready for synthesis for the computing-model/scope portion
(well-anchored in a single canonical onboarding source, corroborated
elsewhere); the team-structure portion is durable but changes fast enough
(three staffing transitions within the corpus period) that the note should
be explicit about "as of September 2026."

### Why durable

`[[Submission Infrastructure]]` is the second-most-referenced entity in the
corpus (86 occurrences) and is the umbrella under which nearly every other
candidate here sits operationally. A single, high-quality onboarding
meeting gives a canonical, deliberately-taught explanation of what SI is
and is not, and this framing is consistently corroborated (not
contradicted) across dozens of weekly meetings.

### Current understanding

Per `2026-03-04-CMS-Computing-Model-Submission-Infrastructure-Onboarding.md`
(Antonio Pérez-Calero Yzquierdo and Marco Mascheroni onboarding new hire
Luis Simas): SI's scope is **acquiring and allocating compute** (via
Compute Elements), explicitly *not* data movement/storage. CMS uses a
**pull/late-binding "pilot model"** (contrast: push/vacuum models). Tier-0
(repack/prompt reconstruction) has the highest operational priority because
data loss there is irreversible, unlike recoverable delays in MC
production or analysis. Production (~80% of resources, driven by
WMAgent/RequestManager) is distinguished from analysis (~400 physicists via
CRAB). The control plane is high-availability, CERN-primary/Fermilab
-secondary, backed by 3–4 redundant glideinWMS factories. "Tier-0" is
explicitly flagged as an overloaded term (place / function / team).

Team structure: a small (~5 FTE-equivalent) Submission Infrastructure team,
co-led by Antonio Pérez-Calero Yzquierdo and Marco Mascheroni, distinct
from the "New WM Dev Team" (Candidate 1) and from multi-experiment "Factory
Operations" (Candidate 2, led on the US/OSG side by Jeff Dost). Staffing
changed substantially within the corpus period: Luis Simas joined as
factory-ops hire March 2026; Florian Von Cube departed for KIT around May
2026 (retaining a bounded glideinWMS/DiracX side-project); Pablo Izquierdo
Gonzalez joined September 2026 as HTCondor/frontend operator, restoring
"nominal staffing" (`2026-09-03-Submission-Infrastructure-Weekly-Meeting.md`).
A **WM Level 2 Transition** — Marco Mascheroni moving into the CMS
Workload Management Level-2 coordinator role while retaining ~75% time on
SI — is documented as pending approval as of
`2026-09-04-Marco-WM-Level-2-Transition-and-SI-Priorities.md`, explicitly
framed by James Letts as SI "speeding up toward the new WM," not slowing
down, since DiracX transition support is SI's top stated priority
(corroborated by `2026-09-08-Submission-Infrastructure-Weekly-Meeting-Team-Planning-and-Project-Roadmap.md`).

Budget/roadmap: `2026-06-05-Submission-Infrastructure-Budget-Review-Planning.md`
records that scale tests confirm ~800,000 running jobs / ~3M cores is
achievable, memory (~2MB/job) is the binding scaling constraint, and
hardware is judged adequate through HL-LHC if failed units are replaced.
A named staffing-risk scenario: losing Jeff Dost would concentrate factory
expertise dangerously in one person (Marco).

### Disagreements / open questions

- Whether removing SI's dedicated Level-2 slot (if absorbed into a
  non-US-held role) is organizationally acceptable — raised, not resolved
  (`2026-09-04-Marco-WM-Level-2-Transition-and-SI-Priorities.md`).
- Antonio vs. Alan Malta Rodrigues/Marco on whether WM should maximize job
  materialization into schedulers or constrain it for bookkeeping-cost
  reasons — flagged as an unresolved CMS-wide design trade-off
  (`2026-05-06-WM-Dev-Team-Weekly-Meeting-Data-Placement-and-SI-Requirements-Review.md`).
- Valentin Kuznetsov/Marco vs. Alan/Kevin Lannon on "thin integration" risk
  — layering glideinWMS/Condor atop PanDA/DIRAC risking a duplicated
  "two engines" architecture, echoing prior WMCore over-complexity concerns
  (`2026-03-02-New-WM-Dev-Team-Weekly-Meeting.md`, `2026-03-03-New-WM-Dev-Team-Weekly-Meeting.md`).
- CRAB schedd scalability limit (DAG-startup memory exhaustion under sudden
  pool-capacity availability) surfaced as an unresolved concern Antonio
  wants addressed proactively (`2026-09-03-Submission-Infrastructure-Weekly-Meeting.md`).

### Sources

- `2026-03-04-CMS-Computing-Model-Submission-Infrastructure-Onboarding.md`
  (primary/canonical)
- `2026-02-26-Submission-Infrastructure-Weekly-Meeting.md`,
  `2026-03-02-New-WM-Dev-Team-Weekly-Meeting.md`,
  `2026-03-03-New-WM-Dev-Team-Weekly-Meeting.md`
- `2026-05-08-Submission-Infrastructure-Candidate-Interview-Pablo-Izquierdo.md`,
  `2026-05-19-Submission-Infrastructure-Candidate-Interview-Sanji.md`,
  `2026-05-29-Submission-Infrastructure-Candidate-Interview-and-DIRAC-Decision-Debrief.md`
- `2026-06-05-Submission-Infrastructure-Budget-Review-Planning.md`
- `2026-07-13-New-WM-Dev-Team-Weekly-Meeting-Effort-Roundtable-and-Use-Case-Boundaries.md`
- `2026-08-26-CMS-OC-Weekly-Meeting.md`
- `2026-09-03-New-WM-Dev-Team-Weekly-Meeting.md`, `2026-09-03-Submission-Infrastructure-Weekly-Meeting.md`
- `2026-09-04-Marco-WM-Level-2-Transition-and-SI-Priorities.md`
- `2026-09-08-Submission-Infrastructure-Weekly-Meeting-Team-Planning-and-Project-Roadmap.md`
- Not yet inspected, but a historically-anchoring reference that would
  materially strengthen the computing-model section during synthesis:
  `40-References/CMS/LHCC-Computing-Model-Review-2021/` (a 2021 LHCC
  computing-model review document — useful for confirming whether the
  pilot-model/Tier-0-priority description is long-standing CMS doctrine or
  a more recent framing).

### Relationships

- Umbrella concept for **Candidates 1–4 and 6–7**; the "New WM Dev Team"
  described here is the organizational home of Candidate 1.
- Effort-allocation and use-case-boundary decisions
  (`2026-07-13`) materially constrain Candidates 1 and 6 (e.g., CMS Connect
  explicitly stays outside DiracX; Tier-0 repacker stays outside
  DiracX/Rucio for now).

---

## Candidate 6: Data-Aware Matchmaking (Rucio-Distance-Based Job-to-Site Matching)

**Status:** needs-more-evidence
**Readiness:** needs more evidence before synthesis — this is genuinely at
proposal/sketch stage, with only two or three meetings, and the corpus
itself contains an important internal distinction (two separate,
similarly-named efforts) that a synthesis note would need to get right.

### Why potentially durable, but why it is not yet ready

The general problem (matching jobs to sites using Rucio data-locality
information, extending beyond CMS's current `Desired_Sites` mechanism) is
architecturally significant and recurs in three different meetings across
two months, which meets the "more than one meeting" bar. However:

- The **July 8** origin (`2026-07-08-Data-Aware-Matchmaking-Design-Discussion.md`,
  largely Italian-language transcript, explicitly noted by the digesting
  agent as low-confidence on some terms) is a first-pass sketch by Marco
  Mascheroni and Andrea Piccinelli: match strictly-local sites first, then
  after ~8 hours relax to "reasonably close" sites within a Rucio
  per-RSE distance threshold. Several details are explicitly "to be
  decided" (e.g., how to cache distances, multi-RSE replicas).
  Given the transcript uncertainty, this source should be re-checked
  directly (not solely via the digest) before any synthesis.
- The **August 27** DIRAC Ops meeting
  (`2026-08-27-DIRAC-Ops-Meeting-Matchmaker-Prototype-and-VO-Round-Table.md`)
  describes a **separate, unrelated-in-origin** Redis-based
  matchmaker/scheduler prototype by an intern ("Jan"), aimed at replacing
  the *legacy DIRAC* matchmaker at scale (target: 1,000 matches/sec, 10M
  jobs) — thematically adjacent (also "matchmaking redesign") but not the
  same project as the July proposal. The intern's departure with no
  documented continuation plan leaves this thread's status uncertain.
- The **September 9** meeting
  (`2026-09-09-CMS-Submission-Infrastructure-Meeting-Data-Aware-Matchmaking-Immortal-Pilots-Condor24.md`)
  continues the July (not the August) thread with HTCondor developer Jaime
  Frey, who confirms ClassAd language currently lacks a compact
  "iterate-and-threshold" construct, meaning new HTCondor functionality
  would be required. Still explicitly unresolved/design-stage.

A synthesis note written now would risk conflating two distinct efforts
that merely share a "matchmaking redesign" theme. More source material (or
a direct re-read of the July 8 transcript to resolve its transcription
uncertainty) is recommended before promoting this to a full concept note.

### Sources

- `2026-07-08-Data-Aware-Matchmaking-Design-Discussion.md` (transcription
  uncertainty flagged — re-verify before synthesis)
- `2026-08-27-DIRAC-Ops-Meeting-Matchmaker-Prototype-and-VO-Round-Table.md`
  (distinct effort — do not conflate)
- `2026-09-09-CMS-Submission-Infrastructure-Meeting-Data-Aware-Matchmaking-Immortal-Pilots-Condor24.md`

### Relationships

- Motivated by the same underlying problem space as **Candidate 4** (CPU
  efficiency / resource waste), but is a specific proposed technical
  mechanism, not the same concept.
- Co-occurs with, but is not technically dependent on, the "Immortal
  Pilots" proposal (also proposal-stage, only two meetings of evidence —
  see "Considered and not proposed" below).

---

## Candidate 7: CWL-Based Workflow/Job Translation Prototype (Bottom-Up vs. Top-Down Design Tension)

**Status:** needs-more-evidence
**Readiness:** needs more evidence before synthesis — genuinely early
prototype work explicitly deferred pending a larger decision, but flagged
here because the underlying *design-philosophy tension* recurs across six
months and two independent prototyping efforts, which is itself a
noteworthy, durable pattern even though neither prototype has converged.

### Why potentially durable, but why it is not yet ready

Three connected September 2026 meetings document an explicit, unresolved
disagreement: Vijay's team's `workgraph.cwl` prototype works **top-down**
from the WMAgent job package/sandbox, deferring job-splitting to DiracX
(`2026-09-08-CWL-Workflow-Prototype-Bottom-Up-vs-Top-Down-Design.md`), while
Marco Mascheroni's proof-of-concept works **bottom-up** from Request
Manager JSON through to per-job pset-tweak/cmsRun/stage-out, arguing the
top-down approach requires reproducing ~3,000 lines of existing logic vs.
~10 (`2026-09-08-CWL-Translation-Job-Runtime-Requirements-Bottom-Up-vs-Top-Down.md`).
Both meetings explicitly defer resolution to a larger discussion with Alan
Malta Rodrigues. Three runtime requirements were agreed regardless of
approach: the CMSSW executable (via CVMFS), a "job particular" file
(event/Lumi boundary), and the PSet config.

Notably, the *same* bottom-up-vs-top-down tension, between the *same*
person (Marco) and different collaborators, appears six months earlier in
`2026-03-06-Prototype-Workflow-Systems-and-AI-Assisted-Development.md`
(Dima's DAGMan-native "fix DAGMan" approach vs. Marco's log-parsing
microagent), where the meeting explicitly ends without resolution ("both
said they are comfortable" proceeding in parallel). This recurrence across
two unrelated prototyping efforts six months apart is the strongest
evidence this is a real, recurring design-philosophy fault line in the
team rather than a one-off implementation detail — but because neither
instance reached a decision, and the underlying technology (CWL adoption)
is itself unconfirmed as CMS's direction (`2026-09-04-Conditions-Workshop-HLT-Provisioning-and-CWL-Discussion.md`
frames it as a removable, temporary adapter; whether Tier-0/MCM even needs
CWL translation is unresolved), a synthesis note now would mostly document
an open question rather than durable understanding.

### Sources

- `2026-03-06-Prototype-Workflow-Systems-and-AI-Assisted-Development.md`
- `2026-09-04-Conditions-Workshop-HLT-Provisioning-and-CWL-Discussion.md`
- `2026-09-08-CWL-Translation-Job-Runtime-Requirements-Bottom-Up-vs-Top-Down.md`
- `2026-09-08-CWL-Workflow-Prototype-Bottom-Up-vs-Top-Down-Design.md`
- `2026-09-09-Conditions-Preparation-Workshop-2026-Validation-Tier0-and-Future-WMS.md`
  (context: WMAgent/WM4 frozen since Sept 2025, DiracX-based replacement
  targeted, earliest usable system mid-2027 — the strategic backdrop
  against which the CWL prototypes are being explored)

### Relationships

- A concrete instance of the same job-materialization/translation question
  left open under **Candidate 1** (DiracX integration).
- Constrained by the use-case-boundary decisions under **Candidate 5**
  (e.g., CMS Connect staying outside DiracX).

---

## Considered and not proposed as standalone candidates

Per SYNTHESIS.md principle 2 ("evidence before frequency"), the following
recurring topics were deliberately **not** proposed as standalone
candidates. They may be worth revisiting once more source material
accumulates, or are better represented as sub-points within the candidates
above.

- **HTCondor training/onboarding practice** (`2026-04-09-HTCondor-Training-Session.md`,
  `2026-04-10-Overload-Enabled-Fix-Planning-and-Condor-Overview-Training.md`,
  `2026-09-02-HTCondor-Shadowing-Session-CNAF-Efficiency-Debugging.md`,
  `2026-09-14-HTCondor-Fundamentals-Training-Slots-Pools-and-Job-Submission.md`).
  This is real and recurring (two full onboarding cycles, ~7 months apart,
  using the same "a little at a time" pacing), but it documents *how the
  team teaches itself HTCondor*, not a durable technical or architectural
  concept in its own right. The underlying technical content is already
  covered by the seed vocabulary entity `[[HTCondor]]` and by Candidate 2.
- **"Overload Enabled" mechanism/bug** — real, well-documented
  (`2026-04-10-Overload-Enabled-Fix-Planning-and-Condor-Overview-Training.md`),
  but it is a specific configuration mechanism inside Candidate 2's
  architecture and a contributing factor to Candidate 4's efficiency
  problem. It is represented as a sub-point of both rather than a
  standalone note.
- **GPU Sharing (MIG vs. MPS)** — one substantive meeting
  (`2026-03-26-1402-GPU-Sharing-MIG-vs-MPS-Discussion.md`, a KIT thesis
  walkthrough) plus brief forward-looking mentions elsewhere
  (`2026-09-09-CMS-OC-Weekly-Meeting-CPU-Efficiency-Strategy.md`,
  `2026-09-04-Conditions-Workshop-HLT-Provisioning-and-CWL-Discussion.md`,
  `2026-05-29-Pilot-Monitoring-and-Efficiency-Presentation-Prep.md`). Single
  primary source; insufficient independent corroboration yet for a durable
  concept note. Worth revisiting if GPU/heterogeneous-computing discussion
  grows (the `[[Heterogeneous Computing]]` wikilink already has 15
  occurrences corpus-wide, suggesting a broader concept may eventually be
  warranted, but MIG-vs-MPS specifically is thin).
- **"Immortal Pilots"** — a real, named proposal, but only two meetings
  (`2026-09-09-CMS-Submission-Infrastructure-Meeting-Data-Aware-Matchmaking-Immortal-Pilots-Condor24.md`,
  `2026-09-15-OSG-Factory-Ops-Meeting.md`), both within a one-week window,
  with three named "showstopper" concerns and no decision. Represented as
  an open question under Candidates 2 and 4.
- **InterSeed** (DIRAC's HTCondor CE-interface rewrite) — real and
  recurring within the DiracX thread, but it is a component-level detail
  of Candidate 1's integration questions, not an independent durable
  concept on its own.
- **DIRAC/DiracX ADR process** — recurring but represented as an evidence
  point (repeatedly-slipping timeline) within Candidate 1, rather than a
  standalone concept about ADR process itself.
- **CMS Connect** — mentioned once as an explicit scope boundary
  (`2026-07-13-New-WM-Dev-Team-Weekly-Meeting-Effort-Roundtable-and-Use-Case-Boundaries.md`);
  too thin on its own, represented as a relationship/boundary fact under
  Candidate 5.

## Note on the two PDF-only "meeting" artifacts

`20-Meetings/20241021_CHEP24_Overloading.pdf` and other PDF files in
`20-Meetings/` (CHEP26 proceedings, WLCG TR draft, etc.) were listed but not
opened during this discovery pass — they are conference proceedings/slides
co-located with meeting notes rather than meeting transcripts, and several
appear directly relevant to Candidates 2, 3, and 4 (see "Sources — not yet
inspected" above). They should be read directly during synthesis of those
candidates, not treated as already-incorporated evidence.
