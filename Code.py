import geopandas as gpd
from datetime import datetime
from t4gpd.sun.STHardShadow import STHardShadow
from t4gpd.sun.STTreeHardShadow import STTreeHardShadow

buffer = gpd.read_file('./data/Zone.shp')
print('Zone importée')
buildings = gpd.read_file('./data/Buildings.shp')
print('Bâtiments importés')
trees = gpd.read_file('./data/Arbres_alignement.shp')
print('Arbres importés')

buildings = buildings[~buildings['HAUTEUR'].isnull() & buildings['HAUTEUR'] > 0]
trees = trees[(trees['hauteurtot'] > 0) & trees['rayoncouro'] > 0]
print('Ombres calculées')

dt = datetime(2021, 7, 21, 11, 30)
shadows = STHardShadow(buildings, dt, occludersElevationFieldname='HAUTEUR', altitudeOfShadowPlane=0, aggregate=True).run()
treeshadow = STTreeHardShadow(trees, dt, treeHeightFieldname = 'hauteurtot', treeCrownRadiusFieldname = 'rayoncouro', altitudeOfShadowPlane=0, aggregate=True).run()
shadows = gpd.overlay(shadows, buildings, how='difference')

shadows.to_file('./produced_data/shadows.shp')
treeshadow.to_file('./produced_data/treeshadows.shp')
