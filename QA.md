# Frequent Questions & Answers<!-- omit in toc -->

- [How do I get started with the competition files?](#how-do-i-get-started-with-the-competition-files)
- [How do I record my screen in Ubuntu?](#how-do-i-record-my-screen-in-ubuntu)
- [What are the missions?](#what-are-the-missions)
  - [Fire Suppression](#fire-suppression)
  - [Search and Rescue](#search-and-rescue)
- [How long are the missions?](#how-long-are-the-missions)
- [How far away will the drone see the survivors/water/fire?](#how-far-away-will-the-drone-see-the-survivorswaterfire)
- [How much water will the fire suppression mission have?](#how-much-water-will-the-fire-suppression-mission-have)
- [How much water does it take to extinguish a fire?](#how-much-water-does-it-take-to-extinguish-a-fire)
- [When will the drone start dropping the water?](#when-will-the-drone-start-dropping-the-water)
- [Will I have access to the locations and statuses of the survivors/fires/water?](#will-i-have-access-to-the-locations-and-statuses-of-the-survivorsfireswater)
  - [Fire Suppression (same for practice and competition)](#fire-suppression-same-for-practice-and-competition)
  - [Search and Rescue](#search-and-rescue-1)
- [Where will the drone start the mission?](#where-will-the-drone-start-the-mission)
- [I am launching a map, but the drone gets initialized somewhere else (e.g. map is in Nantucket, but the drone is in Boston). Is this a bug?](#i-am-launching-a-map-but-the-drone-gets-initialized-somewhere-else-eg-map-is-in-nantucket-but-the-drone-is-in-boston-is-this-a-bug)
- [How quickly does the drone climb/descend/move laterally?](#how-quickly-does-the-drone-climbdescendmove-laterally)
- [Can I increase the simulation rate?](#can-i-increase-the-simulation-rate)
- [How big are the maps?](#how-big-are-the-maps)
- [How will the competition maps be provided?](#how-will-the-competition-maps-be-provided)
- [Can I use an outside library to accomplish the mission?](#can-i-use-an-outside-library-to-accomplish-the-mission)
- [My drone doesn't move when I start the simulation using the instructions. What do I do?](#my-drone-doesnt-move-when-i-start-the-simulation-using-the-instructions-what-do-i-do)
- [I borrowed a laptop and my project folder is out of date. How do I update it?](#i-borrowed-a-laptop-and-my-project-folder-is-out-of-date-how-do-i-update-it)
- [How can I make a suggestion for design or functionality improvements?](#how-can-i-make-a-suggestion-for-design-or-functionality-improvements)
- [Who are the Lockheed Martin points of contact and how can I get in touch with them?](#who-are-the-lockheed-martin-points-of-contact-and-how-can-i-get-in-touch-with-them)

## How do I get started with the competition files?

1. Update your local version of the repository by pulling in updates.

   ``` sh
   # Change directory to the the local copy of the repository
   cd ~/Momentum/lm-mit-momentum22/
   # Pull latest changes from the remote repository
   git pull
   ```

2. Ensure that the following commands succeed.

   ``` sh
   # Call the command to print the contents of a file, 
   # but redirect the output to a null device to keep our terminal clutter-free.
   # If the command fails, it will print out the error to the console. 
   # If it succeeds, it will simply return without any output.
   cat ~/Momentum/lm-mit-momentum22/launch_px4_Fire_Competition.bash > /dev/null
   cat ~/Momentum/lm-mit-momentum22/launch_px4_SAR_Competition.bash > /dev/null
   cat ~/Momentum/lm-mit-momentum22/maps/Fire_Competition.json > /dev/null
   cat ~/Momentum/lm-mit-momentum22/maps/SAR_Competition.json > /dev/null
   ```

   > If you get `cat: /home/<username>/Momentum/lm-mit-momentum22/<file>: No such file or directory`, you need to return to step 1. If it still doesn't work, you need to back up your changes, delete the local repository directory, reclone the repository from the remote, and apply your changes from backup.

3. Launch the simulation using the correct map and bash script (each code block goes into a new terminal window)

   a. Fire Suppression

      ``` sh
      # Get into the Momentum22 project folder
      cd ~/Momentum/lm-mit-momentum22

      # Launch PX4 with the jMavSim simulation target and set the starting location to Fire Competition
      bash launch_px4_Fire_Competition.bash
      ```

      ``` sh
      # Get into the Momentum22 project folder
      cd ~/Momentum/lm-mit-momentum22

      # Launch Visualizer with the Fire Competition map
      bokeh serve Visualizer --show --args -v Fire_Competition
      ```

      ``` sh
      # Get into the Momentum22 project folder
      cd ~/Momentum/lm-mit-momentum22

      # Launch Student code (replace <name of your script> with the name of the file where you have your solution)
      python3 student/<name of your script>.py 
      ```

   b. Search and Rescue

      ``` sh
      # Get into the Momentum22 project folder
      cd ~/Momentum/lm-mit-momentum22

      # Launch PX4 with the jMavSim simulation target and set the starting location to SAR Competition
      bash launch_px4_SAR_Competition.bash
      ```

      ``` sh
      # Get into the Momentum22 project folder
      cd ~/Momentum/lm-mit-momentum22

      # Launch Visualizer with the SAR Competition map
      bokeh serve Visualizer --show --args -v SAR_Competition
      ```

      ``` sh
      # Get into the Momentum22 project folder
      cd ~/Momentum/lm-mit-momentum22

      # Launch Student code (replace <name of your script> with the name of the file where you have your solution)
      python3 student/<name of your script>.py 
      ```
  
4. After dry-running your solution against the competition map and when you feel comfortable with your solution, please [record your screen](#how-do-i-record-my-screen-in-ubuntu) with a live run of your solution. When recording, ensure to
   - Run your simulation at 1x speed
   - Capture the takeoff and the end of the mission - your video should be at least 10 mins long

    >You may tweak your solution and try as many times before recording as you feel necessary, you only need to submit your best run to us.

5. Upload your recording to YouTube and include a link to the video with your submission.
6. Assemble your submission email. It shall include:
   - Your Python code
   - A list of all of your dependencies and their version numbers
   - A link to the YouTube video you uploaded in step 5
7. Send your submission email to stephen.t.kubik@lmco.com.

## How do I record my screen in Ubuntu?

Before your first recording, increase the screen record time from default my executing the following command in a terminal: `gsettings set org.gnome.settings-daemon.plugins.media-keys max-screencast-length 1800`. This is a one-time action and you only need to do it once.

To start a recording, press `Ctrl+Shift+Alt+R`. You should see a small red circle appear in the upper right of your screen next to the volume and power controls.

To stop a recording, press the same key command (`Ctrl+Shift+Alt+R`). Depending on the length of your video, it may take a few minutes to finish encoding, but once the video is ready, it will be available in the `~/Videos` directory as `Screencast from <date> <time>.webm`.

>Ensure to capture the takeoff and the end of the mission - your video should be at least 10 mins long.

## What are the missions?

### Fire Suppression

- Put out as much of the fire as you can, as fast as you can
  - You will be given a map with clearly defined land/water boundaries and KNOWN fire locations
    - Land/water boundaries are defined in the [waterbodies.geojson](https://github.com/lmco/lm-mit-momentum22/blob/main/data/waterbodies.geojson) file
    - Fire locations are defined in the map record's `data_fs` field (check the [/maps directory](https://github.com/lmco/lm-mit-momentum22/tree/main/maps) for all of the map records)
  - Fires are stationary and do not move over time
  - You do not need to worry about any environmental conditions such as wind or air density
  - Pick up water by flying over water (no need to stop or hover)
    - Up to 60 seconds worth of water may be picked up or deposited at any one time
  - Put out fire by flying over fire
    - See for more details[How much water does it take to extinguish a fire?](#how-much-water-does-it-take-to-extinguish-a-fire)
  - Choose the most efficient sequencing/routing to fight the most fires as quickly as possible
    - The number percent of total fire area extinguished will be your score. Time with be the tie breaker for those who extinguish all fires.
  - Mission complete when you are confident that the fires have been extinguished, or you run out of time (10 mins)
    - Land to indicate that mission is complete

### Search and Rescue

- Search as much of the water area as you can, as fast as you can
  - You will be given a map with clearly defined land/water boundaries but UNKNOWN number of survivors in UNKNOWN locations
    - Land/water boundaries are defined in the [waterbodies.geojson](https://github.com/lmco/lm-mit-momentum22/blob/main/data/waterbodies.geojson) file
  - Survivors are stationary and do not move over time
  - You do not need to worry about any environmental conditions such as wind or air density
  - Find survivors by flying within 31m of them
  - No rescue required - your vehicle is just the "spotter"
  - Choose the most efficient routing to search the most area as quickly as possible.
  - You may use any search pattern, including pre-established patterns or those of your own design
  - Mission complete when you are confident that you have found all of the survivors (unknown number), or you run out of time (10 mins)
    - Land to indicate that mission is complete. Time with be the tie breaker for those who find identical numbers of survivors.

## How long are the missions?

10 minutes

## How far away will the drone see the survivors/water/fire?

- Survivors: 31 meters away
- Fire/water: 5 meters away

## How much water will the fire suppression mission have?

The drone can take up and deposit up to 60 seconds worth of water (it takes the same amount of time to take up water as it does to deposit it).

## How much water does it take to extinguish a fire?

The fire is shrunk by a factor of 0.05 of its previous area for every second that the water is deposited over the fire, but scaled by the update rate (100 Hz or once every 0.01 sec). Put another way, after 1 second of water, the fire will have `area=0.95*0.01*previous_area` executed `1/update_rate` (100) times, where `area` of the previous iteration becomes the `previous_area` of the next iteration. While not realistic, this simplifies implementation and makes big fires not as daunting to put out.

## When will the drone start dropping the water?

The water will deposit so long as the drone is at least within a 5 meter radius of a fire edge or vertex or is inside the fire polygon.

## Will I have access to the locations and statuses of the survivors/fires/water?

### Fire Suppression (same for practice and competition)

- Fire statuses: Fire area extenguished in percent is available via the visualizer and in real-time via a connection to the visualizer (see how to access programmatically in example student code)
- Fire locations:
  - Map records contain initial fire vertex locations in the `data_fs` field (see [maps/boston_fire.json](https://github.com/lmco/lm-mit-momentum22/blob/main/maps/boston_fire.json#L16) for example)
  - Fire vertex locations are viewable in real-time via the Visualizer tables
  - Fire vertex locations are available in real-time programmatically via a connection to the visualizer (see how to access programmatically in example student code)
- Water status: same as fire statuses
- Water locations: [waterbodies.geojson](https://github.com/lmco/lm-mit-momentum22/blob/main/data/waterbodies.geojson) specifies water and land geometries. See [data_maker.py](https://github.com/lmco/lm-mit-momentum22/blob/main/utils/data_maker.py) for ideas on how to start working with this file.

### Search and Rescue

- Water locations: [waterbodies.geojson](https://github.com/lmco/lm-mit-momentum22/blob/main/data/waterbodies.geojson) specifies water and land geometries. See [data_maker.py](https://github.com/lmco/lm-mit-momentum22/blob/main/utils/data_maker.py) for ideas on how to start working with this file.
- Practice maps
  - Survivor statuses:
    - Real-time count of found survivors is available via the Visualizer tables
    - Real-time count of found survivors is available programmatically via a connection to the visualizer (see how to access programmatically in example student code)
  - Survivor locations: Map records contain survivor locations in the `data_snr` field (see [maps/boston_sar.json](https://github.com/lmco/lm-mit-momentum22/blob/main/maps/boston_sar.json#L20) for example). These locations are also viewable via the Visualizer tables.
- Competition map
  - Survivor statuses: 
    - Real-time count of found survivors is available via the Visualizer tables
    - Real-time count of found survivors is available programmatically via a connection to the visualizer (see how to access programmatically in example student code)
  - Survivor locations: No access to any locations for competition maps (neither programmatically nor via Visualizer tables).

## Where will the drone start the mission?

The drone's initial position is determined by the `.bash` script we have provided you at the root of this repository. The competition drone will start on the coastline, in the vicinity of water for both mission types.

## I am launching a map, but the drone gets initialized somewhere else (e.g. map is in Nantucket, but the drone is in Boston). Is this a bug?

No, this is not a bug. You likely forgot to use the correct `.bash` launcher script. Make sure that the launcher script you're using corresponds to your map. For example, when launching the Nantucket map, you have to use the `launch_px4_nantucket.bash` launcher script.

## How quickly does the drone climb/descend/move laterally?

>Refer to [PX4 Parameter Table](https://dev.px4.io/master/en/advanced/parameter_reference.html) for the full set of parameters.

| Parameter                 | Value             | Units             | PX4 Parameter Table Name  |
|--------------             | --------------    | --------------    | --------------            |
| X/Y max velocity          | 12.0              | m/s               | MPC_XY_VEL_MAX            |
| Z up max velocity         | 3.0               | m/s               | MPC_Z_VEL_MAX_UP          |
| Z down max velocity       | 1.0               | m/s               | MPC_Z_VEL_MAX_DN          |
| X/Y max acceleration      | 5.0               | m/s/s             | MPC_ACC_HOR_MAX           |
| Z up max acceleration     | 5.0               | m/s/s             | MPC_ACC_UP_MAX            |
| Z down max acceleration   | 3.0               | m/s/s             | MPC_ACC_DOWN_MAX          |

## Can I increase the simulation rate?

Yes, you have to set the `PX4_SIM_SPEED_FACTOR` global variable to a factor greater than 1. To do this, export the variable in the same terminal window where you will launch PX4 (either manually or using one of the launcher scripts) using

``` sh
# PX4_SIM_SPEED_FACTOR < 1 is slower than real-time
# PX4_SIM_SPEED_FACTOR = 1 is real-time
# PX4_SIM_SPEED_FACTOR > 1 is faster than real-time
export PX4_SIM_SPEED_FACTOR=2
```

The exported value will be persistent so long as that particular terminal window is open. If you open a new terminal window or restart your computer/VM, you will have to export the variable value again.

>Setting this **only affects the PX4 simulation rate and does not impact the visualizer**. The rates for fire extinguishing and water uptake/deposit will remain the same, and the scoring mechanism will continue at the same rate. As such, we do not recommend going above a 5x simulation speed and **this is not a valid configuration for final submission**.

## How big are the maps?

Maps are 16:9 aspect ratio with latitudinal dimension of 0.003 degrees. You may check the exact dimensions and location of geographical bounds of a map by inspecting the `bounds` field of your map's `.json` record. You will find these map records in the [/maps directory](https://github.com/lmco/lm-mit-momentum22/tree/main/maps).

## How will the competition maps be provided?

The competition maps will be pushed to this GitHub repository a few days before the due date (21 JAN 2022, 9AM EST). The competition map will be in a combination binary and `.json` format for the Search and Rescue mission and `.json` for the Fire Suppression mission.

## Can I use an outside library to accomplish the mission?

Yes, you may use additional outside libraries. This includes libraries included with Python as well as those available via `pip`. Staff will run your scripts at the end of the competition and will make their best efforts to install your dependencies.

We just ask that you please :

- Restrict to libraries available via pip and those packaged with Python by default
- Do not install any libraries that defeat the spirit of the exercise
- Tell us whenever you decide to use a library, which library you want to use, and what purpose you want to use it for (we may veto your use if it violates point 2 above)
- Provide us with the list of your dependencies and their versions with your code submission at the end of the competition to make sure we're running what you're running

We welcome your creativity!

Libraries that have been pre-approved (either by default or by request of other students) are:

- numpy
- json
- os
- math
- navpy
- geopandas
- Shapely
- Rtree
- pathlib
- datetime
- time
- typing
- enum
- inspect
- argparse
- traceback
- multiprocessing
- queue
- collections

## My drone doesn't move when I start the simulation using the instructions. What do I do?

You likely have a new version of MavSDK. Try downgrading using:

``` sh
pip3 install --force-reinstall mavsdk==0.21.0
```

## I borrowed a laptop and my project folder is out of date. How do I update it?

>Background: These machines have been preloaded with software for the MIT Momentum 2022 challenge, as described in the documentation on [GitHub](https://github.com/lmco/lm-mit-momentum22).  However they are not configured for your personal GitHub accounts.  This means that they can’t get updated Momentum software, which will be essential during the challenge.  To fix this, we need you to create SSH keys on the laptop and save them to your personal GitHub account, linking the two.

Steps:

1. Remove any existing SSH keys by typing the following into a terminal on the laptop:

    ``` sh
    cd ~/.ssh
    rm -f id*
    ```

2. Create a new public and private key for your laptop.  First type:

    ``` sh
    ssh-keygen -t ed25519 -C your_email@example.com
    ```

    When prompted “Enter file in which to save the key”, just press Enter.
    When prompted for a passphrase, just press Enter.

3. View and copy your new public key, so that it’s in the clipboard when we visit the GitHub website.  Type:

    ``` sh
    cat ~/.ssh/id_ed25519.pub
    ```

    You should see something like:

    ``` sh
    ssh-ed25519 AAAA12345678901234567890123456789012345678901234567890 your_email@example.com
    ```

    Select this, right-click and pick “copy”.

4. Add this key to your GitHub account, by following these steps:

    - Sign in to GitHub.
    - Click on your profile icon on the top-right corner of the page.
    - Click on Settings.
    - Click on SSH and GPG Keys.
    - Click on New SSH Key or Add SSH Key.
    - Give the key a title in the title field like “Bob’s Momentum 2022 Laptop”.
    - Paste the key into the Key field.
    - Click Add SSH Key.
    - If prompted, confirm your GitHub password.

5. Test that it works, by seeing if you can update the Momentum ’22 code on your laptop.  Type:

    ``` sh
    cd ~
    cd Momentum
    cd lm-mit-momentum22
    git pull
    ```

    >At this point you should see a list of updates being applied to your laptop.  If so: success!  If not: contact us on the Slack channels to help figure out the problem.

## How can I make a suggestion for design or functionality improvements?

Reach out to the [Lockheed Martin points of contact](#who-are-the-lockheed-martin-points-of-contact-and-how-can-i-get-in-touch-with-them) on Slack with your suggestions.

## Who are the Lockheed Martin points of contact and how can I get in touch with them?

Reach out to any of the following people via Slack:

- Andrew Fabian
- Irina Lavryonova
- Michael Nothem
- Stephen Kubik
- Navid Tehrani
- Jay Thibodeau
- Rochelle Shidler
