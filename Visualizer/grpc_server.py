##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################
# Grpc
import grpc
import viz_pb2 as viz_connect
import viz_pb2_grpc as viz_connect_grpc

# Multiprocessing
import multiprocessing
from multiprocessing import Queue
from concurrent import futures

# Bokeh visualization
from bokeh.util.logconfig import bokeh_logger as log


class Momentum22VizServicer(viz_connect_grpc.Momentum22VizServicer):
    """
    Makes the GRPC servicer for connecting to the student code.
    
    Attributes
    ----------
    qLanding : multiprocessing.Queue
        Queue where to put the messages coming over the line.
    qTakeoff : multiprocessing.Queue
        Queue where to put the messages coming over the line.
    qLocation : multiprocessing.Queue
        Queue where to put the messages coming over the line.
    
    Methods
    -------
    SetLandingStatus(request: viz_connect.LandingNotification, context: (unused))
        Gets the landing status from the grpc connection, puts it into the appropriate queue and replies back with the acknowledgement.
    SetTakeoffStatus(request: viz_connect.TakeoffNotification, context: (unused))
        Gets the takeoff status from the grpc connection, puts it into the appropriate queue and replies back with the acknowledgement.
    SetDroneLocation(request: viz_connect.Location, context: (unused))
        Gets the drone location from the grpc connection, puts it into the appropriate queue and replies back with the acknowledgement.
    """
    
    def __init__(self, qLanding: Queue, qTakeoff: Queue, qLocation: Queue) -> None:
        """ 
        Makes the grpc servicer.

        Parameters
        ----------
        qLanding : multiprocessing.Queue
            Queue where to put landing notifications.
        qTakeoff : multiprocessing.Queue
            Queue where to put takeoff notifications.
        qLocation : multiprocessing.Queue
            Queue where to put position (location) notifications.
        """
        
        self.qLanding = qLanding
        self.qTakeoff = qTakeoff
        self.qLocation = qLocation
    
    
    
    def SetLandingStatus(self, request: viz_connect.LandingNotification, context) -> viz_connect.ReqAck:
        """
        Processes the message that set the Landing status in the Visualizer.

        Parameters
        ----------
        request : viz_connect.LandingNotification
            The request that came over the line to set the landing status.
        context : [type]
            unused

        Returns
        -------
        viz_connect.ReqAck
            The acknowledgement of receipt of the message
        """
        
        ack = viz_connect.ReqAck(msgId = request.msgId)
        self.qLanding.put(request)
        return ack
    
    def SetTakeoffStatus(self, request: viz_connect.TakeoffNotification, context) -> viz_connect.ReqAck:
        """
        Processes the message that set the Takeoff  status in the Visualizer.

        Parameters
        ----------
        request : viz_connect.Takeoff Notification
            The request that came over the line to set the Takeoff  status.
        context : [type]
            unused

        Returns
        -------
        viz_connect.ReqAck
            The acknowledgement of receipt of the message
        """
        
        ack = viz_connect.ReqAck(msgId = request.msgId)
        self.qTakeoff.put(request)
        return ack
    
    def SetDroneLocation(self, request:viz_connect.Location, context) -> viz_connect.ReqAck:
        """
        Processes the message that set the Drone Location in the Visualizer.

        Parameters
        ----------
        request : viz_connect.DroneLocation
            The request that came over the line to set the Drone Location.
        context : [type]
            unused

        Returns
        -------
        viz_connect.ReqAck
            The acknowledgement of receipt of the message
        """
        
        ack = viz_connect.ReqAck(msgId = request.msgId)
        self.qLocation.put(request)
        return ack
    
def serveGrpc(qLanding: Queue, qTakeoff: Queue, qLocation: Queue) -> None:
    """
    Start the server and keep it alive until done.

    Parameters
    ----------
    qLanding : multiprocessing.Queue
        Queue where to put landing notifications.
    qTakeoff : multiprocessing.Queue
        Queue where to put takeoff notifications.
    qLocation : multiprocessing.Queue
        Queue where to put position (location) notifications.
    """
    
    # Create a new server with no more than 10 worker threads to process incoming connections.
    # The 10 count for the threads is arbitrary, but it seems to work.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Connect the servicer to the server
    viz_connect_grpc.add_Momentum22VizServicer_to_server(
        Momentum22VizServicer(qLanding, qTakeoff, qLocation), server)
    
    # Specify where to serve (localhost:51052)
    server.add_insecure_port('[::]:51052')
    
    # Star the server
    server.start()
    log.info(" -- INIT GRPC: server started")
    try:
        # Spin until terminated with keyboard interrupt
        server.wait_for_termination()
    except KeyboardInterrupt:
        # Catch keyboard interrupt, stop the server, and join/close processes
        server.stop(None)
        cleanUp()

# Process that all of this happens in (assigned when start is called)
p = None

def start(qLanding: Queue, qTakeoff: Queue, qLocation: Queue) -> None:
    """
    Starts the grpc server and puts it into a new process.

    Parameters
    ----------
    qLanding : multiprocessing.Queue
        Queue where to put landing notifications.
    qTakeoff : multiprocessing.Queue
        Queue where to put takeoff notifications.
    qLocation : multiprocessing.Queue
        Queue where to put position (location) notifications.
    """
    
    # Throw the server into another process so that we can do viz tasks without interruptions
    p = multiprocessing.Process(target=serveGrpc, args=(qLanding, qTakeoff, qLocation))
    p.start()
    
def cleanUp() -> None:
    """
    Cleans up the grpc process.
    """
    
    log.info(" --- Cleaning up gRPC server")
    if(p is not None):
        p.join()
        p.close()
    
