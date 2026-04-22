"""Amend the current git commit with a Claude Code session transcript."""

from __future__ import annotations

import re
import subprocess
import textwrap
from datetime import datetime
from pathlib import Path

import click
import questionary

from claude_code_transcripts import find_local_sessions, parse_session_file


def filter_message_content(text: str) -> str:
    """Remove XML tags and skill execution details from message content."""
    text = re.sub(r'<command-\w+>.*?</command-\w+>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)

    if 'Base directory for this skill' in text:
        text = text.split('Base directory for this skill')[0]

    lines = text.split('\n')
    filtered_lines = []
    for i, line in enumerate(lines):
        if line.strip() == '---' and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line.startswith('<command-') or next_line.startswith('Base directory'):
                break
        filtered_lines.append(line)

    return '\n'.join(filtered_lines).strip()


def extract_user_prompts(session_file: Path) -> str:
    """Extract user prompts from session file and format as Markdown."""
    session_data = parse_session_file(session_file)
    loglines = session_data.get('loglines', [])

    prompts = []
    for entry in loglines:
        if entry.get('type') != 'user':
            continue

        message = entry.get('message', {})
        content = message.get('content', '')

        if isinstance(content, str):
            text = content.strip()
        elif isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, dict):
                    if block.get('type') == 'text':
                        text_parts.append(block.get('text', '').strip())
            text = ' '.join(text_parts)
        else:
            text = str(content).strip()

        if text:
            text = filter_message_content(text)
            if text:
                prompts.append(text)

    if not prompts:
        return ''

    wrapped_prompts = []
    for prompt in prompts:
        wrapped = textwrap.fill(prompt, width=72)
        wrapped_prompts.append(wrapped)

    return '\n\n---\n\n'.join(wrapped_prompts)


def amend_commit_with_transcript(transcript_text: str) -> None:
    """Amend the current git commit to include the transcript."""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%B'],
            capture_output=True,
            text=True,
            check=True,
        )
        current_message = result.stdout.rstrip()

        lines = current_message.split('\n')

        trailer_indices = []
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i]
            if not line:
                break
            if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
                trailer_indices.append(i)
            else:
                break

        if trailer_indices:
            first_trailer_idx = min(trailer_indices)
            if first_trailer_idx > 0 and not lines[first_trailer_idx - 1]:
                body_end = first_trailer_idx - 1
            else:
                body_end = first_trailer_idx

            message_body = '\n'.join(lines[:body_end]).rstrip()
            trailers_text = '\n'.join(lines[first_trailer_idx:])
        else:
            message_body = current_message
            trailers_text = ''

        new_message = f'{message_body}\n\n### Transcript\n\n{transcript_text}'
        if trailers_text:
            new_message = f'{new_message}\n\n{trailers_text}'

        subprocess.run(
            ['git', 'commit', '--amend', '-F', '-'],
            input=new_message,
            capture_output=True,
            text=True,
            check=True,
        )
        click.echo('✓ Commit amended with transcript')
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        raise click.ClickException(f'Failed to amend commit: {error_msg}') from e


@click.command()
def main() -> None:
    """Extract user prompts from a Claude Code session and amend the current commit."""
    projects_folder = Path.home() / '.claude' / 'projects'

    if not projects_folder.exists():
        click.echo(f'Projects folder not found: {projects_folder}')
        click.echo('No local Claude Code sessions available.')
        return

    click.echo('Loading local sessions...')
    results = find_local_sessions(projects_folder, limit=10)

    if not results:
        click.echo('No local sessions found.')
        return

    choices = []
    for filepath, summary in results:
        stat = filepath.stat()
        mod_time = datetime.fromtimestamp(stat.st_mtime)
        size_kb = stat.st_size / 1024
        date_str = mod_time.strftime('%Y-%m-%d %H:%M')
        if len(summary) > 50:
            summary = summary[:47] + '...'
        display = f'{date_str}  {size_kb:5.0f} KB  {summary}'
        choices.append(questionary.Choice(title=display, value=filepath))

    selected = questionary.select(
        'Select a session to convert:',
        choices=choices,
    ).ask()

    if selected is None:
        click.echo('No session selected.')
        return

    session_file = selected

    click.echo('Extracting user prompts...')
    transcript_text = extract_user_prompts(session_file)

    if not transcript_text:
        click.echo('No user prompts found in session.')
        return

    click.echo('Amending commit...')
    amend_commit_with_transcript(transcript_text)
    click.echo('\n✓ Done! Transcript added to commit.')


def cli(args: list[str] | None = None):
    main(args)


if __name__ == '__main__':
    main()
