##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################
# Datastore
from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode
from data import MapType

# Bokeh visualization
from bokeh.plotting import figure
from bokeh.models import PointDrawTool, PolyDrawTool, CrosshairTool, WheelZoomTool
from bokeh.util.logconfig import bokeh_logger as log


class Plot(VisualizationSharedDataStore):
    """
    Sets up the plot.
    
    Attributes
    ----------
    figure : bokeh.plotting.figure
        Figure where the ownship and object of interest are overlayed on top of the waterbodies picture.
    crosshair_tool : CrosshairTool
        Tool that aids in figuring out the lat/lon from axes.
    wheel_zoom_tool : WheelZoomTool
        Tool to zoom into the map using the mouse wheel.
    survivor_renderer : self.figure.scatter
        Renderer for the survivor icons.
    fires_renderer : self.figure.patches
        Renderer for the fire icons.
    survivor_tool : PointDrawTool
        Tool to draw the survivors.
    fire_tool : PolyDrawTool
        Tool to draw the fires.
    """
    
    def __init__(self) -> None:
        log.info(" -- INIT PLOT")
        self.Viz = VisualizationSharedDataStore
        self.Viz.plot = self

        # Create figure object.
        self.figure = figure(title='MIT Momentum Map Maker',
                             plot_height=1152,
                             plot_width=2048,
                             x_range=(self.Viz.data.bbox[0], 
                                      self.Viz.data.bbox[2]),
                             y_range=(self.Viz.data.bbox[1], 
                                      self.Viz.data.bbox[3]),
                             toolbar_location='below',
                             tools="pan, reset, box_select" 
                                    if self.Viz.mode == Mode.MAP_MAKER 
                                    else "reset",
                             sizing_mode="scale_both")
        self.figure.xgrid.grid_line_color = None
        self.figure.ygrid.grid_line_color = None

        # Show the waterbodies on the plot
        self.figure.image_url(url=self.Viz.data.waterbodies_filepath,
                              x=self.Viz.data.new_england_area_bbox[0],
                              y=self.Viz.data.new_england_area_bbox[3],
                              w=self.Viz.data.new_england_area_bbox[2] - self.Viz.data.new_england_area_bbox[0],
                              h=self.Viz.data.new_england_area_bbox[3] - self.Viz.data.new_england_area_bbox[1])
        
        # Show the ownship symbol on the plot
        self.figure.image_url(url='url',
                              x='lon',
                              y='lat',
                              anchor='center',
                              w='w',
                              w_units='screen',
                              h='h',
                              h_units='screen',
                              source=self.Viz.data.ownship_data_source)
        
        # Add the crosshair tool to aid in reading lat/lon from the axes
        self.crosshair_tool = CrosshairTool(description="Crosshair Tool")
        self.figure.add_tools(self.crosshair_tool)

        if(self.Viz.mode == Mode.MAP_MAKER):
            self.wheel_zoom_tool = WheelZoomTool(maintain_focus=True)
            self.figure.add_tools(self.wheel_zoom_tool)
            
            # Set up for plotting survivors
            # The plot will update automatically as data is manipulated in the table source
            self.survivor_renderer = self.figure.scatter(x='x', 
                                                         y='y', 
                                                         color='orange', 
                                                         alpha=1.0, 
                                                         source=self.Viz.data.survivors_table_source, 
                                                         size=10)
            # Set up for plotting fires
            # The plot will update automatically as data is manipulated in the table source
            self.fires_renderer = self.figure.patches(xs='xs', 
                                                      ys='ys', 
                                                      fill_color='red', 
                                                      alpha=1.0, 
                                                      source=self.Viz.data.fires_table_source, 
                                                      line_width=0)

            # Set up the tool for drawing survivors
            self.survivor_tool = PointDrawTool(renderers=[self.survivor_renderer],
                                               description="Survivor draw tool (select, click once on map to draw a survivor)")
            self.figure.add_tools(self.survivor_tool)
            self.figure.toolbar.active_tap = self.survivor_tool

            # Set up the tool for drawing fires
            self.fire_tool = PolyDrawTool(renderers=[self.fires_renderer],
                                          description="Fire draw tool (select, double click on map to start, click once on map to add vertices, double click on map to end with final vertex)")
            self.figure.add_tools(self.fire_tool)
        else: # Visualizer mode        
            # Set up the correct renderer type for our mode
            # The plot will update automatically as data is manipulated in the table source
            if(self.Viz.data.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE):
                # Set up for plotting survivors
                self.survivor_renderer = self.figure.scatter(x='x', 
                                                             y='y', 
                                                             color='color', 
                                                             alpha='alpha', 
                                                             source=self.Viz.data.survivors_table_source, 
                                                             size=10)
            elif(self.Viz.data.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION):
                # Set up for plotting fires
                # The plot will update automatically as data is manipulated in the table source
                self.fires_renderer = self.figure.patches(xs='xs', 
                                                          ys='ys', 
                                                          fill_color='fill_color', 
                                                          alpha='alpha', 
                                                          source=self.Viz.data.fires_table_source, 
                                                          line_width=0)
                
            ## This shows the radii of influence - useful for debugging
            # self.radii_debug_renderer = self.figure.patches(xs='xs', 
            #                                                 ys='ys', 
            #                                                 fill_color='green', 
            #                                                 alpha=0.5, 
            #                                                 source=self.Viz.data.debug_radii_table_source, 
            #                                                 line_width=0)
            # self.drone_radii_debug_renderer = self.figure.patches(xs='xs', 
            #                                                       ys='ys', 
            #                                                       fill_color='purple', 
            #                                                       alpha=0.5, 
            #                                                       source=self.Viz.data.debug_drone_table_source, 
            #                                                       line_width=0)
            
            # Set up for drawing the ownship track
            # The plot will update automatically as data is manipulated in the table source
            self.figure.line(x='lon', 
                             y='lat', 
                             color='olivedrab', 
                             alpha=1, 
                             source=self.Viz.data.drone_pos_data_source, 
                             line_width=5)
        
        # Show the ownship symbol on the plot
        self.figure.image_url(url='url',
                              x='lon',
                              y='lat',
                              anchor='center',
                              w='w',
                              w_units='screen',
                              h='h',
                              h_units='screen',
                              source=self.Viz.data.ownship_data_source)
        
