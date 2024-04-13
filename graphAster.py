import matplotlib.pyplot as plt

filename = "export_ast"

with open("./plots/" + filename + ".csv") as file:
    # file.readline() # format line
    data = file.readlines()
    data_list = []
    pos = [[],[],[]] # pos[x_i][~t]
    for i in range(len(data)):
        data_list.append(data[i].strip("\n").split(","))
    print(len(data_list),len(data_list[0]))
    for i in range(len(data_list)):
        for j in range(len(data_list[i])):
            # print(pos)
            pos[j%3].append(float(data_list[i][j]))

###########################################
#               Orbit Plot                #
###########################################

ax = plt.figure().add_subplot(111, projection='3d')
ax.scatter(pos[0], pos[1], pos[2], marker=".")
ax.set_xlabel('x (AU)')
ax.set_ylabel('y (AU)')
ax.set_zlabel('z (AU)')

plt.title('Asteroid Orbit Over One Year')
plt.show()

###########################################
#                xyz Plot                 #
###########################################

plt.plot(pos[0], label="x (AU)")
plt.plot(pos[1], label="y (AU)")
plt.plot(pos[2], label="z (AU)")
plt.legend()
plt.show()
