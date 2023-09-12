#this code can be optimized; let's look here if we have performance issues

from math import sqrt

def find_distances(waypoints):

    waypoint_distances = {}

    #TODO: FIX THE LOGIC SO IT ISNT TRASH

    numpoints = len(waypoints)

    for startI in range(numpoints):
        for endI in range(startI + 1, numpoints):
            
            x = waypoints[endI][1] - waypoints[startI][0]
            y = waypoints[endI][1] - waypoints[startI][1]
            z = waypoints[endI][2] - waypoints[startI][2]

            distanceXY = sqrt(x**2 + y**2)
            distance = sqrt(distanceXY**2 + z**2)

            waypoint_distances[(startI, endI)] = distance
    
    return waypoint_distances

def find_path(waypoints):
    waypoint_distances = find_distances(waypoints)
    print(waypoint_distances)



#run a test if WaypointOptimizer is run directly
#(as opposed to being imported into a different script)
if __name__ == "__main__":
    find_path([(5, 2, 1), (0,0,0), (2,3,2), (1,1,1)])