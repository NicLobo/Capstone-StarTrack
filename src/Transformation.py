import csv
import ast
from datetime import datetime
from Point import Point
import os
import pandas
from csv import writer
import statistics
from statistics import mode
import glob
import pandas as pd  
import ActivityLocation

#trace file path
def tracerelated(tracepath): 
    data = csv.reader(open(tracepath))

    li = []
 
    c=0
    
    for line in data:
        
        if c>0: 
            dt = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S.%f')
            li.append(Point(float(line[0]),float(line[1]),dt, None,float(line[3])))

        
        c = c+1

    return li

#stop file path
def stoprelated(stopfilepath): 
    data = csv.reader(open(stopfilepath))

    li = []
 
    c=0
    
    for line in data:
        
        if c>0: 
            dt = datetime.strptime(line[4], '%Y-%m-%d %H:%M:%S.%f')
            tracepath = os.path.dirname(os.path.dirname(stopfilepath))
            coord = pandas.read_csv(tracepath+'/trace.csv')
            print(float(line[9]))
            lat = float(coord.iloc[int(float(line[9])):int(float(line[9]))+1,0])
            long = float(coord.iloc[int(float(line[9])):int(float(line[9]))+1,1])
            print(lat,long)
            li.append(Point(lat,long,dt, line[8],float(line[9])))

        
        c = c+1

    return li

#episode path
def episoderelated(episodepath): 
    data = csv.reader(open(episodepath))

    li = []
    filename = os.path.basename(episodepath)
    idname = os.path.splitext(filename)[0]

    c=0
    
    for line in data:
        
        if c>0:
            dt = datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S.%f')
            li.append(Point(float(line[0]),float(line[1]),dt,line[4],float(idname[0])))

        
        c = c+1

    return li

def convertActivityLocation(ActvityLoactionList):
    convertedList = []
    for i in ActvityLoactionList:
        activityList = []
        for j in i[1]: # The list with all nearby locations
            activityList.append([j.name, float(j.lat), float(j.lon), j.amenity])
        # Append to final list
        convertedList.append([i[0].lat, i[0].lon, activityList])
    return convertedList

# Convert CSV file(i.e. fetchOutput.csv) into a nested list for mapping
def convertActivityCSV(userFile):
    convertedList = []
    with open(userFile, 'r') as inputFile:
        fileReader = csv.reader(inputFile)
        next(fileReader) # Skip Header
        for row in fileReader:
            nearbyList = ast.literal_eval(row[2])
            activityObjectList = []
            for activiyList in nearbyList:
                activityObjectList.append(convertListToActivityLocationObject(activiyList))
            convertedList.append([float(row[0]),float(row[1]),activityObjectList])
    print(convertedList)
    return convertedList

def convertListToActivityLocationObject(activityLocationList):
    newActivityLocation = ActivityLocation.ActivityLocation(activityLocationList[0],float(activityLocationList[1]),float(activityLocationList[2]), activityLocationList[3])
    return newActivityLocation


#trace file path          
def summarymode(tracefilepath):
    modes = []


    changec = 0
    
    files = glob.glob(os.path.dirname(tracefilepath)+'/episode'+ "/*.csv")
    print(files)
    
    for f in files:
        data = csv.reader(open(f))
        c = 0
        
        for line in data:
            
            if c>0: 
                
                modes.append(line[4])
                
                break
            
            c = c+1
    
    stats=os.path.dirname(tracefilepath)+'/summarymode.csv'
    with open(stats, 'w') as f1:
        writer_object = writer(f1)
        writer_object.writerow(['Summary Mode'])
        writer_object.writerow([str(mode(modes)) ])

def summaryModeTrace(tracefilepath):
    summarymodefilepath = os.path.dirname(tracefilepath)+'/summarymode.csv'
    c=0
    data = csv.reader(open(summarymodefilepath))
    li=""
    for line in data:
        
        if c>0: 
            
            li += line[0]

        
        c = c+1

    return li

convertActivityCSV("trace/trace1/activitylocations/trace-activityLocation.csv")