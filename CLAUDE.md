# RU-AIBOTWORKS — repo-wide instructions

## Website design work

Before writing or reviewing any website's markup, styling, or layout, read
[`designs/premium-web-design-standard.md`](designs/premium-web-design-standard.md)
and, if one exists, the matching `designs/<domain>/` brief. Every project and
template's `DESIGN.md` must declare compliance with that standard by name and
version — this applies regardless of which agent persona is doing the work.

Do not paste the standard's text into a prompt, skill, or DESIGN.md — link to
it. One canonical copy keeps every future read cheap and every agent on the
current version.

## Folder structure

```text
templates/<domain>/<template-name>/   reference builds shown to clients
designs/<domain>/                       the design brief for that domain
projects/<domain>/<client-project>/    real client work, copied from a template
ru-aibotworks/                         the generated agent company — see its own README
```

## Project status tracking

Any `projects/<domain>/<client-project>/` folder may carry a `STATUS.yaml`
declaring its status and which registry agents are assigned to it. The
RU-AIBOTWORKS portal's Projects page reads every one of these to show what is
running across all client projects at once. See
[`projects/README.md`](projects/README.md) for the schema.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
