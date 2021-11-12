from student_base import student_base
import time
import numpy

class my_flight_controller(student_base):
	
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
		
		# First Survivor
		print("Goto first survivor")
		goalLat = 42.35754262671063 # first survivor
		goalLon = -70.99401256062542
		goalAlt = 100 
		self.goto(goalLat, goalLon, goalAlt)
		err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])
		tol = 0.0001 # Approximately 50 feet tolerance
		while err > tol:
			print('Aircraft is enroute to first survivor')
			time.sleep(10)
			err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])

		# Second survivor
		print("Goto second survivor")
		goalLat = 42.362233880225155 # second survivor
		goalLon = -70.98969351990434
		goalAlt = 100 
		self.goto(goalLat, goalLon, goalAlt)
		err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])
		tol = 0.0001 # Approximately 50 feet tolerance
		while err > tol:
			print('Aircraft is enroute second survivor')
			time.sleep(10)
			err = numpy.linalg.norm([goalLat - telemetry['latitude'], goalLon - telemetry['longitude']])
			
		# Home
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
