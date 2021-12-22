##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

import pickle
from typing import Dict
from pathlib import Path
from datetime import datetime
import json
import traceback
from typing import Dict
from os.path import exists


def deserialize(map_name: str) -> Dict:
    with open("maps/" + map_name + ".bin", "rb") as picklefile:
        return pickle.load(picklefile)

def save_map_record_as(self, log) -> None:
    """
    Saves the map record to file in the maps directory.
    """
    if(not self.disable_save):
        try:
            log.info(" ---- Saving map")
            
            # Make sure the directory exists
            Path("maps").mkdir(parents=True, exist_ok=True)
            
            with open("maps/" + self.map_data_dict['map_name'] + ".json", 'w+') as outfile:
                # Date the file
                self.map_data_dict["generated_on"] = datetime.now().strftime(
                    "%d/%m/%Y_%H:%M:%S")
                
                # Save bounds
                # Make we don't have any cascading lists
                self.Viz.data_table.bounds_table.source.data = {'minx': self.flatten(self.bounds_table_source.data['minx']),
                                                                'miny': self.flatten(self.bounds_table_source.data['miny']),
                                                                'maxx': self.flatten(self.bounds_table_source.data['maxx']),
                                                                'maxy': self.flatten(self.bounds_table_source.data['maxy'])}
                self.map_data_dict["bounds"] = self.Viz.data_table.bounds_table.source.data
                
                # Save objects of interest
                if(self.Viz.map_name is None):
                    # The first line is empty when saving from scrapt, so skip that entry
                    self.map_data_dict["data_fs"]['xs'] = self.Viz.data_table.fires_table.source.data['xs'][1:]
                    self.map_data_dict["data_fs"]['ys'] = self.Viz.data_table.fires_table.source.data['ys'][1:]
                else:
                    self.map_data_dict["data_fs"]['xs'] = self.Viz.data_table.fires_table.source.data['xs']
                    self.map_data_dict["data_fs"]['ys'] = self.Viz.data_table.fires_table.source.data['ys']
                    
                # Make we don't have any cascading lists
                self.map_data_dict["data_snr"]['x'] = self.flatten(self.Viz.data_table.survivors_table.source.data['x'])
                self.map_data_dict["data_snr"]['y'] = self.flatten(self.Viz.data_table.survivors_table.source.data['y'])

                # Save as pretty json
                json.dump(self.map_data_dict,
                        outfile,
                        indent=4,
                        sort_keys=True)
        except:
            log.error(traceback.format_exc())
            log.error("Map save encountered an issue (see traceback above)")

def load_map_record(self, log, map_name: str) -> Dict:
    """
    Loads the given map from the maps directory.

    Parameters
    ----------
    map_name : str
        Name of the map to load (without extension).

    Returns
    -------
    Dict
        The data read from the map record file.
    """
    if(exists("maps/" + map_name + ".json")):
        self.disable_save = False
        with open("maps/" + map_name + ".json") as f:
            map_data = json.load(f)
            return map_data
    elif(exists("maps/" + map_name + ".bin")):
        self.disable_save = True
        return deserialize(map_name)
    elif(len(map_name) == 0):
        self.disable_save = False
    else:
        log.error("Map with the name " + map_name + " does not exist. Stopping execution")
        exit()