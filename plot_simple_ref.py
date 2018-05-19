
from matplotlib import pyplot as plt

import utils_plot

circuits = [
        'PINI3_H*',
        'PINI3_H+',
        'SNI_H*',
        'SNI_H+',
        ]
for circuit in circuits:
    utils_plot.plot_line(circuit)

utils_plot.setup_plot()
utils_plot.display()
