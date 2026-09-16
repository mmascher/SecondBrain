---
type: meeting
date: 2026-04-29
participants:
  - Marco Mascheroni
  - Jaime Frey
  - Luis Simas
topics:
  - ARM/ARC64 requirements in glideinWMS factory
  - GPU / MIG support in HTCondor
  - NVIDIA MPS
  - condor_gpu_discovery -divide option
  - job event log memory/usage attributes
---

# CMS Submission Infrastructure Meeting

## Summary

Marco Mascheroni and Jaime Frey (HTCondor developer) discussed a glideinWMS pull request that hardcodes ARC64 requirements for ARM factory entries, then covered how HTCondor handles MIG-partitioned GPUs, NVIDIA MPS, the `condor_gpu_discovery -divide` option, and how to correctly interpret memory/usage fields in the HTCondor job event log. Luis Simas, the new factory ops operator (replacing Viva, started around March 1st), joined partway through and asked follow-up questions related to his work monitoring overloaded pilots.

## Decisions / Conclusions

- For the ARM/ARC64 glideinWMS pull request, it is sufficient to explicitly set only the `Arch == "X86_64"` comparison (or the equivalent ARC64 comparison) in the submit description; HTCondor's default requirements expression only appends a sub-expression for a given attribute (e.g. `Arch`, `OpSys`) if that attribute is not already referenced anywhere in the submitted requirements. The rest of the default requirements will still be appended automatically.
- Marco leaned toward setting this ARC64 comparison in both the ARM and x86_64 cases, as future-proofing in case a factory is ever deployed on an ARM machine, though he characterized this as possibly over-engineering.
- MIG setup/teardown on a GPU must be done by the system administrator before HTCondor (or a glidein) starts; HTCondor/glideinWMS cannot switch a GPU between MIG and non-MIG mode. This applies both to bare-metal startds and glideins.
- `condor_gpu_discovery` automatically detects MIG-mode GPUs and reports only the MIG partitions, not the underlying physical GPUs — no special glidein configuration is needed for this detection to work.
- The one MIG-specific restriction (per Jaime, a CUDA library limitation, not an HTCondor one) is that no single process/job can use more than one MIG partition simultaneously. Jaime believed this restriction, along with MIG GPUs previously having unusual-looking names, may no longer apply in the latest CUDA library versions.
- `condor_gpu_discovery -divide` is unrelated to MIG. It makes HTCondor advertise more (virtual) GPUs than physically exist, each with a fraction of the real memory, relying entirely on user jobs not to collide — there is no enforcement. Jaime does not recommend using `-divide` in a glidein scenario for general-purpose use, due to risk of jobs from different users interfering with each other; it might be acceptable only in a constrained scenario (e.g. a pilot restricted to payload jobs from a single experiment/production, run by expert users).
- NVIDIA MPS (Multi-Process Service, used for GPU time-slicing) is not something HTCondor is aware of in any way; using it would happen entirely behind HTCondor's back.
- HTCondor is expected to correctly report/discover all GPUs and their properties (memory, CUDA capability) on a machine, including under MIG, via `RequestGPUs`/`RequireGPUs` matchmaking; a job can request all free GPUs via `RequestGpus = target.Gpus`. However, there is a known caveat: older HTCondor versions (Jaime mentioned the 24.x series specifically) running in the pilot may not correctly select MIG GPUs when the CE communicates which GPU to use to the pilot via `CUDA_VISIBLE_DEVICES` set to an integer — this only works correctly if MIG GPUs are referenced by their full UUID name instead. Jaime diagnosed a related problem at the University of Texas at El Paso in the past but has not tracked whether/where a fix landed, and suggested this is a question for Tim Cartwright regarding whether the default factory configuration handles MIG machines correctly.
- Pilots generally do not need to perform GPU matchmaking themselves: the glideinWMS factory already knows in advance whether a pilot will land on a GPU node and sets the requested GPU count for the pilot accordingly; GPU `RequestGPUs`/matchmaking based on GPU properties is done by the user/payload job, not the pilot.
- Regarding the HTCondor job event log: in the job terminated event (event ID 005), the reported "usage" is peak usage across all processes under the pilot (all pilot daemons plus all payload jobs that ran). "Memory" (not "memory usage") in that context is the amount of memory requested from/allocated by the worker node, corresponding to the submit description's request, not what the collector advertises (which in CMS's case is inflated due to overloading/overcommitting whole-node pilots to avoid stranding CPUs when jobs don't use their full requested memory).
- The job terminated event has three relevant columns per resource type: Usage (peak usage detected), Request (what was asked of the worker node), and Allocated (what the worker node actually gave, which can sometimes be slightly more than requested, to make it more likely a dynamic slot can be reused for a subsequent job).
- The separate "ad information" event (which Luis/Marco observed is emitted after the terminated event, and which they are using in their monitoring scripts because it is easier to parse than the terminated event) contains a mix of job-ad and slot-ad attributes; in it, "memory" corresponds to the amount of memory provided to the dynamic slot/job, and "memory usage" corresponds to the peak memory the job actually consumed. Jaime believes these are populated via a pilot configuration mechanism that copies selected slot-ad attributes into the job ad, likely at job launch time, and doubted that these copied values update afterward.
- Ad-information events triggered by a triggering job event (e.g. start executing, terminated) will reliably be emitted afterward, and their format is stable, though most-recently-emitted values (e.g. memory usage) may change over a job's lifetime — for values like peak memory usage, the copy following the terminated event should be used. Jaime confirmed this event does not carry all the information present in the terminated event, but agreed it contains enough for Luis and Marco's monitoring purposes.

## Discussion

### ARM/ARC64 glideinWMS pull request

Marco described a glideinWMS pull request (shared as a link in the chat) that hardcodes ARC64 requirements for ARM entries in the factory's condor_submit of the pilot startup script. This was prompted by the observation that the CERN compute element looks at the requirement string in the JDL to redirect pilots to the correct architecture resource — this requirement apparently propagates from the factory's condor_submit through the CE down to the underlying batch system (also HTCondor in this case). Since the factory itself runs on x86_64 hardware, and glideinWMS does not normally touch HTCondor's default requirements expression, Marco was concerned about overwriting the requirement and about robustness if HTCondor's default ARC64/x86_64 handling changes in the future. Jaime clarified how HTCondor's default requirements expression works per sub-expression (see Decisions above), resolving Marco's confusion about whether setting one comparison would suppress the rest of the default expression.

### GPU / MIG support

Marco raised this on behalf of the group's ongoing (but not yet significantly tested) interest in GPU support, specifically wanting to test MIG at a particular site whose name was not stated in the transcript. Jaime brought in TJ (present but not separately transcribed as speaking) as a resource for the MIG question. Marco explained glideinWMS currently runs `condor_gpu_discovery` mainly to detect GPU presence/errors, relying on the startd to re-run discovery and advertise full attributes to the collector. Jaime explained the general MIG behavior (see Decisions) and the `-divide` option's unrelated purpose.

Luis then asked a follow-up about how HTCondor handles multiple GPUs on one machine, wanting to detect all MIG-partitioned GPUs on a node and advertise that (dynamic) count so user jobs could request them. Jaime confirmed the general mechanism (RequestGPUs/RequireGPUs, startd assigns matching GPUs to dynamic slots via CUDA_VISIBLE_DEVICES) works the same way whether or not MIG is in use, but flagged the known older-pilot-version caveat with UUID vs. integer GPU addressing under MIG.

Marco also asked about NVIDIA MPS for GPU time-slicing; Jaime was unfamiliar with the term and confirmed HTCondor has no awareness of it.

### Job event log memory/usage semantics

Prompted by Luis's monitoring work on overloaded pilots, Marco and Luis worked through the meaning of memory- and usage-related fields across the job terminated event (005) and the associated ad information event (028), including the difference between requested, allocated, and peak-usage memory, and how CMS's whole-node overloading/overcommitment scheme (advertising more memory to the collector than physically reserved, to avoid leaving CPUs idle when jobs underuse their memory allocation) relates to these values. Marco and Luis are using the ad information event in their monitoring scripts because it is easier to parse than the terminated event, and confirmed with Jaime that it reliably follows triggering events and contains sufficient (if not complete) information for their purposes.

### Introductions and meeting cadence

Luis Simas was introduced as the new factory ops operator, replacing Viva, having started around March 1st. He is currently working on a project monitoring overloaded pilots, which motivated his questions. Marco noted this is a biweekly meeting between CMS and the HTCondor developers (Jaime and TJ) used to ask technical questions directly rather than going through the user support forum. Jaime noted he has login access to CERN machines and can sometimes help diagnose issues live between meetings, though this need has become less frequent as the system has stabilized compared to roughly 10 years ago when CMS was scaling up.

The next biweekly meeting was expected to be skipped (Marco will be at Fermilab in two weeks, and Luis will be on vacation), with the group planning to reconvene around May 27th or follow up via email if anything urgent arises in the meantime.

## Action Items

None explicitly assigned; Jaime suggested that whether the default glideinWMS factory configuration correctly handles MIG GPUs is "a question for Tim Cartwright," but this was not established as a committed follow-up.

## Open Questions

- Whether the default glideinWMS factory configuration correctly sets `CUDA_VISIBLE_DEVICES` (by UUID rather than integer) for pilots landing on MIG-enabled machines, and whether the older-pilot-version MIG GPU selection bug Jaime diagnosed at the University of Texas at El Paso has since been fixed.
- Whether it is worth setting the ARC64 requirement comparison for both ARM and x86_64 factory entries (future-proofing) versus only for ARM entries.

## Related

[[CMS]] · [[glideinWMS]] · [[HTCondor]] · [[GPU]] · [[Heterogeneous Computing]] · [[Factory]] · [[Factory Operator]] · [[Pilot Jobs]] · [[Submission Infrastructure]] · [[Monitoring]]

## Source

meeting_saved_closed_caption.txt (from `2026-04-29 18.05.09 CMS Submission Infrastructure meeting`)
