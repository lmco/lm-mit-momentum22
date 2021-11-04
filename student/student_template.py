from student_base import student_base
import time
import asyncio

class student_flight_controller(student_base):
	
	async def student_main(self, drone):
		
		# The parameter 'drone' is an instance of a MavSDK Drone object, with communication happening in the background.
		# You can query it for things like position.
		
		print("Checking the drone's position")
		
		async for position in drone.telemetry.position():
			print(position)
			break
							
		# You can also use it to send commands to the drone:
		
		print("To the sky!")
		
		await drone.action.arm()
		await drone.action.takeoff()
		
		# This is the command to delay by some amount of time
		
		print("Waiting 10 seconds")
		
		await asyncio.sleep(10)
		
		# Here we trigger a landing, and then wait for it to be complete
		
		print("Landing")
		
		await drone.action.land()
		
		async for in_air_now in drone.telemetry.in_air():
			if not in_air_now:
				break
			else:
				print("Still landing")
			
		print("Finished")


		
# This bit on code causes the flight controller to run when this file is executed.
		
if __name__ == "__main__":
	fcs = student_flight_controller()
	fcs.run()
