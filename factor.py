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
Belief propagation for MI
"""

import numpy as np
import networkx as nx

import abs_circuit

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
        return min(1, intrinsic_leakage + extrinsic_leakage)
    else:
        loss = (alpha if g.nodes[src]['kind'] == '+' else beta)
        loss = loss**(g.degree(src) - 2)
        return min(1, loss * prod(
            messages[src2][src] for src2 in g.neighbors(src)
            if src2 != dest
            ))

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
        max_iter=256,
        ):
    var_leakage = {n: l*leakage_mi for n, l in var_leakage.items()}
    messages_old = init_belief_propagation(g, var_leakage)
    n=2
    messages = belief_propagation_iter(
            g, var_leakage, cont_vars, messages_old, N, alpha, beta)
    while not are_messages_close(messages_old, messages, rtol):
        if n >= max_iter:
            print("Max number of iterations exceeded")
            break
            #raise ValueError('Max number of iterations exceeded')
        messages_old = messages
        n *= 2
        for _ in range(n):
            messages = belief_propagation_iter(
                    g, var_leakage, cont_vars, messages, N, alpha, beta)
    print(f'Number of iterations: {2*n}')
    info = belief_propatation_final(g, var_leakage, cont_vars, messages, N)
    return info

import sys
if __name__ == '__main__':
    in_fname = sys.argv[1]
    with open(in_fname) as f:
        s = f.read()
    g, var_leakage, cont_vars, var_map = abs_circuit.build_circuit_model(*abs_circuit.parse_circuit_raw(s))
    from pprint import pprint
    b = belief_propagation(
            g, var_leakage,
            cont_vars,
            leakage_mi=0.01,
            N=10,
            alpha=1,
            beta=1,
            rtol=0.1,
            max_iter=100,
            )
    pprint(b)

