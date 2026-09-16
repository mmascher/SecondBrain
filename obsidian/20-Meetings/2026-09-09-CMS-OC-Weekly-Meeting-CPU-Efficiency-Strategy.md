---
type: meeting
date: 2026-09-09
participants:
  - Stephan Lammel
  - Stefan (Purdue)
  - Kevin Pedro
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Stefano Belforte
  - Christoph Wissing
  - Matti Kortelainen
  - James Letts
  - Alan
topics:
  - CPU efficiency
  - resource utilization strategy
  - pilot oversubscription
  - I/O and data placement
  - HTCondor scheduling
  - workload management
  - memory provisioning
  - CO2/energy footprint
---

# CMS O&C Weekly Meeting — CPU/Resource Efficiency Strategy Discussion

## Summary

This session of the CMS Offline & Computing weekly meeting was a wide-ranging brainstorming discussion about how to define, measure, and improve CPU/resource efficiency across CMS submission infrastructure, framed explicitly by the chair (Stephan Lammel) as an effort to identify a medium/long-term strategy rather than short-term fixes. Topics included: what metric should define "efficiency" (raw CPU busy-ness vs. real throughput vs. CPU cycles/instructions delivered vs. events produced), CO2/energy footprint as an emerging but not-yet-actionable consideration, I/O and data-placement strategies (remote I/O vs. local caching vs. ATLAS-style data pre-placement), possible new HTCondor scheduling capabilities, dynamic/responsive autoscaling of pilots, resource-requirement characterization (memory, cores) for jobs, pilot oversubscription levels, and policy questions around inefficient jobs and user/analysis workflows. No concrete technical solution was adopted; the group agreed to continue the discussion offline in smaller groups and bring a proposed strategy back to a future Offline & Computing meeting.

**Note on transcript speaker attribution:** the closed-caption transcript attributes a large share of the discussion's content to "Stephan Lammel," including some material that other participants explicitly refer to in the third person as having come from someone named "Dima" (also transcribed once as "Tima"), who is never given his own speaker label in this transcript. This suggests a diarization/captioning artifact rather than that Stephan Lammel authored all of that content personally. Where the note below attributes substantive technical points to "Stephan Lammel / Dima (per transcript labeling)," this reflects that uncertainty rather than a confirmed single-author attribution.

## Decisions / Conclusions

- No specific technical or policy changes were decided in this meeting.
- The group agreed on a process: follow up offline between a subset of groups to work out a proposed efficiency strategy, then bring it back to a future Offline & Computing (or weekly) meeting for group-wide agreement.
- Stephan Lammel stated that root-cause efficiency analysis and strategy work should be done "for ourselves," not primarily to satisfy LHCC/scrutiny reporting.

## Action Items

- [ ] Raise the idea of a new HTCondor job/slot state (e.g., a "transferring" state allowing a new job to start on a slot while the previous job's output is still transferring) with the HTCondor developers at the biweekly WM/HTCondor developers meeting — Marco Mascheroni
- [ ] Add the StepChain/TaskChain trade-off study (independent tasks vs. fully dependent steps) to the shared Google Doc — Alan
- [ ] Check the CPU-cycle-equivalent efficiency metric/monitoring link shared in the document (previously presented by Luis in a general meeting) — Stephan Lammel
- [ ] Add further efficiency-strategy ideas to the shared Google Doc and notify Daniel and Stephan Lammel — all participants

## Discussion

### Framing and goals

Stephan Lammel opened by stating the goal was not to find short-term fixes but to identify a medium/long-term strategy, with medium-term implementation steps toward it. He raised, as a secondary but growing consideration, CO2/energy footprint of computing (referencing momentum from a talk at ICHEP), suggesting CMS should at least begin monitoring/collecting this information and how it is measured, even though it isn't yet actionable at job granularity.

### What should "efficiency" mean?

Several participants converged on the idea that CMS lacks an agreed definition of the metric to optimize. Points raised (attribution per the caption artifact noted above, likely including "Dima"):
- Simply keeping CPUs/threads "busy" is not a good proxy for efficiency, since it's possible to fill slots in ways that thrash caches and make throughput worse.
- A better metric would be something closer to real throughput — events produced per CPU cycle, or instruction throughput relative to what a workflow actually requires — rather than raw utilization percentage.
- James Letts characterized the problem as inherently multidimensional (CPU, disk, memory, and — soon — GPU), following a Pareto-optimization framing: improving efficiency along one axis (e.g., disk, via remote reads of premixed pileup libraries) has previously come at the cost of another (CPU efficiency). He argued the group's real figure of merit is event throughput, and cautioned that adding GPU offload will likely further reduce CPU-utilization numbers even while increasing overall throughput. He also relayed an anecdote (a ~10-year-old exchange with HTCondor developer Miron Livny) as a prompt to first write down concretely what problem the group is actually trying to solve, rather than jumping to solutions.
- Christoph Wissing similarly stressed the need to first agree on the metric to optimize, and to distinguish between optimizing for CMS's actual benefit versus optimizing merely to pass LHCC reviews.
- Stephan Lammel later proposed that a CPU-cycle/instruction-based metric (comparing instructions/cycles a workflow needs vs. what is actually delivered) could be a cleaner, easier-to-compute proxy than counting produced events, and would better isolate the effect of "trashing" resources (e.g., cache thrashing from oversubscription).
- Kevin Pedro cautioned that using more cores/cycles is not itself a win if it doesn't translate into more events; the tradeoff between "run more efficiently but produce fewer events" and "produce more events but waste some cores" is a real decision, not a free lunch, and requires moving to a new Pareto front rather than just accepting a tradeoff.
- Antonio Perez-Calero Yzquierdo noted that "throughput" itself needs a precise definition: an individual job may look slower under oversubscription/pilot overloading even though aggregate throughput across all jobs sharing the pilot is higher.
- Multiple participants (Matti Kortelainen, Christoph Wissing, Stefano Belforte) explicitly called for a detailed, root-cause understanding of exactly where CPU efficiency is currently being lost before prioritizing specific optimizations. Marco Mascheroni raised the same difficulty from a different angle: without knowing where a "smoking gun" inefficiency is, it's hard to prioritize among many possible optimizations, and it's possible no single smoking gun exists — only that sufficient studies haven't yet been done.
- Antonio noted that CMS has an equivalent efficiency metric now available in monitoring (link shared by Marco Mascheroni in the shared document); Luis had previously presented on this in a general meeting.

### I/O, data placement, and caching strategies

Stefan (Purdue) raised remote I/O as an increasingly important factor given USCMS's move toward concentrating storage at Fermilab with compute at Tier-2 sites (e.g., Purdue, Caltech); he proposed a staging mechanism where a job would not start running until its input files are already present locally at the site.

This led to an extended discussion, with Stephan Lammel/Dima (per transcript labeling) working through what this would mean in practice:
- It was noted this is close to the ATLAS model of pre-placing data before a job is even submitted/started.
- A concern raised: if a job holds its allocated CPU slot while waiting for data to be staged in, that CPU time is wasted; if instead the job is not yet allocated a slot while staging happens, scheduling becomes more complex because it now depends on where the data physically is, reducing the current flexibility to run CMS workflows at nearly any site.
- Antonio Perez-Calero Yzquierdo summarized the underlying idea as: don't materialize/inject a job into the HTCondor queue until required conditions (fully identified resource requirements, input data already staged at a nearby site, etc.) are met, so that once a job is queued it is guaranteed to run under near-optimal conditions.
- Marco Mascheroni suggested this might require new HTCondor functionality — e.g., a "transferring" slot/job state that lets a new job start on the same slot while the previous job's output is still being transferred out, to avoid wasting slot time during stage-out. He proposed raising this with the HTCondor developers at the biweekly developer meeting.
- Stephan Lammel cautioned this pushes the problem back onto workload management (deciding what data/pieces are needed before starting) and, if data locality becomes a hard precondition, could remove flexibility to run anywhere regardless of data placement — a trade CMS has relied on operationally.
- Stephan Lammel/Dima also connected this to CVMFS cache pre-warming (e.g., pre-filling the CMSSW/Singularity image cache on the worker node) as a related but distinct "caching" concept, separate from data pre-placement.
- James Letts's premixed-pileup example (remote reads saving disk but costing CPU efficiency) was cited multiple times as a concrete instance of this I/O-vs-CPU tradeoff, and as a reminder of why the deep causes of inefficiency haven't already been fixed.

### Dynamic/responsive scheduling

Kevin Pedro argued that fixed-size pilots (even with static oversubscription) may not be sufficient to fully utilize resources going forward, and proposed something more responsive/automatic that rescales jobs, pilots, or slots on the timescale of minutes based on live monitoring — drawing an analogy to work done with GPU-usage metrics in the "SuperNIC"/SONIC-type context (referred to in the transcript as "supersonic"), where auto-scaling decisions are made on a timescale of minutes rather than the ~48-hour timescale typical of current pilot management. He noted this has implications for workload management, for CMS software (e.g., changing job thread counts on the fly), and requires low-overhead, fast decision-making.

Antonio Perez-Calero Yzquierdo connected this to the existing "pilot overloading"/oversubscription strategy: since the deep causes of payload inefficiency haven't been fixed, CMS has instead pushed more payloads into each pilot; he suggested going further with more sophisticated, dynamic overloading (adding boundaries between payloads, pushing additional work into a pilot dynamically) as a way to react to and extract value from unavoidable inefficiency, rather than eliminating its root cause.

### Resource-requirement characterization

Alan (attendee joining partway through) identified poor characterization of workflow resource requirements (leading to systematic over-allocation relative to actual usage) as a major, widely shared pain point, distinct from raw scheduling speed. He noted CMS is already planning mechanisms — referred to as a "scouting"/"assembling" strategy — intended to reduce this over-allocation, and that this is already documented in a requirements Google Doc.

Alan also referenced prior/ongoing studies comparing StepChain and TaskChain-style workflow construction (a spectrum from fully independent tasks to fully dependent steps), which reveal various trade-offs (e.g., maximizing resource utilization vs. maximizing throughput vs. minimizing disk footprint, and potential for policy-driven workflow composition). He noted this kind of flexible workflow construction is expected to be native in DIRACX (referred to in the transcript as "JiraCAX," likely a mis-transcription), and committed to adding this material to the Google Doc.

Antonio Perez-Calero Yzquierdo added that evidence suggests jobs typically request roughly 2x more memory than they actually use, and argued the more promising lever may be larger pilot/slot sizes (already increased at Tier-1 sites) extended to more of the grid, rather than requesting more memory per core.

### Memory provisioning and oversubscription

Stephan Lammel outlined several strategic ideas he had entered into the shared document, including:
- Smarter, unified job wrappers that overlap the startup (e.g., Singularity container start) of the next job with the shutdown of the previous job on the same slot, since both are largely non-CPU-bound.
- Adjusting CVMFS cache sizing, which is currently sized per core, to account for higher oversubscription levels so the cache isn't thrashed.
- A policy that disadvantages inefficient/problematic jobs, e.g., limiting the number of simultaneous instances of an inefficient job (pushing responsibility back to the requesting physics group or Monte Carlo generator team to improve efficiency), or preferentially routing inefficient jobs to less powerful/older CPUs so their relative efficiency appears higher (noting this doesn't help if the bottleneck is something like cache-line thrashing rather than raw CPU cycles).
- Requesting a higher memory-per-core ratio for future hardware purchases, noting ATLAS already does something similar indirectly via memory-specific batch queues at sites.
- Using freed-up disk space to overlap job stage-out with the next job's startup (largely CPU-light), an idea to investigate with the HTCondor team.
- Increasing pilot oversubscription (current level described as ~25% oversubscription running multiple jobs per 8-core pilot) — e.g., by raising the default per-job memory request (e.g., from 3GB to 4GB, with part of the 4GB usable as swap) to enable higher oversubscription (he suggested up to ~50%).

Matti Kortelainen pushed back on treating memory like CPU/disk: memory must be provisioned for peak usage (a job exceeding its memory request gets killed), so some reserve is expected and unsurprising; the real problem is that actual memory needs are not known before a job runs. Stephan Lammel responded that swap space could let peak memory usage be absorbed without killing the job (at some performance cost), enabling more aggressive oversubscription. Antonio Perez-Calero Yzquierdo was skeptical that requesting more memory was the priority lever, preferring larger pilot/slot sizes instead (see above), and noted the topic requires care around c-group-based isolation to avoid spiky memory usage from one job killing others sharing a pilot or worker node.

### Validation and site heterogeneity

Antonio Perez-Calero Yzquierdo asked whether workflow validation before injection into WM/queues happens on specific, controlled machines (e.g., at CERN) or under realistic, wide grid conditions, and whether this affects the accuracy of resource-requirement estimates (runtime, memory). Stephan Lammel/Dima stated there is no strict validation process except for Monte Carlo campaigns.

Stephan Lammel/Dima also described a Tier-0-focused efficiency study: even a "trivial" pure-reconstruction workflow reading only from CERN does not reach 90% efficiency (current level described as around 80%, "8" in the transcript is understood as roughly 80%); site-to-site efficiency for the same workflow varies substantially (Leonardo performed differently from Tier-1 sites like "Tirjuana Kraff," attributed to network-related effects), and real CPU performance varies by roughly a factor of up to three across different CPU models even when core counts match, adding another dimension that is hard to control for. The conclusion drawn was that with multi-dimensional, multi-step production workflows, isolating individual causes of 5–10% efficiency differences is very difficult unless a much larger (factor of 2–3) discrepancy exists.

### Policy, physics needs, and user workflows

Stefano Belforte argued that if CPU efficiency were already at 90%, this discussion would not be happening, and that the group lacks a clear, current picture of its main inefficiency causes; he advocated an iterative approach — first fix the biggest known problems, then reassess. He argued CMS needs to move away from a 20-year-old model of "submit whatever is given to us and cross fingers" toward actively testing, measuring, and — where necessary — pushing back on workflows that cannot be run efficiently, including telling users, PPD, or physics groups that something needs to change. He also noted that user/analysis workflows currently have very low CPU efficiency and consume about 30% of resources, and argued that either their share of resources should be capped, or they need to be managed with the same level of control as production workflows (e.g., disallowing patterns like running a Singularity container inside another Singularity container for short, ~5-minute jobs) — acceptable in isolation but problematic at the scale of hundreds of thousands of jobs.

Stephan Lammel/Dima responded that, from long experience, physicists generally do not prioritize efficiency — if told they'd get half the needed events, most would still proceed, and specific requests (e.g., a particular generator version) will be made regardless of known inefficiency; CMS needs to accept and plan around this reality rather than expect physics requirements to change to suit efficiency goals. He also noted that even without changing user behavior, the group expects to continue "leaving on the table" resources roughly comparable in scale to run-to-run variation and to ongoing physics requests for known-inefficient legacy generator versions.

Christoph Wissing added that beyond agreeing on a metric, the group needs to distinguish clearly between policy and exceptions to policy, and — critically — decide in advance who has the authority to override a policy, rather than resolving that only after the fact (to avoid a situation where someone is pushed into overriding a policy and then blamed for it). He suggested prototyping a small number of concrete technical ideas (e.g., a system that automatically adjusts priorities based on degrading efficiency) with proper monitoring so that questions arising during the process can be answered.

Marco Mascheroni proposed an additional idea: declaring a target efficiency for a workflow and aborting/flagging it if the first ~20% of jobs run significantly below that target, as a preemptive tool to catch unexpected problems early (distinct from routine production variance) and help debug efficiency issues in the system.

### Scale of the opportunity

Stephan Lammel argued that the submission-infrastructure model, effective at the start of Run 1, is showing its age, and that CMS has been losing efficiency gradually over the last 10–15 years, likely worsening into the High-Luminosity LHC era; he called this a good time for a "coarse adjustment." He noted even 10% of ~500,000 cores is larger than CMS's biggest Tier-1 site, framing this as a case for pursuing even structural fixes (e.g., network or switch reconfiguration) if they could recover resources at that scale.

## Open Questions

- What is the right metric (or metrics) to define and optimize for CMS efficiency — raw utilization, CPU-cycle/instruction throughput, or event throughput — and how should CO2/energy footprint eventually factor in?
- Where exactly is CPU efficiency currently being lost? Multiple participants agreed this root cause has not been established with confidence.
- Should CO2/energy footprint be tracked now even though it isn't yet actionable, and how would it eventually be measured per job?
- Should user/analysis workflows be capped at a smaller resource share, or managed under the same operational controls as production workflows?
- Who should have the authority to grant exceptions to any new efficiency-related policy, and how should that be decided in advance?
- Is a data/job pre-placement or staging model (à la ATLAS) worth pursuing given the loss of scheduling flexibility it would likely introduce, or is a more demand-driven caching approach preferable?
- Is increasing default per-job memory requests (to enable higher oversubscription) a worthwhile lever, or is increasing pilot/slot size a better path (disputed between Stephan Lammel and Antonio Perez-Calero Yzquierdo)?
- Whether/how validation of workflows prior to injection into WM should be made more representative of real grid heterogeneity.

## Related

[[CMS]] · [[HTCondor]] · [[WMAgent]] · [[Workload Management]] · [[Pilot Jobs]] · [[CVMFS]] · [[DIRACX]] · [[GPU]] · [[Heterogeneous Computing]] · [[Resource Provisioning]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-09 15.27.40 CMS O&C Weekly Meeting`)
