# Instructions:
# 1. Navigate your command line to the root folder of the project (the MapMaker folder should be a subfolder to the root)
# 2. Enter `bokeh serve MapMaker --show`
# 3. A web browser tab should open with the MapMaker utility at http://localhost:5006/MapMaker
# TODO: This utility works as intended, but will be refactored to combine with the visualizer

from bokeh.io import curdoc
from bokeh.plotting import  figure, Column, Row
from bokeh.models import GeoJSONDataSource, HoverTool, ColumnDataSource, DataTable, TableColumn, PointDrawTool, PolyDrawTool, Div, Button, CustomJS, RadioButtonGroup, TextInput
import os
import geopandas as gpd
import inspect
import json
from datetime import datetime
import traceback

# Create bouding box for the scope of mapping (contiguous USA)
contiguous_usa_bbox = (-130.25390625, 22.55314748, -65.63232422, 49.55372551) #epsg:4269, 4326

map_data = {"map_name":"sample_name",
            "map_type": 0, #0=fs, 1=snr
            "bounds": {'minx': contiguous_usa_bbox[0], 'miny': contiguous_usa_bbox[1], 'maxx': contiguous_usa_bbox[2], 'maxy': contiguous_usa_bbox[3]},
            "data_fs": {},
            "data_snr": {},
            }

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
           tools = "pan, wheel_zoom, box_zoom, reset",
           sizing_mode="scale_both")
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


# Make tool to draw survivors
#http://docs.bokeh.org/en/1.0.0/docs/user_guide/examples/tools_point_draw.html
sourceSurvivors = ColumnDataSource({'x': [], 'y': [], 'color': []})
scatter_renderer = p.scatter(x='x', y='y', source=sourceSurvivors, color='color', size=20)
columns = [TableColumn(field="x", title="Lat"),
           TableColumn(field="y", title="Lon"),
           TableColumn(field='color', title='color')]
tableSurvivors = DataTable(source=sourceSurvivors, columns=columns, editable=True, sizing_mode="stretch_both", height_policy="fit", min_height=200)
draw_tool = PointDrawTool(renderers=[scatter_renderer], empty_value='orange', description="Survivor draw tool (select, click once on map to survivors)")
p.add_tools(draw_tool)
p.toolbar.active_tap = draw_tool
divSurvivors = Div(text="""Entered Survivors<br>
(select the Point Draw Tool and click on the map where you'd like to add new Survivors)""", sizing_mode="stretch_both")


# Make tool to draw fires
sourceFires = ColumnDataSource({'xs': [], 'ys': [], 'fill_color': []})
p1 = p.patches(xs='xs', ys='ys', fill_color='fill_color', source=sourceFires, line_width=0, alpha=0.4)
columnsFires = [TableColumn(field="xs", title="Lats"),
                TableColumn(field="ys", title="Lons"),
                TableColumn(field='fill_color', title='Color')]
tableFires = DataTable(source=sourceFires, columns=columnsFires, editable=True, sizing_mode="stretch_both", height_policy="fit",  min_height=200)
draw_tool_p1 = PolyDrawTool(renderers=[p1], empty_value='red', description="Fire draw tool (select, double click on map to start, click once on map to add vertices, double click on map to end)")
p.add_tools(draw_tool_p1)
p.toolbar.active_drag = draw_tool_p1
divFires = Div(text="""Entered Fires<br>(select the Poly Draw Tool and click on the map where you'd like to add new Fires)""", sizing_mode="stretch_both")


# Make table to see map bounds
sourceMapBounds = ColumnDataSource({'minx': [map_data['bounds']['minx']], 'miny': [map_data['bounds']['miny']], 'maxx': [map_data['bounds']['maxx']], 'maxy': [map_data['bounds']['maxy']]})
columnsMapBounds = [TableColumn(field="minx", title="minx"),
                    TableColumn(field="miny", title="miny"),
                    TableColumn(field='maxx', title='maxx'),
                    TableColumn(field='maxy', title='maxy')]
tableMapBounds = DataTable(source=sourceMapBounds, columns=columnsMapBounds, editable=True, sizing_mode="stretch_both")
divMapBounds = Div(text="""Resulting Map Bounds<br>(zoom in such that the map shows what you'd like to be within your map)""", sizing_mode="stretch_both")
# Dynamically update map bounds table as you pan and zoom around
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
# Register callbacks for table updates
p.x_range.on_change('start', updateMapBoundMinX)
p.x_range.on_change('end', updateMapBoundMaxX)
p.y_range.on_change('start', updateMapBoundMinY)
p.y_range.on_change('end', updateMapBoundMaxY)


# Create space to enter map name
file_name = TextInput(value=map_data['map_name'], title="Enter map name (file will be saved as <what you enter>.json):", sizing_mode="stretch_width")
def set_map_name(attr, old, new):
    map_data['map_name'] = new
file_name.on_change('value_input', set_map_name)


# Create the save button
button = Button(label="SAVE MAP", button_type="success", sizing_mode="stretch_width")
button.js_on_click(CustomJS(code="console.log('button: click!', this.toString())")) # FIXME: save the map on click here
def save_map():
    try:
        with open(map_data['map_name'] + ".json", 'w+') as outfile:
            map_data["generated_on"] = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
            map_data["bounds"] = tableMapBounds.source.data
            map_data["data_fs"] = tableFires.source.data
            map_data["data_snr"] = tableSurvivors.source.data
            json.dump(map_data, outfile, indent=4, sort_keys=True)
    except:
        print(traceback.format_exc())
        print("Map save encountered an issue (see traceback above)")
button.on_click(save_map)


# Make a binary selection for the track this map is for
LABELS = ["Fire Fighting", "Search & Rescue"]
radio_button_group = RadioButtonGroup(labels=LABELS, active=map_data['map_type'], sizing_mode="stretch_width")
def set_map_type(attr):
    print("TODO: map_type " + str(attr))
    map_data['map_type'] = attr
radio_button_group.on_click(set_map_type)
divTrack = Div(text="""Select which track this map will be for""", sizing_mode="stretch_both")


curdoc().add_root(Row(p, Column(divTrack, radio_button_group, divSurvivors, tableSurvivors, divFires, tableFires, divMapBounds, tableMapBounds, file_name, button, sizing_mode="stretch_both"), sizing_mode="stretch_both"))