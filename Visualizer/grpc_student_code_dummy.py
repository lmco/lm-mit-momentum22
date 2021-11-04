##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

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
time_steps = 10

for item in range(time_steps):
    print(item)
    # Simulate doing mavsdk tasks
    # mavsdkBlock()
    
    curr_time = int((time.time()-start_time)*1000) #! NOTE: milliseconds
    # Queue up things to send
    time.sleep(1)
    if(item == 0):
        print("takeoff")
        tn = viz_connect.TakeoffNotification(msgId=item + 1, isTakenOff=True, px4Time=(curr_time))
        qTakeoff.put(tn)
    elif(item == time_steps - 1):
        print("landing")
        ln = viz_connect.LandingNotification(msgId=item + 1, isLanded=True, px4Time=(curr_time))
        qLanding.put(ln)
    else:
        print("location")
        loc = viz_connect.Location(msgId=item + 1, longitude=(41.123456 + item*1), latitude=(-82.123456 + item*1), px4Time=(curr_time))
        qLocation.put(loc)
    
    
    
print('All task requests sent\n', end='')

# Block until all tasks are done
qLanding.join()
qTakeoff.join()
qLocation.join()
print('All work completed')