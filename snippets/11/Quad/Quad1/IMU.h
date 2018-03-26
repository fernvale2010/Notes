/*
 * IMU.h
 *
 *  Created on: May 12, 2012
 *      Author: Thomas Teisberg
 */

#ifndef IMU_H_
#define IMU_H_

#include <FreeSixIMU.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>

#include "CommunicationUtils.h"
#include "FreeSixIMU.h"
#include <Wire.h>

class IMU {
public:
	IMU(int i);
	virtual ~IMU();
	void initIMU();

	void update();

	float getNS();
	float getEW();
	float getYaw();

	bool checkBeyondLimits();

	void zero();
	void zeroYaw();

	void printDebugStr();

	float ypr[3];

protected:
	FreeSixIMU imusensor;

private:
	float calibration[3];
	float oldyaw;
};

#endif /* IMU_H_ */
