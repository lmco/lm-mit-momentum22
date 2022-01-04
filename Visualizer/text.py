##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################
# Datastore
from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode

# Bokeh visualization
from bokeh.models import TextInput
from bokeh.util.logconfig import bokeh_logger as log


class Text(VisualizationSharedDataStore):
    """
    Keeps track of information relating to text fields, 
    including forwarding entries made into them to the appropriate sinks.
    
    Attributes
    ----------
    Viz : VisualizationSharedDataStore
        Datastore that contains the component objects of the visualizer.
    map_name_text_box : TextInput
        Bokeh object for editable text field.
    """
    
    def __init__(self) -> None:        
        log.info(" -- INIT TEXT")
        self.Viz = VisualizationSharedDataStore
        self.Viz.text = self

        # Create text field to enter map name
        self.map_name_text_box = TextInput(value=self.Viz.data.map_data_dict['map_name'], 
                                           title="Enter map name (file will be saved as <what you enter>.json):",
                                           sizing_mode="stretch_width", 
                                           disabled=self.Viz.mode == Mode.VISUALIZATION or self.Viz.data.disable_save)
        self.map_name_text_box.on_change(
            'value_input', self.Viz.button.set_map_name)
