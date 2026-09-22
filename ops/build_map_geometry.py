"""Reproduce the preview geometry from archived official NRCS/Census GeoJSON.
No network calls, smoothing, inferred boundaries, or production publication.
"""
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASINS={'Laramie and North Platte':'co-laramie-north-platte','South Platte':'co-south-platte','Arkansas':'co-arkansas','Upper Rio Grande':'co-upper-rio-grande','Colorado Headwaters':'co-colorado-headwaters','Gunnison':'co-gunnison','San Miguel-Dolores-Animas-San Juan':'co-san-miguel-dolores-animas-san-juan','Yampa-White-Little Snake':'co-yampa-white-little-snake'}
def build():
    source=ROOT/'evidence/map'
    raw=json.loads((source/'co_8.geojson').read_text())
    state=json.loads((source/'colorado-state.geojson').read_text())['features'][0]
    rad=math.pi/180
    n=(math.sin(37*rad)+math.sin(41*rad))/2
    c=math.cos(37*rad)**2+2*n*math.sin(37*rad)
    rho0=math.sqrt(c-2*n*math.sin(39*rad))/n
    def project(p):
        lon,lat=p[:2];rho=math.sqrt(c-2*n*math.sin(lat*rad))/n;t=n*(lon+105.5)*rad
        return rho*math.sin(t),rho0-rho*math.cos(t)
    points=[project(p) for ring in state['geometry']['coordinates'] for p in ring]
    xmin=min(p[0] for p in points);xmax=max(p[0] for p in points)
    ymin=min(p[1] for p in points);ymax=max(p[1] for p in points)
    scale=min(660/(xmax-xmin),450/(ymax-ymin))
    def xy(p):
        x,y=project(p)
        return [round(360+(x-(xmin+xmax)/2)*scale,2),round(255-(y-(ymin+ymax)/2)*scale,2)]
    def path(g):
        polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
        return ' '.join('M'+'L'.join(','.join(map(str,xy(p))) for p in ring)+'Z' for poly in polys for ring in poly)
    items=[]
    for f in raw['features']:
        p=f['properties'];items.append({'id':BASINS.get(p['name']),'name':p['name'],'source_id':p['id'],'path':path(f['geometry']),'label':xy([p['x'],p['y']])})
    result={'width':720,'height':510,'state':path(state['geometry']),'basins':items,'source':'https://nwcc-apps.sc.egov.usda.gov/awdb/basin-defs/geojson/co_8.geojson','projection':'Albers equal-area; center 39 N, 105.5 W; standard parallels 37/41 N','note':'Official NRCS generalized map polygons. SVG clipped to Census Colorado boundary; readings describe full NRCS reporting basins.'}
    (ROOT/'site/assets/colorado-basins.json').write_text(json.dumps(result,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
if __name__=='__main__':build()
