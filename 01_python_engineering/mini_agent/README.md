# Mini Learning Agent

A small, evidence-based Python experiment developed during Week 1 of the AI
engineering roadmap. It demonstrates how a program moves from an entry point
through service and formatting layers while keeping session state explicit.

## Learning evidence

This experiment covers:

- Python entry points, modules, imports, and call chains;
- separation between formatting, business rules, and application state;
- instance state that is isolated between `LearningSession` objects;
- explicit `TypeError` and `ValueError` contracts;
- JSON-driven normal, boundary, Unicode, and wrong-type cases;
- pytest verification of success paths, failure paths, and state isolation.

## Structure

```text
mini_agent/
├── agent.py                 # Stateful LearningSession
├── formatter.py             # Pure text normalization
├── service.py               # Validation and message creation
├── main.py                  # Program entry point
├── experiment.py            # JSON-driven reproducible experiment
├── fixtures/topic_cases.json # Documented experiment inputs
└── tests/                   # Focused pytest cases
```

Module dependency:

```text
main.py → agent.py → service.py → formatter.py
```

Data flow:

```text
raw topic → validation → normalization → message → session state → output
```

## Run

From this directory:

```powershell
python main.py
python experiment.py
pytest -q
```

From the repository root, the same test suite can be run with:

```powershell
pytest -q 01_python_engineering/mini_agent/tests
```

Expected application output:

```text
Today we learn: python agent
Completed topics: ['python agent']
```

## Experiment design

`fixtures/topic_cases.json` contains five cases:

| Case | Purpose |
| --- | --- |
| `normal-lowercase` | Baseline success path |
| `trim-and-normalize` | Whitespace and case normalization |
| `unicode-topic` | Chinese/English Unicode handling |
| `blank-topic` | Business validation failure |
| `wrong-type` | Runtime type-contract failure |

The experiment prints structured JSON so results are easy to inspect or reuse.
State changes occur only after validation and message creation succeed.

Validation snapshot on 2026-08-19: all five documented data cases and seven
focused behavior checks passed (`12 passed`).

## Limitations and next steps

- State exists only in memory and disappears when the process exits.
- The experiment has no CLI arguments, persistence, logging, or API calls.
- A later iteration can add file persistence after its failure modes and tests
  are designed explicitly.
