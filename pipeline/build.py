"""Build a portable static dashboard from frozen, verified NRCS evidence."""
import argparse
import csv
import json
import hashlib
import shutil
from pathlib import Path
from .proof import PRODUCTS, REFERENCE, verify
from .pages import render_pages

ROOT = Path(__file__).resolve().parents[1]


def build(output):
    evidence = ROOT / 'evidence' / '2026-09-21'
    provenance = json.loads((evidence / 'proof.json').read_text())
    for name, expected in provenance['source_sha256'].items():
        if hashlib.sha256((evidence/name).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Frozen evidence changed: {name}; review before building')
    regions, observations = [], []
    for key, (region_id, name, _) in PRODUCTS.items():
        raw = json.loads((evidence / f'{key}.json').read_text())
        normalized, proof = verify(raw, (evidence / f'{key}-chart.html').read_text(), key)
        observations.extend(normalized)
        years = list(map(int, proof['historical_water_years']))
        newest = max(years)
        regions.append(dict(id=region_id, name=name, source=proof['source_chart'],
            coverage=[min(years), max(years)], station_labels=proof['chart_series_labels'],
            dates=[r['date'] for r in raw], median=[r[REFERENCE] for r in raw],
            years={str(y): [r[str(y)] for r in raw] for y in range(newest-3, newest+1)}))
    snapshot = dict(schema_version='1.0.0', status='frozen', observation_date='2026-09-21',
        verified_at=provenance['verified_at'], reference_period='1991–2020', units='inches SWE',
        method='nrcs-published-por-v1', regions=regions)
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'site', output, dirs_exist_ok=True)
    render_pages(output)
    from .signup import configure
    configure(output)
    data = output / 'data'
    data.mkdir(exist_ok=True)
    (data/'snapshot.json').write_text(json.dumps(snapshot, separators=(',', ':'), allow_nan=False), encoding='utf-8')
    # Public files carry the same values as the dashboard and retain history.
    metadata = dict(provenance, display_scope='Published NRCS station-based SWE series',
        status='frozen', units='inches SWE', reference_period='1991-2020',
        privacy='No subscriber data', csv_null='Empty field means missing; 0 means measured zero')
    (data/'metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    (data/'series.json').write_text(json.dumps(dict(metadata=metadata, observations=observations), separators=(',', ':'), allow_nan=False), encoding='utf-8')
    with (data/'series.csv').open('w', newline='', encoding='utf-8') as f:
        writer=csv.DictWriter(f, fieldnames=list(observations[0]))
        writer.writeheader()
        writer.writerows(observations)
    print(f'Built static site: {output.resolve()}')


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'dist')
    build(parser.parse_args().output)
