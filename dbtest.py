#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from kokudo_db import *
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
import json

def _create_geojsonX(ret):
    res = {'type' : 'FeatureCollection', 'features': []}
    cnt = 0
    for r in ret:
        print cnt
        item = {
          'type' : 'Feature',
          'geometry':json.loads(r['geometry']),
          'properties': {}
        }
        for k, i in r.items():
            if not k == 'geometry':
                item['properties'][k] = i
        res['features'].append(item)
        cnt = cnt + 1
    return res
    
def _create_geojson(ret):
    res = '{"type": "FeatureCollection", "features": ['
    cnt = 0
    for r in ret:
        print cnt
        prop = {}
        for k, i in r.items():
            if not k == 'geometry':
                prop[k] = i
        item = '{"type":"Feature", "geometry":"%s", "properties":"%s"}' % (r['geometry'], json.dumps(prop))
        if i == 0:
          res = res + item
        else:
          res = res + ',' + item
        cnt = cnt + 1
    res = res + ']}'
    return res

connect('kokudo.sqlite', 'C:\\tool\\spatialite\\mod_spatialite-4.2.0-win-x86\\mod_spatialite.dll')
print 'start...'
#ret = get_railroad_section(railwayLineName=u'いわて銀河鉄道線', operationCompany=u'アイジーアールいわて銀河鉄道')
#ret = get_bus_route(boc=u'JRバステック（株）')
#ret = get_administrative_district_route(prefectureName=u'秋田県')
ret = get_bus_route_by_geometry(float("139.47905321972655"),35.47379443660201,140.02836962597655,35.80860811548238)
print "x", len(ret)
print json.dumps(_create_geojsonX(ret))
#for r in ret:
#    print r
