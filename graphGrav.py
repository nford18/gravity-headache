"""
Script to graph the asteroid simulation position data 

Author: Nicholas Ford
"""
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
    # Nothing yet
    return 

"""
function to be minimized by the optimization algorithm

@param t: array of two time values
@param args: 2D array of data to interp off of 

@return the minimum distance from a spacecraft to the asteroid
"""
def f(t, args):
    t1, t2 = t
    lisa, asteroid, time = args
    # interpolate the [x,y,z] of the asteroid for the given t2 time
    interpAster = [interp(t2, time, asteroid[0]),interp(t2, time, asteroid[1]),interp(t2, time, asteroid[2])]
    # interpolate the [x,y,z] of each LISA spacecraft for the given t1 time
    interpLisa = []
    for i in range(3):
        interpLisa.append([interp(t1, time, lisa[i][0]),interp(t2, time, lisa[i][1]),interp(t2, time, lisa[i][2])])
    # return the minimum of the distances between each of the three spacecraft and the asteroid  
    return min(getDistSquare(interpLisa[0], interpAster), getDistSquare(interpLisa[1], interpAster), getDistSquare(interpLisa[2], interpAster))

# import LISA data
filename = "export_lisa"
with open("./plots/" + filename + ".csv") as file:
    file.readline() # format line
    data = file.readlines()
    data_list = []
    pos_lisa = [[[],[],[]],[[],[],[]],[[],[],[]]] # pos[n][x_i][~t]
    # feed raw data string into array
    for i in range(len(data)):
        data_list.append(data[i].strip("\n").split(","))
    # translate data array into 2D position array and populate time array
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
    # feed raw data string into array
    for i in range(len(data)):
        data_list.append(data[i].strip("\n").split(","))
    # translate data array into 2D position array and populate time array
    for i in range(len(data_list)):
        timeFull.append(float(i)/365.0/24.0)
        for j in range(len(data_list[i])):
            pos_aster[j%3].append(float(data_list[i][j]))

# calculate acceleration
accel = []
M = 8611.922318
G = 6.67 * 10**(-11)

result = minimize(f, [0,0], args=[pos_lisa, pos_aster, timeFull])

if(not result.success):
    print("Error:" + str(result.message))
else:
    # interpolating the data around the minimum found above

    thirtyMinutesRange = 0.5/24.0/365.0 # pow(5.70776256, -5)  (30 mins in years)
    minuteStep = 1.0/60.0/24.0/365.0 # pow(1.90258752, -6)  (1 min in years)

    t = -thirtyMinutesRange # initialize time var to left bound of range 
    timePeak = [] # array that holds time values for plotting
    i = -30
    while(t <= thirtyMinutesRange):
        # get the squared distance (in AU)
        dist2 = f([result.x[0]+t, result.x[1]+t], args=[pos_lisa, pos_aster, timeFull])
        
        # convert the distance to m, plug into accel formula, and append to array
        # a_i from F = GMm/r^2 => a = GM/r^2
        accel.append(G*M/(dist2*(METERS_IN_AU)**2))
        timePeak.append(i)
        i += 1
        t += minuteStep
print("Minimum Distance:", math.sqrt(f(result.x, args=[pos_lisa, pos_aster, timeFull]))* METERS_IN_AU, "m")

plt.scatter(timePeak, accel, marker = ".")
plt.title("LISA Craft Acceleration from Asteroid Around Its Peak")
plt.xlabel("Time (min)")
plt.ylabel("Acceleration (m/s^2)")
plt.show()