# import math
import matplotlib.pyplot as plt
# import numpy.random as rand

with open("./cappy/data/fullData.csv", "r") as file:
    file.readline()
    data = file.readlines()
    masses1 = []
    masses2 = []
    masses3 = []
    # i = 0
    max = 0
    for line in data:
        value = float(line.strip("\n").split(",")[9])
        if(value < 10**1):
            masses1.append(value)
        # elif(value < 10**2):
        #     masses2.append(value)
        else:
            masses3.append(value)
        # print(i)
        # i += 1
    print("test")
    print(len(masses1))
    print(len(masses2))
    print(len(masses3))
    plt.hist(masses1, bins = "auto", label="Small masses")
    plt.legend()
    # plt.xscale("log")
    plt.show()

    plt.hist(masses2, bins = "auto", label="Medium masses")
    plt.legend()
    plt.show()

    plt.hist(masses3, bins = "auto", label="Large masses")
    plt.legend()
    plt.show()
    # plt.xlim(0, 500)
    # print(masses)
    # print(str(len(masses2)))
    # # plt.show()
    # print("test")
        