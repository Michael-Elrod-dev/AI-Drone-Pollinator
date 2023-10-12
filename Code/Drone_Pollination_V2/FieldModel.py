from matplotlib import image
from matplotlib import pyplot
from sklearn.datasets import make_blobs
from sklearn.neighbors import NearestNeighbors
import numpy as np
#import cv2

# This class provides model of a field with flowers distributed in clusters
class FieldModel: 
    def __init__ (self, dimension):
        self.length = dimension
        self.width = dimension
        self.numclusters = int(dimension/20)
        self.minFlowerPerClusters = 1
        self.maxFlowerPerClusters = dimension*10
        self.numflowers = np.random.randint(self.minFlowerPerClusters, self.maxFlowerPerClusters, self.numclusters)
        self.flowers, self.labels, self.centers = make_blobs(n_samples=self.numflowers, center_box =(0,self.width), 
                                                             centers=None, cluster_std=float(self.width)/8.0, return_centers=True)
        self.pollinationTime = 5 # in seconds
        
        # Locate flowers that are outside the bounds of the field and remove them
        for i in range(len(self.flowers)-1, -1, -1):
            flower = self.flowers[i]
            if flower[0] > self.length or flower[0] < 0 \
                or flower[1] > self.width or flower[1] < 0:
                self.flowers = np.delete(self.flowers, i, 0)
                self.labels = np.delete(self.labels, i, 0)
        
        self.neighborsDict = dict()

    def getFlowers(self):
        return self.flowers
    
    def getWidth(self):
        return self.width()
    
    # Returns all flowers within the specified radius of the given point
    def getFlowersWithinRadius(self, point, radius):
        if radius not in self.neighborsDict:
            neigh = NearestNeighbors(radius=radius)
            neigh.fit(self.flowers)
            self.neighborsDict[radius] = neigh
        else:
            neigh = self.neighborsDict[radius]
        neighborsGraph = neigh.radius_neighbors([point])
        neighborFlowers = self.flowers[neighborsGraph[1][0]]
        return neighborFlowers

    # def getPlanterModel(self):
    #     return self.planterModel
    
    # def getFlowerLocations(self):
    #     return self.flowerLocations

