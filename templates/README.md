# Templates

Reference builds the workforce shows to prospective clients. One folder per
domain (category), one folder per template inside it:

```text
templates/
  <domain>/                  e.g. school, restaurant
    <template-name>/         e.g. premium-v1
      DESIGN.md               names the standard + domain brief it satisfies
      backend/  frontend/     the actual build
```

A template's `DESIGN.md` must declare compliance with
[`../designs/premium-web-design-standard.md`](../designs/premium-web-design-standard.md)
and the matching domain brief under `../designs/<domain>/`. `design-owner`
will not pass a template through the Design gate without both.

## Starting a client project from a template

Copy the template folder into `projects/<domain>/<client-project-name>/` and
diverge there. Never edit a template in place to fit one client — that is how
templates stop looking like reference work. If the client's needs teach the
workforce something the template should always do, fold that lesson back into
the template and its `DESIGN.md` as a separate change, not as a side effect of
the client build.

## Adding a new domain

1. Write `../designs/<domain>/<domain>-design-brief.md` first —
   `product-design-lead` owns this.
2. Build `<domain>/<template-name>/` against it.
3. `design-owner` runs the Design gate before it is shown to any client.
