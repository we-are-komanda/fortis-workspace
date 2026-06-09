# ADR-0001: Frontend Owned by Parent Repository

## Status

Accepted

## Date

2026-06-09

## Context

The Fortis workspace previously tracked `frontend/` as a Git submodule pointing to `Ramilko37/awesome-project`.

The project direction changed: Fortis frontend development should now happen directly in the Fortis workspace repository, without depending on or referencing the previous `awesome-project` remote.

## Decision

Track `frontend/` directly in the parent Fortis repository instead of as a Git submodule.

At the time of this decision, `knowledge-base/` remained an independent submodule. It was later moved into the parent repository by [[03_Architecture/ADR-0002-knowledge-base-owned-by-parent-repository|ADR-0002]].

## Consequences

- Frontend changes are committed in the parent Fortis repository.
- The parent repository now owns the frontend source tree.
- The old `Ramilko37/awesome-project` remote is no longer part of the active workspace configuration.
- Cross-repository coordination was still needed for `knowledge-base/` until ADR-0002 moved it into the parent repository.
