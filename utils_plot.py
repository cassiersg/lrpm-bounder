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
import matplotlib2tikz
import sys

import muls_gen
import obs_mi

colors = [f'C{i}' for i in range(20)]

obs_mis = np.logspace(-2.5, -1.2, 100)

default_d = 16

LABEL_SHARES_NAME = 0
LABEL_NAME = 1
LABEL_SHARES = 2
LABEL_NONE = 3

n_plots = 0
seen_names = set()
seen_shares = set()
def setup_plot():
    global n_plots
    global seen_names
    global seen_shares
    n_plots = 0
    seen_names = set()
    seen_shares = set()
    plt.xlabel('Observation MI (bits)')
    plt.ylabel('Target MI (bits)')
    plt.ylim(max(plt.gca().get_ylim()[0], 10**-28), 10**1.1)
    plt.legend()
    #plt.title(f'')

circ_names_map = {
        'SNI': r'\sni',
        'SNI_H': r'\snih',
        'SNI_H+': r'\snihp',
        'SNI_H*': r'\snihs',
        'SNI_H+ naive': r'\snihp naive',
        'PINI1': r'\pinia',
        'PINI2': r'\pinib',
        'PINI2_H': r'\pinibh',
        'PINI2_H+': r'\pinibhp',
        'PINI3': r'\pinic',
        'PINI3_H': r'\pinich',
        'PINI3_H+': r'\pinichp',
        'PINI3_H*': r'\pinichs',
        'GreedyMult': r'\greedymult',
        'GreedyMult_H': r'\greedymulth',
        'GreedyMult_H+': r'\greedymulthp',
        'GreedyMult_H*': r'\greedymulths',
        }
def map_circ_name(circuit):
    return circ_names_map.get(circuit, circuit)

def plot_line(circuit, d=None, color=None, kind='-', label=LABEL_SHARES_NAME,
        obs_mis=obs_mis, **kwargs):
    global n_plots
    global seen_names
    global seen_shares
    if label == LABEL_SHARES_NAME and d is None:
        label = LABEL_NAME
    if label == LABEL_SHARES_NAME:
        label = f"{d} shares {map_circ_name(circuit)}"
    elif label == LABEL_NAME and circuit not in seen_names:
        seen_names.add(circuit)
        label = map_circ_name(circuit)
    elif label == LABEL_SHARES and d not in seen_shares:
        seen_shares.add(d)
        label = f"{d} shares"
    else:
        label = None
    if d is None:
        d = default_d
    if color is None:
        color = colors[n_plots]
    target_mis = obs_mi.compute_target_mis(obs_mis, circuit, d)
    plt.loglog(obs_mis, target_mis, color + kind, label=label, **kwargs)
    n_plots += 1


def to_tikz(name_pattern='../SNI_opt_2/figs/{}.tex'):
    try:
        fname = sys.argv[0].split('.')[0]
        matplotlib2tikz.save(name_pattern.format(fname),
                figureheight='\\figureheight', figurewidth='\\figurewidth',
                externalize_tables=True, override_externals=True,
                tex_relative_path_to_data='figs')
    except Exception as e:
        print('Could not export plot into tikz format', e)

def display(name_pattern='../SNI_opt_2/figs/{}.tex'):
    to_tikz(name_pattern)
    plt.show()

