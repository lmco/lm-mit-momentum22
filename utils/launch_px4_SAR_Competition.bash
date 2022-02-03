##################################################################
#   Copyright 2021 Lockheed Martin Corporation.                  #
#   Use of this software is subject to the BSD 3-Clause License. #
##################################################################

cd ~/Momentum/PX4/PX4-Autopilot/
export PX4_HOME_LAT=43.962
export PX4_HOME_LON=-77.325
export PX4_HOME_ALT=10
export PX4_SIM_SPEED_FACTOR=1
HEADLESS=1 make px4_sitl jmavsim
sleep 5
param set MPC_Z_VEL_MAX_DN 1.0
param set MPC_Z_VEL_MAX_UP 3.0
param set MPC_XY_VEL_MAX 12
