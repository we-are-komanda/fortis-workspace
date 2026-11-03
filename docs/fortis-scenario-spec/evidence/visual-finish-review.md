disposition: fix

Missing inputs: PRODUCT.md and QUALITY BAR card were not supplied or found; the parent confirms the direction authority is the original HTML plus README.md. A new concept roll is inapplicable to this reference restoration. Reviewed original `/private/tmp/scn-reference.png`, all nine named captures, the HTML drawing code, README.md sections 1–9, and the shared terrain/2D/3D/CSS sources. No runtime tests or detector were run by this reviewer.

## persistence

Fail: no PRODUCT.md. The existing README.md does preserve the product scope, approved reference, behavior, and responsive exceptions; preserve that authority rather than inventing a new design direction. The supplied full original screenshot provides the reference checkpoint. All required captures exist, have plausible viewport dimensions, and visibly represent their named states: preparation-1440, playback-1440, comparison-1440, comparison-1280, comparison-390, comparison-390-controls, comparison-dark, initial-webgl-fallback-1280, fallback-1440. The narrow controls capture is intentionally scrolled. Error-state empty scene space is intentional, not malformed evidence.

## fidelity

| Salient element | Verdict | Evidence |
|---|---|---|
| TYPE | Acceptable adaptation | Compact dark sans, restrained hierarchy, and blue controls retain the reference character. Existing Fortis shell and accessible 44px controls are explicitly required by README sections 2 and 8; matching the mock shell is not required. |
| MATERIAL: enterprise | Match | Six shaded volumes, pale roofs with fine seams, four cylindrical tanks, yard perimeter, and internal lanes are visibly present in preparation/playback/comparison at 1440. The reference is diagrammatic 2.5D, so raster or photoreal assets are not required. |
| MATERIAL: terrain | Contradicted in two details | The reference river traverses the scene and exits both ends; current water is a closed, isolated lake with rounded caps. Reference trees form an irregular scattering over the hill; current trees form a conspicuous evenly filled spiral disk. These differences are visible in both renderers and originate in shared geometry. |
| GROUND | Match | Source base colors agree exactly: light land #e7ecdf, hill #c6d6b7, water #b7dce3. Screenshots retain the pale green field. Subtle reference terrain tessellation is absent, leaving a visibly cleaner field; restore this only as map geometry detail, without decorative page texture. |
| Map topology and focal scale | Acceptable adaptation, with water exception above | Northwest forest/hill, southeast hill, crossing cream roads, central yard, dashed radius, and colored paths are retained. Comparison gives the map its own column; north-up 2D has a smaller yard than 3D, consistent with viewing the full 10km radius. |
| Panels and timeline | Match | Library left, scene center, comparison controls right, floating setup/playback detail, lower time transport follow the reference's reading order. |
| Narrow layout | Acceptable adaptation | Map precedes stacked controls at 390px, as README section 8 requires. Both narrow captures show legible controls and no visible page-width overflow. |
| Fallback control composition | Contradicted | At initial-webgl-fallback-1280, the zoom stack covers the setup card's facts and primary-action edge. This is a real visible overlap at a required desktop viewport. |
| Truth and boundaries | Match in inspected evidence | Synthetic labels are prominent; no weather, physical calculation, production outcome, or completed AI generation is claimed. Error capture names the problem and exposes 2D recovery. |

## ceiling

The enterprise detail reaches the reference's diagrammatic material level. The landscape still leaves the reference's continuous river, irregular forest distribution, and faint tessellated surface unused. No separate quality card exists, so the original HTML drawing is the ceiling. Motion, hover, and assistive behavior cannot be inferred from still captures and are outside this review's claims. The inspected screenshots show no material craft-floor refusal that requires a separate visual redesign.

## material_fixes

1. Fidelity/material: replace the shared closed `lake` outline with a continuous winding river geometry that extends beyond the visible northern and southern scene bounds, following the original HTML river shape; use the same authored geometry in 2D and 3D and recapture both views.
2. Fidelity/material: replace the visible spiral forest disk with a deterministic irregular scatter matching the original hill footprint and varied tree tones; restore the reference's faint terrain tessellation where it aids the same landscape detail. Keep the existing palette and enterprise rendering.
3. Floor/responsive composition: move the zoom stack out of the setup-card footprint at 1280×720; reserve independent vertical or horizontal space so no fact, action, or control overlaps. Recapture initial WebGL fallback at that exact viewport.
4. Persistence: add a concise PRODUCT.md pointing to the existing scenario specification and recording the user's explicit requirement that landscape and 3D detail follow the original reference. Do not create a second product specification.

## keep

Keep the existing Fortis shell, blue palette, quiet map ground, detailed enterprise volumes and roofs, synthetic labeling, shared scene geometry, accessible control sizing, and comparison's separate panel while correcting the landscape fidelity and fallback overlap.
