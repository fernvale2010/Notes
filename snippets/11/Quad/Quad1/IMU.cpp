/*
 * IMU.cpp
 *
 * Handles all data collection, zeroing, and calcualations associated with the
 * IMU.
 *
 * This code relies on the open-source FreeSixIMU library.
 *
 *  Created on: May 12, 2012
 *      Author: Thomas Teisberg
 */

#include "IMU.h"

IMU::IMU(int i) {
	imusensor = FreeSixIMU();
}

IMU::~IMU() {
	// TODO Auto-generated destructor stub
}
// Initializes the IMU, must call before doing anything else
void IMU::initIMU()
{
	// Initialize I2C
	Wire.begin();
	delay(5);
	imusensor.init();
	delay(5);
	update();

	calibration[0] = 0;
	calibration[1] = 0;
	calibration[2] = 0;

	oldyaw = ypr[0];
}

// Get new data
void IMU::update()
{

	imusensor.getYawPitchRoll(ypr);
	ypr[0] = ypr[0] - calibration[0]; // YAW
	ypr[1] = ypr[1] - calibration[1]; // EW
	ypr[2] = ypr[2] - calibration[2]; // NS



	ypr[0] += ((int)(oldyaw/360))*360;
	float tmpyaw;
	if(ypr[0] > oldyaw) tmpyaw = ypr[0] - 360;
	else tmpyaw = ypr[0] + 360;

	if(fabs(oldyaw - tmpyaw) < fabs(oldyaw - ypr[0])) ypr[0] = tmpyaw;

	oldyaw = ypr[0];
}

// Get tilt in degrees on the NS axis (to north = positive)
float IMU::getNS()
{
	return ypr[2];
}

// Get tilt in degress on the EW axis (to east = positive)
float IMU::getEW()
{
	return ypr[1];
}

// Get yaw in degrees (clockwise = positive)
float IMU::getYaw()
{
	return ypr[0];
}

// Print current sensor data
void IMU::printDebugStr(){
	Serial.print("YPR] ");
	Serial.print("NS :: ");
	Serial.print(getNS());
	Serial.print(" | EW :: ");
	Serial.print(getEW());
	Serial.print(" | YAW :: ");
	Serial.println(getYaw());
}

// Check if IMU data has passed allowed bounds (>30 degrees tilt)
bool IMU::checkBeyondLimits(){
	if(abs(getNS()) > 30) return true;
	if(abs(getEW()) > 30) return true;
	return false;
}

// Zero the IMU at the current orientation
void IMU::zero(){
	imusensor.getYawPitchRoll(calibration);
	oldyaw = ypr[0];
}

// Zero the yaw value at the current orientation
void IMU::zeroYaw(){
	float vals[3];
	imusensor.getYawPitchRoll(vals);
	calibration[0] = vals[0];
}

