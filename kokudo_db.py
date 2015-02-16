# -*- coding: utf-8 -*-
import os
import sys
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import math
import re
from kanji import convert_integerstring
import glob
import csv
import StringIO

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/pyshp')
import shapefile


database_proxy = Proxy()  # Create a proxy for our db.

SRID = 4326


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
    bsc = IntegerField()   # バス区分 1:路線バス(民間) 2:公営 3:コミュニティバス 4:デマンドバス 5:その他
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


class SedimentDisasterHazardAreaSurface(Model):
    """
    土砂災害危険箇所データ(面)のモデル
    """
    PK_UID = PrimaryKeyField()
    prefectureName = TextField(index=True)
    hazardAreaType = IntegerField()
    remarks = TextField()
    geometry = PolygonField()

    class Meta:
        database = database_proxy


class SedimentDisasterHazardAreaLine(Model):
    """
    土砂災害危険箇所データ(線)のモデル
    """
    PK_UID = PrimaryKeyField()
    prefectureName = TextField(index=True)
    hazardAreaType = IntegerField()
    remarks = TextField()
    geometry = LineStringField()

    class Meta:
        database = database_proxy


class SedimentDisasterHazardAreaPoint(Model):
    """
    土砂災害危険箇所データ(線)のモデル
    """
    PK_UID = PrimaryKeyField()
    prefectureName = TextField(index=True)
    hazardAreaType = IntegerField()
    remarks = TextField()
    geometry = PointField()

    class Meta:
        database = database_proxy


class ExpectedFloodArea(Model):
    """
    国土数値情報　浸水想定区域データ
    """
    PK_UID = PrimaryKeyField()
    prefectureName = TextField(index=True)
    waterDepth = IntegerField()
    attributeId = TextField()
    geometry = PolygonField()

    class Meta:
        database = database_proxy


class ExpectedFloodAreaAttribute(Model):
    """
    国土数値情報　浸水想定区域データ の属性情報
    """
    PK_UID = PrimaryKeyField()
    attributeId = TextField(index=True)
    prefectureName = TextField(index=True)
    creatingType = IntegerField() # 作成種別コード 
    creatingBody = TextField()    # 作成主体 当該浸水想定区域図を作成した機関名。
    designatedDate = TextField()  # 指定年月日 当該浸水想定区域を指定した年月日
    announcementNumber = TextField()  # 告示番号 当該浸水想定区域を告示した際の告示番号。
    targetRiver  = TextField()    # 対象となる洪水予報河川
    designedStorm = TextField()   # 指定の前提となる計画降雨
    municipalGovernments  = TextField()  # 関係市町村
    description = TextField()        # 説明
    remarks = TextField()         # その他計算条件等

    class Meta:
        database = database_proxy


class Gust(Model):
    """
    国土数値情報　竜巻等の突風データ の属性情報
    """
    gustNo = IntegerField(primary_key=True)
    type = TextField()
    fujitaScale = TextField()
    damageAreaWidth = TextField()
    damageAreaLength = TextField()
    passingSpeed = IntegerField()
    continuanceTime = IntegerField()
    rotationDirection = TextField()
    appearancePointType = TextField()
    atmosphericPressureDirection = TextField()
    feature = TextField()

    class Meta:
        database = database_proxy


class GustDetail(Model):
    """
    国土数値情報　竜巻等の突風データ の発生・消失の詳細
    """
    id = PrimaryKeyField()
    gustNo = ForeignKeyField(Gust, related_name='details')
    detailType = IntegerField()             # 0:発生 1:消失
    occurrenceDate = DateField()            # データの発生日時
    dateErrorRange = TextField()            # 誤差範囲
    prefectureName = TextField()
    cityName = TextField()
    address = TextField()
    detailPoint = PointField()
    latErrorRage = TextField()
    longErrorRage = TextField()

    class Meta:
        database = database_proxy
        indexes = (
            (('gustNo', 'detailType'), True),
        )


class GustMovementDirection(Model):
    """
    国土数値情報　竜巻等の突風データ の当該竜巻等の突風移動方向
    """
    id = PrimaryKeyField()
    gustNo = ForeignKeyField(Gust, related_name='movementDirections')
    movementDirection = TextField()

    class Meta:
        database = database_proxy
        indexes = (
            (('gustNo', 'movementDirection'), False),
        )

class GustAtmosphericPressure(Model):
    """
    国土数値情報　竜巻等の突風データ の 総観場詳細 
    """
    id = PrimaryKeyField()
    gustNo = ForeignKeyField(Gust, related_name='atmosphericPressures')
    atmosphericPressureDirection = TextField()

    class Meta:
        database = database_proxy
        indexes = (
            (('gustNo', 'atmosphericPressureDirection'), False),
        )


class Address(Model):
    """
    住所の情報
    """
    id = PrimaryKeyField()
    address = TextField(index=True)
    lat = FloatField()
    long = FloatField()

    class Meta:
        database = database_proxy


def connect(path, spatialite_path, evn_sep=';'):
    """
    データベースへの接続
    @param path sqliteのパス
    @param spatialite_path mod_spatialiteへのパス
    @param env_sep 環境変数PATHの接続文字 WINDOWSは; LINUXは:
    """
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


def setup(path, spatialite_path, evn_sep=';'):
    """
    データベースの作成
    @param path sqliteのパス
    @param spatialite_path mod_spatialiteへのパス
    @param env_sep 環境変数PATHの接続文字 WINDOWSは; LINUXは:
    """
    connect(path, spatialite_path, evn_sep)
    database_proxy.create_tables([Address, ExpectedFloodAreaAttribute], True)
    database_proxy.get_conn().execute('SELECT InitSpatialMetaData()')

    # 国土数値情報(行政区域)のモデル
    database_proxy.get_conn().execute("""
        CREATE TABLE IF NOT EXISTS "AdministrativeDistrict" (
          "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
          "prefectureName" TEXT,
          "subPrefectureName" TEXT ,
          "countyName" TEXT ,
          "cityName" TEXT ,
          "administrativeAreaCode" TEXT);
    """)
    database_proxy.get_conn().execute("""
        Select AddGeometryColumn ("AdministrativeDistrict", "Geometry", ?, "POLYGON", 2);
    """, (SRID,))
    database_proxy.get_conn().execute("""
        SELECT CreateSpatialIndex("AdministrativeDistrict", "geometry")
    """)

    # 国土数値情報(鉄道―路線)のモデル
    database_proxy.get_conn().execute("""
        CREATE TABLE IF NOT EXISTS "RailroadSection" (
          "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
          "railwayType" TEXT,
          "serviceProviderType" TEXT ,
          "railwayLineName" TEXT ,
          "operationCompany" TEXT);
    """)
    database_proxy.get_conn().execute("""
        Select AddGeometryColumn ("RailroadSection", "geometry", ?, "LINESTRING", 2);
    """, (SRID,))
    database_proxy.get_conn().execute("""
        SELECT CreateSpatialIndex("RailroadSection", "geometry")
    """)

    # 国土数値情報(鉄道―駅)のモデル
    database_proxy.get_conn().execute("""
        CREATE TABLE IF NOT EXISTS "Station" (
          "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
          "railwayType" TEXT,
          "serviceProviderType" TEXT ,
          "railwayLineName" TEXT ,
          "stationName" TEXT,
          "operationCompany" TEXT);
    """)
    database_proxy.get_conn().execute("""
        Select AddGeometryColumn ("Station", "geometry", ?, "LINESTRING", 2);
    """, (SRID,))
    database_proxy.get_conn().execute("""
        SELECT CreateSpatialIndex("Station", "geometry")
    """)

    # 国土数値情報（バスルート）のモデル
    database_proxy.get_conn().execute("""
        CREATE TABLE IF NOT EXISTS "BusRoute" (
          "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
          "bsc" INTEGER,
          "boc" TEXT ,
          "bln" TEXT ,
          "rpd" DOUBLE,
          "rps" DOUBLE,
          "rph" DOUBLE,
          "rmk" TEXT);
    """)
    database_proxy.get_conn().execute("""
        Select AddGeometryColumn ("BusRoute", "geometry", ?, "MULTILINESTRING", 2);
    """, (SRID,))
    database_proxy.get_conn().execute("""
        SELECT CreateSpatialIndex("BusRoute", "geometry")
    """)


    # 土砂災害危険箇所データ(面)のモデル
    database_proxy.get_conn().execute("""
        CREATE TABLE IF NOT EXISTS "SedimentDisasterHazardAreaSurface" (
          "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
          "prefectureName" TEXT,
          "hazardAreaType" INTEGER ,
          "remarks" TEXT);
    """)
    database_proxy.get_conn().execute("""
        Select AddGeometryColumn ("SedimentDisasterHazardAreaSurface", "geometry", ?, "POLYGON", 2);
    """, (SRID,))
    database_proxy.get_conn().execute("""
        SELECT CreateSpatialIndex("SedimentDisasterHazardAreaSurface", "geometry")
    """)

    # 土砂災害危険箇所データ(線)のモデル
    database_proxy.get_conn().execute("""
        CREATE TABLE IF NOT EXISTS "SedimentDisasterHazardAreaLine" (
          "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
          "prefectureName" TEXT,
          "hazardAreaType" INTEGER ,
          "remarks" TEXT);
    """)
    database_proxy.get_conn().execute("""
        Select AddGeometryColumn ("SedimentDisasterHazardAreaLine", "geometry", ?, "LINESTRING", 2);
    """, (SRID,))
    database_proxy.get_conn().execute("""
        SELECT CreateSpatialIndex("SedimentDisasterHazardAreaLine", "geometry")
    """)


    # 土砂災害危険箇所データ(点)のモデル
    database_proxy.get_conn().execute("""
        CREATE TABLE IF NOT EXISTS "SedimentDisasterHazardAreaPoint" (
          "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
          "prefectureName" TEXT,
          "hazardAreaType" INTEGER ,
          "remarks" TEXT);
    """)
    database_proxy.get_conn().execute("""
        Select AddGeometryColumn ("SedimentDisasterHazardAreaPoint", "geometry", ?, "POINT", 2);
    """, (SRID,))
    database_proxy.get_conn().execute("""
        SELECT CreateSpatialIndex("SedimentDisasterHazardAreaPoint", "geometry")
    """)

    # 土砂災害危険箇所データ(面)のモデル
    database_proxy.get_conn().execute("""
        CREATE TABLE IF NOT EXISTS "ExpectedFloodArea" (
          "PK_UID" INTEGER PRIMARY KEY AUTOINCREMENT,
          "prefectureName" TEXT,
          "waterDepth" INTEGER ,
          "attributeId" INTEGER);
    """)
    database_proxy.get_conn().execute("""
        Select AddGeometryColumn ("ExpectedFloodArea", "geometry", ?, "POLYGON", 2);
    """, (SRID,))
    database_proxy.get_conn().execute("""
        SELECT CreateSpatialIndex("ExpectedFloodArea", "geometry")
    """)


def _merge_cond(pre_cond, cond):
    """
    SQLの条件文を結合
    @param pre_cond 現在の条件
    @param cond 新しい条件
    @return 結合した条件
    """
    ret_cond = None
    if pre_cond:
        ret_cond = pre_cond & cond
    else:
        ret_cond = cond
    return ret_cond


def _get_table_base(tbl, filed_inf):
    """
    指定のテーブルを条件を付与して取得する
    Geometryの列の場合はJSONで取得
    @param tbl テーブルモデルのオブジェクト
    @param filed_inf 列 {'field' : フィールド名, 'cond' : 条件 Noneの時は検索しない}
    @return 取得した結果
    """
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
    """
    行政区域の取得
    @param prefectureName 検索条件：県　Noneの場合は検索対象外
    @param subPrefectureName 検索条件：小区　Noneの場合は検索対象外
    @param countyName 検索条件：群　Noneの場合は検索対象外
    @param cityName 検索条件：市　Noneの場合は検索対象外
    @param administrativeAreaCode 検索条件：コード　Noneの場合は検索対象外
    @return 取得した結果
    """
    return _get_table_base(AdministrativeDistrict, [
        {'field': 'prefectureName', 'cond': prefectureName},
        {'field': 'subPrefectureName', 'cond': subPrefectureName},
        {'field': 'countyName', 'cond': countyName},
        {'field': 'cityName', 'cond': cityName},
        {'field': 'administrativeAreaCode', 'cond': administrativeAreaCode},
        {'field': 'geometry', 'cond': None},
    ])


def get_administrative_district_by_geometry(xmin, ymin, xmax, ymax):
    """
    選択した範囲に重なる行政区域の取得
    @param xmin 取得範囲
    @param ymin 取得範囲
    @param xmax 取得範囲
    @param ymax 取得範囲
    @return 取得した結果
    """
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
    """, (xmin, ymin, xmax, ymax))
    ret = []
    for r in rows:
        ret.append({
            'PK_UID': r[0],
            'prefectureName': r[1],
            'subPrefectureName': r[2],
            'countryName': r[3],
            'cityName': r[4],
            'administrativeAreaCode': r[5],
            'geometry': r[6]
        })
    return ret


def get_bus_route(bsc=None, boc=None, bln=None, rpd=None, rps=None, rph=None, rmk=None):
    """
    バスルートの取得
    @param bsc 検索条件：コード　Noneの場合は検索対象外
    @param boc 検索条件：運営会社　Noneの場合は検索対象外
    @param bln 検索条件：路線名　Noneの場合は検索対象外
    @param rpd 検索条件：平日の運行状況　Noneの場合は検索対象外
    @param rps 検索条件：土曜日の運行状況　Noneの場合は検索対象外
    @param rph 検索条件：休日の運行状況　Noneの場合は検索対象外
    @param rmk 検索条件：備考　Noneの場合は検索対象外
    @return 取得した結果
    """
    return _get_table_base(BusRoute, [
        {'field': 'bsc', 'cond': bsc},
        {'field': 'boc', 'cond': boc},
        {'field': 'bln', 'cond': bln},
        {'field': 'rpd', 'cond': rpd},
        {'field': 'rps', 'cond': rps},
        {'field': 'rph', 'cond': rph},
        {'field': 'rmk', 'cond': rmk},
        {'field': 'geometry', 'cond': None},
    ])


def get_bus_route_by_geometry(xmin, ymin, xmax, ymax):
    """
    選択した範囲に重なるバスルートの取得
    @param xmin 取得範囲
    @param ymin 取得範囲
    @param xmax 取得範囲
    @param ymax 取得範囲
    @return 取得した結果
    """
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
    """, (xmin, ymin, xmax, ymax))
    ret = []
    for r in rows:
        ret.append({
            'PK_UID': r[0],
            'bsc': r[1],
            'boc': r[2],
            'bln': r[3],
            'rpd': r[4],
            'rps': r[5],
            'rph': r[6],
            'rmk': r[7],
            'geometry': r[8]
        })
    return ret


def get_railroad_section(railwayType=None, serviceProviderType=None, railwayLineName=None, operationCompany=None):
    """
    鉄道路線の取得
    @param railwayType 検索条件：鉄道区分コード　Noneの場合は検索対象外
    @param serviceProviderType 検索条件：事業者種別コード　Noneの場合は検索対象外
    @param railwayLineName 検索条件：路線名　Noneの場合は検索対象外
    @param operationCompany 検索条件：運行会社名　Noneの場合は検索対象外
    @return 取得した結果
    """
    return _get_table_base(RailroadSection, [
        {'field': 'railwayType', 'cond': railwayType},
        {'field': 'serviceProviderType', 'cond': serviceProviderType},
        {'field': 'railwayLineName', 'cond': railwayLineName},
        {'field': 'operationCompany', 'cond': operationCompany},
        {'field': 'geometry', 'cond': None},
    ])


def get_railroad_section_by_geometry(xmin, ymin, xmax, ymax):
    """
    選択した範囲に重なる鉄道路線の取得
    @param xmin 取得範囲
    @param ymin 取得範囲
    @param xmax 取得範囲
    @param ymax 取得範囲
    @return 取得した結果
    """
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
    """, (xmin, ymin, xmax, ymax))
    ret = []
    for r in rows:
        ret.append({
            'PK_UID': r[0],
            'railwayType': r[1],
            'serviceProviderType': r[2],
            'railwayLineName': r[3],
            'operationCompany': r[4],
            'geometry': r[5]
        })
    return ret


def get_station(railwayType=None, serviceProviderType=None, railwayLineName=None, operationCompany=None, stationName=None):
    """
    鉄道路線の取得
    @param railwayType 検索条件：鉄道区分コード　Noneの場合は検索対象外
    @param serviceProviderType 検索条件：事業者種別コード　Noneの場合は検索対象外
    @param railwayLineName 検索条件：路線名　Noneの場合は検索対象外
    @param operationCompany 検索条件：運行会社名　Noneの場合は検索対象外
    @param stationName 検索条件：駅名　Noneの場合は検索対象外
    @return 取得した結果
    """
    return _get_table_base(Station, [
        {'field': 'railwayType', 'cond': railwayType},
        {'field': 'serviceProviderType', 'cond': serviceProviderType},
        {'field': 'railwayLineName', 'cond': railwayLineName},
        {'field': 'operationCompany', 'cond': operationCompany},
        {'field': 'stationName', 'cond': stationName},
        {'field': 'geometry', 'cond': None},
    ])


def get_station_by_geometry(xmin, ymin, xmax, ymax):
    """
    選択した範囲に重なる駅の取得
    @param xmin 取得範囲
    @param ymin 取得範囲
    @param xmax 取得範囲
    @param ymax 取得範囲
    @return 取得した結果
    """
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
    """, (xmin, ymin, xmax, ymax))
    ret = []
    for r in rows:
        ret.append({
            'PK_UID': r[0],
            'railwayType': r[1],
            'serviceProviderType': r[2],
            'railwayLineName': r[3],
            'operationCompany': r[4],
            'StationName': r[5],
            'geometry': r[6]
        })
    return ret


def get_administrative_area_code_list():
    ret = []
    rs = AdministrativeDistrict.select(AdministrativeDistrict.administrativeAreaCode).distinct()
    for r in rs:
        ret.append(r.administrativeAreaCode)
    return ret


def trancate_address():
    Address.delete().execute()


def import_address(data_source):
    """
    アドレスのインポート
    """
    with database_proxy.transaction():
        # 多すぎるとエラーになるので適度に分割
        for i in range(int(math.ceil(len(data_source) / 200.0))):
            Address.insert_many(data_source[i*200:(i+1)*200]).execute()
        database_proxy.commit()


def convert_addresslist_to_pos(addresses):
    """
    指定の住所から座標を取得する
    末尾以外の数字は漢数字として処理する。
    「北海道旭川市南八条通25丁目3」時は「北海道旭川市南八条通二十五丁目3」で検索する
    @param address 住所のリスト
    """
    patter_lastnum = re.compile('[0-9]+$', re.IGNORECASE)
    chk_list = []
    dict_convert = {}
    for address in addresses:
      prefix = patter_lastnum.split(address)
      last_num = patter_lastnum.findall(address)
      chkstr = prefix[0]
      chkstr = convert_integerstring(chkstr)
      if len(last_num) > 0:
          chkstr = '%s%s' % (chkstr, last_num[0])
      chk_list.append(chkstr)
      dict_convert[address] = chkstr


    rs = Address.select().where(Address.address << chk_list)
    i = 0
    ret = {}
    for r in rs:
        if not r.address in ret:
            ret[r.address] = {'count':0, 'long':0, 'lat':0}
        ret[r.address]['long'] += r.long
        ret[r.address]['lat'] += r.lat
        ret[r.address]['count'] += 1
        i = i + 1
    for key, item in ret.items():
        ret[key]['long'] = ret[key]['long'] / ret[key]['count']
        ret[key]['lat'] = ret[key]['lat'] / ret[key]['count']
    res = {}
    for address in addresses:
        key = dict_convert[address]
        res[address] = None
        if key in dict_convert:
            if key in ret:
                res[address] = {'lat' : ret[key]['lat'], 'long' : ret[key]['long']}

    return res


def _makeGeometryString(type, shape):
    r = type + '('
    i = 0
    for d in shape.points:
        if i > 0:
            r += ','
        r = r + ('%f %f' % (d[0], d[1]))
        i += 1
    r += ')'
    return r


def _makeMultiGeometryString(type, shape):
    r = type + '(('
    i = 0
    parts = shape.parts
    parts.append(-1)
    partptr = 1 #初回スキップ
    for d in shape.points:
        if parts[partptr] == i:
            r = r + '),('
            partptr += 1
        elif i > 0:
            r += ','
        r = r + ('%f %f' % (d[0], d[1]))
        i += 1
    r += '))'
    return r


def import_administrative_district(shape_path):
    sf = shapefile.Reader(shape_path)
    shapeRecs = sf.iterShapeRecords()
    with database_proxy.transaction():
        AdministrativeDistrict.delete().execute()
        for sr in shapeRecs:
            database_proxy.get_conn().execute(
                """
                INSERT INTO AdministrativeDistrict
                  (prefectureName, subPrefectureName, countyName, cityName, administrativeAreaCode, geometry)
                VALUES(?,?,?,?,?,GeometryFromText(?, ?))
                """,
                (
                    sr.record[0].decode('cp932'),
                    sr.record[1].decode('cp932'),
                    sr.record[2].decode('cp932'),
                    sr.record[3].decode('cp932'),
                    sr.record[4].decode('cp932'),
                    _makeMultiGeometryString('POLYGON', sr.shape), SRID
                )
            )
        database_proxy.commit()


def import_railroad_section(shape_path):
    sf = shapefile.Reader(shape_path)
    shapeRecs = sf.iterShapeRecords()
    with database_proxy.transaction():
        RailroadSection.delete().execute()
        for sr in shapeRecs:
            database_proxy.get_conn().execute(
                """
                INSERT INTO RailroadSection
                  (railwayType, serviceProviderType, railwayLineName, operationCompany, geometry)
                VALUES(?,?,?,?,GeometryFromText(?, ?))
                """,
                (
                    sr.record[0].decode('cp932'),
                    sr.record[1].decode('cp932'),
                    sr.record[2].decode('cp932'),
                    sr.record[3].decode('cp932'),
                    _makeGeometryString('LINESTRING', sr.shape), SRID
                )
            )
        database_proxy.commit()


def import_station(shape_path):
    sf = shapefile.Reader(shape_path)
    shapeRecs = sf.iterShapeRecords()
    with database_proxy.transaction():
        Station.delete().execute()
        for sr in shapeRecs:
            database_proxy.get_conn().execute(
                """
                INSERT INTO Station
                  (railwayType, serviceProviderType, railwayLineName, operationCompany, stationName, geometry)
                VALUES(?,?,?,?,?,GeometryFromText(?, ?))
                """,
                (
                    sr.record[0].decode('cp932'),
                    sr.record[1].decode('cp932'),
                    sr.record[2].decode('cp932'),
                    sr.record[3].decode('cp932'),
                    sr.record[4].decode('cp932'),
                    _makeGeometryString('LINESTRING', sr.shape), SRID
                )
            )
        database_proxy.commit()


def import_bus_route(shape_path):
    sf = shapefile.Reader(shape_path)
    shapeRecs = sf.iterShapeRecords()
    with database_proxy.transaction():
        BusRoute.delete().execute()
        for sr in shapeRecs:
            database_proxy.get_conn().execute(
                """
                INSERT INTO BusRoute
                  (bsc, boc, bln, rpd, rps, rph, rmk, geometry)
                VALUES(?, ?, ?, ?, ?, ?, ?, GeometryFromText(?, ?))
                """,
                (
                    sr.record[0],
                    sr.record[1].decode('cp932'),
                    sr.record[2].decode('cp932'),
                    sr.record[3],
                    sr.record[4],
                    sr.record[5],
                    sr.record[6].decode('cp932'),
                    _makeMultiGeometryString('MULTILINESTRING', sr.shape), SRID
                )
            )
        database_proxy.commit()


def _import_sediment_disaster_hazard_area_base(table, type, prefecture_name, shape_path):
    sf = shapefile.Reader(shape_path)
    shapeRecs = sf.iterShapeRecords()
    fnc = _makeGeometryString
    if type == 'POLYGON':
        fnc = _makeMultiGeometryString

    with database_proxy.transaction():
        table.delete().filter(SedimentDisasterHazardAreaSurface.prefectureName==prefecture_name).execute()

        for sr in shapeRecs:
            database_proxy.get_conn().execute(
                """
                INSERT INTO
                """ + table.__name__ +
                """
                  (prefectureName, hazardAreaType, remarks, geometry)
                VALUES(?,?,?,GeometryFromText(?, ?))
                """,
                (
                    prefecture_name,
                    sr.record[0].decode('cp932'),
                    sr.record[1].decode('cp932'),
                    fnc(type, sr.shape), SRID
                )
            )
        database_proxy.commit()


def import_sediment_disaster_hazard_area_surface(prefecture_name, shape_path):
    _import_sediment_disaster_hazard_area_base(SedimentDisasterHazardAreaSurface, 'POLYGON', prefecture_name, shape_path)

def import_sediment_disaster_hazard_area_line(prefecture_name, shape_path):
    _import_sediment_disaster_hazard_area_base(SedimentDisasterHazardAreaLine, 'LINESTRING', prefecture_name, shape_path)

def import_sediment_disaster_hazard_area_point(prefecture_name, shape_path):
    _import_sediment_disaster_hazard_area_base(SedimentDisasterHazardAreaPoint, 'POINT', prefecture_name, shape_path)


def _get_sediment_disaster_hazard_area_by_geometry(table_name, xmin, ymin, xmax, ymax):
    """
    選択した範囲に重なる土砂災害危険箇所データの取得
    @param table_name テーブル名
    @param xmin 取得範囲
    @param ymin 取得範囲
    @param xmax 取得範囲
    @param ymax 取得範囲
    @return 取得した結果
    """
    rows = database_proxy.get_conn().execute("""
      SELECT
        PK_UID,
        prefectureName,
        hazardAreaType,
        remarks,
        AsGeoJson(geometry)
      FROM
        %s
        inner join idx_%s_geometry ON pkid = PK_UID
      WHERE
          MBROverlaps(
            BuildMBR(xmin,ymin,xmax,ymax),
            BuildMBR(?, ?, ?, ?)
        );
    """ % (table_name, table_name), (xmin, ymin, xmax, ymax))
    ret = []
    for r in rows:
        ret.append({
            'PK_UID': r[0],
            'prefectureName': r[1],
            'hazardAreaType': r[2],
            'remarks': r[3],
            'geometry': r[4]
        })
    return ret

def get_sediment_disaster_hazard_area_surface_by_geometry(xmin, ymin, xmax, ymax):
    return _get_sediment_disaster_hazard_area_by_geometry(SedimentDisasterHazardAreaSurface.__name__, xmin, ymin, xmax, ymax)

def get_sediment_disaster_hazard_area_line_by_geometry(xmin, ymin, xmax, ymax):
    return _get_sediment_disaster_hazard_area_by_geometry(SedimentDisasterHazardAreaLine.__name__, xmin, ymin, xmax, ymax)

def get_sediment_disaster_hazard_area_point_by_geometry(xmin, ymin, xmax, ymax):
    return _get_sediment_disaster_hazard_area_by_geometry(SedimentDisasterHazardAreaPoint.__name__, xmin, ymin, xmax, ymax)


expected_flood_area_attr_key_converter = {
  u'作成種別コード' : 'creatingType',
  u'作成主体' : 'creatingBody' ,
  u'指定年月日' : 'designatedDate',
  u'告示番号' : 'announcementNumber',
  u'対象となる洪水予報河川' : 'targetRiver',
  u'指定の前提となる計画降雨' : 'designedStorm',
  u'関係市町村' : 'municipalGovernments',
  u'説明文' : 'description'
}

def import_expected_flood_area( prefecture_name, shape_path, attr_dir):
    with database_proxy.transaction():
        ExpectedFloodArea.delete().filter(ExpectedFloodAreaAttribute.prefectureName==prefecture_name).execute()
        ExpectedFloodAreaAttribute.delete().filter(ExpectedFloodAreaAttribute.prefectureName==prefecture_name).execute()

        # 属性ファイルのインポート
        attr_files = glob.glob(os.path.join(attr_dir, '*.txt'))
        for attr_file in attr_files:
            base, ext = os.path.splitext(os.path.basename(attr_file))
            data = {
                'attributeId' : base,
                'prefectureName' : prefecture_name,
                'creatingType' : 0,
                'creatingBody' : '',
                'designatedDate' : '',
                'announcementNumber' : '',
                'targetRiver' : '',
                'designedStorm' : '',
                'municipalGovernments' : '',
                'description' : '',
                'remarks' : ''
            }
            f = open(attr_file)
            attr_data = f.read().decode('cp932').encode('utf8')
            for row in csv.reader(StringIO.StringIO(attr_data.strip())):
                if row[0].decode('utf8') in expected_flood_area_attr_key_converter:
                    key = expected_flood_area_attr_key_converter[row[0].decode('utf8')]
                else:
                    key = 'remarks'
                if key == 'description':
                    data[key] += row[2].decode('utf8') + '\n'
                elif key == 'remarks':
                    data[key] += row[0].decode('utf8') + ':' + row[2].decode('utf8') + '\n'
                elif key == 'creatingType':
                    data[key] = int(row[2].decode('utf8'))
                else:
                    data[key] = row[2].decode('utf8')
            f.close()
            ExpectedFloodAreaAttribute.insert_many([data]).execute()

        sf = shapefile.Reader(shape_path)
        try:
            # 国土数値情報のshpファイルが不正で、shpファイル中のコンテンツ長と実際の長さのつじつまが合っていない。
            # しかたないのでshxファイル経由で各レコードを取得する
            i = 0
            while True:
                sr = sf.shape(i)
                r = sf.record(i)
                database_proxy.get_conn().execute(
                    """
                    INSERT INTO ExpectedFloodArea
                      (prefectureName, waterDepth, attributeId, geometry)
                    VALUES(?,?,?,GeometryFromText(?, ?))
                    """,
                    (
                        prefecture_name,
                        r[0],
                        r[5].decode('cp932'),
                        _makeMultiGeometryString('POLYGON', sr), SRID
                    )
                )
                i += 1
        except IndexError:
            pass
        database_proxy.commit()


def get_expected_flood_area_by_geometry(xmin, ymin, xmax, ymax):
    """
    選択した範囲に重なる土砂災害危険箇所データの取得
    @param table_name テーブル名
    @param xmin 取得範囲
    @param ymin 取得範囲
    @param xmax 取得範囲
    @param ymax 取得範囲
    @return 取得した結果
    """
    rows = database_proxy.get_conn().execute("""
      SELECT
        PK_UID,
        prefectureName,
        waterDepth,
        attributeId,
        AsGeoJson(geometry)
      FROM
        ExpectedFloodArea
        inner join idx_ExpectedFloodArea_geometry ON pkid = PK_UID
      WHERE
          MBROverlaps(
            BuildMBR(xmin,ymin,xmax,ymax),
            BuildMBR(?, ?, ?, ?)
        );
    """ , (xmin, ymin, xmax, ymax))
    ret_geo = []
    for r in rows:
        ret_geo.append({
            'PK_UID': r[0],
            'prefectureName': r[1],
            'waterDepth': r[2],
            'attributeId': r[3],
            'geometry': r[4]
        })
    return ret_geo