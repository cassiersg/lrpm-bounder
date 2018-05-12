
import numpy as np
from matplotlib import pyplot as plt
import matplotlib2tikz

import muls_gen
import refs_gen

import obs_mi

obs_mis = np.logspace(-3, -0.5, 30)
#obs_mis = np.linspace(10**-2.3, 10**-1.1, 100)


for d in [2, 4, 8, 16]:
    ref1 = refs_gen.ref_generator(d, refs_gen.bat_ref, io_sums=True)
    target_mis = obs_mi.compute_target_mis2(obs_mis, ref1, var_name='s')
    plt.loglog(
            obs_mis,
            target_mis,
            #color_circuit[circuit]+kind_d[d],
            label=f'{d} shares'
            )

#for circuit in color_circuit.keys():
#    for d in kind_d.keys():
#        target_mis = obs_mi.compute_target_mis(obs_mis, circuit, d)
#        plt.loglog(
#                obs_mis,
#                target_mis,
#                color_circuit[circuit]+kind_d[d],
#                label=f'{d} shares {circuit.upper().replace("_", "-")}'
#                )

plt.xlabel('obs-mi')
plt.ylabel('target-mi')
plt.legend()
#plt.title(f'')
fname = __file__.split('.')[0]
#matplotlib2tikz.save(f'../pini_mul/figs/{fname}.tex', figureheight='\\figureheight', figurewidth='\\figurewidth')
plt.show()

