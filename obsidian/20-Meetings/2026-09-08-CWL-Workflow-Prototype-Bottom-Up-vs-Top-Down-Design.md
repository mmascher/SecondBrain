---
type: meeting
date: 2026-09-08
participants:
  - Marco Mascheroni
  - Vijay Chakravarty
topics:
  - CWL-based workflow definition for CMS job submission
  - Bottom-up vs top-down design approach
  - Marco's proof-of-concept (Request Manager based)
  - Vijay's workgraph.cwl (WMAgent job package based)
  - Relationship to the transformation system / DiracX
---

# CWL Workflow Prototype: Bottom-Up vs Top-Down Design Discussion

## Summary

Marco Mascheroni and Vijay Chakravarty compared two approaches to defining, in CWL (Common Workflow Language), the per-job step chain used for CMS job execution (e.g. GenSim, SimDigi, RECO/AOD, MiniAOD, NanoAOD). Vijay described work he and colleagues (inspired by a repository Ryan had built for a similar approach in Analysis Productions) had done on a `workgraph.cwl`, built from the WMAgent job package (`unpacker.py` and related sandbox/job-package artifacts), deliberately skipping the splitting step and treating the transformation system as a black box since they were told DiracX would handle it. Marco walked through an older proof-of-concept of his own, built bottom-up from a WMAgent Request Manager request document (which defines the full workflow: steps, parentage map, global tag, CMSSW version, ScramArch, primary dataset per step), the `splitting.json` document produced by request-manager splitting, and per-job `job.json`/tweak files, feeding a script that runs pset tweaking (via a script referred to as "EDMPsetThree" as heard) and `cmsRun` for each step, then a custom stage-out step. Marco argued for designing the single-job/per-step CWL definition bottom-up (starting from what a single job actually needs to execute: pset tweak, cmsRun, stage-out) rather than top-down from WMAgent's job-package/sandbox internals, and said the latter requires reproducing roughly 3,000 lines of WMAgent code that could be done in about 10. The two also briefly discussed what per-job splitting information is already known in general shape even without a finalized transformation system, both for Monte Carlo and for input-dataset (non-MC) workflows.

## Decisions / Conclusions

None reached in this meeting. Marco stated explicitly that the bottom-up vs top-down design choice "is not something you should decide" in this conversation and proposed discussing it further with Alan.

## Action Items

- [ ] Continue the bottom-up vs top-down CWL design discussion with Alan (a larger conversation flagged as needed) — Marco Mascheroni, Vijay Chakravarty (planned for 2pm the same day, per Vijay)

## Discussion

### Two dimensions of the workflow

Marco framed the general problem as splitting work along two dimensions: a "horizontal" dimension (for a single job, the sequence of steps it must run — e.g. pset tweak, then CMSSW run, repeated per step) and a "vertical" dimension (splitting the full dataset across many jobs, e.g. by file). He said the immediate goal under discussion was the horizontal dimension: defining, for a single job's input, all the steps that job must execute.

### Vijay's approach: workgraph.cwl from the WMAgent job package

Vijay explained that the team's approach (inspired by a repository Ryan built to try something similar in Analysis Productions) intentionally skips the splitting/transformation step, since they were told the transformation system would be handled by DiracX and could be treated as a black box. Their `workgraph.cwl` is built by taking the WMAgent job package/sandbox (including `unpacker.py`, which unpacks the job package) as input and feeding it into the graph. Vijay noted they have not seen the `splitting.json` document Marco referenced, and confirmed the team relies on the WMAgent job package specifically because, without running splitting themselves, they otherwise have no way to obtain per-job file lists.

### Marco's proof-of-concept: bottom-up from the Request Manager

Marco walked through an earlier proof-of-concept he had built, starting from a WMAgent Request Manager document rather than the job package. He noted the Request Manager request document already defines the full workflow description: multiple steps (e.g. GenSim, SimDigi, RECO, AOD, MiniAOD — a full step chain), a parentage map between steps, and per-step parameters (global tag, CMSSW version, ScramArch, primary dataset). He also pointed out that when the Request Manager runs splitting, it produces a `splitting.json` document, and that all the pset configurations are likewise available from the Request Manager.

From these Request Manager inputs, Marco's proof-of-concept produced, per job, a `job.json`/tweak file describing what to tweak in each step's pset. His worker-node script then, per step, loaded parameters from this file (`request.json`) and ran a pset-tweak step (via a script he referred to as "EDMPsetThree", provided by the core team member he referred to as "Shazad" — transcription uncertain), followed by `cmsRun`, repeating this for each step in the chain, and finished with a custom stage-out step he had written himself. He said the splitting logic used was the "bare WMAgent splitting," improved by Alan, since he found the request-based splitting had some issues ("mocking") he was not happy with.

Marco contrasted this with using the WMAgent job package as an input, which he said requires reproducing roughly 3,000 lines of code to do what could be done in about 10 lines starting from the Request Manager output directly. He said he is fine with Vijay's team not reusing any of his code, but argued for the same underlying approach: define, bottom-up, the sequence of pset-tweak/cmsRun/stage-out operations a single job needs, rather than starting from WMAgent's job-package structure and working down from it.

### Splitting and the transformation system

Vijay noted the team had deliberately not implemented splitting themselves partly because of significant uncertainty about what form the transformation and splitting steps will ultimately take, and because they were waiting on ADRs (architecture decision records).

Marco argued that even without a finalized transformation system, the general shape of what each job needs is already known:
- For Monte Carlo: the transformation system provides bookkeeping such as a Lumi-section range (since MC generates a fake dataset) — e.g. a job might be told to generate events for Lumi range 1000–3000.
- For input-dataset (non-MC) workflows: splitting (by file, event-aware, etc., as in CRAB) provides each job a list of files to analyze and a run/Lumi selection within those files, since files are organized by Run/Lumi.

On this basis, Marco concluded that the transformation system does not need to be finalized to define the per-job/per-step (horizontal) CWL logic, supporting his preference for a bottom-up approach.

## Open Questions

- What exact form the transformation system's output/transformation step will take (Marco noted it is likely not a "DiracX transformation" but was uncertain what it will be).
- Whether to proceed with a bottom-up (single-job step-chain first) or top-down (WMAgent job-package first) design for the CWL-based workflow — explicitly deferred to a further discussion involving Alan.
- How splitting/transformation will be finalized and integrated once ADRs are available.

## Related

[[CMS]] · [[WMAgent]] · [[WMCore]] · [[DIRACX]] · [[CRAB]] · [[Workload Management]] · [[Submission Infrastructure]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-08 11.11.54 Marco Mascheroni's Personal Meeting Room`)
