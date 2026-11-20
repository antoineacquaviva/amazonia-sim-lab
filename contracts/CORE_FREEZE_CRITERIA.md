# CORE_FREEZE_CRITERIA.md — Critères de sortie de la Phase « Cœur Symétrique »

> **Phase active du dépôt** : `CORE_STABILIZATION` (Mode 2 à blanc — tuiles Gardiens, Rêves et Croissance jouables sans effets personnalisés).
> **Stock historique des 100 profils** : gelé sur le tag Git `archive/v5.4.3-legacy-100-tiles` et rangé dans `archive/legacy_tiles_v5_3/` + `archive/banque_idees_tuiles_v5_3.md`.

Tant que ces critères ne sont pas atteints sur les simulations Mode 2 (`B0..B2` sur `N=3..6`), **aucune nouvelle tuile asymétrique n'est implémentée** et le noyau (`engine/{state,rng,primitives,core_engine}.py`) reste dégelé pour itérer vite.

---

## 1. Grille cible de *Core Freeze* (Mode 2 à blanc, Bot `B2`, `N=3..6`)

| Axe | Métrique | État de référence (`calibration_pari_gardiens_v5_4`, `v5.4.3`) | Cible *Core Freeze* (à ajuster par l'auteur) |
| :--- | :--- | :--- | :--- |
| **Invariance `N=3..6`** | Écart max `mean_ratio_arbres` entre `N=3` et `N=6` | **+9,0 pts** (`70,5 %` à 3j → `79,5 %` à 6j) | **≤ 4,0 pts** |
| **Invariance pire table** | Écart max `table_cvar20_ratio` entre `N=3` et `N=6` | **+16,6 pts** (`59,6 %` → `76,2 %`) | **≤ 6,0 pts** |
| **Marge de difficulté** | `mean_ratio_arbres` global (cœur nu, avant pouvoirs) | **74,7 %** (`cvar20 = 63,9 %`, survie `100 %`) | **55 % – 68 %** (laisser de la marge aux futures tuiles) |
| **Équilibre des 3 fins** | `% Tour 8` / `% Sommeil Rêves` / `% Éveil Gardiens` | `87,8 %` / `5,3 %` / `6,9 %` | `65–85 %` T8, `≥ 5 %` Sommeil, `≥ 5 %` Éveil (cohérent `N=3..6`) |
| **Risque Pari Gardiens** | Taux de réussite d'Éveil (`success_rate_pct`) | **80,2 %** (`UNLIMITED` `9,9 %` vs `MAX_1_DEF` `3,9 %`) | **40 % – 65 %** (vrai arbitrage risque/récompense) |
| **Santé des systèmes** | Aucune mécanique morte en Mode 2 | `insects_spent_step5 = 0.0`, `sabotage_in_deck = 0.01` sur tours d'Éveil | Furtivité, Sabotage, Insectes/Parade, Pièges, Rêves et Pari Gardiens tous actifs |
| **Profondeur tactique** | Hiérarchie bots & négociation muette | À re-vérifier sur châssis final | **`B0 < B1 < B2`** strict + `Delta_V_negociation > 0` |
| **Budget cognitif** | `mean_fiddliness_ops`, `mean_mem_debt`, `mid_combat_interrupts` | `2,65` ops / `0,0` / `0,026` | Conserver `fiddliness ≤ 3,5` et `mem_debt == 0` |

---

## 2. Protocole de passage au *Core Freeze* (reprise des tuiles)

Une fois la grille ci-dessus validée sur une campagne Cloud Mode 2 de référence :

1. **Re-sceller le noyau** : regénérer `contracts/kernel_locks.sha256` (`engine/{state,rng,primitives,core_engine}.py`) et `contracts/core_state_api.md`.
2. **Concevoir les tuiles par micro-vagues** (jamais 100 d'un coup) :
   - Puiser dans [`archive/banque_idees_tuiles_v5_3.md`](../archive/banque_idees_tuiles_v5_3.md) les concepts classés `✅ Transposable` ou `🟡 À adapter`.
   - Implémenter d'abord **1 seul profil canonique par emplacement** (ou une famille à la fois : Rêves → Gardiens → Croissance), en validant chaque vague par campagne comparative Mode 3 vs Mode 2.
   - N'ajouter des variantes `B/C` que là où la télémétrie révèle un vrai levier d'équilibrage ou de contraste ludique.
