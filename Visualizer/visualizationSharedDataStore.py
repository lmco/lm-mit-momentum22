##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

from enum import Enum

class Mode(Enum):
    MAP_MAKER = 0
    VISUALIZATION = 1

class VisualizationSharedDataStore(object):
    button = None
    data_table = None
    data = None
    plot = None
    text = None
    
    mode = Mode.VISUALIZATION
    map_name = None