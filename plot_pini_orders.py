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

circuits = [
        'PINI3_H+',
        'SNI_H+',
        'GreedyMult_H+',
        ]

kind_d = {
        2: '-',
        4: '-',
        8: '-',
        16: '-',
        32: '-',
        }

for i, circuit in enumerate(circuits):
    for d, kind in kind_d.items():
        utils_plot.plot_line(circuit, d, utils_plot.colors[i], kind,
                label=utils_plot.LABEL_NAME)

utils_plot.setup_plot()
utils_plot.display()
