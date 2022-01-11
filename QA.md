# Common Questions & Answers<!-- omit in toc -->

- [What are the missions?](#what-are-the-missions)
- [How long are the missions?](#how-long-are-the-missions)
- [How far away will the drone see the survivors/water/fire?](#how-far-away-will-the-drone-see-the-survivorswaterfire)
- [How much water will the fire suppression mission have?](#how-much-water-will-the-fire-suppression-mission-have)
- [Will I have access to the locations and statuses of the survivors/fires/water?](#will-i-have-access-to-the-locations-and-statuses-of-the-survivorsfireswater)
- [How quickly does the drone climb/descend/move laterally?](#how-quickly-does-the-drone-climbdescendmove-laterally)
- [How big are the maps?](#how-big-are-the-maps)
- [How will the competition maps be provided?](#how-will-the-competition-maps-be-provided)
- [Can I use an outside library to accomplish the mission?](#can-i-use-an-outside-library-to-accomplish-the-mission)
- [My drone doesn't move when I start the simulation using the instructions. What do I do?](#my-drone-doesnt-move-when-i-start-the-simulation-using-the-instructions-what-do-i-do)
- [I borrowed a laptop and my project folder is out of date. How do I update it?](#i-borrowed-a-laptop-and-my-project-folder-is-out-of-date-how-do-i-update-it)
- [How can I make a suggestion for design or functionality improvements?](#how-can-i-make-a-suggestion-for-design-or-functionality-improvements)
- [Who are the Lockheed Martin points of contact and how can I get in touch with them?](#who-are-the-lockheed-martin-points-of-contact-and-how-can-i-get-in-touch-with-them)

## What are the missions?

- Fire/water: Put out as much of the fire as you can, as fast as you can
  - You will be given a map with clearly defined land/water boundaries and KNOWN fire locations
  - Fires are stationary and do not move over time
  - Pick up water by flying over water (no need to stop or hover)
  - Put out fire by flying over fire
  - Choose the most efficient sequencing/routing to fight the most fires as quickly as possible
  - Mission complete when you are confident that the fires have been extinguished, or you run out of time (10 mins)

- Search and Rescue: search as much of the water area as you can, as fast as you can
  - You will be given a map with clearly defined land/water boundaries but UNKNOWN number of survivors in UNKNOWN locations
  - Survivors are stationary and do not move over time
  - Find survivors by flying within 31m of them
  - No rescue required - your vehicle is just the "spotter"
  - Choose the most efficient routing to search the most area as quickly as possible.
  - You may use any search pattern, including pre-established patterns or those of your own design
  - Mission complete when you are confident that you have found all the survivors (unknown number), or you run out of time (10 mins)

## How long are the missions?

10 minutes

## How far away will the drone see the survivors/water/fire?

- Survivors: 31 meters away
- Fire/water: 5 meters away

## How much water will the fire suppression mission have?

The drone can take up and deposit up to 60 seconds worth of water (it takes the same amount of time to take up water as it does to deposit it).

## Will I have access to the locations and statuses of the survivors/fires/water?

- Fire Suppression (same for practice and competition):
  - Fire statuses: Not programmatically, but these metrics are available via the Visualizer tables.
  - Fire locations: Map records contain fire locations in the `data_fs` field (see [maps/boston_fire.json](https://github.com/lmco/lm-mit-momentum22/blob/main/maps/boston_fire.json#L16) for example). These locations are also viewable via the Visualizer tables. Upcoming: near real-time locations will be available programmatically via a connection to the visualizer.
  - Water status: same as fire statuses.
  - Water locations: [waterbodies.geojson](https://github.com/lmco/lm-mit-momentum22/blob/main/data/waterbodies.geojson) specifies water and land geometries.
- Search and Rescue
  - Water locations: [waterbodies.geojson](https://github.com/lmco/lm-mit-momentum22/blob/main/data/waterbodies.geojson) specifies water and land geometries.
  - Practice maps
    - Survivor statuses: Not programmatically, but these metrics are available via the Visualizer tables. Upcoming: a near real-time count of found survivors will be available programmatically via a connection to the visualizer.
    - Survivor locations: Map records contain survivor locations in the `data_snr` field (see [maps/boston_sar.json](https://github.com/lmco/lm-mit-momentum22/blob/main/maps/boston_sar.json#L20) for example). These locations are also viewable via the Visualizer tables.
  - Competition map
    - Survivor statuses: The total number of survivors and how many have been discovered is viewable via the Visualizer tables only. Upcoming: a near real-time count of found survivors will be available programmatically via a connection to the visualizer.
    - Survivor locations: No access to any locations for competition maps (neither programmatically nor via Visualizer tables).

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

## How big are the maps?

Maps are 16:9 aspect ratio with latitudinal dimension of 0.003 degrees.

## How will the competition maps be provided?

The competition maps will be pushed to this GitHub repository a few days before the due date (actual date TBD). The competition map will be in binary format for the Search and Rescue mission and JSON for the Fire Suppression mission.

## Can I use an outside library to accomplish the mission?

Yes, you may use additional libraries. This includes libraries included with Python as well as those available via `pip`. Staff will run your scripts at the end of the competition and will make their best efforts to install your dependencies.

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
