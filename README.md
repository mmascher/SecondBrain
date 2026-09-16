# SubmissionInfrastructureBrain

A personal knowledge base for the CMS Submission Infrastructure and Workload
Management ecosystem.

The project collects and organizes information from historical meetings,
technical documentation, presentations, proceedings, and source code into an
Obsidian knowledge base. The goal is to preserve both the information itself
and the context and reasoning behind it, and eventually make that knowledge
usable by coding and research agents.

## Goals

The knowledge base is intended to make it possible to:

- recover historical context from past discussions;
- understand how CMS Submission Infrastructure and Workload Management
  systems evolved;
- connect decisions and architectural discussions across meetings;
- preserve relationships between people, projects, systems, and concepts;
- combine meeting knowledge with documentation and implementation details;
- provide relevant context to coding and research agents without requiring
  the entire corpus to be loaded at once.

The emphasis is on **durable knowledge and provenance**, rather than simply
storing transcripts or generating summaries.

## Knowledge architecture

The Obsidian vault is organized into several layers:

```text
obsidian/
├── 00-Inbox/          Temporary landing area
├── 10-Projects/       Active projects and workstreams
├── 20-Meetings/       Meeting notes derived from transcripts
├── 30-Concepts/       Durable knowledge synthesized across sources
├── 40-References/     External documentation and reference material
├── 50-People/         Professional context about relevant people
├── 60-Presentations/  Presentation artifacts and source material
├── 70-Proceedings/    Papers and proceedings
├── 80-Code/           Local clones of source repositories
└── 90-Daily/          Scratch notes and temporary material
