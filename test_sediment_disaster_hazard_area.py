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

def main(argvs, argc):
    """
    このスクリプトでは国土行政区域のShapeファイルをデータベースにインポートします。
    データが重すぎるようなら、QGIS等で、ジオメトリを簡素化したShapeを使用してください。
    """
    mod_spatialite_path = argvs[1]
    db_path = argvs[2]
    connect(db_path, mod_spatialite_path)
    ret = get_sediment_disaster_hazard_area_surface_by_geometry(35.45, 35.7, 139.4,  139.81)
    for r in ret:
        print r

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
