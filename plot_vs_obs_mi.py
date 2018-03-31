
from pprint import pprint

import numpy as np
from matplotlib import pyplot as plt

import abs2lkm
import muls_gen
import librfactor_python


def compute_target_mis(obs_mi, c, n_obs=1, tol=1e-3, var_name='x'):
    abs_c_idx, var_map = abs2lkm.circuit2abs_idx(c)
    v = c.fmt_var([var for var in c.vars if var.name == var_name][0])
    x_idx = var_map[v]
    pfg = librfactor_python.PyFactorGraph(*abs_c_idx)
    return [pfg.bp_mi(obs_mi, n_obs, tol, 1.0, 1.0, 10000)[0][x_idx]
            for obs_mi in obs_mis]

color_circuit = {'isw': 'b', 'pini1': 'r', 'BBP15': 'g', 'bat': 'k'}
kind_d = {1: '-', 2: '.-', 4: '+-', 8: '*-', 16: '+-', 32: '-'}
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
#plt.show()

