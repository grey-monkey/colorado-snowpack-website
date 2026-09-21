# Data proof — September 21, 2026

## Second-slice labeling decision

Public wording is **published NRCS station-based SWE series**, narrowly scoped
to the exact daily period-of-record products verified below. It does not claim
area weighting, fixed station coverage, basin-total volume, or daily reporting
counts. The official chart station list includes non-Colorado stations in the
statewide product; 2026 legends identify 115 statewide and 31 Headwaters sites.
Historical legends change. These counts are not completeness percentages.

The [NRCS product guide](https://www.nrcs.usda.gov/programs-initiatives/sswsf-snow-survey-and-water-supply-forecasting-program/snow-and-water-products)
warns about incompatible basin definitions in other report products. The
[Colorado FAQ](https://www.wcc.nrcs.usda.gov/ftpref/support/states/CO/products/faq/)
documents custom basins and representative stations on divides. The
[normals page](https://www.nrcs.usda.gov/resources/data-and-reports/climatic-and-hydrologic-normals)
identifies the 1991–2020 reference and distinguishes medians from averages.
Neither documentation nor these exports establishes daily denominator/weight
behavior sufficiently to make a stronger public aggregation claim. Narrow labels
and an explicit coverage note resolve the first dashboard's interpretation gate;
sensor-level reconstruction is not necessary for this display.

No new regions or approximate map boundaries were added. The two verified
products are selected through a bookmarkable list. Daily/weekly changes are
differences in published series, with coverage caution, not snowfall claims.
Website display acceptance is limited to this frozen, provisional snapshot.
Future automated acceptance remains separate.

## Products and scope

Use NRCS published period-of-record daily SWE aggregates, not reconstructed
averages of basin percentages. Product identifiers are `assocHUCco3/state_of_colorado`
and `assocHUCco_8/colorado_headwaters` under
https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/WTEQ/.
The chart pages link their matching `.json` and `.csv` files.

Source: https://www.wcc.nrcs.usda.gov/ftpref/support/states/CO/products/faq/

The statewide product includes representative stations outside Colorado. It is
a station-based snowpack index, not total water volume over the state. The
Colorado Headwaters product is the NRCS custom major basin, not a silently
substituted HUC watershed. Geometry integration remains pending.

## Completed proof

30,378 values (including null positions) agree between JSON and corresponding
chart traces to an absolute tolerance of 1e-9 inches. Charts and JSON share an
upstream product; this validates product integration, not independent sensor
accuracy. Statewide water years span 1987–2026; Colorado Headwaters spans
1986–2026. A year column does not establish complete daily station coverage.

September 21, 2026 values:

| Product | SWE, inches | Same-date median, inches | Percent of median |
|---|---:|---:|---|
| State of Colorado | 0.0443478261 | 0 | Not meaningful |
| Colorado Headwaters | 0.0516129032 | 0 | Not meaningful |

Both official charts label the current percentage N/A. The export preserves the
published median `Median ('91-'20)`, distinct from the period-of-record median.
The chart y-axis verifies inches of SWE. SWE is water contained in snow, not
snow depth or fresh snowfall.

## Version 0.1 rules

- Water year runs October–September. Source MM-DD is mapped to the actual calendar
  year; synthetic chart dates are never used as observation dates.
- The common 366-day chart axis contains February 29. For non-leap water years,
  omit that date, without shifting March or interpolating an observation.
- Select daily traces; exclude the alternate hidden `firstOfMonth` trace.
  A truncated current-year trace has missing future values, not zeroes.
- JSON null remains missing; numeric zero remains zero. Reject negative,
  nonnumeric, infinite, and NaN SWE values.
- Suppress ratios when the reference is missing or below 0.1 inches. This is a
  proposed editorial stability threshold, not an NRCS threshold. Preserve raw
  SWE and reference. Do not infer absence of snow from an undefined percentage.
- Preserve annual chart station labels. They vary historically. No claim of a
  fixed station population or independent completeness assessment is made.
- Every observation is flagged provisional and coverage not independently
  verified. Missing and near-zero reference flags are explicit.
- Proof timestamp is distinct from observation date. Frozen raw files retain
  source values and hashes. This initial proof has no production retrieval job.

## Before production acceptance

Confirm aggregation and daily station coverage semantics against NRCS methods;
verify year-to-year comparability and major-basin boundaries. Implement freshness,
bounded fetching, last-valid retention, revisions, atomic snapshot publication,
and a seven-calendar-day comparison with coverage checks. Add schema/reuse
documentation and shared snapshot rendering for the site and newsletter.

Research exports may include missing trailing dates in a water year. The website
must select the latest actual observation and evaluate staleness separately.
Do not present these frozen files as live or automatically refreshed.
