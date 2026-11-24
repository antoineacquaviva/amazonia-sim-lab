/* ============================================================================
 * Amazonia Doc Studio — Illustrations SVG des 30 tuiles & Icône Reptile (v6.2)
 * Module vanilla JS autonome (UTF-8 sans BOM, LF, 100 % file:// & HTTPS).
 * ============================================================================ */
(function (global) {
  'use strict';

  const VERSION = '6.2.0';

  // --------------------------------------------------------------------------
  // Mini-icône Reptile SVG nette (14x14 par défaut, viewBox="0 0 24 24")
  // Silhouette franche de tête de caïman vert émeraude, lisible dès 14 px.
  // --------------------------------------------------------------------------
  const REPTILE_ICON_VIEWBOX = '0 0 24 24';
  const REPTILE_ICON_INNER_SVG =
    '<path d="M1.8 14.4L4.2 9.4L6.8 6.4L9.2 7.5L11.3 5.5L13.5 8.1L21.5 9.6C22.4 9.8 22.6 11.7 21.6 12.2L13.2 13L20.8 15.2C21.2 16.2 20.1 17.6 18.2 18.1C12.8 19.3 6.8 19.3 1.8 17.6Z" fill="#10b981" stroke="#064e3b" stroke-width="1.5" stroke-linejoin="round"/>' +
    '<path d="M12.8 12.9L21 12.3L20.2 15.1L12.8 12.9Z" fill="#064e3b"/>' +
    '<path d="M14.2 12.7L15.4 14.8L16.6 12.5M17.5 12.4L18.7 14.5L19.9 12.2" fill="#ffffff" stroke="#064e3b" stroke-width="0.7" stroke-linejoin="round"/>' +
    '<path d="M3.8 16.5C8.2 17.6 13.4 17.6 18 16.5" fill="none" stroke="#a7f3d0" stroke-width="1.2" stroke-linecap="round"/>' +
    '<circle cx="9.6" cy="9.9" r="2.3" fill="#fbbf24" stroke="#064e3b" stroke-width="1.1"/>' +
    '<ellipse cx="9.8" cy="9.9" rx="0.65" ry="1.5" fill="#064e3b"/>' +
    '<circle cx="19.6" cy="10.4" r="0.9" fill="#064e3b"/>';

  function getReptileIconSvg(size) {
    const px = Number(size) > 0 ? Number(size) : 14;
    return (
      '<svg xmlns="http://www.w3.org/2000/svg" class="exp-peuple-icon-svg exp-peuple-icon-R" ' +
      'data-peuple-icon="R" width="' + px + '" height="' + px + '" ' +
      'viewBox="' + REPTILE_ICON_VIEWBOX + '" role="img" aria-label="Reptiles" focusable="false">' +
      REPTILE_ICON_INNER_SVG +
      '</svg>'
    );
  }

  function getReptileWheelIconSvg(cx, cy, size) {
    const px = Number(size) > 0 ? Number(size) : 20;
    const x = (Number(cx) - px / 2).toFixed(1);
    const y = (Number(cy) - px - 6).toFixed(1);
    return (
      '<svg class="exp-wheel-peuple-icon exp-peuple-icon-R" data-peuple-icon="R" ' +
      'x="' + x + '" y="' + y + '" width="' + px + '" height="' + px + '" ' +
      'viewBox="' + REPTILE_ICON_VIEWBOX + '" aria-hidden="true">' +
      REPTILE_ICON_INNER_SVG +
      '</svg>'
    );
  }

  const REPTILE_ICON_SVG = getReptileIconSvg(14);

  // --------------------------------------------------------------------------
  // Cadres & fonds harmonisés par famille / Peuple d'origine (64x64)
  // --------------------------------------------------------------------------
  const BACKDROPS = {
    M:
      '<rect x="1.5" y="1.5" width="61" height="61" rx="12" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>' +
      '<circle cx="32" cy="32" r="23.5" fill="#fde68a" opacity="0.55"/>',
    R:
      '<rect x="1.5" y="1.5" width="61" height="61" rx="12" fill="#d1fae5" stroke="#10b981" stroke-width="2"/>' +
      '<circle cx="32" cy="32" r="23.5" fill="#a7f3d0" opacity="0.55"/>',
    O:
      '<rect x="1.5" y="1.5" width="61" height="61" rx="12" fill="#e0f2fe" stroke="#0ea5e9" stroke-width="2"/>' +
      '<circle cx="32" cy="32" r="23.5" fill="#bae6fd" opacity="0.55"/>',
    I:
      '<rect x="1.5" y="1.5" width="61" height="61" rx="12" fill="#ecfccb" stroke="#84cc16" stroke-width="2"/>' +
      '<circle cx="32" cy="32" r="23.5" fill="#d9f99d" opacity="0.58"/>',
    RH:
      '<rect x="1.5" y="1.5" width="61" height="61" rx="12" fill="#1e1b4b" stroke="#f43f5e" stroke-width="2"/>' +
      '<circle cx="32" cy="32" r="23" fill="#312e81"/>' +
      '<circle cx="32" cy="32" r="16.5" fill="#4f46e5" opacity="0.45"/>' +
      '<circle cx="11" cy="11" r="1.2" fill="#fde68a" opacity="0.9"/>' +
      '<circle cx="53" cy="12" r="1" fill="#fbcfe8" opacity="0.85"/>' +
      '<circle cx="12" cy="52" r="0.95" fill="#e0e7ff" opacity="0.8"/>' +
      '<circle cx="52" cy="51" r="1.15" fill="#fde68a" opacity="0.85"/>',
    RE:
      '<rect x="1.5" y="1.5" width="61" height="61" rx="12" fill="#1e1b4b" stroke="#8b5cf6" stroke-width="2"/>' +
      '<circle cx="32" cy="32" r="23" fill="#312e81"/>' +
      '<circle cx="32" cy="32" r="16.5" fill="#6d28d9" opacity="0.45"/>' +
      '<circle cx="11" cy="11" r="1.2" fill="#fde68a" opacity="0.9"/>' +
      '<circle cx="53" cy="12" r="1" fill="#c4b5fd" opacity="0.85"/>' +
      '<circle cx="12" cy="52" r="0.95" fill="#e0e7ff" opacity="0.8"/>' +
      '<circle cx="52" cy="51" r="1.15" fill="#fde68a" opacity="0.85"/>'
  };

  function wrapMedallion(tileId, label, backdropKey, artworkSvg) {
    return (
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="56" height="56" ' +
      'class="exp-tile-svg exp-tile-svg-' + tileId + '" data-svg-tile="' + tileId + '" ' +
      'role="img" aria-label="' + label + '" focusable="false">' +
      (BACKDROPS[backdropKey] || BACKDROPS.M) +
      artworkSvg +
      '</svg>'
    );
  }

  // --------------------------------------------------------------------------
  // 30 médaillons d'identification SVG (15 Gardiens, 10 Rêves, 5 Nids)
  // --------------------------------------------------------------------------
  const TILE_ILLUSTRATIONS_V62 = {
    // === 15 GARDIENS (G1..G15) ===

    // G1 — Le Bond du Jaguar (M>R) : tête de jaguar doré aux rosettes sombres
    G1: wrapMedallion(
      'G1',
      'Le Bond du Jaguar',
      'M',
      '<circle cx="17" cy="18" r="6.5" fill="#d97706" stroke="#451a03" stroke-width="1.8"/>' +
      '<circle cx="17" cy="18" r="3" fill="#451a03"/>' +
      '<circle cx="47" cy="18" r="6.5" fill="#d97706" stroke="#451a03" stroke-width="1.8"/>' +
      '<circle cx="47" cy="18" r="3" fill="#451a03"/>' +
      '<path d="M13 31C13 19 21 13 32 13C43 13 51 19 51 31C51 42 44 51 32 52C20 51 13 42 13 31Z" fill="#f59e0b" stroke="#451a03" stroke-width="1.9" stroke-linejoin="round"/>' +
      '<path d="M21 38C21 33 26 31 32 31C38 31 43 33 43 38C43 44 38 49 32 49C26 49 21 44 21 38Z" fill="#fef3c7" stroke="#451a03" stroke-width="1.3"/>' +
      '<path d="M27.5 36.5L36.5 36.5L32 41.5Z" fill="#451a03"/>' +
      '<path d="M32 41.5V45M28 45.5Q32 48 36 45.5" fill="none" stroke="#451a03" stroke-width="1.7" stroke-linecap="round"/>' +
      '<path d="M20 28L28 29.5L23.5 32Z" fill="#fef08a" stroke="#451a03" stroke-width="1.3" stroke-linejoin="round"/>' +
      '<path d="M44 28L36 29.5L40.5 32Z" fill="#fef08a" stroke="#451a03" stroke-width="1.3" stroke-linejoin="round"/>' +
      '<circle cx="24" cy="29.6" r="1.2" fill="#451a03"/>' +
      '<circle cx="40" cy="29.6" r="1.2" fill="#451a03"/>' +
      '<circle cx="32" cy="21" r="2.7" fill="none" stroke="#451a03" stroke-width="1.6" stroke-dasharray="5 2"/>' +
      '<circle cx="32" cy="21" r="1" fill="#451a03"/>' +
      '<circle cx="22.5" cy="21.5" r="2.3" fill="none" stroke="#451a03" stroke-width="1.5" stroke-dasharray="4 2"/>' +
      '<circle cx="41.5" cy="21.5" r="2.3" fill="none" stroke="#451a03" stroke-width="1.5" stroke-dasharray="4 2"/>' +
      '<circle cx="17.5" cy="35" r="2.1" fill="#451a03"/>' +
      '<circle cx="46.5" cy="35" r="2.1" fill="#451a03"/>' +
      '<circle cx="25.5" cy="41.5" r="1" fill="#451a03"/>' +
      '<circle cx="38.5" cy="41.5" r="1" fill="#451a03"/>'
    ),

    // G2 — L'Étreinte de l'Anaconda (R>M) : grand anaconda vert enroulé en spirale
    G2: wrapMedallion(
      'G2',
      'L’Étreinte de l’Anaconda',
      'R',
      '<path d="M48 47C55 37 54 22 44 15C33 8 17 12 12 24C7 37 15 51 29 53C41 54 49 45 47 34C45 24 35 19 26 23C19 26 18 35 24 41C29 45 36 43 37 37" fill="none" stroke="#064e3b" stroke-width="9" stroke-linecap="round"/>' +
      '<path d="M48 47C55 37 54 22 44 15C33 8 17 12 12 24C7 37 15 51 29 53C41 54 49 45 47 34C45 24 35 19 26 23C19 26 18 35 24 41C29 45 36 43 37 37" fill="none" stroke="#16a34a" stroke-width="6" stroke-linecap="round"/>' +
      '<ellipse cx="43" cy="15" rx="2.4" ry="1.6" transform="rotate(32 43 15)" fill="#052e16"/>' +
      '<ellipse cx="26" cy="12" rx="2.5" ry="1.6" transform="rotate(-18 26 12)" fill="#052e16"/>' +
      '<ellipse cx="12" cy="26" rx="2.4" ry="1.6" transform="rotate(-82 12 26)" fill="#052e16"/>' +
      '<ellipse cx="18" cy="46" rx="2.5" ry="1.6" transform="rotate(38 18 46)" fill="#052e16"/>' +
      '<ellipse cx="38" cy="51" rx="2.5" ry="1.6" transform="rotate(-18 38 51)" fill="#052e16"/>' +
      '<ellipse cx="47" cy="34" rx="2.3" ry="1.5" transform="rotate(84 47 34)" fill="#052e16"/>' +
      '<path d="M24 31L31 25C36 25 40 29 38 35C35 39 27 38 24 34Z" fill="#15803d" stroke="#064e3b" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M29 29L36 30" stroke="#052e16" stroke-width="1.4" stroke-linecap="round"/>' +
      '<circle cx="29.2" cy="30.5" r="1.5" fill="#fbbf24" stroke="#052e16" stroke-width="0.6"/>' +
      '<circle cx="29.2" cy="30.5" r="0.6" fill="#052e16"/>' +
      '<path d="M24 33L18.5 34.5M18.5 34.5L16.3 32.8M18.5 34.5L16.7 36.6" fill="none" stroke="#dc2626" stroke-width="1.4" stroke-linecap="round"/>'
    ),

    // G3 — La Voltige de l'Atèle (M>O) : singe-araignée noir/brun suspendu par sa longue queue à une liane
    G3: wrapMedallion(
      'G3',
      'La Voltige de l’Atèle',
      'M',
      '<path d="M5 15Q31 7 59 16" fill="none" stroke="#15803d" stroke-width="3.4" stroke-linecap="round"/>' +
      '<path d="M14 13C10 7 17 6 19 11Z" fill="#22c55e" stroke="#14532d" stroke-width="1"/>' +
      '<path d="M48 13C51 7 57 9 54 14Z" fill="#22c55e" stroke="#14532d" stroke-width="1"/>' +
      '<path d="M36 11C39 6 44 9 41 14C38 19 34 22 33 28" fill="none" stroke="#1c1917" stroke-width="3" stroke-linecap="round"/>' +
      '<ellipse cx="31" cy="35" rx="6.5" ry="8.8" transform="rotate(-14 31 35)" fill="#292524" stroke="#0c0a09" stroke-width="1.6"/>' +
      '<circle cx="20.5" cy="43.5" r="2.2" fill="#292524"/>' +
      '<circle cx="31.5" cy="45.5" r="2.2" fill="#292524"/>' +
      '<circle cx="26" cy="44.5" r="5.6" fill="#292524" stroke="#0c0a09" stroke-width="1.6"/>' +
      '<ellipse cx="25.5" cy="45.5" rx="3.4" ry="2.7" fill="#e7e5e4"/>' +
      '<circle cx="24.1" cy="44.9" r="0.95" fill="#0c0a09"/>' +
      '<circle cx="26.9" cy="45.1" r="0.95" fill="#0c0a09"/>' +
      '<path d="M35 32Q45 26 50 17" fill="none" stroke="#1c1917" stroke-width="3" stroke-linecap="round"/>' +
      '<path d="M27 32Q18 27 12 34" fill="none" stroke="#1c1917" stroke-width="3" stroke-linecap="round"/>' +
      '<path d="M34 41Q43 45 48 53" fill="none" stroke="#1c1917" stroke-width="3" stroke-linecap="round"/>' +
      '<path d="M23 41Q16 47 13 53" fill="none" stroke="#1c1917" stroke-width="2.8" stroke-linecap="round"/>'
    ),

    // G4 — Le Cri d'Alarme de l'Ara (O>M) : profil d'ara rouge/bleu à grand bec courbé
    G4: wrapMedallion(
      'G4',
      'Le Cri d’Alarme de l’Ara',
      'O',
      '<path d="M13 55C14 40 16 24 23 16C28 11 38 11 43 17C44 22 41 28 37 32C35 40 31 49 27 55Z" fill="#dc2626" stroke="#7f1d1d" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M14 55C16 45 20 39 27 37C26 44 23 50 19 55Z" fill="#2563eb" stroke="#1e3a8a" stroke-width="1.5" stroke-linejoin="round"/>' +
      '<path d="M18 39C21 35 26 34 31 35C29 38 25 40 19 41Z" fill="#facc15" stroke="#854d0e" stroke-width="1.2"/>' +
      '<path d="M28 20C32 17 38 18 40 23C38 28 32 29 28 26Z" fill="#ffffff" stroke="#7f1d1d" stroke-width="1.1"/>' +
      '<circle cx="33.5" cy="22.5" r="2.2" fill="#facc15" stroke="#0f172a" stroke-width="1"/>' +
      '<circle cx="33.8" cy="22.5" r="1.1" fill="#0f172a"/>' +
      '<path d="M40 16C48 16 53 21 52 30C49 27 45 25 40 25Z" fill="#fef3c7" stroke="#451a03" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M40 25C44 25 47 27 46 31C42 32 39 30 38 27Z" fill="#1e293b" stroke="#0f172a" stroke-width="1.4" stroke-linejoin="round"/>' +
      '<path d="M53 16Q57 19 55 24" fill="none" stroke="#0284c7" stroke-width="1.8" stroke-linecap="round"/>' +
      '<path d="M56 13Q61 18 58 26" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-linecap="round" opacity="0.75"/>'
    ),

    // G5 — Le Coup de Queue de l'Iguane (R>O) : iguane vert à crête dorsale et queue en fouet
    G5: wrapMedallion(
      'G5',
      'Le Coup de Queue de l’Iguane',
      'R',
      '<path d="M24 38C30 48 44 53 53 45C58 40 57 31 51 27C47 24 44 26 45 30" fill="none" stroke="#064e3b" stroke-width="5.6" stroke-linecap="round"/>' +
      '<path d="M24 38C30 48 44 53 53 45C58 40 57 31 51 27C47 24 44 26 45 30" fill="none" stroke="#22c55e" stroke-width="3.4" stroke-linecap="round"/>' +
      '<path d="M35 48L37 44M45 50L44 46M54 43L51 41M56 34L52 35" stroke="#064e3b" stroke-width="1.8" stroke-linecap="round"/>' +
      '<path d="M16 17L19 13L21 17L24 14L25 19L29 17L29 22L33 22L32 27L36 28L34 32" fill="#4ade80" stroke="#064e3b" stroke-width="1.2" stroke-linejoin="round"/>' +
      '<path d="M10 23C12 18 18 16 24 19C30 22 35 30 33 39C31 44 24 45 20 40C17 36 17 31 15 28C11 28 9 26 10 23Z" fill="#16a34a" stroke="#064e3b" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M12 27C11 32 14 35 17 34" fill="#4ade80" stroke="#064e3b" stroke-width="1.3" stroke-linejoin="round"/>' +
      '<circle cx="17" cy="23.5" r="2" fill="#fde047" stroke="#064e3b" stroke-width="1"/>' +
      '<circle cx="17" cy="23.5" r="0.8" fill="#064e3b"/>' +
      '<circle cx="21.5" cy="27.5" r="1.9" fill="#86efac" stroke="#064e3b" stroke-width="0.9"/>' +
      '<path d="M22 41L16 48M16 48L13 48M16 48L16 51" fill="none" stroke="#064e3b" stroke-width="1.8" stroke-linecap="round"/>' +
      '<path d="M41 21Q48 18 54 22" fill="none" stroke="#047857" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="3 2"/>'
    ),

    // G6 — Le Bec du Toucan (O>R) : toucan toco noir à grand bec jaune-orange vif
    G6: wrapMedallion(
      'G6',
      'Le Bec du Toucan',
      'O',
      '<path d="M12 54C11 40 13 24 20 17C24 13 31 14 33 20C35 28 32 42 29 54Z" fill="#0f172a" stroke="#020617" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M21 20C27 19 32 22 32 30C32 36 27 40 21 39C18 35 18 25 21 20Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>' +
      '<path d="M20 39Q26 42 30 37" fill="none" stroke="#f97316" stroke-width="2" stroke-linecap="round"/>' +
      '<circle cx="25.5" cy="24.5" r="3" fill="#38bdf8" stroke="#0c4a6e" stroke-width="1"/>' +
      '<circle cx="25.8" cy="24.5" r="1.4" fill="#0f172a"/>' +
      '<circle cx="26.2" cy="24" r="0.5" fill="#ffffff"/>' +
      '<path d="M31 18C42 16 53 20 56 29C50 32 39 32 31 30Z" fill="#facc15" stroke="#78350f" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M31 23C41 22 50 24 55 29C49 32 39 32 31 30Z" fill="#f97316" opacity="0.88"/>' +
      '<path d="M51 22.5C54.5 24.5 56 27 56 29C53.5 30.2 51 30.4 49.5 29.5C49.5 26.5 50 24 51 22.5Z" fill="#0f172a"/>' +
      '<path d="M31 27.5Q43 27.5 52 29.5" fill="none" stroke="#78350f" stroke-width="1.3"/>'
    ),

    // G7 — Le Sentier du Tapir (M>H) : profil de tapir brun-gris à museau en trompe
    G7: wrapMedallion(
      'G7',
      'Le Sentier du Tapir',
      'M',
      '<path d="M10 51Q32 47 54 52" fill="none" stroke="#b45309" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="5 3"/>' +
      '<path d="M14 38C12 28 19 20 30 20C38 20 44 22 48 27C52 29 55 32 54 37C53 39 50 39 49 36C48 34 46 34 44 35L42 40L43 49H38L37 41H25L24 49H19L20 41L15 48H11Z" fill="#57534e" stroke="#1c1917" stroke-width="1.8" stroke-linejoin="round"/>' +
      '<path d="M35 20Q41 20 45 24" fill="none" stroke="#292524" stroke-width="2.6" stroke-linecap="round"/>' +
      '<ellipse cx="39" cy="21" rx="2.6" ry="3.8" transform="rotate(-18 39 21)" fill="#44403c" stroke="#f5f5f4" stroke-width="1.5"/>' +
      '<circle cx="44.5" cy="28.5" r="1.4" fill="#1c1917"/>' +
      '<circle cx="44.9" cy="28.1" r="0.45" fill="#fafaf9"/>' +
      '<path d="M18 28Q28 24 37 26" fill="none" stroke="#78716c" stroke-width="1.6" stroke-linecap="round"/>'
    ),

    // G8 — Le Mirage du Boto (M>E) : dauphin rose d'Amazonie bondissant au-dessus d'une vague
    G8: wrapMedallion(
      'G8',
      'Le Mirage du Boto',
      'M',
      '<path d="M13 38C15 24 25 14 37 16C44 17 48 22 49 27L55 31C56 32 55 34 53 34L45 31C41 26 35 24 29 26C24 28 21 33 19 39L14 43L10 39Z" fill="#f472b6" stroke="#831843" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M22 33C26 26 35 23 44 28C39 29 33 29 26 35Z" fill="#fbcfe8"/>' +
      '<path d="M30 28L25 35L32 33Z" fill="#ec4899" stroke="#831843" stroke-width="1.3" stroke-linejoin="round"/>' +
      '<circle cx="44.5" cy="24.5" r="1.3" fill="#831843"/>' +
      '<path d="M6 46Q15 39 24 45T42 45T58 45V54Q58 58 54 58H10Q6 58 6 54Z" fill="#0284c7" opacity="0.88"/>' +
      '<path d="M8 45Q16 39 24 44T40 44T56 44" fill="none" stroke="#bae6fd" stroke-width="2" stroke-linecap="round"/>' +
      '<circle cx="19" cy="18" r="1.6" fill="#38bdf8"/>' +
      '<circle cx="52" cy="21" r="1.4" fill="#38bdf8"/>' +
      '<circle cx="48" cy="39" r="1.5" fill="#7dd3fc"/>'
    ),

    // G9 — Le Guet du Caïman noir (R>H) : tête de caïman sombre affleurant l'eau, yeux dorés
    G9: wrapMedallion(
      'G9',
      'Le Guet du Caïman noir',
      'R',
      '<path d="M6 40H58V54Q58 58 54 58H10Q6 58 6 54Z" fill="#0369a1" opacity="0.82"/>' +
      '<path d="M10 41C11 32 16 25 22 24C24 19 28 18 30 23H34C36 18 40 19 42 24C48 25 53 32 54 41Z" fill="#1e293b" stroke="#020617" stroke-width="1.8" stroke-linejoin="round"/>' +
      '<path d="M17 39C20 31 25 28 32 28C39 28 44 31 47 39Z" fill="#334155"/>' +
      '<circle cx="25.5" cy="24.5" r="4" fill="#fbbf24" stroke="#020617" stroke-width="1.4"/>' +
      '<ellipse cx="25.5" cy="24.5" rx="1.05" ry="2.7" fill="#020617"/>' +
      '<circle cx="38.5" cy="24.5" r="4" fill="#fbbf24" stroke="#020617" stroke-width="1.4"/>' +
      '<ellipse cx="38.5" cy="24.5" rx="1.05" ry="2.7" fill="#020617"/>' +
      '<circle cx="27" cy="35" r="1.4" fill="#020617"/>' +
      '<circle cx="37" cy="35" r="1.4" fill="#020617"/>' +
      '<path d="M8 41Q20 38.5 32 41T56 41" fill="none" stroke="#bae6fd" stroke-width="2" stroke-linecap="round"/>' +
      '<path d="M13 47H27M36 47H51M20 52H44" fill="none" stroke="#7dd3fc" stroke-width="1.6" stroke-linecap="round"/>'
    ),

    // G10 — L'Affût de la Matamata (R>E) : tortue matamata à carapace crénelée et tête triangulaire
    G10: wrapMedallion(
      'G10',
      'L’Affût de la Matamata',
      'R',
      '<path d="M17 31L10 27L13 36M47 31L54 27L51 36M20 49L14 55L23 53M44 49L50 55L41 53" fill="#4d7c0f" stroke="#1a2e05" stroke-width="1.5" stroke-linejoin="round"/>' +
      '<path d="M32 23L38 25L44 28L47 35L45 43L40 50L32 53L24 50L19 43L17 35L20 28L26 25Z" fill="#854d0e" stroke="#422006" stroke-width="1.8" stroke-linejoin="round"/>' +
      '<polygon points="32,27 37,33 32,37 27,33" fill="#ca8a04" stroke="#422006" stroke-width="1.2"/>' +
      '<polygon points="32,38 37,43 32,48 27,43" fill="#ca8a04" stroke="#422006" stroke-width="1.2"/>' +
      '<polygon points="22,34 26,37 22,42 19,38" fill="#a16207" stroke="#422006" stroke-width="1.1"/>' +
      '<polygon points="42,34 45,38 42,42 38,37" fill="#a16207" stroke="#422006" stroke-width="1.1"/>' +
      '<path d="M29 24V19H35V24" fill="#713f12" stroke="#422006" stroke-width="1.4"/>' +
      '<polygon points="32,8 43,19 36,21 28,21 21,19" fill="#a16207" stroke="#422006" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<circle cx="29.5" cy="14.5" r="1.1" fill="#fef08a"/>' +
      '<circle cx="34.5" cy="14.5" r="1.1" fill="#fef08a"/>' +
      '<path d="M32 8V6" stroke="#422006" stroke-width="1.8" stroke-linecap="round"/>'
    ),

    // G11 — Le Piqué de la Harpie (O>H) : harpie féroce en piqué avec sa double huppe emblématique
    G11: wrapMedallion(
      'G11',
      'Le Piqué de la Harpie',
      'O',
      '<path d="M32 34L8 14C9 26 14 34 23 39L32 45L41 39C50 34 55 26 56 14Z" fill="#334155" stroke="#0f172a" stroke-width="1.8" stroke-linejoin="round"/>' +
      '<path d="M13 21L24 31M16 28L25 35M51 21L40 31M48 28L39 35" stroke="#94a3b8" stroke-width="1.4" stroke-linecap="round"/>' +
      '<path d="M25 27L21 12L28 19L32 16L36 19L43 12L39 27Z" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.6" stroke-linejoin="round"/>' +
      '<path d="M21 12L25 18L28 19M43 12L39 18L36 19" fill="#1e293b"/>' +
      '<ellipse cx="32" cy="34" rx="7.5" ry="10.5" fill="#f8fafc" stroke="#0f172a" stroke-width="1.6"/>' +
      '<path d="M25.5 31Q32 35 38.5 31" fill="none" stroke="#0f172a" stroke-width="3.2"/>' +
      '<circle cx="29" cy="24.5" r="1.4" fill="#0f172a"/>' +
      '<circle cx="35" cy="24.5" r="1.4" fill="#0f172a"/>' +
      '<polygon points="29.5,26 34.5,26 32,32" fill="#f59e0b" stroke="#0f172a" stroke-width="1.2" stroke-linejoin="round"/>' +
      '<path d="M27 45L24 53M28 45L28 54M37 45L40 53M36 45L36 54" fill="none" stroke="#eab308" stroke-width="2" stroke-linecap="round"/>'
    ),

    // G12 — Le Chant de l'Ibijau (O>E) : oiseau fantôme perché sur une branche, grands yeux dorés sous un croissant
    G12: wrapMedallion(
      'G12',
      'Le Chant de l’Ibijau',
      'O',
      '<circle cx="32" cy="28" r="21" fill="#1e3a5f" opacity="0.16"/>' +
      '<path d="M47 11A6.5 6.5 0 1 0 53 19A5 5 0 1 1 47 11Z" fill="#f59e0b" stroke="#78350f" stroke-width="1.1"/>' +
      '<path d="M8 50Q30 44 56 49" fill="none" stroke="#78350f" stroke-width="4.2" stroke-linecap="round"/>' +
      '<path d="M21 47C20 35 21 20 31 19C41 20 42 35 41 47Z" fill="#64748b" stroke="#1e293b" stroke-width="1.8" stroke-linejoin="round"/>' +
      '<path d="M25 36V45M31 37V46M37 36V45" stroke="#334155" stroke-width="1.6" stroke-linecap="round"/>' +
      '<circle cx="26.5" cy="27.5" r="4.6" fill="#facc15" stroke="#1e293b" stroke-width="1.5"/>' +
      '<circle cx="26.5" cy="27.5" r="2.2" fill="#0f172a"/>' +
      '<circle cx="27.4" cy="26.4" r="0.8" fill="#ffffff"/>' +
      '<circle cx="35.5" cy="27.5" r="4.6" fill="#facc15" stroke="#1e293b" stroke-width="1.5"/>' +
      '<circle cx="35.5" cy="27.5" r="2.2" fill="#0f172a"/>' +
      '<circle cx="36.4" cy="26.4" r="0.8" fill="#ffffff"/>' +
      '<polygon points="29.5,31.5 32.5,31.5 31,34.5" fill="#1e293b"/>'
    ),

    // G13 — La Langue du Tamanoir (M>I) : tamanoir à long museau effilé, bande noire et queue en panache
    G13: wrapMedallion(
      'G13',
      'La Langue du Tamanoir',
      'M',
      '<path d="M7 42C6 29 14 21 24 23C21 31 20 39 17 47C12 47 8 45 7 42Z" fill="#44403c" stroke="#1c1917" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M10 34L19 29M9 39L18 35M11 43L17 41" stroke="#78716c" stroke-width="1.3" stroke-linecap="round"/>' +
      '<path d="M21 34C21 25 27 21 36 22C42 23 47 26 54 31C55 32 54 34 52 34L42 33L42 46H37L36 38H27L26 46H21Z" fill="#78716c" stroke="#1c1917" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M26 36L35 23L41 25L33 38Z" fill="#1c1917" stroke="#fafaf9" stroke-width="1.3" stroke-linejoin="round"/>' +
      '<circle cx="40.5" cy="24.5" r="2.1" fill="#57534e" stroke="#1c1917" stroke-width="1.2"/>' +
      '<circle cx="44.2" cy="28.2" r="1.2" fill="#1c1917"/>' +
      '<path d="M53.5 32.5Q58 33 57 37.5Q56 40 53 39" fill="none" stroke="#f43f5e" stroke-width="2" stroke-linecap="round"/>'
    ),

    // G14 — Le Terrier du Téju (R>I) : lézard téju noir et blanc près d'un terrier
    G14: wrapMedallion(
      'G14',
      'Le Terrier du Téju',
      'R',
      '<path d="M8 33C10 19 20 13 31 14C39 15 44 21 46 31H8Z" fill="#a16207" stroke="#451a03" stroke-width="1.6" stroke-linejoin="round"/>' +
      '<path d="M15 31C16 22 22 19 28 20C33 21 36 25 36 31Z" fill="#1c1917"/>' +
      '<path d="M10 49C14 53 22 52 27 46C31 41 37 39 43 40C48 41 53 39 56 36C51 32 45 31 38 33C31 35 25 39 20 45C17 48 13 49 10 49Z" fill="#0f172a" stroke="#020617" stroke-width="1.6" stroke-linejoin="round"/>' +
      '<path d="M27 38L29 43M33 35L35 41M39 33L40 40M45 33L45 39" stroke="#f8fafc" stroke-width="2.2" stroke-linecap="round"/>' +
      '<path d="M16 49L18 51M22 45L24 48" stroke="#f8fafc" stroke-width="1.7" stroke-linecap="round"/>' +
      '<circle cx="49.5" cy="35.3" r="1.3" fill="#fbbf24"/>' +
      '<path d="M32 42L29 49M43 40L46 47M27 37L22 35" stroke="#0f172a" stroke-width="2.1" stroke-linecap="round"/>'
    ),

    // G15 — Le Va-et-vient du Colibri (O>I) : colibri émeraude en vol stationnaire devant une fleur
    G15: wrapMedallion(
      'G15',
      'Le Va-et-vient du Colibri',
      'O',
      '<path d="M51 54Q49 44 50 37" fill="none" stroke="#15803d" stroke-width="2.4" stroke-linecap="round"/>' +
      '<path d="M43 32C46 25 53 23 56 28C58 32 54 37 49 38C54 40 55 45 50 47C45 47 42 42 44 37Z" fill="#f43f5e" stroke="#881337" stroke-width="1.5" stroke-linejoin="round"/>' +
      '<circle cx="48" cy="35" r="3" fill="#fbbf24"/>' +
      '<path d="M25 27C19 16 12 12 10 17C9 23 15 28 23 31Z" fill="#34d399" stroke="#065f46" stroke-width="1.5" stroke-linejoin="round"/>' +
      '<path d="M27 25C24 14 19 10 16 14C15 19 20 25 26 28Z" fill="#a7f3d0" stroke="#065f46" stroke-width="1.2" opacity="0.85"/>' +
      '<path d="M21 37C23 28 29 24 35 26C38 28 37 34 32 38C27 42 22 45 14 50L16 42Z" fill="#059669" stroke="#064e3b" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M32 29C35 30 35 34 31 35C29 33 30 30 32 29Z" fill="#e11d48"/>' +
      '<circle cx="33.5" cy="27.8" r="1.2" fill="#0f172a"/>' +
      '<path d="M36.5 28.5L47 34" stroke="#0f172a" stroke-width="1.8" stroke-linecap="round"/>'
    ),

    // === 5 NIDS (M1..M5) ===

    // M1 — La Fourmilière Coupe-Feuilles (I>M) : fourmi rouge portant une grande feuille verte découpée
    M1: wrapMedallion(
      'M1',
      'La Fourmilière Coupe-Feuilles',
      'I',
      '<path d="M8 54Q32 45 56 54V56Q56 58 52 58H12Q8 58 8 56Z" fill="#b45309" opacity="0.65"/>' +
      '<path d="M24 34C22 19 34 9 48 11C53 16 53 27 44 33L40 28L38 34C33 36 28 36 24 34Z" fill="#16a34a" stroke="#14532d" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M26 32Q37 22 47 13M34 25L33 17M40 20L46 21" fill="none" stroke="#bbf7d0" stroke-width="1.3" stroke-linecap="round"/>' +
      '<ellipse cx="18" cy="43" rx="6.2" ry="4.8" transform="rotate(-12 18 43)" fill="#b91c1c" stroke="#450a0a" stroke-width="1.6"/>' +
      '<ellipse cx="29" cy="41.5" rx="4.2" ry="3.2" fill="#dc2626" stroke="#450a0a" stroke-width="1.5"/>' +
      '<circle cx="38" cy="39.5" r="4.1" fill="#b91c1c" stroke="#450a0a" stroke-width="1.6"/>' +
      '<circle cx="39.5" cy="38.5" r="0.9" fill="#fef08a"/>' +
      '<path d="M41 37L46 34M41 40L47 41" fill="none" stroke="#450a0a" stroke-width="1.4" stroke-linecap="round"/>' +
      '<path d="M26 44L22 52M29 44L30 52M33 44L38 51" fill="none" stroke="#450a0a" stroke-width="1.8" stroke-linecap="round"/>'
    ),

    // M2 — La Termitière à Glu (I>R) : termitière cathédrale ocre avec gouttes ambrées
    M2: wrapMedallion(
      'M2',
      'La Termitière à Glu',
      'I',
      '<path d="M12 54L18 30L22 35L27 13L32 8L37 15L41 30L46 25L52 54Z" fill="#b45309" stroke="#451a03" stroke-width="1.8" stroke-linejoin="round"/>' +
      '<path d="M21 54L26 23L32 13L36 27L42 54Z" fill="#d97706"/>' +
      '<path d="M27 54V43Q31 39 34 43V54Z" fill="#451a03"/>' +
      '<ellipse cx="32" cy="23" rx="1.6" ry="3" fill="#451a03"/>' +
      '<path d="M24 27C22 33 21 37 19 41A3.6 3.6 0 0 0 26 41C26 37 25 32 24 27Z" fill="#fbbf24" stroke="#78350f" stroke-width="1.3"/>' +
      '<circle cx="21.8" cy="40.2" r="1" fill="#fef9c3"/>' +
      '<path d="M39 26C37 32 36 36 37 39.5A3.8 3.8 0 0 0 44.5 39.5C44.5 35.5 41 31 39 26Z" fill="#fde047" stroke="#78350f" stroke-width="1.3"/>' +
      '<circle cx="39.8" cy="39" r="1.1" fill="#ffffff"/>' +
      '<path d="M47 36C47 36 43.5 41.5 43.5 44.5A3.5 3.5 0 0 0 50.5 44.5C50.5 41.5 47 36 47 36Z" fill="#fbbf24" stroke="#78350f" stroke-width="1.2"/>' +
      '<circle cx="46.2" cy="44" r="0.9" fill="#fef9c3"/>' +
      '<path d="M16 42C16 42 13 46.5 13 49A3 3 0 0 0 19 49C19 46.5 16 42 16 42Z" fill="#f59e0b" stroke="#78350f" stroke-width="1.2"/>'
    ),

    // M3 — La Branche des Guêpes Cazadores (I>O) : nid alvéolé suspendu à une branche + guêpe en vol
    M3: wrapMedallion(
      'M3',
      'La Branche des Guêpes Cazadores',
      'I',
      '<path d="M6 16Q30 11 58 17" fill="none" stroke="#78350f" stroke-width="4" stroke-linecap="round"/>' +
      '<path d="M44 13C47 7 54 8 52 14Z" fill="#16a34a" stroke="#14532d" stroke-width="1.1"/>' +
      '<path d="M24 14V20" stroke="#475569" stroke-width="2.4"/>' +
      '<path d="M15 31C15 22 19 19 24 19C29 19 33 22 33 31C33 39 29 44 24 45C19 44 15 39 15 31Z" fill="#cbd5e1" stroke="#334155" stroke-width="1.7"/>' +
      '<polygon points="21,29 24,27 27,29 27,32 24,34 21,32" fill="#475569"/>' +
      '<polygon points="18,35 21,33 24,35 24,38 21,40 18,38" fill="#475569"/>' +
      '<polygon points="24,35 27,33 30,35 30,38 27,40 24,38" fill="#475569"/>' +
      '<ellipse cx="44" cy="29" rx="7" ry="3.5" transform="rotate(-24 44 29)" fill="#e0f2fe" stroke="#0369a1" stroke-width="1.2"/>' +
      '<ellipse cx="49" cy="33" rx="6" ry="3" transform="rotate(-8 49 33)" fill="#f8fafc" stroke="#0369a1" stroke-width="1.1"/>' +
      '<ellipse cx="48" cy="43" rx="7" ry="4.2" transform="rotate(24 48 43)" fill="#facc15" stroke="#0f172a" stroke-width="1.5"/>' +
      '<path d="M45 39L43 44M49 40L47 46M53 42L51 47" stroke="#0f172a" stroke-width="1.8"/>' +
      '<circle cx="39" cy="38" r="3.4" fill="#0f172a"/>' +
      '<path d="M36 36L32 33M37 35L35 31" stroke="#0f172a" stroke-width="1.3" stroke-linecap="round"/>'
    ),

    // M4 — La Ruche des Mélipones (I>H) : rayons hexagonaux dorés + abeille mélipone
    M4: wrapMedallion(
      'M4',
      'La Ruche des Mélipones',
      'I',
      '<polygon points="18,22 24,18.5 30,22 30,29 24,32.5 18,29" fill="#fbbf24" stroke="#92400e" stroke-width="1.6"/>' +
      '<polygon points="30,22 36,18.5 42,22 42,29 36,32.5 30,29" fill="#fde68a" stroke="#92400e" stroke-width="1.6"/>' +
      '<polygon points="12,32.5 18,29 24,32.5 24,39.5 18,43 12,39.5" fill="#f59e0b" stroke="#92400e" stroke-width="1.6"/>' +
      '<polygon points="24,32.5 30,29 36,32.5 36,39.5 30,43 24,39.5" fill="#fbbf24" stroke="#92400e" stroke-width="1.6"/>' +
      '<polygon points="18,43 24,39.5 30,43 30,50 24,53.5 18,50" fill="#fde047" stroke="#92400e" stroke-width="1.6"/>' +
      '<polygon points="30,43 36,39.5 42,43 42,50 36,53.5 30,50" fill="#f59e0b" stroke="#92400e" stroke-width="1.6"/>' +
      '<ellipse cx="47" cy="24" rx="6" ry="3.3" transform="rotate(-30 47 24)" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.2"/>' +
      '<ellipse cx="51" cy="29" rx="5.2" ry="2.8" transform="rotate(-10 51 29)" fill="#ffffff" stroke="#0284c7" stroke-width="1.1"/>' +
      '<ellipse cx="47" cy="36" rx="7.5" ry="5.5" transform="rotate(14 47 36)" fill="#fde047" stroke="#78350f" stroke-width="1.6"/>' +
      '<path d="M44 31.5L43 40.5M48 31.5L47 41.2M52 33L51 40.5" stroke="#78350f" stroke-width="1.9"/>' +
      '<circle cx="39.5" cy="34.5" r="3.4" fill="#78350f"/>' +
      '<circle cx="38.5" cy="33.8" r="0.9" fill="#fef9c3"/>'
    ),

    // M5 — Le Jardin du Diable (I>E) : fourmi sombre entourée de pousses vertes jaillissant d'une souche
    M5: wrapMedallion(
      'M5',
      'Le Jardin du Diable',
      'I',
      '<path d="M22 41C16 32 14 23 18 15C24 20 26 28 26 40Z" fill="#22c55e" stroke="#14532d" stroke-width="1.5" stroke-linejoin="round"/>' +
      '<path d="M42 41C48 32 50 23 46 15C40 20 38 28 38 40Z" fill="#22c55e" stroke="#14532d" stroke-width="1.5" stroke-linejoin="round"/>' +
      '<path d="M32 39C28 27 28 16 32 10C36 16 36 27 32 39Z" fill="#4ade80" stroke="#14532d" stroke-width="1.5" stroke-linejoin="round"/>' +
      '<path d="M18 54L22 39H42L46 54Q32 56 18 54Z" fill="#78350f" stroke="#451a03" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<ellipse cx="32" cy="39.5" rx="10" ry="3.2" fill="#fde68a" stroke="#451a03" stroke-width="1.4"/>' +
      '<ellipse cx="26" cy="31" rx="4.2" ry="3.4" fill="#1e293b" stroke="#f8fafc" stroke-width="1"/>' +
      '<circle cx="32" cy="31.5" r="2.7" fill="#0f172a" stroke="#f8fafc" stroke-width="1"/>' +
      '<circle cx="37.5" cy="30.5" r="3.1" fill="#1e293b" stroke="#f8fafc" stroke-width="1"/>' +
      '<path d="M39.5 28.5L43 26M39.5 31.5L43 33M29 34L26 39M32 34L32 39M35 34L38 39" fill="none" stroke="#0f172a" stroke-width="1.5" stroke-linecap="round"/>'
    ),

    // === 10 RÊVES (R1..R10) — Halo nocturne / stellaire commun ===

    // R1 — Le Seuil des Deux Mondes (H>E) : arche lumineuse ouverte entre deux piliers
    R1: wrapMedallion(
      'R1',
      'Le Seuil des Deux Mondes',
      'RH',
      '<path d="M21 50V29A11 11 0 0 1 43 29V50Z" fill="#fde68a" opacity="0.92"/>' +
      '<path d="M25 50V30A7 7 0 0 1 39 30V50Z" fill="#fef9c3"/>' +
      '<path d="M15 52V28A17 17 0 0 1 49 28V52" fill="none" stroke="#c4b5fd" stroke-width="4.2" stroke-linecap="round"/>' +
      '<rect x="12.5" y="27" width="7" height="25" rx="1.5" fill="#cbd5e1" stroke="#312e81" stroke-width="1.4"/>' +
      '<rect x="44.5" y="27" width="7" height="25" rx="1.5" fill="#cbd5e1" stroke="#312e81" stroke-width="1.4"/>' +
      '<rect x="11" y="25" width="10" height="3.2" rx="1" fill="#e0e7ff"/>' +
      '<rect x="43" y="25" width="10" height="3.2" rx="1" fill="#e0e7ff"/>' +
      '<rect x="18" y="49" width="28" height="3.2" rx="1" fill="#e0e7ff"/>' +
      '<rect x="14" y="52.5" width="36" height="3.2" rx="1" fill="#94a3b8"/>' +
      '<polygon points="32,21 33.8,26 38.8,27.8 33.8,29.6 32,34.6 30.2,29.6 25.2,27.8 30.2,26" fill="#f59e0b"/>'
    ),

    // R2 — Le Voile de l'Oubli (E>H) : voile/brume violette glissant sur un œil fermé
    R2: wrapMedallion(
      'R2',
      'Le Voile de l’Oubli',
      'RE',
      '<path d="M13 27Q32 42 51 27" fill="none" stroke="#fef9c3" stroke-width="3" stroke-linecap="round"/>' +
      '<path d="M19 32L16 38M25 35L23.5 41.5M32 36V43M39 35L40.5 41.5M45 32L48 38" stroke="#fde68a" stroke-width="1.9" stroke-linecap="round"/>' +
      '<path d="M19 21Q32 14 45 21" fill="none" stroke="#e9d5ff" stroke-width="1.5" stroke-linecap="round" opacity="0.65"/>' +
      '<path d="M7 30C16 22 25 25 34 31C42 36 50 35 57 29C55 37 46 42 35 39C25 36 16 39 7 35Z" fill="#a855f7" opacity="0.72"/>' +
      '<path d="M9 44C20 38 30 47 44 43C50 41 54 43 56 46C49 52 38 52 28 49C19 46 13 48 9 44Z" fill="#c084fc" opacity="0.74"/>' +
      '<path d="M12 20C22 16 32 23 44 19" fill="none" stroke="#e9d5ff" stroke-width="2" stroke-linecap="round" opacity="0.72"/>'
    ),

    // R3 — La Danse des Esprits-Fauves (H>M) : masque tribal félin entouré d'étincelles
    R3: wrapMedallion(
      'R3',
      'La Danse des Esprits-Fauves',
      'RH',
      '<path d="M18 24L17 13L27 19H37L47 13L46 24L49 34L42 48L32 52L22 48L15 34Z" fill="#f59e0b" stroke="#fef3c7" stroke-width="1.7" stroke-linejoin="round"/>' +
      '<path d="M20 28L28 31L23 35Z" fill="#1e1b4b"/>' +
      '<path d="M44 28L36 31L41 35Z" fill="#1e1b4b"/>' +
      '<circle cx="24.2" cy="31.3" r="1.4" fill="#fef08a"/>' +
      '<circle cx="39.8" cy="31.3" r="1.4" fill="#fef08a"/>' +
      '<path d="M32 22V37M28 38L32 42L36 38Z" fill="#e11d48" stroke="#fef3c7" stroke-width="1.2" stroke-linejoin="round"/>' +
      '<path d="M18 37L24 39M19 42L25 43M46 37L40 39M45 42L39 43" stroke="#fef9c3" stroke-width="1.6" stroke-linecap="round"/>' +
      '<polygon points="11,17 12.2,20 15.2,21.2 12.2,22.4 11,25.4 9.8,22.4 6.8,21.2 9.8,20" fill="#fde047"/>' +
      '<polygon points="53,19 54.1,21.5 56.6,22.6 54.1,23.7 53,26.2 51.9,23.7 49.4,22.6 51.9,21.5" fill="#fb7185"/>' +
      '<circle cx="12" cy="46" r="1.8" fill="#fde047"/>' +
      '<circle cx="52" cy="45" r="1.8" fill="#fde047"/>'
    ),

    // R4 — Le Sommeil de la Pierre-Serpent (H>R) : serpent lové endormi sur une pierre gravée
    R4: wrapMedallion(
      'R4',
      'Le Sommeil de la Pierre-Serpent',
      'RH',
      '<path d="M10 49C10 38 17 31 32 31C47 31 54 38 54 49C54 53 46 55 32 55C18 55 10 53 10 49Z" fill="#64748b" stroke="#e2e8f0" stroke-width="1.6"/>' +
      '<path d="M18 46L23 42L28 46L33 42L38 46L43 42L47 46" fill="none" stroke="#e0e7ff" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>' +
      '<path d="M22 50.5H42" stroke="#1e1b4b" stroke-width="1.4" stroke-linecap="round"/>' +
      '<path d="M19 32C16 24 22 15 33 15C44 15 48 24 44 31C40 37 26 37 23 30C21 25 26 20 33 21C38 22 39 27 35 29" fill="none" stroke="#064e3b" stroke-width="7.2" stroke-linecap="round"/>' +
      '<path d="M19 32C16 24 22 15 33 15C44 15 48 24 44 31C40 37 26 37 23 30C21 25 26 20 33 21C38 22 39 27 35 29" fill="none" stroke="#10b981" stroke-width="4.6" stroke-linecap="round"/>' +
      '<ellipse cx="34" cy="29" rx="5.2" ry="3.3" fill="#34d399" stroke="#064e3b" stroke-width="1.3"/>' +
      '<path d="M31.5 28.8Q33.5 30.8 35.5 28.8" fill="none" stroke="#064e3b" stroke-width="1.3" stroke-linecap="round"/>'
    ),

    // R5 — La Vision des Plumes Claires (H>O) : œil lumineux couronné de trois plumes
    R5: wrapMedallion(
      'R5',
      'La Vision des Plumes Claires',
      'RH',
      '<path d="M32 29C28 21 28 13 32 8C36 13 36 21 32 29Z" fill="#ffffff" stroke="#7dd3fc" stroke-width="1.3"/>' +
      '<path d="M32 28V11" stroke="#f59e0b" stroke-width="1.1"/>' +
      '<path d="M24 31C17 26 14 19 15 13C21 16 25 22 26 30Z" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1.3"/>' +
      '<path d="M40 31C47 26 50 19 49 13C43 16 39 22 38 30Z" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1.3"/>' +
      '<path d="M12 41Q32 27 52 41Q32 55 12 41Z" fill="#fef9c3" stroke="#fde047" stroke-width="1.8" stroke-linejoin="round"/>' +
      '<circle cx="32" cy="41" r="7.5" fill="#0ea5e9" stroke="#1e1b4b" stroke-width="1.4"/>' +
      '<circle cx="32" cy="41" r="3.4" fill="#1e1b4b"/>' +
      '<circle cx="34.2" cy="38.8" r="1.5" fill="#ffffff"/>'
    ),

    // R6 — Le Miel des Ancêtres (H>I) : coupe dorée débordant de miel avec une jeune pousse
    R6: wrapMedallion(
      'R6',
      'Le Miel des Ancêtres',
      'RH',
      '<path d="M32 29V15" stroke="#4ade80" stroke-width="2.4" stroke-linecap="round"/>' +
      '<path d="M32 21C25 19 22 13 24 10C29 10 32 14 32 21Z" fill="#22c55e" stroke="#bbf7d0" stroke-width="1.1"/>' +
      '<path d="M32 19C39 17 42 12 40 9C35 9 32 13 32 19Z" fill="#4ade80" stroke="#bbf7d0" stroke-width="1.1"/>' +
      '<path d="M18 30H46C45 40 39 45 32 45C25 45 19 40 18 30Z" fill="#d97706" stroke="#fef3c7" stroke-width="1.6" stroke-linejoin="round"/>' +
      '<path d="M29 45H35L36 52H28Z" fill="#f59e0b" stroke="#fef3c7" stroke-width="1.3"/>' +
      '<rect x="22" y="51.5" width="20" height="3.5" rx="1.5" fill="#fbbf24" stroke="#fef3c7" stroke-width="1.2"/>' +
      '<path d="M17 29C22 26 42 26 47 29C47 32 44 33 42 32C41 37 38 38 37 33C34 32 30 33 28 38C26 40 24 38 24 33C21 33 17 32 17 29Z" fill="#fde047" stroke="#b45309" stroke-width="1.2" stroke-linejoin="round"/>'
    ),

    // R7 — L'Ombre du Maître des Bois (E>M) : silhouette spectrale de ramures/bois de cerf forestier
    R7: wrapMedallion(
      'R7',
      'L’Ombre du Maître des Bois',
      'RE',
      '<path d="M26 39C18 34 12 24 12 13M16 27L22 21M13 19L19 13M20 33L12 31" fill="none" stroke="#c4b5fd" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<path d="M38 39C46 34 52 24 52 13M48 27L42 21M51 19L45 13M44 33L52 31" fill="none" stroke="#c4b5fd" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<path d="M26 39C18 34 12 24 12 13M38 39C46 34 52 24 52 13" fill="none" stroke="#f5f3ff" stroke-width="1.1" stroke-linecap="round"/>' +
      '<path d="M25 37L32 34L39 37L36 53L32 56L28 53Z" fill="#1e1b4b" stroke="#e9d5ff" stroke-width="1.8" stroke-linejoin="round"/>' +
      '<circle cx="29" cy="43" r="1.4" fill="#fde68a"/>' +
      '<circle cx="35" cy="43" r="1.4" fill="#fde68a"/>' +
      '<circle cx="32" cy="24" r="1.6" fill="#fde68a"/>'
    ),

    // R8 — Le Mirage du Fleuve-Miroir (E>R) : souche se reflétant sur une onde miroir lunaire
    R8: wrapMedallion(
      'R8',
      'Le Mirage du Fleuve-Miroir',
      'RE',
      '<circle cx="49" cy="15" r="4.5" fill="#fef08a"/>' +
      '<path d="M21 34L24 20H40L43 34Z" fill="#d97706" stroke="#fde68a" stroke-width="1.5" stroke-linejoin="round"/>' +
      '<ellipse cx="32" cy="20" rx="8" ry="2.5" fill="#fef3c7" stroke="#92400e" stroke-width="1.1"/>' +
      '<path d="M28 24V31M36 25V31" stroke="#78350f" stroke-width="1.4" stroke-linecap="round"/>' +
      '<path d="M21 36L24 50H40L43 36Z" fill="#38bdf8" opacity="0.48" stroke="#bae6fd" stroke-width="1.2" stroke-dasharray="3 2"/>' +
      '<path d="M8 35H56" stroke="#e0f2fe" stroke-width="2" stroke-linecap="round"/>' +
      '<path d="M14 41H50M19 46H45M24 51H40" stroke="#7dd3fc" stroke-width="1.5" stroke-linecap="round" opacity="0.85"/>'
    ),

    // R9 — L'Écho des Voix Célestes (E>O) : ondes sonores concentriques autour d'une étoile
    R9: wrapMedallion(
      'R9',
      'L’Écho des Voix Célestes',
      'RE',
      '<circle cx="32" cy="32" r="21" fill="none" stroke="#a78bfa" stroke-width="1.6" stroke-dasharray="14 6"/>' +
      '<circle cx="32" cy="32" r="15.5" fill="none" stroke="#7dd3fc" stroke-width="1.9" stroke-dasharray="12 5"/>' +
      '<circle cx="32" cy="32" r="10" fill="none" stroke="#fde68a" stroke-width="1.8" stroke-dasharray="9 4"/>' +
      '<polygon points="32,18 35,29 46,32 35,35 32,46 29,35 18,32 29,29" fill="#fef08a" stroke="#f59e0b" stroke-width="1.2" stroke-linejoin="round"/>' +
      '<circle cx="32" cy="32" r="3.2" fill="#ffffff"/>'
    ),

    // R10 — La Nuée des Songes (E>I) : essaim de lucioles/papillons nocturnes autour d'un croissant
    R10: wrapMedallion(
      'R10',
      'La Nuée des Songes',
      'RE',
      '<path d="M34 18A15 15 0 1 0 34 46A14.2 14.2 0 0 1 34 18Z" fill="#fde047" stroke="#fef9c3" stroke-width="1.3" stroke-linejoin="round"/>' +
      '<path d="M40 20C36 16 33 19 36 23C33 25 36 27 40 24C44 27 47 25 44 23C47 19 44 16 40 20Z" fill="#c4b5fd" stroke="#ffffff" stroke-width="0.9"/>' +
      '<path d="M47 34C43 30 40 33 43 37C40 39 43 41 47 38C51 41 54 39 51 37C54 33 51 30 47 34Z" fill="#a7f3d0" stroke="#ffffff" stroke-width="0.9"/>' +
      '<path d="M35 34C32 31 30 33 32 36C30 37 32 39 35 37C38 39 40 37 38 36C40 33 38 31 35 34Z" fill="#fbcfe8" stroke="#ffffff" stroke-width="0.8"/>' +
      '<circle cx="49" cy="17" r="2.2" fill="#fef08a" opacity="0.5"/>' +
      '<circle cx="49" cy="17" r="1.1" fill="#ffffff"/>' +
      '<circle cx="38" cy="47" r="2.4" fill="#fde047" opacity="0.5"/>' +
      '<circle cx="38" cy="47" r="1.2" fill="#ffffff"/>' +
      '<circle cx="51" cy="46" r="2" fill="#a7f3d0" opacity="0.55"/>' +
      '<circle cx="51" cy="46" r="1" fill="#ffffff"/>' +
      '<circle cx="31" cy="24" r="1.9" fill="#fde047" opacity="0.6"/>' +
      '<circle cx="31" cy="24" r="0.95" fill="#ffffff"/>'
    )
  };

  const TILE_ILLUSTRATION_IDS = Object.keys(TILE_ILLUSTRATIONS_V62);

  function getTileIllustrationSvg(tileId) {
    if (!tileId) return '';
    const key = String(tileId).trim().toUpperCase();
    return TILE_ILLUSTRATIONS_V62[key] || '';
  }

  const api = {
    VERSION,
    REPTILE_ICON_VIEWBOX,
    REPTILE_ICON_INNER_SVG,
    REPTILE_ICON_SVG,
    getReptileIconSvg,
    getReptileWheelIconSvg,
    TILE_ILLUSTRATION_IDS,
    TILE_ILLUSTRATIONS_V62,
    getTileIllustrationSvg
  };

  global.AmazoniaTileIllustrationsV62 = api;
  if (typeof global.window !== 'undefined') {
    global.window.AmazoniaTileIllustrationsV62 = api;
  }
})(typeof window !== 'undefined' ? window : globalThis);
