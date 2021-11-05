##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

from concurrent import futures
import grpc

import viz_pb2 as viz_connect
import viz_pb2_grpc as viz_connect_grpc

import multiprocessing

from bokeh.util.logconfig import bokeh_logger as log


class Momentum22VizServicer(viz_connect_grpc.Momentum22VizServicer):
    def __init__(self, ql, qt, qp) -> None:
        self.qLanding = ql
        self.qTakeoff = qt
        self.qLocation = qp
        pass
    
    def SetLandingStatus(self, request, context):
        ack = viz_connect.ReqAck(msgId = request.msgId)
        self.qLanding.put(request)
        log.info(ack)
        return ack
    
    def SetTakeoffStatus(self, request, context):
        ack = viz_connect.ReqAck(msgId = request.msgId)
        self.qTakeoff.put(request)
        log.info(ack)
        return ack
    
    def SetDroneLocation(self, request, context):
        ack = viz_connect.ReqAck(msgId = request.msgId)
        self.qLocation.put(request)
        log.info(ack)
        return ack
    
def serveGrpc(qLanding, qTakeoff, qLocation):
    """
    Start the server and keep it alive until done
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    viz_connect_grpc.add_Momentum22VizServicer_to_server(
        Momentum22VizServicer(qLanding, qTakeoff, qLocation), server)
    server.add_insecure_port('[::]:51052')
    server.start()
    log.info(" -- gRPC server started")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(None)

p = None

def start(qLanding, qTakeoff, qLocation):
    # Throw the server into another process so that we can do viz tasks without interruptions
    p = multiprocessing.Process(target=serveGrpc, args=(qLanding, qTakeoff, qLocation))
    p.start()
    
def cleanUp():
    p.join()
    p.close()
    
