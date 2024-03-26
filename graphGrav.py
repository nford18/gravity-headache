import matplotlib.pyplot as plt
import math

DONUT_RADIUS = 0.2 # AU

"""Gets the squared distance from start to end at the i-th time step"""
def getDistSquare(start, end, i):
    return (end[0][i]-start[0][i])**2 + (end[1][i]-start[1][i])**2 + (end[2][i]-start[2][i])**2

"""Gets the unit vector from start toward end at the i-th time step"""
def getDir(start, end, i):
    mag = math.sqrt(getDistSquare(start, end, i))
    return [(end[0][i]-start[0][i])/mag, (end[1][i]-start[1][i])/mag, (end[2][i]-start[2][i])/mag]

"""Retrieves a random mass based on the distributions of asteroid density and asteroid diameter"""
def getMass():
    return 


# import LISA data
filename = "export_lisa"
with open("./plots/" + filename + ".csv") as file:
    file.readline() # format line
    data = file.readlines()
    data_list = []
    pos_lisa = [[[],[],[]],[[],[],[]],[[],[],[]]] # pos[n][x_i][~t]
    running = True
    for i in range(len(data)):
        data_list.append(data[i].strip("\n").split(","))
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            pos_lisa[j//3][j%3].append(float(data_list[i][j]))


# import Asteroid data
filename = "export_ast"
with open("./plots/" + filename + ".csv") as file:
    file.readline() # format line
    data = file.readlines()
    data_list = []
    pos_aster = [[],[],[]] # pos[x_i][~t]
    for i in range(len(data)):
        data_list.append(data[i].strip("\n").split(","))
    print(len(data_list),len(data_list[0]))
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            pos_aster[j%3].append(float(data_list[i][j]))

# calculate acceleration
accel = []
M=1
if(len(pos_aster[0]) == len(pos_lisa[0][0])):
    for i in range(len(pos_aster[0])):
        minDistSquare = min(getDistSquare(pos_lisa[0], pos_aster, i),
                    getDistSquare(pos_lisa[1], pos_aster, i),
                    getDistSquare(pos_lisa[2], pos_aster, i))
        # only save the value if it's in the donut
        if (minDistSquare < DONUT_RADIUS**2):
        # a_i from F = GMm/r^2 => a = GM/r^2 ; G=1 in our units
            a_i = M/minDistSquare  
            accel.append(a_i)
else:
    # Show error message
    print("Array lengths do not match: array[" + str(len(pos_aster[0])) + "] and array[" + str(len(pos_lisa[0][0])) + "] found.")

"""

density will be chosen from a hat.
    - look up distribution
for volume make histogram of known ones then pull other asteroid volumes out of a hat

Do we want to average the acceleration felt by the three spacecraft?
    (a0 + a1 + a2)/3
Or the closest spacecraft to the asteroid?
    a_minDist
    - possibly this ( confirm with shane)

"""
        
