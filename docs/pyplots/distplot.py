import numpy as np
import matplotlib.pyplot as plt
from relpy import statBox

x = np.random.randn(100)
distobj = statBox.dist(x, use_BIC=True)
distobj.plot()