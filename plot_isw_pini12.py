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

import utils_plot
import obs_mi

circuits = [
        'PINI2',
        'PINI1',
        'SNI',
        ]

for i, circuit in enumerate(circuits):
    utils_plot.plot_line(circuit, color=utils_plot.colors[i])
    target_mis = obs_mi.lb2_mi(utils_plot.obs_mis, circuit, utils_plot.default_d)
    plt.loglog(
            utils_plot.obs_mis,
            target_mis,
            f'C{i}'+'-.',
            )

utils_plot.setup_plot()
utils_plot.display()

