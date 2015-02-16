#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from kokudo_db import *
import urllib
import urllib2
from lxml import etree
import zipfile
import os
import csv, StringIO

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
        print ("Usage #python %s mod_spatialite_path db_path shape_path" % argvs[0])
        return 1
    mod_spatialite_path = argvs[1]
    db_path = argvs[2]
    shape_path = argvs[3]
    setup(db_path, mod_spatialite_path)
    import_administrative_district(shape_path)


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
