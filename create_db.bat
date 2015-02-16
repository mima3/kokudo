set DB_PATH=.\kokudo.sqlite
set SPATIALITE=C:\tool\spatialite\mod_spatialite-4.2.0-win-x86\mod_spatialite.dll

python import_administrative_district.py %SPATIALITE% %DB_PATH% original_data\N03-140401_GML\N03-14_140401_simple.shp
python import_railroad_section.py %SPATIALITE% %DB_PATH% original_data\N02-13\N02-13_RailroadSection.shp
python import_station.py %SPATIALITE% %DB_PATH% original_data\N02-13\N02-13_Station.shp
python import_bus_route.py %SPATIALITE% %DB_PATH% original_data\N07-11_GML\N07-11-jgd_simple.shp
