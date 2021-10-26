from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode
from data import MapType

from bokeh.models import DataTable, TableColumn, Div
from bokeh.util.logconfig import bokeh_logger as log


class VizDataTable(VisualizationSharedDataStore):
    def __init__(self) -> None:
        log.info(" -- INIT DATA_TABLE")
        self.Viz = VisualizationSharedDataStore
        self.Viz.data_table = self

        # Tables
        if(self.Viz.mode == Mode.VISUALIZATION):
            self.columns_snr = [TableColumn(field="x", title="Lat"),
                                TableColumn(field="y", title="Lon"),
                                TableColumn(field='color', title='Color'),
                                TableColumn(field='alpha', title='Transparency')]
            self.columns_fs = [TableColumn(field="xs", title="Lats"),
                               TableColumn(field="ys", title="Lons"),
                               TableColumn(field='fill_color', title='Color'),
                               TableColumn(field='alpha', title='Transparency')]
        else:
            self.columns_snr = [TableColumn(field="x", title="Lat"),
                                TableColumn(field="y", title="Lon")]
            self.columns_fs = [TableColumn(field="xs", title="Lats"),
                               TableColumn(field="ys", title="Lons")]
            

        self.bounds_table = DataTable(source=self.Viz.data.bounds_table_source,
                                      columns=[TableColumn(field="minx", title="minx"),
                                               TableColumn(
                                                   field="miny", title="miny"),
                                               TableColumn(
                                                   field='maxx', title='maxx'),
                                               TableColumn(field='maxy', title='maxy')],
                                      editable=self.Viz.mode == Mode.MAP_MAKER,
                                      sizing_mode="stretch_both")
        self.survivors_table = DataTable(source=self.Viz.data.survivors_table_source,
                                         columns=self.columns_snr,
                                         editable=self.Viz.mode == Mode.MAP_MAKER,
                                         sizing_mode="stretch_both",
                                         height_policy="fit",
                                         min_height=200)
        self.fires_table = DataTable(source=self.Viz.data.fires_table_source,
                                     columns=self.columns_fs,
                                     editable=self.Viz.mode == Mode.MAP_MAKER,
                                     sizing_mode="stretch_both",
                                     height_policy="fit",
                                     min_height=200)
        self.wind_table = DataTable(source=self.Viz.data.wind_table_source,
                                    columns=[TableColumn(field="spd_kts", title="Speed (kts)"),
                                              TableColumn(field="dir_deg", title="Direction (deg)")],
                                    editable=False,
                                    sizing_mode="stretch_both")
        self.stats_table = DataTable(source=self.Viz.data.stats_table_source,
                                    columns=[TableColumn(field="elapsed_dur", title="Elapsed Mission Duration"),
                                            TableColumn(field="remaining_dur", title="Remaining Mission Duration"),
                                            TableColumn(field="mission_stat", title="Found survivors" if self.Viz.data.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE else "% Fires extinguished"),
                                            TableColumn(field="lat", title="Drone Lat"),
                                            TableColumn(field="lng", title="Drone Lng"),
                                            TableColumn(field="status", title="Drone Status"),
                                            TableColumn(field="points", title="Points")],
                                    editable=False,
                                    sizing_mode="stretch_both")

        # Table descriptions
        self.survivors_table_description = Div(text="""Entered Survivors<br>
                                               (select the Point Draw Tool and click on the map where you'd like to add new Survivors)"""
                                               if (self.Viz.mode == Mode.MAP_MAKER) else "Survivors",
                                               sizing_mode="stretch_both")
        self.fires_table_description = Div(text="""Entered Fires<br>
                                           (select the Poly Draw Tool and click on the map where you'd like to add new Fires)"""
                                           if (self.Viz.mode == Mode.MAP_MAKER) else "Fires",
                                           sizing_mode="stretch_both")
        self.bounds_table_description = Div(text="""Resulting Map Bounds<br>
                                            (zoom in such that the map shows what you'd like to be within your map)"""
                                            if self.Viz.mode == Mode.MAP_MAKER else """Map Bounds""",
                                            sizing_mode="stretch_both")
        self.wind_table_description = Div(text="""Wind<br>
                                               (not enabled)""")
        self.stats_table_description = Div(text="""Simulation Statistics""")

        # Register callbacks for table updates
        self.Viz.plot.figure.x_range.on_change(
            'start', self.updateMapBoundMinX)
        self.Viz.plot.figure.x_range.on_change('end', self.updateMapBoundMaxX)
        self.Viz.plot.figure.y_range.on_change(
            'start', self.updateMapBoundMinY)
        self.Viz.plot.figure.y_range.on_change('end', self.updateMapBoundMaxY)

    def updateMapBoundMinX(self, attr, old, new):
        self.Viz.data.bounds_table_source.data = {'minx': [new],
                                                  'miny': [self.Viz.data.bounds_table_source.data['miny'][0]],
                                                  'maxx': [self.Viz.data.bounds_table_source.data['maxx'][0]],
                                                  'maxy': [self.Viz.data.bounds_table_source.data['maxy'][0]]}
        self.bounds_table.update()

    def updateMapBoundMinY(self, attr, old, new):
        self.Viz.data.bounds_table_source.data = {'minx': [self.Viz.data.bounds_table_source.data['minx'][0]],
                                                  'miny': [new],
                                                  'maxx': [self.Viz.data.bounds_table_source.data['maxx'][0]],
                                                  'maxy': [self.Viz.data.bounds_table_source.data['maxy'][0]]}
        self.bounds_table.update()

    def updateMapBoundMaxX(self, attr, old, new):
        self.Viz.data.bounds_table_source.data = {'minx': [self.Viz.data.bounds_table_source.data['minx'][0]],
                                                  'miny': [self.Viz.data.bounds_table_source.data['miny'][0]],
                                                  'maxx': [new],
                                                  'maxy': [self.Viz.data.bounds_table_source.data['maxy'][0]]}
        self.bounds_table.update()

    def updateMapBoundMaxY(self, attr, old, new):
        self.Viz.data.bounds_table_source.data = {'minx': [self.Viz.data.bounds_table_source.data['minx'][0]],
                                                  'miny': [self.Viz.data.bounds_table_source.data['miny'][0]],
                                                  'maxx': [self.Viz.data.bounds_table_source.data['maxx'][0]],
                                                  'maxy': [new]}
        self.bounds_table.update()
