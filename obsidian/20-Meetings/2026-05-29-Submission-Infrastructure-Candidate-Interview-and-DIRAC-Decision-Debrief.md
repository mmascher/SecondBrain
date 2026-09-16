---
type: meeting
date: 2026-05-29
participants:
  - Stephan Lammel
  - Marco Mascheroni
  - Antonio Perez-Calero Yzquierdo
  - ilakkiavisakan (candidate)
topics:
  - candidate interview for open Submission Infrastructure position
  - candidate background: ATLAS TDAQ technical studentship, Kubernetes, HTCondor, monitoring, OpenEBS/AWS spot-instance projects
  - hiring process and CERN per-country hiring-contingent constraint
  - communication gap around the already-made DIRAC/DiracX workload-management decision
  - Tier0 commissioning timeline and CSA milestone
  - CWL vs. Condor job-description mapping for DiracX
  - glideinWMS/DiracX global-pool integration and Florian's (KIT) involvement
  - CHEP conference outcomes and WN/Dublin retreat
  - management week (face-to-face) logistics and G7 Evian border-crossing concerns
---

# Submission Infrastructure Candidate Interview and DIRAC Decision Debrief

## Summary

This meeting combined a candidate interview for an open [[Submission Infrastructure]] position with a subsequent internal debrief and general team sync between Stephan Lammel, Marco Mascheroni, and Antonio Perez-Calero Yzquierdo. The candidate (Zoom label "ilakkiavisakan"; their name was pronounced differently several times in conversation, e.g. "Ilakkia"/"Elyakia"/"Silakia" — the transcript does not resolve a single reliable spelling) is a CERN technical student on the [[ATLAS]] Trigger and Data Acquisition (TDAQ) team, about 8 months into a technical studentship, currently building a Kubernetes dashboard for the ATLAS Event Filter ("EF") farm. The panel probed their experience with [[HTCondor]], Kubernetes/OpenEBS, AWS spot-instance workflows, monitoring stacks (EFK, Prometheus/Grafana), configuration management (Ansible), and large-scale system debugging, and answered the candidate's own question about CMS's current biggest operational headaches.

After the candidate left, Marco, Antonio, and Stephan briefly discussed the hiring pool and process (including CERN's per-country hiring-contingent rules) before moving to unrelated team-sync topics: a communication gap around the already-finalized decision to adopt [[DIRAC]]/[[DIRACX]] as the primary future workload-management system (surfaced by a slide bullet that implied the decision was still open), the Tier0 commissioning timeline, the need to map [[CWL]] and Condor job descriptions to each other, the planned glideinWMS/DiracX global-pool integration involving Florian (now at KIT), outcomes from the CHEP conference (where Antonio convened the distributed-computing track) and a recent multi-experiment retreat, and logistics for the mid-June management face-to-face meeting, including a possible impact from G7-related border restrictions near CERN.

## Decisions / Conclusions

- CMS's decision to adopt [[DIRAC]] (via [[DIRACX]]) as the primary new workload/workflow-management system was already made roughly three weeks before this meeting (per Stephan) and had been presented at the March CMS collaboration meeting and discussed in a CMS computing weekly meeting. The previously "reserved" fallback option is no longer being held open ("the reservation has been released"); the decision would only be revisited if the team runs into an "insurmountable issue."
- A first, simple Monte Carlo workflow on the new system is targeted for readiness around a milestone transcribed as "CSA 28" (exact designation/year uncertain in the transcript); Tier0 commissioning on the new system would follow, starting in 2029.
- The panel does not plan to interview additional candidates as a hard requirement; Stephan noted there is no obligation to interview more people once a suitable candidate is found, and that the decision of whether to keep interviewing is up to Marco and Antonio.
- Per Stephan, candidate selection should be based purely on who the panel prefers, independent of current country-representation balance; CERN's per-country employment-contingent system (a mix of member-state contribution-based and non-member-state quotas) is only checked afterward, and if the preferred candidate's country is currently over-contingent ("in a veto state"), the panel would have to move to the next candidate. This constraint has previously blocked at least one candidate (cited: a candidate from Pakistan, over the country's limit at the time).
- Florian's involvement in the glideinWMS/DiracX global-pool integration was already arranged directly between Stephan and Marcus (Florian's new manager at KIT): Marcus agreed that Florian can spend an agreed percentage of his time on this integration, as a specific project rather than an open-ended commitment. The integration work sits organizationally under the DIRAC project, though Submission Infrastructure expects to be heavily involved.

## Action Items

- [ ] Re-check the recruiter-submitted candidate list once more for any candidates that may have been missed, before the hiring decision is finalized — Marco Mascheroni
- [ ] Decide, together, whether to make an offer from the current candidate pool or continue interviewing, after reviewing notes over the weekend — Marco Mascheroni, Antonio Perez-Calero Yzquierdo
- [ ] Install and run a DIRAC instance to evaluate feasibility, targeting the DIRAC hackathon in early July — Marco Mascheroni
- [ ] Keep an eye on ensuring CWL and Condor job-description syntax can be reliably mapped to each other as DiracX integration proceeds — Marco Mascheroni

## Discussion

### Candidate interview
- Background: bachelor's studies in civil engineering (India) with a shift toward software engineering/DevOps/distributed systems during a fourth-year exchange at IIT Delhi; subsequently a CERN technical studentship on the ATLAS TDAQ team (~8 months in). Their technical studentship contract was extended the day before this meeting, from an original end date in August to the end of October, though the candidate said they would prefer to finish their current project rather than work strictly to the contract end date.
- Current CERN work: building a Kubernetes dashboard for the ATLAS Event Filter ("EF") farm, subscribing to Kubernetes watch events (pods, nodes, daemon sets, replica sets) over a WebSocket, querying node/CPU/disk/memory metrics from a Thanos/Prometheus data source, and rendering them via a Flask backend API and a React.js frontend.
- Open-source contribution: automated cleanup of orphaned PersistentVolumes/PersistentVolumeClaims left behind by StatefulSet pods (e.g. MongoDB) in [[OpenEBS]] (a CNCF project), using a label-based scan to avoid deleting unrelated volumes; previously done manually.
- Personal project (with a friend, using an IIT Delhi institutional account): batch-processing ~10,000 jobs on AWS Spot Instances, using [[HTCondor]] to track job progress, checkpointing completed work to S3 (leveraging idempotency to resume from the last checkpoint rather than restarting), polling the AWS spot-termination-notice URL, and staggering each worker's S3 write time to avoid overloading the S3 bucket when many instances are reclaimed simultaneously. Reported learning that Kubernetes readiness/liveness probes are insufficient to detect a stuck worker, and using timestamp-based progress checks (e.g. time since last state change) or Condor job-hold heuristics instead.
- HTCondor knowledge: candidate's initial answer distinguishing `condor_q` and `condor_status` was uncertain; Marco and Antonio clarified that `condor_q` queries the schedd (job queue) while `condor_status` queries the collector (machine/pool state), with the negotiator handling matchmaking between them.
- Monitoring experience: built a "honeypots-as-a-service" system on AWS (SSH/email/malware honeypots across multiple sites), using an EFK stack (Fluent Bit → Elasticsearch → Kibana) for log analysis and Prometheus/Grafana for metrics.
- Debugging/system-design experience: for the Kubernetes dashboard, an initial per-event push design overwhelmed the UI under high event volume; fixed by batching updates through a message queue (flushing every ~10 seconds or after ~10 events) and by diffing against a baseline JSON structure instead of re-sending full event payloads.
- Configuration management: has used Ansible, not Puppet (the tool the team uses).
- Scalability experience: limited to the honeypot project, at a much smaller scale than CMS/ATLAS-level systems; no direct large-scale system-management experience. Described approach to debugging a scalability issue as: first check logs/Grafana/ELK dashboards to localize the issue, then use Condor commands (e.g. `condor_q`) once a specific job/cluster ID is identified.
- Career motivation and outlook: values CERN's variety of sub-teams (cited ATLAS TDAQ as having ~18–19 members split across networking, machine learning, online software, and readout) compared to more siloed industry teams; plans to continue in this field for 2–3 more years before considering a master's or PhD; when asked directly, said they lean toward SRE/operations-style roles ("debugging and problem solving") over pure development.
- Candidate's own question to the panel: asked what the panel sees as CMS's biggest operational pain point for the upcoming run, referencing a CMS HL-LHC report on workflow management (citing points like user-facing workflow usability and lack of GPU-aware scheduling). Stephan answered that production-workflow operations currently consume the most effort, and that a priority is making failure reasons clearer and more actionable for both physicists and the production team, plus more automation to reduce that load; a second major area of effort is data management, tied to the recent adoption of [[Rucio]] and ongoing integration work. Antonio and Marco added that integration of heterogeneous resources (CPU/GPU scheduling and matchmaking, resource description, accounting, monitoring) and the shift from a uniform grid-node model with pledged resources to a mixed landscape including general-purpose HPC centers under an allocation-based model are the team's main forward-looking challenges ahead of the High-Luminosity LHC. Stephan distinguished this from current day-to-day operational headaches, noting the team must also plan for technologies that will only become available on the HL-LHC timescale.

### Hiring process and candidate pool
- Following the interview, Marco and Antonio gave their impressions of the candidate as capable but junior, without much experience managing a system at the scale the team operates, and discussed them briefly relative to other candidates already interviewed for the same opening (names and comparative judgments about those other candidates are omitted here as personnel evaluation).
- The group agreed the process should not be drawn out further; Stephan noted panels have previously interviewed as few as one candidate (after filtering) when there was a clear match, and there is no requirement to interview a larger number.
- Antonio raised, as a separate consideration, that Spain seems underrepresented among people from Spanish institutes engaged in central CMS computing roles (citing the Tier-2 in Santander as an example of a site not otherwise engaged centrally), and asked whether origin should factor into candidate selection.
- Stephan clarified there is no origin-based preference, but there is a structural constraint: CERN allocates a hiring contingent per country (member states based on their financial contribution fraction, plus a separate contingent for non-member states), and hiring can be blocked if a country is currently over its contingent — this has happened before (cited: a previous candidate from Pakistan). Stephan's guidance was to choose the preferred candidate regardless of current country representation, and only fall back to the next candidate if a contingent block ("veto") applies once the choice is put forward, since the contingent list changes month to month.
- Salary differences between candidates were mentioned only briefly: per Stephan, the main structural difference arises when hiring someone directly from a university (SAA route) versus other paths.

### DIRAC/DiracX decision and internal communication
- Antonio reported that a slide bullet from a recent CMS computing meeting ("Tier0 will have to adapt for DIRAC") prompted him to ask whether CMS had actually already decided on DIRAC as the workload-management solution, since he — and, per corridor conversations at CHEP, other CMS Computing colleagues — had not registered that the decision was final.
- Stephan confirmed the decision was made about three weeks earlier and had already been presented in the March CMS collaboration meeting (plenary) and discussed again afterward in a CMS computing weekly meeting; he acknowledged a "communication" gap and said this is why he is now maintaining a standing/continuously-updated page (rather than only meeting slides) so people can catch up roughly once a week without needing to review Indico slides after missing a meeting.
- At CHEP, in the distributed-computing track that Antonio convened, questions were raised (attributed to a name transcribed uncertainly as "Simonica"/"Paran") about how the team would know when it becomes "too late" to fall back from DIRAC to the alternative option, since Andrea Piccinelli's presented timeline still implicitly showed an "Option A / Option B" framing. Stephan's position, as restated in this meeting, is that the decision has been made, and reconsideration would only happen in the event of an insurmountable issue — not that a formal reversal point exists in the timeline.
- The DIRAC/DiracX team, on their own conference track, presented DIRAC/DiracX and its community without including CMS in that framing yet, since CMS's engagement (via a hackathon in early July) has not started.

### Tier0 timeline and CWL/Condor mapping
- Per Stephan, an initial simple Monte Carlo workflow on the new workload-management system is targeted for a milestone transcribed as "CSA 28" (exact meaning/year uncertain); Tier0 commissioning would begin in 2029.
- Antonio noted that DiracX is expected to natively speak the [[CWL]] (Common Workflow Language) as its default job-description format, while CMS's submission infrastructure currently speaks in Condor/classad syntax. Both Antonio and Stephan agreed there needs to be a reliable way to map between the two — either via a shared standardized language or by translating DIRAC's language to Condor — and that it should not matter which direction the translation happens as long as both are equivalently expressible in Condor terms. Antonio mentioned informally testing this by asking an AI tool to produce equivalent job-submission examples in CWL versus Condor syntax to gauge how much they differ. Stephan said he expects Marco to keep an eye on ensuring this mapping holds.

### glideinWMS/DiracX integration and Florian (KIT)
- Antonio had informally discussed with Florian, during a CHEP lunch break, whether Florian would be interested in staying involved with Submission Infrastructure on a specific project (not a central role) while primarily now working at KIT.
- Stephan clarified this had, in fact, already been arranged directly with Marcus (Florian's manager at KIT): Marcus agreed that Florian can dedicate an agreed percentage of his time to integrating the global pool ([[glideinWMS]]) with [[DIRACX]], as a bounded project rather than an open-ended commitment to Submission Infrastructure work. This project is organized under the DIRAC project, though Submission Infrastructure expects heavy involvement, and the project's technical lead is expected to be one of Submission Infrastructure's level-2 people. Florian's name already appears in this context on slides Stephan prepared for the upcoming management face-to-face, which Antonio had not been aware of.
- Marco and Antonio expressed some concern about how much time Florian will realistically be able to dedicate once he is also settling into his new KIT responsibilities, and noted (based on past experience) that Florian had continued working on unrelated things (cited: something referred to as "Auditor") during the tail end of his prior time with Submission Infrastructure despite nominally being fully dedicated — which Antonio believes contributed to the team's GPU-related CHEP contribution being less mature than hoped. Stephan's position was that a manager cannot dictate what an employee does beyond their committed hours, but that the team should ensure work is properly assigned and logged, and suggested giving people well-scoped projects with an expected duration (e.g. "three months") rather than trying to enforce hour-by-hour compliance. Marco noted the team does not currently set explicit project timelines and suggested this might be worth doing going forward.

### CHEP conference and recent retreat
- The CHEP conference (in Thailand) concluded on the day of this meeting; Antonio served as convener of the distributed-computing track.
- The group also referenced a recent multi-experiment retreat/workshop — described inconsistently in the transcript as the "WN Retreat" or "Dublin Retreat," apparently held in connection with Fermilab (the transcript is unclear on the precise name and location). Marco described it as primarily team-building (e.g. carpooling and bonding with a colleague, Federico) combined with high-level, cross-experiment discussion, and said he personally had not yet started any technical follow-up work from it. Both Marco and Stephan considered it a good event overall, though Stephan noted it did not achieve what Andrea (surname not given) had hoped for in terms of building a community around what was referred to only as "the revamped option" (meaning unclear from the transcript).

### Management face-to-face logistics
- The management week face-to-face meeting is planned for the week of June 15th–17th. Antonio has a university teaching obligation (an exam) on Monday the 15th and expects to attend in person only on the 16th/17th, or otherwise remotely.
- Marco raised a concern about the G7 summit in Evian (France) potentially disrupting CERN-area border crossings (specifically Gate E, used to walk from Saint-Genis into CERN) during the same period; Stephan said the impact is not yet clear, pending decisions by Swiss and French authorities, but most people are expected to remain able to be on-site, with the greatest impact likely falling on staff who commute daily from the French side rather than those already staying in Switzerland or arriving by tram. Remote participation in the face-to-face would remain available for anyone affected, and the team plans to recommend telework to affected operations staff once the situation is clearer.
- Stephan said his planned face-to-face slides cover the new workflow-management system and team composition, intended to inform people and prompt discussion.

## Open Questions

- What is the candidate's correct name/spelling (transcript label "ilakkiavisakan"; spoken variants included "Ilakkia," "Elyakia," and "Silakia")?
- Will Marco's re-check of the recruiter list surface any additional candidates, or will the panel proceed to a decision with the current pool?
- What is the exact designation and year behind the "CSA 28" Tier0/Monte-Carlo milestone referenced by Stephan?
- What precisely is the "WN Retreat"/"Dublin Retreat" event referenced, and what was the "revamped option" community-building goal Andrea had hoped for from it?
- When, and to what extent, will Florian actually be able to start on the glideinWMS/DiracX integration work, given his new KIT responsibilities?
- How will G7-related border restrictions near CERN actually play out for the mid-June management face-to-face, and will they meaningfully affect attendance?

## Related

[[Submission Infrastructure]] · [[DIRAC]] · [[DIRACX]] · [[HTCondor]] · [[glideinWMS]] · [[CWL]] · [[Rucio]] · [[CMS]] · [[CERN]] · [[ATLAS]] · [[GPU]] · [[Heterogeneous Computing]] · [[Kubernetes]] · [[CHEP]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-29 10.06.01 Stephan Lammel's Zoom Meeting`)
