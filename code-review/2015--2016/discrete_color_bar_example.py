from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
%config InlineBackend.figure_format='retina'
%matplotlib inline

"""
Log scale discrete colormaps with matplotlib which you can happily copy-paste in jupyter notebook
(inspired by http://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar)
"""

x = [  6.23343507e-03,   2.81348181e-02,   4.68303411e-03,   3.42539566e-01,   3.45920197e-03,   2.90532859e-04,   3.08496503e-05,   2.63339694e-03,   2.63879760e-07]
y = [ 0.80633933,  0.40211565,  0.68903025,  0.4414968,   0.45019223,  0.35095171,  0.37928863,  0.2779556,   0.27843539]
z = [ 4.25201185,  4.11153144,  4.23549925,  4.0512849,   4.05836118,  4.01689744,  4.02224028,  3.96961677,  3.96906273]

nbins = 8
log_x = np.log10(x)
new_range =  (log_x - np.min(log_x))*(nbins/(np.max(log_x)-np.min(log_x)))

# setup the plot
fig, ax = plt.subplots(1,1, figsize=(6,6))

# define the colormap
cmap = plt.cm.YlGnBu
# extract all colors from the .YlGnBu map
cmaplist = [cmap(i) for i in range(cmap.N)]
# create the new map
cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

# define the bins and normalize
bounds = np.linspace(0,nbins,nbins+1)

myticks = [10**-i for i in range(nbins+1)][::-1]

norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# make the scatter
scat = ax.scatter(y,z,c=new_range,s=100,cmap=cmap, norm=norm)

# create a second axes for the colorbar
ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cbar = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')
cbar.ax.set_yticklabels(myticks)

ax.set_title('Well defined discrete colors')
ax2.set_ylabel('Very custom cbar [-]', size=12)