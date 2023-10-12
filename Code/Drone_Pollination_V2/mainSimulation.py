import matplotlib.pyplot as plt
import numpy as np
from FieldModel import FieldModel
from SwarmModel import SwarmModel
from DroneModel import DroneModel
from matplotlib.animation import FuncAnimation

# This is the refresh rate for the animation and also how frequently the drones
# update their information
refreshRate = 50.0 # in Hz or fps

# How long in total a run of the drone swarm should last
time = 5.0 # in minutes

# The number of times the swarm runs a pollination route over the field
generations = 5 # In years

# The size of the field is assumed to alwasy be square
fieldSize = 100 # In meters

# Create the models of our real-life analogous things
fieldModel = FieldModel(fieldSize)
flowers = fieldModel.getFlowers()
DroneModel.flowerDict = {}

PSOweights = np.linspace(-12, -1, 12, endpoint=True)
print(PSOweights)
PSOweights = np.power(10.0, PSOweights)
PSOweights = np.insert(PSOweights, 0, 0, axis=0)

possiblePollinationWeight = np.shape(flowers)[0] * 5.0

pollinationPercentages = []

for PSOweight in PSOweights:
    swarmModel = SwarmModel(fieldModel, refreshRate, time, generations, swarmSize=100, externalWeightInfluence=PSOweight)
    swarmModel.runSimulation()
    values = np.fromiter(DroneModel.flowerDict.values(), dtype=float)
    values[values > 5.0] = 5.0
    amountPollinated = np.sum(values)
    print("For a PSO weight of " + str(PSOweight) + ", the pollination weight was " + str(amountPollinated) + " of a possible " + str(possiblePollinationWeight))
    pollinationPercentages.append(amountPollinated/possiblePollinationWeight*100)
    DroneModel.flowerDict = {}

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.scatter(PSOweights, pollinationPercentages)

ax.set_title("Average Pollination Percentage vs Alpha Values for a Field Size of 1 KM")
ax.set_ylabel("Average Pollination Percentage")
ax.set_xlabel("Alpha Value")

ax.set_xscale('log')

plt.show()

swarmModel.runSimulation()