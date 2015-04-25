import relpy as rp
import numpy as np
import matplotlib.pyplot as plt

f = 1000
hue = ['one' for i in range(50*f)] + ['two' for i in range(30*f)] + ['three' for i in range(20*f)]
rp.plotBox.scatter_plot(x = np.random.randn(100*f), y = np.random.randn(100*f), hue = hue, vlines = 0, alpha= .1, hlines = 0)
plt.show()