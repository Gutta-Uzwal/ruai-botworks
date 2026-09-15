# projects/

One folder per real client build, copied from a `Templates/<domain>/<template-name>/`
reference and then customized. Layout: `projects/<domain>/<client-project>/`.

## STATUS.yaml

Optional, one per project folder, next to its `DESIGN.md`. It is the only thing
the RU-AIBOTWORKS portal's **Projects** page reads to show what is running
across every client project at once — a project with no `STATUS.yaml` still
shows up (status `unknown`), because a silently missing status is exactly the
gap that page exists to surface.

This is a declared status, not an observed one: nothing currently watches
agent execution and writes this file for you. Update it yourself, or have the
agent working the project update it, whenever status actually changes.

```yaml
status: active            # planning | active | paused | blocked | complete
assigned:                 # registry handles — checked against RU-AIBOTWORKS/REGISTRY
  - web-architect
  - frontend-engineer-07
started: 2026-09-15
notes: Implementation phase, waiting on client asset delivery.
```

- `status` — one of the five values above. Anything else is shown as-is but
  won't sort into the usual bucket.
- `assigned` — registry handles (officer or agent `name`, not `person`). A
  handle that doesn't resolve in the registry is flagged on the page rather
  than silently dropped.
- `started` — free-text date; not parsed or validated.
- `notes` — one short line of free text.
