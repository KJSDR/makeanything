## Feature: MCP Server

### Accepts
- Valid file path to an existing log file → returns formatted summary string
- Log file with parseable events → returns full summary with root cause and recommendations

### Rejects
- Non-existent file path → returns error string "Error: file not found: <path>" (does not raise)
- File with no parseable events → returns "No parseable log events found in file." (does not raise)

### Exposes
- One MCP tool: `analyze_log(filepath: str) -> str`
- Server name: `LogLens`
- Transport: stdio (default FastMCP)
