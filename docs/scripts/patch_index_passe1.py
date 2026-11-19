#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Passe 1 : Découplage de index.html vers data/livret_v5_3.js et purge des branches Amortisseur/E."""

from __future__ import annotations

import datetime as dt
import re
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def sub_once(pattern: str, repl: str, text: str, label: str, optional_if_done: str | None = None) -> str:
    if optional_if_done and optional_if_done in text and not re.search(pattern, text, flags=re.DOTALL):
        print(f"  [SKIP] Déjà appliqué : {label}")
        return text
    new_text, count = re.subn(pattern, lambda _m: repl, text, count=1, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"Ancre introuvable ({count} match) pour : {label}")
    print(f"  [OK]   {label}")
    return new_text


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    index_path = root / "index.html"
    if not index_path.is_file():
        raise FileNotFoundError(f"Introuvable : {index_path}")

    src = index_path.read_text(encoding="utf-8").replace("\r\n", "\n")

    print("=== Passe 1 : Patch chirurgical de index.html ===")

    # 1. Onglet 4 : placeholder JSON + Grammaire v5.3 + primitive DEPLACEMENT
    src = sub_once(
        r"""placeholder='\{"chassis_overrides":\s*\{"Regle_Resolution_Piege":\s*"AMORTISSEUR_SANS_PARADE"\},\s*"peuples_cercle":\s*\["M","H","I"\]\s*\.\.\.\}'""",
        """placeholder='{"chassis_overrides": {"P_Max": 5}, "peuples_cercle": ["M","H","I"]}'""",
        src,
        "Onglet 4 : nettoyage du placeholder d'import JSON",
        optional_if_done='placeholder=\'{"chassis_overrides": {"P_Max": 5}',
    )
    src = src.replace("Grammaire Formelle v5.2", "Grammaire Formelle v5.3")
    src = src.replace("`PIEGE` (non engagé)", "`PIEGE` (non déclenché ce tour)")

    # 2. Balise <script src="data/livret_v5_3.js"> + state.chassis ramené aux 7 axes actifs
    if 'src="data/livret_v5_3.js"' not in src:
        src = sub_once(
            r'<script src="data/amazonia_data_v5_3\.js"></script>',
            '<script src="data/amazonia_data_v5_3.js"></script>\n  <script src="data/livret_v5_3.js"></script>',
            src,
            "Insertion de <script src=\"data/livret_v5_3.js\">",
        )
    else:
        print('  [SKIP] Déjà présent : <script src="data/livret_v5_3.js">')

    src = sub_once(
        r"peuplesCercle:\s*\['M',\s*'R',\s*'O',\s*'H'\],.*?(?=\n\s*// Profil choisi)",
        """peuplesCercle: ['M', 'R', 'O', 'H'],
      // Valeurs des 7 axes actifs du châssis v5.3
      chassis: {
        P_Max: 4,
        Regle_Ouverture_Reve_Multiple: 'UNIQUE_PAR_TOUR',
        Offset_Seuil_Parade: 0,
        Mise_En_Place_Tactiques: 'ORDRE_FIXE_T1_T6',
        Declenchement_Fin_De_Piste: 'ARRIVEE_DERNIERE_PARCELLE',
        Role_Abatteuse_Fin_De_Piste: 'STANDARD_COUPE_ARBRE',
        Synergie_Binome_Machines: 'INDIVIDUELLE'
      },""",
        src,
        "Nettoyage de state.chassis (7 axes v5.3)",
    )

    # 3. Purge des branches mortes AMORTISSEUR / E dans le configurateur
    src = sub_once(
        r"function isProfileCompatibleWithChassis\(.*?(?=\n\s*// Calcule l'indice unique)",
        """function isProfileCompatibleWithChassis(tileId, profLetter, chassisObj = state.chassis) {
      const tile = CATALOGUE_TUILES[tileId];
      if (!tile || !tile.profils[profLetter]) return { ok: false, reason: `Le profil ${profLetter} n'existe pas pour ${tileId}.` };
      const prof = tile.profils[profLetter];
      if (prof.requires_options) {
        for (const [axKey, allowedVals] of Object.entries(prof.requires_options)) {
          if (axKey === 'Regle_Resolution_Piege') continue;
          if (!allowedVals.includes(chassisObj[axKey])) {
            return {
              ok: false,
              reason: `${tileId} Profil ${profLetter} (${prof.nom}) exige ${axKey} = ${allowedVals.join(' ou ')}.`
            };
          }
        }
      }
      return { ok: true };
    }
""",
        src,
        "Mise à jour de isProfileCompatibleWithChassis()",
    )

    src = sub_once(
        r"function applyPresetBundle\(bundleKey\)\s*\{.*?(?=\n\s*// -+\s*\n\s*// 8\. ACTIONS DU CONFIGURATEUR)",
        """function applyPresetBundle(bundleKey) {
      state.bundleId = bundleKey;
      Object.keys(state.profileOverrides).forEach(k => { state.profileOverrides[k] = 'A'; });
      state.slotsInsectes.SLOT_BUG_CERVEAU = 'A';
      state.slotsInsectes.SLOT_COLONISATION_GARDIENS = 'A';

      if (bundleKey === 'ESSAI_52_EMBUSCADE') {
        D_SLOTS.forEach(id => { state.profileOverrides[id] = 'D'; });
      } else if (bundleKey === '52_CAPYBARA_D') {
        state.peuplesCercle = ['M', 'H', 'I'];
        Object.assign(state.profileOverrides, { G7: 'D', R3: 'A', G13: 'A', R6: 'D', M1: 'D', M4: 'D' });
      } else if (bundleKey === '52_HARPIE_D') {
        state.peuplesCercle = ['H', 'O', 'I'];
        Object.assign(state.profileOverrides, { G11: 'D', R5: 'D', G15: 'A', R6: 'D', M3: 'D', M4: 'D' });
      } else if (bundleKey === '52_DENDROBATE_D') {
        state.peuplesCercle = ['R', 'E', 'I'];
        Object.assign(state.profileOverrides, { G10: 'D', G14: 'D', R8: 'D', R10: 'D', M2: 'D', M5: 'D' });
      } else if (bundleKey === '52_PIERRE_D') {
        state.peuplesCercle = ['H', 'R', 'I'];
        Object.assign(state.profileOverrides, { G9: 'A', G14: 'D', R4: 'D', R6: 'D', M2: 'D', M4: 'D' });
      } else if (bundleKey === '52_ATELE_D') {
        state.peuplesCercle = ['M', 'O', 'I'];
        Object.assign(state.profileOverrides, { G3: 'D', G4: 'A', G13: 'A', G15: 'A', M1: 'D', M3: 'D' });
      }

      refreshAllUI();
    }
""",
        src,
        "Purge des bundles obsolètes _E dans applyPresetBundle()",
    )

    src = sub_once(
        r"function updateChassisAxis\(key, rawValue\)\s*\{.*?(?=\n\s*function resetChassisToDefault\b)",
        """function updateChassisAxis(key, rawValue) {
      let val = rawValue;
      if (key === 'P_Max' || key === 'Offset_Seuil_Parade') {
        val = Number(rawValue);
      }
      state.chassis[key] = val;
      state.bundleId = 'CUSTOM';
      document.getElementById('preset-bundle-select').value = 'CUSTOM';
      refreshAllUI();
    }
""",
        src,
        "Simplification de updateChassisAxis()",
    )

    src = src.replace(
        "Changez d'abord l'Axe 10 (Résolution des Pièges) dans le configurateur",
        "Ajustez l'axe requis dans le configurateur",
    )

    src = sub_once(
        r"const isEmbuscade = state\.chassis\.Regle_Resolution_Piege === 'EXIGE_PRESENCE_LOCALE';.*?(?=\n\s*document\.getElementById\('summary-arbres-pill'\))",
        """const piegePill = document.getElementById('summary-piege-pill');
      piegePill.textContent = 'Pièges : Embuscade (Déf ≥ 1)';
      piegePill.className = 'px-2 py-0.5 rounded bg-emerald-900/80 border border-emerald-500/50 text-emerald-200 font-medium';
""",
        src,
        "Badge permanent Embuscade (Déf >= 1) dans le bandeau",
        optional_if_done="piegePill.textContent = 'Pièges : Embuscade (Déf ≥ 1)';",
    )

    # 4. Extraction de renderDidacticRulebook() hors de index.html
    src = sub_once(
        r"\n\s*function renderDidacticRulebook\(\)\s*\{.*?(?=\n\s*// -+\s*\n\s*// 11\. RENDU DE L'EXPLORATEUR)",
        "\n    // renderDidacticRulebook() est désormais fourni par data/livret_v5_3.js",
        src,
        "Extraction de renderDidacticRulebook() hors de index.html",
        optional_if_done="// renderDidacticRulebook() est désormais fourni par data/livret_v5_3.js",
    )

    # 5. Extraction de REGLES_COEUR_SYNTHESE hors de index.html + mise à jour de _meta.fichiers_source
    src = sub_once(
        r"// Socle formel compact des règles.*?(?=\n\s*async function copyContextForGemini\b)",
        "// REGLES_COEUR_SYNTHESE est désormais fourni par data/livret_v5_3.js\n",
        src,
        "Extraction de REGLES_COEUR_SYNTHESE hors de index.html",
        optional_if_done="// REGLES_COEUR_SYNTHESE est désormais fourni par data/livret_v5_3.js",
    )

    src = src.replace(
        "fichiers_source: ['data/amazonia_data_v5_3.js', 'data/catalog_v5_3.json', 'index.html']",
        "fichiers_source: ['data/amazonia_data_v5_3.js', 'data/livret_v5_3.js', 'data/catalog_v5_3.json', 'index.html']",
    )

    # Contrôles d'intégrité rapides
    for forbidden in ("AMORTISSEUR_SANS_PARADE", "function renderDidacticRulebook(", "const REGLES_COEUR_SYNTHESE ="):
        if forbidden in src:
            raise RuntimeError(f"Résidu inattendu dans index.html : {forbidden}")

    # Sauvegarde + écriture
    backup_dir = root / "data" / ".backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak_path = backup_dir / f"index.html.{ts}.bak"
    shutil.copy2(index_path, bak_path)
    index_path.write_text(src, encoding="utf-8", newline="\n")

    print(f"\n[BACKUP] {bak_path.relative_to(root)}")
    print(f"[WRITE]  index.html mis à jour avec succès (prêt pour la Passe 2 : data/livret_v5_3.js).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())