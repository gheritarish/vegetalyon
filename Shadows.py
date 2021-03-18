import geopandas as gpd
from datetime import datetime
from t4gpd.sun.STHardShadow import STHardShadow
from t4gpd.sun.STTreeHardShadow import STTreeHardShadow

buffer = gpd.read_file('./data/Zone.shp')
print('Zone importée')
buildings = gpd.read_file('./data/Buildings.shp').to_crs(epsg=2154)
print('Bâtiments importés')
trees = gpd.read_file('./data/Arbres_alignement.shp').to_crs(epsg=2154)
print('Arbres importés')
grid = gpd.read_file('./produced_data/petite_grille.shp').to_crs(epsg=2154)
print('Grille importée')
grid['Ombre'] = 0

buildings = buildings[~buildings['HAUTEUR'].isnull() & buildings['HAUTEUR'] > 0]
trees = trees[(trees['hauteurtot'] > 0) & trees['rayoncouro'] > 0]

dt = [datetime(2021, month, 21, hour, 00) for month in range(1,13) for hour in [9, 12, 15]]

for date in dt:
    shadows = STHardShadow(buildings, date, occludersElevationFieldname='HAUTEUR', altitudeOfShadowPlane=0, aggregate=True).run()
    treeshadow = STTreeHardShadow(trees, date, treeHeightFieldname = 'hauteurtot', treeCrownRadiusFieldname = 'rayoncouro', altitudeOfShadowPlane=0, aggregate=True).run()
    shadows = gpd.overlay(shadows, buildings, how='difference')
    grid['Coefficient_ombre' + str(date)] = grid.geometry.within(shadows.loc[0, 'geometry'])
    if int(date.strftime("%m")) < 3 or int(date.strftime("%m")) > 10:
        x = 1
    elif int(date.strftime("%m")) > 4 and int(date.strftime("%m")) < 9:
        if int(date.strftime("%H")) == 13:
            x = 10
        else:
            x = 7
    else:
        if int(date.strftime("%H")) == 13:
            x = 5
        else:
            x = 3
    grid['Ombre'] = grid['Ombre'] + x*(1 - grid['Coefficient_ombre' + str(date)])
    print(str(date) + ' terminé')

grid = grid[['Ombre', 'geometry']]

grid.to_file('./produced_data/grid_coefs.shp')
shadows.to_file('./produced_data/shadows.shp')
treeshadow.to_file('./produced_data/treeshadows.shp')
