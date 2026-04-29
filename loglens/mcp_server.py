from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

from loglens import formatter, parser, summarizer

mcp = FastMCP("LogLens")


@mcp.tool()
def analyze_log(filepath: str) -> str:
    """Analyze a log file and return a structured summary with root cause and recommendations."""
    path = Path(filepath)
    if not path.exists():
        return f"Error: file not found: {filepath}"

    events = parser.parse(path.read_text())
    if not events:
        return "No parseable log events found in file."

    summary = summarizer.summarize(events)
    return formatter.format_summary(summary)


if __name__ == "__main__":
    mcp.run()
