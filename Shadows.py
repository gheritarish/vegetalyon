import geopandas as gpd
from shapely.ops import unary_union
from datetime import datetime
from t4gpd.sun.STHardShadow import STHardShadow
from t4gpd.sun.STTreeHardShadow import STTreeHardShadow

buffer = gpd.read_file('./data/Zone.shp') # Import mask
print('Zone importée')
buildings = gpd.read_file('./data/Buildings.shp').to_crs(epsg=2154) # Import buildings
print('Bâtiments importés')
trees = gpd.read_file('./data/Arbres_alignement.shp').to_crs(epsg=2154) # Import trees
print('Arbres importés')
parcs = gpd.read_file('./data/com_parc_jardins_mask.shp').to_crs(epsg=2154) #Import public parcs
print('Parcs importés')
roads = gpd.read_file('./data/voirie_mask.shp').to_crs(epsg=2154) #Import roads
print('Routes importés')
roads['largeurcha'].fillna(2, inplace=True) #Setting a default value of 2m wide for roads without data (including paths)
roads['geometry']=roads['geometry'].buffer(roads['largeurcha']) #Modify the geometry from streamlines to buffers
grid = gpd.read_file('./produced_data/petite_grille.shp').to_crs(epsg=2154) # Import the grid. This grid has no points on the buildings
print('Grille importée')
grid['Ombre'] = 0 # Create a column for the shadows
parcs_geom = unary_union(parcs['geometry'])
roads_geom = unary_union(roads['geometry'])
grid['parcs'] = grid.within(parcs_geom)
grid['roads'] = grid.within(roads_geom)
grid = grid[grid['parcs']==False]
grid = grid[grid['roads']==False]

# Remove the buildings without height and trees without leaves
buildings = buildings[~buildings['HAUTEUR'].isnull() & buildings['HAUTEUR'] > 0]
trees = trees[(trees['hauteurtot'] > 0) & trees['rayoncouro'] > 0]

# Datetime for the whole year at 9, 12 and 15h UTC
dt = [datetime(2021, month, 21, hour, 00) for month in range(1,13) for hour in [9, 12, 15]]


for date in dt:
    shadows = STHardShadow(buildings, date, occludersElevationFieldname='HAUTEUR', altitudeOfShadowPlane=0, aggregate=True).run() # Compute the shadows of the buildings
    treeshadow = STTreeHardShadow(trees, date, treeHeightFieldname = 'hauteurtot', treeCrownRadiusFieldname = 'rayoncouro', altitudeOfShadowPlane=0, aggregate=True).run() # Compute the shadows of the trees
    shadows = gpd.overlay(shadows, buildings, how='difference') # Remove the buildings from the shadows geometry
    grid['Buildings_ombre' + str(date)] = grid.geometry.within(shadows.loc[0, 'geometry']) # Create column: equals 1 if the point is within a building shadow, else 0
    grid['Vegetation_ombre' + str(date)] = grid.geometry.within(treeshadow.loc[0, 'geometry']) # Create column: equals 1 if the point is within a tree shadow, else 0

    if int(date.strftime("%m")) < 3 or int(date.strftime("%m")) > 10: # January, February, November and December
        x = 1 # The coefficient is 1 because the sun is not that important
    elif int(date.strftime("%m")) > 4 and int(date.strftime("%m")) < 9: # Summer (between May and August)
        if int(date.strftime("%H")) == 12: # At noon
            x = 10
        else:
            x = 7
    else:
        if int(date.strftime("%H")) == 12: # At noon
            x = 5
        else:
            x = 3
    grid['Ombre'] = grid['Ombre'] + x*(1 - (grid['Buildings_ombre' + str(date)] | grid['Vegetation_ombre' + str(date)])) # Compute the shadow coefficient, according to the date and time. 1 - grid['Coefficient_ombre' + str(date)] equals 0 if point is in the shadows, 1 otherwise
    print(str(date) + ' terminé') # To know how the algorithm goes

grid = grid[['Ombre', 'geometry']] # Select only relevant columns

grid.to_file('./produced_data/grid_coefs.shp') # Get a file for the shadows and their coefficient
