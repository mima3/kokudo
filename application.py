# coding=utf-8
from bottle import get, post, template, request, Bottle, response, redirect, abort
from json import dumps
import os
import json
from collections import defaultdict
import time
import cgi
import urllib
import kokudo_db
import peewee


app = Bottle()


def setup(conf):
    global app
    kokudo_db.connect(conf.get('database', 'path'), conf.get('database', 'mod_path'), conf.get('database', 'sep'))


@app.get('/')
def Home():
    return 'Kokudo page...'


def _create_geojson(ret):

    res = {'type' : 'FeatureCollection', 'features': []}
    for r in ret:
        item = {
          'type' : 'Feature',
          'geometry':json.loads(r['geometry']),
          'properties': {}
        }
        for k, i in r.items():
            if not k == 'geometry':
                item['properties'][k] = i
        res['features'].append(item)
    return res


@app.get('/json/get_administrative_district')
def get_administrative_district():
    prefectureName = request.query.prefectureName
    subPrefectureName = request.query.subPrefectureName
    countyName = request.query.countyName
    cityName = request.query.cityName
    administrativeAreaCode = request.query.administrativeAreaCode

    ret = kokudo_db.get_administrative_district_route(prefectureName, subPrefectureName, countyName, cityName, administrativeAreaCode)

    response.content_type = 'application/json;charset=utf-8'
    res = _create_geojson(ret)
    return json.dumps(res)


@app.get('/json/get_administrative_district_by_geometry')
def get_administrative_district_by_geometry():
    swlat = float(request.query.swlat)
    swlng = float(request.query.swlng)
    nelat = float(request.query.nelat)
    nelng = float(request.query.nelng)
    ret = kokudo_db.get_administrative_district_by_geometry(swlng, swlat, nelng, nelat)

    response.content_type = 'application/json;charset=utf-8'
    res = _create_geojson(ret)
    return json.dumps(res)


@app.get('/json/get_bus_route_by_geometry')
def get_bus_route_by_geometry():
    swlat = float(request.query.swlat)
    swlng = float(request.query.swlng)
    nelat = float(request.query.nelat)
    nelng = float(request.query.nelng)
    ret = kokudo_db.get_bus_route_by_geometry(swlng, swlat, nelng, nelat)

    response.content_type = 'application/json;charset=utf-8'
    res = _create_geojson(ret)
    return json.dumps(res)


@app.get('/json/get_bus_route')
def get_bus_route():
    bsc = request.query.bsc
    boc = request.query.boc
    bln = request.query.bln
    rpd = request.query.rpd
    rps = request.query.rps
    rph = request.query.rph
    rmk = request.query.rmk

    ret = kokudo_db.get_bus_route(bsc, boc, bln, rpd, rps, rph, rmk)

    response.content_type = 'application/json;charset=utf-8'
    res = _create_geojson(ret)
    return json.dumps(res)


@app.get('/json/get_railroad_section_by_geometry')
def get_railroad_section_by_geometry():
    swlat = float(request.query.swlat)
    swlng = float(request.query.swlng)
    nelat = float(request.query.nelat)
    nelng = float(request.query.nelng)
    ret = kokudo_db.get_railroad_section_by_geometry(swlng, swlat, nelng, nelat)

    response.content_type = 'application/json;charset=utf-8'
    res = _create_geojson(ret)
    return json.dumps(res)


@app.get('/json/get_railroad_section')
def get_railroad_section():
    railwayType = request.query.railwayType
    serviceProviderType = request.query.serviceProviderType
    railwayLineName = request.query.railwayLineName
    operationCompany = request.query.operationCompany
    ret = kokudo_db.get_railroad_section(railwayType, serviceProviderType, railwayLineName, operationCompany)

    response.content_type = 'application/json;charset=utf-8'
    res = _create_geojson(ret)
    return json.dumps(res)


@app.get('/json/get_station_by_geometry')
def get_station_by_geometry():
    swlat = float(request.query.swlat)
    swlng = float(request.query.swlng)
    nelat = float(request.query.nelat)
    nelng = float(request.query.nelng)
    ret = kokudo_db.get_station_by_geometry(swlng, swlat, nelng, nelat)

    response.content_type = 'application/json;charset=utf-8'
    res = _create_geojson(ret)
    return json.dumps(res)


@app.get('/json/get_station')
def get_station():
    railwayType = request.query.railwayType
    serviceProviderType = request.query.serviceProviderType
    railwayLineName = request.query.railwayLineName
    operationCompany = request.query.operationCompany
    stationName = request.query.stationName
    ret = kokudo_db.get_station(railwayType, serviceProviderType, railwayLineName, operationCompany, stationName)

    response.content_type = 'application/json;charset=utf-8'
    res = _create_geojson(ret)
    return json.dumps(res)
