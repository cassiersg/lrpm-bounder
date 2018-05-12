
from matplotlib import pyplot as plt

import utils_plot

circuits = [
        #'isw',
        'isw_h',
        #'isw_ht',
        'isw_hp',
        #'isw_hpt',
        ]

kind_d = [
        (2, '-'),
        (4, '-'),
        (8, '-'),
        (16, '-'),
        (32, '-'),
        ]


for i, circuit in enumerate(circuits):
    for d, kind in kind_d:
        utils_plot.plot_line(circuit, d, utils_plot.colors[i], kind,
                label=utils_plot.LABEL_NAME)

utils_plot.setup_plot()
utils_plot.display()
