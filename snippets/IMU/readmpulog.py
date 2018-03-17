# https://stackoverflow.com/questions/16503560/read-specific-columns-from-a-csv-file-with-csv-module

import numpy as np 
import matplotlib.pyplot as plt


# Implements a linear Kalman filter.
# "Kalman Filters for Undergrads"
class KalmanFilterLinear:
  def __init__(self,_A, _B, _H, _x, _P, _Q, _R):
    self.A = _A                      # State transition matrix.
    self.B = _B                      # Control matrix.
    self.H = _H                      # Observation matrix.
    self.current_state_estimate = _x # Initial state estimate.
    self.current_prob_estimate = _P  # Initial covariance estimate.
    self.Q = _Q                      # Estimated error in process.
    self.R = _R                      # Estimated error in measurements.
  def GetCurrentState(self):
    return self.current_state_estimate
  def Step(self,control_vector,measurement_vector):
    #---------------------------Prediction step-----------------------------
    predicted_state_estimate = self.A * self.current_state_estimate + self.B * control_vector
    predicted_prob_estimate = (self.A * self.current_prob_estimate) * np.transpose(self.A) + self.Q
    #--------------------------Observation step-----------------------------
    innovation = measurement_vector - self.H*predicted_state_estimate
    innovation_covariance = self.H*predicted_prob_estimate*np.transpose(self.H) + self.R
    #-----------------------------Update step-------------------------------
    kalman_gain = predicted_prob_estimate * np.transpose(self.H) * np.linalg.inv(innovation_covariance)
    self.current_state_estimate = predicted_state_estimate + kalman_gain * innovation
    # We need the size of the matrix so we can make an identity matrix.
    size = self.current_prob_estimate.shape[0]
    # eye(n) = nxn identity matrix.
    self.current_prob_estimate = (np.eye(size)-kalman_gain*self.H)*predicted_prob_estimate



# imu = np.loadtxt(r"putty-2018-03-16-194830.log",skiprows=1,delimiter=',')
# imuT = imu.transpose() # rows to columns..
# imuT[0] => acc_x, 
# imuT[1] => acc_y,  .... acc_z, gyro_x, gyro_y, gyro_z

# another way
imu = np.genfromtxt(r"putty-2018-03-16-194830.log", delimiter=',', names=True,dtype=None)
# imu['acc_x'] => acc_x,
# imu['acc_y'] => acc_y

x = np.arange(len(imu['acc_x']))

A = np.matrix([1])
H = np.matrix([1])
B = np.matrix([0])
Q = np.matrix([0.00001])
R = np.matrix([0.1])
xhat = np.matrix([3])
P    = np.matrix([1])


kalman = []
filter = KalmanFilterLinear(A,B,H,xhat,P,Q,R)

# imu_channel = imu['acc_x'] # change this to check the other channels
# imu_channel = imu['acc_y'] # change this to check the other channels
# imu_channel = imu['acc_z'] # change this to check the other channels
# imu_channel = imu['gyro_x'] # change this to check the other channels
imu_channel = imu['gyro_y'] # change this to check the other channels
# imu_channel = imu['gyro_z'] # change this to check the other channels

for i in x:
    measured = imu_channel[i]
    kalman.append(filter.GetCurrentState()[0,0])
    filter.Step(np.matrix([0]),np.matrix([measured]))

fig, ax = plt.subplots()
ax.plot(x, imu_channel, 'grey')
ax.plot(x, kalman, 'blue')


# fig, ax = plt.subplots(4, sharex=True)
# ax[0].plot(x, imu['acc_x'], 'grey', label='acc_x')
# ax[1].plot(x, imu['acc_y'], 'green', label='acc_y')
# ax[2].plot(x, imu['gyro_x'], 'red', label='gyro_x')
# ax[3].plot(x, imu['gyro_y'], 'blue', label='gyro_y')

# Now add the legend with some customizations.
#legend = ax.legend(loc='upper center', shadow=True)

plt.show()












