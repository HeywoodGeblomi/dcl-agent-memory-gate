# DCL Agent Memory Gate

Weekend wiring. Not production. Not a LangGraph drop-in.

Proof-of-concept harness: a naive overwrite memory vs the same loop with Dual Residual evidence + Dynamic Commitment Layer (χ) + a sublation rewrite on flip.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install numpy
python demo.py
```

Seed 0 / T=120 expected:
- baseline final residual ≈ 0.3350
- gated final χ = 1 after one flip
- λ ≈ 0.380

## Files

- `memory_baseline.py` — overwrites on every observation (drifts).
- `memory_gated.py` — DCL step + sublation rewrite when χ flips.
- `dual_residual.py` — Python port of the locked C++ oracle (thresholds 0.04 / 0.005).
- `dcl.py` — hard DCL port.
- `demo.py` — parity-trap scenario.

## Honest limits

- Dual residual is *computed and logged*. It does **not** currently hard-block `dcl_step`.
- This is a 120-step toy loop, not MemGPT / Zep / LangGraph instrumentation.
- Public sibling: https://github.com/HeywoodGeblomi/dual-residual
- Kitchen DCL / residual-sublation / reconstruction-gate stay private. Do not treat those as public links.
