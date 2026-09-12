"""memory_gated.py — dual residual must confirm before DCL writes.

On each observation:
1. Append visible residual to the stream.
2. Run dual_residual.evidence on the recent window.
3. Only if confirmed: step DCL and allow a χ flip.
4. On flip, sublate: keep χ, rewrite the visible value.
5. Unconfirmed observations still land in the store as ordinary writes.
"""
from __future__ import annotations
from typing import Any
import numpy as np
from dual_residual import evidence
from dcl import DCLParams, dcl_init, dcl_step, dcl_commit

class GatedMemory:
    def __init__(self, freeze: bool = False):
        self.store: dict[str, Any] = {}
        self.dcl = dcl_init()
        self.par = DCLParams()
        self.history: list[float] = []
        self.commitment_log: list[int] = []
        self.freeze = freeze
        self.confirmed_steps = 0
        self.refused_steps = 0

    def observe(self, key: str, value: Any, r_fresh: float, k_fresh: float,
                r_corr: float) -> dict:
        self.history.append(float(r_fresh))
        ev = evidence(np.array(self.history[-64:]))
        prev_chi = self.dcl.chi
        flipped = False
        committed = False
        if ev.confirmed and not self.freeze:
            self.confirmed_steps += 1
            dcl_step(self.dcl, self.par, r_fresh, k_fresh, r_corr)
            flipped = self.dcl.chi != prev_chi
            committed = dcl_commit(self.dcl, self.par, r_corr)
        else:
            self.refused_steps += 1
            if ev.confirmed and self.freeze:
                dcl_step(self.dcl, self.par, r_fresh, k_fresh, r_corr, force_chi=0)
                committed = dcl_commit(self.dcl, self.par, r_corr)

        if flipped:
            old_val = self.store.get(key)
            self.store[key] = {
                "core": self.dcl.chi,
                "negated_from": old_val,
                "lifted": True,
            }
        else:
            self.store[key] = value

        self.commitment_log.append(self.dcl.chi)
        return {
            "dual_confirmed": ev.confirmed,
            "talent": ev.suggested.name,
            "chi": self.dcl.chi,
            "flipped": flipped,
            "committed": committed,
            "lambda": self.dcl.lambda_,
        }

    def read(self, key: str) -> Any:
        return self.store.get(key)

    def snapshot(self) -> dict:
        return {
            "store": dict(self.store),
            "chi_log": list(self.commitment_log),
            "lambda": self.dcl.lambda_,
            "confirmed_steps": self.confirmed_steps,
            "refused_steps": self.refused_steps,
        }
