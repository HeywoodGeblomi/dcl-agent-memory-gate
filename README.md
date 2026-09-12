# dcl-agent-memory-gate

Weekend wiring. Dual Residual gate + DCL hidden χ on a toy memory loop.

Not a filed title. Not LangGraph. Not production.

## Run

```bash
pip install -r requirements.txt
python demo.py
```

Needs numpy. One file, one command.

## What you should see

- Baseline: last visible residual only. Overwrites every step.
- Gated: Dual Residual must confirm before DCL may flip χ.
- Frozen: same gate, χ forced to 0. Ablation.

Seed 0 / T=120 is the locked print. If your numbers match the scoreboard in the latest run, the wiring is intact.

## Files

| file | job |
|---|---|
| `dual_residual.py` | Python port of the public Dual Residual oracle. Thresholds locked. |
| `dcl.py` | Hard DCL step + commit. |
| `memory_baseline.py` | Overwrite store. |
| `memory_gated.py` | Confirm then commit. |
| `demo.py` | Parity-trap + freeze ablation. |
| `NON_CLAIMS.md` | Honesty file. Wins on conflict. |

Public primitive: https://github.com/HeywoodGeblomi/dual-residual

DCL kitchen stays private. This repo does not grant it.
