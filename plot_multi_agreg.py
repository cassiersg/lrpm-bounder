
import numpy as np
from matplotlib import pyplot as plt

import utils_plot

circuits = [
        'isw',
        'isw_hp',
        'isw_hpt',
        #'isw_hpe',
        #'isw_hpb',
        #'isw_h',
        #'isw_ht',
        ]

obs_mis = np.logspace(-2.5, -1.0, 100)

for circuit in circuits:
    utils_plot.plot_line(circuit, obs_mis=obs_mis)

utils_plot.setup_plot()
utils_plot.display()
