# Fortis Workspace

Umbrella workspace for the Fortis ecosystem.

This repository stores workspace-level context for the Fortis ecosystem: how the Fortis repositories fit together, how agents should navigate them, and which repository owns each kind of change.

## Repositories

- `frontend/` - Fortis frontend application, tracked as a Git submodule from `Ramilko37/fortis-front`.
- `backend/` - Fortis backend/API repository, tracked as a Git submodule from `Ramilko37/fortis-back`.
- `knowledge-base/` - Obsidian-compatible project knowledge base, tracked as a Git submodule from `Ramilko37/fortis-knowledge-base`.
- `Fortis/` - legacy local Obsidian vault copy kept outside the parent Git history.

Frontend, backend, and knowledge base keep separate Git histories. The parent repository pins the selected commit for each submodule.

## Agent Workflow

Open this directory as the workspace when working across the Fortis ecosystem.

Before making durable product, architecture, UX, or domain decisions, read the knowledge base index and relevant notes. Record durable decisions back into the knowledge base.

Clone with submodules or initialize them after cloning:

```bash
git submodule update --init --recursive
```
