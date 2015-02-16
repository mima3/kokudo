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


def convert_zip_to_csv(code, url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    conn = opener.open(req)
    cont = conn.read()
    zippath = code + '.zip'
    outfile = open(zippath, 'wb')
    outfile.write(cont)
    outfile.close()
    zf = zipfile.ZipFile(zippath, 'r')
    ret = []
    for f in zf.namelist():
        root, ext = os.path.splitext(f)
        if ext == '.csv':
            txt = zf.read(f).decode('cp932').encode('utf8')
            i = 0
            for row in csv.reader(StringIO.StringIO(txt.strip())):
                i = i + 1
                if i == 1:
                    continue
                ret.append({
                    'address' : (row[0] + row[1] + row[2] + row[3]),
                    'lat': float(row[7]),
                    'long': float(row[8])
                })
    zf.close()
    try:
        os.remove(zippath)
    except:
      pass
    return ret


def get_administrative_area(code, fiscalyear, posLevel):
    param = {
        'appId' : 'isjapibeta1',
        'areaCode' : code,
        'fiscalyear' : '\'' + fiscalyear.encode('utf8') + '\'',
        'posLevel' : posLevel
    }
    url = 'http://nlftp.mlit.go.jp/isj/api/1.0b/index.php/app/getISJURL.xml?'
    data = urllib.urlencode(param)
    req = urllib2.Request(url + data)
    opener = urllib2.build_opener()
    conn = opener.open(req)
    cont = conn.read()
    root = etree.fromstring(cont)
    urls = root.xpath('//zipFileUrl')
    ret = []
    for url in urls:
        ret.extend(convert_zip_to_csv(code, url.text))
    return ret


def main(argvs, argc):
    """
    このスクリプトでは位置情報参照情報をデータベースにインポートします。
    以下を参考にしてください。
    http://nlftp.mlit.go.jp/isj/about_api.html
    """
    if argc != 3:
        print ("Usage #python %s mod_spatialite_path db_path" % argvs[0])
        return 1
    mod_spatialite_path = argvs[1]
    db_path = argvs[2]
    setup(db_path, mod_spatialite_path)
    codes = get_administrative_area_code_list()
    datas = []
    i = 1
    trancate_address()
    for code in codes:
      print ('%d/%d:%s' % (i, len(codes), code))
      datas = get_administrative_area(code, u'平成25年' , 0)
      import_address(datas)
      i = i + 1


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
