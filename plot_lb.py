
import numpy as np
from matplotlib import pyplot as plt
import matplotlib2tikz

import muls_gen
import librfactor_python

import obs_mi

circuits = [
        'ISW',
        #'pini1',
        #'pini3',
        'bat_bat_ref',
        ]
color_circuit = {k: f'C{i}' for i, k in enumerate(circuits)}

kind_d = {
        #2: '.-',
        4: '-',
        #8: '+-',
        16: '-',
        #32: '+-',
        }

#obs_mis = np.logspace(-2.5, -1, 100)
obs_mis = np.linspace(10**-2.8, 10**-1.1, 100)
obs_mis2 = np.linspace(10**-2.8, 10**-1.1, 10)

i = 0
for circuit in color_circuit.keys():
    for d in kind_d.keys():
        target_mis = obs_mi.compute_target_mis(obs_mis, circuit, d)
        plt.loglog(
                obs_mis,
                target_mis,
                f'C{i}'+kind_d[d],
                label=f'{d} shares {circuit.upper().replace("_", "-")}'
                )
        target_mis = obs_mi.lb_mi(obs_mis, circuit, d)
        #target_mis = obs_mi.lb2_mi(obs_mis, circuit, d)
        plt.loglog(
                obs_mis,
                target_mis,
                f'C{i}'+'-.',
                #label=f'{d} shares {circuit.upper().replace("_", "-")} LB'
                )
        i += 1

plt.xlabel('obs-mi')
plt.ylabel('target-mi')
plt.ylim(1e-30, None)
plt.legend()
#plt.title(f'')
fname = __file__.split('.')[0]
matplotlib2tikz.save(f'../pini_mul/figs/{fname}.tex', figureheight='\\figureheight', figurewidth='\\figurewidth', externalize_tables=True, override_externals=True, tex_relative_path_to_data='figs')
plt.show()

