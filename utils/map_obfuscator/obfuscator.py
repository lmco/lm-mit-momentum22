##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

import pickle
import json
import os
        
# https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
directory = os.fsencode("maps")
    
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".json"):
         with open(directory.decode('ascii') + "/" + filename, "r") as jsonfile:
            print(directory.decode('ascii') + "/" + filename)
            jsondata = json.load(jsonfile)
            #https://stackoverflow.com/questions/2900035/changing-file-extension-in-python
            pre, ext = os.path.splitext(filename)
            with open("pickled/" + pre + ".bin", "wb+") as picklefile:
                pickle.dump(jsondata, picklefile)
     else:
         continue