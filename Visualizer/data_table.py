##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################
# Datastore
from visualizationSharedDataStore import VisualizationSharedDataStore
from visualizationSharedDataStore import Mode
from data import MapType

# Bokeh visualization
from bokeh.models import DataTable, TableColumn, Div
from bokeh.util.logconfig import bokeh_logger as log


class VizDataTable(VisualizationSharedDataStore):
    """
    Keeps track of information relating to buttons, including forwarding entries made into them to the appropriate sinks.
    
    Attributes
    ----------
    Viz : VisualizationSharedDataStore
        Datastore that contains the component objects of the visualizer.
    columns_snr : bokeh.models.TableColumn list
        Describes the column names and user-friendly titles that the search and rescue data table will have.
    columns_fs :  bokeh.models.TableColumn list
        Describes the column names and user-friendly titles that the fire suppression data table will have.
    bounds_table : bokeh.models.DataTable
        Table containing data about the map bounds.
    survivors_table : bokeh.models.DataTable
        Table containing location and supplementary information about the survivors.
    fires_table : bokeh.models.DataTable
        Table containing locations and supplementary information about the fires.
    wind_table : bokeh.models.DataTable
        Table containing information about the winds affecting the mission (TODO: not implemented).
    stats_table : bokeh.models.DataTable
        Table containing general statistics about the mission at hand.
    survivors_table_description : bokeh.models.Div
        Description for the survivors table.
    fires_table_description : bokeh.models.Div
        Description for the fires table.
    bounds_table_description : bokeh.models.Div
        Description for the bounds table.
    wind_table_description : bokeh.models.Div
        Description for the winds table.
    stats_table_description : bokeh.models.Div
        Description for the mission statistics table.
    """
    
    def __init__(self) -> None:
        log.info(" -- INIT DATA_TABLE")
        self.Viz = VisualizationSharedDataStore
        self.Viz.data_table = self

        # Tables
        if(self.Viz.mode == Mode.VISUALIZATION):
            self.columns_snr = [TableColumn(field="x", title="Lon"),
                                TableColumn(field="y", title="Lat"),
                                TableColumn(field='color', title='Color'),
                                TableColumn(field='alpha', title='Transparency')]
            self.columns_fs = [TableColumn(field="xs", title="Lons"),
                               TableColumn(field="ys", title="Lats"),
                               TableColumn(field='fill_color', title='Color'),
                               TableColumn(field='alpha', title='Transparency')]
        else:
            self.columns_snr = [TableColumn(field="x", title="Lon"),
                                TableColumn(field="y", title="Lat")]
            self.columns_fs = [TableColumn(field="xs", title="Lons"),
                               TableColumn(field="ys", title="Lats")]
            

        self.bounds_table = DataTable(source=self.Viz.data.bounds_table_source,
                                      columns=[TableColumn(field="minx", title="minx"),
                                               TableColumn(field="miny", title="miny"),
                                               TableColumn(field='maxx', title='maxx'),
                                               TableColumn(field='maxy', title='maxy')],
                                      editable=self.Viz.mode == Mode.MAP_MAKER,
                                      sizing_mode="stretch_both",
                                      autosize_mode="fit_viewport")
        self.survivors_table = DataTable(source=self.Viz.data.survivors_table_source,
                                         columns=self.columns_snr,
                                         editable=self.Viz.mode == Mode.MAP_MAKER,
                                         sizing_mode="stretch_both",
                                         autosize_mode="fit_viewport",
                                         height_policy="fit",
                                         min_height=200)
        self.fires_table = DataTable(source=self.Viz.data.fires_table_source,
                                     columns=self.columns_fs,
                                     editable=self.Viz.mode == Mode.MAP_MAKER,
                                     sizing_mode="stretch_both",
                                     autosize_mode="fit_viewport",
                                     height_policy="fit",
                                     min_height=200)
        self.wind_table = DataTable(source=self.Viz.data.wind_table_source,
                                    columns=[TableColumn(field="spd_kts", title="Speed (kts)"),
                                             TableColumn(field="dir_deg", title="Direction (deg)")],
                                    editable=False,
                                    sizing_mode="stretch_both",
                                    autosize_mode="fit_viewport")
        self.stats_table = DataTable(source=self.Viz.data.stats_table_source,
                                     columns=[TableColumn(field="elapsed_dur", title="Elapsed Time (sec)"),
                                              TableColumn(field="remaining_dur", title="Remaining Time (sec)"),
                                              TableColumn(field="mission_stat", title="% Survivors Found" 
                                                          if self.Viz.data.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE 
                                                          else "Water Qt (sec)"),
                                              TableColumn(field="lon", title="Lon"),
                                              TableColumn(field="lat", title="Lat"),
                                              TableColumn(field="status", title="Status"),
                                              TableColumn(field="score", title="Num Survivors Found" 
                                                          if self.Viz.data.map_data_dict["map_type"] == MapType.SEARCH_AND_RESCUE 
                                                          else "% Fires extinguished")],
                                     editable=False,
                                     sizing_mode="stretch_both",
                                     autosize_mode="fit_viewport")

        # Table descriptions
        self.survivors_table_description = Div(text="""Entered Survivors<br>
                                               (select the Point Draw Tool and click on the map where you'd like to add new Survivors)"""
                                               if (self.Viz.mode == Mode.MAP_MAKER) 
                                               else "Survivors",
                                               sizing_mode="stretch_both")
        self.fires_table_description = Div(text="""Entered Fires<br>
                                           (select the Poly Draw Tool and click on the map where you'd like to add new Fires)"""
                                           if (self.Viz.mode == Mode.MAP_MAKER) 
                                           else "Fires",
                                           sizing_mode="stretch_both")
        self.bounds_table_description = Div(text="""Resulting Map Bounds<br>
                                            (zoom in such that the map shows what you'd like to be within your map)"""
                                            if self.Viz.mode == Mode.MAP_MAKER 
                                            else """Map Bounds""",
                                            sizing_mode="stretch_both")
        self.wind_table_description = Div(text="""Wind<br>
                                               (not enabled)""")
        self.stats_table_description = Div(text="""Simulation Statistics""")

        # Register callbacks for table updates
        self.Viz.plot.figure.x_range.on_change('start', self.updateMapBoundMinX)
        self.Viz.plot.figure.x_range.on_change('end',   self.updateMapBoundMaxX)
        self.Viz.plot.figure.y_range.on_change('start', self.updateMapBoundMinY)
        self.Viz.plot.figure.y_range.on_change('end',   self.updateMapBoundMaxY)
        
        
        
    def updateMapBoundMinX(self, attr, old, new) -> None:
        """ Updates the min x bound of the map based on the position of the map.
        
        Intended as a callback called by a bokeh.plotting.figure.
        
        Parameters
        ----------
        attr : [type]
            unused
        old : [type]
            unused
        new : float
            New start of the x_range on a figure.
        """
        
        self.Viz.data.bounds_table_source.patch({'minx': [(0, new)]})
        self.bounds_table.update()

    def updateMapBoundMinY(self, attr, old, new) -> None:
        """ Updates the min y bound of the map based on the position of the map.
        
        Intended as a callback called by a Figure.
        
        Parameters
        ----------
        attr : [type]
            unused
        old : [type]
            unused
        new : float
            New start of the y_range on a figure.
        """
        
        self.Viz.data.bounds_table_source.patch({'miny': [(0, new)]})
        self.bounds_table.update()

    def updateMapBoundMaxX(self, attr, old, new) -> None:
        """ Updates the max x bound of the map based on the position of the map.
        
        Intended as a callback called by a bokeh.plotting.figure.
        
        Parameters
        ----------
        attr : [type]
            unused
        old : [type]
            unused
        new : float
            New end of the x_range on a figure.
        """
        
        self.Viz.data.bounds_table_source.patch({'maxx': [(0, new)]})
        self.bounds_table.update()

    def updateMapBoundMaxY(self, attr, old, new) -> None:
        """ Updates the max x bound of the map based on the position of the map.
        
        Intended as a callback called by a bokeh.plotting.figure.
        
        Parameters
        ----------
        attr : [type]
            unused
        old : [type]
            unused
        new : float
            New end of the y_range on a figure.
        """
        
        self.Viz.data.bounds_table_source.patch({'maxy': [(0, new)]})
        self.bounds_table.update()
