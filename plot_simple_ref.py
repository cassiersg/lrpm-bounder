
from matplotlib import pyplot as plt

import utils_plot

circuits = [
        'pini3_hps',
        'pini3_hp',
        'isw_hps',
        'isw_hp',
        ]
for circuit in circuits:
    utils_plot.plot_line(circuit)

utils_plot.setup_plot()
utils_plot.display()
