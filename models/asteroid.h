#ifndef __ASTEROID__
#define __ASTEROID__
/**
 * blah blah file description
 * 
 * author: Nick Ford
*/


/**
 * Calculates the eccentric anomaly from the mean anomaly and eccentricity. 
 * Function adapted from a matlab program found here:
 * https://www.matlab-monkey.com/astro/keplerEquation/KeplerEquationPub.html
 * 
 * @param M the mean anomaly
 * @param e the eccentricity of the orbit
 * 
 * @return the eccentric anomaly
*/
double besselApprox(double M, double e);

/**
 * Finds the sign of the input. Helper function for bisection
 * @param x the value to find the sign of
 * 
 * @returns the +1/-1 for positive/negative, respectively 
*/
int sign(float x);

/**
 * Function to calculate the bisection of
 * @param E the input eccentric anomaly
 * @param ecc the orbital eccentricity
 * @param M the mean anaomaly
 * 
 * @returns the +1/-1 for positive/negative, respectively 
*/
float f(float E ,float ecc, float M);

/**
 * root finding function, specifically for finding the eccentric anomaly
 * @param M the mean anomaly
 * @param ecc the orbital eccentricity
 * @param a left guess bound
 * @param b right guess bound
 * @param tol tolerence for checking if the root was found
 * 
 * @returns the root that was found
*/
double bisection(double M, double ecc, double a, double b, double tol);

/**
 * Calculates the true anomaly value for a given time and set of orbital parameters
 * 
 * @param t time to find the position at
 * @param N number of divisions for the ellipse
 * @param e eccentricity of the ellipse
 * 
 * @return the true anomaly value at the given time for the elliptical orbit
 */
double getTheta(double t, double e, double period);

/**
 * function to give asteroid model position data from a time and n value
*/
char* model(double theta, double const a, double const ecc, double* const rotMatrix);

int main();
#endif