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
Abstract circuit models
"""

import collections

import networkx as nx

def parse_circuit_raw(circuit):
    statements = (st.strip() for st in circuit.splitlines())
    cont_vars = set()
    bijections = set()
    leaking_ops = set()
    properties = set()
    for i, st in enumerate(statements):
        assert len(st) > 2 and st[1] == ' ', f'Invalid statement "{st}" at line {i+1}'
        kind = st[0]
        if kind == 'C':
            var = st[2:].strip()
            cont_vars.add(var)
        elif kind == 'B':
            bij_vars = filter(bool, map(str.strip, st[2:].strip().split(' ')))
            bijections.add(tuple(bij_vars))
        elif kind in ('P', 'L'):
            assign = st[2:].strip()
            dest, calc = map(str.strip, assign.split('='))
            op_kind = ''.join(set(c for c in calc if not (c.isalnum() or c.isspace() or c == '_')))
            ops = tuple(map(str.strip, calc.replace('*', '+').split('+')))
            if op_kind == '':
                # kind '[PL] X = Y' -> 'L' is meaningless -> always P -> equivalent to B
                bijections.add((dest, ops[0]))
            else:
                assert op_kind in ('', '*', '+'), f'Invalid operation at line {i+1}: invalid opeator set: {op_kind}'
                {'L': leaking_ops, 'P': properties}[kind].add((op_kind, dest, ops))
        else:
            assert False, f'Invalid statement kind "{kind}" for statement ar line {i+1}'
    return cont_vars, bijections, leaking_ops, properties


def build_var_map(bijections, variables):
    g = nx.Graph()
    g.add_nodes_from(variables)
    for bijection in bijections:
        g.add_edges_from(zip(bijection[:-1], bijection[1:]))
    components = [list(sorted(x)) for x in nx.connected_components(g)]
    #var_map = {c[0]: set(c) for c in components}
    var_map = {n: c[0] for c in components for n in c}
    return var_map

def map_ops_vars(equalities, var_map):
    return {(kind, var_map[dest], tuple(var_map[op] for op in ops))
            for kind, dest, ops in equalities}

def list_ops(equalities):
    for (kind, dest, ops) in equalities:
        yield from ops

def list_dest(equalities):
    for (kind, dest, ops) in equalities:
        yield dest

def list_vars(equalities):
    return set(list_ops(equalities)) | set(list_dest(equalities))

def canonicalize_vars(bijections, cont_vars, leaking_ops, properties):
    variables = list_vars(leaking_ops | properties)
    var_map = build_var_map(bijections, variables)
    cont_vars = {var_map[var] for var in cont_vars}
    leaking_ops = map_ops_vars(leaking_ops, var_map)
    properties = map_ops_vars(properties, var_map)
    return var_map, cont_vars, leaking_ops, properties

def compute_var_leakage(variables, leaking_ops):
    all_ops = collections.Counter(list_ops(leaking_ops))
    all_dest = collections.Counter(list_dest(leaking_ops))
    return {var: all_ops[var] + all_dest[var] for var in variables}

def build_graph(equalities):
    variables = list_vars(equalities)
    g = nx.Graph()
    g.add_nodes_from((f'v_{var}' for var in variables), var=True)
    for i, (kind, dest, ops) in enumerate(equalities):
        name = f'e_{i}'
        g.add_node(name, eq=True, kind=kind, dest=dest)
        g.add_edge(name, f'v_{dest}')
        g.add_edges_from((name, f'v_{op}') for op in ops)
    return g

def test_all_var_in_eq(cont_vars, bijections, equalities):
    variables = list_vars(equalities)

def simplify_circuit_model(cont_vars, bijections, leaking_ops, properties):
    test_all_var_in_eq(cont_vars, bijections, leaking_ops | properties)
    var_map, cont_vars, leaking_ops, properties = canonicalize_vars(
            bijections, cont_vars, leaking_ops, properties)
    equalities = leaking_ops | properties
    variables = list_vars(equalities)
    var_leakage = compute_var_leakage(variables, leaking_ops)
    return equalities, var_leakage, cont_vars, var_map

def build_circuit_model(cont_vars, bijections, leaking_ops, properties):
    equalities, var_leakage, cont_vars, var_map = simplify_circuit_model(
            cont_vars, bijections, leaking_ops, properties)
    var_leakage = {f'v_{var}': v for var, v in var_leakage.items()}
    g = build_graph(equalities)
    cont_vars = {f'v_{var}' for var in cont_vars}
    return g, var_leakage, cont_vars, var_map


