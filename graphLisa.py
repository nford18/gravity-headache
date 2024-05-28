"""
Script to graph the LISA simulation position data 

Author: Nicholas Ford
"""
import matplotlib.pyplot as plt
import math

# function to shorthand distance formula in plotting
def getDist(v1, v2,i):
    return math.sqrt( (v1[0][i]-v2[0][i])**2 + (v1[1][i]-v2[1][i])**2 + (v1[2][i]-v2[2][i])**2)

# import lisa position data
filename = "export_lisa"
with open("./plots/" + filename + ".csv") as file:
    # file.readline() # format line
    data = file.readlines()
    data_list = []
    pos = [[[],[],[]],[[],[],[]],[[],[],[]]] # pos[n][x_i][~t]
    # feed raw data string into array
    for i in range(len(data)):
        data_list.append(data[i].strip("\n").split(","))
    # translate data array into 2D position array
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            pos[j//3][j%3].append(float(data_list[i][j]))

###########################################
#               Orbit Plot                #
###########################################

ax = plt.figure().add_subplot(111, projection='3d')
ax.scatter(pos[0][0], pos[0][1], pos[0][2], marker=".")
ax.scatter(pos[1][0], pos[1][1], pos[1][2], marker=".")
ax.scatter(pos[2][0], pos[2][1], pos[2][2], marker=".")
ax.set_xlabel('x (AU)')
ax.set_ylabel('y (AU)')
ax.set_zlabel('z (AU)')
ax.set_xlim3d(-1.05,1.05)
ax.set_ylim3d(-1.05,1.05)

# ax.set_zlim3d(-0.5, 0.5) # zoom out
ax.set_zlim3d(-0.075, 0.075) # zoom in
plt.title('LISA Orbit Over One Year')
plt.show()

###########################################
#          Satellite Separation           #
###########################################

# posDiff = [[],[],[],[]] # t, 01, 02, 12
# t_max = 1 # yr
# dt = 0.001 # yr
# dt = 1.0/(365.0*24.0)
# for i in range(len(pos[0][0])):
#     posDiff[0].append(i*dt)
#     posDiff[1].append(getDist(pos[0],pos[1],i))
#     posDiff[2].append(getDist(pos[0],pos[2],i))
#     posDiff[3].append(getDist(pos[1],pos[2],i))
# plt.plot(posDiff[0], posDiff[1], label = "0-1 Separation")
# plt.plot(posDiff[0], posDiff[2], label = "0-2 Separation")
# plt.plot(posDiff[0], posDiff[3], label = "1-2 Separation")
# plt.title("LISA Craft Separation Through Orbit")
# plt.xlabel("Time (yr)")
# plt.ylabel("Distance (AU)")
# plt.legend()
# plt.show()



###########################################
#      Attempt to View Noise Source       #
###########################################
# This section is not used in final plots

# xyPlot = [[],[]] # x,y
# t_max = 1 # yr
# dt = 0.001 # yr
# for i in range(len(pos[0][0])):
#     xyPlot[0].append(pos[0][0][i])
#     xyPlot[1].append(pos[0][1][i])
# plt.plot(xyPlot[0], xyPlot[1], label = "1-2 Separation")
# plt.title("LISA Craft Separation Through Orbit")
# plt.xlabel("Time (yr)")
# plt.ylabel("Distance (AU)")
# plt.legend()
# plt.show()