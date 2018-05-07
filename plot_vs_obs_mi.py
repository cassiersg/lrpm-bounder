
import numpy as np
from matplotlib import pyplot as plt

import muls_gen
import librfactor_python

import obs_mi

color_circuit = [
        #'BBP15',
        #'pini1',
        #'pini2',
        #'pini3',
        #'pini4',
        'pini5',
        'pini5dr',
        'pini5drt',
        #'pini5drbat',
        'pini5drbatt',
        #'bat_simple_ref',
        #'bat_bat_ref',
        #'bat_half_ref', 'bat_half1_ref', 'bat_isw_ref',
        ]
color_circuit = {k: f'C{i}' for i, k in enumerate(color_circuit)}
kind_d = {
        #2: '.-',
        4: '+-',
        #8: '*-',
        16: '+-',
        32: '+-',
        }
obs_mis = np.logspace(-3, -1, 30)
res = dict()
for circuit in color_circuit.keys():
    for d in kind_d.keys():
        target_mis = obs_mi.compute_target_mis(obs_mis, circuit, d)
        plt.loglog(
                obs_mis,
                target_mis,
                color_circuit[circuit]+kind_d[d],
                label=f'{d} shares {circuit.upper().replace("_", "-")}'
                )
        target_mis = obs_mi.lb_mi(obs_mis, circuit, d)
        plt.loglog(
                obs_mis,
                target_mis,
                color_circuit[circuit]+kind_d[d],
                label=f'{d} shares {circuit.upper().replace("_", "-")} LB'
                )
plt.xlabel('obs-mi')
plt.ylabel('target-mi')
plt.legend()
plt.title(f'1 obs')
plt.ylim(1e-42, 1e1)
#plt.show()

