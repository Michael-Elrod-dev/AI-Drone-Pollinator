import time
import numpy as np
import matplotlib.pyplot as plt
from FieldModel import FieldModel
from SwarmModel import SwarmModel
from DroneModel import DroneModel
from matplotlib.animation import FuncAnimation

# This is the refresh rate for the animation and also how frequently the drones
# update their information
refreshRate = 50.0 # in Hz or fps
start_time = time.time()

# How long in total a run of the drone swarm should last
time_duration = 5.0 # in minutes

# The number of times the swarm runs a pollination route over the field
generations = 5 # In years

# The size of the field is assumed to alwasy be square
fieldSize = 100 # In meters

# Create the models of our real-life analogous things
fieldModel = FieldModel(fieldSize)
swarmModel = SwarmModel(fieldModel, refreshRate, time_duration, generations, swarmSize=10) # the number of drones in the swarm
flowers = fieldModel.getFlowers()

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(6,6)

# Updates the list of flowers that have been affected by the drones
def updateEffectedFlowers():
    effectedFlowers = []
    times = []

    for flower in flowers:
        if flower.tobytes() in swarmModel.flowerDict:
            effectedFlowers.append(flower)

    effectedFlowers = np.array(effectedFlowers)
    times = [swarmModel.flowerDict[effectedFlower.tobytes()] for effectedFlower in effectedFlowers]
    
    return effectedFlowers, times

def animate(i):
    ax.clear()
    elapsed_time = time.time() - start_time
    ax.set_title("Time elapsed: {:.2f} seconds | Frames processed: {}".format(elapsed_time, i))
    #ax.set_title("Time elapsed: " + "{:.2f}".format(float(i)/refreshRate))
    effectedFlowers, times = updateEffectedFlowers()
    ax.scatter(flowers[:, 0], flowers[:, 1], marker=".", c="b")
    dronePositions = swarmModel.getDronePositions()
    droneVelocities, velMagnitudes = swarmModel.getDroneVelocities()
    try:
        ax.scatter(effectedFlowers[:, 0], effectedFlowers[:, 1], marker=".", 
        c=times, cmap="viridis", vmin=0, vmax=5)
    except:
        pass
    # Plot vectors representing the velocities of the drones
    ax.quiver(dronePositions[:, 0], dronePositions[:, 1], droneVelocities[:, 0],
               droneVelocities[:, 1], color='r', units='xy', scale=.02)

    for drone, dronePosition in zip(swarmModel.drones, dronePositions):
        inner_circle = plt.Circle(dronePosition, drone.effectRadius, fill = False)
        outer_circle = plt.Circle(dronePosition, drone.cameraRadius, fill = False)

        ax.add_artist(inner_circle)
        ax.add_artist(outer_circle)

    swarmModel.advanceOneFrame()

    # Set the x and y axis to display a fixed range
    ax.set_xlim([0, fieldSize])
    ax.set_ylim([0, fieldSize])

ani = FuncAnimation(fig, animate, frames=int(time_duration*refreshRate*60),
                    interval=int(1000/refreshRate), repeat=False)

plt.show()
plt.close()