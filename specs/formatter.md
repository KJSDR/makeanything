## Feature: Formatter

### Accepts
- Summary dict with keys: counts, time_range, errors, warnings, root_cause, recommendations, rag_hit
- Empty errors or warnings lists (omits that section)
- Empty recommendations list (omits that section)
- rag_hit = True (appends RAG notice line)
- rag_hit = False or missing (no RAG notice)

### Rejects
- N/A — formatter is display-only, no validation needed
