##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode

from bokeh.models import GeoJSONDataSource, ColumnDataSource
import os
import geopandas as gpd
import inspect
import json
from datetime import datetime
import traceback
from enum import IntEnum
from bokeh.util.logconfig import bokeh_logger as log
from pathlib import Path
from typing import Dict
from multiprocessing import Queue
from queue import Empty
import collections


class MapType(IntEnum):
    FIRE_SUPPRESSION = 0
    SEARCH_AND_RESCUE = 1


class Data(VisualizationSharedDataStore):
    def __init__(self, **kwargs) -> None:
        log.info(" -- INIT DATA")
        self.Viz = VisualizationSharedDataStore
        self.Viz.data = self
        
        self.qLanding = Queue()
        self.qTakeoff = Queue()
        self.qLocation = Queue()
        
        self.start_time = -1
        
        self.map_data_dict = None

        # Create bounding box for the scope of mapping (contiguous USA)
        self.contiguous_usa_bbox = (-130.25390625,
                                    22.55314748, -65.63232422, 49.55372551)
        if(self.Viz.mode == Mode.MAP_MAKER):
            self.bbox = self.contiguous_usa_bbox
            self.map_data_dict = {
                "map_name": "sample_name",
                "map_type": MapType.FIRE_SUPPRESSION,
                "bounds": {'minx': self.bbox[0],
                           'miny': self.bbox[1],
                           'maxx': self.bbox[2],
                           'maxy': self.bbox[3]},
                "data_fs": {'xs': [],
                            'ys': [], },
                "data_snr": {'x': [],
                             'y': []},
                "wind": {'spd_kts': 0,
                         'dir_deg': 0},
                "mission_duration_min": 6,
            }
        elif(self.Viz.map_name is not None):
            self.map_data_dict = self.load_map_record(self.Viz.map_name)
            self.bbox = (self.Viz.data.map_data_dict['bounds']['minx'][0],
                         self.Viz.data.map_data_dict['bounds']['miny'][0],
                         self.Viz.data.map_data_dict['bounds']['maxx'][0],
                         self.Viz.data.map_data_dict['bounds']['maxy'][0])
        else:
            log.error("Visualizer map name still None")

        # May choose to not draw these... this is just for reference
        usa_state_outlines = gpd.read_file(os.path.join(os.path.basename(os.path.dirname(inspect.getfile(
            lambda: None))), 'static/cb_2018_us_state_20m.zip'), bbox=self.bbox, crs="EPSG:4326")

        # Convert data to geojson for bokeh
        self.usa_states_outlines_geojson = GeoJSONDataSource(
            geojson=usa_state_outlines.to_json())

        self.waterbodies_filepath = [os.path.join(os.path.basename(
            os.path.dirname(inspect.getfile(lambda: None))), 'static', 'waterbodies.svg')]
        
        self.ownship_filepath = [os.path.join(os.path.basename(
            os.path.dirname(inspect.getfile(lambda: None))), 'static', 'Picture2.png')]

        self.ownship_data_source = ColumnDataSource({
                'url': self.ownship_filepath,
                'lat': [0],
                'lon': [0],
                'w': [20],
                'h': [20],
                })
        
        self.wind_table_source = ColumnDataSource({
                'spd_kts': [self.Viz.data.map_data_dict['wind']['spd_kts']],
                'dir_deg': [self.Viz.data.map_data_dict['wind']['dir_deg']]})
        self.bounds_table_source = ColumnDataSource({
                'minx': [self.Viz.data.map_data_dict['bounds']['minx']],
                'miny': [self.Viz.data.map_data_dict['bounds']['miny']],
                'maxx': [self.Viz.data.map_data_dict['bounds']['maxx']],
                'maxy': [self.Viz.data.map_data_dict['bounds']['maxy']]})
        self.stats_table_source = ColumnDataSource({
                'elapsed_dur': [0],
                'remaining_dur': [0],
                'mission_stat': [0],
                'lat': [0],
                'lon': [0],
                'status': [0]})
        
        self.drone_pos_data_source = ColumnDataSource({
                'lat': [0],
                'lon': [0]})
        

        # Table data sources
        if(self.Viz.mode == Mode.MAP_MAKER):
            self.survivors_table_source = ColumnDataSource({
                'x': [self.Viz.data.map_data_dict['data_snr']['x']],
                'y': [self.Viz.data.map_data_dict['data_snr']['y']]})
            self.fires_table_source = ColumnDataSource({
                'xs': [self.Viz.data.map_data_dict['data_fs']['xs']],
                'ys': [self.Viz.data.map_data_dict['data_fs']['ys']]})
        else:
            self.survivors_table_source = ColumnDataSource({
                'x': self.Viz.data.map_data_dict['data_snr']['x'],
                'y': self.Viz.data.map_data_dict['data_snr']['y'],
                'color': ['orange']*len(self.Viz.data.map_data_dict['data_snr']['y']),
                'alpha': [0.0]*len(self.Viz.data.map_data_dict['data_snr']['y'])} if self.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE else {})
            self.fires_table_source = ColumnDataSource({
                'xs': self.Viz.data.map_data_dict['data_fs']['xs'],
                'ys': self.Viz.data.map_data_dict['data_fs']['ys'],
                'fill_color': ['red']*len(self.Viz.data.map_data_dict['data_fs']['ys']),
                'alpha': [0]*len(self.Viz.data.map_data_dict['data_fs']['ys'])} if self.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION else {})
            
        
        

    def save_map_record(self) -> None:
        try:
            log.info(" ---- Saving map")
            Path("maps").mkdir(parents=True, exist_ok=True)
            with open("maps/" + self.map_data_dict['map_name'] + ".json", 'w+') as outfile:
                self.map_data_dict["generated_on"] = datetime.now().strftime(
                    "%d/%m/%Y_%H:%M:%S")
                self.map_data_dict["bounds"] = self.Viz.data_table.bounds_table.source.data
                self.map_data_dict["data_fs"]['xs'] = self.Viz.data_table.fires_table.source.data['xs'][1:]
                self.map_data_dict["data_fs"]['ys'] = self.Viz.data_table.fires_table.source.data['ys'][1:]
                self.map_data_dict["data_snr"]['x'] = self.Viz.data_table.survivors_table.source.data['x'][1:]
                self.map_data_dict["data_snr"]['y'] = self.Viz.data_table.survivors_table.source.data['y'][1:]

                json.dump(self.map_data_dict, outfile,
                          indent=4, sort_keys=True)
        except:
            log.error(traceback.format_exc())
            log.error("Map save encountered an issue (see traceback above)")

    def load_map_record(self, map_name) -> Dict:
        with open("maps/" + map_name + ".json") as f:
            map_data = json.load(f)
            return map_data

    def check_landing_status(self):
        try:
            if(not self.qLanding.empty()):
                log.info(" --- Updating landing status")
            ln = self.qLanding.get(block=True, timeout=0.1)
            if(ln.isLanded):
                self.stats_table_source.patch({'status': [(0, "On the Ground")]})
        except Empty:
            pass
    def check_takeoff_status(self):
        try:
            if(not self.qTakeoff.empty()):
                log.info(" --- Updating takeoff status")
            tn = self.qTakeoff.get(block=True, timeout=0.1)
            if(tn.isTakenOff and self.start_time == -1):
                self.start_time = tn.px4Time/1000.0
                self.stats_table_source.patch({'status': [(0, "Taking Off")]})
        except Empty:
            pass
    def update_local_location(self):
        try:
            if(not self.qLocation.empty()):
                log.info(" --- Updating local location")
            loc = self.qLocation.get(block=True, timeout=0.1)
            
            self.stats_table_source.patch({'elapsed_dur': [(0, loc.px4Time/1000.0 - self.start_time)],
                                           'remaining_dur': [(0, self.map_data_dict['mission_duration_min']*60 - loc.px4Time/1000.0 - self.start_time)],
                                           'lat': [(0, loc.latitude)],
                                           'lon': [(0, loc.longitude)],
                                           'status': [(0, "In Air")]})
            
            self.ownship_data_source.patch({'lat': [(0, loc.latitude)],
                                           'lon': [(0, loc.longitude)]})
            
            
            if(self.drone_pos_data_source.data['lat'][0] == 0):
                self.drone_pos_data_source.data = {
                    'lat': [loc.latitude],
                    'lon': [loc.longitude]
                }
            else:
                new_lat = self.flatten([self.drone_pos_data_source.data['lat'], loc.latitude])
                new_lon = self.flatten([self.drone_pos_data_source.data['lon'], loc.longitude])
                self.drone_pos_data_source.data = {
                    'lat': new_lat,
                    'lon': new_lon
                }
            log.info(self.drone_pos_data_source.data)
            
            
        except Empty:
            pass
        
    def flatten(self, x):
        #https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
        if isinstance(x, collections.Iterable):
            return [a for i in x for a in self.flatten(i)]
        else:
            return [x]