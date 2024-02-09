import math
import matplotlib.pyplot as plt

r_arr = []
with open("./cappy/plots/radius_dist_source_data.csv") as file:
    file.readline()
    data = file.readlines()
    for line in data:
        lineArr = line.split(",")
        if (lineArr[4] == "TRUE"):
            r_arr.append(float(lineArr[1])/2)
        # elif (lineArr[5] == "TRUE"):
        #     n_arr.append(n)
        #     n += 1
        #     r_arr.append(10**(float(lineArr[2])/5.0) / math.sqrt(float(lineArr[3])) * 1.329)
print("Valid points found: " + str(len(r_arr)))
output = plt.hist(r_arr, bins = "auto", density = True)
# print(output)
sum = 0
with open("./cappy/plots/radius_distribution.csv", "w+") as file:
    for i in range(len(output[0])):
        sum += output[0][i]
        file.write(str(i) + "," + str(output[0][i]) + "\n")
    file.write("total," + str(sum) + "\n")
    file.write("start," + str(output[1][0]) + "\n")
    file.write("width," + str(output[1][1] - output[1][0]) + "\n")
# plt.show()
