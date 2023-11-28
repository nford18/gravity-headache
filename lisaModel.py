#define _USE_MATH_DEFINES
import math
#include <string.h>
#include <stdio.h>

R = 1 # orbit radius in AU
ecc = 0.00965 # eccentricity of orbit
f_m = 1 # modulation frequency (1/yr)
# these give the initial ecliptic longitude and orientation of the constellation
lamb = 0
kappa = 0 

"""function to give LISA model position data from a time and n value"""
def model(t, n):
    alpha = 2*math.pi*f_m*t + kappa
    beta = 2*math.pi*n/3 + lamb
    x = R*math.cos(alpha) + 0.5*ecc*R*(math.cos(2*alpha-beta)-3*math.cos(beta)) + 0.125*ecc**2*R*(3*math.cos(3*alpha-2*beta)-10*math.cos(alpha)-5*math.cos(alpha-2*beta))
    y = R*math.sin(alpha) + 0.5*ecc*R*(math.sin(2*alpha-beta)-3*math.sin(beta)) + 0.125*ecc**2*R*(3*math.sin(3*alpha-2*beta)-10*math.sin(alpha)+5*math.sin(alpha-2*beta))
    z = -math.sqrt(3)*ecc*R*math.cos(alpha-beta) + math.sqrt(3)*ecc**2*R*(math.cos(alpha-beta)**2 + 2*math.sin(alpha-beta)**2)
    rtnStr = str(round(x,6)) + "," + str(round(y,6)) + "," + str(round(z,6))
    return rtnStr

# data format: x0,y0,z0,x1,y1,z1,x2,y2,z2\n"
# time in years
fileStr = ""
t_max = 1
dt = 0.001
for i in range(math.floor(t_max/dt)):
    temp = ""
    for n in range(3):
        temp += model(i*dt, n)
        if(n < 2):
            temp += ","
    fileStr += temp + "\n"
# print(fileStr)
with open("./cappy/plots/exportpy.csv","w") as file:
    file.write(fileStr)