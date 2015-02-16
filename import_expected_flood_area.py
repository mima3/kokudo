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
    {'prefix':'A31-12_01', 'prefecture_name': u'北海道'},
    {'prefix':'A31-12_02', 'prefecture_name': u'青森'},
    {'prefix':'A31-12_03', 'prefecture_name': u'岩手'},
    {'prefix':'A31-12_04', 'prefecture_name': u'宮城'},
    {'prefix':'A31-12_05', 'prefecture_name': u'秋田'},
    {'prefix':'A31-12_06', 'prefecture_name': u'山形'},
    {'prefix':'A31-12_07', 'prefecture_name': u'福島'},
    {'prefix':'A31-12_08', 'prefecture_name': u'茨城'},
    {'prefix':'A31-12_09', 'prefecture_name': u'栃木'},
    {'prefix':'A31-12_10', 'prefecture_name': u'群馬'},
    {'prefix':'A31-12_11', 'prefecture_name': u'埼玉'},
    {'prefix':'A31-12_12', 'prefecture_name': u'千葉'},
    {'prefix':'A31-12_13', 'prefecture_name': u'東京'},
    {'prefix':'A31-12_14', 'prefecture_name': u'神奈川'},
    {'prefix':'A31-12_15', 'prefecture_name': u'新潟'},
    {'prefix':'A31-12_16', 'prefecture_name': u'富山'},
    {'prefix':'A31-12_17', 'prefecture_name': u'石川'},
    {'prefix':'A31-12_18', 'prefecture_name': u'福井'},
    {'prefix':'A31-12_19', 'prefecture_name': u'山梨'},
    {'prefix':'A31-12_20', 'prefecture_name': u'長野'},
    {'prefix':'A31-12_21', 'prefecture_name': u'岐阜'},
    {'prefix':'A31-12_22', 'prefecture_name': u'静岡'},
    {'prefix':'A31-12_23', 'prefecture_name': u'愛知'},
    {'prefix':'A31-12_24', 'prefecture_name': u'三重'},
    {'prefix':'A31-12_25', 'prefecture_name': u'滋賀'},
    {'prefix':'A31-12_26', 'prefecture_name': u'京都'},
    {'prefix':'A31-12_27', 'prefecture_name': u'大阪'},
    {'prefix':'A31-12_28', 'prefecture_name': u'兵庫'},
    {'prefix':'A31-12_29', 'prefecture_name': u'奈良'},
    {'prefix':'A31-12_30', 'prefecture_name': u'和歌山'},
    {'prefix':'A31-12_31', 'prefecture_name': u'鳥取'},
    {'prefix':'A31-12_32', 'prefecture_name': u'島根'},
    {'prefix':'A31-12_33', 'prefecture_name': u'岡山'},
    {'prefix':'A31-12_34', 'prefecture_name': u'広島'},
    {'prefix':'A31-12_35', 'prefecture_name': u'山口'},
    {'prefix':'A31-12_36', 'prefecture_name': u'徳島'},
    {'prefix':'A31-12_37', 'prefecture_name': u'香川'},
    {'prefix':'A31-12_38', 'prefecture_name': u'愛媛'},
    {'prefix':'A31-12_39', 'prefecture_name': u'高知'},
    {'prefix':'A31-12_40', 'prefecture_name': u'福岡'},
    {'prefix':'A31-12_41', 'prefecture_name': u'佐賀'},
    {'prefix':'A31-12_42', 'prefecture_name': u'長崎'},
    {'prefix':'A31-12_43', 'prefecture_name': u'熊本'},
    {'prefix':'A31-12_44', 'prefecture_name': u'大分'},
    {'prefix':'A31-12_45', 'prefecture_name': u'宮崎'},
    {'prefix':'A31-12_46', 'prefecture_name': u'鹿児島'},
    {'prefix':'A31-12_47', 'prefecture_name': u'沖縄'}
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
        # shapeファイルの場所のパターンは３通り
        # A31-12_27_GML\A31-12_27_GML
        # A31-12_27_GML
        # A31-12_27_GML\Shape
        dirname = os.path.join(source_dir,  f['prefix'] + '_GML' , f['prefix'] + '_GML')
        if not os.path.exists(dirname):
            dirname = os.path.join(source_dir,  f['prefix'] + '_GML', 'Shape')
            if not os.path.exists(dirname):
                dirname = os.path.join(source_dir,  f['prefix'] + '_GML')

        shap_path = os.path.join(dirname, f['prefix'] + '.shp')
        attr_path = os.path.join(dirname, u'属性テキストファイル')
        import_expected_flood_area(f['prefecture_name'], shap_path, attr_path)

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
