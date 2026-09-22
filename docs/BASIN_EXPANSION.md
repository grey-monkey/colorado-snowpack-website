# Colorado basin coverage and terrain update

The dashboard includes Colorado statewide and all eight custom major basin products in the NRCS Colorado Snow Survey catalog (assocHUCco_8). Existing statewide and Colorado Headwaters identifiers remain unchanged. The menu groups basins by receiving river system, retaining NRCS combined boundaries. Every basin retains its own published 1991–2020 median and full historical exports.

Official catalog: https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/WTEQ/assocHUCco_8/

Validation: 137,982 annual/reference positions compared with official chart traces; all nine products report September 21, 2026. The transition from two to nine products preserves prior observations. Newsletter names now derive from the same basin catalog. 21 Python checks, 12 JavaScript checks, 15 browser checks, and nine-region checks at 320, 390, 768, and 1440 pixels passed. Controlled missing, zero, stale, outage and duplicate-delivery protections remain covered.

The contour background uses real public-domain USGS National Map geometry near Longs Peak, north up, NAD83 / UTM zone 13N. Source lines at 100-foot intervals were selected every 200 feet, clipped, and uniformly scaled. No smoothing or invented control points. The 699 retained line segments have no strict crossings. Source URL, exact cropped geometry, source hash and bounds are in evidence/terrain/longs-peak-contours.json. It is decorative terrain, not a basin map or snow observation.

Expanded accepted history is about 55 MB; the fresh static publication is about 60 MB. Existing safety ceilings were adjusted to 80 MB for the database and 90 MB for publication, still within the existing free public GitHub/Pages stack. No paid service, credential, email DNS, signup configuration, or scheduling change was introduced.
