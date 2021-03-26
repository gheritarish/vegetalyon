import geopandas as gpd
from shapely.ops import unary_union

buffer = gpd.read_file('./data/Zone.shp') # Import mask
print('Zone importée')

buildings = gpd.read_file('./data/Buildings.shp').to_crs(epsg=2154) # Import buildings
print('Bâtiments importés')

trees = gpd.read_file('./data/Arbres_alignement.shp').to_crs(epsg=2154) # Import trees
print('Arbres importés')

squares = gpd.read_file('./data/com_parc_jardins_mask.shp').to_crs(epsg=2154) # Import public squares
print('Parcs importés')

roads = gpd.read_file('./data/voirie_mask.shp').to_crs(epsg=2154) # Import roads
print('Routes importées')
roads['largeurcha'].fillna(2, inplace=True) # Setting a default value of 2 meters wide for roads without data (including paths)
roads['geometry'] = roads['geometry'].buffer(roads['largeurcha']) # Modify the geometry from streamlines to buffers
roads.to_file('./produced_data/voirie_buffer.shp')

grid = gpd.read_file('./produced_data/Grid.shp').to_crs(epsg=2154) # Import the original grid
print('Grille importée')

buildings_geom = unary_union(buildings['geometry'])
squares_geom = unary_union(squares['geometry'])
roads_geom = unary_union(roads['geometry'])
grid['buildings'] = grid.within(buildings_geom)
grid['squares'] = grid.within(squares_geom)
grid['roads'] = grid.within(roads_geom)

grid = grid[grid['buildings'] == False]
grid = grid[grid['squares'] == False]
grid = grid[grid['roads'] == False]
print('Grille réduite')

grid.to_file('./produced_data/petite_grille.shp')
