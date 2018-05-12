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

ds = list(range(1, 32))
x = [d+1 for d in ds]
y = []
for d in ds:
    cmimo = runtime_costs.cost_mimo(d)
    cgreedy = runtime_costs.cost_greedy(d)
    cpini = runtime_costs.cost_pini1_sbox(d)
    cpini2 = runtime_costs.cost_pini2_sbox(d)
    c_isw_h = runtime_costs.cost_mimo_h(d, mul=runtime_costs.cost_isw_h_mul)
    c_isw_hp = runtime_costs.cost_mimo_h(d, mul=runtime_costs.cost_isw_hp_mul)
    c_isw_hps = runtime_costs.cost_mimo_h(d, mul=runtime_costs.cost_isw_hps_mul)
    y.append([1, cmimo/cgreedy, cpini/cgreedy, cpini2/cgreedy, c_isw_h/cgreedy,
        c_isw_hp/cgreedy, c_isw_hps/cgreedy])
y = np.array(y)
plt.plot(x, y, '.-')
plt.legend(['Greedy strategy', 'MIMO-SNI', 'PINI1', 'PINI2', 'MIMO ISW-H',
    'MIMO ISW-HP', 'MIMO ISW-HPS'])
plt.xlabel('Order $d$')
plt.ylabel('Relative runtime cost')
utils_plot.display()

