
import numpy as np
from matplotlib import pyplot as plt
import matplotlib2tikz

import muls_gen
import librfactor_python

import obs_mi

circuits = [
        'pini1',
        'pini2',
        'pini4dr',
        #'pini5h',
        #'pini5',
        #'pini5bat',
        #'bat_bat_ref',
        #'pini5hdr',
        #'pini5dr',
        #'pini5drbat',
        'pini6drbat',
        'bat2_bat_ref',
        ]
color_circuit = {k: f'C{i}' for i, k in enumerate(circuits)}

kind_d = {
        #2: '.-',
        #4: '+-',
        #8: '*-',
        16: '-',
        #32: '+-',
        }

obs_mis = np.logspace(-2.3, -1, 30)
obs_mis = np.linspace(10**-2.3, 10**-1.1, 100)

for circuit in color_circuit.keys():
    for d in kind_d.keys():
        target_mis = obs_mi.compute_target_mis(obs_mis, circuit, d)
        plt.loglog(
                obs_mis,
                target_mis,
                color_circuit[circuit]+kind_d[d],
                label=f'{d} shares {circuit.upper().replace("_", "-")}'
                )

plt.xlabel('obs-mi')
plt.ylabel('target-mi')
plt.legend()
#plt.title(f'')
fname = __file__.split('.')[0]
matplotlib2tikz.save(f'../pini_mul/figs/{fname}.tex', figureheight='\\figureheight', figurewidth='\\figurewidth')
plt.show()

