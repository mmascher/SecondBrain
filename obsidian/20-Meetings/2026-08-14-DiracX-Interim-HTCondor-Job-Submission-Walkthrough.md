---
type: meeting
date: 2026-08-14
participants:
  - Marco Mascheroni
  - Camille Mauceri
  - Andrea Piccinelli
  - Alan Malta Rodrigues
topics:
  - DiracX architecture walkthrough (FastAPI router, scheduler, workers, Redis, Seaweed, Uvicorn)
  - Marco's throwaway DiracX-to-HTCondor job submission prototype
  - Comparison with the hackathon "dummy job submission" prototype (Camille/Andrea)
  - Dirac JDL vs. Condor JDL and JDL conversion
  - HTCondor ID token / global pool key requirements for submission
  - Deployment to test18 (Valentin Kuznetsov's DiracX instance) and Kubernetes
  - Missing pieces: transformation system, site selection, status monitoring, sandbox/file staging
  - CWL work (Camille) and its relationship to the transformation system
---

# DiracX Interim HTCondor Job Submission Prototype Walkthrough

## Summary

Camille Mauceri asked Marco Mascheroni to walk through the "dummy job submission to Condor" prototype he has been working on, and whether there was anything she could help with. Marco first compared his approach with what Camille and Andrea Piccinelli had built during an earlier hackathon: their prototype registered a task in the DiracX database that only changed a job's status (e.g., waiting, received) without actually executing anything, using a DiracX "job executor" class picked up by a periodic monitoring task. Marco then shared his screen and walked through his own prototype (explicitly described as a throwaway implementation pending the DIRAC Architecture Decision Record, or ADR), which follows the same monitor-task/executor-task pattern but, instead of just changing status, submits the job to an HTCondor scheduler (collector "1400", scheduler "059", described as a CRAB test scheduler) and then updates the job status with the result. He demonstrated DiracX's local deployment (`pixi run local start`), the DiracX CLI (`dirac submit job`, `dirac task run`, `dirac jobs submit`), a Dirac-JDL-to-Condor-JDL conversion function he wrote (AI-assisted, not yet verified), and a `debugpy`-based debugging setup he added locally. He also explained DiracX's internal components (FastAPI REST router, scheduler, small/medium/large workers, Redis, Seaweed, Uvicorn). The group discussed several open pieces still missing from the prototype (transformation system, site list, status polling, file/script staging) and how this work might eventually be integrated with the DiracX instance deployed at test18. Camille reported she had independently already replicated a similar Hello World submission against test18. No firm decisions were reached on the final architecture; several points were explicitly deferred pending the ADR and a discussion between Marco and Valentin Kuznetsov.

## Decisions / Conclusions

- Marco's current implementation is explicitly a "throwaway"/prototype, done ahead of the ADR that will define the transformation system; it is not intended as a final implementation, and the job database it currently uses may not be the one the future transformation system pulls jobs from.
- DiracX exposes two distinct ways to trigger work: `dirac jobs submit` goes through the FastAPI REST router (`routers/jobs`) and is the normal job-submission path, while `dirac task run` directly triggers a registered task on the server (used here for testing/debugging), bypassing the REST interface.
- Dirac JDL and Condor JDL are both key-value formats, but use different keys and are interpreted differently by their respective servers; conversion between them is required. Marco wrote a conversion function for this (JDL string → key-value pairs → Condor submit description), noting it was AI-assisted and not yet fully verified.
- Submitting to the HTCondor scheduler requires a Condor ID token generated from the global pool key, and the submitting user must be separately authorized on the scheduler; submitting to scheduler "059" additionally requires being on the CERN VPN/network.
- Camille confirmed the earlier virtual machine that Valentin Kuznetsov had set up was for legacy DIRAC, not DiracX, and is no longer relevant for this work; Alan Malta Rodrigues confirmed DiracX at test18 is deployed via Kubernetes (also effectively running on a VM, but through the Kubernetes setup).
- The transformation system does not yet exist; it is expected to take a workflow description and generate jobs. There is currently no clear advantage to routing through Dirac before Condor when this piece is missing — one could submit to Condor directly — so the current demonstration is explicitly framed as a toy/learning example.
- Camille had already independently submitted a similar Hello World job to test18 before this meeting, using a setup similar to Marco's, and confirmed she could see the job in the DiracX dashboard with its status updated (e.g., to "waiting") after logging in via the browser.

## Action Items

- [ ] Clean up and commit the current DiracX→HTCondor prototype branch, and share the branch and a Condor ID token with Camille — Marco Mascheroni
- [ ] Replicate Marco's DiracX-to-HTCondor submission setup (pixi local shell, install dependencies, submit) once the branch is shared — Camille Mauceri

## Discussion

### Comparison with the hackathon prototype
Camille and Andrea recalled that their hackathon prototype registered a task/class into the DiracX database; it changed a job's status (e.g., waiting, received) but did not actually execute anything anywhere. Marco confirmed this matches the "job executor" pattern: a periodic monitoring task picks up jobs in a given state and calls an executor task (passed a single job ID) that updates the job's status. Marco's prototype follows the same monitor/executor pattern, but the executor actually submits to HTCondor rather than only changing status.

### DiracX architecture walkthrough
Marco walked through the components started by `pixi run local start`: a FastAPI web application (Uvicorn) exposing REST routers, including a `jobs` router; a scheduler and three workers (small, medium, large) that pick up and run registered tasks, including periodic tasks such as the job-monitoring task; Redis, which the scheduler uses to distribute tasks to workers; and Seaweed, an S3-like storage service which Marco believes is used to store input sandboxes. A local SQLite database is recreated each time the local instance is restarted. Marco also noted that `dirac task run` (used for testing) is a different path from `dirac jobs submit` (the REST interface used for normal submissions).

### Job submission and JDL conversion
Marco demonstrated submitting a "Hello World" job using a Dirac JDL file (distinct from Condor JDL) via `dirac submit job`, first against his local instance and then, via a gist, against Valentin's test18 instance. His prototype converts the Dirac JDL into a Condor submit description using a conversion function he wrote (AI-assisted, unverified) before submitting to the HTCondor scheduler with the Python `htcondor` bindings. He added the `htcondor` Python bindings as a `pixi.toml` dependency for this to work. The current test JDL does not specify a site list, so the resulting Condor job would not actually be scheduled to run anywhere; adding a site list is still needed.

### Debugging setup
Marco added `debugpy` support locally (starting the server/worker with a debug flag) to allow attaching a debugger and stepping through the code (e.g., through the JDL-parsing and submission functions) using VS Code's debugger. He noted this is not an official/supported feature and that he intends to open a ticket about it.

### Credentials and network requirements
Submitting to the HTCondor scheduler requires an HTCondor ID token generated using the global pool key; users must also be individually authorized on the scheduler. Submitting to scheduler "059" specifically requires being on the CERN network/VPN.

### Deployment and integration with test18
Andrea asked whether using this from the "Mars" repository / from a VM would require installing DiracX from a specific repository, and how the DiracX service would need to be restarted to pick up code changes; Marco said checking out his branch and running `pixi install` would be enough locally. Andrea was unsure whether the test18 instance was a Kubernetes pod or a plain pixi-based install; Alan clarified test18's DiracX runs in Kubernetes. Camille clarified that the separate VM previously set up by Valentin was for legacy DIRAC, not DiracX, and is not relevant here.

Alan raised what he considered the larger question: once Marco's prototype is ready, how should this task-execution logic be integrated with the DiracX instance deployed at test18. This includes bringing over the Condor credential/ID token mechanism, which Andrea noted is currently hardcoded (e.g., the scheduler name) in the job executor and would likely need to change for the Kubernetes-deployed instance; it was unclear whether a different/specific token would be needed there. Alan's view (offered as an opinion, not a decision) was that Marco and Valentin should discuss this directly, and that this is not currently blocking Camille's work. Andrea separately suggested that once Marco is back (Marco is away the following week), Marco and Valentin should talk about replicating this at test18.

### Transformation system, CWL, and next steps for Camille
Alan asked whether Camille's CWL work would need a second translation step in addition to the Dirac-JDL-to-Condor-JDL conversion. Marco clarified that the transformation system — not yet built — is the piece that will take a CWL workflow description and split it into jobs; this is separate from the submission demo shown in the meeting. He noted legacy DIRAC's own transformation system could potentially be reused and connected to DiracX (a direction he said Valentin may be advocating for, not decided), or the group could wait for the ADR before designing a new one. He also noted that DiracX itself does not use CWL; only legacy DIRAC has historically not used it either — CWL support would be new work regardless.

Camille said she sees her CWL work and this DiracX/Condor submission prototype as separate, parallel activities: she will continue CWL work aimed at being ready once DiracX has a transformation system that can accept CWL, while independently wanting to replicate Marco's current Dirac-to-Condor submission setup for learning/practice purposes, regardless of how much the transformation system later changes the back end. Marco agreed to clean up and commit his branch and share it, along with a Condor token, so Camille can reproduce the local-shell submission steps.

### Remaining missing pieces
Marco identified several things not yet implemented in his prototype:
- **Status monitoring**: currently only submission is implemented; a periodic task still needs to check Condor job status (e.g., via a Condor queue query) and update the DiracX job status accordingly.
- **File/script staging**: the current test only runs an inline `echo` command; there is no mechanism yet for a user to upload their own script to DiracX and have it passed to Condor at submission time. Marco noted a `dirac task run` listing shows an existing "clean sandbox" task, suggesting DiracX may already have some sandbox-management functionality (via Seaweed) that could be leveraged for this.

### Camille's independent test18 submission
Camille reported that, prior to seeing Marco's gist, she had already submitted a similar Hello World job against test18 using a comparable setup, and saw her job appear on the DiracX dashboard with its status updated (e.g., to "waiting") after logging in through the browser. Both Camille and Marco noted needing to obtain a CA certificate from Kubernetes when submitting from a personal laptop rather than a shared machine.

## Open Questions

- Will the job database used by this prototype remain the one the future transformation system pulls jobs from, or will it need to be bypassed once the transformation system exists? Left pending the ADR.
- Should the transformation system reuse legacy DIRAC's existing transformation system connected to DiracX, or should a new one be designed after the ADR? Not decided; Marco suggested Valentin may favor reuse.
- Will CWL require an additional translation step beyond the Dirac-JDL-to-Condor-JDL conversion already needed? Raised by Alan, not resolved.
- How exactly should this Condor-submission task execution be integrated with the DiracX deployment at test18, including how the Condor credential/ID token (currently hardcoded to Marco's local setup) should be managed there? Left for Marco and Valentin to discuss directly.
- How should user-supplied script/executable files be uploaded to DiracX and made available to Condor at submission time (sandbox/file staging)? Not yet implemented.

## Related

[[DIRAC]] · [[DIRACX]] · [[HTCondor]] · [[Kubernetes]] · [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-08-14 10.03.49 DiracX interim job submission chat`)
