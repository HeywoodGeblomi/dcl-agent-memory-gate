# Done when

Private gated-memory loop. Not a public grant. NON_CLAIMS.md wins on conflict.

- Standing key: `repo.dcl-agent-memory-gate.claim`
- Refuse stream: real git work (insertions / timestamp deltas) must keep gated χ = 0 and frozen χ = 0
- Confirm stream: a series from our private work logs or repo activity, NOT `noisy_ramp_confirmed` seed 42 amp 15
- Finish line: refuse stream does not flip χ; confirm stream splits gated χ vs frozen χ; this file plus NON_CLAIMS.md still hold

Thresholds stay locked: 0.04 / 0.005 / 0.1 / 0.2. Do not edit `dual_residual.py` to chase a flip.

## Status

- standing key: `repo.dcl-agent-memory-gate.claim`
- claim text: "toy harness: dual residual gates DCL χ on memory writes; not production."
- live_refuse: dual-residual git insertions n=33, confirm 0/33, gated χ 0, frozen χ 0, claim kept
- live_confirm: BLOCKED — no private residual log on the machine
- audit_only_filesize_confirm: demoted, not a claim
- kill_b: not a claim
- wrap: complete
