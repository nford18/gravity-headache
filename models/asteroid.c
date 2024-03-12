#define _USE_MATH_DEFINES
#define LINE_MAX 150
#define omega_EARTH 0 // argument of perihelion of Earth in degrees
#include "asteroid.h"
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

double* getThetas(int N, double e, double a, double period) {
    int kTerms = 10;    // number of terms to keep in infinite series defining
    double M;           // mean motion (rad)
    double anomaly;       // eccentric anomaly (rad)
    double* theta = malloc(N*sizeof(double));  // preallocate space for true anomaly (rad) array
                            
    // Calculate eccentric anomaly at each point in orbit
    // i-th step around the ellipse
    for (int i=0; i<N; i++){
        // M varies from 0 to 2*pi over one orbit
        // TODO: must be adjusted based on the period
        M = i*2*M_PI/N;
        // initialize eccentric anomaly to mean anomaly
        anomaly = M;
        // include first kTerms in infinite series
        for (int k = 1; k <=kTerms; k++) {
            anomaly += 2/k * jn(k,k*e) * sin(k*M);
        }
        // calculate theta from eccentric anomaly values
        theta[i] = 2 * atan(sqrt((1+e)/(1-e)) * tan(anomaly/2));
    }  
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
    double a = 1.084; // semimajor axis in AU
    double ecc = 0.0028; // eccentricity of orbit
    double longitude = 282.58; // longitude of perihelion in degrees
    double Omega0 = 360 - omega_EARTH + longitude; // modified longitude of perihelion
    double omega = 210.62; // argument of perihelion in degrees
    double iota = 22.08; // inclination of orbital plane in degrees
    double period = 1.13; // sidereal orbital period in years
    // double H = 24.8; // absolute magnitude in ??

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
    printf("%.12lf", dt);
    // double dt = 0.001;
    int N = (int)floor(t_max/dt);
    double* thetas = getThetas(N, ecc, a, period);

    for(int i=0; i<N; i++){
        // printf("%d",i);
        char* data_i = model(thetas[i], a, ecc, rotationMatrix);
        fprintf(file, "%s\n", data_i);
        free(data_i);
    }
    free(thetas);
    fclose(file);
    printf("Data Creation Finished\n");
    return 0;
}