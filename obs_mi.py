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

import joblib

import librfactor_python
import muls_gen


mem = joblib.Memory(cachedir='cache',
       # verbose=0
        )

@mem.cache
def gen_lkm(c_name, d, var_name):
    c = muls_gen.muls[c_name](d)
    abs_c_idx, var_map = c.to_lkm(rand_var_leak=1, only_inputs_leak=False)
    v = c.fmt_var([var for var in c.vars if var.name == var_name][0])
    x_idx = var_map[v]
    return abs_c_idx, x_idx

@mem.cache
def compute_target_mis(obs_mis, c_name,  d, tol=1e-5, var_name='x'):
    abs_c_idx, x_idx = gen_lkm(c_name, d, var_name)
    pfg = librfactor_python.PyFactorGraph(*abs_c_idx)
    return [pfg.bp_mi(obs_mi, 1, tol, 1.0, 1.0, 10000, False)[0][x_idx]
            for obs_mi in obs_mis]

@mem.cache
def compute_target_mis_orders(obs_mi, c_name,  ds, tol=1e-5, var_name='x'):
    res = []
    for d in ds:
        abs_c_idx, x_idx = gen_lkm(c_name, d, var_name)
        pfg = librfactor_python.PyFactorGraph(*abs_c_idx)
        res.append(
                pfg.bp_mi(obs_mi, 1, tol, 1.0, 1.0, 10000, False)[0][x_idx]
                )
    return res

@mem.cache
def ub_mi(obs_mis, c_name,  d, tol=1e-3, var_name='x'):
    c = muls_gen.muls[c_name](d)
    abs_c_idx, var_map = c.to_lkm(rand_var_leak=1, only_inputs_leak=False)
    v = c.fmt_var([var for var in c.vars if var.name == var_name][0])
    x_idx = var_map[v]
    is_cont, leakage, ops = abs_c_idx
    tot_leak = sum(leakage)
    return [(obs_mi*tot_leak/d)**d for obs_mi in obs_mis]

@mem.cache
def lb_mi(obs_mis, c_name,  d, tol=1e-3, var_name='x'):
    c = muls_gen.muls[c_name](d)
    abs_c_idx, var_map = c.to_lkm(rand_var_leak=1, only_inputs_leak=True)
    v = c.fmt_var([var for var in c.vars if var.name == var_name][0])
    x_idx = var_map[v]
    is_cont, leakage, ops = abs_c_idx
    tot_leak = sum(leakage)
    return [2*(obs_mi*tot_leak/2/d)**d for obs_mi in obs_mis]

@mem.cache
def lb2_mi(obs_mis, c_name,  d, tol=1e-5, var_name='x'):
    c = muls_gen.muls[c_name](d)
    abs_c_idx, var_map = c.to_lkm(rand_var_leak=1, only_inputs_leak=True)
    v = c.fmt_var([var for var in c.vars if var.name == var_name][0])
    x_idx = var_map[v]
    pfg = librfactor_python.PyFactorGraph(*abs_c_idx)
    return [pfg.bp_mi(obs_mi, 1, tol, 1.0, 1.0, 10000, True)[0][x_idx]
            for obs_mi in obs_mis]
