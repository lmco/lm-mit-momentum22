# Getting Started <!-- omit in toc -->

If you are viewing this file offline, the most up to date version of these instructions is located in the [project GitHub](https://github.com/lmco/lm-mit-momentum22).


**NOTES:**

1. Unless otherwise specified, all instructions are to be entered into the terminal in your Ubuntu installation.
2. Commands that start with `sudo` will require your user password. Using sudo invokes superuser security privileges and is akin to running an application as an administrator in Windows.
3. There is a [playlist](https://youtube.com/playlist?list=PLvn3cENh89AszwCOFpApcvQNTHO7Ap-us) showing successful execution of these commands.
4. If you have specific questions that are not answered by this document, check out the constantantly updating [Q&A](https://github.com/katabeta/lm-mit-momentum/blob/master/QA.md).

## Table of Contents <!-- omit in toc -->
<!-- TOC and section numbers automatically generated, do not manually edit -->
- [1. Install Ubuntu 20.04 LTS](#1-install-ubuntu-2004-lts)
  - [1.1. Basic steps to install Ubuntu outside of a Virtual Machine](#11-basic-steps-to-install-ubuntu-outside-of-a-virtual-machine)
  - [1.2. Basic steps to install Ubuntu inside of a Virtual Machine](#12-basic-steps-to-install-ubuntu-inside-of-a-virtual-machine)
- [2. Install VS Code IDE](#2-install-vs-code-ide)
- [3. Get Gazebo and PX4](#3-get-gazebo-and-px4)
  - [3.1. Clone PX4 and install Gazebo9](#31-clone-px4-and-install-gazebo9)
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

## 1. Install Ubuntu 20.04 LTS

The software required for this project runs and is supported only in Ubuntu 18.04 or 20.04. As such, it is necessary to install the Ubuntu 20.04 operating system to complete the project.

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

## 3. Get PX4

PX4 is industry-standard autopilot software for hobbyist drone applications. It provides easy access to high quality control laws for a variety of drones, including in simulation. For the purposes of this project, this software will allow the user to simply set waypoints, while the PX4 software performs all of the necessary calculations to control and interface with the motors to get the drone to the next waypoint.

### 3.1. Clone PX4

``` sh
# Return to home project directory
cd ~/Momentum

# Install GIT. Git is a free and open source version control system designed for storing/collaborating on files and projects.
# Many open-source software packages can be obtained via GIT. Project Momentum files are also stored using GIT.
sudo apt install git

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

### 3.2. Build PX4

Summary of [PX4 simulation with Gazebo](https://dev.px4.io/master/en/simulation/gazebo.html):

``` sh
# Get into the PX4 project directory
cd ~/Momentum/PX4/PX4-Autopilot

# Make the project with default drone target and gazebo simulation target
HEADLESS=1 make px4_sitl jmavsim
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

### 4.1. Fix problem where PX4 can't connect to QGroundControl

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
### 10.2. Launch Everything and Write an Autopilot Script

TODO - discuss launching the sim, visualizer, and student's main script

