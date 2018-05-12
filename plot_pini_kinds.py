
from matplotlib import pyplot as plt

import utils_plot

circuits = [
        'pini2',
        'pini1',
        'pini2_hp',
        'pini3_hp',
        'isw_hp',
        ]

for circuit in circuits:
    utils_plot.plot_line(circuit)

utils_plot.setup_plot()
utils_plot.display()
