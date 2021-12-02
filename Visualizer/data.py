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
from shapely.geometry import Point, Polygon
from shapely.ops import transform
from rtree import index
import pyproj
from functools import partial
import math


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
        # self.area_bbox = (-130.25390625, 22.55314748, -65.63232422, 49.55372551)
        
        # Create bounding box for the scope of mapping (New England)
        self.area_bbox = (-80.41417236584573, 40.258338053379745, -69.06461890186635, 44.5188750075358)
        if(self.Viz.mode == Mode.MAP_MAKER):
            self.bbox = self.area_bbox
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
        
        self.waterbodies = gpd.read_file('data/waterbodies.geojson', bbox=self.bbox, crs="EPSG:4326")
        
        self.radius_of_influence = 25 if self.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE else 1 # in m
        
        self.polygons_of_interest = []
        if self.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION:
            for i in range(0, len(self.map_data_dict["data_fs"]['xs'])):
                xs = self.map_data_dict["data_fs"]['xs'][i]
                ys = self.map_data_dict["data_fs"]['ys'][i]
                
                self.polygons_of_interest.append(Polygon(tuple(zip(xs, ys))))
                self.starting_fire_area = 0
                for polygon in self.polygons_of_interest:
                    self.starting_fire_area = self.starting_fire_area + polygon.area*6370**2 
                
        else:
            merged_list = tuple(zip(self.map_data_dict["data_snr"]['x'], self.map_data_dict["data_snr"]['y'])) 
            for survivor in merged_list:
                self.polygons_of_interest.append(self.point_to_circle(survivor, 5))
        
        
        self.survivors_found = 0
        
        self.water_limit = 100
        self.water_quantity = 0
        self.water_start_time = -1
        
        self.fire_last_observed_time = -1

        self.waterbodies_filepath = [os.path.join(os.path.basename(
            os.path.dirname(inspect.getfile(lambda: None))), 'static', 'waterbodies.svg')]
        
        self.ownship_filepath = [os.path.join(os.path.basename(
            os.path.dirname(inspect.getfile(lambda: None))), 'static', 'Picture2.png')]

        self.ownship_data_source = ColumnDataSource({
                'url': self.ownship_filepath,
                'lon': [0],
                'lat': [0],
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
                'lon': [0],
                'lat': [0],
                'status': [0],
                'score': [0]})
        
        self.drone_pos_data_source = ColumnDataSource({
                'lon': [0],
                'lat': [0]
                })
        

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
                'alpha': [1]*len(self.Viz.data.map_data_dict['data_fs']['ys'])} if self.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION else {})
            
        self.debug_radii_table_source = ColumnDataSource({
                'xs': [list(poly.exterior.coords.xy[0]) for poly in self.polygons_of_interest],
                'ys': [list(poly.exterior.coords.xy[1]) for poly in self.polygons_of_interest]})
        
        self.debug_drone_table_source = ColumnDataSource({
                'xs': [0],
                'ys': [0]})
            
        
        

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
            ln = self.qLanding.get(block=False)
            if(ln.isLanded):
                self.stats_table_source.patch({'status': [(0, "On the Ground")]})
        except Empty:
            pass
        
    def check_takeoff_status(self):
        try:
            if(not self.qTakeoff.empty()):
                log.info(" --- Updating takeoff status")
            tn = self.qTakeoff.get(block=False)
            if(tn.isTakenOff and self.start_time == -1):
                self.start_time = tn.px4Time/1000.0
                self.stats_table_source.patch({'status': [(0, "Taking Off")]})
        except Empty:
            pass
        
    def update_local_location(self):
        try:
            if(not self.qLocation.empty()):
                log.info(" --- Updating local location")
            loc = self.qLocation.get(block=False)
            elapsed_duration = loc.px4Time/1000.0 - self.start_time
            self.stats_table_source.patch({'elapsed_dur': [(0, math.floor(elapsed_duration))],
                                           'remaining_dur': [(0, math.floor(self.map_data_dict['mission_duration_min']*60.0 - elapsed_duration))],
                                           'lon': [(0, loc.longitude)],
                                           'lat': [(0, loc.latitude)],
                                           'status': [(0, "In Air")]})
            
            self.ownship_data_source.patch({'lon': [(0, loc.longitude)],
                                            'lat': [(0, loc.latitude)],
                                           })
            
            
            if(self.drone_pos_data_source.data['lat'][0] == 0):
                self.drone_pos_data_source.data = {
                    'lon': [loc.longitude],
                    'lat': [loc.latitude]
                }
            else:
                new_lat = self.flatten([self.drone_pos_data_source.data['lat'], loc.latitude])
                new_lon = self.flatten([self.drone_pos_data_source.data['lon'], loc.longitude])
                self.drone_pos_data_source.data = {
                    'lon': new_lon,
                    'lat': new_lat
                }
            # log.info([self.drone_pos_data_source.data['lon'][-1], self.drone_pos_data_source.data['lat'][-1]])
            
            drone_circle = self.point_to_circle((loc.longitude, loc.latitude), self.radius_of_influence)
            if self.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION:
                self.fire_suppression_intersections(drone_circle, loc.px4Time)
            else:
                self.snr_intersections(drone_circle)
                
            self.debug_drone_table_source.patch({'xs': [(0, list(drone_circle.exterior.coords.xy[0]))],
                                                'ys': [(0, list(drone_circle.exterior.coords.xy[1]))]})           
            
        except Empty:
            pass
        
    def flatten(self, x):
        #https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
        if isinstance(x, collections.Iterable):
            return [a for i in x for a in self.flatten(i)]
        else:
            return [x]
    
    def point_to_circle(self, point_coord, radius):
        # https://gis.stackexchange.com/questions/367496/plot-a-circle-with-a-given-radius-around-points-on-map-using-python
        lon, lat = point_coord

        local_azimuthal_projection = "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(
            lat, lon
        )
        wgs84_to_aeqd = partial(
            pyproj.transform,
            pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
            pyproj.Proj(local_azimuthal_projection),
        )
        aeqd_to_wgs84 = partial(
            pyproj.transform,
            pyproj.Proj(local_azimuthal_projection),
            pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
        )

        center = Point(float(lon), float(lat))
        point_transformed = transform(wgs84_to_aeqd, center)
        buffer = point_transformed.buffer(radius)
        
        polygon = transform(aeqd_to_wgs84, buffer)
        # Get the polygon with lat lon coordinates
        return polygon
    
    def fire_suppression_intersections(self, drone_circle, time_location_observed):        
        object_indeces = self.check_drone_location_against_object_of_interest(drone_circle, self.polygons_of_interest)
        fire_area_now = 0
        if(len(object_indeces) > 0 and self.water_quantity > 0):
            if(self.fire_last_observed_time == -1):
                self.fire_last_observed_time = time_location_observed
                
            for idx in object_indeces:
                polygon_reduction_factor = 0.05
                if(self.water_quantity > ((time_location_observed - self.fire_last_observed_time)/1000.0) * 10.0):
                    self.polygons_of_interest[idx] = self.shrink_shapely_polygon(self.polygons_of_interest[idx], polygon_reduction_factor * ((time_location_observed - self.fire_last_observed_time)/1000.0))
                
                    self.water_quantity -= ((time_location_observed - self.fire_last_observed_time)/1000.0) * 10.0
                else:
                    factor = self.water_quantity / ( ((time_location_observed - self.fire_last_observed_time)/1000.0) * 10.0 ) * polygon_reduction_factor
                    self.polygons_of_interest[idx] = self.shrink_shapely_polygon(self.polygons_of_interest[idx], factor * ((time_location_observed - self.fire_last_observed_time)/1000.0))
                    self.water_quantity = 0
                    
                if(self.polygons_of_interest[idx].is_empty):
                    self.fires_table_source.patch({ 'xs': [(idx, [0])],
                                                    'ys': [(idx, [0])]})
                else:
                    self.fires_table_source.patch({ 'xs': [(idx, list(self.polygons_of_interest[idx].exterior.coords.xy[0]))],
                                                    'ys': [(idx, list(self.polygons_of_interest[idx].exterior.coords.xy[1]))]})
                
            self.fire_last_observed_time = time_location_observed
            
        else:
            self.fire_last_observed_time = -1
            
        for poly in self.polygons_of_interest:
            fire_area_now += poly.area*6370**2 
        
        # left sjoin on position in order to check if the points are in the waterbodies
        # https://gis.stackexchange.com/questions/208546/check-if-a-point-falls-within-a-multipolygon-with-python
        # Solution 4
        points_world = gpd.GeoDataFrame({'notes': ['drone'], 'geometry': [
            drone_circle
            ]}, crs="EPSG:4326")

        pointInWaterbodies = gpd.sjoin(points_world, self.waterbodies, how='left')
        groupedInWaterbodies = pointInWaterbodies.groupby('index_right')
        if(len(groupedInWaterbodies.groups) > 0):
            if(self.water_start_time == -1):
                self.water_start_time = time_location_observed
            self.water_quantity = (time_location_observed - self.water_start_time)/1000 * 10  # 10 gallons/sec
            self.water_quantity = self.water_limit if self.water_quantity > self.water_limit else self.water_quantity
            self.stats_table_source.patch({'mission_stat': [(0, self.water_quantity)]})
        else:
            self.water_start_time = -1
        
        self.stats_table_source.patch({'score': [(0, 100.0 - (fire_area_now/float(self.starting_fire_area) * 100.0))]})
        self.stats_table_source.patch({'mission_stat': [(0, self.water_quantity)]})
    
    def snr_intersections(self, drone_circle):        
        object_indeces = self.check_drone_location_against_object_of_interest(drone_circle, self.polygons_of_interest)
        for idx in object_indeces:
            if self.survivors_table_source.data['alpha'][idx] == 0:
                self.survivors_found = self.survivors_found + 1
                self.survivors_table_source.patch({'alpha': [(idx, 1)]});
            
        # TODO: this is the score
        self.stats_table_source.patch({'mission_stat': [(0, self.survivors_found/float(len(self.map_data_dict["data_snr"]['x']))*100.0)]})
        self.stats_table_source.patch({'score': [(0, self.survivors_found)]})

    def check_drone_location_against_object_of_interest(self, drone_circle, objects):
        # https://stackoverflow.com/questions/14697442/faster-way-of-polygon-intersection-with-shapely/14804366
        idx = index.Index()
        # Populate R-tree index with bounds of grid cells
        for pos, cell in enumerate(objects):
            # assuming cell is a shapely object
            idx.insert(pos, cell.bounds)
        
        object_indeces = []
        for pos in idx.intersection(drone_circle.bounds):
            object_indeces.append(pos)
        
        return object_indeces
    
    def shrink_shapely_polygon(self, my_polygon, factor=0.10):
        # https://stackoverflow.com/a/67205583
        ''' returns the shapely polygon which is smaller or bigger by passed factor.
            If swell = True , then it returns bigger polygon, else smaller '''

        xs = list(my_polygon.exterior.coords.xy[0])
        ys = list(my_polygon.exterior.coords.xy[1])
        x_center = 0.5 * min(xs) + 0.5 * max(xs)
        y_center = 0.5 * min(ys) + 0.5 * max(ys)
        min_corner = Point(min(xs), min(ys))
        # max_corner = Point(max(xs), max(ys))
        center = Point(x_center, y_center)
        shrink_distance = center.distance(min_corner)*factor
        
        my_polygon_shrunken = my_polygon.buffer(-shrink_distance) #shrink

        # # visualize for debugging
        # x, y = my_polygon.exterior.xy
        # plt.plot(x,y)
        # x, y = my_polygon_shrunken.exterior.xy
        # plt.plot(x,y)
        # # to net let the image be distorted along the axis
        # plt.axis('equal')
        # plt.show()    
    
        return my_polygon_shrunken
    