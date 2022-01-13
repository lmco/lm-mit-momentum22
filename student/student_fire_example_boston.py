from student_base import student_base
import time
import numpy

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

	def student_run(self, telemetry, commands):
		
		# The telemetry dictionary contains fields that describe the drone's position and flight state.
		# It updates continuously, so it can be polled for new information.
		# Use a time.sleep() between polls to keep the CPU load down and give the background communications
		# a chance to run.
		
		print("Printing telemetry")
		for i in range(4):
			print(telemetry)
			time.sleep(0.5)
			
		# Several commands are available to control the drone:
		# 
		# self.arm()
		# self.disarm()
		# self.takeoff()
		# self.land()
		# self.goto(lat, lon, alt)
		#
		# Note that the commands return immediately, not when the drone
		# has actually reached the specified condition.
		
		print("Arming")
		self.arm()
		
		print("Taking off")
		homeLat = telemetry['latitude']
		homeLon = telemetry['longitude']
		self.takeoff()
		
		print("Waiting 6 seconds")
		time.sleep(6)
		
		# Get Water
		print("Get to water")
		goalLat = 42.3608 # water
		goalLon = -70.9904
		goalAlt = 100 
		self.goto(goalLat, goalLon, goalAlt)
		err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])
		tol = 0.0001 # Approximately 50 feet tolerance
		while err > tol:
			print('Aircraft is enroute to water')
			time.sleep(10)
			err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])


		print("Picking up water")
		water_start_time = time.time()
		while(time.time() - water_start_time < 10.0):
			print("Water level: " + str(round(telemetry['water_pct_remaining'], 2)) + '%')
			time.sleep(5)
		print("Water level: " + str(round(telemetry['water_pct_remaining'], 2)) + '%')

		# fire
		print("Go to fire")
		goalLat = 42.36045 # fire
		goalLon = -70.99165
		goalAlt = 100 
		self.goto(goalLat, goalLon, goalAlt)
		err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])
		tol = 0.0001 # Approximately 50 feet tolerance
		while err > tol:
			print('Aircraft is enroute to fire')
			time.sleep(10)
			err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])
			
		# Home

		print("Putting out fire")
		water_start_time = time.time()
		while(time.time() - water_start_time < 10.0):
			time.sleep(5)
			print("Fire remaining: " + str(round(telemetry['fires_pct_remaining'], 2)) + '%')
   
			# print("Fire polygons")
			# for poly in self.telemetry['fire_polygons']:
			# 	print(poly.wkt)
		print("Fire remaining: " + str(round(telemetry['fires_pct_remaining'], 2)) + '%')

		print("Returning to Base")
		goalLat = homeLat # Home
		goalLon = homeLon
		goalAlt = 100 
		self.goto(goalLat, goalLon, goalAlt)
		err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])
		tol = 0.00001 # Approximately 5 feet tolerance
		while err > tol:
			print('Aircraft is enroute; returning to base')
			time.sleep(10)
			err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])
		
		print("Landing")
		self.land()
		
		while telemetry['in_air']:
			time.sleep(0.1)
			
		print("Landed")
		while True:
			lat = telemetry['latitude']
			lon = telemetry['longitude']
			print(f'Latitude: {lat}, Longitude: {lon}')
			time.sleep(1)
		
		
# This bit of code just makes it so that this class actually runs when executed from the command line,
# rather than just being silently defined.

if __name__ == "__main__":
	fcs = my_flight_controller()
	fcs.run()
