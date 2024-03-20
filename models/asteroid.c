#define _USE_MATH_DEFINES
#define LINE_MAX 150
#define omega_EARTH 0 // argument of perihelion of Earth in degrees
#include "asteroid.h"
#include <stdbool.h>
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

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

float bisection(float M, float ecc, float a, float b, float tol){ 
    // # approximates a root, R, of f bounded 
    // # by a and b to within tolerance 
    // # | f(m) | < tol with m the midpoint 
    // # between a and b Recursive implementation
    // # check if a and b bound a root
    if (sign(f(a, ecc, M)) == sign(f(b, ecc, M))){
        perror("The scalars a and b do not bound a root\n");
        // return -10.0;
    }
        
    while(true){
        float m = (a + b)/2;
        if (fabs(f(m, ecc, M)) < tol){
            // # stopping condition, report m as root
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
    // i-th step around the ellipse

    // M varies from 0 to 2*pi/period over one period
    M = 2*M_PI*t/period;
    printf("%lf: ", M);
    // calculate eccentric anomaly from mean anomaly and eccentricity
    // anomaly = besselApprox(M, e);
    anomaly = bisection(M, e, 0, 2*M_PI, 0.001);
    // calculate theta from eccentric anomaly values
    theta = 2 * atan(sqrt((1+e)/(1-e)) * tan(anomaly/2));
    printf("%lf\n", theta);
    // theta must be freed somewhere 
    return theta;  
}

char* model(double theta, double const a, double const ecc, double* const rotMatrix){
    /** angular speed of the asteroid around the sun (for time sim).
     *  may have to calulate at every point
     */
    
    double r = a*(1-pow(ecc,2))/(1+ecc*cos(theta));
    double x = rotMatrix[0]*r*cos(theta) + rotMatrix[1]*r*sin(theta);
    double y = rotMatrix[3]*r*cos(theta) + rotMatrix[4]*r*sin(theta);
    double z = rotMatrix[6]*r*cos(theta) + rotMatrix[7]*r*sin(theta);
    // double x_flat = r*cos(theta);
    // double y_flat = r*sin(theta);

    
    char tempText[LINE_MAX];
    char* rtnStr = (char*) malloc(LINE_MAX);
    // snprintf(tempText, sizeof(tempText), "%.10lf,%.10lf", x_flat, y_flat);
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
    // double mass = 0.001; // derived mass of asteroid in kg

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
    double rotationMatrix[9] = {
        cos(Omega0)*cos(omega) - sin(Omega0)*cos(iota)*sin(omega),  // 1 1
        cos(Omega0)*sin(omega) + sin(Omega0)*cos(iota)*cos(omega),  // 1 2
        sin(Omega0)*sin(iota),                                       // 1 3
        -sin(Omega0)*cos(omega) - cos(Omega0)*cos(iota)*sin(omega), // 2 1
        -sin(Omega0)*sin(omega) + cos(Omega0)*cos(iota)*cos(omega), // 2 2
        cos(Omega0)*sin(iota),                                       // 2 3 
        sin(iota)*sin(omega),                                         // 3 1
        -sin(iota)*cos(omega),                                        // 3 2
        cos(iota)                                                     // 3 3   
    }; 

    printf("Constants Defined\nData Creation Started...\n");
    fflush(stdout);
    FILE* file = fopen("../plots/export_ast.csv", "w");
    // data format: x,y,z\n"
    // time in years
    double t_max = 1;
    double dt = 1.0/((double)365.0*24.0);
    printf("dt: %.12lf\n", dt);
    // double dt = 0.001;
    int N = (int)floor(t_max/dt);
    // double* thetas = getThetas(N, ecc, a, period);

    for(int i=0; i<N; i++){
        double theta = getTheta(i*dt, ecc, period);
        char* data_i = model(theta, a, ecc, rotationMatrix);
        fprintf(file, "%s\n", data_i);
        free(data_i);
    }
    fclose(file);
    printf("Data Creation Finished\n");
    return 0;
}