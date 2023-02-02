import csv
import os
import osmnx

import Mapping
import AlternativeRoute
import fetchActivityLocations
import NetworkGraph
import ShortestRoute

import tkinter
from tkinter import filedialog
tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing



def findActivityLocations(userFile):
    #First, do input processing.

    listStops = []
    with open(userFile,'r') as inputFile:
        fileReader = csv.reader(inputFile)
        # Skip Header
        next(fileReader)
        # Import list of stops
        for row in fileReader:
            stop = (float(row[0]),float(row[1]))
            listStops.append(stop)
    
    #Call fetchActivityLocations
    result = fetchActivityLocations.fetchStopAL(listStops)
    
    # Write Result to a csv file.
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'fetchOutput.csv')
    with open(outFile, 'w', newline='') as outputFile:
        fileWriter = csv.writer(outputFile)
        # Creater Header
        fileWriter.writerow(['Latitude', 'Longitude', 'Nearby Activity Locations'])

        for i in result:
            activityList = []
            for j in i[1]:
                activityList.append([j.name, float(j.lat), float(j.lon)])

            fileWriter.writerow([i[0].lat, i[0].lon, activityList])        

    
    print("Complete. The path of the generated file is: \n" + dirName)

def generateShortestPath(userFile, motion):
    #File Preprocessing

    inputPoints = []
    with open(userFile,'r') as inputFile:
        fileReader = csv.reader(inputFile)
        # Import points
        for row in fileReader:
            point = (float(row[0]),float(row[1]))
            inputPoints.append(point)
    
    #Generate NetworkGraph
    networkGraph = NetworkGraph.NetworkGraph(inputPoints[0], inputPoints[-1], inputPoints, motion)
    shortestRoute = ShortestRoute.ShortestRoute(networkGraph, inputPoints)
    
    print("Complete, now you can do the mapping.")
    return networkGraph, shortestRoute

def generateAlternativePath(userFile):
    #File Preprocessing

    inputPoints = []
    with open(userFile,'r') as inputFile:
        fileReader = csv.reader(inputFile)
        # Import points
        for row in fileReader:
            point = (float(row[0]),float(row[1]))
            inputPoints.append(point)
    
    # Generate Graph
    alternativeRoute = AlternativeRoute.AlternativeRoute(inputPoints)
    print("Complete, now you can put the points on the map.")
    return alternativeRoute


def mapEpisodes(userFile):
    listCoords = []
    listTimeStamp = []
    listMode = []
    with open(userFile, 'r') as inputFile:
        fileReader = csv.reader(inputFile)
        # Skip Header
        next(fileReader)
        # Import data
        for row in fileReader:
            location = (float(row[0]), float(row[1]))
            listCoords.append(location)
            listTimeStamp.append(row[2]) # Have to update
            listMode.append(row[3]) # Have to update
    # Generate Graph 
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'episode_path.html')
    Mapping.MapEpisodePoints(listCoords,listTimeStamp,listMode,outFile)

    print("Complete.\n The name of the file is episode_path.html.\n The path of the generated file is: \n" + dirName)    

def mapActivityLocations(userFile):
    listLocations = []
    listDescription = []
    with open(userFile,'r') as inputFile:
        fileReader = csv.reader(inputFile)
        next(fileReader)
        for row in fileReader:
            location = (float(row[0]),float(row[1]))
            listLocations.append(location)
            listDescription.append(row[2])

    # Generate Map
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'activity_location.html')
    Mapping.MapActivityLocation(listLocations,listDescription,outFile)
    print("Complete.\n The name of the file is activity_location.html.\n The path of the generated file is: \n" + dirName)


def mapSRoute(userNetworkGraph,userMotion, userRoute):
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'shortest_path.html')

    # Mapping
    Mapping.MapRoute(userNetworkGraph.graph,userMotion, userRoute.routes, outFile)
    print("Complete.\n The name of the file is shortest_path.html.\n The path of the generated file is: \n" + dirName)

def mapARoute(userMode, userRoute):
    dirName = os.path.dirname(os.path.abspath(__file__))
    outFile = os.path.join(dirName, 'alternative_path.html')

    # Mapping
    Mapping.MapRoute(userRoute.network.graph, userMode, userRoute.path.routes, outFile)
    print("Complete.\n The name of the file is alternative_path.html.\n The path of the generated file is: \n" + dirName)


# Driver code
if __name__ == '__main__':
    print("Please select the csv file you want to process: ")
    inputFile = filedialog.askopenfilename()


    while True:
        moduleSelect = int(input("Please select the module you want to go over: "))
        if (moduleSelect == 3):
            findActivityLocations(inputFile)
        elif(moduleSelect == 5):
            inputMotion = input("Please insert the motion of the episode: ")
            shortestNetworkGraph, shortestRoute =  generateShortestPath(inputFile, inputMotion)
        elif(moduleSelect == 6):
            alternativeRoute = generateAlternativePath(inputFile)
        elif(moduleSelect == 8):
            print("Please select the csv file you want to process: ")
            inputFile = filedialog.askopenfilename()
            mapActivityLocations(inputFile)
        elif(moduleSelect == 9):
            sRouteMotion = input("Please insert the motion of the episode: ")
            mapSRoute(shortestNetworkGraph, sRouteMotion, shortestRoute)
        elif (moduleSelect == 10):
            inputMotion = input("Please insert the mode of the points: ")
            print("Hello world!")
        elif (moduleSelect == 0):
            break
        else:
            print("Error. You choose the wrong number.")
