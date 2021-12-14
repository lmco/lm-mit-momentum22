##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

from enum import Enum

class Mode(Enum):
    """
    Represents the modes that the user can start the visualizer in
    
    Modes
    -----
    MAP_MAKER : 0
        Mode that gives controls for making custom maps, but does not allow interaction with PX4 or student code
    VISUALIZATION : 1
        Mode that allows interaction with PX4 or student code, but does not allow any interactions with the maps themselves
    """
    
    MAP_MAKER = 0
    VISUALIZATION = 1

class VisualizationSharedDataStore(object):
    """ Data store for the Visualizer
    
    This object stores the sub-objects that make up the Visualizer
    
    Attributes
    ----------
    button : VizButton
        button-controller that keeps track of the button states and interactions with them
    data_table : VizDataTable
        data-table-controller that keeps track of the data table states and interactions with them
    data : Data
        data-controller that performs all calculations and keeps track of the scoring and mission statistics
    plot : Plot
        plot-controller that sets up the plot and keeps track of the interactions with the plot (both from code and user)
    text : Text
        text-controller that sets up and keeps track of the changes in text entry fields
    mode : Enum
        the mode that the visualization is running in
    map_name : str
        name of the map the visualization is working with (can be None)
    """
    
    # The group below inherits from this object (as assigned in main.py)
    button = None
    data_table = None
    data = None
    plot = None
    text = None
    
    mode = Mode.VISUALIZATION
    map_name = None