/********************************************************************
 * Complimentary Filter
 * http://www.hobbytronics.co.uk/accelerometer-gyro
 *
 * Here is the code for the complimentary filter. It takes as inputs, the angle calculated from the
 * accelerometer, and the rate of rotation in degrees/second from the gyro.
 * filterAngle is the calculated angle from the filter
 * dt is the time period between taking readings in seconds (e.g. dt=0.02 is a reading rate of 50 times per second)
 * timeConstant is a value which is used to determine how quickly the calculated angle is corrected by the accelerometer
 * value. Play around with this value to get the best response/accuracy required.
 *
 ********************************************************************/
float filterAngle;
float dt=0.02;

float comp_filter(float newAngle, float newRate) {

   float filterTerm0;
   float filterTerm1;
   float filterTerm2;
   float timeConstant;

   timeConstant=0.5; // default 1.0

   filterTerm0 = (newAngle - filterAngle) * timeConstant * timeConstant;
   filterTerm2 += filterTerm0 * dt;
   filterTerm1 = filterTerm2 + ((newAngle - filterAngle) * 2 * timeConstant) + newRate;
   filterAngle = (filterTerm1 * dt) + filterAngle;

   return previousAngle; // This is actually the current angle, but is stored for the next iteration
}
