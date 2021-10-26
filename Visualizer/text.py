from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode

from bokeh.models import TextInput
from bokeh.util.logconfig import bokeh_logger as log


class Text(VisualizationSharedDataStore):
    def __init__(self) -> None:
        log.info(" -- INIT TEXT")
        self.Viz = VisualizationSharedDataStore
        self.Viz.text = self

        # Create space to enter map name
        self.map_name_text_box = TextInput(value=self.Viz.data.map_data_dict['map_name'], title="Enter map name (file will be saved as <what you enter>.json):",
                                           sizing_mode="stretch_width", disabled=self.Viz.mode == Mode.VISUALIZATION)
        self.map_name_text_box.on_change(
            'value_input', self.Viz.button.set_map_name)
