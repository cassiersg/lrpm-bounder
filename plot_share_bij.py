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

import itertools as it

from matplotlib import pyplot as plt

import utils_plot

circuits = [
        ('SNI', 'SNIb'),
        ('SNI_H', 'SNI_Hb'),
        ('SNI_H*', 'SNI_H*b'),
        ]

if 0:
    for i, (c, cb) in enumerate(circuits):
        utils_plot.plot_line(c, color=f'C{i}')
        utils_plot.plot_line(cb, color=f'C{i}', kind='^-', label=None,
                markevery=5)

    utils_plot.setup_plot()
    utils_plot.display()
    #plt.show()
else:
    for i, circuit in enumerate(circuits[1]):
        for d in [2, 4, 8, 16, 32]:
            utils_plot.plot_line(circuit, d, utils_plot.colors[i],
                    label=utils_plot.LABEL_NAME)
    utils_plot.setup_plot()
    plt.show()

