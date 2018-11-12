#! /usr/bin/python3

# Copyright 2018 Gaëtan Cassiers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
"""

import numpy as np
from matplotlib import pyplot as plt

import runtime_costs
import utils_plot
import obs_mi

ds = list(range(1, 32))
x = [d+1 for d in ds]
muls = [
        ('SNI', 'C0.-'),
        ('PINI1', 'C1.-'),
        ('GreedyMult', 'C2.-'),
        ('SNI_H', 'C0x-'),
        ('PINI3_H', 'C1x-'),
        ('GreedyMult_H', 'C2x-'),
        ('SNI_H*', 'C0v-'),
        ('PINI3_H*', 'C1v-'),
        ('GreedyMult_H*', 'C2v-'),
        ('SNI_H+', 'C0^-'),
        ('PINI3_H+', 'C1^-'),
        ('GreedyMult_H+', 'C2^-'),
        ('PINI2', 'C3.-'),
        ]

obs_mi_val = 10**-1

for mul, markinfo in muls:
    costs = [runtime_costs.cost_mul(d, mul) for d in ds]
    circuit = mul
    target_mis = obs_mi.compute_target_mis_orders(obs_mi_val, circuit, ds)
    plt.loglog(costs, target_mis, markinfo,
            #markersize=2,
            )
plt.legend([utils_plot.map_circ_name(mul) for mul, _ in muls])
plt.xlabel('Relative runtime cost')
plt.ylabel('Target MI')
plt.title('obs_mi = {:.3e} bit'.format(obs_mi_val))
#utils_plot.display()
plt.show()

