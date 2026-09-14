#!/usr/bin/env python3
"""
ru_aibotworks_portal.py — generate the CEO portal from the registry.

Six pages, one stylesheet, one data file. Every figure on every page is computed
from RU-AIBOTWORKS-REGISTRY, so no page can disagree with another (invariant 11).

    RU-AIBOTWORKS-index.html         the company at a glance
    RU-AIBOTWORKS-org-chart.html     reporting structure, CEO to engineer
    RU-AIBOTWORKS-workforce.html     every agent, by division, department and team
    RU-AIBOTWORKS-workflow.html      how a build reaches production
    RU-AIBOTWORKS-architecture.html  planes, lanes, and the gate
    RU-AIBOTWORKS-governance.html    the harness: invariants and standard controls

    python ru_aibotworks_portal.py
"""
from __future__ import annotations

import json
import sys
from datetime import date
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ru_aibotworks_generate import BUDGETS, blast_radius_for, grants_for  # noqa: E402
from ru_aibotworks_registry import Company  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "RU-AIBOTWORKS-PORTAL"
TODAY = date.today()

PAGES = [
    ("RU-AIBOTWORKS-index.html", "Overview"),
    ("RU-AIBOTWORKS-org-chart.html", "Reporting"),
    ("RU-AIBOTWORKS-workforce.html", "Workforce"),
    ("RU-AIBOTWORKS-workflow.html", "Workflow"),
    ("RU-AIBOTWORKS-architecture.html", "Architecture"),
    ("RU-AIBOTWORKS-governance.html", "Governance"),
]

STYLE = """
/* RU-AIBOTWORKS portal — blueprint. Dark-first, light supported, theme-aware. */
:root {
  --bg:#F4F6F9; --panel:#FFFFFF; --panel-2:#FAFBFC; --line:#DFE4EB; --line-2:#EDF0F4;
  --ink:#141C27; --ink-2:#3C4959; --muted:#6B7B8F;
  --accent:#0E7C86; --accent-soft:rgba(14,124,134,.10);
  --veto:#C2384A;  --veto-soft:rgba(194,56,74,.10);
  --lead:#9A6B00;  --lead-soft:rgba(154,107,0,.10);
  --corp:#6D4AC4;  --corp-soft:rgba(109,74,196,.10);
  --indep:#1B7A4D; --indep-soft:rgba(27,122,77,.10);
  --grid:rgba(20,28,39,.045);
  --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --r:10px;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:#080C12; --panel:#0E141D; --panel-2:#121A24; --line:#1D2938; --line-2:#161F2B;
    --ink:#E8F0F8; --ink-2:#B6C6D8; --muted:#7B8FA6;
    --accent:#4DD6E8; --accent-soft:rgba(77,214,232,.12);
    --veto:#FF7A85;  --veto-soft:rgba(255,122,133,.12);
    --lead:#FFC857;  --lead-soft:rgba(255,200,87,.12);
    --corp:#A78BFA;  --corp-soft:rgba(167,139,250,.12);
    --indep:#43D9A0; --indep-soft:rgba(67,217,160,.12);
    --grid:rgba(232,240,248,.04);
  }
}
:root[data-theme="dark"] {
  --bg:#080C12; --panel:#0E141D; --panel-2:#121A24; --line:#1D2938; --line-2:#161F2B;
  --ink:#E8F0F8; --ink-2:#B6C6D8; --muted:#7B8FA6;
  --accent:#4DD6E8; --accent-soft:rgba(77,214,232,.12);
  --veto:#FF7A85;  --veto-soft:rgba(255,122,133,.12);
  --lead:#FFC857;  --lead-soft:rgba(255,200,87,.12);
  --corp:#A78BFA;  --corp-soft:rgba(167,139,250,.12);
  --indep:#43D9A0; --indep-soft:rgba(67,217,160,.12);
  --grid:rgba(232,240,248,.04);
}

*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.6 var(--sans); -webkit-font-smoothing:antialiased;
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),
                   linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:32px 32px;
}
a{color:var(--accent); text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1220px; margin:0 auto; padding-inline:20px; padding-block:0 72px}

/* ── masthead ───────────────────────────────────────────────── */
header.mast{
  border-bottom:1px solid var(--line); background:var(--panel);
  position:sticky; top:0; z-index:20; backdrop-filter:saturate(140%) blur(6px);
}
.mast-in{max-width:1220px;margin:0 auto;padding:14px 20px;display:flex;
  align-items:center;gap:18px;flex-wrap:wrap}
.brand{font-family:var(--mono);font-weight:700;letter-spacing:.06em;font-size:15px;
  color:var(--ink);white-space:nowrap}
.brand span{color:var(--accent)}
nav.tabs{display:flex;gap:2px;flex-wrap:wrap;margin-left:auto}
nav.tabs a{
  font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--muted);
  padding:7px 11px;border-radius:7px;border:1px solid transparent;white-space:nowrap;
}
nav.tabs a:hover{color:var(--ink);background:var(--panel-2);text-decoration:none}
nav.tabs a[aria-current="page"]{color:var(--accent);background:var(--accent-soft);
  border-color:var(--accent)}
.theme-btn{font-family:var(--mono);font-size:12px;color:var(--muted);background:none;
  border:1px solid var(--line);border-radius:7px;padding:7px 10px;cursor:pointer}
.theme-btn:hover{color:var(--ink);border-color:var(--accent)}

/* ── page head ──────────────────────────────────────────────── */
.phead{padding:46px 0 26px;border-bottom:1px solid var(--line-2);margin-bottom:30px}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.18em;
  text-transform:uppercase;color:var(--accent);margin:0 0 12px}
h1{font-size:clamp(26px,4.4vw,40px);line-height:1.14;margin:0 0 12px;letter-spacing:-.02em}
.lede{font-size:17px;color:var(--ink-2);max-width:74ch;margin:0}

h2{font-size:21px;margin:46px 0 8px;letter-spacing:-.01em;scroll-margin-top:80px}
h3{font-size:15px;margin:26px 0 8px;font-family:var(--mono);letter-spacing:.02em}
.sub{color:var(--muted);font-size:14px;margin:0 0 18px;max-width:78ch}
p{max-width:78ch;color:var(--ink-2)}

/* ── stat grid ──────────────────────────────────────────────── */
.stats{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));
  margin:26px 0}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);
  padding:16px 16px 14px;position:relative;overflow:hidden}
.stat::before{content:"";position:absolute;inset:0 auto 0 0;width:3px;background:var(--accent)}
.stat.v::before{background:var(--veto)} .stat.c::before{background:var(--corp)}
.stat.i::before{background:var(--indep)} .stat.l::before{background:var(--lead)}
.stat .n{font-family:var(--mono);font-size:30px;font-weight:700;line-height:1;
  letter-spacing:-.03em;color:var(--ink)}
.stat .k{font-size:11.5px;color:var(--muted);margin-top:7px;letter-spacing:.03em;
  text-transform:uppercase;font-family:var(--mono)}
.stat .d{font-size:12px;color:var(--ink-2);margin-top:7px;line-height:1.45}

/* ── cards & panels ─────────────────────────────────────────── */
.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);
  padding:20px;margin:18px 0}
.grid2{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(310px,1fr))}
.grid3{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}

/* ── tables ─────────────────────────────────────────────────── */
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);
  background:var(--panel);margin:16px 0}
table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:520px}
th{font-family:var(--mono);font-size:11px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--muted);text-align:left;padding:11px 14px;border-bottom:1px solid var(--line);
  background:var(--panel-2);position:sticky;top:0}
td{padding:10px 14px;border-bottom:1px solid var(--line-2);color:var(--ink-2);
  vertical-align:top}
tr:last-child td{border-bottom:none}
tbody tr:hover td{background:var(--panel-2)}
td.name{font-family:var(--mono);font-size:12.5px;color:var(--ink);white-space:nowrap}

/* ── chips ──────────────────────────────────────────────────── */
.chip{display:inline-flex;align-items:center;gap:5px;font-family:var(--mono);
  font-size:10.5px;letter-spacing:.05em;padding:2px 7px;border-radius:5px;
  border:1px solid var(--line);color:var(--muted);white-space:nowrap;text-transform:uppercase}
.chip.veto{color:var(--veto);border-color:var(--veto);background:var(--veto-soft)}
.chip.ro{color:var(--accent);border-color:var(--accent);background:var(--accent-soft)}
.chip.lead{color:var(--lead);border-color:var(--lead);background:var(--lead-soft)}
.chip.l4{color:var(--corp);border-color:var(--corp);background:var(--corp-soft)}
.chip.new{color:var(--indep);border-color:var(--indep);background:var(--indep-soft)}
.chip.t0{opacity:.7} .chip.t2{color:var(--lead);border-color:var(--lead)}

/* ── org chart ──────────────────────────────────────────────── */
.chart{overflow-x:auto;background:var(--panel);border:1px solid var(--line);
  border-radius:var(--r);padding:22px;margin:18px 0}
.chart svg{display:block;min-width:620px;max-width:760px;width:100%;height:auto}
.node-box{fill:var(--panel-2);stroke:var(--line)}
.node-box.acc{stroke:var(--accent)} .node-box.veto{stroke:var(--veto)}
.node-box.corp{stroke:var(--corp)} .node-box.indep{stroke:var(--indep)}
.node-t{font-family:var(--mono);font-size:12px;fill:var(--ink)}
.node-s{font-family:var(--mono);font-size:9.5px;fill:var(--muted)}
.edge{stroke:var(--line);stroke-width:1.4;fill:none}
.edge.dash{stroke-dasharray:4 4;stroke:var(--muted);opacity:.6}

/* ── workforce explorer ─────────────────────────────────────── */
.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:20px 0 8px;
  position:sticky;top:60px;z-index:10;background:var(--bg);padding:10px 0}
.toolbar input[type=search]{
  flex:1 1 260px;min-width:0;font:13px var(--mono);padding:10px 13px;border-radius:8px;
  border:1px solid var(--line);background:var(--panel);color:var(--ink)}
.toolbar input:focus{outline:2px solid var(--accent);outline-offset:-1px;border-color:var(--accent)}
.filters{display:flex;gap:4px;flex-wrap:wrap}
.fbtn{font:11px var(--mono);letter-spacing:.05em;padding:7px 10px;border-radius:7px;
  border:1px solid var(--line);background:var(--panel);color:var(--muted);cursor:pointer;
  text-transform:uppercase}
.fbtn:hover{color:var(--ink);border-color:var(--accent)}
.fbtn[aria-pressed="true"]{color:var(--accent);border-color:var(--accent);
  background:var(--accent-soft)}
.count{font:12px var(--mono);color:var(--muted);margin-left:auto;white-space:nowrap}

details.dept{border:1px solid var(--line);border-radius:var(--r);background:var(--panel);
  margin:12px 0;overflow:hidden}
details.dept > summary{
  padding:14px 18px;cursor:pointer;list-style:none;display:flex;gap:12px;
  align-items:baseline;flex-wrap:wrap;background:var(--panel-2)}
details.dept > summary::-webkit-details-marker{display:none}
details.dept > summary::before{content:"▸";font-family:var(--mono);color:var(--accent);
  transition:transform .15s}
details.dept[open] > summary::before{transform:rotate(90deg)}
.dept-name{font-family:var(--mono);font-size:14px;color:var(--ink);font-weight:600}
.dept-officer{font-family:var(--mono);font-size:11.5px;color:var(--accent)}
.dept-mission{font-size:12.5px;color:var(--muted);flex:1 1 100%;margin-top:2px}
.dept-n{font-family:var(--mono);font-size:11px;color:var(--muted);margin-left:auto}
.team{border-top:1px solid var(--line-2);padding:14px 18px}
.team-h{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;margin-bottom:4px}
.team-name{font-family:var(--mono);font-size:12.5px;color:var(--ink)}
.team-mission{font-size:12px;color:var(--muted);margin:0 0 10px;max-width:80ch}
.people{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(272px,1fr))}
.person{border:1px solid var(--line-2);border-radius:8px;padding:10px 12px;
  background:var(--panel-2)}
.person.is-lead{border-color:var(--lead)}
.person .pn{font-family:var(--mono);font-size:12px;color:var(--ink);
  display:flex;gap:6px;align-items:baseline;flex-wrap:wrap}
.person .pp{font-size:13.5px;font-weight:700;letter-spacing:.01em}
.person .ph{color:var(--muted);font-size:11px}
.person .pr{font-size:12px;color:var(--muted);margin-top:5px;line-height:1.45}
.person .pm{font-family:var(--mono);font-size:10px;color:var(--muted);margin-top:7px;
  display:flex;gap:6px;flex-wrap:wrap}
.hidden{display:none !important}

/* ── misc ───────────────────────────────────────────────────── */
.note{border-left:3px solid var(--accent);background:var(--accent-soft);
  padding:13px 16px;border-radius:0 8px 8px 0;margin:18px 0;font-size:14px;
  color:var(--ink-2);max-width:80ch}
.note.warn{border-color:var(--veto);background:var(--veto-soft)}
.note strong{color:var(--ink)}
code{font-family:var(--mono);font-size:.9em;background:var(--panel-2);
  border:1px solid var(--line-2);border-radius:4px;padding:1px 5px;color:var(--ink)}
ul.tight{padding-left:20px;max-width:80ch;color:var(--ink-2)}
ul.tight li{margin:5px 0}
footer.foot{border-top:1px solid var(--line);margin-top:56px;padding:24px 0;
  font-family:var(--mono);font-size:11.5px;color:var(--muted);
  display:flex;gap:14px;flex-wrap:wrap;justify-content:space-between}
.flow{display:grid;gap:10px}
.step{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start;
  border:1px solid var(--line);border-radius:var(--r);background:var(--panel);padding:14px 16px}
.step .i{font-family:var(--mono);font-size:11px;color:var(--accent);border:1px solid var(--accent);
  border-radius:6px;padding:4px 8px;background:var(--accent-soft);white-space:nowrap}
.step .t{font-family:var(--mono);font-size:13px;color:var(--ink);margin-bottom:3px}
.step .b{font-size:13px;color:var(--ink-2);margin:0}
.step.ceo{border-color:var(--lead)} .step.ceo .i{color:var(--lead);border-color:var(--lead);
  background:var(--lead-soft)}
.step.stop{border-color:var(--veto)} .step.stop .i{color:var(--veto);border-color:var(--veto);
  background:var(--veto-soft)}
@media (max-width:560px){
  .step{grid-template-columns:1fr}
  .toolbar{position:static}
  th{position:static}
}
"""

THEME_JS = """
(function(){
  try{
    var t=localStorage.getItem('ruai-theme');
    if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t);
  }catch(e){}
  window.ruaiToggle=function(){
    var r=document.documentElement,
        cur=r.getAttribute('data-theme'),
        sysDark=window.matchMedia('(prefers-color-scheme: dark)').matches,
        now=cur?cur:(sysDark?'dark':'light'),
        next=now==='dark'?'light':'dark';
    r.setAttribute('data-theme',next);
    try{localStorage.setItem('ruai-theme',next);}catch(e){}
  };
})();
"""


def e(x) -> str:
    return escape(str(x), quote=True)


def person_of(c: Company, handle: str) -> str:
    """A reporting target is an officer or an agent; both carry a person name."""
    if handle in c.officer_by_name:
        return c.officer_by_name[handle].person
    agent = c.agent_by_name.get(handle)
    return agent.person if agent else handle


def shell(title: str, current: str, body: str, figures: dict, extra_js: str = "") -> str:
    tabs = "\n".join(
        f'      <a href="{f}"{" aria-current=\"page\"" if label == current else ""}>{label}</a>'
        for f, label in PAGES
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · RU-AIBOTWORKS</title>
<script>{THEME_JS}</script>
<link rel="stylesheet" href="RU-AIBOTWORKS-portal.css">
</head>
<body>
<header class="mast">
  <div class="mast-in">
    <div class="brand">RU<span>-</span>AIBOTWORKS</div>
    <nav class="tabs">
{tabs}
      <button class="theme-btn" onclick="ruaiToggle()" aria-label="Toggle theme">◐ theme</button>
    </nav>
  </div>
</header>
<main class="wrap">
{body}
<footer class="foot">
  <span>Generated {TODAY.isoformat()} from RU-AIBOTWORKS-REGISTRY · every figure computed, none asserted</span>
  <span>{figures['agents_total']} agents · {figures['officers']} officers · {figures['vetoes']} vetoes</span>
</footer>
</main>
{extra_js}
</body>
</html>
"""


def phead(eyebrow: str, h1: str, lede: str) -> str:
    return f'<div class="phead"><p class="eyebrow">{e(eyebrow)}</p><h1>{e(h1)}</h1>' \
           f'<p class="lede">{lede}</p></div>'


def stat(n, k, d="", cls="") -> str:
    dd = f'<div class="d">{d}</div>' if d else ""
    return f'<div class="stat {cls}"><div class="n">{n}</div><div class="k">{e(k)}</div>{dd}</div>'


# ═══════════════════════════ page: overview ═══════════════════════════

def page_index(c: Company) -> str:
    f = c.figures
    body = phead(
        "CEO reference",
        "The company, as it actually is",
        "Nothing on this page is typed by hand. Every number is counted from the registry "
        "when this page is generated, so no two pages can disagree about what the company is.",
    )
    body += f"""
<div class="stats">
  {stat(f['agents_total'], 'agents total', 'Officers plus the whole workforce.')}
  {stat(f['officers'], 'officers', f"{f['officers_original']} original + <strong>{f['officers_added']} added</strong>.", 'c')}
  {stat(f['vetoes'], 'standing vetoes', 'Only the CEO overrides. Unchanged by the expansion.', 'v')}
  {stat(f['reserved_decisions'], 'decisions are yours', 'What to build · the design · veto override · off-stack.', 'l')}
</div>

<h2>What changed</h2>
<p class="sub">Six officers were added and two new lanes of work opened. The three things
that make the quality claim true &mdash; three vetoes, four reserved decisions, and a
read-only reviewer &mdash; are untouched.</p>

<div class="tw"><table>
<thead><tr><th>Figure</th><th>Before</th><th>After</th><th>Note</th></tr></thead>
<tbody>
<tr><td class="name">officers</td><td>13</td><td><strong>{f['officers']}</strong></td>
    <td>+{f['officers_added']}: coo, hr-director, payroll-controller, finance-controller,
        service-management-lead, data-protection-officer</td></tr>
<tr><td class="name">L4 chiefs</td><td>1</td><td><strong>{f['chiefs_l4']}</strong></td>
    <td>cto keeps delivery; coo takes the corporate line</td></tr>
<tr><td class="name">L3 officers</td><td>7</td><td><strong>{f['officers_l3']}</strong></td>
    <td>4 corporate + the independent DPO</td></tr>
<tr><td class="name">L2 named authorities</td><td>5</td><td><strong>{f['officers_l2']}</strong></td>
    <td>unchanged</td></tr>
<tr><td class="name">standing vetoes</td><td>3</td><td><strong>{f['vetoes']}</strong></td>
    <td>the DPO advises; quality-compliance blocks</td></tr>
<tr><td class="name">CEO direct reports</td><td>1</td><td><strong>{f['ceo_direct_reports']}</strong></td>
    <td>cto, coo, data-protection-officer</td></tr>
<tr><td class="name">delivery engineers</td><td>202 planned</td><td><strong>{f['engineers_delivery_baseline']} built</strong></td>
    <td>the charter baseline, now individually designed</td></tr>
<tr><td class="name">mobile engineers</td><td>0</td><td><strong>{f['engineers_mobile_expansion']}</strong></td>
    <td>Lane C: Kotlin/Compose, Flutter, React Native</td></tr>
<tr><td class="name">corporate staff</td><td>0</td><td><strong>{f['staff_corporate']}</strong></td>
    <td>HR, Payroll, Finance, Service Management, Data Protection</td></tr>
<tr><td class="name">delivery lanes</td><td>2</td><td><strong>{f['lanes']}</strong></td>
    <td>A, B, plus C1/C2/C3 for mobile</td></tr>
</tbody></table></div>

<h2>Structure</h2>
<div class="stats">
  {stat(f['divisions'], 'divisions', 'Delivery · Corporate · Independent.')}
  {stat(f['departments'], 'departments', 'Each owned by exactly one officer.')}
  {stat(f['teams'], 'teams', f"{f['team_leads_promoted_l2']} led at L2, {f['team_leads_coordinating_l1']} coordinated at L1.", 'l')}
  {stat(f['named'], 'named employees', 'Every agent has a person name and a dispatch handle.')}
</div>

<h2>Safety posture</h2>
<p class="sub">Measured against STD-AGENT-001. These are the numbers an auditor asks for
first, and they are read from the registry rather than from intent.</p>
<div class="stats">
  {stat(f['tools_registered'], 'tools registered', 'Complete contracts. Unregistered means unreachable.')}
  {stat(f['tools_registered_denied'], 'registered &amp; denied', 'Tier 3 and 4 tools, visible and granted to nobody.', 'v')}
  {stat(f['max_tier_granted'], 'highest tier granted', 'Tier 2 &mdash; reversible with a recorded rollback.', 'i')}
  {stat(f['read_only_officers'], 'read-only officers', 'No veto holder can write what it blocks.', 'v')}
</div>

<div class="note"><strong>The rule the whole structure rests on.</strong>
Three officers can stop a release &mdash; <code>security-engineer</code>,
<code>sre</code>, <code>quality-compliance</code>. Only you can unstop it. The
<code>cto</code> cannot, and neither can the new <code>coo</code>: an autonomous chief
under delivery pressure must not reach its own stop buttons.</div>

<h2>Model mix and cost tiers</h2>
<div class="tw"><table>
<thead><tr><th>Model</th><th>Agents</th><th>Input $/MTok</th><th>Output $/MTok</th><th>Used for</th></tr></thead>
<tbody>
{"".join(
    f'<tr><td class="name">{e(m)}</td><td>{f["model_mix"].get(m, 0)}</td>'
    f'<td>{v["input"] if v["input"] is not None else "&mdash;"}</td>'
    f'<td>{v["output"] if v["output"] is not None else "&mdash;"}</td>'
    f'<td>{e(v["note"])}</td></tr>'
    for m, v in c.identity["models"].items()
)}
</tbody></table></div>
<p class="sub">No agent runs on the premium tier today. <code>fable</code> costs roughly
2.6&times; Opus and is opt-in only &mdash; never for a security agent, which the genome
enforces.</p>
"""
    return shell("Overview", "Overview", body, f)


# ═══════════════════════════ page: org chart ═══════════════════════════

def svg_org(c: Company) -> str:
    """
    Indented tree. Chosen over a fan-out tree because 19 nodes with real names do not
    fit across a page, and squeezing them produces clipped labels and edges that imply
    the wrong parent. Indentation shows depth without lying about width.
    """
    BW, BH, PITCH, INDENT, PAD = 258, 40, 52, 46, 16

    # (name, sublabel, css class) in display order; depth drives the indent.
    order: list[tuple[str, int]] = [
        ("CEO", 0), ("cto", 1),
        ("product-owner", 2), ("design-owner", 2), ("web-architect", 2),
        ("data-architect", 2), ("platform-architect", 2),
        ("security-engineer", 3), ("sre", 3), ("release-manager", 3),
        ("dependency-steward", 3),
        ("testing-architect", 2), ("merge-authority", 3),
        ("quality-compliance", 2),
        ("coo", 1),
        ("hr-director", 2), ("payroll-controller", 2), ("finance-controller", 2),
        ("service-management-lead", 2),
        ("data-protection-officer", 1),
    ]

    def meta(name: str) -> tuple[str, str]:
        if name == "CEO":
            return "L5 · human · 4 reserved decisions", "acc"
        o = c.officer_by_name[name]
        head = sum(
            len(c.agents_in(d["id"])) for d in c.departments if d["officer"] == name
        )
        bits = [name, o.level, o.function]
        if o.power:
            bits.append(o.power)
        if head:
            bits.append(f"{head} staff")
        if o.added != "original":
            bits.append("NEW")
        cls = ("veto" if o.power == "VETO"
               else "indep" if o.division == "Independent"
               else "corp" if o.division == "Corporate"
               else "acc" if o.power == "READ-ONLY" or o.level == "L4"
               else "")
        return " · ".join(bits), cls

    rows = []
    for i, (name, depth) in enumerate(order):
        x = PAD + depth * INDENT
        y = PAD + i * PITCH
        rows.append((name, depth, x, y))

    pos = {name: (x, y) for name, _, x, y in rows}
    parts = []

    # Edges first so boxes paint over them.
    for i, (name, depth, x, y) in enumerate(rows):
        if depth == 0:
            continue
        # nearest preceding row at depth-1 is the parent
        parent = next(r for r in reversed(rows[:i]) if r[1] == depth - 1)
        px, py = parent[2], parent[3]
        spine = px + 14
        parts.append(
            f'<path class="edge" d="M{spine} {py + BH} V{y + BH / 2} H{x}"/>'
        )

    for name, depth, x, y in rows:
        sub, cls = meta(name)
        # The person's name reads as the label; the full handle stays in the
        # sub-line, because the handle is what appears in every receipt.
        label = "CEO · Uzwal Gutta" if name == "CEO" else c.officer_by_name[name].person
        parts.append(
            f'<g><rect class="node-box {cls}" x="{x}" y="{y}" width="{BW}" height="{BH}" rx="7"/>'
            f'<text class="node-t" x="{x + 12}" y="{y + 18}">{e(label)}</text>'
            f'<text class="node-s" x="{x + 12}" y="{y + 32}">{e(sub)}</text></g>'
        )

    # The workforce, hanging off the bottom of the chart.
    wy = PAD + len(rows) * PITCH + 8
    parts.append(
        f'<rect class="node-box" x="{PAD}" y="{wy}" width="{BW + 120}" height="{BH}" rx="7"/>'
        f'<text class="node-t" x="{PAD + 12}" y="{wy + 18}">'
        f'{c.figures["workforce_total"]} agents below the officer layer</text>'
        f'<text class="node-s" x="{PAD + 12}" y="{wy + 32}">'
        f'{c.figures["departments"]} departments · {c.figures["teams"]} teams · '
        f'{c.figures["team_leads"]} leads</text>'
    )
    parts.append(f'<path class="edge dash" d="M{PAD + 14} {PAD + (len(rows) - 1) * PITCH + BH} V{wy}"/>')

    width = PAD * 2 + 3 * INDENT + BW + 120
    height = wy + BH + PAD
    return (
        f'<svg viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="RU-AIBOTWORKS reporting structure, CEO to officer">'
        + "".join(parts) + "</svg>"
    )


def page_org(c: Company) -> str:
    f = c.figures
    body = phead(
        "Reporting structure",
        "Who reports to whom, and who can stop a release",
        "Three lines leave the CEO. One builds, one runs the company, and one assesses "
        "data protection independently of both.",
    )
    body += f'<div class="chart">{svg_org(c)}</div>'

    body += """
<div class="note"><strong>Why <code>merge-authority</code> reports to
<code>testing-architect</code>.</strong> It reviews the architects' work, so it must not
report to them. That single edge is why verification cannot be overruled by the team it
verifies &mdash; and it is why the reviewer holds no <code>Write</code> tool at all.</div>

<div class="note"><strong>Why the Data Protection Officer reports to you directly.</strong>
GDPR Art. 38(3) requires the DPO to reach the highest management level and to take no
instruction on how to perform the role. Routing it through <code>coo</code> or
<code>cto</code> would make the independence nominal. It raises findings;
<code>quality-compliance</code> blocks on them; only you unblock.</div>

<h2>The 19 officers</h2>
<p class="sub">Six of these are new. The column on the right says which.</p>
"""
    rows = []
    for o in c.officers:
        chips = []
        if o.power == "VETO":
            chips.append('<span class="chip veto">veto</span>')
        if o.power == "READ-ONLY":
            chips.append('<span class="chip ro">read-only</span>')
        if o.level == "L4":
            chips.append('<span class="chip l4">chief</span>')
        if o.added != "original":
            chips.append('<span class="chip new">new</span>')
        owned = [d for d in c.departments if d["officer"] == o.name]
        head = sum(len(c.agents_in(d["id"])) for d in owned)
        rows.append(
            f'<tr><td class="name"><strong>{e(o.person)}</strong></td>'
            f'<td class="name">{e(o.name)} {"".join(chips)}</td>'
            f'<td>{e(o.level)}</td><td class="name">{e(o.reports_to)}</td>'
            f'<td>{e(o.function)}</td><td>{e(o.decides)}</td>'
            f'<td>{head}</td><td>{e(o.model)}</td>'
            f'<td>{"ADR-002" if o.added != "original" else "original"}</td></tr>'
        )
    body += (
        '<div class="tw"><table><thead><tr><th>Officer</th><th>Level</th><th>Reports to</th>'
        '<th>Function</th><th>Decides</th><th>Staff</th><th>Model</th><th>Added</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )

    body += f"""
<h2>The authority ladder</h2>
<div class="tw"><table>
<thead><tr><th>Level</th><th>Held by</th><th>May decide</th><th>May not</th></tr></thead>
<tbody>
<tr><td class="name">L5</td><td>CEO &mdash; human, 1</td><td>Commercial direction, veto override</td><td>Ship code</td></tr>
<tr><td class="name">L4</td><td><code>cto</code>, <code>coo</code> &mdash; 2</td><td>Triage, dispatch, corporate direction</td><td>Override a veto</td></tr>
<tr><td class="name">L3</td><td>{f['officers_l3']} officers</td><td>Anything binding their function</td><td>Cross into another function</td></tr>
<tr><td class="name">L2</td><td>{f['officers_l2']} named authorities + {f['team_leads_promoted_l2']} team leads</td><td>One named call, or one team's sequencing</td><td>Anything outside that call</td></tr>
<tr><td class="name">L1</td><td>every engineer</td><td>Implementation approach inside an assigned task</td><td>Decide scope, merge, or ship</td></tr>
</tbody></table></div>

<div class="note"><strong>Team leads are promoted deliberately, and logged.</strong>
{f['team_leads_promoted_l2']} of the {f['teams']} team leads hold L2, each with a written
reason, a date, and the requesting officer's name in the promotion register. The other
{f['team_leads_coordinating_l1']} stay at L1 because their department's officer is itself
L2 &mdash; there is no room above them, and an L2 reporting to an L2 inverts authority.
Those departments are flat: everyone reports to the officer, and the lead coordinates
without a reporting line beneath it.</div>
"""
    return shell("Reporting", "Reporting", body, f)


# ═══════════════════════════ page: workforce ═══════════════════════════

def page_workforce(c: Company) -> str:
    f = c.figures
    body = phead(
        "Workforce",
        "The workforce, by team",
        f"The {f['workforce_total']} agents below the officer layer, across "
        f"{f['departments']} departments and {f['teams']} teams. Search by name, role, "
        "skill, department or capability. "
        f'The {f["officers"]} officers are on '
        '<a href="RU-AIBOTWORKS-org-chart.html">Reporting</a>.',
    )
    body += f"""
<div class="stats">
  {stat(f['engineers_delivery_baseline'], 'delivery', 'The charter baseline of 202, individually designed.')}
  {stat(f['engineers_mobile_expansion'], 'mobile', 'Lane C. Three stacks.', 'i')}
  {stat(f['staff_corporate'], 'corporate', 'HR, Payroll, Finance, Service Mgmt, Data Protection.', 'c')}
  {stat(f['team_leads'], 'team leads', 'One per team, every one of them logged.', 'l')}
</div>

<div class="toolbar">
  <input type="search" id="q" placeholder="Search {f['workforce_total']} agents — name, handle, role, skill…"
         aria-label="Search agents">
  <div class="filters" id="filters">
    <button class="fbtn" data-f="all" aria-pressed="true">all</button>
    <button class="fbtn" data-f="Delivery" aria-pressed="false">delivery</button>
    <button class="fbtn" data-f="Corporate" aria-pressed="false">corporate</button>
    <button class="fbtn" data-f="Independent" aria-pressed="false">independent</button>
    <button class="fbtn" data-f="lead" aria-pressed="false">leads</button>
    <button class="fbtn" data-f="readonly" aria-pressed="false">read-only</button>
  </div>
  <span class="count" id="count"></span>
</div>
"""
    for dept in c.departments:
        officer = c.officer_by_name[dept["officer"]]
        members = c.agents_in(dept["id"])
        teams_html = []
        for team in dept["teams"]:
            tm = c.agents_in(dept["id"], team["id"])
            people = []
            for a in tm:
                chips = []
                if a.lead:
                    chips.append(f'<span class="chip lead">lead · {e(a.level)}</span>')
                if a.read_only:
                    chips.append('<span class="chip ro">read-only</span>')
                haystack = " ".join(
                    [a.person, a.name, a.role, a.plugin, dept["id"], dept["name"], team["name"]]
                    + [s["id"] for s in a.skills] + [s["about"] for s in a.skills]
                ).lower()
                flags = f'{dept["division"]}'
                if a.lead:
                    flags += " lead"
                if a.read_only:
                    flags += " readonly"
                people.append(
                    f'<div class="person{" is-lead" if a.lead else ""}" '
                    f'data-h="{e(haystack)}" data-f="{e(flags)}">'
                    f'<div class="pn"><strong class="pp">{e(a.person)}</strong>'
                    f'<span class="ph">{e(a.name)}</span>{"".join(chips)}</div>'
                    f'<div class="pr">{e(a.role)}</div>'
                    f'<div class="pm"><span class="chip">{e(a.model)}</span>'
                    f'<span class="chip t{a.tier}">tier {a.tier}</span>'
                    f'<span class="chip">{len(a.skills)} skill{"s" if len(a.skills) != 1 else ""}</span>'
                    f'<span class="chip">&rarr; {e(person_of(c, c.reports_to_of(a)))}</span>'
                    f'</div></div>'
                )
            teams_html.append(
                f'<div class="team" data-team="1">'
                f'<div class="team-h"><span class="team-name">{e(team["name"])}</span>'
                f'<span class="chip lead">lead: {e(c.agent_by_name[team["lead"]].person)}</span>'
                f'<span class="dept-n">{len(tm)}</span></div>'
                f'<p class="team-mission">{e(team["mission"])}</p>'
                f'<div class="people">{"".join(people)}</div></div>'
            )
        badge = {"Corporate": "chip l4", "Independent": "chip new"}.get(dept["division"], "chip")
        body += (
            f'<details class="dept" data-div="{e(dept["division"])}" open>'
            f'<summary><span class="dept-name">{e(dept["name"])}</span>'
            f'<span class="dept-officer">{e(officer.name)}</span>'
            f'<span class="{badge}">{e(dept["division"])}</span>'
            f'<span class="dept-n">{len(members)} staff · {len(dept["teams"])} teams</span>'
            f'<span class="dept-mission">{e(dept["mission"])}</span></summary>'
            f'{"".join(teams_html)}</details>'
        )

    js = """
<script>
(function(){
  var q=document.getElementById('q'), count=document.getElementById('count'),
      people=[].slice.call(document.querySelectorAll('.person')),
      teams=[].slice.call(document.querySelectorAll('.team')),
      depts=[].slice.call(document.querySelectorAll('details.dept')),
      btns=[].slice.call(document.querySelectorAll('.fbtn')),
      filter='all';

  function apply(){
    var term=q.value.trim().toLowerCase(), shown=0;
    people.forEach(function(p){
      var okTerm = !term || p.dataset.h.indexOf(term)>-1;
      var okF = filter==='all' || p.dataset.f.indexOf(filter)>-1;
      var vis = okTerm && okF;
      p.classList.toggle('hidden', !vis);
      if(vis) shown++;
    });
    teams.forEach(function(t){
      t.classList.toggle('hidden', !t.querySelector('.person:not(.hidden)'));
    });
    depts.forEach(function(d){
      var any=d.querySelector('.person:not(.hidden)');
      d.classList.toggle('hidden', !any);
      if(any && (term||filter!=='all')) d.open=true;
    });
    count.textContent = shown + ' of ' + people.length + ' agents';
  }
  q.addEventListener('input', apply);
  btns.forEach(function(b){
    b.addEventListener('click', function(){
      filter=b.dataset.f;
      btns.forEach(function(x){x.setAttribute('aria-pressed', String(x===b));});
      apply();
    });
  });
  apply();
})();
</script>
"""
    return shell("Workforce", "Workforce", body, f, js)


# ═══════════════════════════ page: workflow ═══════════════════════════

def page_workflow(c: Company) -> str:
    f = c.figures
    steps = [
        ("/build", "CEO or officer opens the work", "The only entry point. Never an orchestrator — capability does not confer authority.", ""),
        ("triage", "cto sizes it XS / S / M / L", "L4, and belongs to cto alone. Under-sizing is the cheapest way to route around review, so this is the one place to be suspicious of your own convenience.", ""),
        ("service", "service-management-lead checks the calendar", "Is a change freeze active? Which SLA applies? Freeze windows are read by the policy plane, not by a person remembering.", ""),
        ("requirements", "product-owner writes success criteria", "Criteria that can be falsified. A criterion nobody can fail is decoration.", ""),
        ("privacy", "data-protection-officer scopes the regimes", "GDPR always. HIPAA if healthcare, PCI DSS if e-commerce, SOC 2 if SaaS or CRM. Decided now, not at audit.", ""),
        ("design", "design-owner commits DESIGN.md", "One design generator, one aesthetic family. Two active generators give the workforce contradictory style instructions.", ""),
        ("CEO", "You approve the design", "Your first decision. The only defence against ten sibling websites.", "ceo"),
        ("architecture", "web-architect and data-architect decide", "Lane A, B, C1, C2 or C3 — exactly one. Schema, grain, retention and the ADR.", ""),
        ("build", "Architects dispatch engineers", "Each engineer returns a candidate, never a merge. Every tool call passes Cedar and leaves an Ed25519 receipt in a hash chain.", ""),
        ("review", "merge-authority reviews", "Read-only, reporting outside the team that wrote the code. Blocks with evidence, never with an opinion.", ""),
        ("CEO", "You approve the merge", "Your second decision. No agent merges its own work.", "ceo"),
        ("gate", "Nine job families run in CI", "Promotion depends on job success, not a pass percentage. A cancelled, timed-out or unscheduled job is a failure.", ""),
        ("vetoes", "Three officers may stop it here", "security-engineer on a vulnerability or broken receipt chain · sre on production instability · quality-compliance on documented non-conformance. Only you override.", "stop"),
        ("promote", "release-manager promotes to main", "Routes failures to the owning officer. Never fixes them.", ""),
        ("payroll", "payroll-controller closes the meter", "Tokens and wall clock per agent, allocated to the project, reconciled against the provider invoice.", ""),
        ("teardown", "dependency-steward uninstalls Tier C", "The step everyone skips, and the reason context budgets rot.", ""),
    ]
    body = phead(
        "Workflow",
        "How a build reaches production",
        "Sixteen steps. Two of them are yours. Everything between them is governed, "
        "receipted, and reviewed by someone who did not write it.",
    )
    body += '<div class="flow">'
    for tag, title, note, cls in steps:
        body += (
            f'<div class="step {cls}"><span class="i">{e(tag)}</span>'
            f'<div><div class="t">{e(title)}</div><p class="b">{e(note)}</p></div></div>'
        )
    body += "</div>"

    body += """
<h2>Failure routing</h2>
<p class="sub"><code>release-manager</code> routes. It does not fix. Routing a failure to
the wrong owner costs a cycle; fixing it yourself costs the separation the whole gate
depends on.</p>
<div class="tw"><table>
<thead><tr><th>Failure</th><th>Goes to</th></tr></thead><tbody>
<tr><td>Test failure</td><td class="name">testing-architect</td></tr>
<tr><td>Type error</td><td class="name">owning architect</td></tr>
<tr><td>Dependency audit or SAST finding</td><td class="name">security-engineer <span class="chip veto">veto</span></td></tr>
<tr><td>Broken link, Mermaid parse failure</td><td class="name">cto → docgen</td></tr>
<tr><td>Pin drift, uncertified plugin</td><td class="name">dependency-steward</td></tr>
<tr><td>Policy receipt chain broken</td><td class="name">security-engineer <span class="chip veto">veto</span></td></tr>
<tr><td>Cedar policy blocking legitimate work</td><td class="name">platform-architect — loosen from receipts</td></tr>
<tr><td>E2E failure</td><td class="name">testing-architect</td></tr>
<tr><td>Golden-trace flip</td><td class="name">dependency-steward — advisory, never blocks</td></tr>
<tr><td>Missing or stale DESIGN.md</td><td class="name">design-owner</td></tr>
<tr><td>Production instability</td><td class="name">sre <span class="chip veto">veto</span></td></tr>
<tr><td>Documented non-conformance</td><td class="name">quality-compliance <span class="chip veto">veto</span></td></tr>
<tr><td>Privacy finding</td><td class="name">data-protection-officer → quality-compliance</td></tr>
<tr><td>Budget exhausted</td><td class="name">finance-controller — halts, never warns</td></tr>
<tr><td>Client-raised incident</td><td class="name">service-management-lead → sre</td></tr>
</tbody></table></div>

<div class="note"><strong>Two decisions per build.</strong> That is the target shape, and
the expansion does not change it. Neither <code>coo</code> nor the Data Protection Officer
sits on the <code>/build</code> path &mdash; corporate escalations stop at an officer, and
privacy findings reach you only through <code>quality-compliance</code>'s veto.</div>
"""
    return shell("Workflow", "Workflow", body, f)


# ═══════════════════════════ page: architecture ═══════════════════════════

def page_architecture(c: Company) -> str:
    f = c.figures
    planes = [
        ("1 · Control", "Starts, stops, schedules, budgets. Holds the kill switch.", "Fully trusted", "deployment obligation", "veto"),
        ("2 · Policy", "Evaluates every tool call: who, what, where, which tier, what budget.", "Fully trusted, deterministic", "owned here", ""),
        ("3 · Identity", "Issues short-lived scoped credentials. Records the human principal.", "Fully trusted", "deployment obligation", "veto"),
        ("4 · Reasoning", "The model, the prompt, the planner. Decides what to do next.", "UNTRUSTED", "owned here", "lead"),
        ("5 · Execution", "Where model-generated code actually runs.", "HOSTILE — assume compromise", "deployment obligation", "veto"),
        ("6 · Tool &amp; data", "The registered tool surface and the systems behind it.", "Trusted code, untrusted callers", "owned here", ""),
        ("7 · Observability", "Traces, tool-call log, provenance, receipts.", "Fully trusted, append-only", "owned here", ""),
    ]
    body = phead(
        "Architecture",
        "Seven planes, five lanes, one gate",
        "The line that matters runs between what proposes and what authorises. If the "
        "model is on both sides of it, the architecture is wrong.",
    )
    body += """
<h2>The seven planes</h2>
<p class="sub">This repository is not a runtime, so it owns four planes and declares the
other three as deployment obligations. Naming the gap is itself a control &mdash; a
repository that claims to enforce sandboxing it does not run is worse than one that
says so.</p>
<div class="tw"><table>
<thead><tr><th>Plane</th><th>Responsibility</th><th>Trust</th><th>Status</th></tr></thead><tbody>
"""
    for name, resp, trust, status, cls in planes:
        chip = f'<span class="chip {cls}">{status}</span>' if cls else f'<span class="chip">{status}</span>'
        body += f'<tr><td class="name">{name}</td><td>{resp}</td><td>{e(trust)}</td><td>{chip}</td></tr>'
    body += "</tbody></table></div>"

    body += f"""
<div class="note warn"><strong>What this repository does not do.</strong> It does not run
a kernel-isolated sandbox, issue credential leases, or host an out-of-band kill switch.
Those are the control, identity and execution planes, and they are production deployment
requirements. The database has tables for kill-switch and restore drills
(<code>ops.KillSwitchDrill</code>, <code>ops.RestoreDrill</code>) precisely so that the
absence of a dated, measured record is visible rather than assumed.</div>

<h2>Delivery lanes</h2>
<p class="sub">One lane per project, chosen by <code>web-architect</code> at Architecture
and recorded in that project's <code>DESIGN.md</code>. A project never carries two.</p>
<div class="tw"><table>
<thead><tr><th>Lane</th><th>What it builds</th><th>Stack</th><th>Chosen when</th></tr></thead><tbody>
<tr><td class="name">A</td><td>Database-backed web</td><td>Django + React</td><td>Accounts, data, workflows</td></tr>
<tr><td class="name">B</td><td>Static-first web</td><td>Vite + React, no DB</td><td>Content-heavy, Core Web Vitals critical</td></tr>
<tr><td class="name">C1</td><td>Android native</td><td>Kotlin + Jetpack Compose</td><td>Android-only, premium UX, deep platform integration</td></tr>
<tr><td class="name">C2</td><td>Cross-platform mobile</td><td>Flutter / Dart 3</td><td>Android and iOS from one budget</td></tr>
<tr><td class="name">C3</td><td>Mobile companion</td><td>React Native + Expo</td><td>Client already buying the web lane</td></tr>
</tbody></table></div>

<div class="note warn"><strong>The iOS limit, stated at scoping.</strong> Xcode is
macOS-only. All three mobile sub-lanes build Android on Windows. C2 and C3 write
iOS-capable code but cannot compile it here. An iOS deliverable needs a macOS runner
budgeted before the project starts &mdash; told to the client at scoping, not discovered
at release.</div>

<h2>The gate</h2>
<p class="sub">Nine job families. Every one deterministic, every one in CI, so the gate
costs zero context tokens.</p>
<div class="tw"><table>
<thead><tr><th>Family</th><th>Runs</th><th>Blocks</th></tr></thead><tbody>
<tr><td>Project tests — Lane A</td><td><code>pip-audit</code>, <code>mypy</code>, <code>pytest</code></td><td>yes</td></tr>
<tr><td>Project tests — Lane B</td><td><code>npm audit</code>, <code>tsc --noEmit</code>, <code>vitest</code></td><td>yes</td></tr>
<tr><td>Project tests — Lane C</td><td><code>gradle test</code> / <code>flutter test</code> / <code>jest</code>, device matrix</td><td>yes</td></tr>
<tr><td>Repository</td><td><code>ru_aibotworks_genome.py --validate</code>, <code>ru_aibotworks_generate.py --check</code></td><td>yes</td></tr>
<tr><td>Links</td><td>internal <strong>and</strong> external</td><td>yes</td></tr>
<tr><td>Diagrams</td><td>every Mermaid block parsed</td><td>yes</td></tr>
<tr><td>Plugin integrity</td><td>pins match the lock file; certifications current</td><td>yes</td></tr>
<tr><td>Policy receipts</td><td>chain verifies <strong>offline</strong></td><td>yes</td></tr>
<tr><td>Agent regression</td><td>golden-trace diff</td><td><span class="chip lead">advisory</span></td></tr>
</tbody></table></div>
<p class="sub">The last row is advisory on purpose. Golden-trace diffing against
non-deterministic models produces false positives, and a flaky blocker teaches people to
bypass the gate.</p>

<h2>Where things live</h2>
<div class="tw"><table>
<thead><tr><th>Path</th><th>Holds</th><th>Generated?</th></tr></thead><tbody>
<tr><td class="name">RU-AIBOTWORKS-REGISTRY/</td><td>The single source of truth: identity, officers, departments, workforce, tools</td><td>no — reviewed like code</td></tr>
<tr><td class="name">RU-AIBOTWORKS-PLATFORM/</td><td>Registry loader, genome validator, generator, seed builder, this portal</td><td>no</td></tr>
<tr><td class="name">RU-AIBOTWORKS-DEPARTMENTS/</td><td>{f['agents_total']} agent packages — charter, registration, tools, evaluation, skills</td><td><strong>yes</strong></td></tr>
<tr><td class="name">RU-AIBOTWORKS-DATABASE/</td><td>SQL Server schema and the generated seed</td><td>seed: <strong>yes</strong></td></tr>
<tr><td class="name">RU-AIBOTWORKS-PORTAL/</td><td>These six pages</td><td><strong>yes</strong></td></tr>
<tr><td class="name">RU-AIBOTWORKS-DOCS/</td><td>ADRs and the charter</td><td>no</td></tr>
<tr><td class="name">.claude/agents/</td><td>The {f['officers']} officers Claude Code loads</td><td><strong>yes</strong> — synced from the registry</td></tr>
</tbody></table></div>
"""
    return shell("Architecture", "Architecture", body, f)


# ═══════════════════════════ page: governance ═══════════════════════════

def page_governance(c: Company) -> str:
    f = c.figures
    body = phead(
        "Governance",
        "The harness every agent is held in",
        "Twenty-four checks run over the whole company on every build. Each one exists "
        "because something can go wrong silently, and silence is the failure mode that "
        "matters here.",
    )
    body += f"""
<div class="stats">
  {stat(24, 'checks', 'Run by ru_aibotworks_genome.py on every push.')}
  {stat(f['agents_total'], 'agents covered', 'Every agent. No exemptions, no exceptions.')}
  {stat(f['tools_registered_denied'], 'tools denied to all', 'Tier 3 and 4, registered so the refusal is auditable.', 'v')}
  {stat(0, 'dangerous grants', 'Verified in the database, not asserted here.', 'i')}
</div>

<h2>Company invariants</h2>
<div class="tw"><table>
<thead><tr><th>#</th><th>Invariant</th><th>Why it exists</th></tr></thead><tbody>
<tr><td class="name">I1</td><td>Every reporting line resolves</td><td>An agent reporting to nobody is an agent nobody is accountable for</td></tr>
<tr><td class="name">I2</td><td>Authority never inverts</td><td>A reviewer that reports to who it reviews is not a reviewer</td></tr>
<tr><td class="name">I3</td><td>Exactly three standing vetoes</td><td>A fourth stop button dilutes all four; a third fewer removes a real one</td></tr>
<tr><td class="name">I4</td><td>The reserved-decision list has not shrunk</td><td>Delegation creeps quietly; this catches it</td></tr>
<tr><td class="name">I5</td><td>Every agent has department, team, role, domains and a skill</td><td>An ungoverned agent looks identical to a governed one</td></tr>
<tr><td class="name">I6</td><td>No L2 without a logged promotion</td><td>Authority acquired without a record is drift</td></tr>
<tr><td class="name">I7</td><td>Every capability maps to exactly one officer</td><td>Two owners means no owner</td></tr>
<tr><td class="name">I8</td><td>No orchestrator at the entry point</td><td>Capability does not confer authority</td></tr>
<tr><td class="name">I9</td><td>No veto holder writes what it blocks</td><td>An agent that can edit what it blocks is not a control</td></tr>
<tr><td class="name">I10</td><td>Every project has a DESIGN.md</td><td>The only defence against ten sibling websites</td></tr>
<tr><td class="name">I11</td><td>Every figure derives from one computed source</td><td>Two documents that disagree are both untrustworthy</td></tr>
<tr><td class="name">I12</td><td>Every read-only agent is capped at tier 0</td><td>Read-only in name and writeable in fact is the worst case</td></tr>
<tr><td class="name">I13</td><td>One lane and one design generator per build</td><td>Two active generators give contradictory instructions</td></tr>
</tbody></table></div>

<h2>STD-AGENT-001 controls</h2>
<p class="sub">The highest-leverage controls from the Engineering Standard, enforced by
the same validator rather than by a document nobody re-reads.</p>
<div class="tw"><table>
<thead><tr><th>Control</th><th>Requirement</th><th>How it is held</th></tr></thead><tbody>
<tr><td class="name">A1.2</td><td>Backups unreachable from any agent identity</td><td><code>backup-operator</code> and <code>reaper</code> are unassumable; the check fails if either leaves the forbidden list</td></tr>
<tr><td class="name">A1.3</td><td>Default-deny egress, including DNS</td><td>Registry declares <code>default: deny</code> with an explicit allowlist; an empty allowlist fails closed</td></tr>
<tr><td class="name">A1.4</td><td>No hard-delete verb</td><td>No granted tool name matches a delete verb; <code>record.soft_delete</code> exists so nothing ever needs one</td></tr>
<tr><td class="name">A1.6</td><td>No agent writes its own configuration</td><td>Every granted write tool carries <code>blocked_if: target.is_agent_configuration</code></td></tr>
<tr><td class="name">A1.7</td><td>Hard budgets enforced by the runtime</td><td>Steps, tokens, cost and mutations per agent; <code>fin.Budget</code> refuses any row that warns instead of halting</td></tr>
<tr><td class="name">A1.8</td><td>Append-only trajectory log</td><td><code>ops.ToolCall</code> and <code>ops.ContextProvenance</code>, written under a principal no agent holds</td></tr>
<tr><td class="name">AGT-TOOL-01</td><td>Complete contract before invocation</td><td>All {f['tools_registered']} tools carry every required field; incomplete means Tier 3 and denied</td></tr>
<tr><td class="name">AGT-DES-01</td><td>Tier and rollback on every tool</td><td>The database refuses a grantable Tier 2+ tool with a null rollback &mdash; a CHECK constraint, not a review note</td></tr>
<tr><td class="name">AGT-AUT-01</td><td>Tier 4 is never automatic</td><td>No agent declares max_tier above 2; Tier 3 and 4 tools are granted to nobody</td></tr>
</tbody></table></div>

<h2>Compliance posture</h2>
<p class="sub">Obligations attach per project at scoping, from a fixed matrix. Applying
every regime to every project is what makes compliance ceremonial; applying none until
audit is what makes it fatal.</p>
<div class="grid2">
  <div class="panel">
    <h3>Always in force</h3>
    <ul class="tight">
      {"".join(f"<li>{e(r)}</li>" for r in c.identity["compliance"]["always"])}
    </ul>
  </div>
  <div class="panel">
    <h3>Attaches by template</h3>
    <ul class="tight">
      {"".join(f"<li><strong>{e(k)}</strong> &mdash; {', '.join(e(t) for t in v)}</li>" for k, v in c.identity["compliance"]["conditional"].items())}
    </ul>
  </div>
</div>

<div class="note"><strong>PCI DSS &mdash; integrate, never implement.</strong> Card data
does not enter our systems. Hosted fields only, keeping the client in SAQ-A scope. A
project that would place a card number in our database is rescoped or declined, and
<code>security-engineer</code> holds that line as a veto matter.</div>

<div class="note"><strong>HIPAA &mdash; PHI never enters a context window.</strong> The
healthcare template is built against synthetic fixtures. Agents on a HIPAA project run at
<code>max_tier: 2</code> with no egress beyond the allowlist. That is the three-factor
rule applied concretely: a session with PHI scope gets no untrusted content and no
outbound channel.</div>

<h2>Review cadence</h2>
<p class="sub">The distinguishing question is never whether a control exists. It is when
it was last exercised. A kill switch that has never been pulled and a backup that has
never been restored are absent controls with present documentation.</p>
<div class="tw"><table>
<thead><tr><th>Activity</th><th>Frequency</th><th>Owner</th></tr></thead><tbody>
<tr><td>Kill-switch game day, latency measured and published</td><td>quarterly</td><td class="name">kill-switch-operator</td></tr>
<tr><td>Restore drill, measured RTO</td><td>quarterly</td><td class="name">database-admin</td></tr>
<tr><td>Transitive-closure audit against backup accounts</td><td>quarterly</td><td class="name">identity-and-access-engineer</td></tr>
<tr><td>Agent registration and blast-radius review</td><td>every 6 months</td><td class="name">agent-registrar</td></tr>
<tr><td>Tool contract review — tiers, rollbacks, scopes</td><td>every 6 months</td><td class="name">tool-registry-engineer</td></tr>
<tr><td>Evaluation-harness cheat test</td><td>every 6 months</td><td class="name">llm-evaluation-engineer</td></tr>
<tr><td>Judge-drift check against a frozen calibration set</td><td>monthly</td><td class="name">llm-evaluation-engineer</td></tr>
<tr><td>Injection-canary and honeytoken verification</td><td>continuous, reviewed monthly</td><td class="name">injection-canary-engineer</td></tr>
<tr><td>Exception register — every open exception has an owner and an expiry</td><td>monthly</td><td class="name">nonconformance-recorder</td></tr>
<tr><td>Payroll reconciliation against the provider invoice</td><td>monthly</td><td class="name">payroll-reconciliation-auditor</td></tr>
</tbody></table></div>
"""
    return shell("Governance", "Governance", body, f)


def main() -> int:
    c = Company.load()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "RU-AIBOTWORKS-portal.css").write_text(STYLE, encoding="utf-8")

    pages = {
        "RU-AIBOTWORKS-index.html": page_index(c),
        "RU-AIBOTWORKS-org-chart.html": page_org(c),
        "RU-AIBOTWORKS-workforce.html": page_workforce(c),
        "RU-AIBOTWORKS-workflow.html": page_workflow(c),
        "RU-AIBOTWORKS-architecture.html": page_architecture(c),
        "RU-AIBOTWORKS-governance.html": page_governance(c),
    }
    for name, html in pages.items():
        (OUT / name).write_text(html, encoding="utf-8")

    (OUT / "RU-AIBOTWORKS-company.json").write_text(
        json.dumps(
            {
                "generated": TODAY.isoformat(),
                "figures": c.figures,
                "officers": [
                    {"name": o.name, "level": o.level, "reports_to": o.reports_to,
                     "function": o.function, "division": o.division, "power": o.power,
                     "model": o.model, "decides": o.decides, "added": o.added}
                    for o in c.officers
                ],
                "departments": c.departments,
                "agents": [
                    {"name": a.name, "role": a.role, "model": a.model, "tier": a.tier,
                     "level": a.level, "lead": a.lead, "read_only": a.read_only,
                     "department": a.department, "team": a.team, "cohort": a.cohort,
                     "capability": a.plugin, "reports_to": c.reports_to_of(a),
                     "domains": list(a.domains),
                     "skills": [s["id"] for s in a.skills],
                     "tools": grants_for(a),
                     "budgets": BUDGETS[a.tier],
                     "blast_radius": blast_radius_for(a, c)}
                    for a in c.agents
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    total = sum((OUT / n).stat().st_size for n in pages) // 1024
    print(f"portal generated — {len(pages)} pages, {total} KB")
    for name in pages:
        print(f"  {name}")
    print(f"  RU-AIBOTWORKS-portal.css · RU-AIBOTWORKS-company.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
