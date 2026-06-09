# Fortis Workspace Instructions

This is the workspace for the Fortis ecosystem.

The parent repository owns the frontend application and knowledge base directly, and keeps workspace-level instructions in the parent repo.

## Repository Map

- `frontend/` - frontend application tracked directly in this repository.
- `backend/` - reserved backend/API path. Prefer implementing the backend directly here unless the team explicitly decides to split it into a separate repository.
- `knowledge-base/` - Obsidian-compatible knowledge base tracked directly in this repository.
- `Fortis/` - legacy local Obsidian vault copy kept outside the parent Git history.

## Repository Boundaries

- Parent repo stores the frontend, knowledge base, workspace-level instructions, scripts, and coordination docs.
- Frontend changes happen in `frontend/` and are committed in the parent repository.
- Backend changes happen in `backend/`.
- Durable context lives in `knowledge-base/` and is committed in the parent repository.
- Keep backend history in this repository unless a future ADR chooses a separate backend repository.
- If a future child repository is added, document the repository boundary and workflow in the knowledge base first.
- Do not copy external repository source files into this repo without a recorded ownership decision.
- Do not store secrets, credentials, private keys, or production tokens in any repository.

## Context First

Before making durable product, UX, architecture, domain, or integration decisions:

1. Read `knowledge-base/00_Index.md`.
2. Check relevant notes in `knowledge-base/`.
3. If the decision changes project direction, update the knowledge base.

Prefer durable notes over chat-only memory.

## Knowledge Base Update Triggers

Update `knowledge-base/` when the conversation or implementation produces:

- a new requirement
- a changed assumption
- a rejected approach
- a chosen architecture
- a backend/frontend contract
- a deployment or environment rule
- a security, privacy, or data-retention constraint
- an unresolved open question

Use Markdown compatible with Obsidian. Prefer Obsidian links where useful, for example `[[Glossary]]` or `[[Architecture Overview]]`.

## Decision Logging

Record durable decisions in the knowledge base when they affect:

- product scope
- domain model
- API contracts
- frontend/backend boundaries
- security
- deployment
- data model
- AI/model integrations

Use ADR-style notes for architecture decisions.

## Backend/Frontend Boundary

Frontend and backend details should be linked through explicit contracts:

- API routes and schemas
- auth/session assumptions
- environment variables
- deployment notes
- integration risks

If a decision affects more than one repository, record it in the knowledge base and implement code changes in each owning repository separately.

## Engineering Guards

- Prefer existing project patterns over new abstractions.
- Keep changes scoped to the owning repository.
- Do not refactor unrelated code.
- Do not introduce new dependencies without a clear reason.
- Run relevant tests/checks before claiming work is complete.
- Never overwrite user changes.
- Never use destructive Git commands unless the user explicitly asks for that operation.

## Next.js Guard

The frontend may use a Next.js version with breaking changes.

Before changing Next.js APIs, routing, config, server/client boundaries, caching, build behavior, or file conventions, read the relevant guide in:

`frontend/node_modules/next/dist/docs/`

Heed deprecation notices.

## Agent Skills To Prefer

- Use systematic debugging when investigating bugs, failed tests, broken UI, or unclear runtime behavior.
- Use test-driven development for bug fixes and behavior changes when the expected behavior can be specified.
- Use frontend design and responsive UI guidelines when changing user-facing screens.
- Use official/local Next.js docs before changing framework behavior.
- Use verification-before-completion before reporting that implementation is complete.
