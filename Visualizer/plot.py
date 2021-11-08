##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

from bokeh.models.tools import WheelZoomTool
from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode
from data import MapType

from bokeh.plotting import figure
from bokeh.models import PointDrawTool, PolyDrawTool
from bokeh.util.logconfig import bokeh_logger as log


class Plot(VisualizationSharedDataStore):
    def __init__(self) -> None:
        log.info(" -- INIT PLOT")
        self.Viz = VisualizationSharedDataStore
        self.Viz.plot = self

        # Create figure object.
        self.figure = figure(title='MIT Momentum Map Maker',
                             plot_height=1080,
                             plot_width=1920,
                             x_range=(
                                 self.Viz.data.bbox[0], self.Viz.data.bbox[2]),
                             y_range=(
                                 self.Viz.data.bbox[1], self.Viz.data.bbox[3]),
                             toolbar_location='below',
                             tools="pan, box_zoom, reset" if self.Viz.mode == Mode.MAP_MAKER else "reset",
                             sizing_mode="scale_both")
        self.figure.xgrid.grid_line_color = None
        self.figure.ygrid.grid_line_color = None

        self.figure.image_url(url=self.Viz.data.waterbodies_filepath,
                              x=self.Viz.data.area_bbox[0],
                              y=self.Viz.data.area_bbox[3],
                              w=self.Viz.data.area_bbox[2] -
                              self.Viz.data.area_bbox[0],
                              h=self.Viz.data.area_bbox[3] - self.Viz.data.area_bbox[1])
        self.figure.image_url(url='url',
                              x='lon',
                              y='lat',
                              anchor='center',
                              w='w',
                              w_units='screen',
                              h='h',
                              h_units='screen',
                              source=self.Viz.data.ownship_data_source)
        

        if(self.Viz.mode == Mode.MAP_MAKER):
            self.wheel_zoom_tool = WheelZoomTool(maintain_focus=True)
            self.figure.add_tools(self.wheel_zoom_tool)
            
            self.survivor_renderer = self.figure.scatter(
                x='x', y='y', color='orange', alpha=0.4, source=self.Viz.data.survivors_table_source, size=5)
            self.fires_renderer = self.figure.patches(
                xs='xs', ys='ys', fill_color='red', alpha=0.4, source=self.Viz.data.fires_table_source, line_width=0)

            self.survivor_tool = PointDrawTool(renderers=[self.survivor_renderer],
                                               description="Survivor draw tool (select, click once on map to survivors)")
            self.figure.add_tools(self.survivor_tool)
            self.figure.toolbar.active_tap = self.survivor_tool

            self.fire_tool = PolyDrawTool(renderers=[self.fires_renderer],
                                          description="Fire draw tool (select, double click on map to start, click once on map to add vertices, double click on map to end)")
            self.figure.add_tools(self.fire_tool)
        else:
            self.figure.line(source=self.Viz.data.drone_pos_data_source, x='lon', y='lat', alpha=1, color='olivedrab', line_width=5)
            if(self.Viz.data.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE):
                self.survivor_renderer = self.figure.scatter(
                    x='x', y='y', color='color', alpha='alpha', source=self.Viz.data.survivors_table_source, size=5)
            elif(self.Viz.data.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION):
                self.fires_renderer = self.figure.patches(
                    xs='xs', ys='ys', fill_color='fill_color', alpha='alpha', source=self.Viz.data.fires_table_source, line_width=0)
