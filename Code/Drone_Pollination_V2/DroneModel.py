import math
import numpy as np

# This class provides a model of an individual drone within a swarm
class DroneModel: 
    flowerDict = {}
    def __init__ (self, droneId, swarmModel, initPos, fieldModel, refreshRate, 
                  initVelocity=np.array([0,5.0]), effectRadius=2,
                  cameraRadius=3, maxSpeed=5.0, safeDistance=3,
                  reductionTime=.5):
        
        self.droneId = droneId
        self.swarmModel = swarmModel
        self.pos = initPos
        self.vel = initVelocity/refreshRate
        self.effectRadius = effectRadius
        self.cameraRadius = cameraRadius
        self.refreshRate = float(refreshRate)
        self.fieldModel = fieldModel
        self.maxSpeed = maxSpeed
        self.safeDistance = safeDistance
        self.totalWeight = 0
        self.reductionTime = reductionTime
        self.reductionFrames = 0
    
    def getVecMag(self, vec):
        return np.sqrt(np.sum(np.multiply(vec,vec)))
    
    def getWeights(self, flowers):
        times = self.swarmModel.getTimes(flowers)
        return np.array([max(self.fieldModel.pollinationTime - time, 0) for time in times])
    
    def advanceOneFrame(self, averageWeightedPos, externalWeightInfluence):
        cameraFlowers = self.getFlowersInRadius(self.cameraRadius)
        effectedFlowers = self.getFlowersInRadius(self.effectRadius)
        # Update the flower dictionary to see how long each flower has been blown on
        self.swarmModel.updateFlowerDict(effectedFlowers, cameraFlowers)

        camWeights = self.getWeights(cameraFlowers)
        effWeights = self.getWeights(effectedFlowers)

        self.totalWeight = np.sum(camWeights)

        if self.reductionFrames == 0 and effectedFlowers.size > 0 \
            and self.getVecMag(self.vel) < .05 and np.sum(effWeights)/effectedFlowers.size < .05:
                self.reductionFrames = self.reductionTime * self.refreshRate
        
        if self.reductionFrames > 0:
            self.determineVelocity(effectedFlowers, effWeights, averageWeightedPos, externalWeightInfluence)
            self.reductionFrames -= 1
        else:
            self.determineVelocity(cameraFlowers, camWeights, averageWeightedPos, externalWeightInfluence)
        
        self.updatePosition()

    def getFlowersInRadius(self, radius):
        # try:
        return self.fieldModel.getFlowersWithinRadius(self.pos, radius)
        # except:
        #     print("NAN error occurred")
        return np.empty(0)
    
    def collisionAvoidanceVelocityInfluence(self):
        for drone in self.swarmModel.drones:
            if drone.droneId != self.droneId:
                vectorFromSelf2Drone = self.pos - drone.pos
                distance = np.sum(np.multiply(vectorFromSelf2Drone, vectorFromSelf2Drone))
                if distance < self.safeDistance:
                    self.vel = vectorFromSelf2Drone/distance
                    print("imminent collision avoided, drone distance is " + str(distance))
                elif distance < self.safeDistance * 4:
                    self.vel = self.vel + vectorFromSelf2Drone/distance
        
    def PSOVelocityInfluence(self, averageWeightedPos, externalWeightInfluence):
        if averageWeightedPos[0] != -1:
            PSOVel = np.array(averageWeightedPos) - self.pos
            self.vel = self.vel * (1 - externalWeightInfluence) + PSOVel * externalWeightInfluence
        
    def determineVelocity(self, flowers, weights, averageWeightedPos, externalWeightInfluence):
        if np.sum(weights) == 0:
            self.PSOVelocityInfluence(averageWeightedPos, externalWeightInfluence)
        else:
            currentMean = np.sum(np.multiply(flowers, weights.reshape((weights.size,1))), axis=0)/np.sum(weights)
            self.vel = currentMean - self.pos
            self.PSOVelocityInfluence(averageWeightedPos, externalWeightInfluence)
        self.collisionAvoidanceVelocityInfluence()
        magnitude = self.getVecMag(self.vel)
        if magnitude == 0 or math.isnan(self.vel[0]) or math.isnan(self.vel[1]):
            # velocity = np.array([0, self.maxSpeed/self.refreshRate])
            return
        elif(flowers.size > 0):
            if  magnitude < .5 and np.sum(weights)/flowers.size < .05:
                self.vel = self.maxSpeed/self.refreshRate * (self.vel/magnitude)
            
        if  magnitude > self.maxSpeed/self.refreshRate:
            self.vel = self.maxSpeed/self.refreshRate * (self.vel/magnitude)

    def updatePosition(self):
        newPos = self.pos + self.vel 
        if(newPos[0] < 0 or newPos[0] > self.fieldModel.width):
            self.vel[0] = -self.vel[0]
        if(newPos[1] < 0 or newPos[0] > self.fieldModel.length):
            self.vel[1] = -self.vel[1]
        self.pos = self.pos + self.vel 
