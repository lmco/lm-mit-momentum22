##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################


## This is based on the Boston missions

import sys
sys.path.append('Visualizer/')

import time

import grpc

import viz_pb2 as viz_connect
import viz_pb2_grpc as viz_connect_grpc

import threading, queue

qLanding = queue.Queue()
qTakeoff = queue.Queue()
qLocation = queue.Queue()

channel = grpc.insecure_channel('localhost:51052')
stub = viz_connect_grpc.Momentum22VizStub(channel)

def mavsdkBlock():
    """
    Simulate doing mavsdk things
    """
    print("sleep commence")
    time.sleep(1)
    print("sleep done")

def worker():
    """
    Process the queue of incoming grpc messages to send out
    """
    while True:
        try:
            if(not qTakeoff.empty()):
                item = qTakeoff.get()
                print(f'Working on {item}')
                ack2 = stub.SetTakeoffStatus(item)
                print(ack2)
                qTakeoff.task_done()
        except queue.Empty:
            pass
        
        try:
            if(not qLocation.empty()):
                item = qLocation.get()
                print(f'Working on {item}')
                ack3 = stub.SetDroneLocation(item)
                print(ack3)
                qLocation.task_done()
        except queue.Empty:
            pass
        
        try:
            if(not qLanding.empty()):
                item = qLanding.get()
                print(f'Working on {item}')
                ack1 = stub.SetLandingStatus(item)
                print(ack1)
                qLanding.task_done()
        except queue.Empty:
            pass
        
# Start the queue thread
threading.Thread(target=worker, daemon=True).start()

start_time = time.time()


survivor_lons = [
            -71.00560345562178,
            -70.99401256062542,
            -70.98550669471554,
            -70.9827742403818,
            -70.98969351990434,
            -70.98374382095183,
            -70.99330741111994
        ]
survivor_lats = [
            42.356241403108065,
            42.35754262671063,
            42.35689201490935,
            42.360487501179605,
            42.362233880225155,
            42.36439117198731,
            42.36459662834561
        ]

time_steps = len(survivor_lons) + 2
# time_steps = 6

for item in range(time_steps):
    print(item)
    # Simulate doing mavsdk tasks
    # mavsdkBlock()
    
    curr_time = int((time.time()-start_time)*1000) #! NOTE: milliseconds
    if(item == 0):
        print("takeoff")
        tn = viz_connect.TakeoffNotification(msgId=item + 1, isTakenOff=True, px4Time=(curr_time))
        qTakeoff.put(tn)
    elif(item == time_steps - 1):
        print("landing")
        ln = viz_connect.LandingNotification(msgId=item + 1, isLanded=True, px4Time=(curr_time))
        qLanding.put(ln)
    # elif(item == 1):
    #     print("water location")
    #     loc = viz_connect.Location(msgId=item + 1, latitude=(42.36562763876802), longitude=(-70.99973019252967), px4Time=(curr_time))
    #     qLocation.put(loc)
    # elif(item == 2):
    #     print("water2 location")
    #     loc = viz_connect.Location(msgId=item + 1, latitude=(42.36562763876802), longitude=(-70.99973019252967), px4Time=(curr_time))
    #     qLocation.put(loc)
    # elif(item == 3):
    #     print("fire location")
    #     loc = viz_connect.Location(msgId=item + 1, latitude=(42.36597704345451), longitude=(-71.0087424915964), px4Time=(curr_time))
    #     qLocation.put(loc)
    # elif(item == 4):
    #     print("fire2 location")
    #     loc = viz_connect.Location(msgId=item + 1, latitude=(42.36597704345451), longitude=(-71.0087424915964), px4Time=(curr_time))
    #     qLocation.put(loc)
    else:
        print("location")
        loc = viz_connect.Location(msgId=item + 1, latitude=(survivor_lats[item - 1]), longitude=(survivor_lons[item - 1]), px4Time=(curr_time))        
        qLocation.put(loc)
    
    # Queue up things to send
    time.sleep(2)
    
    
    
print('All task requests sent\n', end='')

# Block until all tasks are done
qLanding.join()
qTakeoff.join()
qLocation.join()
print('All work completed')