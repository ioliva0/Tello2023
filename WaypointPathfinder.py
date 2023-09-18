"""
This code takes in waypoints in the format (x, y, z) (all in centimeters)
and computes the shortest path between them
"""



#this code can be optimized; let's look here if we have performance issues

from math import sqrt

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
    
    return waypoint_distances

"""
#This is the method to call in other scripts
#waypoints are stored in this format:
(waypoint x (left-right), waypoint y (back-front), waypoint z (bottom-top))
all distances are in centimeters
startI and endI are the index of the starting and ending point
"""
def find_path(waypoints, startI, endI):
    
    waypoint_distances = find_distances(waypoints)
    print(waypoint_distances)

    waypoint_indices = range(waypoints).pop(startI, endI)



#run a test if the Pathfinder script is run directly
#(as opposed to being imported into a different script)
if __name__ == "__main__":
    find_path([(5, 2, 1), (0,0,0), (2,3,2), (1,1,1)])