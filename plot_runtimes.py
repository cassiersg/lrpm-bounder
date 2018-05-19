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
muls = ['SNI', 'SNI_H', 'SNI_H+', 'SNI_H*', 'PINI1', 'PINI2', 'PINI3_H+',
        'PINI3_H*', 'GreedyMult_H+', 'GreedyMult_H*']
costs = np.array(
        [[runtime_costs.cost_mul(d, mul) for d in ds] for mul in muls]
        )
y = (costs / costs[0,:]).transpose()
plt.plot(x, y, '.-', markersize=1)
plt.legend([mul.replace('_', '-') for mul in muls])
plt.xlabel('Order $d$')
plt.ylabel('Relative runtime cost')
utils_plot.display()

