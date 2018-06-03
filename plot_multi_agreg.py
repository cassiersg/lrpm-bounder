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

import numpy as np
from matplotlib import pyplot as plt

import utils_plot

circuits = [
        'SNI',
        'SNI_H+',
        'SNI_H+ naive',
        #'SNI_hpe',
        #'SNI_hpb',
        #'SNI_H',
        #'SNI_ht',
        ]

obs_mis = np.logspace(-2.5, -1.0, 100)

for circuit in circuits:
    utils_plot.plot_line(circuit, obs_mis=obs_mis)

utils_plot.setup_plot()
utils_plot.display()
