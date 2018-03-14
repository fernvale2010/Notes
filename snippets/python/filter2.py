

import numpy as np
import scipy as sp
from scipy.signal import lfilter
import matplotlib.pyplot as plt

mu, sigma = 0, 500

x = np.arange(1, 100, 0.1)  # x axis
z = np.random.normal(mu, sigma, len(x))  # noise, mean and standard deviation for normal distribution
y = x ** 2 + z # data
plt.plot(x, y, linewidth=2, linestyle="-", c="b")  # it include some noise




n = 15  # the larger n is, the smoother curve will be
b = [1.0 / n] * n
a = 1
yy = lfilter(b,a,y)
plt.plot(x, yy, linewidth=2, linestyle="-", c="b")  # smooth by filter

