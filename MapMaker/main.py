# Instructions:
# 1. Navigation your command line to the root folder of the project
# 2. Enter `bokeh serve MapMaker --show`
# 3. A web browser tab should open with the MapMaker utility
# FIXME: This file is not complete - saving values entered using the utility is a todo!

from bokeh.io import show, output_file, curdoc
from bokeh.plotting import  figure, Column, Row
from bokeh.models import GeoJSONDataSource, HoverTool, ColumnDataSource, DataTable, TableColumn, PointDrawTool, PolyDrawTool, Div
import os
import geopandas as gpd
from shapely.geometry import Polygon
import inspect

# Create bouding box for the scope of mapping (contiguous USA)
contiguous_usa_bbox = (-130.25390625, 22.55314748, -65.63232422, 49.55372551) #epsg:4269, 4326
bounding_polygon = Polygon([
    (contiguous_usa_bbox[0],contiguous_usa_bbox[1]), 
    (contiguous_usa_bbox[0], contiguous_usa_bbox[3]), 
    (contiguous_usa_bbox[2], contiguous_usa_bbox[3]), 
    (contiguous_usa_bbox[2], contiguous_usa_bbox[1]), 
    (contiguous_usa_bbox[0],contiguous_usa_bbox[1])])
# May choose to not draw these... this is just for reference
usa_states = gpd.read_file(os.path.join(os.path.basename(os.path.dirname(inspect.getfile(lambda: None))),'static/cb_2018_us_state_20m.zip'), bbox=contiguous_usa_bbox, crs="EPSG:4326")

# Convert data to geojson for bokeh
usa_states_geojson = GeoJSONDataSource(geojson=usa_states.to_json())

# Create figure object.
p = figure(title = 'MIT Momentum Map Maker', 
           plot_height = 1080,
           plot_width = 1920,
           x_range=(contiguous_usa_bbox[0], contiguous_usa_bbox[2]),
           y_range=(contiguous_usa_bbox[1], contiguous_usa_bbox[3]),
           toolbar_location = 'below',
           tools = "pan, wheel_zoom, box_zoom, reset")
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
image_url = p.image_url(url=[os.path.join(os.path.basename(os.path.dirname(inspect.getfile(lambda: None))), 'static', 'waterbodies.svg')], 
                        x=contiguous_usa_bbox[0], 
                        y=contiguous_usa_bbox[3], 
                        w=contiguous_usa_bbox[2]-contiguous_usa_bbox[0], 
                        h=contiguous_usa_bbox[3]-contiguous_usa_bbox[1])
states_glyph = p.patches('xs','ys', source = usa_states_geojson,
                                    fill_color = None,
                                    line_color = 'gray', 
                                    line_width = 0.5, 
                                    fill_alpha = 1,
                                    syncable=False)# Create hover tool
p.add_tools(HoverTool(renderers = [states_glyph],
                      tooltips = [('State','@NAME')]))

#http://docs.bokeh.org/en/1.0.0/docs/user_guide/examples/tools_point_draw.html
sourceSurvivors = ColumnDataSource({'x': [], 'y': [], 'color': []})
scatter_renderer = p.scatter(x='x', y='y', source=sourceSurvivors, color='color', size=20)
columns = [TableColumn(field="x", title="Lat"),
           TableColumn(field="y", title="Lon"),
           TableColumn(field='color', title='color')]
tableSurvivors = DataTable(source=sourceSurvivors, columns=columns, editable=True, height=200)
draw_tool = PointDrawTool(renderers=[scatter_renderer], empty_value='orange')
p.add_tools(draw_tool)
p.toolbar.active_tap = draw_tool
divSurvivors = Div(text="""Entered Survivors<br>
(select the Point Draw Tool and click on the map where you'd like to add new Survivors)""",
width=500, height=50)

sourceFires = ColumnDataSource({'xs': [], 'ys': [], 'fill_color': []})
p1 = p.patches(xs='xs', ys='ys', fill_color='fill_color', source=sourceFires, line_width=0, alpha=0.4)
columnsFires = [TableColumn(field="xs", title="Lats"),
                TableColumn(field="ys", title="Lons"),
                TableColumn(field='fill_color', title='Color')]
tableFires = DataTable(source=sourceFires, columns=columnsFires, editable=True, height=200)
draw_tool_p1 = PolyDrawTool(renderers=[p1], empty_value='red')
p.add_tools(draw_tool_p1)
p.toolbar.active_drag = draw_tool_p1
divFires = Div(text="""Entered Fires<br>
(select the Poly Draw Tool and click on the map where you'd like to add new Fires)""",
width=500, height=50)

sourceMapBounds = ColumnDataSource({'minx': [1], 'miny': [2], 'maxx': [3], 'maxy': [4]})
columnsMapBounds = [TableColumn(field="minx", title="minx"),
                    TableColumn(field="miny", title="miny"),
                    TableColumn(field='maxx', title='maxx'),
                    TableColumn(field='maxy', title='maxy')]
tableMapBounds = DataTable(source=sourceMapBounds, columns=columnsMapBounds, editable=True, height=200)
divMapBounds = Div(text="""Resulting Map Bounds<br>
(zoom in such that the map shows what you'd like to be within your map)""",
width=500, height=50)

#https://github.com/bokeh/bokeh/blob/branch-3.0/examples/app/sliders.py#L66
def updateMapBoundMinX(attr, old, new):
    sourceMapBounds.data = {'minx': [new], 
    'miny': [sourceMapBounds.data['miny'][0]], 
    'maxx': [sourceMapBounds.data['maxx'][0]], 
    'maxy': [sourceMapBounds.data['maxy'][0]]}
    tableMapBounds.update()
def updateMapBoundMinY(attr, old, new):
    sourceMapBounds.data = {'minx': [sourceMapBounds.data['minx'][0]], 
    'miny': [new], 
    'maxx': [sourceMapBounds.data['maxx'][0]], 
    'maxy': [sourceMapBounds.data['maxy'][0]]}
    tableMapBounds.update()
def updateMapBoundMaxX(attr, old, new):
    sourceMapBounds.data = {'minx': [sourceMapBounds.data['minx'][0]], 
    'miny': [sourceMapBounds.data['miny'][0]], 
    'maxx': [new], 
    'maxy': [sourceMapBounds.data['maxy'][0]]}
    tableMapBounds.update()
def updateMapBoundMaxY(attr, old, new):
    sourceMapBounds.data = {'minx': [sourceMapBounds.data['minx'][0]], 
    'miny': [sourceMapBounds.data['miny'][0]], 
    'maxx': [sourceMapBounds.data['maxx'][0]], 
    'maxy': [new]}
    tableMapBounds.update()

p.x_range.on_change('start', updateMapBoundMinX)
p.x_range.on_change('end', updateMapBoundMaxX)
p.y_range.on_change('start', updateMapBoundMinY)
p.y_range.on_change('end', updateMapBoundMaxY)

curdoc().add_root(Row(p, Column(divSurvivors, tableSurvivors, divFires, tableFires, divMapBounds, tableMapBounds)))