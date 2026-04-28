## Feature: Log Parser

### Accepts
- Lines matching `YYYY-MM-DD HH:MM:SS LEVEL message` where LEVEL is ERROR, WARNING, INFO, or DEBUG
- Multi-word messages
- Files with mixed severity levels
- Files with blank lines or non-matching lines (skipped silently)

### Rejects
- Lines missing timestamp, level, or message (skipped, not raised)
- Levels outside ERROR / WARNING / INFO / DEBUG (not parsed)
- Empty input string (returns empty list, no error)
