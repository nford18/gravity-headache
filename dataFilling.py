import math
import matplotlib.pyplot as plt
import numpy.random as rand

# file has order: "e","a","i","om","w","diameter","H","albedo"
with open("./data/sbdb_query_results.csv") as file:
    file.readline() # skip header line
    data = file.readlines()
with open("./data/fullData.csv", "w+") as new_file:
    new_file.write("\'e\', \'a\', \'i\', \'om\', \'w\', \'diameter\', \'H\', \'albedo\', \'type\', \'mass\',\n")
    for index, line in enumerate(data):
        lineArr = line.strip("\n").split(",")
        newline = ["e","a","i","om","w","diameter","H","albedo","type","mass"]
        hadDiameter = lineArr[5] != ""
        hadAlbedo = lineArr[7] != ""
        hadH = lineArr[6] != "" # apparently there can be blank H values

        # populate new line with orbital parameters
        newline[0] = lineArr[0] # e
        newline[1] = lineArr[1] # a
        newline[2] = lineArr[2] # i
        newline[3] = lineArr[3] # om
        newline[4] = lineArr[4] # w
        newline[5] = lineArr[5] # diameter
        newline[6] = lineArr[6] # H
        newline[7] = lineArr[7] # albedo
        # might add period to data grabbing
        # newline[8] = lineArr[8] # period

        if(not hadH):
            print("line", index, "skipped due to missing H-value.")
        else:
            if(hadAlbedo):
                # grab given albedo
                albedo = float(lineArr[7])
                # find type from albedo
                if (abs(albedo-0.03) <=0.001):
                    astType = "C"
                elif (albedo > 0.18):
                    astType = "S"
                else:
                    # if [0.1, 0.18), pick S or M based on rarity distribution
                    if(rand.uniform(0.0,0.25) <=0.17):
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
                newline[7] = str(albedo)
            newline[8] = astType

            if (hadDiameter):
                # grab given diameter
                diameter = float(lineArr[5])
            else:
                # derive diameter
                diameter = 10**(-float(lineArr[6])/5.0) / math.sqrt(float(albedo)) * 1329
                newline[5] = str(diameter)
                    
            # get density from type
            if (astType == "C"):
                density = rand.uniform(3.111069652, 3.441218905)
            elif (astType == "S"):
                density = rand.uniform(3.183649635, 3.444379562)
            else:
                density = rand.uniform(6.73375, 6.87875)
            
            volume = math.pi/6.0 * math.pow(diameter,3)
            newline[9] = str(volume*density)
            for element in newline:
                new_file.write(element.strip("[]\'") + ", ")
            new_file.write("\n")