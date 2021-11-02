import time

import grpc

import viz_pb2 as viz_connect
import viz_pb2_grpc as viz_connect_grpc


channel = grpc.insecure_channel('localhost:51052')
stub = viz_connect_grpc.Momentum22VizStub(channel)

ln = viz_connect.LandingNotification(msgId=1, isLanded=True, px4Time=123456)
tn = viz_connect.TakeoffNotification(msgId=1, isTakenOff=True, px4Time=123456)
loc = viz_connect.Location(msgId=1, latitude = 41.123456, longitude = 82.123456, px4Time = 123456)

for i in range (10):
    ack1 = stub.SetLandingStatus(ln)
    ack2 = stub.SetTakeoffStatus(tn)
    ack3 = stub.SetDroneLocation(loc)
    print(ack1)
    print(ack2)
    print(ack3)
    ln.msgId = ln.msgId + 1
    tn.msgId = tn.msgId + 1
    loc.msgId = loc.msgId + 1
    
    time.sleep(1)
