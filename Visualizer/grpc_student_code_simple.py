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
    print("sleep commence")
    time.sleep(1)
    print("sleep done")

def worker():
    while True:
        item = qLanding.get()
        print(f'Working on {item}')
        ack1 = stub.SetLandingStatus(item)
        print(ack1)
        print(f'Finished {item}')
        qLanding.task_done()
        
        item = qTakeoff.get()
        print(f'Working on {item}')
        ack2 = stub.SetTakeoffStatus(item)
        print(ack2)
        print(f'Finished {item}')
        qTakeoff.task_done()
        
        item = qLocation.get()
        print(f'Working on {item}')
        ack3 = stub.SetDroneLocation(item)
        print(ack3)
        print(f'Finished {item}')
        
        qLocation.task_done()
        
threading.Thread(target=worker, daemon=True).start()

start_time = time.time()
for item in range(10):
    curr_time = int((time.time()-start_time)*1000) #! NOTE: milliseconds
    ln = viz_connect.LandingNotification(msgId=item, isLanded=True, px4Time=(curr_time))
    tn = viz_connect.TakeoffNotification(msgId=item, isTakenOff=True, px4Time=(curr_time))
    loc = viz_connect.Location(msgId=item, latitude=41.123456, longitude=82.123456, px4Time=(curr_time))
    qLanding.put(ln)
    qTakeoff.put(tn)
    qLocation.put(loc)
    mavsdkBlock()
print('All task requests sent\n', end='')

# block until all tasks are done
qLanding.join()
qTakeoff.join()
qLocation.join()
print('All work completed')