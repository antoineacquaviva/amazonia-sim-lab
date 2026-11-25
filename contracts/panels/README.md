# `contracts/panels/` — Staging & Comparaison Multi-Panels (`v6.3`)

Ce répertoire accueille en parallèle les **3 catalogues candidats indépendants** générés par 3 modèles distincts lors de l'Étape 2 (`v6.3`), avant sélection et assemblage du panel canonique retenu dans `contracts/tiles_canon_v6_3.json`.

## Convention de nommage

```text
contracts/panels/
├── README.md        # Ce guide
├── panel_1.json     # Catalogue complet candidat #1 (30 emplacements, schéma v6.3.1)
├── panel_2.json     # Catalogue complet candidat #2 (30 emplacements, schéma v6.3.1)
└── panel_3.json     # Catalogue complet candidat #3 (30 emplacements, schéma v6.3.1)
```

## Métadonnées recommandées par panel (`_meta`)

Chaque fichier `panel_<N>.json` respecte `contracts/tiles_canon_v6_3.schema.json` et renseigne dans `_meta` :
- `"schema_version": "6.3.1"` (ou `"6.3.0"` rétro-compatible) ;
- `"socle_verrouille": "6.2.0"` ;
- `"cadrage_source": "docs/cadrage_tuiles_v6_3.md"` ;
- `"panel_id": "panel_1"` (ou `"panel_2"`, `"panel_3"`) ;
- `"source_modele": "<nom du modèle / session>"` ;
- `"c02_supprime": true` ;
- `"murs_porteurs_verrouilles": ["M1_TEMPS_BATAILLE", "M2_CONSERVATION_THERMIQUE", "M3_INTEGRITE_PLATEAU_ET_ICONES", "M4_AUTONOMIE_PLANCHER_SOLO"]`.

Sur chaque tuile, il est recommandé de séparer explicitement :
- `"entrees_plancher"` : prérequis bloquants nécessaires à l'effet plancher garanti dès la `Face 1` en solo (`M4_AUTONOMIE_PLANCHER_SOLO`) ;
- `"entrees_synergie"` : états inter-tuiles optionnels (`BLEU`, `CALE`, `INSECTE_PASSAGER`, `ALTEREE`, `ECAILLE`, `CROC`...) exploités en alternative (`OU`), en amplificateur (`Si…`) ou en `Face 2`.

## Commandes de validation et de comparaison

1. **Valider un panel individuel (schéma + 197 assises + 4 murs porteurs `M1..M4`)** :
   ```bash
   uv run python scripts/audit_197.py contracts/panels/panel_1.json
   uv run python scripts/audit_197.py contracts/panels/panel_2.json
   uv run python scripts/audit_197.py contracts/panels/panel_3.json
   ```
2. **Rapport JSON détaillé d'un panel** :
   ```bash
   uv run python scripts/audit_197.py contracts/panels/panel_1.json --json
   ```
3. **Audit comparatif côte à côte des 3 panels (`panel_1` / `panel_2` / `panel_3`)** :
   ```bash
   uv run python scripts/audit_197.py --panels-dir contracts/panels
   ```
4. **Export JSON de la matrice comparative multi-panels** :
   ```bash
   uv run python scripts/audit_197.py --panels-dir contracts/panels --json
   ```

> **Comportement dans `verify_lot.py`** : les candidats archivés dans `contracts/panels/panel_*.json` sont vérifiés comme JSON valides (UTF-8) et résumés à titre diagnostic **sans bloquer `verify_lot.py`**, afin de pouvoir conserver et comparer les versions brutes des 3 IA avant assemblage final dans `contracts/tiles_canon_v6_3.json` (qui, lui, reste bloquant).
