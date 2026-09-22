import copy
import json
import tempfile
import unittest
from datetime import datetime,timezone,date
from pathlib import Path
from pipeline.refresh import refresh,connect,read_release,candidate,Rejected
from pipeline.proof import BASE,PRODUCTS,chart_payload
from pipeline.publish import publish
from pipeline.weekly import facts

EVIDENCE=Path(__file__).resolve().parents[1]/'evidence/2026-09-21'
NOW=datetime(2026,9,21,18,tzinfo=timezone.utc)


def fixtures():
    return {BASE+p+'.'+extension:(EVIDENCE/(key+suffix)).read_bytes()
        for key,(_,_,p) in PRODUCTS.items()
        for extension,suffix in [('json','.json'),('html','-chart.html')]}


def altered(sources,md='09-22',value=.1):
    """Clearly synthetic test payloads; edited chart and export, never production."""
    result=copy.deepcopy(sources)
    for _,(_,_,p) in PRODUCTS.items():
        raw=json.loads(result[BASE+p+'.json']);i=next(i for i,r in enumerate(raw) if r['date']==md)
        raw[i]['2026']=value;result[BASE+p+'.json']=json.dumps(raw).encode()
        html=result[BASE+p+'.html'].decode();traces,layout=chart_payload(html)
        for t in traces:
            if t.get('meta',{}).get('wateryear')=='2026':
                t['y'] += [None]*max(0,i+1-len(t['y']));t['y'][i]=value
        for a in layout['annotations']:
            if a['text'].startswith('Current as of') and md=='09-22':a['text']=a['text'].replace('09/21/2026','09/22/2026')
        result[BASE+p+'.html']=('Plotly.newPlot("test",'+json.dumps(traces)+','+json.dumps(layout)+')').encode()
    return result


class AcceptedFlow(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store=Path(self.temp.name)/'snowpack.sqlite';self.source=fixtures()

    def read(self):
        db=connect(self.store)
        try:return read_release(db)
        finally:db.close()

    def test_accept_reject_outage_recovery_and_idempotence(self):
        accepted=refresh(self.store,self.source.__getitem__,NOW);self.assertEqual(accepted['status'],'accepted')
        initial=self.read();self.assertEqual(initial['observations'][-1]['observation_date'],'2026-09-21')
        again=refresh(self.store,self.source.__getitem__,NOW);self.assertEqual(again['status'],'unchanged')
        self.assertEqual(again['changed_observations'],0)
        def outage(url):raise OSError('simulated network outage')
        self.assertEqual(refresh(self.store,outage,NOW)['status'],'retrieval_failed')
        self.assertEqual(self.read(),initial)
        bad=copy.deepcopy(self.source);key=next(k for k in bad if k.endswith('.json'))
        rows=json.loads(bad[key]);rows[100]['2026']=-1;bad[key]=json.dumps(rows).encode()
        self.assertEqual(refresh(self.store,bad.__getitem__,NOW)['status'],'validation_failed')
        self.assertEqual(self.read(),initial)
        recovered=refresh(self.store,altered(self.source).__getitem__,NOW.replace(day=22))
        self.assertEqual(recovered['status'],'accepted');self.assertEqual(recovered['changed_observations'],2)
        self.assertEqual(self.read()['observation_date'],'2026-09-22')
        db=connect(self.store)
        try:self.assertEqual(read_release(db,1),initial)
        finally:db.close()

    def test_missing_latest_and_stale_sources_do_not_replace_head(self):
        refresh(self.store,self.source.__getitem__,NOW);initial=self.read()
        self.assertEqual(refresh(self.store,altered(self.source,md='09-21',value=None).__getitem__,NOW)['status'],'source_missing')
        self.assertEqual(refresh(self.store,self.source.__getitem__,NOW.replace(day=25))['status'],'source_missing')
        self.assertEqual(self.read(),initial)

    def test_measured_zero_is_accepted_not_missing(self):
        result=refresh(self.store,altered(self.source,value=0).__getitem__,NOW.replace(day=22))
        self.assertEqual(result['status'],'accepted')
        latest=[r for r in self.read()['observations'] if r['observation_date']=='2026-09-22']
        self.assertTrue(all(r['swe_inches']==0 and r['percent_of_median'] is None for r in latest))

    def test_interior_missing_revision_preserved_and_recap_withheld(self):
        refresh(self.store,self.source.__getitem__,NOW)
        result=refresh(self.store,altered(self.source,md='09-14',value=None).__getitem__,NOW)
        self.assertEqual(result['changed_observations'],2)
        recap=facts(self.read(),today=date(2026,9,21))
        self.assertFalse(recap['delivery_eligible']);self.assertIsNone(recap['regions'][0]['net_swe_change_inches'])

    def test_weekly_exact_interval_and_nonzero_winter_median(self):
        refresh(self.store,self.source.__getitem__,NOW);release=self.read()
        recap=facts(release,today=date(2026,9,21));self.assertEqual(recap['start'],'2026-09-14')
        self.assertTrue(recap['delivery_eligible']);self.assertIsNone(recap['regions'][0]['percentage_point_change'])
        winter=facts(release,end='2026-02-01',today=date(2026,2,1))
        self.assertEqual(winter['start'],'2026-01-25');self.assertIsNotNone(winter['regions'][0]['percentage_point_change'])
        leap=facts(release,end='2024-03-01',today=date(2024,3,1));self.assertEqual(leap['start'],'2024-02-23')
        rollover=facts(release,end='2025-10-03',today=date(2025,10,3));self.assertEqual(rollover['start'],'2025-09-26')
        self.assertFalse(facts(release,today=date(2026,9,25))['delivery_eligible'])

    def test_publish_pins_consistent_release_and_retains_it_on_failure(self):
        refresh(self.store,self.source.__getitem__,NOW);public=Path(self.temp.name)/'public'
        publish(self.store,public);path=public/'data/releases/1'
        for asset in ('longs-peak.webp','manrope-latin.woff2','OFL-Manrope.txt'):
            self.assertEqual((public/'assets'/asset).read_bytes(),(EVIDENCE.parents[1]/'site/assets'/asset).read_bytes())
        before=(path/'snapshot.json').read_bytes();snapshot=json.loads(before)
        exported=json.loads((path/'series.json').read_text())
        self.assertEqual(snapshot['release_id'],exported['metadata']['release_id'])
        region=snapshot['regions'][0];i=region['dates'].index('09-21')
        row=next(r for r in exported['observations'] if r['region_id']==region['id'] and r['observation_date']=='2026-09-21')
        self.assertEqual(region['years']['2026'][i],row['swe_inches'])
        self.assertIn('data/releases/1/snapshot.json',(public/'index.html').read_text())
        def outage(url):raise OSError()
        refresh(self.store,outage,NOW);publish(self.store,public)
        self.assertEqual((path/'snapshot.json').read_bytes(),before)
        self.assertEqual(json.loads((public/'data/health.json').read_text())['status'],'retrieval_failed')
        refresh(self.store,altered(self.source).__getitem__,NOW.replace(day=22));publish(self.store,public)
        self.assertIn('data/releases/2/snapshot.json',(public/'index.html').read_text())
        self.assertEqual((path/'snapshot.json').read_bytes(),before)

    def test_no_accepted_data_does_not_overwrite_existing_site(self):
        output=Path(self.temp.name)/'public';output.mkdir();(output/'index.html').write_text('last good')
        with self.assertRaises(ValueError):publish(self.store,output)
        self.assertEqual((output/'index.html').read_text(),'last good')
