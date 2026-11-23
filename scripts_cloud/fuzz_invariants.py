"""Fuzzer déterministe d'invariants physiques exécuté sous PyPy 3.11 (porte [8/8] verify_lot)."""

from __future__ import annotations

import argparse
import itertools
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
from engine.primitives import GameOver
from engine.state import (
    CANONICAL_P_MAX,
    CANONICAL_PROFIL_PISTE,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RETIRED,
    PEUPLES_ORDER,
    PIEGE_AUCUN,
    STEP_3_2_REVEAL,
    STEP_5_2_RATISSAGE,
    STEP_5_3_END_CHECK,
    TRACK_LEN,
    GameConfig,
    GameState,
    is_tactique_code,
    unpack_machine_card,
)
from engine.telemetry import TelemetryTracker

_ALL_TABLES_BY_N: dict[int, tuple[tuple[str, ...], ...]] = {
    n: tuple(itertools.combinations(PEUPLES_ORDER, n)) for n in (3, 4, 5, 6)
}


class BoundAttackInvariantTracker(TelemetryTracker):
    """Vérifie l'invariant bout-en-bout 3.2 -> 5.2 sur chaque tour de chaque partie.

    Toute machine liée à une Tactique (1..6) en sortie de 3.2 doit avoir attaqué avant
    la fin de 5.2 (`attacked == True`), sauf si elle a quitté la partie (`RETIRED` / `pos == 0`).
    """

    def __init__(self) -> None:
        super().__init__()
        self._bound_end_3_2: list[tuple[int, int, int, int]] = []
        self.checked_bindings: int = 0
        self.violations: list[str] = []

    def on_step_transition(self, state: GameState, prev_step: int, next_step: int) -> None:
        if prev_step == STEP_3_2_REVEAL:
            bound: list[tuple[int, int, int, int]] = []
            n = state.cfg.n_players
            for s in range(n):
                card, _, _, _, bound_t = state.get_player_hand(s)
                if 1 <= card <= 2 * n and is_tactique_code(bound_t):
                    ray, mt = unpack_machine_card(card)
                    pos, st, _ = state.get_machine_pos_status(ray, mt)
                    if st == MACHINE_STATUS_NORMAL and pos > 0:
                        bound.append((state.tour, ray, mt, bound_t))
            self._bound_end_3_2 = bound
        elif prev_step == STEP_5_2_RATISSAGE and next_step == STEP_5_3_END_CHECK:
            for b_tour, ray, mt, bound_t in self._bound_end_3_2:
                self.checked_bindings += 1
                pos, st, _ = state.get_machine_pos_status(ray, mt)
                _, _, attacked = state.get_machine_turn_stats(ray, mt)
                if not attacked and st != MACHINE_STATUS_RETIRED and pos > 0:
                    msg = (
                        f"Invariant 3.2->5.2 violé : tour={b_tour}, ray={ray}, m_type={mt}, "
                        f"bound_t=T{bound_t}, pos={pos}, status={st}, attacked={attacked}"
                    )
                    self.violations.append(msg)
                    raise AssertionError(msg)
            self._bound_end_3_2 = []
        super().on_step_transition(state, prev_step, next_step)


def _check_board_invariants(state: GameState) -> None:
    cfg = state.cfg
    n = cfg.n_players
    p_max = cfg.p_max
    assert cfg.profil_piste == CANONICAL_PROFIL_PISTE
    assert p_max == CANONICAL_P_MAX
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
                assert state.get_parcel_piege(r, p) == PIEGE_AUCUN, "Piège sur Route Forestière"
                if cfg.mode >= 2:
                    assert state.get_parcel_nid(r, p)[0] == 0, "Nid sur Route Forestière"

        # Furtivité v6.1 par rayon (rives 0=Piège et 1=Sabotage sur p=1 ; aucune occupation sur p>=2 ni Insectes)
        d_piege = state.get_furtivite_nb_def_rive(r, 1, FURT_RIVE_PIEGE)
        d_sab = state.get_furtivite_nb_def_rive(r, 1, FURT_RIVE_SABOTAGE)
        assert 0 <= d_piege <= 2, f"Plus de 2 Défenseurs Rive Piège sur rayon {r} : {d_piege}"
        assert 0 <= d_sab <= 2, f"Plus de 2 Défenseurs Rive Sabotage sur rayon {r} : {d_sab}"
        if not state.is_ray_furtivite_open(r) and state.step <= 31:
            assert d_piege == 0 and d_sab == 0, f"Défenseurs en Furtivité sur rayon rasé {r}"
        for p in range(1, p_max + 1):
            assert state.get_furtivite_insectes(r, p) == 0, "Insecte en Furtivité (interdit en v6.1)"
            if p >= 2:
                assert state.get_furtivite_slots(r, p) == (0, 0, 0, 0)

    for c in range(1, TRACK_LEN + 1):
        assert state.get_bugs_at_case(c) >= 0
        assert state.get_colonie_at_case(c) >= 0

    # Conservation stricte des machines normales : au début d'un tour (avant pioche) ou après 6.3
    active_normal_machines = sum(
        1
        for r in range(n)
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        if state.get_machine_pos_status(r, mt)[1] == MACHINE_STATUS_NORMAL
    )
    assert 0 <= active_normal_machines <= 2 * n
    assert state.sabotage_deck_count >= 0


def _fuzz_range(bounds: tuple[int, int, int]) -> int:
    start_idx, end_idx, total = bounds

    # Socle scellé v6.1 : 20 % Mode 1, 50 % Mode 2, 30 % Mode 4 (catalogue actif 30 tuiles)
    t1 = (total * 20) // 100
    t2 = (total * 70) // 100

    for game_idx in range(start_idx, end_idx):
        mode = 1 if game_idx < t1 else (2 if game_idx < t2 else 4)
        n_players = 3 + (game_idx % 4)
        tables_n = _ALL_TABLES_BY_N[n_players]
        peuples = tables_n[(game_idx // 4) % len(tables_n)]
        bot_sel = game_idx % 5  # 0,1,2 -> B0 ; 3 -> B1 ; 4 -> B2

        cfg = GameConfig(
            n_players=n_players,
            mode=mode,
            peuples=peuples,
            exp_seed=900_000 + mode * 10_000,
            rep_id=game_idx,
            max_revision_passes=0 if bot_sel < 3 else 3,
        )

        state = GameState(cfg)
        trk = BoundAttackInvariantTracker()

        if bot_sel == 3:
            over = play_game_b1(state, max_steps=2000, telemetry=trk)
            _check_board_invariants(state)
            assert 1 <= over.tour_fin <= 8 and 0.0 <= over.ratio_arbres <= 1.0
            assert not trk.violations
            if mode <= 2:
                assert trk.summary().mem_debt_score == 0
            continue

        if bot_sel == 4:
            over = play_game_b2(state, max_steps=2000, telemetry=trk)
            _check_board_invariants(state)
            assert 1 <= over.tour_fin <= 8 and 0.0 <= over.ratio_arbres <= 1.0
            assert not trk.violations
            if mode <= 2:
                assert trk.summary().mem_debt_score == 0
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
                assert not trk.violations
                if mode <= 2:
                    assert trk.summary().mem_debt_score == 0
                break

            choice = choose_b0(state, out)
            apply_choice(state, choice, telemetry=trk)

    return end_idx - start_idx


def run_fuzzer(total_games: int = 1000, workers: int | None = None) -> tuple[float, float]:
    """Joue `total_games` parties (Modes 1, 2, 4 ; B0, B1, B2) sur N=3..6 et les 42 tables de Peuples."""
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
