# Backend Directory Structure

Use this when adding files under `src/signalforge`.

```text
src/signalforge/
├── api/
├── cache/
├── config/
├── contracts/
├── core/
├── llm/
├── models/
├── observability/
├── pipeline/
├── sources/
└── utils/
```

## Placement Rules

| New thing | Default location |
| --- | --- |
| FastAPI app, route, middleware, schema, or API error | `src/signalforge/api/` |
| Report persistence, status, or file cache behavior | `src/signalforge/cache/` |
| Runtime settings field or settings helper | `src/signalforge/config/` |
| Protocol/interface shared across modules | `src/signalforge/contracts/` |
| LLM model invocation or prompt-loading behavior | `src/signalforge/llm/` |
| Reusable Pydantic domain/report model | `src/signalforge/models/` |
| Pipeline orchestration, nodes, extraction, aggregation, events | `src/signalforge/pipeline/` |
| External source adapter | `src/signalforge/sources/` |
| Cross-cutting helper with 2+ real users | `src/signalforge/utils/` |

## Rules

- Keep route handlers thin and push pipeline/business behavior into the modules
  that own it.
- Keep local cache details behind cache abstractions.
- Do not add hosted auth/admin/billing modules to `main`.
- Add tests beside the behavior being changed; do not rely only on snapshots or
  manual API checks.
