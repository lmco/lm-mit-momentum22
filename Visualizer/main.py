##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

"""
Top level script that serves as the Bokeh entry point.
Serves the Momentum 2022 Visualization in the browser
(by default at http://localhost:5006/Visualizer).

Usage of this script is:
    * bokeh serve Visualizer --show --args -m <mapname>
    * bokeh serve Visualizer --show --args -v <mapname>
For more details on how to use the above, see the module readme.
"""

# Datastore
from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode
from data import Data
from data import MapType
from plot import Plot
from data_table import VizDataTable
from text import Text
from button import VizButton

# Bokeh visualization
from bokeh.util.logconfig import bokeh_logger as log
from bokeh.io import curdoc
from bokeh.plotting import Column, Row

# Grpc
import grpc_server

# Argparse
import argparse

# https://stackoverflow.com/questions/22368458/how-to-make-argparse-print-usage-when-no-option-is-given-to-the-code
parser = argparse.ArgumentParser(description="MIT Momentum 2022 Visualization and Map Maker Utility.", 
                                 prog="bokeh serve Visualizer --show --args")
group = parser.add_mutually_exclusive_group()
# Add mapmaker argument
group.add_argument("-m", 
                   "--mapmaker", 
                   nargs='?', 
                   type=str, 
                   metavar='MAPNAME', 
                   const=1,
                   help="Launch the Map Maker (with an optional map name to edit the map or create a derivative)")
# Add mapmaker visualizer
group.add_argument("-v", 
                   "--visualizer", 
                   nargs=1, 
                   metavar='MAPNAME',
                   help="Launch the visualizer (enter the name of the map or the map record filename)")
args = parser.parse_args()


class Visualizer(VisualizationSharedDataStore):
    """ 
    Top-level class for the visualization application.
    
    Attributes
    ----------
    Viz : VisualizationSharedDataStore
        Datastore that contains the component objects of the visualizer.
        
    Methods
    -------
    init()
        Initializes the components of the visualization.
    update()
        Checks on the messages coming from the student code.
    serve()
        Assembles the page according to the type of mode and serves it.
    """
    
    def __init__(self) -> None:
        self.Viz = VisualizationSharedDataStore
        try:
            if(args.mapmaker):
                self.Viz.mode = Mode.MAP_MAKER
                if(args.mapmaker != 1):
                    self.Viz.map_name = args.mapmaker

                log.info(" - MAP MAKER")

            elif(args.visualizer):
                self.Viz.mode = Mode.VISUALIZATION
                self.Viz.map_name = args.visualizer[0]
                log.info(" - VISUALIZER")

            else:
                log.error(parser.print_usage())

        except Exception as e:
            log.error(e)



    def init(self) -> None:
        """ 
        Initializes the components necessary to start the Visualization in the correct order.
        """
        
        Data()
        Plot()
        VizDataTable()
        VizButton()
        Text()

    def update(self) -> None:
        """ 
        Checks in on data coming over from the student code.
        Intended as a periodic callback function called by curdoc.
        """
        
        if self.Viz.mode == Mode.VISUALIZATION:
            self.Viz.data.check_landing_status()
            self.Viz.data.check_takeoff_status()
            self.Viz.data.update_local_location()
    
    def file_io_update(self) -> None:
        if self.Viz.mode == Mode.VISUALIZATION:
            done = False
            while not done:
                try:
                    done = self.Viz.data.prep_viz_data()
                except KeyboardInterrupt:
                    continue
            


    def serve(self) -> None:
        """
        Assembles the page according to the type of mode and serves it.
        
        Also sets up the callback to update data that depend on the grpc connection.
        """
        
        if self.Viz.mode == Mode.MAP_MAKER:
            curdoc().add_root(Row(self.Viz.plot.figure, Column(self.Viz.button.radio_button_description,
                                                               self.Viz.button.radio_button_group,
                                                               self.Viz.data_table.survivors_table_description,
                                                               self.Viz.data_table.survivors_table,
                                                               self.Viz.data_table.fires_table_description,
                                                               self.Viz.data_table.fires_table,
                                                               self.Viz.data_table.bounds_table_description,
                                                               self.Viz.data_table.bounds_table,
                                                            #    self.Viz.data_table.wind_table_description, # TODO: wind not implemented, so don't show it
                                                            #    self.Viz.data_table.wind_table,
                                                               self.Viz.button.cheat_button,
                                                               self.Viz.text.map_name_text_box,
                                                               self.Viz.button.save_as_button,
                                                               self.Viz.button.bind_map_button,
                                                               width_policy="min", min_width=500), width_policy="max", width=2048))
            curdoc().title = "Momentum 22 MapMaker"
        elif self.Viz.mode == Mode.VISUALIZATION and self.Viz.data.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION:
            curdoc().add_root(Row(self.Viz.plot.figure, Column(self.Viz.button.radio_button_description,
                                                               self.Viz.data_table.stats_table_description,
                                                               self.Viz.data_table.stats_table,
                                                               self.Viz.data_table.fires_table_description,
                                                               self.Viz.data_table.fires_table,
                                                               self.Viz.data_table.bounds_table_description,
                                                               self.Viz.data_table.bounds_table,
                                                            #    self.Viz.data_table.wind_table_description,
                                                            #    self.Viz.data_table.wind_table,
                                                               self.Viz.text.map_name_text_box,
                                                               self.Viz.button.save_as_button,
                                                               self.Viz.button.cheat_button,
                                                               width_policy="min", min_width=500), width_policy="max", width=2048))
        elif self.Viz.mode == Mode.VISUALIZATION and self.Viz.data.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE and not self.Viz.data.disable_save:
            curdoc().add_root(Row(self.Viz.plot.figure, Column(self.Viz.button.radio_button_description,
                                                               self.Viz.data_table.stats_table_description,
                                                               self.Viz.data_table.stats_table,
                                                               self.Viz.data_table.survivors_table_description,
                                                               self.Viz.data_table.survivors_table,
                                                               self.Viz.data_table.bounds_table_description,
                                                               self.Viz.data_table.bounds_table,
                                                            #    self.Viz.data_table.wind_table_description,
                                                            #    self.Viz.data_table.wind_table,
                                                               self.Viz.text.map_name_text_box,
                                                               self.Viz.button.save_as_button,
                                                               self.Viz.button.cheat_button,
                                                               width_policy="min", min_width=500), width_policy="max", width=2048))
        elif self.Viz.mode == Mode.VISUALIZATION and self.Viz.data.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE and self.Viz.data.disable_save:
            curdoc().add_root(Row(self.Viz.plot.figure, Column(self.Viz.button.radio_button_description,
                                                               self.Viz.data_table.stats_table_description,
                                                               self.Viz.data_table.stats_table,
                                                               self.Viz.data_table.bounds_table_description,
                                                               self.Viz.data_table.bounds_table,
                                                            #    self.Viz.data_table.wind_table_description,
                                                            #    self.Viz.data_table.wind_table,
                                                               self.Viz.text.map_name_text_box,
                                                               self.Viz.button.save_as_button,
                                                               self.Viz.button.cheat_button,
                                                               width_policy="min", min_width=500), width_policy="max", width=2048))

        if self.Viz.mode == Mode.VISUALIZATION:
            # Start the grpc server (internally operates in another process)
            grpc_server.start(self.data.qLanding, self.data.qTakeoff, self.data.qLocation)
            
            #https://discourse.bokeh.org/t/bokeh-application-title/1068/3
            curdoc().title = "Momentum 22 Visualizer"
            
            # Check in on grpc data every 10 ms
            curdoc().add_periodic_callback(self.update, 10)  # period in ms            
            # Check in on grpc data every 500 ms - rarer to make sure that we don't make everything sluggish for this
            curdoc().add_periodic_callback(self.file_io_update, 500)  # period in ms       

# Create the visualizer
visualizer = Visualizer()
# Initialize the components
visualizer.init()
# Start serving the page and processing the updates
visualizer.serve()