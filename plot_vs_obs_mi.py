
from pprint import pprint

import numpy as np
from matplotlib import pyplot as plt

import abs2lkm
import muls_gen
import librfactor_python


def compute_target_mis(obs_mis, c, n_obs=1, tol=1e-3, var_name='x'):
    v = c.fmt_var([var for var in c.vars if var.name == var_name][0])
    s, var_map = abs2lkm.convert(c)
    x_name = var_map[v]
    return [librfactor_python.factor_mi(s, obs_mi, n_obs, tol, 1000)[0][x_name] for obs_mi in obs_mis]

color_circuit = {'isw': 'b', 'pini1': 'r', 'BBP15': 'g'}
kind_d = {1: '-', 2: '.-', 4: '+-', 8: '*-', 16: '+-'}
obs_mis = np.logspace(-3, -1, 30)
res = dict()
for circuit in color_circuit.keys():
    for d in kind_d.keys():
        c = muls_gen.muls[circuit](d)
        target_mis = compute_target_mis(obs_mis, c)
        plt.loglog(obs_mis, target_mis, color_circuit[circuit]+kind_d[d], label=f'{d} shares, {circuit.upper()}')
plt.xlabel('obs_mi')
plt.ylabel('target_mi')
plt.legend()
plt.title(f'1 obs')
plt.show()

