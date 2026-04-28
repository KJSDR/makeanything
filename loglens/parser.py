import re
from dataclasses import dataclass

_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(ERROR|WARNING|INFO|DEBUG)\s+(.+)$"
)


@dataclass
class LogEvent:
    timestamp: str
    level: str
    message: str


def parse(text: str) -> list[LogEvent]:
    events = []
    for line in text.splitlines():
        m = _PATTERN.match(line.strip())
        if m:
            events.append(LogEvent(timestamp=m.group(1), level=m.group(2), message=m.group(3)))
    return events
