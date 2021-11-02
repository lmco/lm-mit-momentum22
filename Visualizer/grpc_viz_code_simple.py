from concurrent import futures
import logging

import grpc

import viz_pb2 as viz_connect
import viz_pb2_grpc as viz_connect_grpc

import time
import multiprocessing

def vizBlock():
    print("sleep commence")
    time.sleep(60)
    print("sleep done")


class Momentum22VizServicer(viz_connect_grpc.Momentum22VizServicer):
    def __init__(self) -> None:
        pass
    
    def SetLandingStatus(self, request, context):
        ack = viz_connect.ReqAck(msgId = request.msgId)
        print(request)
        return ack
    
    def SetTakeoffStatus(self, request, context):
        ack = viz_connect.ReqAck(msgId = request.msgId)
        print(request)
        return ack
    
    def SetDroneLocation(self, request, context):
        ack = viz_connect.ReqAck(msgId = request.msgId)
        print(request)
        return ack
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    viz_connect_grpc.add_Momentum22VizServicer_to_server(
        Momentum22VizServicer(), server)
    server.add_insecure_port('[::]:51052')
    server.start()
    server.wait_for_termination()
    
if __name__ == '__main__':
    logging.basicConfig()
    p = multiprocessing.Process(target=serve)
    p.start()
    
    vizBlock()
    
