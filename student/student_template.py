from student_base import student_base
import time
import numpy
from typing import Dict

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
	
	def student_run(self, telemetry: Dict, commands: Dict) -> None:
		"""
		Defines drone behavior with respect to time given the telemetry.

		Students develop their based code in this method (you may develop)
		your own methods and classes in addition to this).

		Parameters
		----------
		telemetry : Dict
			Telemetry coming from the simulated drone.
		commands : Dict
			Issue basic commands via this dictionary (you use the method in 
   			the example missions).
		"""
  
		# Student code goes in this method.
		# See student_fire_example_boston.py and 
  		# student_SAR_example_boston.py for ideas on
		# how to fill out this method to complete the challenge.
		pass
		
		
# This bit of code just makes it so that this class actually runs when executed from the command line,
# rather than just being silently defined.

if __name__ == "__main__":
	fcs = my_flight_controller()
	fcs.run()
