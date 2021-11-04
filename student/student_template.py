from student_base import student_base
import time

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
		self.takeoff()
		
		print("Waiting 6 seconds")
		time.sleep(6)
		
		print("Goto somewhere else")
		self.goto(telemetry['latitude'], telemetry['longitude'] - 0.00005, 0.5)
		
		print("Waiting 10 seconds")
		time.sleep(10)
		
		print("Landing")
		self.land()
		
		while telemetry['in_air']:
			time.sleep(0.1)
			
		print("Landed")
		
		
# This bit of code just makes it so that this class actually runs when executed from the command line,
# rather than just being silently defined.

if __name__ == "__main__":
	fcs = my_flight_controller()
	fcs.run()
