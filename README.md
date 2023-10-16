# AI Drone Pollinator
![Animation](https://github.com/Michael-Elrod-dev/Drone-Pollination/blob/main/Assets/Example.png)

This project simulates a swarm of drones navigating a field to pollinate flowers. The visualization provides insights into the movement patterns of drones and their interactions with the flower clusters.

## Tech Stack
- **Language**: Python
- **Visualization**: Matplotlib
- **Machine Learning**: scikit-learn

## Directory Structure

- `mainAnimation.py`: Main script that sets up and runs the animation.
- `FieldModel.py`: Contains the `FieldModel` class that represents the field with flowers.
- `SwarmModel.py`: Contains the `SwarmModel` class that represents the swarm of drones.
- `DroneModel.py`: Contains the `DroneModel` class that represents an individual drone.

## Setup and Execution

1. Ensure you have the required libraries installed:
    ```bash
    pip install matplotlib numpy scikit-learn
    ```
2. Navigate to the project directory and run:
    ```bash
    python mainAnimation.py
    ```

## Visualization

The simulation shows drones (represented with velocity vectors) navigating the field to pollinate flower clusters. Flowers affected by drones change color based on the duration of interaction. The simulation provides insights into how drones collectively navigate and cover the entire field.

