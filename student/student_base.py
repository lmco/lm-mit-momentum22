##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

# Student flight control base class
#
# This class does the following:
# - receives aircraft data from MavLink
# - forwards that data directly to the Visualization system for display
# - also forwards that data to the student's derived class
# - defines methods that the student's derived class can call to tell the drone to do things
#
# The vizualization communications, Mavlink communications, and student code are all in seperate threads.

# TODO: Store PX4 Time is self.px4Time

import sys
sys.path.append('Visualizer/')

import time
import grpc
import viz_pb2 as viz_connect
import viz_pb2_grpc as viz_connect_grpc
import threading
import mavsdk
import asyncio
import navpy

class student_base:

	def __init__(self):
		self.channel = grpc.insecure_channel('localhost:51052')
		self.stub = viz_connect_grpc.Momentum22VizStub(self.channel)
		self.px4Time = 0
		self.msgId = 0
		self.in_air_lp = False
		self.home_alt = 0
		
		self.telemetry = {}
		self.telemetry['altitude'] = 0
		self.telemetry['latitude'] = 0
		self.telemetry['longitude'] = 0
		self.telemetry['in_air'] = False

		self.commands = {}
		self.commands['arm'] = False
		self.commands['takeoff'] = False
		self.commands['land'] = False
		self.commands['disarm'] = False
		self.commands['goto'] = False
		
		self.mav_shutdown = False
		self.viz_stopping = False
		self.viz_thread = None
		self.student_thread = None

	######### Interface for the Viz Thread ###########
				
	def viz_thread_start(self):
		self.viz_thread = threading.Thread(target=self.viz_thread_main, args=(self,))
		self.viz_thread.start();
		
	def viz_thread_stop(self):
		self.viz_stopping = True
		self.viz_thread.join()
		
	######### Implementation for the Viz Thread ###########
	
	def viz_thread_main(self, args):
		while not self.viz_stopping:
			self.viz_send_updates()
			time.sleep(0.1)
					
	def viz_send_updates(self):
		self.px4Time = int(time.time()*1000.0)
		self.viz_send_location(self.telemetry['latitude'], self.telemetry['longitude'])
		self.viz_send_ground_state(self.telemetry['in_air'])
		self.new_data_set = False
						
	def viz_send_location(self, latitude, longitude):
		loc = viz_connect.Location(msgId=self.msgId, latitude=latitude, longitude=longitude, px4Time=self.px4Time)
		self.msgId += 1
		ack = self.stub.SetDroneLocation(loc)

	def viz_send_ground_state(self, in_air):
		if in_air != self.in_air_lp:
			self.in_air_lp = in_air
			if in_air:
				tn = viz_connect.TakeoffNotification(msgId=self.msgId, isTakenOff=True, px4Time=self.px4Time)
				ack = self.stub.SetTakeoffStatus(tn)
			if not in_air:
				ln = viz_connect.LandingNotification(msgId=self.msgId, isLanded=True, px4Time=self.px4Time)
				ack = self.stub.SetLandingStatus(ln)
			self.msgId += 1

	######### MAV Interface ###########
	
	def mav_run(self):
		asyncio.ensure_future(self.mav_start())
		asyncio.get_event_loop().run_forever()
		
	async def mav_start(self):
		self.drone = mavsdk.System()
		await self.drone.connect()
		asyncio.ensure_future(self.mav_in_air(self.drone))
		asyncio.ensure_future(self.mav_position(self.drone))
		asyncio.ensure_future(self.mav_shutdown_watcher())
		asyncio.ensure_future(self.mav_command_watcher(self.drone))
		
	def mav_thread_stop(self):
		self.mav_shutdown = True
		
	async def mav_shutdown_watcher(self):
		while not self.mav_shutdown:
			await asyncio.sleep(0.1)
		asyncio.get_event_loop().stop()
		
	async def mav_in_air(self, drone):
		async for in_air in drone.telemetry.in_air():
			self.telemetry['in_air'] = in_air
			
	async def mav_position(self, drone):
		async for position in drone.telemetry.position():
			self.telemetry['latitude'] = position.latitude_deg
			self.telemetry['longitude'] = position.longitude_deg
			self.telemetry['altitude'] = position.relative_altitude_m
			self.home_alt = position.absolute_altitude_m - position.relative_altitude_m
	
	async def mav_command_watcher(self, drone):
		while not self.mav_shutdown:
			if self.commands['arm']:
				await drone.action.arm()
				self.commands['arm'] = False
			if self.commands['disarm']:
				await drone.action.disarm()
				self.commands['disarm'] = False
			if self.commands['takeoff']:
				await drone.action.takeoff()
				self.commands['takeoff'] = False
			if self.commands['land']:
				await drone.action.land()
				self.commands['land'] = False
			if self.commands['goto']:
				lat, lon, alt = self.commands['goto']
				await drone.action.goto_location(lat, lon, alt + self.home_alt, 0)
				self.commands['goto'] = False
			await asyncio.sleep(0.01)
			
	########## Student Thread Interface ############
	
	def student_thread_start(self):
		self.student_thread = threading.Thread(target=self.student_thread_main, args=(self,))
		self.student_thread.start();
		
	def student_thread_wait_for_stop(self):
		self.student_thread.join()

	def student_thread_main(self, args):
		time.sleep(1)
		self.student_run(self.telemetry, self.commands)
		self.mav_thread_stop()
		
	def student_run(self, telemetry):
		print("Override this method in your class!")
		
	############# Student Commands ###############
	
	def arm(self):
		self.commands['arm'] = True
		while self.commands['arm']:
			time.sleep(0.01)
			
	def disarm(self):
		self.commands['disarm'] = True
		while self.commands['disarm']:
			time.sleep(0.01)
			
	def takeoff(self):
		self.commands['takeoff'] = True
		while self.commands['takeoff']:
			time.sleep(0.01)
		
	def land(self):
		self.commands['land'] = True
		while self.commands['land']:
			time.sleep(0.01)
		
	def goto(self, lat, lon, alt):
		self.commands['goto'] = (lat, lon, alt)
		while self.commands['goto']:
			time.sleep(0.01)
			
	########## Main ############
	
	def run(self):
		self.viz_thread_start()
		self.student_thread_start()
		self.mav_run()
		self.student_thread_wait_for_stop()
		self.viz_thread_stop()
	
	
			
if __name__ == "__main__":
	print("This script can't be run directly.  Create a class that inherits student_base, and run that instead.")

