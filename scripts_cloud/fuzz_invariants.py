"""Fuzzer déterministe d'invariants physiques exécuté sous PyPy 3.11 (porte [6/6] verify_lot)."""

from __future__ import annotations

import argparse
import multiprocessing
import os
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bots.bot_b0 import choose_b0
from bots.heuristic_engine import play_game_b1, play_game_b2
from engine.core_engine import apply_choice, step_until_decision
from engine.effects import load_all_effects, lot_01, lot_02  # noqa: F401
from engine.effects.registry import list_registered_tiles
from engine.primitives import GameOver
from engine.rng import SRC_TACTICS_SETUP, rand_below
from engine.state import (
    PEUPLES_ORDER,
    TRACK_LEN,
    GameConfig,
    GameState,
)
from engine.telemetry import TelemetryTracker


def _check_board_invariants(state: GameState) -> None:
    cfg = state.cfg
    n = cfg.n_players
    p_max = cfg.p_max
    dotation = cfg.dotation_arbres

    for r in range(n):
        for p in range(1, p_max + 1):
            arbres = state.get_parcel_arbres(r, p)
            souches = state.get_parcel_souches(r, p)
            cap = dotation[p - 1]
            assert 0 <= arbres + souches <= cap, (
                f"Invariant Arbres+Souches violé sur ({r},{p}) : {arbres}+{souches} > {cap}"
            )
            assert state.get_parcel_insectes(r, p) >= 0
            assert state.get_parcel_defenseurs(r, p) >= 0

            if arbres == 0 and souches == 0:
                assert state.get_parcel_defenseurs(r, p) == 0, "Défenseur sur Route Forestière"
                assert state.get_parcel_insectes(r, p) == 0, "Insecte sur Route Forestière"
                if cfg.mode >= 2:
                    assert state.get_parcel_nid(r, p)[0] == 0, "Nid sur Route Forestière"

    for l_idx in range(n):
        for p in range(1, p_max + 1):
            s0, s1, s2, s3 = state.get_furtivite_slots(l_idx, p)
            d0 = (1 if s0 else 0) + (1 if s1 else 0)
            d1 = (1 if s2 else 0) + (1 if s3 else 0)
            tot = d0 + d1
            assert 0 <= tot <= 2, f"Plus de 2 Défenseurs en Furtivité ({l_idx},{p}) : {tot}"
            if tot == 2:
                assert d0 == 2 or d1 == 2, "Binôme Furtivité scindé sur les 2 rives"
            assert state.get_furtivite_insectes(l_idx, p) >= 0

    for c in range(1, TRACK_LEN + 1):
        assert state.get_bugs_at_case(c) >= 0
        assert state.get_colonie_at_case(c) >= 0


def _pick_registered_tile_profiles(
    game_idx: int,
    by_slot: dict[str, list[str]],
) -> tuple[tuple[str, str], ...]:
    selected: list[tuple[str, str]] = []
    for idx_s, (slot_id, profs) in enumerate(sorted(by_slot.items())):
        pick = rand_below(len(profs), 777_000, game_idx, SRC_TACTICS_SETUP, 0, idx_s, 0)
        selected.append((slot_id, profs[pick]))
    return tuple(selected)


def _fuzz_range(bounds: tuple[int, int, int]) -> int:
    start_idx, end_idx, total = bounds
    rotations = tuple(PEUPLES_ORDER[rot:] + PEUPLES_ORDER[:rot] for rot in range(6))

    by_slot: dict[str, list[str]] = {}
    for s_id, prof in list_registered_tiles():
        by_slot.setdefault(s_id, []).append(prof)

    t1 = (total * 35) // 100
    t2 = (total * 70) // 100

    for game_idx in range(start_idx, end_idx):
        mode = 1 if game_idx < t1 else (2 if game_idx < t2 else 3)
        n_players = 3 + (game_idx % 4)
        chassis_id = (game_idx * 17) & 127
        peuples = rotations[game_idx % 6][:n_players]
        bot_sel = game_idx % 5  # 0,1,2 -> B0 ; 3 -> B1 ; 4 -> B2

        base_cfg = GameConfig.from_chassis_index(
            chassis_id,
            n_players=n_players,
            mode=mode,
            peuples=peuples,
            exp_seed=900_000 + mode * 10_000,
            rep_id=game_idx,
            max_revision_passes=0 if bot_sel < 3 else 3,
        )
        if mode == 3:
            t_profs = _pick_registered_tile_profiles(game_idx, by_slot)
            cfg = GameConfig(
                n_players=base_cfg.n_players,
                mode=3,
                peuples=base_cfg.peuples,
                exp_seed=base_cfg.exp_seed,
                rep_id=base_cfg.rep_id,
                coordonnateur_initial=base_cfg.coordonnateur_initial,
                max_revision_passes=base_cfg.max_revision_passes,
                p_max=base_cfg.p_max,
                regle_ouverture_reve_multiple=base_cfg.regle_ouverture_reve_multiple,
                offset_seuil_parade=base_cfg.offset_seuil_parade,
                mise_en_place_tactiques=base_cfg.mise_en_place_tactiques,
                declenchement_fin_de_piste=base_cfg.declenchement_fin_de_piste,
                role_abatteuse_fin_de_piste=base_cfg.role_abatteuse_fin_de_piste,
                synergie_binome_machines=base_cfg.synergie_binome_machines,
                tile_profiles=t_profs,
            )
        else:
            cfg = base_cfg

        state = GameState(cfg)
        trk = TelemetryTracker() if (game_idx % 20 == 0) else None

        if bot_sel == 3:
            over = play_game_b1(state, max_steps=2000, chassis_id=chassis_id, telemetry=trk)
            _check_board_invariants(state)
            assert 1 <= over.tour_fin <= 8 and 0.0 <= over.ratio_arbres <= 1.0
            continue

        if bot_sel == 4:
            over = play_game_b2(state, max_steps=2000, chassis_id=chassis_id, telemetry=trk)
            _check_board_invariants(state)
            assert 1 <= over.tour_fin <= 8 and 0.0 <= over.ratio_arbres <= 1.0
            continue

        steps = 0
        last_checked_tour = 0

        while True:
            steps += 1
            assert steps <= 2000, f"Non-terminaison sur game_idx={game_idx}"
            out = step_until_decision(state, max_internal_steps=2000, telemetry=trk)

            if state.tour != last_checked_tour:
                _check_board_invariants(state)
                last_checked_tour = state.tour

            if steps == 3 and (game_idx % 50 == 0):
                snap = state.raw_used_bytes()
                cloned = state.clone()
                assert cloned.raw_used_bytes() == snap
                if not isinstance(out, GameOver):
                    apply_choice(cloned, choose_b0(cloned, out))
                    assert state.raw_used_bytes() == snap

            if isinstance(out, GameOver):
                _check_board_invariants(state)
                assert 1 <= out.tour_fin <= 8
                assert 0.0 <= out.ratio_arbres <= 1.0
                break

            choice = choose_b0(state, out)
            apply_choice(state, choice, telemetry=trk)

    return end_idx - start_idx


def run_fuzzer(total_games: int = 1000, workers: int | None = None) -> tuple[float, float]:
    """Joue `total_games` parties (Modes 1, 2, 3 ; B0, B1, B2) sur N=3..6 et châssis 0..127."""
    n_workers = workers if workers is not None else min(4, max(1, os.cpu_count() or 1))
    t0 = time.perf_counter()

    if n_workers <= 1 or total_games < 200:
        _fuzz_range((0, total_games, total_games))
    else:
        chunk = total_games // n_workers
        rem = total_games % n_workers
        chunks: list[tuple[int, int, int]] = []
        cur = 0
        for w in range(n_workers):
            nxt = cur + chunk + (1 if w < rem else 0)
            if nxt > cur:
                chunks.append((cur, nxt, total_games))
            cur = nxt
        with multiprocessing.Pool(processes=len(chunks)) as pool:
            done = sum(pool.map(_fuzz_range, chunks))
        assert done == total_games

    elapsed = time.perf_counter() - t0
    gps = total_games / elapsed if elapsed > 0 else 0.0
    return elapsed, gps


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PyPy Invariant Fuzzer")
    parser.add_argument("--games", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=None)
    args = parser.parse_args(argv)

    elapsed, gps = run_fuzzer(args.games, workers=args.workers)
    impl = platform.python_implementation()
    print(
        f"Fuzzer OK ({impl} {platform.python_version()}) : "
        f"{args.games} parties en {elapsed:.3f}s ({gps:.0f} parties/s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
