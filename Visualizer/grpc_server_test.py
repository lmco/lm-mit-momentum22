from concurrent import futures
import logging

import grpc

import viz_pb2 as viz_connect
import viz_pb2_grpc as viz_connect_grpc


class Momentum22VizServicer(viz_connect_grpc.Momentum22VizServicer):
    def __init__(self) -> None:
        pass
    
    def SetLandingStatus(self, request, context):
        # ln = viz_connect.LandingNotification(msgId = 1, isLanded=True, px4Time = 0)
        ack = viz_connect.ReqAck(msgId = request.msgId)
        print(request)
        return ack
    
    def SetTakeoffStatus(self, request, context):
        # tn = viz_connect.TakeoffNotification(msgId = 1, isTakenOff=True, px4Time = 0)
        ack = viz_connect.ReqAck(msgId = request.msgId)
        print(request)
        return ack
    
    def SetDroneLocation(self, request, context):
        # loc = viz_connect.Location(msgId=request.msgId, latitude = 41.123456, longitude = 82.123456, px4Time = 123456)
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
    serve()
