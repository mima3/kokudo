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
    if argc != 4:
        print ("Usage #python %s mod_spatialite_path db_path source_dir" % argvs[0])
        return 1
    mod_spatialite_path = argvs[1]
    db_path = argvs[2]
    source_dir = argvs[3]
    setup(db_path, mod_spatialite_path)
    appearance_point_shape_path = os.path.join(source_dir, 'AppearancePoint_Gust.shp')
    disappearance_point_shape_path = os.path.join(source_dir, 'DisappearancePoint_Gust.shp')
    import_gust(appearance_point_shape_path, disappearance_point_shape_path)


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
