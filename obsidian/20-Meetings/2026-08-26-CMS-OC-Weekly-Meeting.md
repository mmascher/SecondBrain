---
type: meeting
date: 2026-08-26
participants:
  - Phat Srimanobhas
  - Kevin Pedro
  - Chris Jones
  - Matti Kortelainen
  - Stephan Lammel
  - Andrea Piccinelli
  - V Daniel Elvira
  - Liz Sexton-Kennedy
  - Daniele Spiga
topics:
  - PLAT job crash debugging
  - DMWM report
  - software project roadmap and metrics
  - CSA28 planning
  - WLCG technical roadmap
  - outgoing Level-2 coordinators
  - LHCC/WLCG week preview (Run3 close-out, 2028 resource request, disk/tape mitigation)
---

# CMS O&C Weekly Meeting

## Summary

Note: this transcript is a partial recording — it begins and ends mid-sentence, so it does not cover the full meeting. The captured portion covers: ongoing debugging of crashing PLAT/PPD jobs, a brief DMWM status report, a report on the CMS offline computing "software project" roadmap effort and evaluation of project-management tooling, a clarification of the CSA28 planning process, a relayed WLCG technical-roadmap timeline update, thanks to several outgoing Level-2 coordinators, and the beginning of a preview of slides for the upcoming LHCC/WLCG week presentation (Run 3 + heavy-ion data-taking close-out, CPU/resource usage, a preliminary 2028 resource request, and mitigation strategies for an anticipated disk/tape shortfall). The transcript cuts off mid-sentence during the discussion of dataset lifetime and storage-usage monitoring.

## Decisions / Conclusions

- The CSA28 planning process was clarified (not newly decided in this meeting, but stated by Stephan Lammel): the offline & computing group will first put together its own CSA28 plan as part of the offline computing / software project plan, and only then hand it to the CSA coordinators, who will sync it with the rest of the overall plan. Communication with CSA leaders will happen after that internal plan exists, or otherwise at Offline & Computing week.
- CMS's short-term (2027) resource requirements were assessed as reasonably likely to be met, based on interaction with sites through the CMS Computing Resources Board; uncertainty increases significantly for 2028 due to hardware price/availability risk.
- For the near term, CMS does not anticipate requesting additional resources for the luminosity ramp-up phase, in order to limit short-term risk and focus on longer-term strategy.

## Action Items

- [ ] Post the exact configuration change needed (thread stack size option) to the GitHub issue, to test whether a larger thread stack size affects the PLAT job crashes — Matti Kortelainen
- [ ] Present a proposal for metrics (to monitor/track/measure project progress) and a concrete plan to help Level-2s and activity owners resolve roadblocks, at Offline & Computing week in September, given that a full resourced roadmap may not be ready in time — V. Daniel Elvira

## Discussion

### PLAT/PPD job crash debugging

The group discussed ongoing, unreproduced crashes in PLAT jobs (PPD jobs) running at CERN. Kevin Pedro asked whether the affected jobs share a common site; Phat Srimanobhas confirmed they run away at CERN, and said he had tried but failed to identify a machine-configuration cause. Kevin Pedro raised the possibility of a site/machine-level issue (misconfigured VMs, disk, or RAM causing corruption) rather than a code issue, noting this was speculative. Chris Jones proposed an additional hypothesis: a stack overflow from deep call stacks combined with many thread-local statics, where colliding stacks can cause silent corruption. He suggested testing with a larger thread stack size, configurable via the "thread stack size" option in the process options block. Matti Kortelainen agreed to post the exact change needed in the issue.

### DMWM report

Andrea Piccinelli reported no particular news from the prior week, other than confirming that a new DESK client version addressing a previously reported ratio issue should be going into production.

### Software project roadmap and PM tooling

V. Daniel Elvira reported on the "software project" effort: he had reminded relevant Level-2s to fill in a Google spreadsheet with effort-needed/available information to support resource-scheduling input for the roadmap. Some Level-2s had promised this information by mid-August, others by end of August. He noted meeting this deadline matters if the group is serious about presenting a roadmap at the September Offline & Computing week, but acknowledged the summer break has caused delays (Level-2s on vacation or needing to reach people on vacation), so expectations may need to be managed. If a full resourced roadmap is not ready, he plans to instead present a proposal for tracking metrics and a concrete plan to help Level-2s and activity owners address effort gaps and roadblocks, describing it as intentionally rough and subject to iteration.

Separately, Daniel Elvira described evaluating project-management tools, including Open Project (free "community version"). He concluded it does not fit the group's needs: it lacks a cross-activity roll-up engine (e.g., to automatically compute available/needed effort and coverage ratio per year, or other compound metrics across activities), lacks automatic baseline-comparison reporting (what changed since a given date), and its Gantt chart support does not allow PDF export (only screenshots). He has been consulting project managers with relevant experience, including Frank Hartman (who has not yet responded) about tools used for detectors, and is asking whether CMS or CERN offers support such as licenses for a professional version of Open Project or an alternative. Liz Sexton-Kennedy noted she had also given up on Open Project and now plans to draw Gantt charts herself for presentations. Daniel Elvira said he is considering the same approach, potentially with the help of Claude, referencing a prior interaction where Claude produced a useful proposal for processing spreadsheet information; he raised persistence (how to store a periodic, professional record of project status over time) as an open consideration.

### CSA28 planning

Daniel Elvira asked whether there is a plan to communicate with CSA28 leaders before Offline & Computing week, to check on their planning progress and interaction with Level-1 coordination areas. Stephan Lammel clarified the process: the group first needs its own CSA28 plan (as part of the offline computing / software project plan), and only after that will it be shared with the CSA coordinators, who will then sync it with the rest of the plan; otherwise, this will happen at Offline & Computing week. Milestones for CSA28 have been put up (per Stephan Lammel).

### WLCG technical roadmap (relayed report)

Stephan Lammel relayed a report from James (technical board, not present due to an OTF in progress): the technical roadmap timeline for WLCG has shifted by a few months because the ATLAS Computing TDR review has moved from autumn of this year to spring of next year, to align with the roadmaps; the group still wants its roadmaps complete before the end of this year. James also mentioned Alicia's involvement with the ongoing OTF and the next two OTFs (an FDS/XOT workshop) together with related epics in the US.

### Outgoing Level-2 coordinators

Stephan Lammel thanked outgoing Level-2 coordinators: Pat Javier (reconstruction, term ending in a few days), Pietro (machine learning), and Andrea Piccinelli (Data Management and Workflow Management development). He also thanked Phat Srimanobhas, who is stepping down after providing guidance to offline computing for the past two years, and invited attendees to Offline & Computing week for a celebration.

### LHCC/WLCG week preview (Daniele Spiga)

Daniele Spiga previewed slides to be presented the following week at the LHCC week WLCG session, covering: Run 3 (including heavy-ion) close-out status from the CMS perspective, overall WLCG reporting, GPU-benchmarking-related mitigation strategies for an anticipated resource shortfall (short term, into 2028), and monitoring updates on storage/data usage and dataset lifetime on storage.

Key points on Run 3 + heavy-ion close-out: data taking is complete, with high data-certification efficiency; CMS recorded 2018 petabytes (~2 PB, transcript states "2018 petabyte") of raw heavy-ion data across two storage endpoints, and a total of 46 petabytes of raw data overall for 2026 (including scouting data), all successfully recorded and concluded by end of July. Central resources also generated about 55 billion Monte Carlo events. The strategy of avoiding AOD/MiniAOD output where possible saved roughly 30 petabytes of storage space (skipping ~40% of such output). About 42 billion existing Monte Carlo events were re-derived with a refined NanoAOD version. CPU usage was dominated by Run 3 Monte Carlo production, with Run 3 data processing, Run 2 Ultra Legacy Monte Carlo, and analysis contributing additional shares. The strategy of expanding Tier-0 overflow continued, this round extending beyond Tier-1 to a few selected Tier-2 sites; core usage peaked above 550K cores, driven significantly by HLT and opportunistic resources (about 10% of total pledged resources).

Preliminary 2028 resource request: the plan relies on already-pledged CPU resources (including the HLT farm) to cover Monte Carlo production needs, including for CSA28 (analysis and exercise use). Disk requests include a modest increase for both Tier-1 and Tier-2 to support analysis of 2027 reprocessed data and storage of mini-NanoAOD for CSA challenges. An additional 26 petabytes of tape is foreseen to support storing CSA data products and newly generated Run 3 data.

Mitigation strategy: for the short term, CMS aims to keep tracking technology trends and interacting with sites (via the CMS Computing Resources Board) to adjust plans; 2027 needs are viewed as reasonably likely to be met, but 2028 carries more uncertainty due to hardware price/availability risk. No additional resource request is anticipated for the luminosity ramp-up phase in the near term. For an anticipated tape shortfall, CMS expects to need to launch (and run at a higher frequency than currently planned) tape-deletion campaigns. For an anticipated disk shortfall, three handles were identified: accelerating the shrink of locally-managed storage while increasing centrally-managed storage (relative to pledges), reducing the on-disk lifetime of datasets, and — as a last resort, with a potential negative impact on end-user analysis — retiring/removing datasets. For the longer term, the group plans to update its projections once WLCG resource projections become available (toward end of 2027 / early 2028), incorporating relevant R&D efforts. The transcript ends mid-sentence during a statement that CMS is already facing a significant [storage] shortfall attributed to "the well-known..." (cause not captured).

## Open Questions

- Root cause of the PLAT/PPD job crashes at CERN remains unresolved; both a site/machine-level cause (VM misconfiguration, disk/RAM issues) and a code-level cause (thread-stack collision/stack overflow) remain open hypotheses to be tested.
- Whether CMS or CERN offers support (e.g., professional-version licenses) for project-management tooling such as Open Project is an open question raised by Daniel Elvira, pending a response from Frank Hartman and others.
- The cause of the storage shortfall CMS is "already facing," referenced at the point the transcript cuts off, is not captured.

## Related

[[CMS]] · [[WLCG]] · [[CERN]]

## Source

meeting_saved_closed_caption.txt (from `2026-08-26 15.37.40 CMS O&C Weekly Meeting`)
