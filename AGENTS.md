# Fortis Workspace Instructions

This is the umbrella workspace for the Fortis ecosystem.

## Repository Map

- `frontend/` - frontend application repository.
- `backend/` - backend/API repository.
- `knowledge-base/` - preferred path for the Obsidian-compatible knowledge base repository.
- `Fortis/` - current local Obsidian vault path, if `knowledge-base/` has not been created or renamed yet.

## Rules

- Keep frontend, backend, and knowledge-base Git histories separate.
- The parent repository stores only workspace-level instructions, scripts, and coordination docs.
- Code changes happen inside the owning child repository.
- Durable product, domain, architecture, UX, and integration decisions are recorded in the knowledge base.
- Before major decisions, read the knowledge base index and relevant notes.
- Do not store secrets in any repository.

## Knowledge Base Usage

Use Markdown compatible with Obsidian.

Prefer durable notes over chat-only memory:

- product decisions
- architecture decisions
- domain vocabulary
- backend/frontend contracts
- UX principles
- meeting summaries
- open questions

When the knowledge base has an index, start from `00_Index.md`.

## Backend/Frontend Boundary

Frontend and backend details should be linked through explicit contracts:

- API routes and schemas
- auth/session assumptions
- environment variables
- deployment notes
- integration risks

If a decision affects more than one repository, record it in the knowledge base and implement code changes in each owning repository separately.

