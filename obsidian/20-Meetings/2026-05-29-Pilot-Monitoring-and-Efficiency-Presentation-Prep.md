---
type: meeting
date: 2026-05-29
participants:
  - Marco Mascheroni
  - Luis Simas
topics:
  - Preparation of Luis's presentation on pilot monitoring and efficiency
  - CMS job monitoring OpenSearch index and Grafana dashboards
  - Distinction between job efficiency, payload efficiency, scheduling efficiency, and pilot/envelope monitoring
  - Discrepancy between pilot-layer efficiency and site-reported resource efficiency (overloading)
  - CPU efficiency analysis tables (Condor-based vs. job-report/step-chain-based sources) and the PNR dashboard
  - Alerts on existing monitoring dashboards
  - COMPOPS channel: misrouted incident ticket
  - KIT site admins using COMPOPS monitoring to verify GPU test jobs
---

# Pilot Monitoring and Efficiency Presentation Prep

## Summary

Marco and Luis worked through the structure of a presentation Luis is preparing (for the SI group) on pilot monitoring, using Marco's existing slide deck as a starting template. They reviewed what monitoring currently exists: every 12 minutes, information about each job is queried from the SchedDs (referred to in the transcript as "SCADIs") — a cadence Carlos had decided on — and pushed into an OpenSearch index that Marco called "the index," which underlies all of the team's Grafana dashboards. Luis pointed out that this covers job-level monitoring but not pilot/envelope-level monitoring, which is the gap his own work has been addressing.

The discussion moved into the different notions of "efficiency" in use: payload/job efficiency (reviewed weekly at the Monday COMPOPS meeting) is distinct from the pilot/site resource-usage efficiency, and the two can diverge significantly due to overloading and pilot overhead — Luis gave an example where a site's payload efficiency appeared to be 46% while the site itself reported seeing 70% efficiency, because the pilot layer can compensate for things the payload-level number doesn't capture. Marco explained that, absent overloading, overall site efficiency would roughly be the product of scheduling efficiency and job efficiency, but overloading makes deriving a "true" efficiency number from these components difficult. They also looked at the existing CPU efficiency analysis tables page, noting two families of tables: ones based on Condor data and others (including a "step chain" table) based on job self-reports; Marco recalled seeing some differences between them in the past but wasn't certain of the details. A separate dashboard referred to as the "PNR" efficiency dashboard, which Marco recalled from a Monday COMPOPS meeting, is believed to be based on the job-report data, but this needs to be confirmed. Neither could find an existing dashboard specifically for pilot-level/payload efficiency despite it being a frequently discussed topic.

Marco proposed a presentation angle: rather than framing the talk primarily around efficiency, frame it around pilot monitoring, and use the efficiency/overloading story as a use case illustrating why pilot-level (envelope) monitoring is valuable — since before Luis's work there was no way to measure the impact of the overloading strategy, and now there is. Luis agreed this resolved the difficulty he'd been having finding the right angle for his contribution, since overloading itself is already a well-established, familiar topic for the audience. They agreed Luis should reuse Marco's existing, previously-presented slides where practical (the group commonly recycles slides due to limited prep time) and focus new effort on the new material, while retaining the option to rework slides such as the pilot lifecycle diagram if he has time and prefers a different visual approach. Marco also suggested Luis mention the various existing pilot-monitoring dashboards (including pilot log dashboards, some apparently built on top of a "Data Factory"-related source) that have not previously been presented to the group, and flag legacy dashboards that are working but that Luis is planning to review and improve, as a "future work" closing point.

Separately, Luis raised two smaller updates. First, a site admin had opened an incident ticket in the COMPOPS Mattermost channel about the recent incident, but it went unanswered because it was assigned to the wrong group; Luis resolved it directly by confirming with the site admin that the issue was already fixed, and the ticket was closed. Marco said he had missed this and would pay more attention to the COMPOPS channel going forward. Second, Luis mentioned that in a channel with KIT, KIT's site admins have been working closely with a user running production GPU test jobs, using COMPOPS monitoring themselves to check whether jobs actually ran at their site — behavior Marco and Luis agreed is unusual (site admins don't normally track which jobs run where) but welcome, characterizing KIT as acting like "power users."

## Decisions / Conclusions

- The group agreed on a presentation structure: lead with the existing state of monitoring (good job-level monitoring via the 12-minute SchedD-to-OpenSearch pipeline and its Grafana dashboards, but no pilot/envelope-level monitoring), then use efficiency and overloading measurement as a concrete use case motivating why pilot monitoring is valuable, and then present Luis's pilot-monitoring work (including the overloading-efficiency measurement it enables) as the contribution filling that gap.
- Luis will reuse Marco's existing slides for established/background material and concentrate new work on the pilot-monitoring content, with the option to rework slides (e.g., the pilot lifecycle diagram) if time allows.
- Luis will remove/de-emphasize the "efficiency" framing on the introductory slide to avoid confusing the audience, keeping notes for himself on what to say instead.

## Action Items

- [ ] Continue preparing and building out the presentation slides on pilot monitoring, following the agreed structure (reuse existing slides for background, add new material for pilot monitoring/overloading, include a future-work note on improving legacy pilot dashboards and possibly alerts) — Luis Simas
- [ ] Ask around (mentioned: Hassan Ahmed, and a colleague referred to as "Gregor"/"Greggone") to confirm whether the CPU efficiency tables and the PNR dashboard are based on job-report data — Luis Simas
- [ ] Pay more attention to / look into the COMPOPS Mattermost channel, including the recently misrouted incident ticket — Marco Mascheroni

## Discussion

### Job monitoring pipeline and dashboards
Every 12 minutes, information about each job is queried from the SchedDs and written into an OpenSearch index (a cadence decided by Carlos). All of the team's Grafana dashboards are built on top of this index. This gives good visibility into job-level behavior but no visibility into the pilot/envelope layer around the job — the gap Luis's monitoring work addresses.

### Efficiency terminology and discrepancies
- Payload/job efficiency is reviewed weekly at the Monday COMPOPS meeting, but this measures job efficiency, not pilot-level efficiency.
- Luis noted that payload efficiency numbers can look very different from what a site itself observes (e.g., 46% vs. a site-reported 70%), because the pilot layer can compensate for inefficiencies that the payload-level metric alone doesn't reflect (overloading and pilot overhead).
- Marco explained that overall site efficiency would, absent overloading, roughly correspond to the product of scheduling efficiency (whether pilots are running jobs at all) and job efficiency (how efficiently running jobs use resources) — but overloading and pilot start/idle effects (e.g., a pilot running for 20 minutes with no job matched) complicate deriving a single "true" efficiency figure. He described this as an unresolved source of confusion in the numbers that people are likely to ask about.
- The CPU efficiency analysis tables page has two categories of tables: some based on Condor data, and others (including a "step chain" table) based on job self-reports submitted when jobs finish. Marco recalled noticing differences between them previously but was not certain of the specifics.
- A "PNR" dashboard, which Marco recalled seeing referenced at a Monday COMPOPS meeting, is believed (not confirmed) to be based on the job-report data. Marco proposed cross-checking this with Hassan Ahmed and Gregor.
- Neither Marco nor Luis could locate an existing dashboard dedicated to pilot/payload-level efficiency, despite it being a recurring topic of discussion at COMPOPS meetings.

### Alerts on dashboards
Luis noted that an existing dashboard (referenced in the context of a recent incident) made a spike in errors very visually clear and could readily be turned into an alert. Marco referenced an existing commitment to do more work on alerting based on dashboards, though the transcript is unclear on the specifics of what exactly was committed to or by whom.

### Luis's additional dashboards
Luis showed several dashboards he has built beyond the core overloading-efficiency ones, including an average efficiency-gain-from-overloading plot and a recently added memory dashboard, describing the set as having "grown quite a bit."

### COMPOPS channel incident ticket
A site admin opened an incident ticket in the COMPOPS Mattermost channel related to a recent incident, but it initially went unanswered because it had been assigned to the wrong group. Luis followed up directly with the site admin, confirmed the issue was already fixed, and the ticket was closed. Marco said he had missed the message and noted he monitors many channels, making it easy for lower-priority notifications to be missed once they're no longer highlighted.

### KIT site admins and GPU test jobs
In a Mattermost channel with KIT, KIT's site admins have reportedly been working closely with a user running production jobs to test GPUs, using COMPOPS monitoring themselves to verify whether those jobs actually ran at the KIT site. Both Marco and Luis characterized this as unusual — site admins don't typically track which specific jobs run at their site — but described it as a welcome example of KIT acting as "power users."

## Open Questions

- Whether the CPU efficiency analysis tables and the PNR dashboard are actually based on job-report data, as currently assumed — to be confirmed with Hassan Ahmed and Gregor.
- What exactly is meant by the earlier commitment to do more work on alerts, and its current status.
- The precise cause(s) of past discrepancies observed between the Condor-based and job-report-based CPU efficiency tables.

## Related

[[Submission Infrastructure]] · [[Pilot Jobs]] · [[HTCondor]] · [[Monitoring]] · [[OpenSearch]] · [[Grafana]] · [[Factory Operations]] · [[GPU]] · [[CMS]]

## Source

meeting_saved_closed_caption.txt (from `2026-05-29 14.12.44 Submission Infrastructure Weekly Meeting`)
