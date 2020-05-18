import numpy as np
import matplotlib.pyplot as plt

import os

path = os.path.join(os.path.dirname(__file__), "premier_ordre_vals.txt")

data = np.loadtxt(path, delimiter=",")

plt.plot(*data.transpose())
plt.show()
