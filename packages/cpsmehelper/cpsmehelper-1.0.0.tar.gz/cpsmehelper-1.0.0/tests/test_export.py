import numpy as np
from matplotlib import pyplot as plt
from cpsmehelper import export_figure

# create plot 
data = np.random.randn(10)
fig, ax = plt.subplots()
ax.plot(data, data)
ax.plot(data, -data)
plt.xlabel('xlabel')
plt.ylabel('ylabel')
plt.legend(['some data', 'different data'])

# export figure to a .svg file with a set presentation style of one full PP textbox
export_figure(fig, name='test_presentation_1x1.svg', style='presentation_1x1')