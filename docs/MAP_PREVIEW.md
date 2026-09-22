# Colorado Snowpack: map edition preview

Local branch: map-preview. Not pushed, deployed, or connected to newsletter sending. Production stays on b573c53.

## Design

The map sits above the season chart. Select a basin on the map or in the readable companion list to update the existing region selector and chart. The chart slider, water-year selector and map date picker share one date. Region/year/date are preserved in preview URLs. The overview at the top of the page remains explicitly dated to the latest accepted observation; the map and chart explore the chosen date.

Default color mode chooses percent of the same-date 1991–2020 median when any basin has a usable reference. When all basin references are missing or below 0.1 inch, it uses SWE in inches. Users can explicitly choose either measure. Fixed color bands avoid making small day-to-day differences look dramatic. Numeric labels accompany color, with a full readable list on phones. This is not a map of snow coverage, snow depth, total water storage or forecast conditions.

Percent bands use rounded displayed percentages: below 50, 50–79, 80–119, 120–149, 150+. These are display bands, not official drought or hazard classifications. Inches bands: measured zero, positive below 1, 1–<5, 5–<10, 10–<20, 20+. Missing observations have hatching; unusable reference medians have dots in percentage mode. No value is invented for a future date or non-leap February 29.

## Geography

NRCS provides the exact Colorado custom major-basin map polygons at:
https://nwcc-apps.sc.egov.usda.gov/awdb/basin-defs/geojson/co_8.geojson

Its FAQ describes these as coarse/generalized polygons. We preserve all their vertices and basin identifiers; they are appropriate to statewide display, not survey-grade or parcel-level use. Eight features join one-to-one with the eight dashboard products. The two additional eastern-plains features have no matching SWE series in the dashboard and remain unreported. Other gaps in the eight-region footprint also remain unreported.

Colorado outline: U.S. Census Bureau TIGERweb States, January 1, 2026 vintage. Exact query, downloaded geometry and SHA-256 hashes are archived under evidence/map. Albers equal-area projection centered on Colorado (39 N, 105.5 W; standard parallels 37/41 N). SVG clips the NRCS polygons to the official Colorado outline. Measurements still describe complete NRCS reporting basins, including out-of-state sites. No polygon is hand-drawn or fabricated; no measurements are geographically interpolated.

Reproduce geometry with `python ops/build_map_geometry.py`. No map API key, external tile service, tracking, browser geolocation or recurring cost is needed. Boundary geometry is about 133 KB and is hosted locally with the site.

## Newsletter draft

Download map image produces a standalone 1200×1040 PNG with date, metric, numeric basin readings, fixed legend, source and limitations. It excludes interactive selection highlighting. Current and historical examples are saved for review. Every image is explicitly labeled LOCAL PREVIEW. Nothing has been attached to or sent through Kit, and no production newsletter template or schedule changed. Final newsletter integration remains a separate owner-reviewed step.

## Menu refinement

Selected region uses bold text. The orange focus rectangle is removed from the region selector, with a subtle green inset underline retained for keyboard users. Normal capitalization preserves long-name readability. This change is also preview-only.

## Validation

Official geometry reproduced exactly from archived sources. Tests cover nine-region identity, zero/missing/near-zero distinctions, non-leap dates, explicit and automatic color modes, selection synchronization, date/year synchronization, keyboard focus retention, 320/390/768/1440 layouts, PNG generation for summer and winter, and map-retrieval failure without losing the existing chart.

The local preview has noindex/nofollow and no active signup configuration. Source evidence and data remain public weather/geographic information only.
