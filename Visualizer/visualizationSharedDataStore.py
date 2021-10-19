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