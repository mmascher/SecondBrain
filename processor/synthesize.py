#!/usr/bin/env python3

"""
Synthesize durable knowledge from the accumulated SecondBrain corpus.

The synthesis workflow is deliberately separate from transcript processing.

Modes:
  discover    Inspect the accumulated corpus and propose durable concept
              candidates. This mode must not create/update concept notes.
  synthesize  Synthesize approved candidates into durable concept notes.
  update      Revisit existing concept notes using newly available sources.

Python is responsible for:
  - selecting the synthesis mode
  - invoking the selected agent
  - protecting existing concept notes
  - verifying agent output
  - installing validated outputs

The agent is responsible for:
  - inspecting the relevant corpus
  - following processor/SYNTHESIS.md
  - performing the actual knowledge synthesis
"""

from pathlib import Path
import argparse
import subprocess
import sys
import tempfile
import yaml


ROOT = Path(__file__).resolve().parent.parent
MEETINGS = ROOT / "obsidian" / "20-Meetings"
CONCEPTS = ROOT / "obsidian" / "30-Concepts"
REFERENCES = ROOT / "obsidian" / "40-References"
PRESENTATIONS = ROOT / "obsidian" / "60-Presentations"
PROCEEDINGS = ROOT / "obsidian" / "70-Proceedings"
CODE_INDEX = ROOT / "obsidian" / "80-Code-Index.md"
SYNTHESIS_RULES = ROOT / "processor" / "SYNTHESIS.md"
DISCOVERY_DIR = CONCEPTS / "_synthesis"
CANDIDATES = DISCOVERY_DIR / "concept-candidates.md"


def run_agent(prompt, output_dir, agent):
    """Run exactly one bounded synthesis operation."""
    if agent == "codex":
        command = [
            "codex",
            "exec",
            "--full-auto",
            "-C",
            str(ROOT),
            prompt,
        ]
    elif agent == "claude":
        command = [
            "claude",
            "-p",
            prompt,
            "--dangerously-skip-permissions",
        ]
    else:
        raise ValueError(f"Unknown agent: {agent}")

    print()
    print(f"Running agent: {agent}")
    print()

    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{agent} exited with status {result.returncode}"
        )


def validate_discovery(output_dir):
    """Validate the discovery artifact."""
    result_file = output_dir / "result.yaml"
    candidate_file = output_dir / "concept-candidates.md"

    if not result_file.exists():
        raise RuntimeError("Agent completed without producing result.yaml.")

    try:
        result = yaml.safe_load(result_file.read_text()) or {}
    except yaml.YAMLError as exc:
        raise RuntimeError(f"Invalid result.yaml: {exc}") from exc

    if result.get("status") != "discovered":
        raise RuntimeError(
            f"Invalid discovery status: {result.get('status')!r}"
        )

    if not candidate_file.exists() or candidate_file.stat().st_size == 0:
        raise RuntimeError(
            "Agent reported discovery but did not produce "
            "concept-candidates.md."
        )

    return candidate_file


def validate_synthesis(output_dir, mode):
    """Validate synthesized concept notes before installation."""
    result_file = output_dir / "result.yaml"

    if not result_file.exists():
        raise RuntimeError("Agent completed without producing result.yaml.")

    try:
        result = yaml.safe_load(result_file.read_text()) or {}
    except yaml.YAMLError as exc:
        raise RuntimeError(f"Invalid result.yaml: {exc}") from exc

    expected = "synthesized" if mode == "synthesize" else "updated"
    if result.get("status") != expected:
        raise RuntimeError(
            f"Invalid synthesis status: {result.get('status')!r}"
        )

    notes = sorted(output_dir.glob("*.md"))
    notes = [p for p in notes if p.name != "concept-candidates.md"]

    if not notes:
        raise RuntimeError(
            f"Agent reported status={expected} but produced no Markdown notes."
        )

    for note in notes:
        if note.stat().st_size == 0:
            raise RuntimeError(f"Generated concept note is empty: {note.name}")

        text = note.read_text(errors="replace")
        if not text.lstrip().startswith("---"):
            raise RuntimeError(
                f"Concept note lacks YAML frontmatter: {note.name}"
            )

        if "## Sources" not in text:
            raise RuntimeError(
                f"Concept note lacks required ## Sources section: {note.name}"
            )

    return notes


def install_notes(notes, allow_existing=False):
    """Install validated notes without accidental overwrites."""
    CONCEPTS.mkdir(parents=True, exist_ok=True)

    installed = []
    for note in notes:
        destination = CONCEPTS / note.name

        if destination.exists() and not allow_existing:
            raise RuntimeError(
                f"Refusing to overwrite existing concept note: {destination}"
            )

        if destination.exists():
            # update mode is deliberately explicit
            note.replace(destination)
        else:
            note.rename(destination)

        installed.append(destination)

    return installed


def discovery_prompt(output_dir):
    return f"""
You are performing KNOWLEDGE SYNTHESIS DISCOVERY for the SecondBrain project.

This is a DISCOVERY-ONLY operation.

Repository:
{ROOT}

Your synthesis rules are:
{SYNTHESIS_RULES}

Your task is to inspect the accumulated knowledge corpus and identify
candidate durable concepts that deserve synthesis into
{CONCEPTS}.

Start with the existing Markdown meeting notes under:
{MEETINGS}

Use other source material when it is clearly relevant:
{REFERENCES}
{PRESENTATIONS}
{PROCEEDINGS}
{CODE_INDEX}

Do NOT read the entire repository indiscriminately. Start from the meeting
notes, identify recurring themes and relationships, and inspect deeper
sources only where they materially help establish a candidate.

IMPORTANT:
- Do not create or modify anything under {CONCEPTS}, except the temporary
  output directory described below.
- Do not create actual concept notes.
- Do not modify meeting notes or source material.
- Do not treat the seed vocabulary in AGENTS.md as a list of concepts that
  must all become notes.
- A candidate should represent durable knowledge, not merely a frequently
  mentioned noun.
- Prefer concepts supported by multiple independent meetings and/or other
  substantial sources.
- Preserve disagreements and historical evolution.
- Distinguish established understanding from proposals and open questions.
- Avoid creating candidates that merely duplicate another candidate.
- Be conservative: a smaller set of strong candidates is preferable to a
  large taxonomy.

For each candidate, capture:
- proposed title
- why it is durable
- the sources that support it
- important relationships to other candidates
- unresolved disagreements or uncertainty
- whether the candidate appears ready for synthesis or needs more source
  material

Write exactly one file:
  {output_dir}/concept-candidates.md

Also write exactly:
  {output_dir}/result.yaml

with:
  status: discovered

The discovery artifact is a review checkpoint for a human. It must be useful
without requiring the reader to reconstruct the agent's reasoning from logs.

Before finishing, verify that you did not modify anything outside the
temporary output directory.
""".strip()


def synthesis_prompt(output_dir, mode):
    action = {
        "synthesize": "synthesize approved concept candidates into new durable notes",
        "update": "update existing concept notes where the newly accumulated sources materially change or extend them",
    }[mode]

    if mode == "synthesize":
        source = f"""
The approved candidate list is:
{CANDIDATES}

Read that file first. Only synthesize candidates that are explicitly marked
as approved for synthesis. If the file does not contain explicit approvals,
stop and report that there are no approved candidates.
"""
    else:
        source = f"""
Existing concept notes are under:
{CONCEPTS}

Identify notes that are materially affected by newly available meeting notes
or other sources. Do not rewrite notes merely for stylistic reasons.
"""

    return f"""
You are performing KNOWLEDGE SYNTHESIS for the SecondBrain project.

Mode: {mode}
Task: {action}.

Repository:
{ROOT}

Your synthesis rules are:
{SYNTHESIS_RULES}

{source}

Relevant primary corpus:
{MEETINGS}

Additional sources to inspect when relevant:
{REFERENCES}
{PRESENTATIONS}
{PROCEEDINGS}
{CODE_INDEX}

Core requirements:
- Concept notes are durable synthesis, not meeting summaries.
- Use multiple sources where available.
- Prefer source-backed statements over inference.
- Preserve historical evolution and disagreements.
- Distinguish decisions, proposals, current understanding, and open questions.
- Do not silently reconcile conflicting sources.
- Do not invent missing details.
- Do not create a note merely because an entity is in the seed vocabulary.
- Keep each note focused on one durable concept.
- Link related concepts with Obsidian wikilinks when the relationship is
  meaningful, even if the target note does not yet exist.
- Do not create person notes or incidental entity notes as a side effect.

OUTPUT:
Create the validated concept notes only in:
{output_dir}

Each concept note must:
- have YAML frontmatter with at least:
    type: concept
- have a concise title
- explain the durable concept and its context
- synthesize relevant technical/organizational understanding
- identify important historical evolution where relevant
- include uncertainty/disagreement where relevant
- include a "## Sources" section containing Obsidian links or repository
  paths to the supporting source notes/documents
- avoid copying long passages from sources

Also create:
  {output_dir}/result.yaml

with:
  status: {"synthesize": "synthesized", "update": "updated"}[mode]

Do not modify existing concept notes directly during this operation.
The Python wrapper will install the validated outputs.

Before finishing:
1. Verify every generated note is substantive.
2. Verify every generated note has a Sources section.
3. Verify you did not modify anything outside the temporary output directory.
""".strip()


def run_discover(agent):
    DISCOVERY_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
        prefix="secondbrain-synthesis-",
        dir=ROOT / "processor",
    ) as tmp:
        output_dir = Path(tmp)
        run_agent(discovery_prompt(output_dir), output_dir, agent)
        candidate_file = validate_discovery(output_dir)

        # Discovery intentionally installs only the review artifact.
        if CANDIDATES.exists():
            raise RuntimeError(
                f"Refusing to overwrite existing discovery artifact: {CANDIDATES}"
            )

        candidate_file.rename(CANDIDATES)

    print(f"Discovery artifact: {CANDIDATES}")


def run_synthesis(agent, mode):
    if mode == "synthesize" and not CANDIDATES.exists():
        raise RuntimeError(
            f"No candidate file found at {CANDIDATES}. "
            "Run 'discover' first and explicitly approve candidates."
        )

    with tempfile.TemporaryDirectory(
        prefix="secondbrain-synthesis-",
        dir=ROOT / "processor",
    ) as tmp:
        output_dir = Path(tmp)
        run_agent(synthesis_prompt(output_dir, mode), output_dir, agent)
        notes = validate_synthesis(output_dir, mode)

        installed = install_notes(
            notes,
            allow_existing=(mode == "update"),
        )

    print()
    for note in installed:
        print(f"{'Updated' if mode == 'update' else 'Installed'}: {note}")
    print(f"{len(installed)} concept note(s) handled.")


def main():
    parser = argparse.ArgumentParser(
        description="Synthesize durable knowledge for SecondBrain."
    )
    parser.add_argument(
        "mode",
        choices=["discover", "synthesize", "update"],
        help="Synthesis operation to perform.",
    )
    parser.add_argument(
        "--agent",
        choices=["codex", "claude"],
        default="codex",
        help="Agent to use (default: codex).",
    )

    args = parser.parse_args()

    if not SYNTHESIS_RULES.exists():
        parser.error(f"Missing synthesis rules: {SYNTHESIS_RULES}")

    if not ROOT.exists():
        parser.error(f"Repository root does not exist: {ROOT}")

    if args.mode == "discover":
        run_discover(args.agent)
    else:
        run_synthesis(args.agent, args.mode)

    return 0


if __name__ == "__main__":
    sys.exit(main())
