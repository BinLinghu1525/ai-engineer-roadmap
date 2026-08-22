# Week 1 — Python Engineering Learning Notes

## Concepts learned

### Entry point and modules

`main.py` is the entry point. Importing a module executes its top-level code,
but guarded code under `if __name__ == "__main__"` runs only when the file is
executed directly.

### Module dependency, call chain, and data flow

These are related but different views:

- module dependency: `main → agent → service → formatter`;
- call chain: `main() → complete_topic() → create_learning_message() → normalize_topic()`;
- data flow: raw topic → validated string → normalized string → message → state.

### Object state

`LearningSession.completed_topics` is created in `__init__`, so every session
owns an independent list. A class-level mutable list would accidentally share
state between sessions.

### Function contracts and exceptions

The service accepts a non-empty string. It raises `TypeError` for a wrong type
and `ValueError` for blank input. Failed operations do not update session state.

### Pure logic and side effects

Text normalization is a pure transformation. Printing and updating session
history are visible state changes. Keeping these responsibilities separate
makes behavior easier to test.

### Vibe-coding review workflow

The safe loop is: define acceptance criteria → ask AI to inspect → approve a
small plan → review the diff → run tests → inspect staged changes → commit →
push. Code is not accepted merely because AI says it should work.

## Evidence

The [`mini_agent`](../01_python_engineering/mini_agent/) experiment provides
source code, documented JSON cases, and automated tests for these concepts.

## Reflection

The most useful reading strategy is to find the entry point first, map imports,
trace one call chain, and then follow the data. This creates an architectural
map before reading implementation details line by line.
