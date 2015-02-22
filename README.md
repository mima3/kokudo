国土数値情報の取得プログラム
==========
このプログラムは国土数値情報、位置参照情報ダウンロードサービスを利用しています。  

国土数値情報　ダウンロードサービス  
http://nlftp.mlit.go.jp/ksj/  


位置参照情報ダウンロードサービス  
http://nlftp.mlit.go.jp/isj/index.html  

依存ファイル  
-------------
easy_install peewee  


インストール方法
-----------------
1.application.ini.originをコピーしてappication.iniを作成する。  
下記を修正すること。  

    [database]
    path = ./kokudo.sqlite # データべースのパス
    mod_path = C:\tool\spatialite\mod_spatialite.dll # mod_spatialite.dllへのパス
    sep = ;  # 環境変数PATHの区切り文字　WINDOWSは; LINUXは:とする

2.index.cgiの構築  
/home/username/kokudo/ にapplication.ini,databaseファイルがあるものとする.  
/home/username/www/kokudo/ が公開さきのディレクトリとする  
以下のコマンドを実行

    git clone git://github.com/mima3/kokudo.git 
    rm -rf kokudo/.git

    cp -rf kokudo /home/username/www/
    python /home/username/www/kokudo/create_index_cgi.py "/usr/local/bin/python" "/home/username/kokudo/application.ini" > /home/username/www/kokudo/index.cgi
    chmod +x  /home/username/www/kokudo/index.cgi

3.国土数値情報のインポート  
国土数値情報　ダウンロードサービス  から取得したshpファイルをインポートします。  
大きなデータの時などは、QGISなどを利用してshpファイルの簡素化を行ってください。
    
    #行政区域のインポート例
    python import_administrative_district.py C:\tool\spatialite\mod_spatialite-4.2.0-win-x86\mod_spatialite.dll test.sqlite original_data\N03-140401_GML\N03-14_140401_simple.shp
    
    #鉄道路線のインポート例
    python import_railroad_section.py C:\tool\spatialite\mod_spatialite-4.2.0-win-x86\mod_spatialite.dll test.sqlite original_data\N02-13\N02-13_RailroadSection.shp
    
    #鉄道駅のインポート例
    python import_station.py C:\tool\spatialite\mod_spatialite-4.2.0-win-x86\mod_spatialite.dll test.sqlite original_data\N02-13\N02-13_Station.shp
    
    #バス路線図のインポート例
    python import_bus_route.py C:\tool\spatialite\mod_spatialite-4.2.0-win-x86\mod_spatialite.dll test.sqlite original_data\N07-11_GML\N07-11-jgd_simple.shp

    # 土砂災害危険箇所データ
    python import_sediment_disaster_hazard_area.py C:\tool\spatialite\mod_spatialite-4.2.0-win-x86\mod_spatialite.dll kokudo.sqlite .\original_data\KsjTmplt-A26\output

    # 国土数値情報　浸水想定区域データ
    python import_expected_flood_area.py C:\tool\spatialite\mod_spatialite-4.2.0-win-x86\mod_spatialite.dll kokudo.sqlite .\original_data\A31-12\output

    # 国土数値情報　突風等データ
    python import_gust.py C:\tool\spatialite\mod_spatialite-4.2.0-win-x86\mod_spatialite.dll kokudo.sqlite .\original_data\A30b-11_GML

土砂災害危険個所データを取得
--------------------
指定の範囲に重なる土砂災害危険個所データを取得します

    http://127.0.0.1/kokudo/json/get_sediment_disaster_hazard_area_line_by_geometry?swlat=34.45&swlng=137.4&nelat=35.7&nelng=139.81
    http://127.0.0.1/kokudo/json/get_sediment_disaster_hazard_area_point_by_geometry?swlat=34.45&swlng=135.4&nelat=35.7&nelng=139.81
    http://127.0.0.1/kokudo/json/get_sediment_disaster_hazard_area_surface_by_geometry?swlat=35.45&swlng=139.4&nelat=35.7&nelng=139.81

突風等データを取得
--------------------
指定の範囲に重なる突風等データを取得します

    http://127.0.0.1/kokudo/json/get_gust_by_geometry?swlat=35.6537916853287&swlng=139.73208208935546&nelat=35.73743829568898&nelng=139.86941119091796

浸水想定区域データを取得
--------------------
指定の範囲に重なる浸水想定区域データを取得します

    http://127.0.0.1/kokudo/json/get_expected_flood_area_by_geometry?swlat=35.63077349028057&swlng=139.74856158154296&nelat=35.714444224607576&nelng=139.88589068310546

行政区域データを取得
--------------------
指定の範囲に重なる行政区域データを取得します

    http://127.0.0.1/kokudo/json/get_administrative_district_by_geometry?swlat=35.45&swlng=139.4&nelat=35.7&nelng=139.81

駅データを取得
--------------------
運行会社を指定して駅を取得します。

    http://127.0.0.1/kokudo/json/get_station?operationCompany=%E6%9D%B1%E4%BA%AC%E6%80%A5%E8%A1%8C%E9%9B%BB%E9%89%84

鉄道路線データを取得
--------------------
運行会社を指定して路線データを取得します。

    http://127.0.0.1/kokudo/json/get_railroad_section?operationCompany=%E6%9D%B1%E4%BA%AC%E6%80%A5%E8%A1%8C%E9%9B%BB%E9%89%84

バス路線データを取得
--------------------
指定の範囲に重なる行政区域データを取得します

    http://127.0.0.1/kokudo/json/get_bus_route_by_geometry?swlat=35.45&swlng=139.4&nelat=35.7&nelng=139.81


ライセンス
-------------
当方が作成したコードに関してはMITとします。  
その他、jqueryなどに関しては、それぞれにライセンスを参照してください。

    The MIT License (MIT)

    Copyright (c) 2015 m.ita

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
    the Software, and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
    FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
    IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

