"""Verify NRCS published JSON against the corresponding official chart.

Run: python -m pipeline.proof --input PATH --output PATH
Input files: state.json, state-chart.html, basin.json, basin-chart.html.
No network, credentials, newsletter delivery, or production publication.
"""
import argparse
import csv
import hashlib
import json
import math
import re
from datetime import date, datetime, timezone, timedelta
from pathlib import Path

BASE = 'https://nwcc-apps.sc.egov.usda.gov/awdb/basin-plots/POR/WTEQ/'
REFERENCE = "Median ('91-'20)"
# Colorado Snow Survey's eight custom major basins, not arbitrary HUC slices.
# Preserve the original keys and IDs so existing links and accepted history remain valid.
PRODUCTS = {
    'state': ('co-state', 'State of Colorado', 'assocHUCco3/state_of_colorado'),
    'basin': ('co-colorado-headwaters', 'Colorado Headwaters', 'assocHUCco_8/colorado_headwaters'),
    'gunnison': ('co-gunnison', 'Gunnison', 'assocHUCco_8/gunnison'),
    'southwest': ('co-san-miguel-dolores-animas-san-juan', 'San Miguel–Dolores–Animas–San Juan', 'assocHUCco_8/san_miguel-dolores-animas-san_juan'),
    'yampa': ('co-yampa-white-little-snake', 'Yampa–White–Little Snake', 'assocHUCco_8/yampa-white-little_snake'),
    'north-platte': ('co-laramie-north-platte', 'Laramie & North Platte', 'assocHUCco_8/laramie_and_north_platte'),
    'south-platte': ('co-south-platte', 'South Platte', 'assocHUCco_8/south_platte'),
    'arkansas': ('co-arkansas', 'Arkansas', 'assocHUCco_8/arkansas'),
    'rio-grande': ('co-upper-rio-grande', 'Upper Rio Grande', 'assocHUCco_8/upper_rio_grande'),
}
REGION_GROUPS = {
    'co-state': 'Statewide',
    **{PRODUCTS[k][0]: 'Colorado River drainage' for k in ('basin','gunnison','southwest','yampa')},
    **{PRODUCTS[k][0]: 'Platte River drainage' for k in ('north-platte','south-platte')},
    'co-arkansas': 'Arkansas River drainage',
    'co-upper-rio-grande': 'Rio Grande drainage',
}


def observation_date(water_year, month_day):
    month, day = map(int, month_day.split('-'))
    year = water_year - 1 if month >= 10 else water_year
    try:
        return date(year, month, day)
    except ValueError:
        if month_day == '02-29':
            return None  # The source uses a common leap-year plotting axis.
        raise


def number(value):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError('Invalid SWE value')
    return value


def percentage(swe, median):
    number(swe)
    number(median)
    if swe is None or median is None or median < 0.1:
        return None
    return 100 * swe / median


def chart_payload(html):
    start = html.index('[', html.index('Plotly.newPlot('))
    decoder = json.JSONDecoder()
    traces, end = decoder.raw_decode(html[start:])
    layout, _ = decoder.raw_decode(html[start + end:].lstrip(', \n\t\r'))
    if layout['yaxis']['title']['text'] != 'Snow Water Equivalent (in.)':
        raise ValueError('Unexpected chart units')
    return traces, layout


def verify(rows, html, key):
    if not isinstance(rows, list) or len(rows) != 366:
        raise ValueError('Expected the complete 366-day source axis')
    expected_days = {(date(2015, 10, 1) + timedelta(days=i)).strftime('%m-%d') for i in range(366)}
    if {r['date'] for r in rows} != expected_days:
        raise ValueError('Duplicate or missing source dates')
    traces, layout = chart_payload(html)
    series = {}
    labels = {}
    for t in traces:
        if t.get('legendgroup') == 'firstOfMonth':
            continue  # Alternate monthly view is not the daily series.
        name = t.get('name', '')
        match = re.fullmatch(r'(\d{4}) \((\d+) sites\)', name)
        if match or name == REFERENCE:
            field = match[1] if match else REFERENCE
            if len(t['x']) != 366 or len(t['y']) > len(t['x']):
                raise ValueError('Mismatched chart axes')
            if field in series:
                raise ValueError('Ambiguous daily chart series')
            values = t['y'] + [None] * (len(t['x']) - len(t['y']))
            series[field] = dict(zip((x[5:10] for x in t['x']), values))
            labels[field] = name
    years = sorted(k for k in rows[0] if re.fullmatch(r'\d{4}', k))
    if not years or REFERENCE not in series:
        raise ValueError('Missing water years or reference')
    checks = 0
    for row in rows:
        for field in [*years, REFERENCE]:
            actual = number(row[field])
            expected = number(series[field][row['date']])
            if (actual is None) != (expected is None):
                raise ValueError(f'Null mismatch: {field}/{row["date"]}')
            if actual is not None and not math.isclose(actual, expected, abs_tol=1e-9, rel_tol=0):
                raise ValueError(f'Value mismatch: {field}/{row["date"]}')
            checks += 1
    region_id, region_name, path = PRODUCTS[key]
    normalized = []
    for year in years:
        for row in rows:
            observed = observation_date(int(year), row['date'])
            if observed is None:
                continue
            swe = row[year]
            median = row[REFERENCE]
            flags = ['provisional', 'coverage_not_independently_verified']
            if swe is None:
                flags.append('missing')
            if median is None:
                flags.append('missing_reference')
            elif median < 0.1:
                flags.append('near_zero_reference')
            normalized.append(dict(region_id=region_id, observation_date=observed.isoformat(),
                water_year=int(year), swe_inches=swe, median_inches=median,
                percent_of_median=percentage(swe, median), reference_period='1991-2020',
                reference_statistic='median', quality_flags=';'.join(flags)))
    latest = max((r for r in normalized if r['swe_inches'] is not None), key=lambda r:r['observation_date'])
    return normalized, dict(region_id=region_id, region_name=region_name, source_json=BASE+path+'.json',
        source_chart=BASE+path+'.html', matched_values=checks, historical_water_years=years,
        latest=latest, chart_series_labels=labels,
        chart_status=[a['text'] for a in layout.get('annotations', []) if a['text'].startswith('Current as of')])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    all_rows, proofs, hashes = [], [], {}
    # Validate both products completely before emitting any exports.
    for key in PRODUCTS:
        source = args.input / f'{key}.json'
        chart = args.input / f'{key}-chart.html'
        rows, proof = verify(json.loads(source.read_text()), chart.read_text(), key)
        all_rows.extend(rows)
        proofs.append(proof)
        for file in [source, chart]:
            hashes[file.name] = hashlib.sha256(file.read_bytes()).hexdigest()
    report = dict(schema_version='0.1.0', method_version='nrcs-published-por-v1',
        verified_at=datetime.now(timezone.utc).isoformat(), status='research-proof-not-production',
        limitation='Chart and JSON share an upstream product; agreement is not independent sensor validation. Station coverage and aggregation methodology still need confirmation.',
        source_sha256=hashes, products=proofs)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'proof.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    (args.output/'series.json').write_text(json.dumps(dict(metadata=report, observations=all_rows), allow_nan=False)+'\n')
    with (args.output/'series.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(all_rows[0]))
        writer.writeheader()
        writer.writerows(all_rows)
    print(f'Verified {sum(p["matched_values"] for p in proofs):,} chart/export values; exported {len(all_rows):,} observations. Research proof only.')


if __name__ == '__main__':
    main()
