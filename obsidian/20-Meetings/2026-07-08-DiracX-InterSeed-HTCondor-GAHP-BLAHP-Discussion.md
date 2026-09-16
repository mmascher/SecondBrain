---
type: meeting
date: 2026-07-08
participants:
  - Marco Mascheroni
  - Alexandre Boyer
  - Jaime Frey
  - Liz Sexton-Kennedy
topics:
  - DIRAC/DiracX transformation system and CMS collaboration
  - InterSeed computing-element interface project (DiracX)
  - HTCondor GAHP/BLAHP protocols
  - glideinWMS factory job submission model
  - SSH/Slurm submission via Condor Remote Cluster
  - HTCondor support for CWL
  - HEPCloud / glideinWMS overlap
---

# DiracX InterSeed and HTCondor GAHP/BLAHP Discussion

## Summary

Marco Mascheroni set the context: at a recent DIRAC/DiracX hackathon that CMS participated in, the DIRAC development team (working with LHCb) announced they are shifting their DiracX porting priority away from the workload management system (pilots/jobs/scheduling — an area CMS already covers with HTCondor and glideinWMS) and toward the transformation system (which handles linking payloads, merging, and constructing workflows), which CMS does need. At the hackathon, breakout groups discussed integration; one group (Alexandre Boyer, Vijay, and Alan on the DIRAC side) focused on computing-element (CE) interfacing, an area with strong overlap with HTCondor's factory/CE machinery. Marco invited Alexandre Boyer and HTCondor developer Jaime Frey to this meeting to explore that overlap directly.

Alexandre Boyer presented "InterSeed," a small proof-of-concept DIRAC project rewriting DIRAC's CE interface layer (which currently talks to ARC, HTCondor-CE, SSH/batch systems, and cloud providers via LibCloud) as small, typed Python protocols (one per operation, e.g. submit, monitor) instead of a single large untyped base class, along with a Docker-based integration-test proof of concept (spinning up HTCondor, ARC, and Slurm containers) to catch breakage before reaching production. He asked whether InterSeed could reuse HTCondor's own CE-interfacing components instead of duplicating effort. Jaime Frey explained HTCondor's GAHP (heard/rendered as "gap" in the transcript) and BLAHP (rendered as "blap") — GAHP is a general framework/protocol HTCondor uses to isolate its single-threaded C++ codebase from external client libraries (originally for Globus GRAM, later extended to HTCondor-CE, ARC CE, and others); BLAHP is a more specific kind of GAHP for talking to local batch systems, including over SSH. Jaime clarified these are treated as fairly internal to Condor, not designed or well-supported for standalone external use, and suggested InterSeed might get more value from writing its own thin wrapper around underlying client tools/libraries than from building directly on GAHP/BLAHP.

Marco described how glideinWMS's factory avoids this problem: the factory doesn't talk to CE protocols directly — it does a plain `condor_submit` (or uses the Python bindings) to a local HTCondor schedd running on the factory, specifying the CE hostname and type (ARC, HTCondor-CE, etc.) in the job description; Condor's own schedd then handles all CE-protocol-specific details internally via GAHP/BLAHP. Marco suggested this — DIRAC/DiracX submitting through a local Condor schedd rather than talking to GAHP/BLAHP directly — might be a more viable path than building on GAHP/BLAHP as a library. Alexandre agreed it was worth investigating.

The group also discussed SSH-based submission to Slurm-based HPC clusters, which Condor already supports: BLAHP and a parallel file-transfer daemon are installed (no root required) on the HPC login node under the submitting user's account, with passwordless SSH keys set up; HTCondor ships a helper tool called "Condor Remote Cluster" (documented in the Condor manual) that automates this setup. CMS itself doesn't use this directly — Fermilab's HEPCloud team handles that, and it also underlies OSG's "OS pool." Cloud submission (EC2 mainly, with limited/likely unused support for Azure and Google Cloud) was also discussed; Marco and Jaime were both uncertain about current real-world usage, including whether glideinWMS's reported Google Cloud usage is still active.

Alexandre asked about the HTCondor team's process for accepting external contributions (e.g., adding SSH+Slurm support) and about integration testing to prevent regressions. Jaime said HTCondor accepts external contributions on a case-by-case basis via code review, depending on how much a contribution affects their own usage; contributions that fit BLAHP's existing modular plugin design (e.g., a recent contribution adding support for NERSC's Superfacility API for the Perlmutter HPC system, which added only new support scripts without touching BLAHP's central code) are easy to accept, while an entirely new scheduler type requiring new core C++/GAHP code would be much harder. HTCondor's own testing includes manual code review plus existing test suites for BLAHP and HTCondor-CE as part of the release process; Jaime noted ARC testing is comparatively weak, though a standalone ARC CE test mode exists.

Marco asked what level of support CMS/DIRAC could expect if something broke after adopting Condor as a dependency. Jaime distinguished two cases: usage where DIRAC submits through Condor's own machinery (e.g. `condor_submit`, using GAHP/BLAHP internally) is a use case HTCondor is prepared to support; direct external use of GAHP/BLAHP as a standalone building block is not a use case they've designed for or are well-prepared to support.

Partway through, Liz Sexton-Kennedy joined and noted she now works in the Fermilab group supporting HEPCloud, and that Fermilab is looking to retire tools that are covered by other, more community-supported projects. She recalled Marco previously telling her that the only remaining functional difference between glideinWMS and HEPCloud is HEPCloud's decision engine (originally built for cloud cost control, now not doing much), and suggested that HTCondor's growing Slurm/HPC support could be a path to reducing that support burden by consolidating on glideinWMS — offered as her own observation, not a decision made in this meeting.

Liz also raised a separate topic: at a prior cross-experiment/cross-project new-WMS meeting, there was discussion of HTCondor supporting CWL (Common Workflow Language), which she said Brian had spoken positively about, noting other OSG clients were also requesting it. She asked Jaime whether he agreed and whether there was a schedule or plan. Jaime said he is not the main person involved but would loop in the person who is and follow up by email, possibly via a separate meeting. Liz and Marco noted an underlying open question relevant to CMS's own WMS planning: once a CWL description of a workflow exists, should Condor do most of the work of executing it, or does DIRAC/CMS need to write its own execution logic? This was explicitly flagged as not answerable in the time remaining and deferred to a future meeting.

Jaime had to leave early for another meeting. After he left, Alexandre reiterated that InterSeed is currently low priority for the DIRAC side, since the priority is the transformation-system integration with CMS; he will investigate feasibility of using GAHP/BLAHP (or Condor's own submission machinery) with DiracX, and check with DIRAC line management on what's feasible.

## Decisions / Conclusions

- HTCondor's GAHP ("gap") and BLAHP ("blap") protocols are considered internal to Condor by the HTCondor team; they are not designed or well-supported for use as standalone building blocks by external software such as DiracX/InterSeed.
- SSH-based submission to Slurm HPC clusters is already supported in HTCondor: BLAHP plus a file-transfer daemon are installed under the submitting user's own account on the cluster's login node (no root access needed), using passwordless SSH keys; the "Condor Remote Cluster" tool (documented in the Condor manual) automates this setup.
- The HTCondor team would support DIRAC/DiracX usage where CE submission goes through Condor's own machinery (e.g. `condor_submit` to a local schedd, which uses GAHP/BLAHP internally) but would not be well-positioned to support direct external use of GAHP/BLAHP as a standalone library.
- Contributions to BLAHP are easiest to accept when they fit its existing modular plugin design (example given: a recent contribution adding NERSC Superfacility API / Perlmutter support, which added only new support scripts without touching BLAHP's central code); contributions requiring new core C++/GAHP code would be much harder to accept.
- HTCondor's release-process testing includes manual code review and existing test suites for BLAHP and HTCondor-CE submission; ARC testing is comparatively weaker and the team acknowledged it needs improvement, though a standalone ARC CE test mode exists.
- The key open question of whether Condor should handle CWL workflow execution directly, or whether DIRAC/CMS needs custom execution logic, was explicitly identified as unresolved and deferred to a follow-up meeting.
- Alexandre Boyer confirmed the DIRAC-side priority remains the transformation-system integration with CMS; the InterSeed / GAHP-BLAHP investigation is lower priority for now.

## Action Items

- [ ] Investigate the feasibility of using HTCondor's GAHP/BLAHP (or submitting via Condor's own machinery, e.g. a local schedd) for DiracX's CE interfacing, and check with DIRAC line management on what is feasible — Alexandre Boyer
- [ ] Email Jaime Frey, Liz Sexton-Kennedy, and Alexandre Boyer to schedule a follow-up meeting about HTCondor CWL support — Marco Mascheroni
- [ ] Loop in the HTCondor team member working on CWL support and follow up by email — Jaime Frey
- [ ] Include Alexandre Boyer in the next (biweekly) Condor/Submission Infrastructure team meeting — Marco Mascheroni

## Discussion

See Summary above for full discussion detail, including:
- Background on the DIRAC/DiracX hackathon and the split of DIRAC's DiracX porting priorities (workload management vs. transformation system).
- Alexandre Boyer's description of InterSeed's motivation: DIRAC's current CE interface layer conflates lifecycle logic with cross-cutting policy (slot accounting, proxy renewal configuration), lacks abstraction (interfaces have drifted over time), was built mainly for the pool/pilot model but now also needs to support direct job pushes, and is untyped/undiscoverable. InterSeed's proposed fix is small typed Python protocols per operation, plus Docker-based integration tests (HTCondor, ARC, Slurm containers) run before changes reach production.
- Whether Vijay might assist Alexandre on InterSeed was raised by Marco as a suggestion, tied to Vijay's reported focus (per Stefan) on glideinWMS integration; this was not settled — Alexandre indicated it depends on the DIRAC team's current bandwidth relative to the transformation-system priority.
- Marco's interest, expressed as a personal aspiration rather than a decision, in eventually harmonizing CE/submission approaches across experiments (mentioning ATLAS and ALICE), with the caveat "let's not dream."

## Open Questions

- Whether InterSeed should build on HTCondor's GAHP/BLAHP directly, submit via Condor's own machinery (e.g. a local schedd, as glideinWMS's factory does), or continue with its own thin wrappers — not resolved; Alexandre Boyer will investigate.
- Whether Vijay will be assigned to help Alexandre Boyer on the InterSeed/GAHP-BLAHP investigation — raised as a suggestion, not decided.
- Current real-world usage of HTCondor's cloud-provider support (EC2, Azure, Google Cloud) by CMS or glideinWMS — both Marco Mascheroni and Jaime Frey were uncertain, including whether glideinWMS's reported past Google Cloud usage is still active.
- Whether and on what schedule HTCondor will support CWL — Jaime Frey to follow up after looping in the relevant team member.
- Once a CWL workflow description exists, whether Condor should handle most of its execution or whether DIRAC/CMS needs to write custom execution logic — explicitly flagged as unresolved, deferred to a future meeting.

## Related

[[CMS]] · [[DIRAC]] · [[DIRACX]] · [[HTCondor]] · [[glideinWMS]] · [[Factory]] · [[Factory Operations]] · [[Pilot Jobs]] · [[Workload Management]] · [[OSG]] · [[HPC]]

## Source

meeting_saved_closed_caption.txt (from `2026-07-08 18.03.21 CMS Submission Infrastructure meeting`)
