# Fortis Workspace

Umbrella workspace for the Fortis ecosystem.

This repository stores workspace-level context only: how the Fortis repositories fit together, how agents should navigate them, and which repository owns each kind of change.

## Repositories

- `frontend/` - Fortis frontend application, cloned from `Ramilko37/awesome-project`.
- `backend/` - reserved path for the Fortis backend repository.
- `knowledge-base/` - Obsidian-compatible project knowledge base, cloned from `Ramilko37/fortis-knowledge-base`.
- `Fortis/` - legacy local Obsidian vault copy kept outside the parent Git history.

Each child project keeps its own Git history. Do not commit frontend, backend, or Obsidian vault content into this parent repository.

## Agent Workflow

Open this directory as the workspace when working across the Fortis ecosystem.

Before making durable product, architecture, UX, or domain decisions, read the knowledge base index and relevant notes. Record durable decisions back into the knowledge base.

Backend setup is pending the exact repository remote URL.
