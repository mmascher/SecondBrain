#!/usr/bin/env python3

from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "raw transcripts"
MEETINGS = ROOT / "obsidian" / "20-Meetings"
STATE = ROOT / "processor" / "state.yaml"

LARGE_BYTES = 200_000


def load_previous_state():
    if not STATE.exists():
        return {}

    with STATE.open() as f:
        data = yaml.safe_load(f) or {}

    return {
        item["path"]: item
        for item in data.get("transcripts", [])
        if isinstance(item, dict) and "path" in item
    }


def get_transcript_file(directory):
    files = sorted(directory.glob("*.txt"))

    if len(files) != 1:
        print(
            f"WARNING: {directory.name}: "
            f"expected exactly one .txt file, found {len(files)}"
        )

    return files[0] if files else None


def build_source_map():
    """
    Build:

        transcript directory name -> existing Obsidian note

    from the explicit ## Source section.

    Example:

        meeting_saved_closed_caption.txt
        (from `2025-12-11 17.18.16 Submission Infrastructure Weekly Meeting`)

    becomes:

        2025-12-11 17.18.16 Submission Infrastructure Weekly Meeting
            -> 2025-12-11-Submission-Infrastructure-Weekly-Meeting.md
    """

    mapping = {}

    for note in sorted(MEETINGS.glob("*.md")):
        text = note.read_text(errors="replace")

        match = re.search(
            r"(?m)^\s*.*\(\s*from\s+`([^`]+)`\s*\)\s*$",
            text,
        )

        if not match:
            print(f"WARNING: no source mapping found in {note.name}")
            continue

        source_directory = match.group(1).strip()

        if source_directory in mapping:
            print(
                f"WARNING: duplicate source mapping for "
                f"{source_directory}: "
                f"{mapping[source_directory].name} and {note.name}"
            )
            continue

        mapping[source_directory] = note

    return mapping


def classify(directory, transcript, previous, source_map):
    relative_path = str(directory.relative_to(RAW))

    # Preserve explicit decisions already recorded in state.yaml.
    old = previous.get(relative_path)

    if old and old.get("status") in {
        "processed",
        "skipped_non_substantive",
        "skipped_incomplete",
    }:
        return old["status"], old.get("manual", False), old.get("note")

    if old and old.get("manual") is True:
        return old["status"], True, old.get("note")

    # Existing meeting note.
    note = source_map.get(directory.name)

    if note:
        return (
            "processed",
            False,
            str(note.relative_to(ROOT)),
        )

    # Large transcript detection must use the TXT file size.
    if transcript.stat().st_size >= LARGE_BYTES:
        return "pending_large_transcript", False, None

    return "unprocessed", False, None


def main():
    directories = sorted(
        p for p in RAW.iterdir()
        if p.is_dir()
    )

    previous = load_previous_state()
    source_map = build_source_map()

    entries = []

    for directory in directories:
        transcript = get_transcript_file(directory)

        if transcript is None:
            continue

        status, manual, note = classify(
            directory,
            transcript,
            previous,
            source_map,
        )

        entry = {
            "path": str(directory.relative_to(RAW)),
            "transcript": transcript.name,
            "bytes": transcript.stat().st_size,
            "lines": sum(
                1 for _ in transcript.open(errors="replace")
            ),
            "status": status,
            "manual": manual,
        }

        if note:
            entry["note"] = note

        entries.append(entry)

    data = {
        "version": 1,
        "raw_transcripts": str(RAW),
        "meeting_notes": str(MEETINGS),
        "transcripts": entries,
    }

    with STATE.open("w") as f:
        yaml.safe_dump(
            data,
            f,
            sort_keys=False,
            allow_unicode=True,
        )

    counts = {}

    for entry in entries:
        counts[entry["status"]] = counts.get(entry["status"], 0) + 1

    print(f"Total transcripts: {len(entries)}")
    print(f"Processed: {counts.get('processed', 0)}")
    print(
        "Skipped non-substantive: "
        f"{counts.get('skipped_non_substantive', 0)}"
    )
    print(
        "Skipped incomplete: "
        f"{counts.get('skipped_incomplete', 0)}"
    )
    print(
        "Pending large transcript: "
        f"{counts.get('pending_large_transcript', 0)}"
    )
    print(f"Unprocessed: {counts.get('unprocessed', 0)}")

    print()
    print("Existing note associations:")

    for entry in entries:
        if entry["status"] == "processed":
            print(
                f"  {entry['path']}"
                f" -> {entry.get('note', '?')}"
            )

    print()
    print(f"State written to: {STATE}")


if __name__ == "__main__":
    main()
