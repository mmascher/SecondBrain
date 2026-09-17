---
type: concept
---

# Workflow Management

## Overview

Workflow Management is the higher-level coordination of computational work: defining workflows, decomposing them into tasks and jobs, determining what work needs to be executed, and coordinating the progression of that work.

In the CMS computing model, the legacy workflow-management system is based on [[WMAgent]]/WMCore. CMS is transitioning this layer to a [[DIRACX]] (DiracX)-based system for the HL-LHC era, by interfacing its Transformation System with the HTCondor Access Points of the [[Submission Infrastructure]].

## CMS Context

The future DiracX-based system is intended to cover a broad range of CMS processing activities, including Tier-0 processing, data reconstruction, MC simulation, and distributed user analysis.

This transition does **not** imply replacing the underlying CMS batch workload-management and execution infrastructure. DiracX is being integrated with the existing [[Submission Infrastructure]], which remains responsible for acquiring resources and executing workloads through [[HTCondor]] and [[glideinWMS]].

## Relationship to Workload Management

Workflow Management and [[Workload Management]] operate at different architectural layers:

- **Workflow Management** determines and coordinates *what work needs to be done*.
- **Workload Management** provides the batch infrastructure through which that work is submitted, matched to resources, and executed.

In the planned CMS architecture:

```text
Workflow Management
    │
    │ workflows / tasks / jobs
    ▼
Workload Management
    │
    │ scheduling / resource acquisition / execution
    ▼
Compute resources
