# Landing-page section prompt templates

A library of reusable prompts for briefing `ui-designer` / `web-architect` on
one landing-page section at a time. Each template exists so a section gets
built against the [`premium-web-design-standard`](../premium-web-design-standard.md)
instead of drifting toward the generic AI-landing-page defaults that standard's
anti-generic-AI checklist (section 5) rejects.

Inspiration links below were pulled from the 21st.dev component catalog to
show *what the market is currently shipping* for each section shape — they are
reference points for a design conversation, not code to install verbatim.
21st.dev components are third-party, several are paid, and none of them have
been checked against this repo's design standard or license terms. Do not
`npx shadcn add` one of these URLs directly into a client project; use them to
calibrate the brief, then have `ui-designer` build an original composition
that passes the standard's checklist.

## How to use a template

1. Pick the section.
2. Fill in the bracketed fields from the project's DESIGN.md (audience,
   primary action, brand voice, wow-moment budget).
3. Hand the filled prompt to `ui-designer` or `web-architect`, not to 21st.dev
   directly — the standard's five-questions and section-rhythm rules apply
   regardless of which agent implements it.
4. Run the result through the standard's self-critique pass (section 7)
   before it counts as done.

---

## Hero

**Prompt template:**

> Design the hero section for `[project name]`, targeting `[audience]`. In the
> first 5 seconds it must communicate who this is for, what it does, and one
> reason to trust it. The primary action is `[primary CTA]`. Avoid the
> centered-text-on-plain-background pattern the design standard's checklist
> rejects — use one of: a supporting visual/mockup, an asymmetric layout, a
> signature motion moment, or a full-bleed image, matched to the brand's
> `[visual story from DESIGN.md]`. Do not use gradient blobs or glassmorphism
> unless the brand system calls for it.

**Market inspiration (21st.dev):**
- [Underline Hero Section](https://21st.dev/@waleedkibhen/components/underline-hero-section) — decorative type accent as the differentiator instead of imagery
- [Enterprise Hero with Dual CTAs](https://21st.dev/@uniquesonu/components/hero-section-enterprise-ready-landing-page-hero-with-dual-ctas) — theme-aware, dual-CTA structure
- [Marketing Hero with Spotlight](https://21st.dev/@uiable/components/block-hero) — stats pill + mouse-following spotlight as the signature motion moment
- [Agency Hero with Logo Marquee](https://21st.dev/@shadcnspace/components/hero-01) — trust avatars + client-logo marquee for social proof up top

---

## Feature grid

**Prompt template:**

> Design the features section for `[project name]` covering these
> capabilities: `[list 3-6 features]`. Do not default to three-identical-cards
> — vary emphasis (one lead feature larger, or a two-column asymmetric split)
> so it isn't a repeat of the hero's layout shape. Icons/illustrations should
> match the brand's `[icon or illustration style from DESIGN.md]`, not generic
> line icons. Background treatment should differ from the section above and
> below it per the standard's section-rhythm rule.

**Market inspiration (21st.dev):**
- [Feature Section with scroll animation](https://21st.dev/@ravikatiyar162/components/feature-section) — categorized icon grid, framer-motion reveal
- [Icon Feature Grid, two-column](https://21st.dev/@felipemenezes098/components/content-09) — serif heading + two-column instead of a 3-up grid
- [Financial Platform Feature Grid](https://21st.dev/@uiable/components/block-feature-32) — spotlight-border cards, scroll-triggered fade-in

---

## Pricing

**Prompt template:**

> Design the pricing section for `[project name]` with tiers:
> `[list tiers and prices]`. Include a monthly/yearly toggle if pricing
> differs by billing cycle. Highlight the recommended tier without resorting
> to a generic "Most Popular" badge if the brand voice supports something more
> distinctive — `[brand voice note]`. Price transitions on toggle should use
> the standard's micro-motion tier (fast, subtle), not a jarring re-render.

**Market inspiration (21st.dev):**
- [Banner Tiers Pricing Table](https://21st.dev/@arihantcodes_1f7b8c4d/components/banner-tiers) — brutalist styling, banner-highlighted featured plan, animated digit rollers
- [Pricing Table with feature matrix](https://21st.dev/@kokonutd/components/pricing-table) — full comparison matrix, animated price transitions
- [Annual Savings Pricing Grid](https://21st.dev/@7ovr/components/pricing-4) — shows yearly-billed total under the monthly price for transparency

---

## Testimonials

**Prompt template:**

> Design the testimonials section for `[project name]` using these
> quotes/sources: `[list or "TBD — placeholder attributed quotes only, flag
> for real copy"]`. Choose a layout (carousel, staggered grid, single
> spotlight quote) based on quote count and length — don't force a carousel
> if there are only 2-3 quotes. No stock-photo avatars; use `[avatar
> treatment: initials, illustration, or real photos]`.

**Market inspiration (21st.dev):**
- [Testimonials with animated headline + carousel](https://21st.dev/@scrollxui/components/testimonials-with-carousel)
- [Staggered Testimonials Grid](https://21st.dev/@efferd/components/testimonials-3) — quote icons + decorative corner marks, no carousel needed
- [Carousel Testimonials with autoplay](https://21st.dev/@ziegfiroyt/components/testimonial1)

---

## Call to action (closing)

**Prompt template:**

> Design the closing CTA section for `[project name]`. Primary action:
> `[primary CTA]`. This is one of the page's 1-3 signature wow-moment
> candidates per the standard — decide deliberately whether this section earns
> that budget or should stay calm. If secondary conversion (email capture,
> waitlist) matters more than a single button, use an inline form instead of
> a generic button-only CTA.

**Market inspiration (21st.dev):**
- [Gradient CTA Banner](https://21st.dev/@shadcnspace/components/cta-01) — soft gradient + animated primary button
- [CTA with inline email capture](https://21st.dev/@meschacirung/components/call-to-action-3) — waitlist/newsletter pattern
- [CTA with social proof avatars](https://21st.dev/@shadcnstore/components/cta-section-2) — member avatar stack beside the subscribe form

---

## Footer

**Prompt template:**

> Design the footer for `[project name]` with link groups:
> `[list nav groups]`. `[Include / do not include]` a newsletter signup.
> Keep it visually quiet — the footer is not a wow-moment section; it should
> read as the calm landing point after the page's scroll story per the
> standard's blur-test criterion.

**Market inspiration (21st.dev):**
- [Newsletter Signup Footer](https://21st.dev/@7ovr/components/footer-3) — email form + grouped nav columns + social bar
- [Footer with logo, nav, and subscribe](https://21st.dev/@shadcnui-blocks/components/footer-04) — clean baseline structure
- [Animated Wave Footer](https://21st.dev/@arihantcodes_1f7b8c4d/components/animated-wave-footer) — only if the brand's wow-moment budget has room left after the hero

---

## Adding a new section template

When a project needs a section not covered here (nav bar, stats/metrics
strip, FAQ accordion, team grid, etc.), pull 3-5 inspiration results from
21st.dev (`get_inspiration` / `search` tools), write the prompt template
following the pattern above, and append it to this file rather than starting
a new doc — this keeps one canonical library, the same way the design
standard keeps one canonical copy.
