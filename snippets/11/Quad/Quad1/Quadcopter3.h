// Only modify this file to include
// - function definitions (prototypes)
// - include files
// - extern variable definitions
// In the appropriate section

#ifndef Quadcopter_H_
#define Quadcopter_H_
#include "Arduino.h"

#include "IMU.h"
#include "IR.h"
#include "Motors.h"
#include "MemoryFree.h"
#include "PID_v1.h"

//end of add your includes here
#ifdef __cplusplus
extern "C" {
#endif
void loop();
void setup();
#ifdef __cplusplus
} // extern "C"
#endif

//add your function definitions for the project Quadcopter here

void initRunLoop();
void runLoop();


//Do not add code below this line
#endif /* Quadcopter_H_ */
