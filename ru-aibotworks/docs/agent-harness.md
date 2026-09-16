# Agent safety harness

This repository uses [STD-AGENT-001](../../_builddocs/Production-Grade%20Enterprise%20Agentic%20Systems%20-%20Engineering%20Standard%20v1.0.docx)
as the control source for tool-using agents.

## Enforced controls

The repository-level harness currently enforces the standard's highest-leverage
tool-plane controls:

- default-deny egress with an explicit allowlist
- complete contracts for every registered tool
- irreversibility tiers from 0 through 4
- rollback commands for tier 2 and higher
- human approval for tier 3 and tier 4 tools
- no hard-delete, drop, truncate, or purge tool names
- explicit per-task, hourly, and mutation budgets
- before-state logging and receipt retention
- hash-chained append-only receipt verification

The harness is a validation gate, not an execution sandbox. It does not claim
that local Python or shell execution is isolated. Production deployment still
requires a managed sandbox, environment-separated credentials, default-deny
networking, an out-of-band kill switch, and backup reachability evidence.

## Commands

```text
python scripts/agent_harness.py validate
python scripts/agent_harness.py verify-receipts
```

Unclassified tools default to Tier 3 and must not be invoked until a complete
contract is added to the registry.

## Where the contracts live

[agent-tools.json](../../agent-tools.json) is **generated**. It holds the
runtime-reachable surface only. The authoritative registry, including the Tier 3
and Tier 4 tools that are registered and granted to nobody, is
[tools.yaml](../registry/tools.yaml).
Edit that, then run `ru_aibotworks_generate.py`.
