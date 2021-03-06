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

from matplotlib import pyplot as plt

import obs_mi
import utils_plot

circuits = [
        'SNI',
        'SNI_H',
        ]

kind_d = {
        4: '-',
        16: '-',
        }

i = 0
for d in kind_d.keys():
    for circuit in circuits:
        utils_plot.plot_line(circuit, d, color=utils_plot.colors[i],
            kind=kind_d[d])
        target_mis = obs_mi.lb_mi(utils_plot.obs_mis, circuit, d)
        plt.loglog(
                utils_plot.obs_mis,
                target_mis,
                f'C{i}'+'-.',
                #label=f'{d} shares {circuit.replace("_", "-")} LB'
                )
        i += 1

plt.ylim(1e-30, None)
utils_plot.setup_plot()
utils_plot.display()

