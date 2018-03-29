
from pprint import pprint

import abs2lkm
import muls_gen
import librfactor_python

c = muls_gen.isw(3)
v = c.fmt_var([var for var in c.vars if var.name == 'x'][0])
s, var_map = abs2lkm.convert(c)
x_name = var_map[v]
mis, n_iter = librfactor_python.factor_mi(s, 0.01, 10, 1e-6, 100)
pprint(mis)
print('n_iter', n_iter)
print('x', mis[x_name])

