# RU-AIBOTWORKS — repo-wide instructions

## Website design work

Before writing or reviewing any website's markup, styling, or layout, read
[`Design/premium-web-design-standard.md`](Design/premium-web-design-standard.md)
and, if one exists, the matching `Design/<domain>/` brief. Every project and
template's `DESIGN.md` must declare compliance with that standard by name and
version — this applies regardless of which agent persona is doing the work.

Do not paste the standard's text into a prompt, skill, or DESIGN.md — link to
it. One canonical copy keeps every future read cheap and every agent on the
current version.

## Folder structure

```text
Templates/<domain>/<template-name>/   reference builds shown to clients
Design/<domain>/                       the design brief for that domain
projects/<domain>/<client-project>/    real client work, copied from a template
RU-AIBOTWORKS/                         the generated agent company — see its own README
```

## Project status tracking

Any `projects/<domain>/<client-project>/` folder may carry a `STATUS.yaml`
declaring its status and which registry agents are assigned to it. The
RU-AIBOTWORKS portal's Projects page reads every one of these to show what is
running across all client projects at once. See
[`projects/README.md`](projects/README.md) for the schema.
