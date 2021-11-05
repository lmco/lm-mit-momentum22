from functools import partial
from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode
from data import Data
from data import MapType
from plot import Plot
from data_table import VizDataTable
from text import Text
from button import VizButton
from bokeh.util.logconfig import bokeh_logger as log

from bokeh.io import curdoc
from bokeh.plotting import Column, Row

import grpc_server


# https://stackoverflow.com/questions/22368458/how-to-make-argparse-print-usage-when-no-option-is-given-to-the-code
import argparse
parser = argparse.ArgumentParser(
    description="MIT Momentum 2022 Visualization and Map Maker Utility.", prog="bokeh serve Visualizer --show --args")
parser.add_argument("-m", "--mapmaker",
                    help="Launch the Map Maker", action="store_true")
parser.add_argument("-v", "--visualizer", nargs=1, metavar='MAPNAME',
                    help="Launch the visualizer (enter the name of the map or the map record filename)")
args = parser.parse_args()


class Visualizer(VisualizationSharedDataStore):
    def __init__(self) -> None:
        self.Viz = VisualizationSharedDataStore
        try:
            if(args.mapmaker):
                self.Viz.mode = Mode.MAP_MAKER
                log.info(" - MAP MAKER")

            elif(args.visualizer):
                self.Viz.mode = Mode.VISUALIZATION
                self.Viz.map_name = args.visualizer[0]
                log.info(" - VISUALIZER: " + args.visualizer[0])

            else:
                log.error(parser.print_usage())

        except Exception as e:
            log.error(e)

    def init(self) -> None:
        Data()
        Plot()
        VizDataTable()
        VizButton()
        Text()

    def update(self):
        if self.Viz.mode == Mode.VISUALIZATION:
            self.Viz.data.check_landing_status()
            self.Viz.data.check_takeoff_status()
            self.Viz.data.update_local_location()

    def serve(self) -> None:
        if self.Viz.mode == Mode.MAP_MAKER:
            curdoc().add_root(Row(self.Viz.plot.figure, Column(self.Viz.button.radio_button_description,
                                                               self.Viz.button.radio_button_group,
                                                               self.Viz.data_table.survivors_table_description,
                                                               self.Viz.data_table.survivors_table,
                                                               self.Viz.data_table.fires_table_description,
                                                               self.Viz.data_table.fires_table,
                                                               self.Viz.data_table.bounds_table_description,
                                                               self.Viz.data_table.bounds_table,
                                                               self.Viz.data_table.wind_table_description,
                                                               self.Viz.data_table.wind_table,
                                                               self.Viz.text.map_name_text_box,
                                                               self.Viz.button.save_button,
                                                               self.Viz.button.cheat_button,
                                                               sizing_mode="stretch_both"), sizing_mode="stretch_both"))
        elif self.Viz.mode == Mode.VISUALIZATION and self.Viz.data.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION:
            curdoc().add_root(Row(self.Viz.plot.figure, Column(self.Viz.button.radio_button_description,
                                                               self.Viz.data_table.stats_table_description,
                                                               self.Viz.data_table.stats_table,
                                                               self.Viz.data_table.fires_table_description,
                                                               self.Viz.data_table.fires_table,
                                                               self.Viz.data_table.bounds_table_description,
                                                               self.Viz.data_table.bounds_table,
                                                               self.Viz.data_table.wind_table_description,
                                                               self.Viz.data_table.wind_table,
                                                               self.Viz.text.map_name_text_box,
                                                               self.Viz.button.save_button,
                                                               self.Viz.button.cheat_button,
                                                               sizing_mode="stretch_both"), sizing_mode="stretch_both"))
        elif self.Viz.mode == Mode.VISUALIZATION and self.Viz.data.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE:
            curdoc().add_root(Row(self.Viz.plot.figure, Column(self.Viz.button.radio_button_description,
                                                               self.Viz.data_table.stats_table_description,
                                                               self.Viz.data_table.stats_table,
                                                               self.Viz.data_table.survivors_table_description,
                                                               self.Viz.data_table.survivors_table,
                                                               self.Viz.data_table.bounds_table_description,
                                                               self.Viz.data_table.bounds_table,
                                                               self.Viz.data_table.wind_table_description,
                                                               self.Viz.data_table.wind_table,
                                                               self.Viz.text.map_name_text_box,
                                                               self.Viz.button.save_button,
                                                               self.Viz.button.cheat_button,
                                                               sizing_mode="stretch_both"), sizing_mode="stretch_both"))

        if self.Viz.mode == Mode.VISUALIZATION:
            grpc_server.start(self.data.qLanding, self.data.qTakeoff, self.data.qLocation)
            
            curdoc().add_periodic_callback(self.update, 10)  # period in ms            


visualizer = Visualizer()
visualizer.init()
visualizer.serve()
