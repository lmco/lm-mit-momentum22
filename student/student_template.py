from student_base import student_base
import time
import numpy

class my_flight_controller(student_base):
	
	def student_run(self, telemetry, commands):
		# Student code goes in this method.
		# See student_example.py for ideas on
		# how to fill out this method to complete the challenge.
		pass
		
		
# This bit of code just makes it so that this class actually runs when executed from the command line,
# rather than just being silently defined.

if __name__ == "__main__":
	fcs = my_flight_controller()
	fcs.run()
