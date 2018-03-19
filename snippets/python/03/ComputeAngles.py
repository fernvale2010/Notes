import math
import numpy as np 

gyro_scale = 131.0
accel_scale = 16384.0

    
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


print('rotation_x,', 'gyro_total_x,', 'last_x,', 'rotation_y,', 'gyro_total_y,', 'last_y')
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

    # //sg: complementary filter on accelerometer and gyro
    last_x = K * (last_x + gyro_x_delta) + (K1 * rotation_x)
    last_y = K * (last_y + gyro_y_delta) + (K1 * rotation_y)
    
    print("{0:.2f}, {1:.2f}, {2:.2f}, {3:.2f}, {4:.2f}, {5:.2f}".format((rotation_x), (gyro_total_x), (last_x), (rotation_y), (gyro_total_y), (last_y)))

