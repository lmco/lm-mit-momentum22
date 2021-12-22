# Map Obfuscator

Scripts to obfuscate and deobfuscate maps for MIT Momentum 2022.

## Obfuscate

Run `python3 obfuscator.py` to pickle all json files in a `maps` directory. Puts results into a `pickled` directory.

## Deobfuscate

Run `python3 deobfuscator.py` to unpickle all pickle files in a `pickled` directory. Puts results into a `depickled` directory.

## Building the obfuscated map reader for the visualizer

0. Install nuitka (`pip3 install nuitka`).
1. Make script executable (`chmod +x utils/map_obfuscator/make_map_reader.sh`)
2. Run script (`./utils/map_obfuscator/make_map_reader.sh`), which will
   - Obfuscate any maps present in the maps directory of this folder only (but not copy them)
   - Run nuitka to create a map reader module
   - Assemble all of the necessary files into one folder
   - Copy the assembled folder into the Visualizer

>Binary maps are not editable from the interface as is (you have to edit the parent json file and run it through the process described here).
