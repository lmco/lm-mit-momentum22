##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

import geopandas as gpd
from shapely.geometry import Polygon, Point

# Create bounding box for the scope of mapping (contiguous USA)
# bbox = (-130.25390625, 22.55314748, -65.63232422, 49.55372551) #epsg:4269, 4326

# Create bounding box for the scope of mapping (New England)
bbox = (-80.41417236584573, 40.258338053379745, -69.06461890186635, 44.5188750075358)

bounding_polygon = Polygon([(bbox[0],bbox[1]), (bbox[0],bbox[3]), (bbox[2], bbox[3]), (bbox[2], bbox[1]), (bbox[0],bbox[1])])

# Import geojson (sources from Natural Earth and US Census)
# https://geopandas.org/docs/user_guide/projections.html
rivers = gpd.read_file('../data/ne_10m_rivers_north_america.geojson', bbox=bbox, crs="EPSG:4326")
lakes = gpd.read_file('../data/ne_10m_lakes.geojson', bbox=bbox, crs="EPSG:4326")
usa_states = gpd.read_file('../data/cb_2018_us_state_20m.zip', bbox=bbox, crs="EPSG:4326")
oceans = gpd.read_file('../data/ne_10m_ocean_scale_rank.geojson', bbox=bbox, crs="EPSG:4326")

# Clean up data
rivers = rivers[rivers.featurecla != 'Lake Centerline']
rivers = rivers[rivers.featurecla != 'Lake Centerline (Intermittent)']
oceans = gpd.clip(oceans, bounding_polygon).to_crs("EPSG:4326")

# Combine waterbody data
waterbodies = rivers.append(lakes)
waterbodies = waterbodies.append(oceans)

# Save the waterbodies to a file
waterbodies.to_file("../data/waterbodies.geojson", driver='GeoJSON')

# Save the water as an svg because Bokeh doesn't process polylines correctly
# https://tex.stackexchange.com/questions/100190/how-can-i-remove-margins-when-integrating-matplotlib-plots-with-pgfplots
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,5))
ax = plt.gca()
plt.axis('off')
waterbodies.plot(ax=ax, linewidth=0.1)
plt.xlim(bbox[0],bbox[2])
plt.ylim(bbox[1],bbox[3])
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
plt.savefig("../Visualizer/static/waterbodies.svg", bbox_inches='tight', pad_inches=0.0)

# left sjoin on position in order to check if the points are in the waterbodies (here so that I don't forget how to do it)
# https://gis.stackexchange.com/questions/208546/check-if-a-point-falls-within-a-multipolygon-with-python
# Solution 4
# points_world = gpd.GeoDataFrame({'notes': ['water', 'land', 'water', 'land', 'water', 'land', 'great_lakes'], 'geometry': [
#     Point(-72.95891829546144, 41.11641899795742), 
#     Point(-72.66954281013679, 41.38068865655539),
#     Point(-76.39748985675736, 38.63688533327717), 
#     Point(-74.59220133930677, 39.83270782195891), 
#     Point(-122.28664682458502, 37.6515880588658), 
#     Point(-122.44693013721461, 37.737542912755316),
#     Point(-87.4822529168257, 42.698738708909595)
#     ]}, crs="EPSG:4326")

# pointInWaterbodies = gpd.sjoin(points_world, waterbodies, how='left')
# groupedInWaterbodies = pointInWaterbodies.groupby('index_right')
# print(groupedInWaterbodies.groups)