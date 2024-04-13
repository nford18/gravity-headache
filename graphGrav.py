import matplotlib.pyplot as plt
import math
from numpy import interp
from scipy.optimize import minimize

DONUT_RADIUS = 0.2 # AU
METERS_IN_AU = 1.495978*10**11

"""Gets the squared distance from start to end"""
def getDistSquare(start, end):
    return (end[0]-start[0])**2 + (end[1]-start[1])**2 + (end[2]-start[2])**2

"""Gets the unit vector from time i in start toward time j in end"""
def getDir(start, end, i, j):
    mag = math.sqrt(getDistSquare(start, end, i))
    return [(end[0][j]-start[0][i])/mag, (end[1][j]-start[1][i])/mag, (end[2][j]-start[2][i])/mag]

"""Retrieves a random mass based on the distributions of asteroid density and asteroid diameter"""
def getMass():
    return 

def f(t, args):
    t1, t2 = t
    lisa, asteroid, time = args
    # print("\n\nCheck: ", str(len(time)), str(len(asteroid[0])), str(len(lisa[0])))
    interpAster = [interp(t2, time, asteroid[0]),interp(t2, time, asteroid[1]),interp(t2, time, asteroid[2])]
    interpLisa = []
    for i in range(3):
        interpLisa.append([interp(t1, time, lisa[i][0]),interp(t2, time, lisa[i][1]),interp(t2, time, lisa[i][2])])
    return min(getDistSquare(interpLisa[0], interpAster), getDistSquare(interpLisa[1], interpAster), getDistSquare(interpLisa[2], interpAster))
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
    timeFull = []
    for i in range(len(data)):
        data_list.append(data[i].strip("\n").split(","))
    # print(len(data_list),len(data_list[0]))
    for i in range(len(data_list)):
        timeFull.append(float(i)/365.0/24.0)
        for j in range(len(data_list[i])):
            pos_aster[j%3].append(float(data_list[i][j]))


# calculate acceleration
accel = []
# M = 0.0010277825457702485
M = 8611.922318
G = 6.67 * 10**(-11)
# if(not len(pos_aster[0]) == len(pos_lisa[0][0])):
#     # Show error message
#     print("Array lengths do not match: array[" + str(len(pos_aster[0])) + "] and array[" + str(len(pos_lisa[0][0])) + "] found.")
    
# else:
    # for i in range(len(pos_aster[0])):
result = minimize(f, [0,0], args=[pos_lisa, pos_aster, timeFull])
print(result.x)
# only save the value if it's in the donut
# if (minDistSquare < DONUT_RADIUS**2):
if(not result.success):
    print("Error:" + str(result.message))
else:
    # a_i from F = GMm/r^2 => a = GM/r^2 ; G=1 in our units
    thirtyMinutesRange = 0.5/24.0/365.0 # pow(5.70776256, -5)
    minuteStep = 1.0/60.0/24.0/365.0 # pow(1.90258752, -6)
    print(thirtyMinutesRange, minuteStep)
    t = -thirtyMinutesRange
    timePeak = []
    i = -30
    while(t <= thirtyMinutesRange):
        # get the squared distance (in AU)
        dist2 = f([result.x[0]+t, result.x[1]+t], args=[pos_lisa, pos_aster, timeFull])
        # convert the distance to m and plug into accel formula, append
        accel.append(G*M/(dist2*(METERS_IN_AU)**2))
        timePeak.append(i)
        i += 1
        t += minuteStep
# print(accel)
print("Minimum Distance:", math.sqrt(f(result.x, args=[pos_lisa, pos_aster, timeFull]))* METERS_IN_AU, "m")

plt.scatter(timePeak, accel, marker = ".")
plt.title("LISA Craft Acceleration from Asteroid Around Its Peak")
plt.xlabel("Time (min)")
plt.ylabel("Acceleration (m/s^2)")
plt.show()
"""

density will be chosen from a hat.
    - look up distribution
for volume make histogram of known ones then pull other asteroid volumes out of a hat

Do we want to average the acceleration felt by the three spacecraft?
    (a0 + a1 + a2)/3
Or the closest spacecraft to the asteroid? <<< this
    a_minDist
    - possibly this ( confirm with shane)

"""
        
