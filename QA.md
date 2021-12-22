# Common Questions & Answers<!-- omit in toc -->

- [How long are the missions?](#how-long-are-the-missions)
- [How far away will the drone see the survivors/water/fire?](#how-far-away-will-the-drone-see-the-survivorswaterfire)
- [Will I have access to the locations and statuses of the survivors/fires/water?](#will-i-have-access-to-the-locations-and-statuses-of-the-survivorsfireswater)
- [How quickly does the drone climb/descend/move laterally?](#how-quickly-does-the-drone-climbdescendmove-laterally)
- [How big are the maps?](#how-big-are-the-maps)
- [How will the competition maps be provided?](#how-will-the-competition-maps-be-provided)
- [How can I make a suggestion for design or functionality improvements?](#how-can-i-make-a-suggestion-for-design-or-functionality-improvements)
- [Who are the Lockheed Martin points of contact and how can I get in touch with them?](#who-are-the-lockheed-martin-points-of-contact-and-how-can-i-get-in-touch-with-them)

## How long are the missions?

10 minutes

## How far away will the drone see the survivors/water/fire?

- Survivors: 31 meters away
- Fire/water: 5 meters away

## Will I have access to the locations and statuses of the survivors/fires/water?

- Fire Suppression (same for practice and competition):
  - Fire statuses: Not programmatically, but these metrics are available via the Visualizer tables.
  - Fire locations: Map records contain fire locations in the `data_fs` field (see [maps/boston_fire.json](https://github.com/lmco/lm-mit-momentum22/blob/main/maps/boston_fire.json#L16) for example). These locations are also viewable via the Visualizer tables.
  - Water status: same as fire statuses.
  - Water locations: [waterbodies.geojson](https://github.com/lmco/lm-mit-momentum22/blob/main/data/waterbodies.geojson) specifies water and land geometries.
- Search and Rescue
  - Practice maps
    - Survivor statuses: Not programmatically, but these metrics are available via the Visualizer tables.
    - Survivor locations: Map records contain survivor locations in the `data_snr` field (see [maps/boston_sar.json](https://github.com/lmco/lm-mit-momentum22/blob/main/maps/boston_sar.json#L20) for example). These locations are also viewable via the Visualizer tables.
  - Competition map
    - Survivor statuses: The total number of survivors and how many have been discovered is viewable via the Visualizer tables only.
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

## How can I make a suggestion for design or functionality improvements?

Reach out to the [Lockheed Martin points of contact](#who-are-the-lockheed-martin-points-of-contact-and-how-can-i-get-in-touch-with-them) on Slack with your suggestions.

## Who are the Lockheed Martin points of contact and how can I get in touch with them?

Reach out to any of the following people via Slack:

- Andrew Fabian
- Irina Lavryonova
- Michael Nothem
- Stephen Kubik
