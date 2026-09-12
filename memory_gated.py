"""memory_gated.py — dual residual + DCL commitment gate.

On each observation:
1. Run dual_residual.evidence on the visible stream.
2. If confirmed, feed DCL the residual/competence/correlation signals.
3. DCL may flip χ (hidden commitment) — this is the part no pure function of
   visible history can recover.
4. Sublation: when χ flips, negate the old visible commitment but keep the
   core (the χ bit itself) and lift it into the new state.
"""
from __future__ import annotations
from typing import Any
import numpy as np
from dual_residual import evidence, Talent
from dcl import DCLState, DCLParams, dcl_init, dcl_step, dcl_commit

class GatedMemory:
    def __init__(self):
        self.store: dict[str, Any] = {}
        self.dcl = dcl_init()
        self.par = DCLParams()
        self.history: list[float] = []  # visible residual stream for dual check
        self.commitment_log: list[int] = []  # χ history

    def observe(self, key: str, value: Any, r_fresh: float, k_fresh: float,
                r_corr: float) -> dict:
        """Process one observation through the gate."""
        self.history.append(float(r_fresh))
        # 1. Dual residual gate
        ev = evidence(np.array(self.history[-64:]))
        # 2. DCL step (may flip χ)
        prev_chi = self.dcl.chi
        dcl_step(self.dcl, self.par, r_fresh, k_fresh, r_corr)
        flipped = self.dcl.chi != prev_chi
        # 3. Sublation on flip: keep χ, rewrite visible commitment
        if flipped:
            # negate old visible state, preserve core (χ)
            old_val = self.store.get(key)
            if old_val is not None:
                self.store[key] = {"core": self.dcl.chi, "negated_from": old_val,
                                   "lifted": True}
            else:
                self.store[key] = {"core": self.dcl.chi, "lifted": True}
        else:
            self.store[key] = value
        # 4. Commit discharge if tension high
        committed = dcl_commit(self.dcl, self.par, r_corr)
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
        return {"store": dict(self.store), "chi_log": list(self.commitment_log),
                "lambda": self.dcl.lambda_}
