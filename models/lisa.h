#ifndef __LISA__
#define __LISA__
/**
 * This file contains all functions and logic
 * for simulating the lisa spacecraft orbits. 
 * 
 * author: Nicholas Ford
*/


/**
 * function to give LISA model position data from a time and n value
 * 
 * @param t time to find the position at
 * @param n index of the spacecraft (0, 1, or 2)
 * 
 * @return The formatted string holding a position value for a given spacecraft's orbit 
*/
char* model(double t, int n);

/**
 * Runs the simulation
 * 
 * @return success/failure of simulation (0/nonzero, respectively) 
*/
int main();

#endif