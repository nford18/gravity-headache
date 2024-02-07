import matplotlib.pyplot as plt
import math

filename = "export_ast"

def getDist(v1, v2,i):
    return math.sqrt( (v1[0][i]-v2[0][i])**2 + (v1[1][i]-v2[1][i])**2 + (v1[2][i]-v2[2][i])**2)

with open("./cappy/plots/" + filename + ".csv") as file:
    # file.readline() # format line
    data = file.readlines()
    data_list = []
    pos = [[],[],[]] # pos[x_i][~t]
    for i in range(len(data)):
        data_list.append(data[i].strip("\n").split(","))
    print(len(data_list),len(data_list[0]))
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            # print(j%2)
            pos[j%3].append(float(data_list[i][j]))

###########################################
#               Orbit Plot                #
###########################################

ax = plt.figure().add_subplot(111, projection='3d')
ax.scatter(pos[0], pos[1], pos[2], marker=".")
ax.set_xlabel('x (AU)')
ax.set_ylabel('y (AU)')
ax.set_zlabel('z (AU)')

plt.title('The Asteroid plot')
plt.show()