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
sys.path.append('../Visualizer/')

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
        self.in_air_lp = 0
        self.new_data_set = False
        self.new_latitude = 0
        self.new_longitude = 0
        self.new_in_air = False
        self.viz_stopping = False
        self.viz_thread = None
        self.student_stopping = False
        self.student_thread = None

    ######### Interface for the Viz Thread ###########
                
    def viz_thread_start(self):
        self.viz_thread = threading.Thread(target=self.viz_thread_main, args=(self,))
        self.viz_thread.start();
        
    def viz_thread_stop(self):
        self.viz_stopping = True
        self.viz_thread.join()
        
    def viz_set_position(self, latitude, longitude):
        if latitude != self.new_latitude or longitude != self.new_longitude:
            self.new_latitude = latitude
            self.new_longitude = longitude
            self.new_data_set = True

    def viz_set_in_air(self, in_air):
        if in_air != self.new_in_air:
            self.new_in_air = in_air
            self.new_data_set = True

    ######### Implementation for the Viz Thread ###########
    
    def viz_thread_main(self, args):
        while not self.viz_stopping:
            self.viz_send_updates()
            time.sleep(0.01)
                    
    def viz_send_updates(self):
        if self.new_data_set:
            self.viz_send_location(self.new_latitude, self.new_longitude)
            self.viz_send_ground_state(self.new_in_air)
            self.new_data_set = False
                        
    def viz_send_location(self, latitude, longitude):
        loc = viz_connect.Location(msgId=self.msgId, latitude = latitude, longitude = longitude, px4Time = self.px4Time)
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
        
    async def mav_in_air(self, drone):
        async for in_air in drone.telemetry.in_air():
            self.viz_set_in_air(in_air)
            
    async def mav_position(self, drone):
        async for position in drone.telemetry.position():
            self.viz_set_position(position.latitude_deg, position.longitude_deg)
    
    ########## Student Thread Interface ############
    
    def student_thread_start(self):
        self.student_thread = threading.Thread(target=self.student_thread_main, args=(self,))
        self.student_thread.start();
        
    def student_thread_stop(self):
        self.student_stopping = True
        self.student_thread.join()

    def student_thread_main(self, args):
        while not self.viz_stopping:
            self.student_run(self.new_latitude, self.new_longitude, self.new_in_air)
            time.sleep(0.2)
   
    def student_run(self, latitude, longitude, in_air):
        print("Override this method in your class!")
        print(latitude, longitude, in_air)
        
    ########## Main ############
    
    def run(self):
        self.viz_thread_start()
        self.student_thread_start()
        self.mav_run()
    
    
            
if __name__ == "__main__":
    #print("This script can't be run directly.  Create a class that inherits student_base, and run that instead.")
    x = student_base()
    x.run()
