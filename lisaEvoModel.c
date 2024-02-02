// BUILDING FROM PYTHON EXAMPLE FROM PAST HW

// Includes
// Set constants for accel()

// def accel(x_a, x_b, x_c):
//     float acc[3] = {0,0,0};
//     acc[0] = (LISA orbit contribution) + (asteroid contribution);
//     acc[1] = (LISA orbit contribution) + (asteroid contribution);
//     acc[2] = (LISA orbit contribution) + (asteroid contribution);
//     return acc;


// print("V-V Evolution Started...")
// float t = 0; // yrs
// float dt = 0.001; // yrs
// float t_max = 1; 
// pos = [[-b+0.025],[0.0],[b-0.025]]
// v = [[0],[0],[0]]
// time = [0]

// while(t <= t_max){
//     acc = accel(pos[0][t],pos[1][t],pos[2][t])
//     acc_next = accel(pos[0][t] + v[0][t]*dt + acc[0]/2*dt**2, pos[1][t] + v[1][t]*dt + acc[1]/2*dt**2, pos[2][t] + v[2][t]*dt + acc[2]/2*dt**2)
//     for i in range(3){}
//         pos[i].append(pos[i][t] + v[i][t]*dt + acc[i]/2*dt**2)
//         v[i].append(v[i][t] + dt/2*(acc_next[i]+acc[i]))
//     }
//     time.append(t*dt)
//     t += 1
// }
// print("Evolution Completed.")