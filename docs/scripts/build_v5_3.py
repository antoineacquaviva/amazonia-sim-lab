#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build final Amazonia Doc Studio v5.3 :
- Lit automatiquement le index.html d'origine (commit 7843fb3)
- Nettoie toutes les macros LaTeX (\text{Rang }, \rightarrow, \min, \max, \ge...)
- Restaure les interpolations JS avec chr(36)
- Découple les données (100 profils, 7 axes = 128 configs, Changelog v5.3) dans data/amazonia_data_v5_3.js
"""

import re
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "index.html"
DATA_DIR = ROOT / "data"
DATA_JS_PATH = DATA_DIR / "amazonia_data_v5_3.js"
DATA_JSON_PATH = DATA_DIR / "catalog_v5_3.json"

DOLLAR = chr(36)


def clean_latex_artifacts(html: str) -> str:
    """Supprime toutes les commandes LaTeX résiduelles (dont \\text{Rang })."""
    latex_map = [
        (r"\text{Rang } r \\rightarrow r-1", "Rang r → r−1"),
        (r"\text{Rang }", "Rang "),
        (r"\\rightarrow", "→"),
        (r"\rightarrow", "→"),
        (r"\\leftrightarrow", "↔"),
        (r"\leftrightarrow", "↔"),
        (r"\\ge", "≥"),
        (r"\ge", "≥"),
        (r"\pm", "±"),
        (r"\\min(D_1, D_2)", "min(D1, D2)"),
        (r"\\max(D_1, D_2)", "max(D1, D2)"),
        (r"\\max(0, D-1)", "max(0, D−1)"),
        (r"\\max", "max"),
    ]
    for old, new in latex_map:
        html = html.replace(old, new)
    return html


def fix_all_template_literals_in_script(html: str) -> str:
    """Restaure chr(36)+'{...}' uniquement dans les template literals JS."""
    marker = "<!-- BASE DE DONNÉES COMPLÈTE"
    pos = html.find(marker)
    if pos == -1:
        pos = html.rfind("<script>")
    head = html[:pos]
    script_part = html[pos:].replace(DOLLAR + "{", "{")

    out = []
    i = 0
    n = len(script_part)
    stack = []
    brace_depth_stack = []
    fixed_count = 0

    while i < n:
        ch = script_part[i]
        if ch == "\\" and i + 1 < n:
            out.append(ch)
            out.append(script_part[i + 1])
            i += 2
            continue
        if ch == "`":
            if stack and stack[-1] == "TEMPLATE":
                stack.pop()
            else:
                stack.append("TEMPLATE")
            out.append(ch)
            i += 1
            continue
        if stack and stack[-1] == "TEMPLATE" and ch == "{":
            out.append(DOLLAR + "{")
            stack.append("EXPR")
            brace_depth_stack.append(1)
            fixed_count += 1
            i += 1
            continue
        elif stack and stack[-1] == "EXPR":
            if ch == "{":
                brace_depth_stack[-1] += 1
            elif ch == "}":
                brace_depth_stack[-1] -= 1
                if brace_depth_stack[-1] == 0:
                    brace_depth_stack.pop()
                    stack.pop()
        out.append(ch)
        i += 1

    print(f"✓ Automate JS : {fixed_count} interpolations {DOLLAR}{{...}} restaurées sans conflit LaTeX.")
    return head + "".join(out)


def build_v5_3():
    # 0. Lecture idempotente depuis le commit initial 7843fb3
    raw_bytes = subprocess.check_output(["git", "show", "7843fb3:index.html"], cwd=ROOT)
    html = raw_bytes.decode("utf-8").replace("\r\n", "\n")

    # 1. Nettoyage intégral du LaTeX AVANT l'automate JS
    html = clean_latex_artifacts(html)

    # 2. Réparation des interpolations ${...}
    html = fix_all_template_literals_in_script(html)

    # 3. Remplacement des 10 anciens axes par les 7 axes de test v5.3 (2^7 = 128 configs, défaut = Config #1)
    v53_axes_js = """const CHASSIS_AXES_SPEC = [
      {
        key: 'P_Max',
        num: 1,
        label: '1. Topologie & Dotation Seuil Imprimé',
        defaultVal: 4,
        options: [
          { val: 4, text: 'P4_2233 : 4 parcelles [2,2,3,3] (10N Arbres · Standard)' },
          { val: 5, text: 'P5_22233 : 5 parcelles [2,2,2,3,3] (12N Arbres)' }
        ]
      },
      {
        key: 'Regle_Ouverture_Reve_Multiple',
        num: 2,
        label: '2. Ouverture multiple d’un Rêve (3.2)',
        defaultVal: 'UNIQUE_PAR_TOUR',
        options: [
          { val: 'UNIQUE_PAR_TOUR', text: 'Unique par tour (1 ouverture max/tour)' },
          { val: 'PAR_DE_M_DESIGNE', text: 'Cumulatif (1 ouverture par dé M désigné)' }
        ]
      },
      {
        key: 'Offset_Seuil_Parade',
        num: 3,
        label: '3. Décalage du Seuil de Parade',
        defaultVal: 0,
        options: [
          { val: 0, text: 'Offset 0 (Défense ≥ Seuil Imprimé modifié)' },
          { val: 1, text: 'Offset +1 (Exige +1 Défenseur de plus)' }
        ]
      },
      {
        key: 'Mise_En_Place_Tactiques',
        num: 4,
        label: '4. Mise en place Piste des Tactiques',
        defaultVal: 'ORDRE_FIXE_T1_T6',
        options: [
          { val: 'ORDRE_FIXE_T1_T6', text: 'Ordre croissant fixe T1 à T6 (Standard)' },
          { val: 'ALEATOIRE', text: 'Tirage aléatoire au départ' }
        ]
      },
      {
        key: 'Declenchement_Fin_De_Piste',
        num: 5,
        label: '5. Entrée en Siège T4',
        defaultVal: 'ARRIVEE_DERNIERE_PARCELLE',
        options: [
          { val: 'ARRIVEE_DERNIERE_PARCELLE', text: 'Dès présence sur la dernière parcelle intacte' },
          { val: 'DEPASSEMENT_DERNIERE_PARCELLE', text: 'Par dépassement de la dernière parcelle' }
        ]
      },
      {
        key: 'Role_Abatteuse_Fin_De_Piste',
        num: 6,
        label: '6. Rôle de l’Abatteuse en Siège T4',
        defaultVal: 'STANDARD_COUPE_ARBRE',
        options: [
          { val: 'STANDARD_COUPE_ARBRE', text: 'Standard (Coupe uniquement les Arbres)' },
          { val: 'ARRACHE_1_SOUCHE_SI_SANS_ARBRE', text: 'Arrache 1 Souche s’il n’y a plus d’Arbre' }
        ]
      },
      {
        key: 'Synergie_Binome_Machines',
        num: 7,
        label: '7. Puissance du binôme de machines',
        defaultVal: 'INDIVIDUELLE',
        options: [
          { val: 'INDIVIDUELLE', text: 'Individuelle (Propre à chaque machine)' },
          { val: 'MUTUALISATION_PUISSANCE_MEME_PARCELLE', text: 'Mutualisée sur une même parcelle' }
        ]
      }
    ];"""
    html = re.sub(
        r"const CHASSIS_AXES_SPEC\s*=\s*\[[\s\S]*?\];\s*(?=// -+\s*// 3\. CATALOGUE)",
        v53_axes_js + "\n\n    ",
        html, count=1
    )

    # 4. Ajustement des 5 tuiles modifiées en v5.3 (G5 A/B, G7 B, R3 B, R8 B)
    html = re.sub(
        r"(G5:\s*\{[\s\S]*?A:\s*\{[\s\S]*?texte:\s*')[^']*(')",
        r"\g<1><strong>Face 1 :</strong> Choisissez 1 parcelle ciblée contenant au moins 1 Souche : réduisez de <strong>−1</strong> son Seuil de Parade pour ce tour.<br><strong>Face 2 :</strong> Choisissez jusqu’à 2 parcelles ciblées contenant chacune au moins 1 Souche : réduisez de <strong>−1</strong> leur Seuil de Parade pour ce tour.\g<2>",
        html, count=1
    )
    html = re.sub(
        r"(G5:\s*\{[\s\S]*?B:\s*\{[\s\S]*?texte:\s*')[^']*(')",
        r"\g<1><strong>Face 1 (Loi 5) :</strong> Sur les rayons R et O, toute parcelle contenant au moins 1 Souche voit son Seuil de Parade réduit de <strong>−1</strong>.<br><strong>Face 2 (Loi 5) :</strong> Sur tout le plateau, toute parcelle contenant au moins 1 Souche voit son Seuil de Parade réduit de <strong>−1</strong>.\g<2>",
        html, count=1
    )
    html = re.sub(
        r"(G7:\s*\{[\s\S]*?B:\s*\{[\s\S]*?texte:\s*')[^']*(')",
        r"\g<1><strong>Loi 4.1 :</strong> Les binômes en Furtivité peuvent poser un Piège <strong>même sur une parcelle occupée par une machine</strong> (et ce Piège s’arme immédiatement si au moins 1 Défenseur du binôme glisse dessus ou soutient la parcelle).\g<2>",
        html, count=1
    )
    html = re.sub(
        r"(R3:\s*\{[\s\S]*?B:\s*\{[\s\S]*?texte:\s*')[^']*(')",
        r"\g<1><strong>Loi 3.1 :</strong> Lors d’une construction (G ou R), libérez <strong>1 seul des deux Défenseurs constructeurs</strong> vers une parcelle p=1 adjacente non rasée (ou <strong>les 2 constructeurs à N=3 joueurs</strong>).\g<2>",
        html, count=1
    )
    html = re.sub(
        r"(R8:\s*\{[\s\S]*?B:\s*\{[\s\S]*?texte:\s*')[^']*(')",
        r"\g<1><strong>Loi de terrassement (Sanctuarisation) :</strong> Sur les rayons E et R, les Bulldozers laissent <strong>1 Souche</strong> lors du terrassement <strong>uniquement si au moins 1 Défenseur ou 1 Insecte est présent sur la parcelle</strong>.\g<2>",
        html, count=1
    )

    # 5. Mise à jour complète de l'interface et du Livret Didactique en v5.3
    replacements = [
        ("Configurateur v5.2", "Configurateur v5.3"),
        ("v5.2 · Source Unique", "v5.3 · Source Unique"),
        ("Spécification Formelle (116 profils)", "Spécification Formelle (100 profils · Seuil Imprimé)"),
        ("Comparer v5.2 avec :", "Comparer v5.3 avec :"),
        ('<option value="v5.1" selected>v5.1 (86 profils, auto-parade)</option>',
         '<option value="v5.2" selected>v5.2 (116 profils, 2 options Pièges)</option>\n              <option value="v5.1">v5.1 (86 profils, auto-parade)</option>'),
        ("Configurer l'Instance (10 Axes & Peuples)", "Configurer l'Instance (7 Axes & Peuples)"),
        ("Les 10 Axes Paramétrables du Châssis (Produit Cartésien : 2 304 configs)",
         "Les 7 Axes de Test du Châssis v5.3 (Produit Cartésien : 128 configs)"),
        ("Réinitialiser les 10 axes au standard", "Réinitialiser les 7 axes au standard"),
        ("selon vos 10 axes et vos Peuples", "selon vos axes v5.3 et vos Peuples"),
        ("Socle Standard v5.2 (Profils A · Embuscade)", "Socle Standard v5.3 (Profils A · P4_2233)"),
        ('<option value="ESSAI_52_AMORTISSEUR">Bundle : ESSAI_52_AMORTISSEUR (15 subst. E)</option>', ""),
        ('<option value="52_CAPYBARA_E">Module N=3 : 52_CAPYBARA (M–H–I · Amortisseur E)</option>', ""),
        ('<option value="52_HARPIE_E">Module N=3 : 52_HARPIE (H–O–I · Amortisseur E)</option>', ""),
        ('<option value="52_DENDROBATE_E">Module N=3 : 52_DENDROBATE (R–E–I · Amortisseur E)</option>', ""),
        ("🧩 2. Explorateur (116 Profils)", "🧩 2. Explorateur (100 Profils)"),
        ("(32 Emplacements · 116 Profils A, B, C, D, E)", "(32 Emplacements · 100 Profils A, B, C, D)"),
        ("32 emplacements · 116 profils", "32 emplacements · 100 profils"),
        ('<option value="ALL_COMPARE">Comparer tous (A / B / C / D / E)</option>',
         '<option value="ALL_COMPARE">Comparer tous (A / B / C / D)</option>'),
        ('<option value="E">Profil E uniquement (15 Amortisseur)</option>', ""),
        ('<option value="B">Profil B (2 Insectes = 1 Gardien)</option>', ""),
        ("(sur 116)", "(sur 100)"),
        ('<option value="ALL">Toutes les évolutions (v4.3 → v5.2)</option>',
         '<option value="ALL">Toutes les évolutions (v4.3 → v5.3)</option>\n              <option value="v5.3">Nouveautés v5.3 uniquement (Seuil Imprimé, Fin 5.3, 100 profils)</option>'),
        ("schema_version: '5.2'", "schema_version: '5.3'"),
        ('`schema_version: "5.2"`', '`schema_version: "5.3"`'),
        ("configuration_index_2304:", "configuration_index_128:"),
        ("amazonia_instance_v5_2_", "amazonia_instance_v5_3_"),
        ("v4.3 → v4.9 → v5.0 → v5.1 → v5.2", "v4.3 → v4.9 → v5.0 → v5.1 → v5.2 → v5.3"),
        ("Données v5.2", "Données v5.3"),
        ("v5.2 (Consolidée)", "v5.3 (Consolidée)"),
        ("Règle Standard v5.2", "Règle Standard v5.3"),
        ("2 304", "128"),
        # Calculs exacts du capital d'arbres P4_2233 (10N) et P5_22233 (12N)
        ("const totalArbres = n * state.chassis.P_Max * state.chassis.Arbres_Par_Parcelle_Init;",
         "const totalArbres = n * (state.chassis.P_Max === 5 ? 12 : 10);"),
        ("const totalArbres = n * c.P_Max * c.Arbres_Par_Parcelle_Init;",
         "const totalArbres = n * (c.P_Max === 5 ? 12 : 10);"),
        ("capital_arbres_initial: state.peuplesCercle.length * state.chassis.P_Max * state.chassis.Arbres_Par_Parcelle_Init,",
         "topologie_code: state.chassis.P_Max === 5 ? 'P5_22233' : 'P4_2233',\n        capital_arbres_initial: state.peuplesCercle.length * (state.chassis.P_Max === 5 ? 12 : 10),"),
        (f"Capital : {DOLLAR}{{totalArbres}} Arbres ({DOLLAR}{{n}}×{DOLLAR}{{state.chassis.P_Max}}×{DOLLAR}{{state.chassis.Arbres_Par_Parcelle_Init}})",
         f"Capital : {DOLLAR}{{totalArbres}} Arbres ({DOLLAR}{{state.chassis.P_Max === 5 ? 'P5_22233 · 12×' + n : 'P4_2233 · 10×' + n}})"),
        (f"{DOLLAR}{{c.P_Max}} parcelles par rayon × {DOLLAR}{{c.Arbres_Par_Parcelle_Init}} Arbres = {DOLLAR}{{totalArbres}} Arbres debout",
         f"{DOLLAR}{{c.P_Max === 5 ? 'P5_22233 (5 parcelles : 2-2-2-3-3)' : 'P4_2233 (4 parcelles : 2-2-3-3)'}} = {DOLLAR}{{totalArbres}} Arbres debout"),
        (f"Posez <span class=\"dyn-span\">{DOLLAR}{{c.Arbres_Par_Parcelle_Init}} Arbres debout</span> sur chacune des <span class=\"dyn-span\">{DOLLAR}{{c.P_Max}} parcelles</span> de chaque piste Forêt (soit <span class=\"dyn-span\">{DOLLAR}{{totalArbres}} pions Arbre/Souche</span> au total).",
         f"Posez les Arbres debout selon la dotation et le <strong>Seuil Imprimé</strong> de la topologie <span class=\"dyn-span\">{DOLLAR}{{c.P_Max === 5 ? 'P5_22233 (p1=2, p2=2, p3=2, p4=3, p5=3)' : 'P4_2233 (p1=2, p2=2, p3=3, p4=3)'}}</span>, soit <span class=\"dyn-span\">{DOLLAR}{{totalArbres}} Arbres debout</span> au total."),
        # Règles du Livret Didactique v5.3
        ("Le chantier s'arrête dès que l'une des trois conditions suivantes est remplie :",
         "<strong>Vérification Unique en fin d'Étape 5.3</strong> (aucun arrêt immédiat en 3.1, 3.2 ou 4.x) — à la toute fin de 5.3, si l'une des 3 conditions suivantes est vraie, passez immédiatement à la Repousse Finale sans jouer l'Étape 6 :"),
        (f"<li><strong>Réveil de la Forêt (Arrêt par les Gardiens) :</strong> Immédiatement <span class=\"dyn-span\">{DOLLAR}{{texteSeuilGardiens}}</span>.</li>",
         f"<li><strong>Réveil de la Forêt (Synchronisation Active en fin de 5.3) :</strong> Au moins <span class=\"dyn-span\">{DOLLAR}{{n === 6 ? 5 : Math.max(3, Math.min(n, gardiensDispoCount))}} Gardiens sur la piste portent leur marqueur « utilisé »</span> (ont été ouverts ce tour-ci).</li>"),
        ("Pour un <strong>Gardien (G)</strong> ou un <strong>Rêve (R)</strong> : les 2 Défenseurs constructeurs restent sur l'emplacement en bordure de lisière jusqu'à la fin du tour.",
         f"Pour un <strong>Gardien (G)</strong> ou un <strong>Rêve (R)</strong> : les constructeurs restent en bordure de lisière <span class=\"dyn-span\">{DOLLAR}{{n === 3 ? '(Coup de pouce N=3 actif : 1 des 2 Défenseurs constructeurs rejoint gratuitement la parcelle p=1 adjacente non rasée !)' : '(à N=3 joueurs uniquement, 1 des 2 constructeurs rejoint gratuitement p=1)'}}</span>."),
        ("sur chaque parcelle en face qui est à la fois <strong>sans machine et non ciblée ce tour-ci</strong>",
         "sur chaque parcelle en face qui est <strong>sans machine physiquement présente</strong> (même si cette parcelle est ciblée à distance par T2/T3/T5/T6 ce tour-ci)"),
        (f"Seuil = max(1, (Arbres + Souches sur la parcelle){DOLLAR}{{c.Offset_Seuil_Parade === 1 ? ' + 1 (Offset)' : ''}} + Jetons Rouges{DOLLAR}{{c.Synergie_Binome_Machines === 'MUTUALISATION_PUISSANCE_MEME_PARCELLE' ? ' (mutualisés)' : ''}} − Jetons Bleus Surchauffe + Modificateur Tactique)",
         f"Seuil = max(1, Seuil_Imprimé(p) [{DOLLAR}{{c.P_Max === 5 ? '2,2,2,3,3' : '2,2,3,3'}}]{DOLLAR}{{c.Offset_Seuil_Parade === 1 ? ' + 1 (Offset)' : ''}} + Rouges{DOLLAR}{{c.Synergie_Binome_Machines === 'MUTUALISATION_PUISSANCE_MEME_PARCELLE' ? ' (mutualisés)' : ''}} − Bleus + Mod_Tactique + Mod_Tuiles)"),
        ("Retirez tous les jetons Piège qui se sont effectivement déclenchés ce tour-ci, ainsi que le maximum d'Insectes ayant été nécessaires à une Parade classique sur chaque parcelle.",
         "<strong>Verrouillage Étape 5 (Zéro dette d'Insectes) :</strong> Dès le début de l'Étape 5 et jusqu'à la fin de 5.3, les Insectes et Pièges situés sur des parcelles ciblées ne peuvent ni bouger ni payer de coût d'ouverture. En 5.3, retirez les Pièges déclenchés et les Insectes ayant servi en Parade classique."),
    ]
    for old, new in replacements:
        html = html.replace(old, new)

    # 6. Découplage propre : extraction des données dans data/amazonia_data_v5_3.js
    patch_v53_tail = """
// --- ÉPURATION CONSOLIDÉE v5.3 : 100 PROFILS & CHANGELOG v5.3 ---
Object.keys(CATALOGUE_TUILES).forEach(function(tId) {
  if (CATALOGUE_TUILES[tId].profils && CATALOGUE_TUILES[tId].profils.E) {
    delete CATALOGUE_TUILES[tId].profils.E;
  }
});
if (CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS && CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS.profils.B) {
  delete CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS.profils.B;
}

VERSION_CHANGELOG.unshift({
  version: 'v5.3',
  date: 'Version consolidée en vigueur',
  titre: 'Seuil Imprimé Fixe (P4_2233 / P5_22233), Fin de partie unique en 5.3, Embuscade unique (100 profils) & Zéro Dette d’Insectes',
  resume: 'Épuration cognitive majeure : le Seuil de Parade lit un Seuil Imprimé fixe par parcelle (sans jamais compter Arbres ni Souches). Suppression de l’Amortisseur et des 15 profils E (100 profils), vérification unique de fin de partie en fin de 5.3, pose furtive 4.1 autorisée sur parcelle ciblée, verrouillage des Insectes/Pièges sur parcelles ciblées en Étape 5, et bonus constructeur à N=3.',
  deltas: [
    {
      domaine: '1. Topologie & Formule du Seuil Imprimé',
      avant: 'v5.2 : P_Max (3,4,5) × Arbres (2,3) ; Seuil = Arbres + Souches + Rouges - Bleus + Mod_Tactique.',
      apres: 'v5.3 : P4_2233 (10N arbres, seuils [2,2,3,3]) ou P5_22233 (12N arbres, seuils [2,2,2,3,3]). Seuil = max(1, Seuil_Imprimé(p) + Rouges − Bleus + Mod_Tactique + Mod_Tuiles).'
    },
    {
      domaine: '2. Vérification Unique de Fin de Partie (Fin de 5.3)',
      avant: 'v5.2 : Arrêts immédiats en 3.1, 3.2 et 4.x ; Réveil passif à N Gardiens.',
      apres: 'v5.3 : Vérification unique en fin de 5.3 : 1) Sommeil (Rêve au Rang 1), 2) Réveil par Synchronisation Active (min(N, Gardiens dispo) avec min 3, ou 5 à 6J, portent leur marqueur utilisé ce tour), 3) Fin du Tour 8 → Repousse Finale directe sans Étape 6.'
    },
    {
      domaine: '3. Embuscade Unique, Furtivité 4.1 & Verrouillage Étape 5',
      avant: 'v5.2 : 2 options de Pièges (+15 profils E), pose 4.1 interdite sur parcelle ciblée, suivi de dette INSECTES_ENGAGES.',
      apres: 'v5.3 : Embuscade Assistée unique (retrait des 15 profils E). Pose 4.1 autorisée sur parcelle ciblée tant qu’aucune machine n’y est présente. En Étape 5, Insectes et Pièges sur parcelles ciblées verrouillés jusqu’en fin de 5.3.'
    },
    {
      domaine: '4. Bonus N=3 & Ajustements Tuiles (G5, G7 B, R3 B, R8 B, Colonie)',
      avant: 'v5.2 : 2 constructeurs bloqués en lisière à 3J ; Colonisation B actif.',
      apres: 'v5.3 : À N=3, 1 des 2 constructeurs (G ou R) rejoint gratuitement p=1 en 3.1. Retrait de Colonisation B. Ajustements de G5 A/B (−1 Seuil si ≥ 1 Souche), G7 B (pose sous machine), R3 B (1 constructeur libéré, 2 à N=3) et R8 B (exige Défenseur ou Insecte présent).'
    }
  ]
});
"""

    m_script_open = html.rfind("<script>")
    m_state = html.find("// 5. ÉTAT RÉACTIF DE L'INSTANCE EN COURS")
    if m_script_open == -1 or m_state == -1:
        raise RuntimeError("Marqueurs de découplage introuvables dans index.html")

    data_content = html[m_script_open + len("<script>"):m_state].strip() + "\n" + patch_v53_tail
    DATA_DIR.mkdir(exist_ok=True)
    DATA_JS_PATH.write_text(data_content, encoding="utf-8")

    # Remplacer le bloc de données dans index.html par le chargement externe propre
    decoupled_html = (
        html[:m_script_open]
        + '<script src="data/amazonia_data_v5_3.js"></script>\n  <script>\n    '
        + html[m_state:]
    )
    INDEX_PATH.write_text(decoupled_html, encoding="utf-8")

    print(f"✓ Données découplées : {DATA_JS_PATH.relative_to(ROOT)} ({len(data_content.splitlines())} lignes)")
    print(f"✓ Interface allégée : {INDEX_PATH.relative_to(ROOT)} ({len(decoupled_html.splitlines())} lignes)")
    print("✓ Prêt ! Fais Ctrl+F5 sur http://localhost:8000/")


if __name__ == "__main__":
    build_v5_3()