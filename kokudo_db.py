# -*- coding: utf-8 -*-
import os
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase


database_proxy = Proxy()  # Create a proxy for our db.

SRID = 0

class PolygonField(Field):
    db_field = 'polygon'


class PointField(Field):
    db_field = 'point'


class LineStringField(Field):
    db_field = 'linestring'


class MultiPolygonField(Field):
    db_field = 'multipolygon'


class MultiPointField(Field):
    db_field = 'multipoint'


class MultiLineStringField(Field):
    db_field = 'multilinestring'


class AdministrativeDistrict(Model):
    """
    国土数値情報(行政区域)のモデル
    """
    PK_UID = PrimaryKeyField()
    prefectureName = TextField()
    subPrefectureName = TextField()
    countyName = TextField()
    cityName = TextField()
    administrativeAreaCode = TextField()
    geometry = PolygonField()


    class Meta:
        database = database_proxy


class BusRoute(Model):
    """
    国土数値情報（バスルート）のモデル
    """
    PK_UID = PrimaryKeyField()
    bsc = TextField()   # バス区分 1:路線バス(民間) 2:公営 3:コミュニティバス 4:デマンドバス 5:その他
    boc = TextField()   # 事業社名
    bln = TextField()   # バス系統
    rpd = FloatField()  # 平日運行頻度  
    rps = FloatField()  # 土曜日運行頻度
    rph = FloatField()  # 休日運行頻度
    rmk = TextField()   # 備考運行頻度
    geometry = MultiLineStringField()


    class Meta:
        database = database_proxy


class RailroadSection(Model):
    """
    国土数値情報(鉄道―路線)のモデル
    """
    PK_UID = PrimaryKeyField()
    railwayType = TextField()
    serviceProviderType = TextField()
    railwayLineName = TextField()
    operationCompany = TextField()
    geometry = LineStringField()


    class Meta:
        database = database_proxy


class Station(Model):
    """
    国土数値情報(鉄道―駅)のモデル
    """
    PK_UID = PrimaryKeyField()
    railwayType = TextField()
    serviceProviderType = TextField()
    railwayLineName = TextField()
    operationCompany = TextField()
    stationName = TextField()
    geometry = LineStringField()


    class Meta:
        database = database_proxy


class idx_AdministrativeDistrict_geometry(Model):
    pkid = PrimaryKeyField()
    xmin = FloatField()
    xmax = FloatField()
    ymin = FloatField()
    ymax = FloatField()
    class Meta:
        database = database_proxy


class idx_BusRoute_geometry(Model):
    pkid = PrimaryKeyField()
    xmin = FloatField()
    xmax = FloatField()
    ymin = FloatField()
    ymax = FloatField()
    class Meta:
        database = database_proxy


class idx_RailroadSection_geometry(Model):
    pkid = PrimaryKeyField()
    xmin = FloatField()
    xmax = FloatField()
    ymin = FloatField()
    ymax = FloatField()
    class Meta:
        database = database_proxy


class idx_Station_geometry(Model):
    pkid = IntegerField(primary_key=True)
    xmin = FloatField()
    xmax = FloatField()
    ymin = FloatField()
    ymax = FloatField()
    class Meta:
        database = database_proxy


def connect(path, spatialite_path, evn_sep=';'):
    os.environ["PATH"] = os.environ["PATH"] + evn_sep + os.path.dirname(spatialite_path)
    db = SqliteExtDatabase(path)
    database_proxy.initialize(db)
    db.field_overrides = {
      'polygon': 'POLYGON',
      'point': 'POINT',
      'linestring': 'LINESTRING',
      'multipolygon': 'MULTIPOLYGON',
      'multipoint': 'MULTIPOINT',
      'multilinestring': 'MULTILINESTRING',
    }
    db.load_extension(os.path.basename(spatialite_path))


def _merge_cond(pre_cond, cond):
    ret_cond = None
    if pre_cond:
        ret_cond = pre_cond & cond
    else:
        ret_cond = cond
    return ret_cond


def _get_table_base(tbl, filed_inf):
    param = []
    geometry_class = ['PolygonField', 'PointField', 'LineStringField', 'MultiPolygonField', 'MultiLineStringField']
    for f in filed_inf:
        f['fobj'] = getattr(tbl, f['field'])
        if f['fobj'].__class__.__name__ in geometry_class:
            f['field_ret'] = 'gjson_' + f['field']
            g = R('AsGeoJson(' + f['field'] + ')').alias(f['field_ret'])
            param.append(g)
        else:
            param.append(f['fobj'])
            f['field_ret'] = f['field']
    query = tbl.select(*param)

    cond = None
    for f in filed_inf:
        if f['cond']:
            cond = _merge_cond(cond, (f['fobj'] == f['cond']))
    rows = query.where(cond)
    ret = []
    for r in rows:
        item = {}
        for f in filed_inf:
           item[f['field']] = getattr(r, f['field_ret'])
        ret.append(item)
    return ret


def get_administrative_district(prefectureName=None, subPrefectureName=None, countyName=None, cityName=None, administrativeAreaCode=None):
    return _get_table_base(AdministrativeDistrict, 
       [
           {'field': 'prefectureName' , 'cond': prefectureName},
           {'field': 'subPrefectureName' , 'cond': subPrefectureName},
           {'field': 'countyName' , 'cond': countyName},
           {'field': 'cityName' , 'cond': cityName},
           {'field': 'administrativeAreaCode' , 'cond': administrativeAreaCode},
           {'field': 'geometry' , 'cond': None},
       ]
    )


def get_administrative_district_by_geometry(xmin, ymin, xmax, ymax):
    rows = database_proxy.get_conn().execute("""
      SELECT 
        PK_UID,
        prefectureName,
        subPrefectureName,
        countyName,
        cityName,
        administrativeAreaCode,
        AsGeoJson(geometry)
      FROM 
        AdministrativeDistrict 
        inner join idx_AdministrativeDistrict_geometry ON pkid = AdministrativeDistrict.PK_UID 
      WHERE 
          MBROverlaps(
            BuildMBR(xmin,ymin,xmax,ymax),
            BuildMBR(?, ?, ?, ?)
        );
    """,(xmin, ymin, xmax, ymax))
    ret  = []
    for r in rows:
        ret.append({
            'PK_UID' : r[0],
            'prefectureName' : r[1],
            'subPrefectureName' : r[2],
            'countryName' : r[3],
            'cityName' : r[4],
            'administrativeAreaCode' : r[5],
            'geometry' : r[6]
        })
    return ret


def get_bus_route(bsc=None, boc=None, bln=None, rpd=None, rps=None, rph=None, rmk=None):
    return _get_table_base(BusRoute, 
       [
           {'field': 'bsc' , 'cond': bsc},
           {'field': 'boc' , 'cond': boc},
           {'field': 'bln' , 'cond': bln},
           {'field': 'rpd' , 'cond': rpd},
           {'field': 'rps' , 'cond': rps},
           {'field': 'rph' , 'cond': rph},
           {'field': 'rmk' , 'cond': rmk},
           {'field': 'geometry' , 'cond': None},
       ]
    )


def get_bus_route_by_geometry(xmin, ymin, xmax, ymax):
    rows = database_proxy.get_conn().execute("""
      SELECT 
        PK_UID,
        bsc,
        boc,
        bln,
        rpd,
        rps,
        rph,
        rmk,
        AsGeoJson(geometry)
      FROM 
        BusRoute 
        inner join idx_BusRoute_geometry ON pkid = BusRoute.PK_UID 
      WHERE 
          MBROverlaps(
            BuildMBR(xmin,ymin,xmax,ymax),
            BuildMBR(?, ?, ?, ?)
        );
    """,(xmin, ymin, xmax, ymax))
    ret  = []
    for r in rows:
        ret.append({
            'PK_UID' : r[0],
            'bsc' : r[1],
            'boc' : r[2],
            'bln' : r[3],
            'rpd' : r[4],
            'rps' : r[5],
            'rph' : r[6],
            'rmk' : r[7],
            'geometry' : r[8]
        })
    return ret


def get_railroad_section(railwayType=None, serviceProviderType=None, railwayLineName=None, operationCompany=None):
    return _get_table_base(RailroadSection, 
       [
           {'field': 'railwayType' , 'cond': railwayType},
           {'field': 'serviceProviderType' , 'cond': serviceProviderType},
           {'field': 'railwayLineName' , 'cond': railwayLineName},
           {'field': 'operationCompany' , 'cond': operationCompany},
           {'field': 'geometry' , 'cond': None},
       ]
    )


def get_railroad_section_by_geometry(xmin, ymin, xmax, ymax):
    rows = database_proxy.get_conn().execute("""
      SELECT 
        PK_UID,
        railwayType,
        serviceProviderType,
        railwayLineName,
        operationCompany,
        AsGeoJson(geometry)
      FROM 
        RailroadSection 
        inner join idx_RailroadSection_geometry ON pkid = RailroadSection.PK_UID 
      WHERE 
          MBROverlaps(
            BuildMBR(xmin,ymin,xmax,ymax),
            BuildMBR(?, ?, ?, ?)
        );
    """,(xmin, ymin, xmax, ymax))
    ret  = []
    for r in rows:
        ret.append({
            'PK_UID' : r[0],
            'railwayType' : r[1],
            'serviceProviderType' : r[2],
            'railwayLineName' : r[3],
            'operationCompany' : r[4],
            'geometry' : r[5]
        })
    return ret


def get_station(railwayType=None, serviceProviderType=None, railwayLineName=None, operationCompany=None, stationName=None):
    return _get_table_base(Station, 
       [
           {'field': 'railwayType' , 'cond': railwayType},
           {'field': 'serviceProviderType' , 'cond': serviceProviderType},
           {'field': 'railwayLineName' , 'cond': railwayLineName},
           {'field': 'operationCompany' , 'cond': operationCompany},
           {'field': 'stationName' , 'cond': stationName},
           {'field': 'geometry' , 'cond': None},
       ]
    )


def get_station_by_geometry(xmin, ymin, xmax, ymax):
    rows = database_proxy.get_conn().execute("""
      SELECT 
        Station.PK_UID,
        Station.railwayType,
        Station.serviceProviderType,
        Station.railwayLineName,
        Station.operationCompany,
        Station.StationName,
        AsGeoJson(Station.geometry)
      FROM 
        Station 
        inner join idx_Station_geometry ON pkid = Station.PK_UID 
      WHERE 
          MBROverlaps(
            BuildMBR(xmin,ymin,xmax,ymax),
            BuildMBR(?, ?, ?, ?)
        );
    """,(xmin, ymin, xmax, ymax))
    ret  = []
    for r in rows:
        ret.append({
            'PK_UID' : r[0],
            'railwayType' : r[1],
            'serviceProviderType' : r[2],
            'railwayLineName' : r[3],
            'operationCompany' : r[4],
            'StationName' : r[5],
            'geometry' : r[6]
        })
    return ret
