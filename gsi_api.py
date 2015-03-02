# -*- coding: utf-8 -*-
import urllib
import urllib2
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import json


database_proxy = Proxy()  # Create a proxy for our db.


def get_elevation_by_api(long, lat):
    """
    標高値の取得
    http://portal.cyberjapan.jp/help/development/api.html
    """
    url = ('http://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php?lon=%f&lat=%f&outtype=JSON' % (long, lat))
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    conn = opener.open(req)
    cont = conn.read()
    ret = json.loads(cont)
    return ret


def str_isfloat(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


class ElevationCache(Model):
    """
    標高のキャッシュテーブル
    """
    lat = FloatField(index=True)
    long = FloatField(index=True)
    hsrc = TextField(index=True)
    elevation = FloatField(null=True)


    class Meta:
        database = database_proxy

def connect(path):
    db = SqliteExtDatabase(path)
    database_proxy.initialize(db)


def setup(path):
    connect(path)
    database_proxy.create_tables([ElevationCache], True)


def get_elevation(long, lat):
    try:
        ret = ElevationCache.get((ElevationCache.long==long) & (ElevationCache.lat==lat))
        return {'elevation': ret.elevation, 'hsrc': ret.hsrc}

    except ElevationCache.DoesNotExist:
        ret = get_elevation_by_api(long, lat)
        elevation = ret['elevation']
        if not str_isfloat(elevation):
            elevation = None
        ElevationCache.create(
            long = long,
            lat = lat,
            elevation = elevation,
            hsrc = ret['hsrc']
        )
        return ret


class GsiConvertError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def convert_geojson(json):
    for feature in json['features']:
        if feature['geometry']['type'] == 'LineString':
            prop = {}
            start = feature['geometry']['coordinates'][0]
            end = feature['geometry']['coordinates'][len(feature['geometry']['coordinates'])-1]
            start_elevation = get_elevation(start[0], start[1])
            end_elevation = get_elevation(end[0], end[1])
            feature['properties']['start_elevation'] = start_elevation['elevation']
            feature['properties']['end_elevation'] = end_elevation['elevation']
        else:
            raise GsiConvertError('unexpected feature type')
    return json

if __name__ == '__main__':
    setup('elevation_cache.sqlite')
    #print get_elevation_by_api(133, 39)
    #print get_elevation_by_api(139.766084, 35.681382)

    print get_elevation(133, 39)
    print get_elevation(139.766084, 35.681382)
    with open('get_railroad_section.geojson' , 'rb') as f:
        cont = f.read()
        print convert_geojson(json.loads(cont))
