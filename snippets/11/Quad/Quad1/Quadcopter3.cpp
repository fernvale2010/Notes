// Do not remove the include below
#include "Quadcopter3.h"

/*
 * Sensors
 */

IMU imu(1);
IR ir(1);
Motors motors(1);

/**
 * Controllers
 */

float nsOut, nsSet = 0;
PID* nsController = new PID(&imu.ypr[2], &nsOut, &nsSet, 7, 0.0, 1.1, REVERSE);

float ewOut, ewSet = 0;
PID* ewController = new PID(&imu.ypr[1], &ewOut, &ewSet, 10.0, 0.06, 1.5, REVERSE);

float yawOut, yawSet = 0;
PID* yawController = new PID(&imu.ypr[0], &yawOut, &yawSet, 2.0, 0.0, 0.0, DIRECT);

/*
 * Flight variables
 */

int initSpeed = 1000;
long lastWatchdog = 0;

/*
 * Debug
 */

void printPIDGains(){
	Serial.print("NS] P :: ");
	Serial.print(nsController->GetKp());
	Serial.print("   I :: ");
	Serial.print(nsController->GetKi());
	Serial.print("   D :: ");
	Serial.print(nsController->GetKd());
	Serial.print("   EW] P :: ");
	Serial.print(ewController->GetKp());
	Serial.print("   I :: ");
	Serial.print(ewController->GetKi());
	Serial.print("   D :: ");
	Serial.print(ewController->GetKd());
	Serial.print("   YAW] P :: ");
	Serial.print(yawController->GetKp());
	Serial.print("   I :: ");
	Serial.print(yawController->GetKi());
	Serial.print("   D :: ");
	Serial.print(yawController->GetKd());
	Serial.print("   ALT] P :: ");
	Serial.print(heightController->GetKp());
	Serial.print("   I :: ");
	Serial.print(heightController->GetKi());
	Serial.print("   D :: ");
	Serial.println(heightController->GetKd());
}

/*
 * Initializer functions
 */

void initControllers()
{
	nsController->SetOutputLimits(-1000, 1000);
	nsController->SetMode(AUTOMATIC);
	ewController->SetOutputLimits(-1000, 1000);
	ewController->SetMode(AUTOMATIC);
	yawController->SetOutputLimits(-300, 300);
	yawController->SetMode(AUTOMATIC);
	heightController->SetOutputLimits(-10, 10);
	heightController->SetMode(AUTOMATIC);
	heightController->SetSampleTime(12);
	heightSet = 110;
}

/**
 * Setup and Loop
 */

void setup()
{
	initControllers();
	imu.initIMU();
	ir.initIR();
	motors.initMotors();
	imu.update();

	Serial.begin(115200);

	while(true){
		Serial.print(".");
		imu.update();
		if(Serial.available()){ // Wait for initialization command from user
			if(Serial.read() == 'X') break;
		}
	}

//	Serial.println("Z - Enter run mode");
//	Serial.println("I - Increase base speed");
//	Serial.println("K - Decrease base speed");
//	Serial.println("O - Increase init speed");
//	Serial.println("L - Decrease init speed");
//	Serial.println("Q - Increase P gain");
//	Serial.println("A - Decrease P gain");
//	Serial.println("W - Increase I gain");
//	Serial.println("S - Decrease I gain");
//	Serial.println("E - Increase D gain");
//	Serial.println("D - Decrease D gain");
	Serial.println("Initialized.");

	imu.zero();

	lastWatchdog = millis();

}

bool inInitRun = false;

void loop()
{
	if(inInitRun){
		initRunLoop();
		return;
	} else {
		nsController->Compute();
		ewController->Compute();
		yawController->Compute();
	}

	lastWatchdog = millis();
	imu.update();
	ir.update();

	// Take user commands to adjust flight parameters (i.e. PID values)
	if(Serial.available()){
		lastWatchdog = millis();
		motors.stopAll();
		byte inpt = Serial.read();
		if(inpt == 'Z'){
			inInitRun = true;
		} else if(inpt == 'I'){
			testBase += 10;
			Serial.print("Base val: ");
			Serial.println(testBase);
		} else if(inpt == 'K'){
			testBase -= 10;
			Serial.print("Base val: ");
			Serial.println(testBase);
		} else if(inpt == 'O'){
			initSpeed += 10;
			Serial.print("Init speed: ");
			Serial.println(initSpeed);
		} else if(inpt == 'L'){
			initSpeed -= 10;
			Serial.print("Init speed: ");
			Serial.println(initSpeed);
		} else if(inpt == 'q'){ // P -- NS
			nsController->SetTunings(nsController->GetKp()+0.1, nsController->GetKi(), nsController->GetKd());
			printPIDGains();
		} else if(inpt == 'a'){
			nsController->SetTunings(nsController->GetKp()-0.1, nsController->GetKi(), nsController->GetKd());
			printPIDGains();
		} else if(inpt == 'w'){ // I
			nsController->SetTunings(nsController->GetKp(), nsController->GetKi()+0.01, nsController->GetKd());
			printPIDGains();
		} else if(inpt == 's'){
			nsController->SetTunings(nsController->GetKp(), nsController->GetKi()-0.01, nsController->GetKd());
			printPIDGains();
		} else if(inpt == 'e'){ // D
			nsController->SetTunings(nsController->GetKp(), nsController->GetKi(), nsController->GetKd()+0.1);
			printPIDGains();
		} else if(inpt == 'd'){
			nsController->SetTunings(nsController->GetKp(), nsController->GetKi(), nsController->GetKd()-0.1);
			printPIDGains();
		} else if(inpt == 'Q'){ // P -- EW
			ewController->SetTunings(ewController->GetKp()+0.1, ewController->GetKi(), ewController->GetKd());
			printPIDGains();
		} else if(inpt == 'A'){
			ewController->SetTunings(ewController->GetKp()-0.1, ewController->GetKi(), ewController->GetKd());
			printPIDGains();
		} else if(inpt == 'W'){ // I
			ewController->SetTunings(ewController->GetKp(), ewController->GetKi()+0.01, ewController->GetKd());
			printPIDGains();
		} else if(inpt == 'S'){
			ewController->SetTunings(ewController->GetKp(), ewController->GetKi()-0.01, ewController->GetKd());
			printPIDGains();
		} else if(inpt == 'E'){ // D
			ewController->SetTunings(ewController->GetKp(), ewController->GetKi(), ewController->GetKd()+0.1);
			printPIDGains();
		} else if(inpt == 'D'){
			ewController->SetTunings(ewController->GetKp(), ewController->GetKi(), ewController->GetKd()-0.1);
			printPIDGains();
		} else if(inpt == 'r'){ // P -- YAW
			yawController->SetTunings(yawController->GetKp()+0.1, yawController->GetKi(), yawController->GetKd());
			printPIDGains();
		} else if(inpt == 'f'){
			yawController->SetTunings(yawController->GetKp()-0.1, yawController->GetKi(), yawController->GetKd());
			printPIDGains();
		} else if(inpt == 't'){ // I
			yawController->SetTunings(yawController->GetKp(), yawController->GetKi()+0.1, yawController->GetKd());
			printPIDGains();
		} else if(inpt == 'g'){
			yawController->SetTunings(yawController->GetKp(), yawController->GetKi()-0.1, yawController->GetKd());
			printPIDGains();
		} else if(inpt == 'y'){ // D
			yawController->SetTunings(yawController->GetKp(), yawController->GetKi(), yawController->GetKd()+0.1);
			printPIDGains();
		} else if(inpt == 'h'){
			yawController->SetTunings(yawController->GetKp(), yawController->GetKi(), yawController->GetKd()-0.1);
			printPIDGains();
		} else if(inpt == 'C'){ // Zero
			imu.zero();
		} else if(inpt == 'V'){ // Tilt info
			imu.printDebugStr();
		}
	}

}


void initRunLoop()
{
		// Update sensor data
		ir.update();
		imu.update();

		// Check for user input
		if(Serial.available()){
			byte inpt = Serial.read();
			if(inpt == '.' || inpt  == 'o' || inpt == 'l'){ // Handle throttle
				lastWatchdog = millis();
				if(inpt == 'o') initSpeed += 10;
				if(inpt == 'l') initSpeed -= 10;
			}else if(inpt == 'Z'){
				Serial.println("Switching to run mode...");
				inInitRun = false;
				inRun = true;
				return;
			}else{ // Stop if the uer presses any other key
				Serial.println("Stopped. User control.");
				motors.stopAll();
				inInitRun = false;
				inRun = false;

				return;
			}
		}

		// Estop if the quadcopter has tilted too far
		if(imu.checkBeyondLimits()){
			Serial.println("Estopped. IMU.");
			motors.stopAll();
			inInitRun = false;
			inRun = false;
			return;
		}
		
		// Estop if we have received no user input within a set timeout
		if((millis() - lastWatchdog) > 500){
			Serial.println("Estopped. Watchdog.");
			motors.stopAll();
			inInitRun = false;
			inRun = false;
			return;
		}

		nsController->Compute();
		ewController->Compute();
		yawController->Compute();

		motors.setNS(initSpeed + yawOut, nsOut);
		motors.setEW(initSpeed - yawOut, ewOut);

}
