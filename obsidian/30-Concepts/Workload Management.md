### `Workload Management.md`

```markdown
---
type: concept
---

# Workload Management

## Overview

Workload Management is the batch execution and resource-management layer responsible for getting computational work onto available computing resources. It includes submission, matchmaking, resource acquisition, and execution of workloads.

In the CMS architecture, this layer is provided by the [[Submission Infrastructure]], based on [[HTCondor]] and [[glideinWMS]].

## CMS Context

CMS uses a global HTCondor pool and a pilot-based resource-acquisition model implemented by glideinWMS.

User and production jobs are submitted to HTCondor [[Access Points]]. HTCondor performs matchmaking against available resources, while glideinWMS acquires those resources by submitting generic [[Pilot Jobs]] to Compute Elements. Once a pilot is running and joins the HTCondor pool, actual workloads can be matched to it.

This provides CMS with a pull-based, late-binding model in which the workload is matched to resources after the resources have been acquired.

## Relationship to Workflow Management

Workload Management is distinct from [[Workflow Management]]:

- **Workflow Management** determines and coordinates *what work needs to be done*.
- **Workload Management** provides the batch infrastructure through which that work is submitted, matched to resources, and executed.

The planned CMS architecture retains this workload-management layer while introducing DiracX as the future workflow-management system:

```text
Workflow Management
        │
        ▼
CMS Submission Infrastructure
        │
   ┌────┴────┐
   │         │
HTCondor  glideinWMS
   │         │
   │     Pilot submission
   │         │
   └────┬────┘
        ▼
   Compute Elements
