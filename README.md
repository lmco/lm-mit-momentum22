# Getting Started <!-- omit in toc -->

If you are viewing this file offline, the most up to date version of these instructions is located in the [project GitHub](https://github.com/katabeta/lm-mit-momentum).

***ATTENTION STUDENTS:***  **THERE WAS AN UPDATE TO THE LIDAR REGISTRATION ALGORITHM**. If you are using the default templates or are relying on the LIDAR registration algorithm in them, the previous versions of these files contained a bug in the coordinate transforms. This bug has been fixed and you must update your files. Thanks to the student who pointed out the bug during office hours on 25 JAN.

**NOTES:**

1. Unless otherwise specified, all instructions are to be entered into the terminal in your Ubuntu installation.
2. Commands that start with `sudo` will require your user password. Using sudo invokes superuser security privileges and is akin to running an application as an administrator in Windows.
3. There is a [playlist](https://youtube.com/playlist?list=PLvn3cENh89AszwCOFpApcvQNTHO7Ap-us) showing successful execution of these commands.
4. If you have specific questions that are not answered by this document, check out the constantantly updating [Q&A](https://github.com/katabeta/lm-mit-momentum/blob/master/QA.md).

## Table of Contents <!-- omit in toc -->
<!-- TOC and section numbers automatically generated, do not manually edit -->
- [1. Install Ubuntu 18.04 LTS or 20.04 LTS](#1-install-ubuntu-1804-lts-or-2004-lts)
  - [1.1. Basic steps to install Ubuntu outside of a Virtual Machine](#11-basic-steps-to-install-ubuntu-outside-of-a-virtual-machine)
  - [1.2. Basic steps to install Ubuntu inside of a Virtual Machine](#12-basic-steps-to-install-ubuntu-inside-of-a-virtual-machine)
- [2. Install VS Code IDE](#2-install-vs-code-ide)
- [3. Get Gazebo and PX4](#3-get-gazebo-and-px4)
  - [3.1. Clone PX4 and install Gazebo](#31-clone-px4-and-install-gazebo)
  - [3.2. Build PX4](#32-build-px4)
- [4. OPTIONAL Install QGroundControl](#4-optional-install-qgroundcontrol)
  - [4.1. Fix problem where PX4 running Gazebo can't connect to QGroundControl](#41-fix-problem-where-px4-running-gazebo-cant-connect-to-qgroundcontrol)
- [5. Install MAVSDK](#5-install-mavsdk)
- [6. Install navpy and numpy](#6-install-navpy-and-numpy)
- [7. Download py3gazebo](#7-download-py3gazebo)
- [8. Adding LM-provided LiDAR and terrain](#8-adding-lm-provided-lidar-and-terrain)
  - [8.1. Creating your own terrain and LiDAR](#81-creating-your-own-terrain-and-lidar)
- [9. Install py3gazebo](#9-install-py3gazebo)
- [10. Launch simulation](#10-launch-simulation)
  - [10.1. Set home position](#101-set-home-position)
  - [10.2. Launch PX4 with Gazebo](#102-launch-px4-with-gazebo)
  - [10.3. Set PX4 firmware parameters](#103-set-px4-firmware-parameters)
  - [10.4. How to find sensor topic name, message type, and get sample output](#104-how-to-find-sensor-topic-name-message-type-and-get-sample-output)
  - [10.5. OPTIONAL Launch QGroundControl](#105-optional-launch-qgroundcontrol)
- [11. Run a mission file](#11-run-a-mission-file)
- [12. Query sensor values using py3gazebo - GPS Example](#12-query-sensor-values-using-py3gazebo---gps-example)
- [13. Getting started with MAVSDK](#13-getting-started-with-mavsdk)
  - [13.1. Download MAVSDK examples](#131-download-mavsdk-examples)
  - [13.2. Run a MAVSDK example (PX4 and Gazebo have to be running)](#132-run-a-mavsdk-example-px4-and-gazebo-have-to-be-running)
<!-- TOC and section numbers automatically generated, do not manually edit -->

## 1. Install Ubuntu 18.04 LTS or 20.04 LTS

The software required for this project runs and is supported only in Ubuntu 18.04 or 20.04. As such, it is necessary to install this operating system to complete the project.

### 1.1. Basic steps to install Ubuntu outside of a Virtual Machine

1. [Download an Ubuntu image](https://ubuntu.com/download/desktop)
2. [Verify image download is not corrupted](https://ubuntu.com/tutorials/how-to-verify-ubuntu#1-overview)
3. Make a bootable live USB in current OS
    - Make live USB in [Windows](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows#1-overview)
    - Make live USB in [Ubuntu](https://ubuntu.com/tutorials/create-a-usb-stick-on-ubuntu#1-overview)
    - Make live USB in [Mac](https://ubuntu.com/tutorials/create-a-usb-stick-on-macos#1-overview)
4. [Boot from created USB](https://ubuntu.com/tutorials/install-ubuntu-desktop#4-boot-from-usb-flash-drive)
   - If your computer doesn't automatically boot from from the USB and `F12` does not work to invoke the boot menu, pay attention to the bootscreen for the key specific for your computer.
5. Choose how to Install Ubuntu:
    - [Install to dual boot with current OS](https://ubuntu.com/tutorials/install-ubuntu-desktop#6-allocate-drive-space) (**recommended**). This will create an Ubuntu partition on your computer. Select "Install Ubuntu" when prompted after booting from USB, then [follow these steps](https://ubuntu.com/tutorials/install-ubuntu-desktop#6-allocate-drive-space)
    - [Install with persistent storage onto a USB drive](https://www.howtogeek.com/howto/14912/create-a-persistent-bootable-ubuntu-usb-flash-drive/) (**advanced**). This does not require any changes to your computer; instead Ubuntu will exist on its own USB device with its own memory. This will require an additional USB device to install the persistent image onto. Select "Try Ubuntu" when prompted after booting from USB, then [follow these steps](https://www.howtogeek.com/howto/14912/create-a-persistent-bootable-ubuntu-usb-flash-drive/)
    - [Install instead of current OS](https://ubuntu.com/tutorials/install-ubuntu-desktop#6-allocate-drive-space) (**not recommended**). This will replace your computer's OS with Ubuntu. Select "Install Ubuntu" when prompted after booting from USB, then [follow these steps](https://ubuntu.com/tutorials/install-ubuntu-desktop#6-allocate-drive-space)

### 1.2. Basic steps to install Ubuntu inside of a Virtual Machine

1. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. [Download an Ubuntu image](https://ubuntu.com/download/desktop)
3. [Verify image download is not corrupted](https://ubuntu.com/tutorials/how-to-verify-ubuntu#1-overview)
4. [Install Ubuntu in VirtualBox](https://brb.nci.nih.gov/seqtools/installUbuntu.html)

## 2. Install VS Code IDE

VS Code is an open-source light-weight feature-rich IDE (Integrated Development Environment) developed by Microsoft. Using an IDE greatly enhances the developer's comfort when coding by enabling features such as syntax highlighting, suggestions, and linting.

Summary of [VS Code setup instructions](https://code.visualstudio.com/docs/setup/linux):

``` sh
# Make the home directory for the project and step into it.
# You may install your software in a different directory, but then take care to change your home directory when following the instructions.
mkdir -p ~/Momentum
cd ~/Momentum

# Install VS Code from snap
sudo snap install --classic code

# Launch VS Code from current terminal directory and put it in the background
code . &
```

## 3. Get Gazebo and PX4

PX4 is industry-standard autopilot software for hobbyist drone applications. It provides easy access to high quality control laws for a variety of drones, including in simulation. For the purposes of this project, this software will allow the user to simply set waypoints, while the PX4 software performs all of the necessary calculations to control and interface with the motors to get the drone to the next waypoint.

Gazebo is similarly positioned in the robotics simulation world and is heavily used with ROS (Robot Operating System, not used in this project). Gazebo enables real-time physics simulation, sensor and terrain integration, and provides visual feedback for the user.

### 3.1. Clone PX4 and install Gazebo

Summary of [PX4 and Gazebo setup guide for ubuntu](https://dev.px4.io/master/en/setup/dev_env_linux_ubuntu.html):

``` sh
# Return to home project directory
cd ~/Momentum

# Make home directory for PX4
mkdir PX4
cd PX4

# Clone PX4
git clone https://github.com/PX4/PX4-Autopilot.git --recursive

# Get into the PX4 project directory
cd PX4-Autopilot

# Run installer script
bash ./Tools/setup/ubuntu.sh

#
# Log out and log back in.
#
```

Finally, follow [these instructions](https://gazebosim.org/tutorials?tut=install_ubuntu) to update Gazebo to the first-party sources.  Use the "Alternative Installation: Step by Step" instructions.  *(Note that this step may be removed if ubuntu.sh is updated to install a compatible version of Gazebo.)*

### 3.2. Build PX4

Summary of [PX4 simulation with Gazebo](https://dev.px4.io/master/en/simulation/gazebo.html):

``` sh
# Get into the PX4 project directory
cd ~/Momentum/PX4/PX4-Autopilot

# Make the project with default drone target and gazebo simulation target
make px4_sitl gazebo
```

Take note:

- IP-address on the line that looks like `[Msg] Publicized address: 192.168.0.10` will be useful if PX4 can't connect to QGroundControl when running Gazebo.
- IP-address on the line that looks like `[Msg] Connected to gazebo master @ http://127.0.0.1:11345` will be useful when setting up py3gazebo.

## 4. OPTIONAL Install QGroundControl

QGroundControl can be seen as a companion application to PX4. It provides a GUI interface for some of the most commonly used parameters in PX4. It also provides a contextualized view of the running mission. This software is not necessary to complete the project, but it may be useful for debugging.

Summary of [QGRoundControl installation instructions](https://docs.qgroundcontrol.com/master/en/getting_started/download_and_install.html):

``` sh
# Give yourself permissions to use the serial port
sudo usermod -a -G dialout $USER

# Remove modemmanager
sudo apt-get remove modemmanager -y

# Install dependencies
sudo apt install gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl -y

#
# Log out and log back in.
#

# Return to home
cd ~/Momentum

# Download QGroundControl app image
wget https://s3-us-west-2.amazonaws.com/qgroundcontrol/latest/QGroundControl.AppImage

# Add execution permissions to the downloaded file
chmod +x ./QGroundControl.AppImage

# Launch app
./QGroundControl.AppImage # (or double-click)
```

### 4.1. Fix problem where PX4 running Gazebo can't connect to QGroundControl

Summary of [forum post solving this issue](https://discuss.px4.io/t/how-to-make-qgcontrol-connect-to-gazebo-simulation-instance-in-another-host-in-same-lan/9941):

``` sh
# Get into the PX4 project directory
cd ~/Momentum/PX4/PX4-Autopilot

# Edit the startup script
gedit ROMFS/px4fmu_common/init.d-posix/rcS 
```

Add the IP address you see in the console when you run `make px4_sitl gazebo` to the line `mavlink start -x -u $udp_gcs_port_local -r 4000000` using the syntax

``` sh
-t 192.168.x.y
```

e.g.

``` sh
mavlink start -x -u $udp_gcs_port_local -r 4000000 -t 192.168.0.10
```

## 5. Install MAVSDK

MAVSDK provides the Python hooks to interface with PX4. This allows the user to control the drone in a programmatic way, enabling complex missions and performing intricate algorithms.

Summary of [Python MAVSDK installation guide](https://github.com/mavlink/MAVSDK-Python#mavsdk-python):

``` sh
# Install MAVSDK Python library
pip3 install mavsdk
```

## 6. Install navpy and numpy

Navpy provides coordinate system conversion functions

``` sh
pip3 install numpy
pip3 install navpy
```

## 7. Download py3gazebo

Similar to MAVSDK, py3gazebo provides Python hooks to interface with Gazebo and its messages. This software is necessary in this project to read sensor data from Gazebo.

``` sh
# Step into project home directory
cd ~/Momentum

# Clone py3gazebo from GitHub and cd into the folder
git clone https://github.com/wil3/py3gazebo.git
cd py3gazebo

# Run 2to3 on the project
sudo apt-get install 2to3
2to3 -w *.py

# Replace all instances of deprecated `asyncio.async` with `asyncio.ensure_future`
sudo find ./ -type f -exec sed -i 's/asyncio.async/asyncio.ensure_future/g' {} \;

# Update proto definitions from the root of the py3gazebo project
export GAZEBO_HOME=/usr/include/gazebo-11
protoc --proto_path=$GAZEBO_HOME/gazebo/msgs --python_out=pygazebo/msg $GAZEBO_HOME/gazebo/msgs/*proto
```

The Python library is not yet installed. LM is providing an updated `setup.py` script that will be copied in the next step and there will be a prompt to install the library in [section 8](#8-install-py3gazebo).

## 8. Adding LM-provided LiDAR and terrain

Based on this [forum post](https://discuss.px4.io/t/create-custom-model-for-sitl/6700/2).

1. Download the LM provided assets from [this repository](https://github.com/katabeta/lm-mit-momentum) and place parallel to your PX4 top folder

    ``` sh
    # Get into the project directory
    cd ~/Momentum

    # Clone project
    git clone https://github.com/katabeta/lm-mit-momentum.git

    # Check directory tree
    sudo apt-get install tree
    tree -L 2
    ```

   - After downloading, your workspace directory should look like this (*otherwise the script will fail*):

        ``` tree
        .
         ├── lm-mit-momentum
         │   ├── ...
         ├── PX4
         │   └── PX4-Autopilot
         ├── py3gazebo
         │   └── ...
         └── ...
        ```

2. Run the bash script in the downloaded folder

    ``` sh
    # Step into the lm directory
    cd lm-mit-momentum

    # Add execution permissions to the script and execute
    chmod +x lm_setup.sh
    sudo ./lm_setup.sh
    ```

   - If you see the following printed to the terminal and no error messages, the script has succeded:

      ``` sh
      gazebo_iris_lmlidar__terrain2d
      gazebo_iris_lmlidar__terrain3d
      ```

### 8.1. Creating your own terrain and LiDAR

You should **not** need to create your own terrain or LiDAR for this project. If you are still looking for instruction on making your own assets, refer to [making_terrain_lidar.md](https://github.com/katabeta/lm-mit-momentum/blob/master/making_terrain_lidar.md).

## 9. Install py3gazebo

Because there were specific changes required, the `lm_setup.sh` script had to copy a file over before you could install the library. To install the library, do the following:

``` sh
# Step into the py3gazebo folder
cd ~/Momentum/py3gazebo

# Install the Python library
pip3 install .
```

## 10. Launch simulation

### 10.1. Set home position

Setting the home position will ensure that Gazebo, PX4, and the Python mission are on the same page about where the drone is supposed to be.

``` sh
# Get into the PX4 project folder
cd ~/Momentum/PX4/PX4-Autopilot

# Source home position
source set_home.sh

# or do this from anywhere by hand
# https://dev.px4.io/master/en/simulation/gazebo.html#set-custom-takeoff-location
export PX4_HOME_LAT=0 # Deg
export PX4_HOME_LON=0 # Deg
export PX4_HOME_ALT=0 # Meters
```

### 10.2. Launch PX4 with Gazebo

Summary of [PX4 simulation using Gazebo](https://dev.px4.io/master/en/simulation/gazebo.html):

Launching PX4 and Gazebo (the `make...` command) will start the real-time simulation. From here, you can interact with the drone, send missions, move it in the world, and peek at the messages sent in and out of Gazebo.

```sh
# Get into the PX4 project folder
cd ~/Momentum/PX4/PX4-Autopilot

# Launch PX4 and Gazebo with the lidar and 2D terrain
make px4_sitl gazebo___terrain2d
```

### 10.3. Set PX4 firmware parameters

The PX4 firmware parameters set the constants used in the control laws of the autopilot. The following shows how to set the maximum velocities for the drone and load/save these parameters to file, as well as reset them to defaults.

``` sh
# Run from the shell (with pxh>) after launching PX4
# Set params manually
# https://dev.px4.io/master/en/advanced/parameter_reference.html
param set MPC_Z_VEL_MAX_DN 1.0 # m/s, max vertical velocity down
param set MPC_Z_VEL_MAX_UP 3.0 # m/s, max vertical velocity up
param set MPC_XY_VEL_MAX  12.0 # m/s, max horizontal velocity

# Or load from file (root location /PX4-Autopilot/build/px4_sitl_default/tmp/rootfs)
param load iris_defaults # Reset the parameters to when file was saved
param save # Optionally save params (not done automatically with load)

# Reset all params to default
param reset_all
```

### 10.4. How to find sensor topic name, message type, and get sample output

The following commands only work with Gazebo running and drone spawned in the simulation.

Get a list of all gazebo topics, filter for the word `scan`

``` sh
gz topic -l | grep scan
# /gazebo/default/iris_lmlidar/lmlidar/link/lmlidar/scan
```

Get the details on the lidar topic specifically

``` sh
gz topic -i /gazebo/default/iris_lmlidar/lmlidar/link/lmlidar/scan
# Type: gazebo.msgs.LaserScanStamped
# 
# Publishers:
#   192.168.0.10:43455
# 
# Subscribers:
#   192.168.0.10:46127
```

Echo the topic to the terminal - this will spam to your terminal, so press `Ctrl+C` to stop.

``` sh
gz topic -e /gazebo/default/iris_lmlidar/lmlidar/link/lmlidar/scan
# time {
#   sec: 12
#   nsec: 404000000
# }
# scan {
#   frame: "iris_lmlidar::lmlidar::link"
#   world_pose {
#     position {
#       x: 1.1076721818607924
#       y: 0.97990294068076067
#       z: -3.0112717917544356
#     }
#     orientation {
#       x: -9.72964361274114e-05
#       y: -0.0223892966197638
#       z: 0.000623484894630627
#       w: 0.99974912913033442
#     }
#   }
#   angle_min: -0.5236
#   angle_max: 0.5236
#   angle_step: 0.055115789473684208
#   range_min: 0.2
#   range_max: 10
#   count: 20
#   vertical_angle_min: -1.57
#   vertical_angle_max: 0
#   vertical_angle_step: 0.19625
#   vertical_count: 9
#   ranges: 0.34457796070222135
#   ...
#   ranges: 0.57489344102911
#   intensities: 0
#   ...
#   intensities: 0
# }

```

### 10.5. OPTIONAL Launch QGroundControl

Summary of [QGRoundControl installation instructions](https://docs.qgroundcontrol.com/master/en/getting_started/download_and_install.html):

``` sh
# Get into the project home directory
cd ~/Momentum/

# Launch QGroundControl
./QGroundControl.AppImage # (or double-click)
```

## 11. Run a mission file

``` sh
# Get into the folder with the mission file
cd ~/Momentum/lm-mit-momentum/tutorial/demos

# Run mission file
python3 demo_mission.py
```

## 12. Query sensor values using py3gazebo - GPS Example

Get the available Gazebo topics and get the information on the topic of interest (take note of the message type). Gazebo and PX4 have to be running for this to work.

``` sh
gz topic -l | grep gps
# /gazebo/default/iris_lmlidar/gps0/link/gps

gz topic -i /gazebo/default/iris_lmlidar/gps0/link/gps
# Type: gazebo.msgs.GPS
# 
# Publishers:
#   192.168.0.10:45247
# 
# Subscribers:
```

Create a message subscriber class with a message callback and a way to poll the data when needed. Get your Gazebo Master IP-Address and Port from the following message when launching PX4 `[Msg] Connected to gazebo master @ http://127.0.0.1:11345`. The following is the same as in the file [demo_gps_read.py](https://github.com/katabeta/lm-mit-momentum/blob/master/demos/demo_gps_read.py).

``` python
import time # For the example only
import asyncio
import pygazebo

# What you import here depends on the message type you are subscribing to
import pygazebo.msg.v11.gps_pb2



# This is the gazebo master from PX4 message
# `[Msg] Connected to gazebo master @ http://127.0.0.1:11345`
HOST, PORT = "127.0.0.1", 11345


class GazeboMessageSubscriber: 

    def __init__(self, host, port, timeout=30):
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.running = False
        self.timeout = timeout

    async def connect(self):
        connected = False
        for i in range(self.timeout):
            try:
                self.manager = await pygazebo.connect((self.host, self.port))
                connected = True
                break
            except Exception as e:
                print(e)
            await asyncio.sleep(1)

        if connected: 
            # info from gz topic -l, gz topic -i arg goes here
            self.gps_subscriber = self.manager.subscribe('/gazebo/default/iris_lmlidar/link/gps0',
                                                         'gazebo.msgs.GPS',
                                                         self.gps_callback)

            await self.gps_subscriber.wait_for_connection()
            self.running = True
            while self.running:
                await asyncio.sleep(0.1)
        else:
            raise Exception("Timeout connecting to Gazebo.")

    def gps_callback(self, data):
        # What *_pb2 you use here depends on the message type you are subscribing to
        self.GPS = pygazebo.msg.v11.gps_pb2.GPS()
        self.GPS.ParseFromString(data)
    
    async def get_GPS(self):
        for i in range(self.timeout):
            try:
                return self.GPS
            except Exception as e:
                # print(e)
                pass
            await asyncio.sleep(1)
    

async def run():
    gz_sub = GazeboMessageSubscriber(HOST, PORT)
    asyncio.ensure_future(gz_sub.connect())
    gps_val = await gz_sub.get_GPS()
    # Simulate doing stuff and polling for the gps values only when needed
    start = time.time()
    current_time = 0
    last_time = 0
    while (current_time < 20):
        current_time = round(time.time() - start)
        if(current_time % 5 == 0 and last_time < current_time):
            gps_val = await gz_sub.get_GPS()
            print(gps_val)
            last_time = current_time
        if(current_time % 1  == 0 and last_time < current_time):
            print(current_time)
            last_time = current_time0
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
```

## 13. Getting started with MAVSDK

Follow the [MAVSDK quickstart guide](https://mavsdk.mavlink.io/develop/en/python/quickstart.html) to get a headstart on using MAVSDK with your setup. The [API reference](http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/) is useful for understanding how the examples work and for figuring out how to write your own code.

### 13.1. Download MAVSDK examples

``` sh
# Install subversion if not already installed
sudo apt install subversion

# Get into project home directory
cd ~/Momentum

# Download MAVSDK Python examples from the GitHub repository
svn checkout https://github.com/mavlink/MAVSDK-Python/trunk/examples
```

### 13.2. Run a MAVSDK example (PX4 and Gazebo have to be running)

``` sh
# Step into the examples folder
cd ~/Momentum/examples

# Launch example mission to takeoff, hover, then land
python3 takeoff_and_land.py
```
