#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from kokudo_db import *
import os


# db logger.
#import logging
#logger = logging.getLogger('peewee')
#logger.setLevel(logging.DEBUG)
#logger.addHandler(logging.StreamHandler())

filelist = [
    {'prefix':'A26-10_01-g_SedimentDisasterHazardArea', 'prefecture_name': u'北海道'},
    {'prefix':'A26-10_02-g_SedimentDisasterHazardArea', 'prefecture_name': u'青森'},
    {'prefix':'A26-10_03-g_SedimentDisasterHazardArea', 'prefecture_name': u'岩手'},
    {'prefix':'A26-10_04-g_SedimentDisasterHazardArea', 'prefecture_name': u'宮城'},
    {'prefix':'A26-10_05-g_SedimentDisasterHazardArea', 'prefecture_name': u'秋田'},
    {'prefix':'A26-10_06-g_SedimentDisasterHazardArea', 'prefecture_name': u'山形'},
    {'prefix':'A26-10_07-g_SedimentDisasterHazardArea', 'prefecture_name': u'福島'},
    {'prefix':'A26-10_08-g_SedimentDisasterHazardArea', 'prefecture_name': u'茨城'},
    {'prefix':'A26-10_09-g_SedimentDisasterHazardArea', 'prefecture_name': u'栃木'},
    {'prefix':'A26-10_10-g_SedimentDisasterHazardArea', 'prefecture_name': u'群馬'},
    {'prefix':'A26-10_11-g_SedimentDisasterHazardArea', 'prefecture_name': u'埼玉'},
    {'prefix':'A26-10_12-g_SedimentDisasterHazardArea', 'prefecture_name': u'千葉'},
    {'prefix':'A26-10_13-g_SedimentDisasterHazardArea', 'prefecture_name': u'東京'},
    {'prefix':'A26-10_14-g_SedimentDisasterHazardArea', 'prefecture_name': u'神奈川'},
    {'prefix':'A26-10_15-g_SedimentDisasterHazardArea', 'prefecture_name': u'新潟'},
    {'prefix':'A26-10_16-g_SedimentDisasterHazardArea', 'prefecture_name': u'富山'},
    {'prefix':'A26-10_17-g_SedimentDisasterHazardArea', 'prefecture_name': u'石川'},
    {'prefix':'A26-10_18-g_SedimentDisasterHazardArea', 'prefecture_name': u'福井'},
    {'prefix':'A26-10_19-g_SedimentDisasterHazardArea', 'prefecture_name': u'山梨'},
    {'prefix':'A26-10_20-g_SedimentDisasterHazardArea', 'prefecture_name': u'長野'},
    {'prefix':'A26-10_21-g_SedimentDisasterHazardArea', 'prefecture_name': u'岐阜'},
    {'prefix':'A26-10_22-g_SedimentDisasterHazardArea', 'prefecture_name': u'静岡'},
    {'prefix':'A26-10_23-g_SedimentDisasterHazardArea', 'prefecture_name': u'愛知'},
    {'prefix':'A26-10_24-g_SedimentDisasterHazardArea', 'prefecture_name': u'三重'},
    {'prefix':'A26-10_25-g_SedimentDisasterHazardArea', 'prefecture_name': u'滋賀'},
    {'prefix':'A26-10_26-g_SedimentDisasterHazardArea', 'prefecture_name': u'京都'},
    {'prefix':'A26-10_27-g_SedimentDisasterHazardArea', 'prefecture_name': u'大阪'},
    {'prefix':'A26-10_28-g_SedimentDisasterHazardArea', 'prefecture_name': u'兵庫'},
    {'prefix':'A26-10_29-g_SedimentDisasterHazardArea', 'prefecture_name': u'奈良'},
    {'prefix':'A26-10_30-g_SedimentDisasterHazardArea', 'prefecture_name': u'和歌山'},
    {'prefix':'A26-10_31-g_SedimentDisasterHazardArea', 'prefecture_name': u'鳥取'},
    {'prefix':'A26-10_32-g_SedimentDisasterHazardArea', 'prefecture_name': u'島根'},
    {'prefix':'A26-10_33-g_SedimentDisasterHazardArea', 'prefecture_name': u'岡山'},
    {'prefix':'A26-10_34-g_SedimentDisasterHazardArea', 'prefecture_name': u'広島'},
    {'prefix':'A26-10_35-g_SedimentDisasterHazardArea', 'prefecture_name': u'山口'},
    {'prefix':'A26-10_36-g_SedimentDisasterHazardArea', 'prefecture_name': u'徳島'},
    {'prefix':'A26-10_37-g_SedimentDisasterHazardArea', 'prefecture_name': u'香川'},
    {'prefix':'A26-10_38-g_SedimentDisasterHazardArea', 'prefecture_name': u'愛媛'},
    {'prefix':'A26-10_39-g_SedimentDisasterHazardArea', 'prefecture_name': u'高知'},
    {'prefix':'A26-10_40-g_SedimentDisasterHazardArea', 'prefecture_name': u'福岡'},
    {'prefix':'A26-10_41-g_SedimentDisasterHazardArea', 'prefecture_name': u'佐賀'},
    {'prefix':'A26-10_42-g_SedimentDisasterHazardArea', 'prefecture_name': u'長崎'},
    {'prefix':'A26-10_43-g_SedimentDisasterHazardArea', 'prefecture_name': u'熊本'},
    {'prefix':'A26-10_44-g_SedimentDisasterHazardArea', 'prefecture_name': u'大分'},
    {'prefix':'A26-10_45-g_SedimentDisasterHazardArea', 'prefecture_name': u'宮崎'},
    {'prefix':'A26-10_46-g_SedimentDisasterHazardArea', 'prefecture_name': u'鹿児島'},
    {'prefix':'A26-10_47-g_SedimentDisasterHazardArea', 'prefecture_name': u'沖縄'}
]

def main(argvs, argc):
    """
    このスクリプトでは国土行政区域のShapeファイルをデータベースにインポートします。
    データが重すぎるようなら、QGIS等で、ジオメトリを簡素化したShapeを使用してください。
    """
    if argc != 4:
        print ("Usage #python %s mod_spatialite_path db_path source_dir" % argvs[0])
        return 1
    mod_spatialite_path = argvs[1]
    db_path = argvs[2]
    source_dir = argvs[3]
    setup(db_path, mod_spatialite_path)
    for f in filelist:
        print (f['prefecture_name'])
        linepath = source_dir + '/' + f['prefix'] + '_Line.shp'
        surfacepath =  source_dir + '/' + f['prefix'] + '_Surface.shp'
        pointpath =  source_dir + '/' + f['prefix'] + '_Point.shp'
        if os.path.exists(linepath):
            print linepath
            import_sediment_disaster_hazard_area_line(f['prefecture_name'], linepath)
        if os.path.exists(surfacepath):
            print(surfacepath)
            import_sediment_disaster_hazard_area_surface(f['prefecture_name'], surfacepath)
        if os.path.exists(pointpath):
            print(pointpath)
            import_sediment_disaster_hazard_area_point(f['prefecture_name'], pointpath)
    

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
