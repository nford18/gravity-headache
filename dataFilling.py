import math
import matplotlib.pyplot as plt
import numpy.random as rand

# d_arr = []


with open("./cappy/data/fullData.csv", "w+") as new_file:
    # file has order: "e","a","i","om","w","diameter","H","albedo"
    with open("./cappy/data/source_data.csv") as file:
        file.readline() # skip header line
        data = file.readlines()
        for index, line in enumerate(data):
            lineArr = line.strip("\n").split(",")
            newline = ["0: type","1: e","2: a","3: i","4: om","5: w",
                    "6: diameter","7: H","8: albedo","9: density"]
            hadDiameter = lineArr[5] != ""
            hadAlbedo = lineArr[7] != ""
            missingH = lineArr[6] == "" # apparently there are 5 blank H values

            # populate new line with orbital parameters
            newline[1] = lineArr[0] # e
            newline[2] = lineArr[1] # a
            newline[3] = lineArr[2] # i
            newline[4] = lineArr[3] # om
            newline[5] = lineArr[4] # w
            if(missingH):
                print("line", index, "skipped due to missing H-value.")
            else:
                # populate new line with H
                newline[7] = lineArr[6]
                if(hadAlbedo):
                    # populate new line with given albedo
                    newline[8] = lineArr[7]
                    # find type from albedo
                    if (float(lineArr[7])==0.03):
                        newline[0] = "C"
                    elif (float(lineArr[7]) > 0.18):
                        newline[0] = "S"
                    else:
                        # if [0.1, 0.18), pick S or M based on rarity distribution
                        if(rand.uniform(0.0,25.0) <=17.0):
                            newline[0] = "S"
                        else:
                            newline[0] = "M"
                else:
                    # find albedo from a random type
                    randNum = rand.uniform(0.0, 1.0)
                    if(randNum <= 0.75):   # 75% C
                        newline[0] = "C"
                        newline[8] = str(0.03)
                    elif(randNum <= 0.92): # 17% S
                        newline[0] = "S"
                        newline[8] = rand.uniform(0.1,0.22)
                    else:                 # 8% M
                        newline[0] = "M"
                        newline[8] = rand.uniform(0.1,0.18)
                if (hadDiameter):
                    # populate new line with given diameter
                    newline[6] = lineArr[5]
                    # d_arr.append(float(lineArr[1]))
                else:
                    # populate new line with derived diameter
                    # print(lineArr[6], "->", newline[7])
                    # print("<",newline[7],">", " <",newline[8] ,">")
                    newline[6] = str(10**(-float(newline[7])/5.0) / math.sqrt(float(newline[8])) * 1329)
                    
                        
                # get density from type
                if (newline[0] == "C"):
                    newline[9] = str(rand.uniform(3.111069652, 3.441218905, 1)[0])
                elif (newline[0] == "S"):
                    newline[9] = str(rand.uniform(3.183649635, 3.444379562, 1)[0])
                else:
                    newline[9] = str(rand.uniform(6.73375, 6.87875, 1)[0])
                # print(newline)
                new_file.write(str(newline).strip("[]\'") + "\n")
"""
// Graphing diameter for testing 
print("Valid points found: " + str(len(d_arr)))
output = plt.hist(d_arr, bins = "auto", density = True)
# print(output)
sum = 0
start = output[1][0]
width = output[1][1] - output[1][0]
with open("./cappy/data/radius_distribution.csv", "w+") as file:
    for i in range(len(output[0])):
        sum += output[0][i]
        file.write(str(i) + "," + str(output[0][i]) + "\n")
    file.write("total," + str(sum) + "\n")
    file.write("start," + str(output[1][0]) + "\n")
    file.write("width," + str(output[1][1] - output[1][0]) + "\n")
plt.show()
# plt.plot(r_fromD, marker=".", label="diameter")
# # plt.plot(r_fromH, marker=".", label="bronicki")
# plt.xlabel = 'asteroid number'
# plt.ylabel = 'radius (km)'
# plt.legend()
# plt.show()
"""