#!/bin/bash
# https://stackoverflow.com/questions/24112727/relative-paths-based-on-file-location-instead-of-current-working-directory
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

echo -e "\e[1m\e[43m\e[30mObfuscating\e[0m"
python3 obfuscator.py

echo -e "\e[1m\e[43m\e[30mRunning nuitka\e[0m"
python3 -m nuitka --module map_reader.py

echo -e "\e[1m\e[43m\e[30mAssembling map reader\e[0m"
mkdir -p map_reader
mv map_reader.pyi map_reader/map_reader.pyi 
mv map_reader.cpython-38-x86_64-linux-gnu.so map_reader/map_reader.cpython-38-x86_64-linux-gnu.so
rm -r map_reader.build

echo -e "\e[1m\e[43m\e[30mCopying map reader into Visualizer\e[0m"
cp -r map_reader ../../Visualizer

echo -e "\e[1m\e[42m\e[30mDone. If you want to use the binary maps, you have to copy them over \e[4mmanually\e[24m.\e[0m"