---
type: meeting
date: 2026-07-08
participants:
  - Marco Mascheroni
  - Andrea Piccinelli
topics:
  - Data-aware matchmaking proposal (Rucio distance-based HTCondor matching)
  - HTCondor/glideinWMS matchmaking mechanics walkthrough
  - DIRAC/glideinWMS integration timeline and budget review
---

# Data-Aware Matchmaking Design Discussion

## Summary

Note on source quality: this transcript is an auto-generated closed-caption file that mixes Italian and English very inconsistently, with many words badly mistranscribed. The note below reflects a best-effort reconstruction of the discussion; several specific terms remain uncertain and are flagged as such.

Marco Mascheroni and Andrea Piccinelli held a working session, mostly in Italian, to sketch out an early design for adding data-awareness (via [[Rucio]] "distance" information) to HTCondor/[[glideinWMS]] matchmaking. Marco first gave a brief update on the [[DIRAC]]/glideinWMS integration timeline (tied to a budget-review request from a colleague referred to as Lisa), then walked Andrea through how HTCondor negotiator matchmaking currently works (Start/Requirements expressions, partitionable slots, `Desired_Sites`), and proposed a first design for letting jobs fall back to running at a "reasonably close" (rather than only fully local) site after waiting a period of time. Several implementation details were explicitly left undecided.

## Decisions / Conclusions

- The group agreed on a general direction for a first data-aware matchmaking proposal: extend the existing job/site matching logic (which currently requires the pilot's site to be in the job's `Desired_Sites` list) so that, after the job has waited in the queue for a period of time (discussed as roughly 8 hours), it can also match to a site that is not in `Desired_Sites` but is within an acceptable data "distance" — rather than immediately allowing remote-data execution as soon as a free slot appears.
- Rucio has an existing per-RSE "distance" concept (an admin-configured metric based on endpoints) that could be reused as the basis for this design. Marco noted that [[Pelican]], by contrast, does not have an equivalent distance concept.
- This was treated as a first-pass idea to write up and discuss further, not a finalized design — Marco explicitly said several parts "can't all be decided now" and that this was the first of possibly several proposals to sketch out before picking one to develop further with the team.

## Action Items

- [ ] Share the data-aware matchmaking design document at an upcoming meeting and discuss it with a colleague (name unclear in transcript, transcribed as "Jamie"/"Congemi") — Marco Mascheroni

## Discussion

### DIRAC/glideinWMS integration timeline and budget review

Marco relayed that, based on a Friday conversation with colleagues referred to as Lisa and Daniele, and separate discussions with Federico Stagni and a DIRAC developer referred to as "Chris," DIRAC-side work ("staging," per the transcript) is expected to start within a few weeks, with feedback and further work continuing through the end of summer (around late September), followed by a DIRAC workshop. Marco's assessment was that no concrete, detailed technical implementation plan (in his words, a "technical plan with tables of components and their interactions," clarifying deliverables and who works on what) — for glideinWMS or other components — would exist before roughly the end of October. He noted that Lisa had said this planning needs to be done for a budget review, but maintained that his own estimate (no concrete plan before end of October) was already written into a document he had prepared, rather than guessed.

### HTCondor/glideinWMS matchmaking mechanics (walkthrough for Andrea)

Marco used a live `condor_status`/`condor_q`-style view to explain HTCondor matchmaking to Andrea: pilots connect to the pool's central manager, claim a partitionable slot sized according to the resources configured for that pilot (e.g., a fixed core/whole-node allocation), and as individual jobs start, sub-slots are carved out of the parent slot consuming CPU/RAM. He illustrated glideinWMS's slot "overloading" (allocating somewhat more cores than are physically present, plus a core dedicated to an I/O slot) using a live example, and showed example running slots (a GPU job with a memory requirement, and single-core production/analysis jobs).

He explained that both the machine (slot) and the job publish ClassAd-based boolean expressions — the machine's `Start`/requirements expression (checking things like whether the machine is draining, requested CPU/GPU/memory versus what the pilot offers, and remaining wall time) and an equivalent expression on the job side — and that the HTCondor negotiator matches a job to a slot when both expressions evaluate true.

### Existing `Desired_Sites` mechanism

Marco described the existing mechanism: a job defines its desired input data via LFNs; something (referred to ambiguously in the transcript, possibly "WMAgent," transcription uncertain) resolves this to a `Desired_Sites` ClassAd — the list of sites where that data is available. Currently, the job's `Requirements` expression checks whether the pilot's site is a member of this `Desired_Sites` list (a `StringListMember`-type check) as a precondition for matching. Whether `Desired_Sites` should remain static or become dynamic, and which component is responsible for setting it, was noted by Marco as still undecided ("to be decided").

### Proposed data-aware matchmaking extension

Marco proposed extending this mechanism using Rucio's existing per-RSE "distance" concept:

- When a pilot starts at a site, it would (in this proposal) look up and publish a set of distance values — one per Rucio Storage Element (RSE), illustrated with an example of around 50 RSEs — as ClassAds on its slot (e.g., illustrative values like "CERN tape: distance 10," "CERN disk: distance 20," "BNL disk: distance 30").
- A new job-level ClassAd would express a required maximum ("minimum acceptable") data distance for the job; no final name was settled on during the meeting (candidates discussed informally, e.g. involving "required"/"minimum data distance," with the exact wording left open, half-jokingly suggesting asking an LLM for naming help).
- Proposed logic: for roughly the first 8 hours a job is queued, only match it to sites in its `Desired_Sites` list (i.e., true data locality). After that waiting period, relax the requirement so the job can also match a site whose published distance to the job's data is within the job's required threshold, even if that site is not in `Desired_Sites`. Marco's reasoning was to avoid jobs immediately preferring to run remotely from their data as soon as any free slot appears, while still avoiding indefinite starvation if no local site is free.
- Marco noted the current glideinWMS matching expression for this is static ("doesn't change"); implementing this proposal would make part of the expression depend on elapsed queue time and on distance values published by the pilot at start time.

Several implementation questions were raised but explicitly left open (see below), including how to query/cache distance data and how to handle a single file replicated at more than one RSE.

## Open Questions

- How to determine a single applicable data distance for a job when its input data (an LFN) exists at more than one RSE (e.g., both BNL and FNAL) — Marco called this "the difficult part" and said it needed more thought; not resolved in the meeting.
- Whether pilots would query Rucio directly at startup to obtain distance values, or whether this should go through a caching/service layer (e.g., something distributed via [[CVMFS]]) — Marco said he would not want every pilot to query Rucio directly, but did not decide on an alternative during the meeting.
- Which component sets the job's `Desired_Sites` ClassAd today, and whether it should remain static or become dynamic — left as "to be decided."
- What the new job-level distance-requirement ClassAd should be named — not settled.
- How to choose among multiple sites when more than one satisfies the (relaxed) distance requirement simultaneously — raised by Andrea; not answered in the meeting.
- The exact wait-time threshold (discussed illustratively as 8 hours) and distance-limit values were used only as examples, not finalized figures.

## Related

[[glideinWMS]] · [[HTCondor]] · [[Rucio]] · [[DIRAC]] · [[CMS]] · [[Pelican]] · [[Workload Management]] · [[Pilot Jobs]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-08 14.03.25 Chat about data-aware`)
