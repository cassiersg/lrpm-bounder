
from matplotlib import pyplot as plt

import utils_plot
import obs_mi

circuits = [
        'pini2',
        'pini1',
        'isw',
        ]

for i, circuit in enumerate(circuits):
    utils_plot.plot_line(circuit, color=utils_plot.colors[i])
    target_mis = obs_mi.lb2_mi(utils_plot.obs_mis, circuit, utils_plot.default_d)
    plt.loglog(
            utils_plot.obs_mis,
            target_mis,
            f'C{i}'+'-.',
            )

utils_plot.setup_plot()
utils_plot.display()

