##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################
# Datastore
from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode
from data import MapType

# Bokeh visualization
from bokeh.models import Div, Button, RadioButtonGroup
from bokeh.util.logconfig import bokeh_logger as log

# Helpers
from enum import IntEnum


class VizVisibility(IntEnum):
    """
    Represents the visibility modes that the objects of interest can embody.
    
    Modes
    -----
    VISIBLE : 1
        Affected object of interest are visible in the map (alpha=1.0).
    INVISIBLE : 0
        Affected object of interest are invisible in the map (alpha=0.0).
    """
    
    VISIBLE = 1
    INVISIBLE = 0


class VizButton(VisualizationSharedDataStore):
    """
    Keeps track of information relating to buttons, including forwarding entries made into them to the appropriate sinks.
    
    Attributes
    ----------
    Viz : VisualizationSharedDataStore
        Datastore that contains the component objects of the visualizer.
    LABELS : str list
        List of labels that describe the types of maps available.
    radio_button_group : bokeh.models.RadioButtonGroup
        Radio buttons allowing the user the choose the type of map.
    radio_button_description : bokeh.models.Div
        Description for what the radio button group does.
    save_as_button : bokeh.models.Button
        Button that saves the map as using the name entered in the text field as the name of the file and the map.
    bind_map_button : bokeh.models.Button
        Button that binds the map to a preset dimension keeping the centerpoint constant.
    cheat_button : bokeh.models.Button
        Button that changes the visibility of the affected objects of interest to allow cheating.
    cheat_status : VizVisibility
        Keeps track of the visibility on the objects of interest.
    """
    
    def __init__(self) -> None:
        log.info(" -- INIT BUTTON")
        self.Viz = VisualizationSharedDataStore
        self.Viz.button = self

        # Make labels we can index into using Data.MapType
        self.LABELS = ["Fire Fighting", "Search & Rescue"]
        
        # Make a binary selection for the track this map is for
        self.radio_button_group = RadioButtonGroup(labels=self.LABELS, 
                                                   active=int(
                                                   self.Viz.data.map_data_dict['map_type']), 
                                                   width_policy="min",
                                                   min_width=500,
                                                   disabled=self.Viz.mode == Mode.VISUALIZATION)
        self.radio_button_group.on_click(self.set_map_type)
        
        # Make a description for the radio group indication which type of task the map is for
        self.radio_button_description = Div(text="""This map is for <b>""" + 
                                            self.LABELS[self.Viz.data.map_data_dict['map_type']] +
                                            "<b>" 
                                            if self.Viz.mode == Mode.VISUALIZATION 
                                            else """This map will be for""", sizing_mode="stretch_both")

        # Make a save button for the map and make it call the save map method on click
        self.save_as_button = Button(label="SAVE MAP AS", 
                                     button_type="success",
                                     width_policy="min",
                                     min_width=500,
                                     disabled=self.Viz.mode == Mode.VISUALIZATION or self.Viz.data.disable_save)
        self.save_as_button.on_click(self.Viz.data.save_map_record_as)
        
        # Make a bind button for the map and make it call the bind map method on click
        self.bind_map_button = Button(label="BIND WINDOW TO STANDARD DIMS", 
                                      button_type="success",
                                      width_policy="min",
                                      min_width=500,
                                      disabled=self.Viz.mode == Mode.VISUALIZATION)
        self.bind_map_button.on_click(self.Viz.data.bind_bbox)

        # Make a cheat button for the map and make it call the method that changes the visibilities on objects of interest on click
        self.cheat_button = Button(label="CHEAT (TOGGLE VISIBILITY ON THE ITEMS OF INTEREST)", 
                                   button_type="success",
                                   width_policy="min",
                                   min_width=500,
                                   disabled=self.Viz.mode == Mode.MAP_MAKER or self.Viz.data.map_data_dict['map_type'] == MapType.FIRE_SUPPRESSION or self.Viz.data.disable_save)
        self.cheat_button.on_click(self.toggle_items_of_interest)

        # Keep track of the visibility
        self.cheat_status = VizVisibility.INVISIBLE



    def set_map_type(self, attr) -> None:
        """ 
        Sets the map type.
        
        Intended as a callback called by a Button.
        
        Parameters
        ----------
        attr : int
            Map type to set (see Data.MapType).
        """
        
        log.info(" --- Map type set to " + ("Search and Rescue" if attr == MapType.SEARCH_AND_RESCUE else "Fire Suppression"))
        self.Viz.data.map_data_dict['map_type'] = attr

    # Callback to save name entry in the data structure
    def set_map_name(self, attr, old, new) -> None:
        """ 
        Sets the map name.
        
        Intended as a callback called by a Button.
        
        Parameters
        ----------
        attr : [type]
            unused
        old : [type]
            unused
        new : str
            new name of the map to use when saving.
        """
        
        self.Viz.data.map_data_dict['map_name'] = new

    def toggle_items_of_interest(self) -> None:
        """ 
        Toggles the visibilities on the objects of interest.
        
        Intended as a callback called by a bokeh.models.Button.
        """
        
        # Toggle visibility for our records
        self.cheat_status = (VizVisibility.VISIBLE 
                             if self.cheat_status == VizVisibility.INVISIBLE 
                             else VizVisibility.INVISIBLE)
        
        log.info(" --- Cheating " + ("ON" 
                                     if self.cheat_status == VizVisibility.VISIBLE 
                                     else "OFF"))
    
        # Toggle the visibilities only on the objects that belong to the current map type
        if (self.Viz.data.map_data_dict['map_type'] == MapType.SEARCH_AND_RESCUE):
            self.Viz.data.survivors_table_source.data['alpha'] = [self.cheat_status] * len(self.Viz.data.survivors_table_source.data['alpha'])
        elif (self.Viz.data.map_data_dict['map_type'] == MapType.FIRE_SUPPRESSION):
            self.Viz.data.fires_table_source.data['alpha'] = [self.cheat_status] * len(self.Viz.data.fires_table_source.data['alpha'])
        
        
