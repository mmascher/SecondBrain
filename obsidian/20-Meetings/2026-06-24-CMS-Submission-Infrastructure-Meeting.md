---
type: meeting
date: 2026-06-24
participants:
  - Marco Mascheroni
  - Jaime Frey
topics:
  - memory footprint and cgroups scheduling
  - pilot lifetime renewal
  - scheduler load balancing
  - condor_transfer_data behaviour
---

# CMS Submission Infrastructure Meeting

## Summary

A one-on-one sync between Marco Mascheroni and Jaime Frey, explicitly framed by Marco as a brainstorming session covering ideas raised at a recent CMS face-to-face management meeting. Topics included possible strategies for coping with growing job memory footprints, an idea for extending pilot lifetime on the fly, generalizing CMS's scheduler load-balancing algorithm, and a question forwarded from the DIRAC team about `condor_transfer_data` behaviour. Marco also noted that no infrastructure changes had been made recently because Florian's replacement has not yet been hired, and that he intends to bring more people into future instances of this meeting.

## Decisions / Conclusions

- No formal decisions were reached on the memory-scheduling or pilot-lifetime ideas; both were raised as brainstorming proposals for possible future work.
- HTCondor has no built-in, default notion of a maximum job lifetime/runtime; enforcing a runtime limit is entirely up to custom configuration by each site/pool administrator, not something addressed by core Condor development.
- The walltime parameter set in the factory generally does not get used for Condor-based sites; it is meaningful for Slurm sites.
- On-the-fly extension of a pilot's runtime does not fit well with how Slurm typically schedules jobs, since Slurm maintains a schedule of which jobs run next; Jaime was uncertain whether Slurm could support such extension, noting he has limited hands-on Slurm experience.
- As of a recent HTCondor release (Jaime said "just in the 25X series"), a successful `condor_transfer_data` now allows the job to leave the queue shortly afterward. Previously, calling `condor_transfer_data` did not affect the job remaining in the queue, which caused user complaints because they had to explicitly run `condor_rm` afterward to remove the job once its output was retrieved. Prior to the change, running `condor_transfer_data` multiple times on the same job simply resent the same set of files each time.

## Action Items

- [ ] Reply to the DIRAC team's email ("Question about repeated use of condor data transfers pool") explaining the recent `condor_transfer_data` queue-removal behaviour — Marco Mascheroni
- [ ] Write an email to Greg Thain (CC Jaime Frey) laying out the idea of scheduling partitionable-slot jobs based on average rather than peak memory utilization — Marco Mascheroni

## Discussion

### Memory footprint and cgroups-based scheduling

Marco reported that CMS management discussed the likelihood that the memory footprint of payloads will increase — from a current rule-of-thumb of ~2 GB/core on the grid to possibly 5–10 GB/core at peak, though it's unclear how large or frequent that peak usage will be. He noted the increase is expected mainly in the reconstruction step of step-chain jobs, not the generator step. He raised the idea of allowing a single job in a partitionable slot to exceed its requested memory for a period of time rather than scheduling strictly on peak memory usage (which he argued wastes memory when peaks across jobs don't overlap), with jobs killed only if too many jobs go over memory simultaneously. He proposed doing scouting/profiling of jobs' memory usage (peak, spread, duration of peak, average) to inform whether such scheduling would be worthwhile.

Jaime noted this is closely tied to how cgroups memory enforcement and monitoring works, an area primarily handled by Greg Thain, and said he could not comment on it in detail himself. Greg Thain had also recently emailed Marco with feedback on Marco's HTCondor Week presentation; Marco plans to reply and raise this idea with Greg, with Jaime in CC.

Jaime asked whether Marco had profiling data showing how long jobs run at high memory and how far above average they peak. Marco said this was only a guess based on job structure (e.g., ~7–8 hours for the gen part, ~1 hour for reconstruction, then other non-memory-intensive step-chain parts) and that proper profiling would be needed before deciding whether the approach is worth pursuing.

Marco also referenced a past lightning talk by a student (name not captured in the transcript) that measured job throughput based on memory request/estimation, and suggested that a similar simulation-based study — comparing throughput and job-kill rates under peak-based vs. average-based scheduling — could be a useful extension of that work.

### Pilot lifetime renewal

Marco raised an idea discussed previously at CHEP: when a pilot is submitted for a shorter duration than it may need (e.g., started for one or two days out of a possible three), the batch system could be asked on the fly to extend the pilot's lifetime, reducing efficiency losses during pilot draining. He proposed potentially prototyping this with Condor batch systems first, to then make a case to other systems.

Jaime said he had not heard this discussed before and explained that Condor does not have a default built-in concept of maximum job lifetime — this is fully dependent on custom pool policy set by individual site administrators (e.g., at CHTC and in the OSG pool, policies exist for jobs requesting a given runtime, but these are custom to each pool). Enforcement is typically via eviction once a job runs longer than an execution point's configured policy. Marco confirmed there is a "walltime" parameter set in the factory, but Jaime said this generally isn't used for Condor sites — it matters for Slurm. Jaime also expressed doubt that Slurm could easily accommodate on-the-fly lifetime extension, since Slurm's scheduling depends on knowing job durations in advance to schedule subsequent jobs, though he noted limited direct Slurm experience.

### Scheduler load balancing

Marco described the current model where WMAgent runs on the same machine as the scheduler, and CRAB similarly uses a single process submitting all workflows. He noted the new (remote submission) system being planned will decouple this, and that not all submissions will fit on one scheduler. He recalled having previously implemented an algorithm (referenced in a chat link during the meeting) that selects a scheduler from a pool of ~20–30 based on weighted factors such as memory and number of running jobs, though he did not recall the exact algorithm. He asked whether this kind of load balancing could be generalized and be of interest to the HTCondor development team, mentioning CMS Connect (where users SSH into a single large machine) as another case that might eventually need to be split across multiple schedulers.

Jaime described CHTC's typical practice: assigning each user to a single access point/scheduler, manually load-balancing new users onto less-loaded access points, adding new access points when load gets too high, and giving dedicated access points to research groups with heavy processing needs. He confirmed this is a manual process with no automated farming-out mechanism. Jaime noted the main technical difficulty with load balancing a single submitter across multiple SCHEDDs is the lack of good tooling to track which jobs went to which SCHEDD — normal tools like `condor_q` don't easily monitor jobs spread across multiple SCHEDDs, since a user would need to know which SCHEDD to query for a given job. He suggested this could be an interesting area for development: building a simple interface (command line or Python bindings) that hides load-balancing mechanics from the user while preserving the familiar job-status-checking experience.

Marco reiterated this is not urgent but could become relevant for both single-user SSH access points (e.g., CMS Connect) and tools like CRAB/WMAgent as they evolve, and encouraged Jaime to consider allocating development effort if he found it interesting, noting the benefit would be shared broadly.

### condor_transfer_data question (relayed from DIRAC team)

Marco relayed a question from a DIRAC team meeting he had attended, regarding a use case where DIRAC's content developers submit pilots directly to the CE via `condor submit` (JDL) and monitor progress themselves, rather than using a scheduler on the factory (a different model than CMS's Condor-G-based approach). They use `condor_transfer_data` to retrieve stdout/stderr and asked what happens if it is run multiple times — specifically, whether output could be deleted.

Jaime explained this behaviour changed recently: previously, calling `condor_transfer_data` did not cause the job to leave the queue, requiring users to run `condor_rm` explicitly afterward, which had generated complaints. As of a recent (~25X series) HTCondor release, a successful `condor_transfer_data` now allows the job to leave the queue shortly after. Prior to this change, running the command multiple times on the same job simply resent the same set of files each time. Jaime said HTCondor would be open to adding an option to `condor_transfer_data` to prevent the job from leaving the queue, if there is interest in that behaviour. Marco said he would reply to the DIRAC team's email directly rather than having Jaime do so.

### Team and organizational notes

Marco noted no recent changes had been made to the infrastructure because Florian's replacement has not yet been hired, so he has mainly been watching the global pool. He said he intends to involve more people in future instances of this meeting, since it has become a one-on-one discussion; he mentioned that once Florian's replacement joins, and potentially the new factory operator Luis, they could participate, including on Condor-related debugging/development work for the factory. He also mentioned an upcoming DIRAC hackathon the following week and a related email exchange he was following up on.

## Open Questions

- Whether jobs in partitionable slots could be safely allowed to exceed requested memory temporarily, and how much benefit this would provide — depends on profiling data on peak memory duration, spread, and frequency that has not yet been collected.
- Whether extending the earlier student lightning-talk work into a simulation comparing peak-based vs. average-based memory scheduling throughput would be worthwhile.
- Whether pilot lifetime extension is technically feasible with Slurm, given its scheduling model.
- Whether the HTCondor development team would be interested in generalizing/building first-class support for scheduler load balancing and cross-SCHEDD job monitoring tooling.

## Related

[[HTCondor]] · [[CRAB]] · [[WMAgent]] · [[DIRAC]] · [[Factory]] · [[Pilot Jobs]] · [[Submission Infrastructure]] · [[Jaime Frey]] · [[Marco Mascheroni]]

## Source

meeting_saved_closed_caption.txt (from `2026-06-24 18.08.31 CMS Submission Infrastructure meeting`)
