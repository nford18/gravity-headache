#define _USE_MATH_DEFINES
#define LINE_MAX 150
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

/**
 * Function adapted from a matlab program found at this url:
 * https://www.matlab-monkey.com/astro/keplerEquation/KeplerEquationPub.html
 */
double* getThetas() {
    double e = 0.4;     // eccentricity
    double a = 1;       // semi-major axis
    int N = 100;        // number of points defining orbit
    int kTerms = 10;    // number of terms to keep in infinite series defining
    double M;           // mean anomaly
    double alpha;       // eccentric anomaly
    double* theta = malloc(N*sizeof(double));  // preallocate space for true anomaly (theta) array
                            
    // Calculate eccentric anomaly at each point in orbit
    // i-th step around the ellipse
    for (int i=0; i<N; i++){
        // M varies from 0 to 2*pi over one orbit
        M = i*2*M_PI/N;
        // initialize eccentric anomaly to mean anomaly
        alpha = M;
        // include first kTerms in infinite series
        for (int k = 1; k <=kTerms; k++) {
            alpha += 2/k * jn(k,k*e) * sin(k*M);
        }
        // calculate theta from eccentric anomaly values
        theta[i] = 2 * atan(sqrt((1+e)/(1-e)) * tan(alpha/2));
    }  
    // theta must be freed somewhere 
    return theta;  
}

/**
 * function to give LISA model position data from a time and n value
*/
char* model(double theta, double const a, double const ecc, double* const rotMatrix){
    /** angular speed of the asteroid around the sun (for time sim).
     *  may have to calulate at every point
     */
    
    double r = a*(1-pow(ecc,2))/(1+ecc*cos(theta));
    double x = rotMatrix[0]*r*cos(theta) + rotMatrix[1]*r*sin(theta);
    double y = rotMatrix[3]*r*cos(theta) + rotMatrix[4]*r*sin(theta);
    double z = rotMatrix[6]*r*cos(theta) + rotMatrix[7]*r*sin(theta);

    
    // char tempText[LINE_MAX];
    // char* rtnStr = (char*) malloc(LINE_MAX);
    // snprintf(tempText, sizeof(tempText), "%.10lf,%.10lf,%.10lf", x, y, z);
    // snprintf(rtnStr, strlen(tempText), "%s", tempText);
    // return rtnStr;
}

int main(){
    printf("Setting up Constants...\n");
    double omega_earth = 0; // argument of perihelion of Earth
    // this section will be read from a file eventually
    double a = 1; // semimajor axis in AU
    double ecc = 0.00965; // eccentricity of orbit
    double longitude = 0; // longitude of perihelion
    double Omega_0 = 2.0*M_PI - omega_earth + longitude; // modified longitude of perihelion
    double omega = 0; // argument of perihelion
    double iota = 0; // inclination of orbital plane

    // the rotation matrix for the asteroid's orbital plane.
    // accessed as [3*row +col]
    double rotationMatrix[9] = {
        cos(Omega_0)*cos(omega) - sin(Omega_0)*cos(iota)*sin(omega),  // 1 1
        cos(Omega_0)*sin(omega) + sin(Omega_0)*cos(iota)*cos(omega),  // 1 2
        sin(Omega_0)*sin(iota),                                       // 1 3
        -sin(Omega_0)*cos(omega) - cos(Omega_0)*cos(iota)*sin(omega), // 2 1
        -sin(Omega_0)*sin(omega) + cos(Omega_0)*cos(iota)*cos(omega), // 2 2
        cos(Omega_0)*sin(iota),                                       // 2 3 
        sin(iota)*sin(omega),                                         // 3 1
        -sin(iota)*cos(omega),                                        // 3 2
        cos(iota)                                                     // 3 3   
    }; 

    printf("Data Creation Started...\n");
    FILE* file = fopen("export.csv", "w");
    // data format: x,y,z\n"
    // time in years
    double t_max = 1;
    double dt = 1/365/24/3600; // 0.001;

    for(int i=0; i<(int)floor(t_max/dt); i++){
        char temp[100];
        strcpy(temp, "");
        for (int n=0; n<3; n++){
            char* data_i_n = model(i*dt, a, ecc, rotationMatrix);

            strcat(temp, data_i_n);
            free(data_i_n);
            if (n<2){
                strcat(temp, ",");
            }
        }
        fprintf(file, "%s\n", temp);
    }
    fclose(file);
    printf("Data Creation Finished...\n");
    return 0;
}