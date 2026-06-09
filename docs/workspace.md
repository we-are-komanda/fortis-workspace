# Workspace Notes

The parent repository is a coordination layer, not an application monorepo.

Recommended local layout:

```text
Fortis/
├── AGENTS.md
├── README.md
├── docs/
├── frontend/
├── backend/
└── knowledge-base/
```

The current local Obsidian vault may live at `Fortis/` until it is renamed or cloned as `knowledge-base/`.

## Subrepo Strategy

Start with nested repositories ignored by the parent repository. This keeps day-to-day work simple while preserving separate Git histories.

Move to Git submodules only if the team needs the parent repository to pin exact commits of frontend, backend, and knowledge-base.

