import math
import matplotlib.pyplot as plt
import numpy.random as rand

with open("./cappy/data/fullData.csv", "w+") as new_file:
    # file has order: "e","a","i","om","w","diameter","H","albedo"
    new_file.write("\'e\', \'a\', \'i\', \'om\', \'w\', \'mass\',\n")
    with open("./cappy/data/source_data.csv") as file:
        file.readline() # skip header line
        data = file.readlines()
        for index, line in enumerate(data):
            lineArr = line.strip("\n").split(",")
            newline = ["0: e","1: a","2: i","3: om","4: w",
                    "5: diameter"]
            hadDiameter = lineArr[5] != ""
            hadAlbedo = lineArr[7] != ""
            missingH = lineArr[6] == "" # apparently there can be blank H values

            # populate new line with orbital parameters
            newline[0] = lineArr[0] # e
            newline[1] = lineArr[1] # a
            newline[2] = lineArr[2] # i
            newline[3] = lineArr[3] # om
            newline[4] = lineArr[4] # w
            if(missingH):
                print("line", index, "skipped due to missing H-value.")
            else:
                if(hadAlbedo):
                    # grab given albedo
                    albedo = float(lineArr[7])
                    # find type from albedo
                    if (albedo==0.03):
                        astType = "C"
                    elif (albedo > 0.18):
                        astType = "S"
                    else:
                        # if [0.1, 0.18), pick S or M based on rarity distribution
                        if(rand.uniform(0.0,25.0) <=17.0):
                            astType = "S"
                        else:
                            astType = "M"
                else:
                    # find albedo from a random type
                    randNum = rand.uniform(0.0, 1.0)
                    if(randNum <= 0.75):   # 75% C
                        astType = "C"
                        albedo = str(0.03)
                    elif(randNum <= 0.92): # 17% S
                        astType = "S"
                        albedo = rand.uniform(0.1,0.22)
                    else:                 # 8% M
                        astType = "M"
                        albedo = rand.uniform(0.1,0.18)
                if (hadDiameter):
                    # grab given diameter
                    diameter = float(lineArr[5])
                else:
                    # derive diameter
                    diameter = 10**(-float(lineArr[6])/5.0) / math.sqrt(float(albedo)) * 1329
                        
                # get density from type
                if (astType == "C"):
                    density = rand.uniform(3.111069652, 3.441218905)
                elif (astType == "S"):
                    density = rand.uniform(3.183649635, 3.444379562)
                else:
                    density = rand.uniform(6.73375, 6.87875)
                
                newline[5] = str(math.pi/6.0 * math.pow(diameter,3) *density)
                for element in newline:
                    new_file.write(element.strip("[]\'") + ", ")
                new_file.write("\n")
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