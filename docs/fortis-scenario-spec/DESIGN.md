---
name: Fortis SCN-01
description: Implemented synthetic campus within the existing Fortis workspace
colors:
  surface: "#fff"
  ink: "#172b48"
  secondary: "#526782"
  line: "#d7e2f0"
  accent: "#2563eb"
  track-east: "#b45309"
  track-southwest: "#7c3aed"
  scene-ground: "#e7ecdf"
  scene-water: "#b7dce3"
  scene-tree: "#94b18a"
  scene-contour: "#aebda0"
  scene-building: "#bcc9d6"
  scene-roof: "#eef1f4"
  scene-road: "#faf9f1"
  scene-yard: "#d6dbd9"
typography:
  title: { fontSize: "1.05rem", fontWeight: 650 }
  heading: { fontSize: ".95rem", fontWeight: 650 }
  body: { fontSize: ".875rem" }
  detail: { fontSize: ".75rem" }
rounded:
  control: ".375rem"
  overlay: ".5rem"
spacing:
  small: ".5rem"
  panel: ".85rem"
components:
  button-primary: { backgroundColor: "{colors.accent}", textColor: "{colors.surface}", rounded: "{rounded.control}", padding: ".45rem .65rem" }
  button-secondary: { backgroundColor: "{colors.surface}", textColor: "{colors.ink}", rounded: "{rounded.control}", padding: ".45rem .65rem" }
---

# Design System: Fortis SCN-01

## Overview

**Creative North Star: "Synthetic campus atlas"** — a descriptive name for the implemented world, not a new brand direction.
The continuous pale green landscape follows [the original mockup](fortis-scenario-mockups.html); the surrounding Fortis shell remains the incumbent workspace. This is a scoped visual record; product behavior and acceptance live in [PRODUCT.md](PRODUCT.md) and [README.md](README.md).
**Key Characteristics:** quiet map materials, fine cartographic detail, readable industrial volumes, compact task controls.

## Colors

Primary: blue identifies active controls and the north track. Secondary track colors separate east and southwest; terrain stays low contrast so tracks remain legible.
Neutral: white panels, dark navy text, muted blue secondary text and fine blue-gray dividers organize the shell. Ground, water, trees, contours, roofs, roads and yard use the scene tokens above.
Dark mode uses explicit lightened track colors and darker scene materials in the implementation; retain those theme-specific mappings rather than globally inverting the scene.

## Typography

The scenario inherits its surrounding Fortis font stack. It adds no display face: compact semibold headings use the recorded title/heading scale, ordinary text uses body, and supporting details use detail. Timer and timeline labels use tabular numerals; subdued scene labels recede behind geometry.

## Layout

Header tabs and the synthetic-data strip sit above the workspace. At widths of at least 1024px, library / map occupy two columns; comparison adds a right panel (15rem / flexible / 18rem). The ordinary library is 16rem wide. Panels scroll independently; the map has a minimum 27rem height.
Below 1024px, the map and transport precede library and right-panel content in one column. Header and transport controls wrap. Below 640px the stage is 34rem tall; the preparation card narrows to 13rem.
The map heading is upper left; 2D/3D is upper right; preparation or playback details sit below those view controls. Zoom and fit form a vertical group near the lower right; transport and timeline stay below the map.
**The Clear Controls Rule.** With a preparation card present, zoom moves left on narrow screens, and to an 18rem right inset on desktops no taller than 820px. Preserve this exception so the card cannot cover zoom.

## Elevation & Depth

The shell uses fine borders and flat white surfaces; map overlays use soft ambient shadows. The 3D map uses an orthographic architectural oblique view (horizontal roof edges, vertical walls, depth shear 0.22), continuous raised terrain and contours following elevation. Depth comes from box-shaped building walls, light roofs with the original seam spacing and fine silhouette edges, cylindrical tanks, and low rounded tree crowns; avoid replacing those with flat markers.

## Shapes

Controls and event rows have gently curved corners; overlays use the larger radius above. The campus combines five rectilinear building volumes, four round tanks, a bounded yard and internal driveways. Roads curve through the landscape; the river continues across the scene. Forest crowns vary in position and size inside a rounded cluster; fine grid and irregular contour rings continue the map texture.

## Components

Buttons/selects have a minimum 2.75rem height. Primary actions use blue/white; secondary controls use outlined white surfaces. Pressed controls use accent borders and a light accent tint; disabled controls reduce opacity; keyboard focus has a 3px outline with 3px offset.
Library rows pair letter, direction and supporting metadata; selection uses the same accent treatment. Layer toggles remain labeled native checkboxes. Preparation overlays group title, objective, facts and a full-width action. Comparison uses two selectors and stacked event records beside one shared map.
Tracks use colored routes, lettered markers and dashed/projection lines. Preview reduces unselected tracks to 40% opacity. The 2D fallback shares authored terrain, river, road and enterprise data, with flat footprints and tank circles instead of 3D volumes.

## Do's and Don'ts

- **Do** keep terrain, grid, contours, river, irregular forest, detailed roofs, tanks, yard and driveways together as the scene's visual vocabulary.
- **Do** retain the incumbent shell, readable controls, and the preparation/zoom clearance exception.
- **Don't** substitute the previously rejected simplified renderer for the mockup's landscape and industrial detail.
- **Don't** treat the synthetic site as real geography, or turn this visual record into a second product specification.

Sources: `frontend/src/modules/drone-defense/ui/scenario/`, `domain/scenario-site.ts`, `infra/data/scenario/site-v1.json`. Evidence: [preparation](evidence/preparation-1440.png), [comparison desktop](evidence/comparison-1440.png), [comparison mobile](evidence/comparison-390.png), [initial WebGL fallback](evidence/initial-webgl-fallback-1280.png), [original reference](evidence/reference-original-1440.png). Validation scope is recorded separately in [implementation-report.md](implementation-report.md).
