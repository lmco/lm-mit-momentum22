from itertools import count
from xmlrpc.client import MAXINT
from student_base import student_base
import time
import numpy
from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Point
import random


class my_flight_controller(student_base):
	"""
	Student flight controller class.

	Students develop their code in this class.

	Parameters
	----------
	student_base : student_base
			Class defining functionality enabling base functionality

	Methods
	-------
	student_run(self, telemetry: Dict, commands: Dict (optional))
			Method that takes in telemetry and issues drone commands.
	"""
	def get_closest_fire(self, telemetry):
		own_lat = telemetry['latitude']
		own_lon = telemetry['longitude']
		points = []
		for poly in telemetry['fire_polygons']:
			if not poly.is_empty:
				points.append(self.get_random_point_in_polygon(poly))

		min_dist = MAXINT
		count = 0
		for centroid in points:
			# print(str(count) + ". " + centroid.wkt)
			count = count + 1
			centroid_dist = self.dist(own_lat, own_lon, centroid.y, centroid.x)
			if (min_dist > centroid_dist):
				min_centroid = centroid
				min_dist = centroid_dist
		# print("min: " + min_centroid.wkt)

		return min_centroid

	def get_random_point_in_polygon(self, poly):
		#https://gis.stackexchange.com/questions/6412/generate-points-that-lie-inside-polygon
		if (poly.contains(poly.centroid)):
			return poly.centroid
		else:
			minx, miny, maxx, maxy = poly.bounds
			while True:
				p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
				if poly.contains(p):
					return p

	def dist(self, lat1, long1, lat2, long2):
		"""
		Calculate the great circle distance between two points 
		on the earth (specified in decimal degrees)
		"""
		# convert decimal degrees to radians
		lat1, long1, lat2, long2 = map(
			radians, [lat1, long1, lat2, long2])
		# haversine formula
		dlon = long2 - long1
		dlat = lat2 - lat1
		a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a))
		# Radius of earth in kilometers is 6371
		km = 6371 * c
		return km

	def get_fire_area(self, telemetry):
		area = 0
		for poly in telemetry['fire_polygons']:
			area = area + (0 if poly.is_empty else area + poly.area*6370**2)
		return area

	def student_run(self, telemetry, commands):

		# The telemetry dictionary contains fields that describe the drone's position and flight state.
		# It updates continuously, so it can be polled for new information.
		# Use a time.sleep() between polls to keep the CPU load down and give the background communications
		# a chance to run.

		print("Printing telemetry")
		for i in range(4):
			print(telemetry)
			time.sleep(0.5)
   
		print("Arming")
		self.arm()
  
		print("Taking off")
		self.takeoff()

		print("Waiting 6 seconds")
		time.sleep(6)
  
		while(self.get_fire_area(telemetry) > 0):
			print("Getting closest fire")
			fire = self.get_closest_fire(telemetry)
			self.goto(fire.y, fire.x, 8)
			err = numpy.linalg.norm(
				[fire.y - telemetry['latitude'], fire.x - telemetry['longitude']])
			tol = 0.00001
			while err > tol:
				print('Aircraft is enroute to fire')
				time.sleep(0.5)
				err = numpy.linalg.norm(
					[fire.y - telemetry['latitude'], fire.x - telemetry['longitude']])
    
			last_area = self.get_fire_area(telemetry)
			while True:
				if(last_area - self.get_fire_area(telemetry) < 0.05):
					print('Done with fire')
					break
				else:
					time.sleep(2)
					print('Aircraft is at fire')
					last_area = self.get_fire_area(telemetry)
		
		print("Landing")
		self.land()
		
		while telemetry['in_air']:
			time.sleep(0.1)
   
		print("Landed")


if __name__ == "__main__":
	fcs = my_flight_controller()
	fcs.run()
