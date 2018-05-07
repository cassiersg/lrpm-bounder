
import numpy as np
from matplotlib import pyplot as plt

import muls_gen
import librfactor_python


def compute_target_mis(obs_mi, c, ns_obs, tol=1e-3, var_name='x'):
    abs_c_idx, var_map = c.to_lkm()
    v = c.fmt_var([var for var in c.vars if var.name == var_name][0])
    x_idx = var_map[v]
    pfg = librfactor_python.PyFactorGraph(*abs_c_idx)
    return [pfg.bp_mi(obs_mi, n_obs, tol, 1.0, 1.0, 1000)[0][x_idx] for n_obs in ns_obs]

circuit = 'isw'
color_d = {2: 'g', 3: 'b', 4: 'r'}
kind_mi = {1e-3: '.-', 1e-2: "-", 1e-1: '*-'}
ns_obs = 2**np.arange(30)
res = dict()
for obs_mi in kind_mi.keys():
    for d in range(2, 4+1):
        c = muls_gen.muls[circuit](d)
        target_mis = np.array(compute_target_mis(obs_mi, c, ns_obs))
        plt.loglog(ns_obs, target_mis, color_d[d]+kind_mi[obs_mi], label=f'{d} shares {obs_mi} obs-mi')
plt.xlabel('n_obs')
plt.ylabel('target-mi')
plt.legend()
plt.title(f'ISW')
#plt.show()

