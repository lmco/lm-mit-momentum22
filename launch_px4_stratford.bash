cd ~/Momentum/PX4/PX4-Autopilot/
export PX4_HOME_LAT=41.15
export PX4_HOME_LON=-75.14
HEADLESS=1 make px4_sitl gazebo
sleep 5
param set MPC_Z_VEL_MAX_DN 1.0
param set MPC_Z_VEL_MAX_UP 3.0
param set MPC_XY_VEL_MAX 12