/**
 * blah blah file description
 * 
 * author: Nick Ford
*/
/**
 * Function adapted from a matlab program found at this url:
 * https://www.matlab-monkey.com/astro/keplerEquation/KeplerEquationPub.html
 * 
 * @param N number of divisions for the ellipse
 * @param e eccentricity of the ellipse
 * @param a semi-major axis of the ellipse (AU)
 * 
 * @return pointer to an array of true anomaly values for the elliptical orbit
 */
double* getThetas(int N, double e, double a, double period);

/**
 * function to give asteroid model position data from a time and n value
*/
char* model(double theta, double const a, double const ecc, double* const rotMatrix);

int main();