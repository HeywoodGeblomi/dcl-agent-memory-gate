# DCL Agent Memory Gate

**Proof-of-concept:** Instrument a simple long-horizon agent memory loop with the Dual Residual gate + Dynamic Commitment Layer (DCL) to stop drift.

This is the weekend wiring, not the full agent. Baseline = plain vector-ish memory that overwrites on new evidence. Gated = dual residual confirms ownership, DCL holds the hidden χ commitment, sublation keeps it coherent.

## Why this matters

Current agent memory (LangGraph checkpoints, MemGPT, Zep, etc.) loses irreversible internal state. An agent commits to a path; surface evidence shifts; later retrieval drifts or forgets the original constraint. This repo shows the gap and the fix on a minimal loop.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install numpy
python demo.py
```

## What it does

- `memory_baseline.py` — naive memory that updates on every new observation (drifts).
- `memory_gated.py` — wraps the same store with dual-residual confirmation + DCL χ commitment + sublation.
- `demo.py` — runs both on a parity-trap scenario (hidden polarity flips, visible signals stay similar) and prints divergence.
- `dual_residual.py` — pure-Python port of the locked C++ oracle (thresholds immutable: 0.04 / 0.005).
- `dcl.py` — port of the hard DCL from dynamic_commitment.h.

## Expected output

Baseline memory converges to the visible signal and loses the commitment. Gated version keeps the hidden χ and diverges exactly where the parity trap predicts.

See the repos:
- https://github.com/HeywoodGeblomi/dual-residual
- https://github.com/HeywoodGeblomi/residual-sublation

This is a demo harness. Not production. Not a claim of field-level performance.
