#!/usr/bin/env python3

"""
Process meeting transcripts into Obsidian meeting notes.

This script is deliberately conservative.

Python is responsible for:
  - selecting eligible transcripts
  - protecting existing notes
  - invoking Codex
  - verifying output
  - updating state.yaml

Codex is responsible for:
  - reading the complete transcript
  - following processor/AGENTS.md
  - deciding whether the transcript is substantive
  - synthesizing the meeting note
"""

from pathlib import Path
import argparse
import subprocess
import sys
import tempfile
import yaml


ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw transcripts"
MEETINGS = ROOT / "obsidian" / "20-Meetings"
STATE = ROOT / "processor" / "state.yaml"


ELIGIBLE_STATUS = "unprocessed"


def load_state():
    if not STATE.exists():
        raise RuntimeError(
            f"State file does not exist: {STATE}\n"
            "Run inventory.py first."
        )

    with STATE.open() as f:
        return yaml.safe_load(f) or {}


def save_state(data):
    # Write atomically so an interrupted run cannot leave a half-written state.
    with tempfile.NamedTemporaryFile(
        "w",
        dir=STATE.parent,
        prefix=".state.",
        suffix=".yaml",
        delete=False,
    ) as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            allow_unicode=True,
        )
        temporary = Path(f.name)

    temporary.replace(STATE)


def get_entries(data):
    return data.get("transcripts", [])


def find_entry(data, relative_path):
    for entry in get_entries(data):
        if entry.get("path") == relative_path:
            return entry
    return None


def eligible_entries(data):
    """
    Return transcripts which are safe for normal automatic processing.

    Large transcripts, manual-review items, skipped recordings, and already
    processed transcripts are deliberately excluded.
    """
    result = []

    for entry in get_entries(data):
        if entry.get("status") != ELIGIBLE_STATUS:
            continue

        # Never process something explicitly marked manual.
        if entry.get("manual") is True:
            continue

        result.append(entry)

    return result


def transcript_path(entry):
    return RAW / entry["path"] / entry["transcript"]


def expected_note_path(transcript):
    """
    We do not try to reproduce Codex's title-generation logic here.

    Instead, Codex is asked to determine the canonical note filename from
    the transcript/meeting information. This function is therefore only
    used to detect obviously conflicting existing files when a note path
    is explicitly supplied by the agent.
    """
    return None


def run_agent(transcript, output_dir, agent):
    """
    Run the selected coding agent on exactly one transcript.
    """

    relative_transcript = transcript.relative_to(ROOT)

    prompt = f"""
You are processing exactly ONE meeting transcript for the
SubmissionInfrastructureBrain project.

Repository:
{ROOT}

Transcript:
{relative_transcript}

Your instructions are defined by:
{ROOT / "processor" / "AGENTS.md"}

Read and follow that AGENTS.md completely.

IMPORTANT SOURCE-OF-TRUTH RULES:

- The transcript is the source of truth.
- Read the COMPLETE transcript before writing the note.
- Do not invent facts, decisions, participants, dates, actions, or conclusions.
- Distinguish decisions/conclusions from proposals, opinions, observations,
  and open questions.
- Preserve important technical terminology.
- Do not create Phase 2 concept notes.
- Do not modify the original transcript.
- Do not modify any existing Obsidian meeting note.
- Do not create unrelated files.
- If the transcript is genuinely non-substantive, do not fabricate a note.
- If the transcript is incomplete/corrupted enough that a reliable note cannot
  be produced, do not fabricate one.

OUTPUT REQUIREMENT:

You have exactly TWO valid outcomes.

OUTCOME 1 — SUBSTANTIVE TRANSCRIPT

Create exactly ONE new Obsidian meeting note in this temporary output
directory:

{output_dir}

The note must follow the Phase 1 meeting-note format specified in AGENTS.md.

The filename should be a clean Obsidian-compatible Markdown filename,
normally based on the meeting date and title.

The note MUST contain the correct ## Source section pointing back to the
original transcript directory, using the source format already established
in this repository.

Also create:

    {output_dir}/result.yaml

containing exactly:

    status: processed

OUTCOME 2 — NON-SUBSTANTIVE OR UNUSABLE TRANSCRIPT

If the transcript is genuinely non-substantive, or incomplete/corrupted
enough that a reliable meeting note cannot be produced, do NOT create a
Markdown meeting note.

Instead create:

    {output_dir}/result.yaml

containing:

    status: skipped_non_substantive

or:

    status: skipped_incomplete

Include a short reason:

    reason: "..."

Use skipped_non_substantive when the available transcript contains too
little substantive meeting content to reconstruct the discussion.

Use skipped_incomplete when the transcript appears to be a partial,
corrupted, or otherwise incomplete recording where the missing content
prevents reliable synthesis.

Before finishing:

1. Verify that you read the complete transcript.
2. Verify that your classification is supported by the transcript.
3. Verify that you did not modify anything outside the temporary output
   directory.
4. Ensure the temporary output directory contains exactly one result.yaml
   and, only for a substantive transcript, exactly one .md file.

Do not merely describe what you would write. Actually create the required
result.yaml, and create the Markdown file only for a substantive transcript.
""".strip()

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


def validate_output(output_dir):
    result_file = output_dir / "result.yaml"

    if not result_file.exists():
        raise RuntimeError(
            "Agent completed without producing result.yaml."
        )

    try:
        result = yaml.safe_load(result_file.read_text()) or {}
    except yaml.YAMLError as exc:
        raise RuntimeError(
            f"Invalid result.yaml: {exc}"
        ) from exc

    status = result.get("status")

    valid_statuses = {
        "processed",
        "skipped_non_substantive",
        "skipped_incomplete",
    }

    if status not in valid_statuses:
        raise RuntimeError(
            f"Invalid agent status in result.yaml: {status!r}"
        )

    notes = sorted(output_dir.glob("*.md"))

    if status == "processed":
        if len(notes) != 1:
            raise RuntimeError(
                "Agent reported status=processed but did not produce "
                "exactly one Markdown meeting note."
            )

        note = notes[0]

        if note.stat().st_size == 0:
            raise RuntimeError("Generated meeting note is empty.")

        text = note.read_text(errors="replace")

        required_sections = [
            "## Summary",
            "## Decisions / Conclusions",
            "## Action Items",
            "## Discussion",
            "## Open Questions",
            "## Related",
            "## Source",
        ]

        missing = [
            section
            for section in required_sections
            if section not in text
        ]

        if missing:
            raise RuntimeError(
                "Generated note is missing required sections:\n"
                + "\n".join(missing)
            )

        return status, note

    # Skipped outcomes must not contain a Markdown note.
    if notes:
        raise RuntimeError(
            f"Agent reported status={status} but also produced "
            f"Markdown file(s):\n"
            + "\n".join(str(p) for p in notes)
        )

    if not result.get("reason"):
        raise RuntimeError(
            f"Agent reported status={status} without a reason."
        )

    return status, None


def install_note(note):
    """
    Move a validated new note into the Obsidian meeting directory.

    Never overwrite an existing file.
    """
    destination = MEETINGS / note.name

    if destination.exists():
        raise RuntimeError(
            f"Refusing to overwrite existing note: {destination}"
        )

    note.rename(destination)
    return destination


def mark_processed(data, entry, note):
    entry["status"] = "processed"
    entry["manual"] = False
    entry["note"] = str(note.relative_to(ROOT))


def mark_skipped(data, entry, status, reason):
    entry["status"] = status
    entry["manual"] = False
    entry["reason"] = reason


def process_entry(data, entry, agent):
    transcript = transcript_path(entry)

    if not transcript.exists():
        raise RuntimeError(
            f"Transcript does not exist: {transcript}"
        )

    print()
    print("=" * 72)
    print(f"Processing: {entry['path']}")
    print(f"Transcript: {entry['transcript']}")
    print(f"Size:       {entry['bytes']:,} bytes")
    print("=" * 72)

    with tempfile.TemporaryDirectory(
        prefix="submission-brain-",
        dir=ROOT / "processor",
    ) as tmp:
        output_dir = Path(tmp)

        run_agent(transcript, output_dir, agent)

        status, note = validate_output(output_dir)

        if status == "processed":
            print()
            print(f"Generated note: {note.name}")

            destination = install_note(note)

            mark_processed(data, entry, destination)
            save_state(data)

            print(f"Installed: {destination}")
            print("State updated: processed")

            return

        reason = yaml.safe_load(
            (output_dir / "result.yaml").read_text()
        ).get("reason", "")

        mark_skipped(data, entry, status, reason)
        save_state(data)

        print()
        print(f"Skipped: {status}")
        print(f"Reason:  {reason}")
        print(f"State updated: {status}")

def main():
    parser = argparse.ArgumentParser(
        description="Process meeting transcripts into Obsidian notes."
    )

    parser.add_argument(
        "--agent",
        choices=["codex", "claude"],
        default="codex",
        help="Agent to use for transcript processing (default: codex).",
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--next",
        action="store_true",
        help="Process the next eligible transcript.",
    )

    group.add_argument(
        "--path",
        help="Process one specific transcript directory.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help="Maximum number of transcripts to process (default: 1).",
    )

    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be >= 1")

    data = load_state()

    if args.path:
        target = Path(args.path)

        if target.is_absolute():
            try:
                target = target.relative_to(RAW)
            except ValueError:
                parser.error(
                    f"Path must be inside {RAW}"
                )

        entry = find_entry(data, str(target))

        if entry is None:
            parser.error(
                f"Transcript not found in state.yaml: {target}"
            )

        entries = [entry]

    else:
        entries = eligible_entries(data)[:args.limit]

    if not entries:
        print("No eligible transcripts found.")
        return 0

    print(f"Selected {len(entries)} transcript(s).")

    for entry in entries:
        try:
            process_entry(data, entry, args.agent)

        except Exception as exc:
            print()
            print("ERROR:")
            print(exc)
            print()
            print(
                "The transcript was NOT marked as processed."
            )
            print(
                "No state change was committed for this transcript."
            )
            return 1

    print()
    print(f"Successfully processed {len(entries)} transcript(s).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
