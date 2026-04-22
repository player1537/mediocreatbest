"""Amend the current git commit with a pi session's user messages."""

from __future__ import annotations

import json
import subprocess
import textwrap
from datetime import datetime
from pathlib import Path

import click
import questionary


def get_first_user_message_summary(session_file: Path) -> str:
    """Return a brief summary of the first user message in a session file."""
    with session_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "message":
                continue
            message = entry.get("message", {})
            if message.get("role") != "user":
                continue
            content = message.get("content", "")
            if isinstance(content, str):
                text = content.strip()
            elif isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block.get("text", "").strip())
                text = " ".join(parts).strip()
            else:
                text = str(content).strip()
            if text:
                return text[:50] + ("..." if len(text) > 50 else "")
    return "(no content)"


def extract_user_messages(session_file: Path) -> str:
    """Read a pi JSONL session file and return the concatenated user messages."""
    prompts: list[str] = []
    with session_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "message":
                continue
            message = entry.get("message", {})
            if message.get("role") != "user":
                continue
            content = message.get("content", "")
            if isinstance(content, str):
                text = content.strip()
            elif isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        parts.append(block.get("text", "").strip())
                text = " ".join(parts).strip()
            else:
                text = str(content).strip()
            if text:
                prompts.append(text)
    if not prompts:
        return ""
    wrapped = []
    for p in prompts:
        wrapped.append(textwrap.fill(p, width=72))
    return "\n\n---\n\n".join(wrapped)


def amend_commit_with_transcript(transcript_text: str) -> None:
    """Amend the current git commit, appending the transcript."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%B"],
            capture_output=True,
            text=True,
            check=True,
        )
        current_message = result.stdout.rstrip()

        lines = current_message.split("\n")
        trailer_indices = []
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i]
            if not line:
                break
            if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
                trailer_indices.append(i)
            else:
                break
        if trailer_indices:
            first_trailer = min(trailer_indices)
            body_end = (
                first_trailer - 1
                if first_trailer > 0 and not lines[first_trailer - 1]
                else first_trailer
            )
            message_body = "\n".join(lines[:body_end]).rstrip()
            trailers = "\n".join(lines[first_trailer:])
        else:
            message_body = current_message
            trailers = ""

        new_message = f"{message_body}\n\n### Transcript\n\n{transcript_text}"
        if trailers:
            new_message = f"{new_message}\n\n{trailers}"

        subprocess.run(
            ["git", "commit", "--amend", "-F", "-"],
            input=new_message,
            capture_output=True,
            text=True,
            check=True,
        )
        click.echo("✓ Commit amended with transcript")
    except subprocess.CalledProcessError as e:
        err = e.stderr.strip() if e.stderr else str(e)
        raise click.ClickException(f"Failed to amend commit: {err}") from e


@click.command()
def main() -> None:
    """Interactive CLI to select a pi session and amend the current git commit."""
    sessions_dir = Path.home() / ".pi" / "agent" / "sessions"
    if not sessions_dir.is_dir():
        click.echo(f"Pi sessions directory not found: {sessions_dir}")
        return

    session_files = sorted(
        sessions_dir.rglob("*.jsonl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )[:10]

    if not session_files:
        click.echo("No pi session files found.")
        return

    choices = []
    for fp in session_files:
        stat = fp.stat()
        mod = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        size_kb = stat.st_size / 1024
        preview = get_first_user_message_summary(fp)
        title = f"{mod}  {size_kb:5.0f}KB  {preview}"
        choices.append(questionary.Choice(title=title, value=fp))

    selected: Path | None = questionary.select(
        "Select a pi session to extract user messages from:",
        choices=choices,
    ).ask()

    if not selected:
        click.echo("No session selected.")
        return

    click.echo("Extracting user messages...")
    transcript = extract_user_messages(selected)
    if not transcript:
        click.echo("No user messages found in the chosen session.")
        return

    click.echo("Amending current commit...")
    amend_commit_with_transcript(transcript)
    click.echo("\n✓ Done! Transcript added to commit message.")


def cli(args: list[str] | None = None):
    main(args)


if __name__ == "__main__":
    main()
