##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

# Datastore
from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode

# Bokeh visualization
from bokeh.models import GeoJSONDataSource, ColumnDataSource
from bokeh.util.logconfig import bokeh_logger as log

# Shape and coordinate shaping tools
import geopandas as gpd
from shapely.geometry import Point, Polygon
from shapely.ops import transform
from rtree import index
import pyproj
from functools import partial
import math

# Helpers
from enum import IntEnum
import os
import inspect
from typing import Dict
from map_reader import map_reader

# Multiprocessing for grpc data
from multiprocessing import Queue
from queue import Empty
import collections


class MapType(IntEnum):
    """
    Represents the supported map types.
    
    Modes
    -----
    FIRE_SUPPRESSION : 0
        Fire suppression challenge.
    SEARCH_AND_RESCUE : 1
        Search and rescue challenge.
    """
    
    FIRE_SUPPRESSION = 0
    SEARCH_AND_RESCUE = 1


class Data(VisualizationSharedDataStore):
    """
    Stores all of the primary data and performs all of the necessary calculations.

    This is the where all of the math is.

    Parameters
    ----------
    qLanding : multiprocessing.Queue
        Storage for what comes over the grpc line.
    qTakeoff : multiprocessing.Queue
        Storage for what comes over the grpc line.
    qLocation : multiprocessing.Queue
        Storage for what comes over the grpc line.
    start_time : int
        Time when the mission is started.
    map_data_dict : Dict
        Data read from or written to the map file (depending on the mode).
    new_england_area_bbox : float tuple
        Bounding box that describes roughly New England.
    bbox : float tuple
        Bounding box that describes the active area.
    standard_window_lat : float
        Y-axis value to standardize maps over.
    usa_state_outlines : geopandas.GeoDataFrame
        Data Frame containing state outlines for spatial orientation with the map.
    usa_states_outlines_geojson : bokeh.models.GeoJSONDataSource
        GeoJSONDataSource obtained from the Data Frame with the state outlines for plotting in Bokeh.
    waterbodies : geopandas.GeoDataFrame
        Waterbody data used to see if the drone is over water.
    radius_of_influence : float
        Radius within which the drone can collect and deposit water, and see survivors.
    polygons_of_interest : shapely.Polygon list
        List containing all items of interest as Shapely Polygons.
    starting_fire_area : float
        Starting area of fires (used for scoring)
    survivors_found : int
        Count of the number of survivors found.
    water_limit : float
        Limit on how much water can be carried by the drone.
    water_quantity : float
        Current water quantity.
    water_start_time : int
        Time when started collecting water.
    fire_last_observed_time : int
        Time when last observed fire.
    waterbodies_filepath : pathlib.Path list
        Filepath where to find the waterbodies file.
    ownship_filepath : pathlib.Path list
        Filepath where to find the ownship symbol.
    ownship_data_source : bokeh.models.ColumnDataSource
        Data source to drive the drawing of the ownship track.
    wind_table_source : bokeh.models.ColumnDataSource
        Data source to drive the wind tables (not implemented).
    bounds_table_source : bokeh.models.ColumnDataSource
        Data source to drive the bounds table and to save those bounds to the map file.
    stats_table_source : bokeh.models.ColumnDataSource
        Data source to drive the mission statistics table.
    drone_pos_data_source : bokeh.models.ColumnDataSource
        Data source to drive the ownship location.
    survivors_table_source : bokeh.models.ColumnDataSource
        Data source to drive the drawing of the survivors.
    fires_table_source : bokeh.models.ColumnDataSource
        Data source to drive the drawing of the fires.
    debug_radii_table_source : bokeh.models.ColumnDataSource    
        Data source to drive the drawing of the radii of influence (useful for debugging).
    debug_drone_table_source : bokeh.models.ColumnDataSource
        Data source to drive the drone debug table.
        
    Methods
    -------
    save_map_record_as()
        Saves the map record to file.
    load_map_record(map_name: str)
        Loads a map record from file.
    bind_bbox()
        Binds a bounding box to the standard_window_lat value.
    check_landing_status()
        Checks the landing status (from the grpc messages).
    check_takeoff_status()
        Checks the takeoff status (from the grpc messages).
    update_local_location()
        Checks the local location (from the grpc messages).
    flatten(x: list)
        Flattens a list to from a list of lists of lists... to a single list.
    point_to_circle(point_coord: tuple, radius: float)
        Creates a shapely circle with specified radius around the given point.
    fire_suppression_intersections(drone_circle: Polygon, time_location_observed: int)
        Checks if the drone is over fire and performs scoring.
    snr_intersections(drone_circle: Polygon)
        Checks if the drone is over a survivors and performs scoring.
    check_drone_location_against_object_of_interest(drone_circle: Polygon, objects: list)
        Checks if the drone over a generic object of interest.
    shrink_shapely_polygon(my_polygon: Polygon, factor: float=0.10)
        Shrinks a polygon by the given factor.
    """
    
    def __init__(self) -> None:
        log.info(" -- INIT DATA")
        self.Viz = VisualizationSharedDataStore
        self.Viz.data = self
        
        # gRPC queues (this is where the data from gRPC comes into)
        self.qLanding = Queue()
        self.qTakeoff = Queue()
        self.qLocation = Queue()
        
        # Time when we started the mission (-1 means we haven't started)
        self.start_time = -1
        
        # Data read from the mission file
        self.map_data_dict = None

        # Create bounding box for the scope of mapping (contiguous USA or New England)
        # self.usa_area_bbox = (-130.25390625, 22.55314748, -65.63232422, 49.55372551)
        self.new_england_area_bbox = (-80.41417236584573, 40.258338053379745, -69.06461890186635, 44.5188750075358)
        
        if(self.Viz.mode == Mode.MAP_MAKER and self.Viz.map_name is None):
            # Set the active area to the maximum and allow the user to
            # zoom into wherever they want.
            self.bbox = self.new_england_area_bbox
            
            # Creating a new map, so need to create a new map and 
            # there's nothing to read into the map_data_dict.
            self.map_data_dict = {
                "map_name": "sample_name",
                "map_type": MapType.FIRE_SUPPRESSION,
                "bounds": {'minx': self.new_england_area_bbox[0],
                           'miny': self.new_england_area_bbox[1],
                           'maxx': self.new_england_area_bbox[2],
                           'maxy': self.new_england_area_bbox[3]},
                "data_fs": {'xs': [],
                            'ys': [], },
                "data_snr": {'x': [],
                             'y': []},
                "wind": {'spd_kts': 0,
                         'dir_deg': 0},
                "mission_duration_min": 10,
            }
            
            map_reader.load_map_record(self, log, "")
        elif(self.Viz.map_name is not None):
            # We're given a map name, so just load that.
            log.info(" --- LOADING MAP: " + self.Viz.map_name)
            self.map_data_dict = self.load_map_record(self.Viz.map_name)
            self.bbox = (self.Viz.data.map_data_dict['bounds']['minx'][0],
                         self.Viz.data.map_data_dict['bounds']['miny'][0],
                         self.Viz.data.map_data_dict['bounds']['maxx'][0],
                         self.Viz.data.map_data_dict['bounds']['maxy'][0])
        else:
            log.error("Visualizer map name still None")

        # This is the difference between miny and maxy that the bound button will match to.
        # If bound maps are still too big, decrease this value.
        self.standard_window_lat = 0.003
        
        # # This is just for reference - not drawing this right now
        # usa_state_outlines = gpd.read_file(os.path.join(os.path.basename(os.path.dirname(inspect.getfile(
        #     lambda: None))), 'static/cb_2018_us_state_20m.zip'), bbox=self.new_england_area_bbox, crs="EPSG:4326")

        # # Convert data to geojson for bokeh
        # self.usa_states_outlines_geojson = GeoJSONDataSource(
        #     geojson=usa_state_outlines.to_json())
        
        # Waterbody data that we'll be checking against to see if the drone is over water
        self.waterbodies = gpd.read_file('data/waterbodies.geojson', bbox=self.new_england_area_bbox, crs="EPSG:4326")
        
        # This is how close in meters the drone needs to be in order to collect water/extinguish fire/see survivor
        self.radius_of_influence = (25 
                                    if self.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE 
                                    else 5) # in m
        
        # Prepopulate the polygons of interest and just modify this list as the mission progresses
        self.polygons_of_interest = []
        if self.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION:
            for i in range(0, len(self.map_data_dict["data_fs"]['xs'])):
                xs = self.map_data_dict["data_fs"]['xs'][i]
                ys = self.map_data_dict["data_fs"]['ys'][i]
                
                # Create polygons out of the data in the map file to enable operations with Shapely and RTree
                self.polygons_of_interest.append(Polygon(tuple(zip(xs, ys))))
                
                # Figure out the area of the ground covered by this set of fires.
                # This 100% of the score.
                self.starting_fire_area = 0
                for polygon in self.polygons_of_interest:
                    # Polygon x/y are in lat lon, so need the radius of earth to convert to meters
                    self.starting_fire_area = self.starting_fire_area + polygon.area*6370**2 
                
        else:
            merged_list = tuple(zip(self.map_data_dict["data_snr"]['x'], self.map_data_dict["data_snr"]['y'])) 
            for survivor in merged_list:
                # Transform the survivor points into survivor circles with radius 5 to make them intersectable
                self.polygons_of_interest.append(self.point_to_circle(survivor, 5))
        
        # Keep track of the number of survivors founds        
        self.survivors_found = 0
        
        # Maximum quantity of water the drone can hold
        self.water_limit = 100
        # Keep track of the current quantity of water
        self.water_quantity = 0
        # Time when first observed over water (-1 means that was most recently observed over land)
        self.water_start_time = -1
        
        # Time when last observed fire (-1 means haven't seen fire)
        self.fire_last_observed_time = -1

        # Where to find the waterbodies svg (can't use the self.waterbodies because Bokeh's incomplete
        # treatment of GeoJSON files)
        self.waterbodies_filepath = [os.path.join(os.path.basename(
            os.path.dirname(inspect.getfile(lambda: None))), 'static', 'waterbodies.svg')]
        
        # Where to find the ownship icon
        self.ownship_filepath = [os.path.join(os.path.basename(
            os.path.dirname(inspect.getfile(lambda: None))), 'static', 'Picture2.png')]
        
        
        ## Data sources
        # Container for information about ownship
        self.ownship_data_source = ColumnDataSource({
                'url': self.ownship_filepath,
                'lon': [0],
                'lat': [0],
                'w': [20],
                'h': [20],
                })
        # Container for wind data
        self.wind_table_source = ColumnDataSource({
                'spd_kts': [self.Viz.data.map_data_dict['wind']['spd_kts']],
                'dir_deg': [self.Viz.data.map_data_dict['wind']['dir_deg']]})
        # Container for window bounds information 
        self.bounds_table_source = ColumnDataSource({
                'minx': [self.Viz.data.map_data_dict['bounds']['minx']],
                'miny': [self.Viz.data.map_data_dict['bounds']['miny']],
                'maxx': [self.Viz.data.map_data_dict['bounds']['maxx']],
                'maxy': [self.Viz.data.map_data_dict['bounds']['maxy']]})
        # Container for mission statistics
        self.stats_table_source = ColumnDataSource({
                'elapsed_dur': [0],
                'remaining_dur': [0],
                'mission_stat': [0],
                'lon': [0],
                'lat': [0],
                'status': [0],
                'score': [0]})
        # Container for drone position
        self.drone_pos_data_source = ColumnDataSource({
                'lon': [0],
                'lat': [0]
                })
        # I don't know why, but the data sources need to be formatted differently loading a 
        # map from file as opposed to creating a new one. I think it has something to do
        # with how ColumnDataSource treats empty entries (they're not allowed).
        # The below just creates the data containers for the fires and survivors for the 3
        # different operating modes.
        if(self.Viz.mode == Mode.MAP_MAKER and self.Viz.map_name is None):
            self.survivors_table_source = ColumnDataSource({
                'x': [self.Viz.data.map_data_dict['data_snr']['x']],
                'y': [self.Viz.data.map_data_dict['data_snr']['y']]})
            self.fires_table_source = ColumnDataSource({
                'xs': [self.Viz.data.map_data_dict['data_fs']['xs']],
                'ys': [self.Viz.data.map_data_dict['data_fs']['ys']]})
        elif(self.Viz.mode == Mode.MAP_MAKER and self.Viz.map_name is not None):
            self.survivors_table_source = ColumnDataSource({
                'x': self.Viz.data.map_data_dict['data_snr']['x'],
                'y': self.Viz.data.map_data_dict['data_snr']['y']})
            self.fires_table_source = ColumnDataSource({
                'xs': self.Viz.data.map_data_dict['data_fs']['xs'],
                'ys': self.Viz.data.map_data_dict['data_fs']['ys']})
        else:
            self.survivors_table_source = ColumnDataSource({
                'x': self.Viz.data.map_data_dict['data_snr']['x'],
                'y': self.Viz.data.map_data_dict['data_snr']['y'],
                'color': ['orange']*len(self.Viz.data.map_data_dict['data_snr']['y']),
                'alpha': [0.0]*len(self.Viz.data.map_data_dict['data_snr']['y'])} 
                                                           if self.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE 
                                                           else {})
            self.fires_table_source = ColumnDataSource({
                'xs': self.Viz.data.map_data_dict['data_fs']['xs'],
                'ys': self.Viz.data.map_data_dict['data_fs']['ys'],
                'fill_color': ['red']*len(self.Viz.data.map_data_dict['data_fs']['ys']),
                'alpha': [1]*len(self.Viz.data.map_data_dict['data_fs']['ys'])} 
                                                       if self.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION 
                                                       else {})
        # Container for the radius circles (for debugging only)
        self.debug_radii_table_source = ColumnDataSource({
                'xs': [list(poly.exterior.coords.xy[0]) for poly in self.polygons_of_interest],
                'ys': [list(poly.exterior.coords.xy[1]) for poly in self.polygons_of_interest]})
        # Container for the drone table data (for debugging only)
        self.debug_drone_table_source = ColumnDataSource({
                'xs': [0],
                'ys': [0]})
        
        
        
    def save_map_record_as(self) -> None:
        """
        Saves the map record to file in the maps directory.
        """
        map_reader.save_map_record_as(self, log)

    def load_map_record(self, map_name: str) -> Dict:
        """
        Loads the given map from the maps directory.

        Parameters
        ----------
        map_name : str
            Name of the map to load (without extension).

        Returns
        -------
        Dict
            The data read from the map record file.
        """
        return map_reader.load_map_record(self, log, map_name)
        
    def bind_bbox(self) -> None:
        """
        Binds the window to a rectangle with the y dimension of
        standard latitude.
        
        If the bound window is too large for the mission, make
        the standard latitude smaller.
        """
        
        # Make sure we're working with flat lists
        minx = self.flatten(self.bounds_table_source.data['minx'])[0]
        miny = self.flatten(self.bounds_table_source.data['miny'])[0]
        maxx = self.flatten(self.bounds_table_source.data['maxx'])[0]
        maxy = self.flatten(self.bounds_table_source.data['maxy'])[0]
        
        # Find the center of the area we're working with.
        # This is the point we'll perform the operation about.
        centroid = [(minx + maxx) / 2,
                    (miny + maxy) / 2]
        
        # Figure out how much we need to shrink by.
        shrink_ratio = (1.0/float(math.fabs(maxy - miny)/self.standard_window_lat))
        
        # Find new extrema.
        #https://stackoverflow.com/questions/31125511/scale-polygons-by-a-ratio-using-only-a-list-of-their-vertices
        new_min_x = shrink_ratio * (minx - centroid[0]) + centroid[0]
        new_max_x = shrink_ratio * (maxx - centroid[0]) + centroid[0]
        new_min_y = shrink_ratio * (miny - centroid[1]) + centroid[1]
        new_max_y = shrink_ratio * (maxy - centroid[1]) + centroid[1]
        
        # Patch in the new extrema to the bounds table source so that the table updates
        self.bounds_table_source.patch({'minx': [(0, new_min_x)],
                                        'maxx': [(0, new_max_x)],
                                        'miny': [(0, new_min_y)],
                                        'maxy': [(0, new_max_y)]})
        # Prompt the table to update
        self.Viz.data_table.bounds_table.update()
        
        # Update the map window to change its bounds
        #https://stackoverflow.com/questions/42493049/bokeh-python-how-to-update-range-of-extra-axis
        self.plot.figure.x_range.start = new_min_x
        self.plot.figure.x_range.end = new_max_x
        self.plot.figure.y_range.start = new_min_y
        self.plot.figure.y_range.end = new_max_y

    def check_landing_status(self) -> None:
        """
        Checks if the queue filled by grpc has anything to process and patches the new information in.
        """
        
        try:
            if(not self.qLanding.empty()):
                log.info(" --- Updating landing status")
            # Don't block if the queue doesn't have anything, we have other things to do too.
            ln = self.qLanding.get(block=False)
            
            # If queue has some thing for us, patch the new data in.
            if(ln.isLanded):
                self.stats_table_source.patch({'status': [(0, "On the Ground")]})
        except Empty:
            pass
        
    def check_takeoff_status(self) -> None:
        """
        Checks if the queue filled by grpc has anything to process and patches the new information in.
        """
        
        try:
            if(not self.qTakeoff.empty()):
                log.info(" --- Updating takeoff status")
            # Don't block if the queue doesn't have anything, we have other things to do too.
            tn = self.qTakeoff.get(block=False)
            
            # If queue has some thing for us and we're ready for it, patch the new data in.
            if(tn.isTakenOff and self.start_time == -1):
                self.start_time = tn.px4Time/1000.0
                self.stats_table_source.patch({'status': [(0, "Taking Off")]})
        except Empty:
            pass
        
    def update_local_location(self) -> None:
        """
        Checks if the queue filled by grpc has anything to process and patches the new information in.
        """
        
        try:
            if(not self.qLocation.empty()):
                # log.info(" --- Updating local location")
                # Don't spam the console
                pass
            # Don't block if the queue doesn't have anything, we have other things to do too.
            loc = self.qLocation.get(block=False)
            
            # If queue has some thing for us, patch the new data in.
            # Dealing with moderately disparate orders of magnitude, so lose precision when doing all in one go
            elapsed_duration = loc.px4Time/1000.0 - self.start_time
            
            # Update the mission statistics table
            self.stats_table_source.patch({'elapsed_dur': [(0, math.floor(elapsed_duration))],
                                           'remaining_dur': [(0, math.floor(self.map_data_dict['mission_duration_min'] * 60.0 - elapsed_duration))],
                                           'lon': [(0, loc.longitude)],
                                           'lat': [(0, loc.latitude)],
                                           'status': [(0, "In Air")]})
            # Update the location of the ownship
            self.ownship_data_source.patch({'lon': [(0, loc.longitude)],
                                            'lat': [(0, loc.latitude)],
                                           })
            
            # Update the location of the ownship
            if(self.drone_pos_data_source.data['lat'][0] == 0):
                self.drone_pos_data_source.data = {
                    'lon': [loc.longitude],
                    'lat': [loc.latitude]
                }
            else:
                # If this isn't the first location we've received, want to make sure we're maintaining a flat list
                new_lat = self.flatten([self.drone_pos_data_source.data['lat'], loc.latitude])
                new_lon = self.flatten([self.drone_pos_data_source.data['lon'], loc.longitude])
                self.drone_pos_data_source.data = {
                    'lon': new_lon,
                    'lat': new_lat
                }
            # log.info([self.drone_pos_data_source.data['lon'][-1], self.drone_pos_data_source.data['lat'][-1]])
            
            # See if there are any interesting intersections
            drone_circle = self.point_to_circle((loc.longitude, loc.latitude), self.radius_of_influence)
            if self.map_data_dict["map_type"] == MapType.FIRE_SUPPRESSION:
                self.fire_suppression_intersections(drone_circle, loc.px4Time)
            else:
                self.snr_intersections(drone_circle)
                
            # Patch the drone extents we're doing math with (for debugging only)
            self.debug_drone_table_source.patch({'xs': [(0, list(drone_circle.exterior.coords.xy[0]))],
                                                'ys': [(0, list(drone_circle.exterior.coords.xy[1]))]})           
            
        except Empty:
            pass
        
    def flatten(self, x: list) -> list:
        """
        Turns a list of lists of lists... into a flat list of 1 dimension.

        Parameters
        ----------
        x : list
            The list to flatten.

        Returns
        -------
        list
            The flattened list.
        """
        
        # Flatten until the list is no longer iterable
        #https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
        if isinstance(x, collections.Iterable):
            return [a for i in x for a in self.flatten(i)]
        else:
            return [x]
    
    def point_to_circle(self, point_coord: tuple, radius: float) -> Polygon:
        """
        Draws a polygon circle around a point.

        This gives the point a perimeter that can be intersected with.

        Parameters
        ----------
        point_coord : tuple
            The point which should be the center of the circle.
        radius : float
            The radius to use for the circle.

        Returns
        -------
        Polygon
            Circle with center at the given point and with the given radius.
        """
        
        # I don't 100% know how this works, but it clearly does...
        # https://gis.stackexchange.com/questions/367496/plot-a-circle-with-a-given-radius-around-points-on-map-using-python
        lon, lat = point_coord

        # Create some projections in other coordinate systems for ourselves.
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

        # Convert to a convenient coordinate system for the math and convert back when we're done.
        center = Point(float(lon), float(lat))
        point_transformed = transform(wgs84_to_aeqd, center)
        buffer = point_transformed.buffer(radius)
        polygon = transform(aeqd_to_wgs84, buffer)
        # Get the polygon with lat lon coordinates
        return polygon
    
    def fire_suppression_intersections(self, drone_circle: Polygon, time_location_observed: int) -> None:
        """
        Checks if the drone is over fire/water, updates the fire display, and does the fire/water scoring.

        Parameters
        ----------
        drone_circle : Polygon
            The circle representing the area of influence of the drone.
        time_location_observed : int
            The time when the given location was observed.
        """
        
        #### Fire
        # Get which polygons of interest the drone intersects with (couple be multiple)
        object_indeces = self.check_drone_location_against_object_of_interest(drone_circle, self.polygons_of_interest)
        
        # Need to calculate what the fire area will be after this for scoring
        fire_area_now = 0
        
        # If we're intersecting with fires and we have water, do some firefighting
        if(len(object_indeces) > 0 and self.water_quantity > 0):
            # If we didn't come from a fire, make sure to record when we first started fighting
            if(self.fire_last_observed_time == -1):
                self.fire_last_observed_time = time_location_observed
                
            for idx in object_indeces:
                # Make sure the fire fighting isn't over-powered
                polygon_reduction_factor = 0.05
                if(self.water_quantity > ((time_location_observed - self.fire_last_observed_time)/1000.0) * 10.0):
                    # If we have more water than we can deposit in this time segment, shrink by maximum for the time
                    # and recalculate our water reserves
                    self.polygons_of_interest[idx] = self.shrink_shapely_polygon(self.polygons_of_interest[idx], 
                                                                                 polygon_reduction_factor * ((time_location_observed - self.fire_last_observed_time)/1000.0))
                
                    self.water_quantity -= ((time_location_observed - self.fire_last_observed_time)/1000.0) * 10.0
                else:
                    # If this is the last of our water, use up all of the water and calculate how much that would shrink the fire by
                    factor = self.water_quantity / ( ((time_location_observed - self.fire_last_observed_time)/1000.0) * 10.0 ) * polygon_reduction_factor
                    self.polygons_of_interest[idx] = self.shrink_shapely_polygon(self.polygons_of_interest[idx], 
                                                                                 factor)
                    self.water_quantity = 0
                    
                if(self.polygons_of_interest[idx].is_empty):
                    # If a fire has been fully extinguished, make sure to patch that into the data table.
                    self.fires_table_source.patch({ 'xs': [(idx, [0])],
                                                    'ys': [(idx, [0])]})
                else:
                    # If a fire is still around after this, update the perimeter points
                    self.fires_table_source.patch({ 'xs': [(idx, list(self.polygons_of_interest[idx].exterior.coords.xy[0]))],
                                                    'ys': [(idx, list(self.polygons_of_interest[idx].exterior.coords.xy[1]))]})
            
            # Note the time we were last over fire
            self.fire_last_observed_time = time_location_observed
            
        else:
            # Didn't see fire, so clear the last time
            self.fire_last_observed_time = -1
            
        # Recalculate the fire area for scoring
        for poly in self.polygons_of_interest:
            fire_area_now += poly.area*6370**2 
        
        #### Water
        # left sjoin on position in order to check if the points are in the waterbodies
        # https://gis.stackexchange.com/questions/208546/check-if-a-point-falls-within-a-multipolygon-with-python
        # Solution 4
        # Massage the drone perimeter data into the right data frame
        points_world = gpd.GeoDataFrame({'notes': ['drone'], 'geometry': [
            drone_circle
            ]}, crs="EPSG:4326")

        # Get which points are in water
        pointInWaterbodies = gpd.sjoin(points_world, self.waterbodies, how='left')
        groupedInWaterbodies = pointInWaterbodies.groupby('index_right')
        
        if(len(groupedInWaterbodies.groups) > 0):
            # Figure out how much water we picked if any of our points of influence are over water
            if(self.water_start_time == -1):
                # Note when we started collecting water
                self.water_start_time = time_location_observed
            self.water_quantity = (time_location_observed - self.water_start_time)/1000 * 10  # 10 gallons/sec
            # Make sure we don't take on more water than we can carry
            self.water_quantity = (self.water_limit 
                                   if self.water_quantity > self.water_limit 
                                   else self.water_quantity)
            # Patch in our current water quantity
            self.stats_table_source.patch({'mission_stat': [(0, self.water_quantity)]})
        else:
            # Reset water observation time if didn't see water
            self.water_start_time = -1
        
        # Patch in the score and the mission statistics
        self.stats_table_source.patch({'score': [(0, 100.0 - (fire_area_now/float(self.starting_fire_area) * 100.0))]})
        self.stats_table_source.patch({'mission_stat': [(0, self.water_quantity)]})
    
    def snr_intersections(self, drone_circle: Polygon) -> None:
        """
        Checks if the drone can "see" any of the survivors.

        Does the intersections and scoring.

        Parameters
        ----------
        drone_circle : Polygon
            Polygon representing the area of influence of the drone.
        """
        
        # Get the indeces of survivors that intersect with the drone (could be multiple)
        object_indeces = self.check_drone_location_against_object_of_interest(drone_circle, self.polygons_of_interest)
        for idx in object_indeces:
            if self.survivors_table_source.data['alpha'][idx] == 0:
                # Make sure to only count the found survivors once (using their visibility as the marked)
                self.survivors_found = self.survivors_found + 1
                # Since this survivor hasn't already been marked, that means we're finding the person for the first time, so
                # mark them. This way we won't pay attention to them further.
                self.survivors_table_source.patch({'alpha': [(idx, 1)]});
            
        # Patch in the score and the mission statistics
        self.stats_table_source.patch({'mission_stat': [(0, self.survivors_found/float(len(self.map_data_dict["data_snr"]['x']))*100.0)]})
        self.stats_table_source.patch({'score': [(0, self.survivors_found)]})

    def check_drone_location_against_object_of_interest(self, drone_circle: Polygon, objects: list) -> list:
        """
        Checks if the drone location intersects with any of the given polygons.

        Parameters
        ----------
        drone_circle : Polygon
            The drone's area of influence.
        objects : list
            The list of Polygons that represent the objects of interest and what to compare the drone's location to.

        Returns
        -------
        list
            The list of indeces of objects of interest that intersect with the drone's area of influence.
        """
        # https://stackoverflow.com/questions/14697442/faster-way-of-polygon-intersection-with-shapely/1404366
        # Create R-tree
        idx = index.Index()
        # Populate R-tree index with bounds of objects of interest (ooi)
        for pos, ooi in enumerate(objects):
            # assuming ooi is a shapely object
            idx.insert(pos, ooi.bounds)
        
        # Collect the indeces of all intersecting objects
        object_indeces = []
        for pos in idx.intersection(drone_circle.bounds):
            object_indeces.append(pos)
        
        return object_indeces
    
    def shrink_shapely_polygon(self, my_polygon: Polygon, factor: float=0.10) -> Polygon:
        
        """
        Changes the size of the given polygon by the given factor (bigger or smaller).

        Parameters
        ----------
        my_polygon : Polygon
            The polygon whose size to change.
        factor : float, optional
            The factor by which to change the size fo the polygon, by default 0.10.

        Returns
        -------
        Polygon
            The polygon with the amended size.
        """
        # https://stackoverflow.com/a/67205583
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
    
