"""
This code takes in waypoints in the format (x, y, z) (all in centimeters)
and computes the shortest path between them
"""

#this code can be optimized; let's look here if we have performance issues

from math import sqrt, factorial
from time import sleep

def progressMeter(label, percentage, decimal_digits):
    percentageShown = str(min(int((percentage * 100 + 0.5) * (10**decimal_digits)) / (10**decimal_digits), 100))
    percentageShown += " " * (4 + decimal_digits - len(percentageShown))
    print(label + ": " + percentageShown + "% complete   ", end='\r')

"""
Creates a table of the distance between every pair of 2 waypoints
This way we don't have to compute these over and over, speeding up the algorithm
Waypoint distances are stored in this format:

{(waypoint 1 index, waypoint 2 index) : distance}
"""
def find_distances(waypoints):
    waypoint_distances = {}

    numpoints = len(waypoints)

    #iterates through all unique pairs of waypoints
    for startI in range(numpoints):
        progressMeter("Finding waypoint distances", startI/numpoints, 2)
        for endI in range(startI + 1, numpoints):
            
            #finds relative x, y, and z distances between the current waypoint pair
            x = waypoints[endI][1] - waypoints[startI][0]
            y = waypoints[endI][1] - waypoints[startI][1]
            z = waypoints[endI][2] - waypoints[startI][2]

            #Uses the Pythagorean Theorem twice to find the distance between the 2 points 
            distanceXY = sqrt(x**2 + y**2)
            distance = sqrt(distanceXY**2 + z**2)

            #Adds the current waypoint pair and its distance to the list of distances
            waypoint_distances[(startI, endI)] = distance
    print("Finding waypoint distances: 100.00% complete")
    return waypoint_distances

"""
Midpoints are all waypoints but the start and end points

"""
def find_permutations(waypoints, startI, endI):

    midpoints = list(range(0, len(waypoints)))
    midpoints.pop(startI)
    midpoints.remove(endI)

    numpoints = len(midpoints)
    currentArray = []
    combinations = []
    for i in range(numpoints):
        currentArray.append(None)
    total = factorial(len(midpoints))
    permutations = find_permutations_recursive(midpoints, currentArray, combinations, total)
    #print("Finding permutations: 100.00% complete")

    for permutation in permutations:
        permutation.insert(0, startI)
        permutation.append(endI)

    print("Finding permutations: 100.00% complete")
    return permutations
    

def find_permutations_recursive(midpoints, currentArray, combinations, total):
     
    progressMeter("Finding permutations", len(combinations)/total, 2)
    
    currentPossibilities = []

    currIndex = -1
    i = 0
    while i < len(midpoints):
        currIndex += 1
        if currentArray[currIndex] != None:
            continue
        currentPossibilities.append(currentArray.copy())
        currentPossibilities[-1][currIndex] = midpoints[0]
        i += 1
    
    midpoints.pop(0)

    if len(midpoints) == 0:
        combinations.append(currentPossibilities[0])
        return
    
    for possibility in currentPossibilities:
        find_permutations_recursive(midpoints.copy(), possibility.copy(), combinations, total)
    
    return combinations

"""
#This is the method to call in other scripts
#waypoints are stored in this format:
(waypoint x (left-right), waypoint y (back-front), waypoint z (bottom-top))
all distances are in centimeters
startI and endI are the index of the starting and ending point
"""
def find_path(waypoints, startI, endI):
    waypoint_distances = find_distances(waypoints)
    print(waypoints)

    waypoint_permutations = find_permutations(waypoints, startI, endI)

    lowest_distance = None
    shortest_path = None

    for permutation in waypoint_permutations:
        current_distance = 0
        print("####################")
        print(permutation)
        for i in range(len(permutation) - 1):
            startpoint = min(permutation[i], permutation[i+1])
            endpoint = max(permutation[i], permutation[i+1])
            print("start: " + str(startpoint) + ", end: " + str(endpoint))
            current_distance += waypoint_distances[startpoint, endpoint]
        
        
        print("checking total distance")
        print(current_distance)
        if lowest_distance == None or current_distance < lowest_distance:
            lowest_distance = current_distance
            shortest_path = permutation
            print("NEW SHORTEST FOUND")

    print()

    

#run a test if the Pathfinder script is run directly
#(as opposed to being imported into a different script)
if __name__ == "__main__":
    find_path([(5, 2, 1), (0,0,0), (2,3,2), (1,1,1)], 0, 1)
    #permutations = find_permutations([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    #print(permutations)