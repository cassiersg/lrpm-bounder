# Copyright 2018 FirstName LastName
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
Conversion from abstract circuit model to circuit leakage model.
"""

import itertools as it
import sys

import abs_circuit
import muls_gen

def abs_str2idx(cont_vars, bijections, leaking_ops, properties):
    var_map, cont_vars, leaking_ops, properties = abs_circuit.canonicalize_vars(
            bijections, cont_vars, leaking_ops, properties)
    equalities, var_leakage = abs_circuit.var_leakage_and_eq(leaking_ops, properties)
    #equalities, var_leakage, cont_vars, var_map = abs_circuit.simplify_circuit_model(
    #        cont_vars, bijections, leaking_ops, properties)
    all_vars = list(set(it.chain(*((dest, *ops) for _, dest, ops in equalities))))
    var_idx_map = {var: i for i, var in enumerate(all_vars)}
    is_cont = [var in cont_vars for var in all_vars]
    leakage = [var_leakage[var] for var in all_vars]
    ops = [(0 if op_kind == '+' else 1, list(map(var_idx_map.__getitem__, (dest, *ops)))) for
            op_kind, dest, ops in equalities]
    final_var_map = {orig_name: var_idx_map[new_name] for orig_name, new_name in var_map.items()}
    return ((is_cont, leakage, ops), final_var_map)


def export_circuit_model(cont_vars, bijections, leaking_ops, properties):
    var_map, cont_vars, leaking_ops, properties = abs_circuit.canonicalize_vars(
            bijections, cont_vars, leaking_ops, properties)
    equalities, var_leakage = abs_circuit.var_leakage_and_eq(leaking_ops, properties)
    #equalities, var_leakage, cont_vars, var_map = abs_circuit.simplify_circuit_model(
    #        cont_vars, bijections, leaking_ops, properties)
    res = ''
    for op_kind, dest, ops in equalities:
        res += f'E {op_kind} {dest} {" ".join(ops)}\n'
    for var, leakage in var_leakage.items():
        res += f'L {var} {leakage}\n'
    for var in cont_vars:
        res += f'C {var}\n'
    return res, var_map

def export_circuit_model2(cont_vars, bijections, leaking_ops, properties):
    #var_map, cont_vars, leaking_ops, properties = abs_circuit.canonicalize_vars(
    #        bijections, cont_vars, leaking_ops, properties)
    equalities, var_leakage = abs_circuit.var_leakage_and_eq(leaking_ops, properties)
    #equalities, var_leakage, cont_vars, var_map = abs_circuit.simplify_circuit_model(
    #        cont_vars, bijections, leaking_ops, properties)
    res = ''
    for op_kind, dest, ops in equalities:
        res += f'E {op_kind} {dest} {" ".join(ops)}\n'
    for var, leakage in var_leakage.items():
        res += f'L {var} {leakage}\n'
    for var in cont_vars:
        res += f'C {var}\n'
    return res

def circuit2abs_idx(c):
    return abs_str2idx(*abs_circuit.circuit2abstract(c))

def convert(c):
    return export_circuit_model(*abs_circuit.circuit2abstract(c))

def circuit2abs_idx2(c):
    sc, var_map = c.simplified()
    is_cont = [v.continuous for v in sc.vars]
    leakage = sc.leakage()
    ops = ([(0, [v.idx for v in (dest, *ops)]) for dest, ops in sc.l_sums + sc.p_sums] +
           [(1, [v.idx for v in (dest, *ops)]) for dest, ops in sc.l_prods + sc.p_prods])
    final_var_map = {c.fmt_var(v): var_map[v.idx] for v in c.vars}
    return (is_cont, leakage, ops), final_var_map

if __name__ == '__main__':
    mul_kind = sys.argv[1]
    d = sys.argv[2]
    c = muls_gen.muls[mul_kind](int(d))
    res, _ = convert(c)
    if len(sys.argv) < 4:
        print(res)
    else:
        with open(sys.argv[3], 'w') as f:
            f.write(res)

