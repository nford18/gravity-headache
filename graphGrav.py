import matplotlib.pyplot as plt
import math

"""Gets the squared distance from start to end at the i-th time step"""
def getDist2(start, end, i):
    return (end[0][i]-start[0][i])**2 + (end[1][i]-start[1][i])**2 + (end[2][i]-start[2][i])**2

"""Gets the unit vector from start toward end at the i-th time step"""
def getDir(start, end, i):
    mag = math.sqrt(getDist2(start, end, i))
    return [(end[0][i]-start[0][i])/mag, (end[1][i]-start[1][i])/mag, (end[2][i]-start[2][i])/mag]

"""Retrieves a random mass based on the distributions of asteroid density and asteroid diameter"""
def getMass():
    return 


# import LISA data
filename = "export_lisa"
with open("./cappy/plots/" + filename + ".csv") as file:
    # file.readline() # format line
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
with open("./cappy/plots/" + filename + ".csv") as file:
    # file.readline() # format line
    data = file.readlines()
    data_list = []
    pos_aster = [[],[],[]] # pos[x_i][~t]
    for i in range(len(data)):
        data_list.append(data[i].strip("\n").split(","))
    print(len(data_list),len(data_list[0]))
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            pos_aster[j%3].append(float(data_list[i][j]))

accel = []
M=1
if(len(pos_aster[0]) == len(pos_lisa[0][0])):
    for i in range(len(pos_aster[0])):
        minDist = getDist2(pos_lisa[0], pos_aster, i)

        for n in range(1,3):
            dist = getDist2(pos_lisa[n], pos_aster, i)
            if (dist < minDist):
                minDist = dist
        a_i = M/minDist  # from F = GMm/r^2 => a = GM/r^2 ; G=1 in our units
        accel.append(a_i)

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
        
