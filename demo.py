"""demo.py — baseline vs gated vs frozen-χ on a parity-trap scenario."""
from __future__ import annotations
import numpy as np
from memory_baseline import BaselineMemory
from memory_gated import GatedMemory

def parity_trap_scenario(T: int = 120, seed: int = 0):
    rng = np.random.default_rng(seed)
    t = np.arange(T)
    d = np.clip(0.35 + 0.05 * np.sin(2 * np.pi * t / 25.0) + rng.normal(0, 0.03, T), 0, 1)
    c = np.clip(0.70 - 0.002 * t + rng.normal(0, 0.02, T), 0.05, 1)
    r_corr = np.clip(
        0.12
        + 0.10 * (np.sin(2 * np.pi * t / 18.0) > 0.4).astype(float)
        + rng.normal(0, 0.04, T),
        0, 1,
    )
    true_pol = np.zeros(T, dtype=int)
    pol = 0
    flips = [ft for ft in (30, 55, 80, 105) if ft < T]
    for i in range(T):
        if i in flips:
            pol ^= 1
        true_pol[i] = pol
    return d, c, r_corr, true_pol, flips

def _flip_count(log):
    return sum(1 for j in range(1, len(log)) if log[j] != log[j - 1])

def run():
    d, c, rc, true_pol, flips = parity_trap_scenario(120, 0)
    base = BaselineMemory()
    gated = GatedMemory(freeze=False)
    frozen = GatedMemory(freeze=True)
    print(f"Parity-trap: {len(d)} steps, scheduled hidden flips at {flips}")
    print(f"{'step':>5} {'true':>5} {'base':>8} {'chi':>5} {'frz':>5} {'own':>5}")
    for i in range(len(d)):
        base.write("residual", float(d[i]))
        g = gated.observe("residual", float(d[i]), float(d[i]), float(c[i]), float(rc[i]))
        f = frozen.observe("residual", float(d[i]), float(d[i]), float(c[i]), float(rc[i]))
        if i % 15 == 0 or i in flips:
            print(
                f"{i:>5} {true_pol[i]:>5} {float(d[i]):>8.3f} "
                f"{g['chi']:>5} {f['chi']:>5} {str(g['dual_confirmed']):>5}"
            )
    gs = gated.snapshot()
    fs = frozen.snapshot()
    print()
    print("SCOREBOARD")
    print(f"  baseline last visible d     {base.snapshot()['residual']:.4f}")
    print(f"  gated χ / flips / λ         {gs['chi_log'][-1]} / {_flip_count(gs['chi_log'])} / {gs['lambda']:.3f}")
    print(f"  frozen χ / flips / λ        {fs['chi_log'][-1]} / {_flip_count(fs['chi_log'])} / {fs['lambda']:.3f}")
    print(f"  gated dual confirm/refuse   {gs['confirmed_steps']} / {gs['refused_steps']}")
    print()
    print("Baseline overwrites. Frozen χ cannot leave 0. Gated can.")
    print("That is the hole. This is the nail. Not LangGraph. Not production.")

if __name__ == "__main__":
    run()
