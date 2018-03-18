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
Parsing text representation of computation graphs.
"""

import collections

import numpy as np
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
            op_kind = ''.join(set(c for c in calc if c in ('*', '+')))
            assert op_kind in ('*', '+'), f'Invalid operation at line {i+1}: invalid opeator set: {op_kind}'
            ops = tuple(map(str.strip, calc.replace('*', '+').split('+')))
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
    return {f'v_{var}': all_ops[var] + all_dest[var] for var in variables}

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
    for bijection in bijections:
        for var in bijection:
            assert var in variables, f'Variable "{var}" in bijection "{bijection}" unused'
    for var in cont_vars:
        assert var in variables, f'Continuous leakage variable "{var}" unused'

def build_circuit_model(cont_vars, bijections, leaking_ops, properties):
    test_all_var_in_eq(cont_vars, bijections, leaking_ops | properties)
    var_map, cont_vars, leaking_ops, properties = canonicalize_vars(
            bijections, cont_vars, leaking_ops, properties)
    equalities = leaking_ops | properties
    variables = list_vars(equalities)
    var_leakage = compute_var_leakage(variables, leaking_ops)
    g = build_graph(equalities)
    cont_vars = {f'v_{var}' for var in cont_vars}
    return g, var_leakage, cont_vars, var_map

def init_belief_propagation(g, var_leakage):
    return {src: {dest: 0 for dest in g.nodes} for src in g.nodes}

def prod(seq, start=1):
    res = start
    for x in seq:
        res *= x
    return res

def belief_propagation_edge(g,
        var_leakage,
        cont_vars,
        messages,
        src,
        dest,
        N,
        alpha,
        beta
        ):
    if 'var' in g.nodes[src]:
        intrinsic_leakage = var_leakage[src] * (N if src in cont_vars else 1)
        default_coef = N if src in cont_vars else 1
        own_coef = default_coef - 1
        extrinsic_leakage = sum(
                messages[src2][src] * (own_coef if src2 == dest else default_coef)
                for src2 in g.neighbors(src)
                )
        return intrinsic_leakage + extrinsic_leakage
    else:
        loss = (alpha if g.nodes[src]['kind'] == '+' else beta)
        loss = loss**(g.degree(src) - 2)
        return loss * prod(
            messages[src2][src] for src2 in g.neighbors(src)
            if src2 != dest
            )

def belief_propagation_iter(g, var_leakage, cont_vars, messages, N, alpha, beta):
    return {src:
            {dest:
                belief_propagation_edge(
                    g, var_leakage, cont_vars, messages, src, dest, N, alpha, beta
                    )
                for dest in g.nodes}
            for src in g.nodes}

def belief_propatation_final(g, var_leakage, cont_vars, messages, N):
    def tot_info_var(src):
        intrinsic_leakage = var_leakage[src] * (N if src in cont_vars else 1)
        default_coef = N if src in cont_vars else 1
        extrinsic_leakage = sum(
                messages[src2][src] * default_coef
                for src2 in g.neighbors(src)
                )
        return intrinsic_leakage + extrinsic_leakage
    return {src: tot_info_var(src)
            for src in g.nodes if 'var' in g.nodes[src]}

def are_messages_close(msg_old, msg_new, rtol):
    return all(np.isclose(msg_old[src][dest], msg_new[src][dest], rtol=rtol)
            for src in msg_old for dest in msg_old[src])

def belief_propagation(
        g,
        var_leakage,
        cont_vars,
        leakage_mi,
        N=1,
        alpha=1,
        beta=1,
        rtol=0.001,
        max_iter=1000,
        ):
    var_leakage = {n: l*leakage_mi for n, l in var_leakage.items()}
    messages_old = init_belief_propagation(g, var_leakage)
    n=2
    messages = belief_propagation_iter(
            g, var_leakage, cont_vars, messages_old, N, alpha, beta)
    while not are_messages_close(messages_old, messages, rtol):
        if n >= max_iter:
            raise ValueError('Max number of iterations exceeded')
        messages_old = messages
        n *= 2
        for _ in range(n):
            messages = belief_propagation_iter(
                    g, var_leakage, cont_vars, messages, N, alpha, beta)
    info = belief_propatation_final(g, var_leakage, cont_vars, messages, N)
    return info

if __name__ == '__main__':
    with open('circuit.txt') as f:
        s = f.read()
    g, var_leakage, cont_vars, var_map = build_circuit_model(*parse_circuit_raw(s))
    from pprint import pprint
    b = belief_propagation(
            g, var_leakage,
            cont_vars,
            leakage_mi=0.05,
            N=10,
            alpha=1,
            beta=1,
            )
    pprint(b)

