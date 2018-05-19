
from matplotlib import pyplot as plt

import obs_mi
import utils_plot

circuits = [
        'SNI_H',
        'SNI',
        ]

kind_d = {
        4: '-',
        16: '-',
        }

i = 0
for d in kind_d.keys():
    for circuit in circuits:
        utils_plot.plot_line(circuit, d, color=utils_plot.colors[i],
            kind=kind_d[d])
        target_mis = obs_mi.lb_mi(utils_plot.obs_mis, circuit, d)
        plt.loglog(
                utils_plot.obs_mis,
                target_mis,
                f'C{i}'+'-.',
                #label=f'{d} shares {circuit.upper().replace("_", "-")} LB'
                )
        i += 1

plt.ylim(1e-30, None)
utils_plot.setup_plot()
utils_plot.display()

