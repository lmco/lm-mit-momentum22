from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode
from data import MapType

from bokeh.models import Div, Button, RadioButtonGroup
from bokeh.util.logconfig import bokeh_logger as log
from enum import IntEnum


class VizVisibility(IntEnum):
    VISIBLE = 0
    INVISIBLE = 1


class VizButton(VisualizationSharedDataStore):
    def __init__(self) -> None:
        log.info(" -- INIT BUTTON")
        self.Viz = VisualizationSharedDataStore
        self.Viz.button = self

        # Make a binary selection for the track this map is for
        self.LABELS = ["Fire Fighting", "Search & Rescue"]
        self.radio_button_group = RadioButtonGroup(labels=self.LABELS, active=int(
            self.Viz.data.map_data_dict['map_type']), sizing_mode="stretch_width", disabled=self.Viz.mode == Mode.VISUALIZATION)
        self.radio_button_group.on_click(self.set_map_type)
        self.radio_button_description = Div(text="""This map is for <b>""" + self.LABELS[self.Viz.data.map_data_dict['map_type']] +
                                            "<b>" if self.Viz.mode == Mode.VISUALIZATION else """This map will be for""", sizing_mode="stretch_both")

        # Make a safe button for the map
        self.save_button = Button(label="SAVE MAP", button_type="success",
                                  sizing_mode="stretch_width", disabled=self.Viz.mode == Mode.VISUALIZATION)
        self.save_button.on_click(self.Viz.data.save_map_record)

        self.cheat_button = Button(label="CHEAT (TOGGLE VISIBILITY ON THE ITEMS OF INTEREST)", button_type="success",
                                   sizing_mode="stretch_width", disabled=self.Viz.mode == Mode.MAP_MAKER)
        self.cheat_button.on_click(self.toggle_items_of_interest)

        self.cheat_status = VizVisibility.INVISIBLE

    # Callback to save type entry in the data structure
    def set_map_type(self, attr):
        log.info(" --- Map type set to " + ("Search and Rescue" if attr == MapType.SEARCH_AND_RESCUE else "Fire Suppression"))
        self.Viz.data.map_data_dict['map_type'] = attr

    # Callback to save name entry in the data structure
    def set_map_name(self, attr, old, new):
        self.Viz.data.map_data_dict['map_name'] = new

    def toggle_items_of_interest(self):
        log.info(" --- Cheating " + ("ON" if self.cheat_status == VizVisibility.VISIBLE else "OFF"))
        if (self.Viz.data.map_data_dict['map_type'] == MapType.SEARCH_AND_RESCUE):
            self.Viz.data.survivors_table_source.data['alpha'] = [self.cheat_status]*len(self.Viz.data.survivors_table_source.data['alpha'])
        elif (self.Viz.data.map_data_dict['map_type'] == MapType.FIRE_SUPPRESSION):
            self.Viz.data.fires_table_source.data['alpha'] = [self.cheat_status]*len(self.Viz.data.fires_table_source.data['alpha'])
            
        self.cheat_status = VizVisibility.VISIBLE if self.cheat_status == VizVisibility.INVISIBLE else VizVisibility.INVISIBLE
