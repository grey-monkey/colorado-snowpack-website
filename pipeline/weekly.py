"""Deterministic facts from one accepted release; never sends email."""
from datetime import date,datetime,timedelta
from zoneinfo import ZoneInfo
from .proof import percentage


def facts(release,end=None,today=None):
    end=date.fromisoformat(end or release['observation_date'])
    today=today or datetime.now(ZoneInfo('America/Denver')).date()
    if end>date.fromisoformat(release['observation_date']):
        raise ValueError('Reporting interval extends beyond accepted observations')
    start=end-timedelta(days=7)
    rows={(r['region_id'],r['observation_date']):r for r in release['observations']}
    result=[]
    for p in release['metadata']['products']:
        a=rows.get((p['region_id'],start.isoformat()))
        b=rows.get((p['region_id'],end.isoformat()))
        complete=a is not None and b is not None and a['swe_inches'] is not None and b['swe_inches'] is not None
        pa=percentage(a['swe_inches'],a['median_inches']) if a else None
        pb=percentage(b['swe_inches'],b['median_inches']) if b else None
        result.append(dict(region_id=p['region_id'],start_swe_inches=a['swe_inches'] if a else None,
            end_swe_inches=b['swe_inches'] if b else None,
            net_swe_change_inches=b['swe_inches']-a['swe_inches'] if complete else None,
            percentage_point_change=pb-pa if pa is not None and pb is not None else None,
            comparison_status='available_with_coverage_caution' if complete else 'missing_endpoint'))
    return dict(schema_version='1.0.0',release_id=release['id'],start=start.isoformat(),end=end.isoformat(),
        interval='end observation minus observation exactly seven calendar days earlier',
        delivery_eligible=0<=(today-end).days<=2 and all(r['comparison_status']!='missing_endpoint' for r in result),
        limitations=['Daily station coverage not independently verified','Net SWE change is not snowfall'],regions=result)
