# Python Engineering

## Learning Goals

- Move from scripting toward maintainable, production-oriented Python.
- Organize, test, debug, and explain small Python systems.
- Apply typing, error handling, logging, and asynchronous programming appropriately.

## Key Topics

- Project structure, modules, packages, and virtual environments
- Typing, exceptions, logging, `pathlib`, and dataclasses
- Pydantic concepts and data validation
- Decorators, generators, and context managers
- `async`/`await`
- Testing with pytest

## Practice Tasks

- Package a small command-line utility with clear module boundaries.
- Add typed data models, explicit error handling, and structured logging.
- Design focused pytest cases for meaningful behavior and failure paths.
- Compare synchronous and asynchronous implementations of a small I/O workflow.

## Completion Criteria

- Explain the role of packages, environments, typing, exceptions, and tests.
- Build a readable multi-module Python program without hidden configuration.
- Run and interpret its tests, including expected failure cases.
- Document setup, usage, design decisions, and limitations.

## Current evidence

- [`mini_agent`](mini_agent/) — a multi-module learning application with
  explicit state, input contracts, a JSON experiment dataset, and pytest tests.
- [`Week 1 learning notes`](../notes/week-01-python-engineering.md) — concise
  explanations of entry points, call chains, state, exceptions, side effects,
  and the AI-assisted Git workflow.
