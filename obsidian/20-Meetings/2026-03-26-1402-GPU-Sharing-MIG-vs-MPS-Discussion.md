---
type: meeting
date: 2026-03-26
participants:
  - Antonio Perez-Calero Yzquierdo
  - Marco Mascheroni
  - Florian Von Cube
  - Manuel Giffels
  - Robin
  - Tim Voigtländer
  - Artur Gottmann (KIT)
  - Luís Simas
topics:
  - GPU sharing
  - MIG
  - MPS
  - GPU utilization metrics
  - HTCondor partitionable slots
  - KIT GPU cluster
---

# GPU Sharing: MIG vs MPS Discussion

## Summary

Tim Voigtländer (KIT), author of a recently submitted thesis on GPU partitioning, walked the CMS Submission Infrastructure group (Antonio, Marco, Florian, Manuel Giffels) through his findings on sharing a single GPU across multiple processes, comparing MIG (hardware-level partitioning) and MPS (context-fusing software sharing), together with Robin and Artur Gottmann from KIT who added operational experience from KIT's GPU cluster and the CMS HLT farm. The discussion focused on which GPU-utilization metrics are reliable, how MPS could map onto HTCondor partitionable slots, and what a first practical test from the Submission Infrastructure side could look like.

## Decisions / Conclusions

- Time-slicing multiple processes on a single GPU without any optimization (the naive baseline) does not improve throughput: GPU utilization stayed flat (~10%) while runtime increased nearly linearly with the number of processes, in Tim's tests.
- The standard NVIDIA SMI "graphical activity" utilization metric is unreliable once more than one process shares a GPU (it can read close to 100% even when no more work is being done); it remains the de facto standard mainly because it is the only metric accessible without elevated/root privileges.
- More accurate metrics — Streaming Multiprocessor (SM) activity and SM Occupancy, both available via NVIDIA DCGM — require privileged (sudo/root) access and are therefore not usable for arbitrary grid payloads.
- KIT's GPU-as-a-Service benchmarking work concluded that GPU power draw (relative to TDP) is currently the best easily-accessible utilization metric that does not require elevated privileges, though this is not a finalized/official standard. Power draw cannot be attributed to a specific job when a GPU or slot is shared among multiple processes.
- MIG (Multi-Instance GPU) partition configurations are rigid, fixed at setup time, hardware/GPU-model-specific (A100, A40, H100 each have different valid partition tables), and reconfiguration requires restarting GPU-accessing applications (including HTCondor). Tim's assessment, shared by Robin, is that MIG is not suitable for dynamic/flexible slot allocation in a grid context.
- MPS (Multi-Process Service) fuses multiple process contexts into one daemon-managed context, allowing kernel calls from different processes to run concurrently rather than being time-sliced sequentially. In Tim's tests, MPS scaled utilization roughly linearly with the number of concurrent processes while individual process runtime stayed constant, even with 12 concurrent processes on one GPU.
- MPS supports a per-process hard memory limit (`CUDA_MPS_PINNED_DEVICE_MEMORY_LIMIT`); when a process exceeds it, only that process is stopped and other MPS-shared processes are unaffected. Tim recommends using GPU memory as the primary/limiting metric for job placement, rather than compute-utilization limits, because exceeding a memory limit is fatal (crash) while exceeding a utilization limit only degrades performance.
- Attempts to additionally cap active-thread/utilization percentage per MPS process did not produce reliable limiting behavior in Tim's tests (Robin confirmed this is only a "suggestion," not an enforced limit); memory remains the practical, enforceable control.
- MPS works regardless of whether the daemon is started inside or outside a container, as long as the container has access to the daemon's pipe directory; Tim measured no performance difference between the two setups.
- MPS is CUDA-specific; alternative/open-source implementations mentioned (e.g., "G-Safe"/"G-Guardian") also appear to rely on CUDA. Robin confirmed the CMS HLT farm already runs MPS (with ~6 shared instances per machine), replacing an earlier setup without it.
- At KIT (Manuel Giffels), grid jobs that request a GPU without specifying a VRAM amount currently receive a full GPU via the TARDIS meta-scheduler integration.
- HTCondor partitionable slots are not stackable; Tim's KIT setup gives each physical GPU its own partitionable slot (rather than one partitionable slot spanning all GPUs on a machine), meaning jobs can share a GPU sub-sliced by requested memory, but a single job cannot span GPUs assigned to different partitionable slots/startds.
- Robin and Antonio noted that, at least currently, CMS grid payloads are not expected to require more than one GPU per job (multi-GPU training workloads are considered out of scope for the near term); Marco agreed multi-GPU training is likely several years away and tied to future WM system evolution, so the team should keep the initial approach simple and focus on staying within GPU memory limits.
- Artur (KIT) noted that GPU workloads run on KIT resources so far (as offline jobs) have not been computationally heavy and likely would not approach 100% GPU utilization even when several MPS "slices" are stacked on one device, suggesting there is room to test MPS slicing further.

## Action Items

- [ ] Test running two GPU jobs sharing one GPU via a manually started MPS server inside a job, as a first, simplified validation of the approach (without the full partitionable-slot/memory-limit setup) — Submission Infrastructure team (no single owner stated)

## Discussion

### Context and motivation

Antonio opened by referencing a slide/graph shared previously at a CMS computing week session on the future of submission infrastructure, framing the group's interest as understanding how GPU-partitioning choices made at the site level (MIG-style hardware partitioning vs. MPS-style software sharing) affect what CMS pilots discover and how the Submission Infrastructure team can maximize utilization of GPU devices assigned to CMS pilots, whether a full device or a pre-configured slice. Marco added the goal was to understand where partitioning configuration lives (site vs. pilot) and learn from people with hands-on experience — prompting Tim to offer to walk through his recently submitted, publicly available thesis on GPU partitioning (MIG and MPS).

### GPU utilization metrics

Tim described three NVIDIA utilization metrics: (1) the standard NVIDIA SMI "graphical activity" percentage, widely accessible but unreliable with more than one process per GPU (it can spike toward 100% without proportional extra work); (2) Streaming Multiprocessor (SM) activity, obtained via DCGM, more reliable but requiring elevated access; (3) SM Occupancy, similar to SM activity but reporting per-SM utilization rather than simple active/inactive. Tim's thesis primarily relied on SM activity. In response to Antonio's question about whether there is an agreed community standard, Tim said SMI graphical activity remains the practical default because of its accessibility, despite its known weakness under multi-process sharing.

Robin and Tim discussed access restrictions: DCGM-based metrics generally need sudo/root, which Robin's team (GPU-as-a-Service benchmarking) found unworkable given users without elevated access. Robin's team's conclusion was that GPU power draw relative to TDP is currently the best easily-accessible metric, though it also cannot disentangle usage between multiple processes/jobs sharing the same GPU or slot, and is not finalized as an official approach. Antonio asked whether power draw would be accessible to pilots/processes themselves; Robin confirmed it needs no special permissions, with the same caveat about shared slots.

### MIG (Multi-Instance GPU)

Tim explained MIG partitions a GPU into fixed hardware-level pieces, each behaving like an independent GPU with its own process/context. Configuration is defined by per-GPU-model tables (shown for the A100; different for A40/H100) and some configurations waste capacity (e.g., partitions that don't sum to the full available units). Reconfiguring a MIG layout requires restarting GPU-accessing applications, including HTCondor, and in Tim's testing this was sometimes blocked entirely by other services holding the GPU, in some cases requiring a machine restart. Tim's conclusion: MIG is not practically usable for dynamic allocation, since it must be set up once for a consistent workload pattern and does not adapt well to variable job sizes. Robin added that available MIG configurations differ substantially between GPU generations (A100 vs. H100/H200), reinforcing this rigidity. Antonio summarized the operational implication for Submission Infrastructure: pilots would receive whatever partition/slice (or full GPU) the site had already configured, with no ability for CMS to reconfigure or invent arbitrary partition sizes itself.

### MPS (Multi-Process Service)

Tim described MPS as fusing multiple process contexts into one daemon-managed context, allowing concurrent (rather than sequential/time-sliced) execution of kernel calls from different processes. He characterized it as more stable in practice than expected (a failure in one sub-process does not typically crash the whole daemon). In his measurements, MPS utilization scaled roughly linearly with the number of concurrent processes while per-process runtime remained flat, even at 12 concurrent processes on one GPU — in contrast to naive time-slicing, where runtime increased linearly and utilization stayed flat (~10%) regardless of process count.

In response to Antonio's questions, Tim confirmed MPS supports adding process instances dynamically over time (not requiring all workloads to be known upfront), and can be configured so that different users either share the same daemon or are routed to separate (time-sliced) daemons. Tim also described a per-process VRAM hard limit mechanism (`CUDA_MPS_PINNED_DEVICE_MEMORY_LIMIT`) that isolates jobs from each other for memory purposes: exceeding it kills only the offending process, leaving others unaffected. He proposed pairing this with a HTCondor pool variable (e.g., requested GPU memory) matched against total available GPU VRAM (e.g., 40GB for an A100, 32GB for a V100) to control how many jobs get matched onto a given GPU, aligning naturally with HTCondor's partitionable-slot model that Antonio confirmed is CMS's preferred mechanism.

Robin raised that MPS behavior/performance for a given job is not fully foreseeable since it depends on what else is co-scheduled on the same GPU; Tim agreed the benefit is large when co-scheduled workloads are individually light (e.g., many 5%-utilization jobs) but smaller (though still measurable) when workloads are already heavy (e.g., 98% + 50%). This tied into a side discussion about which GPU generation/size experiments are optimizing for and whether MPS-style pooling remains relevant as GPU capacity grows; Tim called this "future thinking" for pooling as newer, larger GPUs make single-job saturation less automatic.

Robin confirmed the CMS HLT farm already runs MPS in production (bare metal, MPS daemon running persistently), with roughly 6 parallel instances shared per machine — noting a 2022 CMS paper describing no performance improvement from multi-process GPU sharing likely predated or did not use MPS-style optimization, which Robin said is now standard on the HLT. Tim confirmed via his own container-based tests that MPS works the same whether the daemon runs inside or outside a container, and that starting the daemon does not appear to require root, as long as containers can reach the daemon's pipe directory. For machines with multiple GPUs, Tim noted a soft limit of ~48 processes per MPS daemon; the workaround is to run one MPS daemon per GPU with separate pipe directories, which in his tests preserved per-GPU performance.

MPS's main stated limitation is that it currently only supports CUDA applications; Marco noted CMS's portability layer (Alpaca) may still rely on CUDA underneath, which was not confirmed in the meeting. Robin confirmed the CMS HLT MPS deployment is CUDA-based.

### Mapping MPS onto HTCondor partitionable slots and grid pilots

Antonio worked through how this would translate into the CMS pilot/grid model: a pilot's `startd` discovers device resources on the worker node and advertises them as a partitionable slot within CMS's own HTCondor pool (the "global pool"), so scheduling/partitioning still follows CMS's own negotiator policies inside the glidein/pilot context. He raised whether, if a pilot is assigned only a slice of a machine (rather than the full machine), CMS's own `startd` would see the full machine or only the slice, and whether nested partitionable slots are possible. Tim confirmed partitionable slots are generally not stackable, and described his own KIT setup as giving each physical GPU on a machine its own partitionable slot (rather than one partitionable slot spanning all GPUs), so jobs draw from whichever GPU's slot has room, and multiple jobs can share one GPU as part of that GPU's slot — but a single job cannot span GPUs belonging to different slots/startds.

Manuel Giffels clarified that for grid jobs via KIT's TARDIS meta-scheduler integration, a job that doesn't request a specific VRAM amount currently receives a full GPU. Tim suggested that requesting a job with multiple stacked sub-processes, or later adding an MPS-aware service layer that knows how much memory a job needs, could allow partial GPU assignment, though he was not certain how grid-job/HTCondor interplay currently handles this at KIT.

Robin and Antonio agreed that CMS does not currently expect (nor is currently designing for) grid payloads requiring more than one GPU; Robin called multi-GPU support outside the team's current scope ("not at this level yet," and noted this is not an official/decided position). Antonio noted this doesn't preclude future multi-GPU partitionable-slot pilots (drawing an analogy to how CPU pilots evolved from single-core to multi-core partitionable slots), but agreed the near-term focus should stay on the single-GPU-per-job case.

### Practical next steps for testing

Marco summarized the plan for a first internal test: currently, the relevant CMS workflows request exactly one GPU per pilot (`RequestGPUs = 1`), so pilots start only one GPU job. A first, simple test would be to let two GPU jobs run concurrently by manually starting an MPS server inside a job and having two GPU processes access the assigned GPU — without the full partitionable-slot/memory-limit machinery Tim described — to check whether performance behaves as expected. Tim agreed this would be the simplest viable test, cautioning it wouldn't include the safeguards (e.g., memory limits) of a complete setup, but would validate the basic performance expectation if the workload is known to fit in a fraction of GPU memory.

Tim also noted a KIT-specific observation late in the discussion: the ratio between GPU utilization capacity and memory capacity matters — if memory allows stacking more processes than compute utilization can actually serve concurrently, throughput will not scale as expected even though nominal 100% utilization is eventually reached. Robin added a caveat that SMI utilization only indicates the absence of idle cycles, not a precise measure of how "full" the GPU actually is.

Tim agreed to share a link to his thesis, which covers the material presented.

## Open Questions

- Whether and to what extent CMS offline (non-HLT) payloads will need or benefit from GPU sharing via MPS is still unclear; the group agreed more real usage experience is needed.
- Whether CUDA-dependency of MPS is a significant limitation for CMS, given CMS's move toward other architectures/portability layers (e.g. Alpaca), was raised but not resolved.
- How grid-job requests currently interact with HTCondor/TARDIS for partial-GPU assignment at KIT was not fully clear even to Manuel Giffels.
- Whether utilization-based (in addition to memory-based) limits should also be used to control which jobs get matched onto a shared MPS GPU remains an open design question ("up for interpretation," per Tim).
- Whether/how a future GPU partitionable-slot model could support multi-GPU pilots is unresolved; considered a longer-term possibility, not a near-term requirement.

## Related

[[CMS]] · [[Submission Infrastructure]] · [[HTCondor]] · [[GPU]] · [[Heterogeneous Computing]] · [[Pilot Jobs]] · [[Monitoring]] · [[Dynamic Resource Provisioning]]

## Source

meeting_saved_closed_caption.txt (from `2026-03-26 14.02.18 Submission Infrastructure Weekly Meeting`)
