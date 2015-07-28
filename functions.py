__author__ = 'Kevin'

import random
from math import *

#some general geographic functions
def bearing(lon1, lat1, lon2, lat2):

    #calculate the bearing of a two point vector
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    bear = degrees(atan2( sin(lon2-lon1)*cos(lat2), cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1)))
    bear = radians((bear+360)%360)

    return bear


def haversine(lon1, lat1, lon2, lat2):
    #calculate the harversine length between two points

    # converting DD to rad
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # using haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    m = 6378137 * c
    return m

def length(line):
    #calculate the harversine length of a line along multiple points

    linelength = 0

    for i in range(len(line)-1):
        start = line[i]
        end = line[i+1]
        verticelength = haversine(start[0], start[1], end[0], end[1])
        linelength += verticelength

    return linelength

def newCoordAlongLine(lon1,lat1, lon2, lat2, distance):
    #calculate new point on edge given a distance along the line

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    bear = atan2(sin(lon2-lon1)*cos(lat2),cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1))
    dist = distance / 6378137.00000
    newlat = asin(sin(lat1)*cos(dist) + cos(lat1)*sin(dist)*cos(bear))
    newlon = lon1 + atan2(sin(bear) * sin(dist) * cos(lat1), cos(dist) - sin(lat1) * sin(newlat))
    newlon = fmod((newlon + 3*pi), (2*pi))-pi

    return newlon*180/pi, newlat*180/pi

def normalizeAngle(bear):
        # Normalize the bearing angle to calculate parallelity

        radians = bear
        #bearing in normalized radians
        #-----------------------------
        radians_norm = radians
        if pi/2 < radians_norm <= 3*pi/2:
            radians_norm = -(pi - radians_norm)
        if 3*pi/2 < radians_norm <= 2*pi:
            radians_norm = -(2*pi - radians_norm)
        #bearing in degrees
        #------------------
        degrees = radians * 180/pi
        #bearing in normalized degrees
        #-----------------------------
        degrees_norm = degrees
        if 90 < degrees_norm <= 270:
            degrees_norm = -(180 - degrees_norm)
        if 270 < degrees_norm <= 360:
            degrees_norm = -(360 - degrees_norm)

        return radians_norm, degrees_norm

def newCoordAtBearing(bear, midpoint, distance):
    #calculate new point on edge given a distance along the line

    lon1,lat1 = map(radians, midpoint)

    dist = distance*1000 / 6378137.00000

    newlat = asin(sin(lat1)*cos(dist) + cos(lat1)*sin(dist)*cos(bear))
    newlon = lon1 + atan2(sin(bear) * sin(dist) * cos(lat1), cos(dist) - sin(lat1) * sin(newlat))
    newlon = fmod((newlon + 3*pi), (2*pi))-pi

    return newlon*180/pi, newlat*180/pi

class boxFetcher:
    #random bounding box generation class

    def __init__(self,minX,minY,maxX,maxY):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY

    def randomCoordInBBox(self):
        #create random coordinate in bounding box

        y = self.minY + random.random() * (self.maxY - self.minY)
        x = self.minX + random.random() * (self.maxX - self.minX)
        return x,y
    def randomBBox(self, w, h):
        #create bounding box with specified w en h around random coordinate in bounding box

        coords = self.randomCoordInBBox()

        newMinx = newCoordAtBearing((3*pi)/2, coords, w/2)[0]
        newMiny = newCoordAtBearing(pi, coords, h/2)[1]
        newMaxx = newCoordAtBearing(pi/2, coords, w/2)[0]
        newMaxy = newCoordAtBearing(2*pi, coords, h/2)[1]

        return coords,newMinx,newMiny,newMaxx,newMaxy

if __name__ == "__main__":
    generate = boxFetcher(3.3313, 50.7209, 4.3301, 51.3529)
    print generate.randomBBox(10,10)