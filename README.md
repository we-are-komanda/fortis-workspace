# Fortis Workspace

Umbrella workspace for the Fortis ecosystem.

This repository stores the Fortis frontend application, project knowledge base, and workspace-level context: how the Fortis repositories fit together, how agents should navigate them, and which repository owns each kind of change.

## Repositories

- `frontend/` - Fortis frontend application, tracked directly in this repository.
- `backend/` - reserved path for the Fortis backend repository.
- `knowledge-base/` - Obsidian-compatible project knowledge base, tracked directly in this repository.
- `Fortis/` - legacy local Obsidian vault copy kept outside the parent Git history.

The frontend and knowledge base are owned directly by this repository.

## Agent Workflow

Open this directory as the workspace when working across the Fortis ecosystem.

Before making durable product, architecture, UX, or domain decisions, read the knowledge base index and relevant notes. Record durable decisions back into the knowledge base.

Backend setup is pending implementation. The current `backend/` directory is the reserved in-repository location for backend/API code unless a future ADR chooses a separate backend repository.
