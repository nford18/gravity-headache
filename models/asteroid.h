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