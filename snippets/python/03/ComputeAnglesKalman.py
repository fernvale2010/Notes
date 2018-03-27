import math
import numpy as np 
import matplotlib.pyplot as plt

gyro_scale = 131.0
accel_scale = 16384.0


def kalman_xy(x, P, measurement, R,
              motion = np.matrix('0. 0. 0. 0.').T,
              Q = np.matrix(np.eye(4))):
    """
    Parameters:    
    x: initial state 4-tuple of location and velocity: (x0, x1, x0_dot, x1_dot)
    P: initial uncertainty convariance matrix
    measurement: observed position
    R: measurement noise 
    motion: external motion added to state vector x
    Q: motion noise (same shape as P)
    """
    return kalman(x, P, measurement, R, motion, Q,
                  F = np.matrix('''
                      1. 0. 1. 0.;
                      0. 1. 0. 1.;
                      0. 0. 1. 0.;
                      0. 0. 0. 1.
                      '''),
                  H = np.matrix('''
                      1. 0. 0. 0.;
                      0. 1. 0. 0.'''))

def kalman(x, P, measurement, R, motion, Q, F, H):
    '''
    Parameters:
    x: initial state
    P: initial uncertainty convariance matrix
    measurement: observed position (same shape as H*x)
    R: measurement noise (same shape as H)
    motion: external motion added to state vector x
    Q: motion noise (same shape as P)
    F: next state function: x_prime = F*x
    H: measurement function: position = H*x

    Return: the updated and predicted new values for (x, P)

    See also http://en.wikipedia.org/wiki/Kalman_filter

    This version of kalman can be applied to many different situations by
    appropriately defining F and H 
    '''
    # UPDATE x, P based on measurement m    
    # distance between measured and current position-belief
    y = np.matrix(measurement).T - H * x
    S = H * P * H.T + R  # residual convariance
    K = P * H.T * S.I    # Kalman gain
    x = x + K*y
    I = np.matrix(np.eye(F.shape[0])) # identity matrix
    P = (I - K*H)*P

    # PREDICT x, P based on motion
    x = F*x + motion
    P = F*P*F.T + Q

    return x, P


    
def twos_compliment(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

    
    
# logfname = r"putty-2018-03-18-100318.log"
logfname = r"putty-2018-03-16-194729.log"
# logfname = r"putty-2018-03-16-194830.log"
imu = np.genfromtxt(logfname, delimiter=',', names=True, dtype=None)

imuAX = imu['acc_x']
imuAY = imu['acc_y']
imuAZ = imu['acc_z']
imuGX = imu['gyro_x']
imuGY = imu['gyro_y']
imuGZ = imu['gyro_z']

K = 0.98
K1 = 1 - K

time_diff = 0.004  # 250Hz


# compute deg/sec
gyro_scaled_x = imuGX[0] / gyro_scale
gyro_scaled_y = imuGY[0] / gyro_scale
gyro_scaled_z = imuGZ[0] / gyro_scale

# compute g
accel_scaled_x = imuAX[0] / accel_scale
accel_scaled_y = imuAY[0] / accel_scale
accel_scaled_z = imuAZ[0] / accel_scale

gyro_x_delta = (gyro_scaled_x * time_diff)
gyro_y_delta = (gyro_scaled_y * time_diff)

last_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
last_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

# //sg: angle from gyro is obtained by summing the changes (ie, integration), so initial angles take from
# accelerometer
gyro_total_x = last_x
gyro_total_y = last_y


x = np.matrix('0. 0. 0. 0.').T 
P = np.matrix(np.eye(4))*1 # initial uncertainty
result = []
R = 0.1

print('rotation_x,', 'rotation_y,', 'gyro_total_x,', 'gyro_total_y,', 'last_x,', 'last_y,', 'kalman_x,', 'kalman_y')
fmtstr = "{0:.2f}, {1:.2f}, {2:.2f}, {3:.2f}, {4:.2f}, {5:.2f}, {6:.2f}, {7:.2f}"

for i in range(1, len(imuAX)):
    # compute deg/sec
    gyro_scaled_x = imuGX[i] / gyro_scale
    gyro_scaled_y = imuGY[i] / gyro_scale
    gyro_scaled_z = imuGZ[i] / gyro_scale

    # compute g
    accel_scaled_x = imuAX[i] / accel_scale
    accel_scaled_y = imuAY[i] / accel_scale
    accel_scaled_z = imuAZ[i] / accel_scale

    gyro_x_delta = (gyro_scaled_x * time_diff)
    gyro_y_delta = (gyro_scaled_y * time_diff)

    # //sg: angle from gyro is obtained by summing the changes (ie, integration), without correction will just keep increasing until saturation
    gyro_total_x += gyro_x_delta
    gyro_total_y += gyro_y_delta

    rotation_x = get_x_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)
    rotation_y = get_y_rotation(accel_scaled_x, accel_scaled_y, accel_scaled_z)

    # //sg: complementary filter on accelerometer and gyro, last_x, last_y, rotation_x, rotation_y are in degrees
    last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
    last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)
    
    # Kalman from kalman3.py
    meas = (rotation_x, rotation_y)
    x, P = kalman_xy(x, P, meas, R)
    result.append((x[:2]).tolist())
    kalman_x = x[0].item()
    kalman_y = x[1].item()
    #print(type(kalman_x), type(kalman_y))

    #
    #print(kalman_x, kalman_y)
    print(fmtstr.format((rotation_x), (rotation_y), (gyro_total_x), (gyro_total_y),  (last_x), (last_y), (kalman_x), (kalman_y)))

