import matplotlib.pyplot as plt
import numpy as np
from cpsmehelper import get_colors

cpsme_colors = get_colors()


# generate data
x = np.linspace(0, 10, 100)  # 100 points from 0 to 10
y = np.sin(x)                # sine function

# create the plot
plt.figure(figsize=(8, 5))
plt.plot(x, y, label='Sine Wave', color=cpsme_colors['red'], linestyle='-', marker='o')  # use cpsme red for plot

# add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Simple Sine Wave Plot')
plt.grid(True)
plt.legend()

# show the plot
plt.show()