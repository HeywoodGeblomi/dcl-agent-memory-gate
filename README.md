# dcl-agent-memory-gate

Weekend wiring. Dual Residual gate + DCL hidden χ on a toy memory loop.

Not a filed title. Not LangGraph. Not production.

## Run

```bash
pip install -r requirements.txt
python demo.py
```

Needs numpy. Optional: `python demo.py --scenario residual_confirm` (or `parity_trap`).

## What you should see

Two scenarios, same three agents (baseline / gated / frozen-χ ablation):

1. **parity_trap** (seed 0, T=120, flips at 30/55/80/105) — Dual Residual confirms 0/120. Gate refuses; χ stays 0. Shows the refuse path.
2. **residual_confirm** — `noisy_ramp_confirmed` from the public dual-residual borderline suite (seed 42, amp 15, T=256). Dual Residual confirms on real 64-step windows; gated χ moves; frozen χ stays 0.

- Baseline: last visible residual only. Overwrites every step.
- Gated: Dual Residual must confirm before DCL may flip χ.
- Frozen: same gate, χ forced to 0. Ablation.

Do not invent numbers. Run `python demo.py` and read the printed SCOREBOARD lines.

## Files

| file | job |
|---|---|
| `dual_residual.py` | Python port of the public Dual Residual oracle. Thresholds locked. |
| `dcl.py` | Hard DCL step + commit. |
| `memory_baseline.py` | Overwrite store. |
| `memory_gated.py` | Confirm then commit. |
| `demo.py` | Parity-trap + residual-confirm + freeze ablation. |
| `NON_CLAIMS.md` | Honesty file. Wins on conflict. |

Public primitive: https://github.com/HeywoodGeblomi/dual-residual

DCL kitchen stays private. This repo does not grant it.
