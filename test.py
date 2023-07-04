from mwplotlib import MilkyWay
import matplotlib.pyplot as plt

plt = MilkyWay.mw_plt(plt)
# plt.MilkyWay.scatter()
# plt.MilkyWay.shape(plot_type="polar", style="region", lw=1)
# plt.MilkyWay.shape(plot_type="polar", style="line", lw=1)
# plt.MilkyWay.shape(plot_type="cartesian", style="region", lw=1)
# plt.MilkyWay.shape(plot_type="cartesian", style="line", lw=1)
# plt.MilkyWay.shape(plot_type="cartesian", style="region", lw=1, unit="pc")
# plt.show()
# input()


plt.MilkyWay.shape(plot_type="polar", style="region", direction="ccw", lw=1)
plt.show()
plt.MilkyWay.shape(plot_type="polar", style="region", direction="cw", lw=1)
plt.show()
plt.MilkyWay.shape(plot_type="cartesian", style="region", direction="ccw", lw=1)
plt.show()
plt.MilkyWay.shape(plot_type="cartesian", style="region", direction="cw", lw=1)
plt.show()
input()

# using ax
fig = plt.figure()
ax1 = plt.subplot(121)
ax1 = MilkyWay.mw_plt(ax1)
ax1.set_title("Cartesian")
ax1.set_xlabel("X (kpc)")
ax1.set_ylabel("Y (kpc)")
ax1.MilkyWay.shape(plot_type="cartesian", style="region", lw=1)
ax2 = plt.subplot(122, projection='polar')
ax2 = MilkyWay.mw_plt(ax2)
ax2.set_title("Polar")
ax2.set_xlabel("R (kpc)")
ax2.set_ylabel("Theta (deg)")
ax2.MilkyWay.shape(plot_type="polar", style="region", lw=1)
plt.show()
# input()

# python setup.py sdist build
# python setup.py bdist_wheel --universal
# twine upload dist/*