# Visualizer

Utility to make and use MIT Momentum competition maps interactively.

## How to use

1. Navigate your command line to the root folder of the project (this Visualizer folder should be a subfolder to the root)
2. Run the visualizer in one of two modes
   1. Enter `bokeh serve Visualizer --show --args -m` on your commandline, press `Enter` for the MapMaker
   2. Enter `bokeh serve Visualizer --show --args -v <mapname>` on your commandline, where `<mapname>` is a map stored in the maps directory, press `Enter` for the Visualizer
3. A web browser tab should open with the Visualizer utility at http://localhost:5006/Visualizer

## Dependencies

``` sh
pip3 install bokeh
pip3 install geopandas
```

Refer to the [geopandas](https://geopandas.org/getting_started/install.html#installing-with-pip) website if you experience issues with missing dependencies for geopandas.
