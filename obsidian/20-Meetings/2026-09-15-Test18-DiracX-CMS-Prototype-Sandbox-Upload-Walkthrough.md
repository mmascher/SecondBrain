---
type: meeting
date: 2026-09-15
participants:
  - Marco Mascheroni
  - Camille Mauceri
topics:
  - Test18 DiracX/CMS Kubernetes prototype instance
  - Sandbox upload to S3 storage (Camille's implementation)
  - Kubernetes cluster access and operations (kubeconfig, pods, logs)
  - Helm chart values.yaml / developer mode (local code mount + pip install)
  - DIRAC client setup via CVMFS (LHCb area) and DIRACX_URL redirection
  - Job submission test on Test18
  - Secrets decryption procedure for Test18 certificates
  - Plan to prioritize ADRs over scale testing
---

# Test18 DiracX/CMS Prototype: Sandbox Upload Walkthrough

## Summary

Marco Mascheroni walked Camille Mauceri through the Test18 Kubernetes-based DiracX/CMS prototype instance, in preparation for testing Camille's implementation of sandbox upload to S3 storage — which she had already tested locally on "Pixie" without an authentication layer — against Test18, which sits behind authentication. Marco demonstrated how to point `kubectl`/the Kubernetes client at the Test18 cluster (a Kubernetes cluster hosted on CMS Web with a `diracx-cms` namespace), how to inspect pods and logs (the worker pod is where job submission actually happens), and how the Helm chart's `developer: true` setting lets a developer mount code from a git repository/branch into the pod and have it pip-installed (setting `PYTHONPATH` alone is not sufficient). He also showed the DIRAC client setup: sourcing the DIRAC/DiracX client from the LHCb CVMFS area and exporting `DIRACX_URL` to redirect it from LHCb's own (inaccessible) DiracX instance to CMS's Test18 instance, without needing a custom client branch. A live job submission was demonstrated (job/cluster ID 76); the job was picked up but remained in "waiting" status, which Marco attributed to updater code Francesco had worked on to set job status. The remainder of the session was spent trying (with partial success) to walk through decrypting the Test18 TLS/service certificates, which are stored encrypted in the Kubernetes cluster and require a documented decrypt-secret script and procedure shared by Valentin Kuznetsov; this did not fully succeed during the meeting (`diracx-cms not found` errors).

Marco characterized the current Test18 work as a prototype/learning exercise — useful for learning the system and surfacing bottlenecks/showstoppers — rather than the serious implementation, which he expects to follow once ADRs (Architecture Decision Records) are available. He said he does not plan to pursue scale testing yet, despite Valentin pushing for it, preferring to first demo progress next week and wait for the ADRs before doing "serious designing."

## Decisions / Conclusions

- Scale testing will not be pursued for now, even though Valentin Kuznetsov has been pushing for it; Marco wants to first demo progress next week and prioritize getting ADRs in place before doing serious design/implementation work.
- The current Test18 prototype work is being treated as a learning exercise (to learn the system and identify bottlenecks/showstoppers), not as throwaway-only — some of the code is expected to be reused once ADR-driven implementation begins.
- The DIRAC/DiracX client used for Test18 is the standard community client sourced from the LHCb CVMFS area, redirected to CMS's own instance via `DIRACX_URL`, rather than a CMS-specific fork/branch — Marco noted this is worth highlighting in his upcoming talk as an example of integrating with the community client rather than maintaining a separate branch.

## Action Items

- [ ] Camille Mauceri: work through setting up local access to Test18 (kubeconfig, values.yaml, and the Helm chart repo/`default.yaml`) and get her sandbox-upload-to-S3 implementation running against it.
- [ ] Camille Mauceri: send any questions/issues encountered to the WMS redesign investigation thread so Valentin Kuznetsov (or Marco, if Valentin doesn't respond the same day) can answer, visible to the whole team.
- [ ] Camille Mauceri: request access from Valentin Kuznetsov to the Test18 kubeconfig YAML (Marco could not confirm the source/permissions of the copy he has and will share his own copy in the meantime).

## Discussion

### Test18 environment and Kubernetes access
Test18 is a Kubernetes cluster hosted on CMS Web, with three physical worker nodes and a control plane managing pod scheduling (unrelated to HTCondor scheduling). The relevant application pods run in a `diracx-cms` namespace. To point the Kubernetes client at Test18, Marco exports a kubeconfig YAML file (`kubeconfig-test18.yaml`); `kubectl cluster-info` (via a `kx`-style alias in his bash RC) confirms which cluster is being targeted. Standard operations shown: `kubectl get pods`, `kubectl logs -f <pod>` (the "worker" pod runs the periodic tasks — Condor executor, monitor, etc. — that are defined in code, and is where job submission actually happens), and `kubectl exec` to get an interactive shell inside a pod (e.g. the MinIO pod), similar to SSHing in. Marco compared this to how a local Pixie/DIRAC instance under `dirac-ps` shows the same set of processes (scheduler + workers) but all running locally in one view, whereas on Kubernetes they run as separate, independently scalable pods (with built-in autoscaling based on load — Marco noted the design already accounts for this).

### Developer mode and images
Setting `developer: true` in the Helm chart's values file allows mounting code from a specified git repository/branch into the pod's filesystem; that code is then `pip install`-ed inside the pod (Marco noted that just setting `PYTHONPATH` was not sufficient — he had tried that). This lets a developer test a local branch without waiting for a full image rebuild. The base images used are DIRAC images to which Valentin Kuznetsov added CMS-specific layers providing HTCondor Python bindings.

### DIRAC client and DIRACX_URL
The DIRAC client Marco uses is sourced from the LHCb CVMFS area (not a CMS-specific build) and does not require the CA/certificate export step "as of recently." By default, `DIRACX_URL` (referred to in places as "Diraq URL") is either empty or points to LHCb's own DiracX instance, which CMS is not authorized to access; exporting `DIRACX_URL` to point at the CMS Test18 instance redirects the same, unmodified community client. Marco considered this an important point to make in his upcoming talk: CMS is integrating with the community DIRAC/DiracX client directly rather than maintaining a separate branch.

### Job submission test
Using the sourced client and exported `DIRACX_URL`, Marco submitted a test job (cluster/job ID 76 — transcription of the exact ID is uncertain). The job was picked up but stayed in "waiting" status; Marco attributed the status handling to updater code that Francesco had worked on. Getting Camille's sandbox-upload implementation working on Test18 was framed as the next step toward running something functionally meaningful (e.g., a Monte Carlo job, as Camille had already done on her local Pixie instance).

### Files/access needed to reproduce the setup
Marco identified three inputs Camille would need to install/run the Helm chart on Test18 herself:
1. The Test18 kubeconfig YAML — Marco was unsure where he originally obtained his copy; he agreed to share his file and have Camille separately request access from Valentin Kuznetsov so that future updates propagate to everyone. Camille reported already having a `kubeconfig-test18.yaml` from a previous submission attempt but could not access the link Marco sent live in the meeting (permissions issue).
2. The Helm chart `values.yaml` for Test18 — sourced from Valentin's messages/AFS area; Camille believed she might already have a copy and would check.
3. A `default.yaml` file (within Valentin's Helm chart repo's files directory) containing DIRAC/DiracX deployment configuration, including a value used by DiracX for deployment (details not fully explained) — access to this also needed to be confirmed/granted.

Camille was also pointed to Valentin's chart repository (to clone/fork for the latest version, including Marco's `developer: true` support).

### Secrets decryption procedure
Test18's certificates are stored encrypted in the Kubernetes cluster and must be downloaded and decoded via a documented procedure (referenced by Marco as coming from an architecture-style document/report Valentin had shared). Marco attempted to run a `decrypt-secret` script (requiring a namespace and a path to the encrypted secret file) live but repeatedly hit a `diracx-cms not found` error and did not resolve it by the end of the meeting; this remained a known gap ("this is the part I'm missing"). Marco separately acknowledged (agreeing with a point attributed to "Alan," not otherwise identified in this transcript) that the overall setup instructions are currently fragmented across chat threads, comments, and documents, and that a single consolidated procedure/reference is still needed.

## Open Questions

- Why does the `decrypt-secret` script fail with a `diracx-cms not found` error, and what is the correct invocation/path for decrypting the Test18 certificates? Unresolved at the end of the meeting.
- Why does a submitted job remain stuck in "waiting" status rather than progressing — is this fully explained by the updater-code status logic Francesco worked on, or is something else needed? Not resolved in this meeting.
- What exactly is the third required config value in `default.yaml` used for by DiracX during deployment? Marco was not certain of the full details.

## Related

[[DIRACX]] · [[DIRAC]] · [[Kubernetes]] · [[HTCondor]] · [[CMS]] · [[Submission Infrastructure]] · [[Workload Management]]

## Source

meeting_saved_closed_caption.txt (from `2026-09-15 17.47.29 Marco Mascheroni's Personal Meeting Room`)
