#!/usr/bin/python
# Attempt to simulate gyro unbiasing with KF
#
# https://groups.google.com/forum/#!topic/diyrovers/SG_qLADU5k8
#

import numpy as np
import Gnuplot
import Gnuplot.funcutils

# Simulate heading/gyro measurements
dt = 0.050
x = np.matrix('250.0; 0.0; 0.0')
z = np.matrix('0.0; 0.0')
A = np.matrix('1.0, 0.010, 0.0; 0.0, 1.0, 0.0; 0.0, 0.0, 1.0')
H = np.matrix('0.0, 0.0, 0.0; 0.0, 0.0, 0.0')
K = np.matrix('0.0, 0.0; 0.0, 0.0; 0.0, 0.0')
Q = np.matrix('1.0, 0.0, 0.0; 0.0, 0.01, 0.0; 0.0, 0.0, 0.0001')
R = np.matrix('1.0, 0.0; 0.0, 0.01')
P = np.matrix('1.0, 0.0, 0.0; 0.0, 1000.0, 0.0; 0.0, 0.0, 1000.0')
I = np.matrix('1.0, 0.0, 0.0; 0.0, 1.0, 0.0; 0.0, 0.0, 1.0')

def kf():
    global x, z, A, H, K, P, Q, R
    x = A * x
    P = A * P * A.T + Q
    tmp = H*P*H.T + R
    K = P * H.T * np.linalg.inv(tmp)
    x = x + K * (z - H * x)
    P = (I - K * H) * P

for i in range(0, 500):
    z[0] = 250.0
    z[1] = 0
    H = np.matrix("1.0, 0.0, 0.0; 0.0, 0.0, 0.0")
    kf()
    for j in range(0, 5):
        z[0] = 0.0
        z[1] = np.random.normal(loc=2.0, scale=0.2, size=None)
        H = np.matrix('0.0, 0.0, 0.0; 0.0, 1.0, 1.0')
        kf()
        print "{0} {1} {2} {3}".format(x.item(0), z.item(1), x.item(1), x.item(2))

# And the results it spit out looks (more or less) like this:
# 
# Heading       Gyro Meas.   Gyro Estimate  Bias estimate
# ------------- -----------  -------------- -------------
# 250.000803122 2.068865221  0.059612669932 1.99414280292
# 250.001096855 1.984590479  0.016170658023 1.99370628247
# 250.002010814 2.196609645  0.131137258287 1.99485809281
# 250.003306030 2.121820431  0.128574296969 1.99483244498
# 250.005630843 2.396441600  0.296119221915 1.99650834720
# 250.003423340 2.161971804  0.202052218422 1.99581619362
# 250.003479512 1.748572189 -0.080147381578 1.99298057953
# 250.004171524 2.283563084  0.148101634804 1.99526731895
# 250.003521646 1.592751190 -0.189919752743 1.99188470709
# 250.001741991 1.833376847 -0.170644179744 1.99207751484
# 249.999908724 2.158480786  0.071353215462 1.99452645037
# 250.001422094 2.248822533  0.186258274093 1.99568103552
# 250.000634635 1.524116374 -0.218746687000 1.99162346017
# 250.000032581 2.182543527  0.032745611072 1.99414016393
# 249.999867536 1.897471796 -0.046667895640 1.99334581497
# 
# Note the gyro measurement versus the gyro estimate. The estimate centers around 0--unbiased. 
# The bias term is a close match to the 2.0 I set in the np.random.normal() call. Of course now
# I have to test it on the actual robot... 




