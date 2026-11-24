---
name: palier-4-canon
description: >-
  Évalue et calibre la sélection canonique des 30 tuiles Canon 0 (et futurs candidats B/C)
  sur toutes les tables équilibrées de 3 à 6 joueurs.
---

# Skill `palier-4-canon` — Calibration & Évaluation du Canon 0 (`30` Emplacements `v6.2`)

## Pré-requis d'Entrée
1. Vérifier dans `STATUS.md` que le noyau `v6.2` (Chantier 4) et les 30 tuiles du Canon 0 (`contracts/tiles_canon_v6_2.json`, statut `ACTIVE_VERIFIED` au Chantier 5) sont livrés.
2. Exécuter `uv run python verify_lot.py` et confirmer 100 % au vert.

## Protocole de Calibration Multi-Tables (`N = 3..6`)
1. **Châssis canonique unique** : `P4_2233`, départ décalé `Bulldozer p=1 / Abatteuse p=2` (zéro exploration d'axes morts).
2. **Protocole A/B apparié (`ACTIVE_VS_NEUTRE`)** : mesurer pour chaque emplacement (`G1..G15`, `R1..R10`, `M1..M5`) l'impact sur les cercles équilibrés (`balanced_neighbor_mirror_tables`), avec IC 95 % groupés par table, correction de Holm-Bonferroni et filtrage sous `< 1` activation/partie.
3. **Critères d'acceptation (`contracts/CORE_FREEZE_CRITERIA.md`)** :
   - `CVaR_20%` (bootstrap par grappes) robuste sur les 20 % pires tables ;
   - Équité inter-modules (*Gardiens & Éveil*, *Rêves & Sommeil*, *Essaim* et table `{H, E, I}`) ;
   - Profondeur stratégique stricte **`B0 < B1 < B2 <= B3`** et `Delta_V_negociation > 0` ;
   - Charge cognitive maîtrisée (`mem_debt == 0`, `law_stack <= 2`, `fiddliness <= 3,5`).
4. **Orchestration & Restitution** : suivre le protocole de devis 5 lignes et de publication auto-portante de [run-campaign](../run-campaign/SKILL.md), puis consigner les résultats dans `STATUS.md` et `docs/digests/`.
