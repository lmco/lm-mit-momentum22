##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

import pickle
import json
import os
        
# https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
directory = os.fsencode("pickled")
    
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".bin"):
         with open(directory.decode('ascii') + "/" + filename, "rb") as picklefile:
            print(directory.decode('ascii') + "/" + filename)
            pickledata = pickle.load(picklefile)
            #https://stackoverflow.com/questions/2900035/changing-file-extension-in-python
            pre, ext = os.path.splitext(filename)
            with open("depickled/" + pre + ".json", "w+") as jsonfile:
                json.dump(pickledata, jsonfile, indent=4, sort_keys=True)
     else:
         continue