#ifndef __ASTEROID__
#define __ASTEROID__
/**
 * This file contains all functions and logic
 * for simulating the asteroid orbit. 
 * 
 * author: Nicholas Ford
*/


/**
 * Calculates the eccentric anomaly from the mean anomaly and eccentricity. 
 * Function adapted from a matlab program found here:
 * https://www.matlab-monkey.com/astro/keplerEquation/KeplerEquationPub.html
 * 
 * Function is no longer in use, but remains in code for solidarity.
 * 
 * @param M the mean anomaly
 * @param e the eccentricity of the orbit
 * 
 * @return The eccentric anomaly
*/
double besselApprox(double M, double e);

/**
 * Finds the sign of the input. Helper function for bisection
 * @param x the value to find the sign of
 * 
 * @returns The +1/-1 for positive/negative, respectively 
*/
int sign(float x);

/**
 * Function that the bisection method is applied to
 * @param E the input eccentric anomaly
 * @param ecc the orbital eccentricity
 * @param M the mean anaomaly
 * 
 * @returns The +1/-1 for positive/negative, respectively 
*/
float f(float E ,float ecc, float M);

/**
 * Root finding function, specifically for finding the eccentric anomaly
 * @param M the mean anomaly
 * @param ecc the orbital eccentricity
 * @param a left guess bound
 * @param b right guess bound
 * @param tol tolerence for checking if the root was found
 * 
 * @returns The root that was found
*/
double bisection(double M, double ecc, double a, double b, double tol);

/**
 * Calculates the true anomaly value for a given time and set of orbital parameters
 * 
 * @param t time to find the angle at
 * @param e eccentricity of the ellipse
 * @param period period of the elliptical orbit
 * 
 * @return The true anomaly value at the given time for the elliptical orbit
 */
double getTheta(double t, double e, double period);

/**
 * function to give asteroid model position data from a time and n value
 * 
 * @param t time to find the position at
 * @param a semimajor axis of the asteroid's orbit
 * @param ecc eccentricity of the asteroid's orbit
 * @param rotMatrix rotation matrix for the asteroid's orbital plane
 * 
 * @return The formatted string holding a position value for a given asteroid's orbit 
*/
char* model(double theta, double const a, double const ecc, double* const rotMatrix);

/**
 * Runs the simulation
 * 
 * @return success/failure of simulation (0/nonzero, respectively) 
*/
int main();
#endif