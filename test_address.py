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
    このスクリプトでは位置情報参照情報をデータベースにインポートします。
    以下を参考にしてください。
    http://nlftp.mlit.go.jp/isj/about_api.html
    """
    mod_spatialite_path = 'C:\\tool\\spatialite\\mod_spatialite-4.2.0-win-x86\\mod_spatialite.dll'
    db_path = '.\kokudo.sqlite'
    connect(db_path, mod_spatialite_path)
    lst = [
        u'北海道旭川市神居町神居古潭819',
        u'北海道旭川市神居町神居古潭xxx',
        u'北海道旭川市神居町神居古潭836',
        u'北海道旭川市南八条通二十五丁目3',
        u'北海道旭川市南八条通25丁目3'
    ]
    r = convert_addresslist_to_pos(lst)
    for key, item in r.items():
        print key
        print item
    #print u'北海道旭川市神居町神居古潭819', convert_address_to_pos(u'北海道旭川市神居町神居古潭819')
    #print u'北海道旭川市神居町神居古潭xxx', convert_address_to_pos(u'北海道旭川市神居町神居古潭xxx')
    #print u'北海道旭川市神居町神居古潭836', convert_address_to_pos(u'北海道旭川市神居町神居古潭836')
    #print u'北海道旭川市南八条通二十五丁目3', convert_address_to_pos(u'北海道旭川市南八条通二十五丁目3')
    #print u'北海道旭川市南八条通25丁目3', convert_address_to_pos(u'北海道旭川市南八条通25丁目3')

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
