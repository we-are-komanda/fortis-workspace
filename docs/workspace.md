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

Current state:

- `frontend/` is cloned from `git@github.com:Ramilko37/awesome-project.git`.
- `knowledge-base/` is cloned from `git@github.com:Ramilko37/fortis-knowledge-base.git`.
- `backend/` is reserved and should be connected after the exact backend remote URL is known.
- `Fortis/` remains as a legacy local vault copy and is ignored by the parent repository.

## Subrepo Strategy

The workspace uses Git submodules for child repositories so GitHub shows the ecosystem shape and the parent repository pins exact child commits.

When a child repository changes:

1. Commit and push inside the child repository.
2. Return to the parent repository.
3. Commit the updated submodule pointer.
