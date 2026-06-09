# ADR-0002: Knowledge Base Owned by Parent Repository

## Status

Accepted

## Date

2026-06-09

## Context

The Fortis workspace previously tracked `knowledge-base/` as a Git submodule pointing to `Ramilko37/fortis-knowledge-base`.

After moving `frontend/` into the parent repository, the project direction also changed for durable context: the knowledge base should live directly in the Fortis workspace repository instead of relying on a separate remote.

## Decision

Track `knowledge-base/` directly in the parent Fortis repository instead of as a Git submodule.

## Consequences

- Knowledge-base changes are committed in the parent Fortis repository.
- The parent repository now owns both frontend source and durable project context.
- The old `Ramilko37/fortis-knowledge-base` remote is no longer part of the active workspace configuration.
- The workspace currently has no active Git submodules.
