##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

# SAR Solutions File Generator
#
# This script reads the survivor coordinates from a SAR JSON file and writes them to a 
# top-secret file format (python pickle).
#
# This works with load_map_record() in Visualizer:data.py.  The expectation is that we 
# will save a map file with all of the search-and-rescue points removed, and then
# use this script to hide the search-and-rescue points in a bin file.  
#
# In Visualizer, data.py will layer the data from the two files on top of each other to
# reconstruct the full set of information.

import json
import pickle
import sys

if len(sys.argv) < 2:
    print("Usage: python MakeSolutionFile.py filename.json")
    sys.exit(1)

jsonfile = sys.argv[1]

print("\nReading " + jsonfile + "\n")

with open(jsonfile) as f:
    jsondata = json.load(f)

print(jsondata)

print("\ndata_snr from json:\n")

data_snr = jsondata['data_snr']

print(data_snr)

binfile = jsonfile[0:-5] + ".snr.bin"

print("\nwriting to bin file via pickle:\n")
print("filename will be " + binfile)

pickle.dump(data_snr, open(binfile, "wb"))

print("\nreading bin file back for verification:\n")

data_snr_read = pickle.load(open(binfile, "rb"))

print(data_snr_read)

print("\nThis file should be moved to the Visualizer/static directory and renamed to a hidden file ('." + binfile + "')\n")
print("Remember to remove the contents of data_snr from the JSON file that is being distributed to students.\n")