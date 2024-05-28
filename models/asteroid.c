#define _USE_MATH_DEFINES
#define LINE_MAX 150
#define omega_EARTH 0 // argument of perihelion of Earth in degrees
#include "asteroid.h"
#include <stdbool.h>
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
// #include <unistd.h>

double besselApprox(double M, double e){
    int kTerms = 10;    // number of terms to keep in infinite series defining
    double anomaly = M;
    // include first kTerms in infinite series
    for (int k = 1; k <=kTerms; k++) {
        anomaly += 2/k * jn(k,k*e) * sin(k*M);
    }
    return anomaly;
}

int sign(float x){
    // return (int) x/fabs(x);
    return (x > 0) - (x < 0);
}

float f(float E ,float ecc, float M){
    // M = E - e sin(E)
    return E - ecc * sin(E) - M;
}

double bisection(double M, double ecc, double a, double b, double tol){ 
    // # approximates a root, R, of f bounded 
    // # by a and b to within tolerance 
    // # | f(m) | < tol with m the midpoint 
    // # between a and b Recursive implementation
    // # check if a and b bound a root
    if (sign(f(a, ecc, M)) == sign(f(b, ecc, M))){
        perror("The scalars a and b do not bound a root\n");
        // return -10.0;
    }
    
    // keeps iterating until midpoint has a function value 
    // within the tolerance of zero
    while(true){
        double m = (a + b)/2;
        if (fabs(f(m, ecc, M)) < tol){
            // stopping condition, report m as root
            return m;
        }else if(sign(f(a, ecc, M)) == sign(f(m, ecc, M))){
            // root is in right half
            a = m;
        }else if (sign(f(b, ecc, M)) == sign(f(m, ecc, M))){
            // root is in left half
            b = m;
        }
    }
}

double getTheta(double t, double e, double period) {
    double M;           // mean motion (rad)
    double anomaly;       // eccentric anomaly (rad)
    double theta; // true anomaly (rad)

    // Calculate eccentric anomaly at each point in orbit

    // M varies from 0 to 2*pi/period over one period
    M = 2*M_PI*t/period;

    // calculate eccentric anomaly from mean anomaly and eccentricity
    anomaly = bisection(M, e, 0, 2*M_PI, 0.000001);

    // calculate theta from eccentric anomaly and eccentricity values
    double eccPart = sqrt((1.0+e)/(1.0-e));
    double tanPart = tan(anomaly/2.0);
    theta = 2.0 * atan(eccPart * tanPart);
    return theta;  
}

char* model(double theta, double const a, double const ecc, double* const rotMatrix){    
    // calculate the radial distance in the plane, before rotation
    double r = a*(1-pow(ecc,2))/(1+ecc*cos(theta));

    // apply rotation matrix to 3D vector <r cos(), r sin(), 0>
    double x = rotMatrix[0]*r*cos(theta) + rotMatrix[1]*r*sin(theta);
    double y = rotMatrix[3]*r*cos(theta) + rotMatrix[4]*r*sin(theta);
    double z = rotMatrix[6]*r*cos(theta) + rotMatrix[7]*r*sin(theta);
    
    // write position data to string for output
    char tempText[LINE_MAX];
    char* rtnStr = (char*) malloc(LINE_MAX);
    snprintf(tempText, sizeof(tempText), "%.10lf,%.10lf,%.10lf", x, y, z);
    snprintf(rtnStr, strlen(tempText), "%s", tempText);
    return rtnStr;
}

// pi * 10^7 seconds in a year

int main(){
    printf("Setting up Constants...\n");
    fflush(stdout);
    // this section will be read from a file eventually

    // fairly circular
    // double a = 1.084; // semimajor axis in AU
    // double ecc = 0.0028; // eccentricity of orbit
    // double longitude = 282.58; // longitude of perihelion in degrees
    // double Omega0 = 360 - omega_EARTH + longitude; // modified longitude of perihelion
    // double omega = 210.62; // argument of perihelion in degrees
    // double iota = 22.08; // inclination of orbital plane in degrees
    // double period = 1.13; // sidereal orbital period in years

    // high period
    double a = 17.79; // semimajor axis in AU
    double ecc = 0.9482; // eccentricity of orbit
    double longitude = 48.70; // longitude of perihelion in degrees
    double Omega0 = 360.0 - omega_EARTH + longitude; // modified longitude of perihelion
    double omega = 333.30; // argument of perihelion in degrees
    double iota = 19.67; // inclination of orbital plane in degrees
    double period = 75.0; // sidereal orbital period in years

    // the rotation matrix for the asteroid's orbital plane.
    // accessed as [3*row +col]
    double rotationMatrix[9] = {                                     // row col
        cos(Omega0)*cos(omega) - sin(Omega0)*cos(iota)*sin(omega),   // 0 0
        cos(Omega0)*sin(omega) + sin(Omega0)*cos(iota)*cos(omega),   // 0 1
        sin(Omega0)*sin(iota),                                       // 0 2
        -sin(Omega0)*cos(omega) - cos(Omega0)*cos(iota)*sin(omega),  // 1 0
        -sin(Omega0)*sin(omega) + cos(Omega0)*cos(iota)*cos(omega),  // 1 1
        cos(Omega0)*sin(iota),                                       // 1 2 
        sin(iota)*sin(omega),                                        // 2 0
        -sin(iota)*cos(omega),                                       // 2 1
        cos(iota)                                                    // 2 2   
    }; 

    printf("Constants Defined\nData Creation Started...\n");
    fflush(stdout);
    FILE* file = fopen("../plots/export_ast.csv", "w");
    if (file == NULL){
        printf("file open error: %d", errno);
        return 1;
    }else{
        // data format: "x,y,z\n"
        // time is in years
        double t_max = 1;
        double dt = 1.0/((double)365.0*24.0); // 1 hour converted to years
        int N = (int)floor(t_max/dt);

        for(int i=0; i<N; i++){
            // get the appropriate theta value
            double theta = getTheta(i*dt, ecc, period);
            // calculate the position data for that theta 
            char* data_i = model(theta, a, ecc, rotationMatrix);
            // write data to file
            int fpfOutput = fprintf(file, "%s\n", data_i);
            // error catching for file writing
            if (fpfOutput < 0){
                printf("File Printing Failed: %d\n",fpfOutput);
            }
            // free the malloced memory
            free(data_i);
        }
        fclose(file);
        printf("Data Creation Finished\n");
        return 0;
    }
}