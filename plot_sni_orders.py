
import numpy as np
from matplotlib import pyplot as plt

import utils_plot

circuits = [
        'SNI_H*',
        ]

kind_d = {
        2: '.-',
        3: '.-',
        4: '.-',
        5: '.-',
        6: '.-',
        7: '.-',
        8: '.-',
        16: '-',
        32: '-',
        }

for i, circuit in enumerate(circuits):
    for d, kind in kind_d.items():
        utils_plot.plot_line(circuit, d, utils_plot.colors[i], kind,
                label=utils_plot.LABEL_NAME,
                obs_mis = np.logspace(-1.32, -1.22, 100)
                )

utils_plot.setup_plot()
utils_plot.display()
