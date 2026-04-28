from pathlib import Path

import click
from dotenv import load_dotenv

load_dotenv()

from loglens import formatter, parser, summarizer


@click.group()
def main():
    pass


@main.command()
@click.argument("logfile", type=click.Path(exists=True))
@click.option("--severity", default=None, help="Filter to this severity level (ERROR, WARNING, INFO)")
@click.option("--since", default=None, help="Only include events at or after this timestamp")
def summarize(logfile, severity, since):
    text = Path(logfile).read_text()
    events = parser.parse(text)

    if severity:
        events = [e for e in events if e.level == severity.upper()]
    if since:
        events = [e for e in events if e.timestamp >= since]

    if not events:
        click.echo("No matching log events found.")
        return

    summary = summarizer.summarize(events)
    click.echo(formatter.format_summary(summary))
