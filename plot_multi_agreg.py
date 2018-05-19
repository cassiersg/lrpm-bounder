
import numpy as np
from matplotlib import pyplot as plt

import utils_plot

circuits = [
        'SNI',
        'SNI_H+',
        'SNI_H+ naive',
        #'SNI_hpe',
        #'SNI_hpb',
        #'SNI_H',
        #'SNI_ht',
        ]

obs_mis = np.logspace(-2.5, -1.0, 100)

for circuit in circuits:
    utils_plot.plot_line(circuit, obs_mis=obs_mis)

utils_plot.setup_plot()
utils_plot.display()
