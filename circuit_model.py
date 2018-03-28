
import math
import itertools as it
import random

import networkx as nx

import utils

class Circuit:
    def __init__(self):
        self.vars = []
        self.bijs = []
        self.l_sums = []
        self.p_sums = []
        self.l_prods = []
        self.p_prods = []

    def var(self, name, continuous=False, kind='intermediate'):
        v = Variable(name, len(self.vars), continuous, kind)
        self.vars.append(v)
        return v

    def bij(self, ops):
        self.bijs.append(ops)

    def l_sum(self, dest, ops):
        self.l_sums.append((dest, ops))

    def p_sum(self, dest, ops):
        self.p_sums.append((dest, ops))

    def l_prod(self, dest, ops):
        self.l_prods.append((dest, ops))

    def p_prod(self, dest, ops):
        self.p_prods.append((dest, ops))

    def fmt_var(self, var):
        fmt_specifier = '{{:0{}}}_{{}}'.format(math.ceil(math.log10(len(self.vars))))
        return fmt_specifier.format(var.idx, var.name)

    def fmt_op(self, dest, ops, op, qual):
        return f'{qual} {self.fmt_var(dest)} = ' + f' {op} '.join(
                map(self.fmt_var, ops))

    def fmt_bij(self, ops):
        return 'B ' + ' '.join(map(self.fmt_var, ops))

    def fmt_cont(self, var):
        return 'C ' + self.fmt_var(var)

    def __str__(self):
        return '\n'.join(it.chain(
                (self.fmt_op(dest, ops, '+', 'L') for dest, ops, in self.l_sums),
                (self.fmt_op(dest, ops, '+', 'P') for dest, ops, in self.p_sums),
                (self.fmt_op(dest, ops, '*', 'L') for dest, ops, in self.l_prods),
                (self.fmt_op(dest, ops, '*', 'P') for dest, ops, in self.p_prods),
                map(self.fmt_bij, self.bijs),
                (self.fmt_cont(var) for var in self.vars if var.continuous),
                ))


class Variable:
    def __init__(self, name, idx, continuous, kind):
        self.name = name
        self.idx = idx
        self.continuous = continuous
        self.kind = kind

class CompGraph:
    def __init__(self, circuit, domain=(0, 1)):
        self.g = nx.DiGraph()
        self.circuit = circuit
        self.domain = domain
        self.build_graph()

    def build_graph(self):
        for var in self.circuit.vars:
            self.g.add_node(var.idx)
            if var.kind == 'input':
                self.g.nodes[var.idx]['input'] = True
            elif var.kind == 'random':
                self.g.nodes[var.idx]['random'] = True
        for (dest, ops) in self.circuit.p_sums + self.circuit.l_sums:
            self.g.nodes[dest.idx]['op'] = '+'
            for op in ops:
                self.g.add_edge(op.idx, dest.idx)
        for (dest, ops) in self.circuit.p_prods + self.circuit.l_prods:
            self.g.nodes[dest.idx]['op'] = '*'
            for op in ops:
                self.g.add_edge(op.idx, dest.idx)
        for node, attrs in self.g.nodes.items():
            assert 'input' in attrs or 'random' in attrs or 'op' in attrs, f'noinput node {self.circuit.fmt_var(self.circuit.vars[node])}'

    def map_inputs(self, inputs):
        return {next(var.idx for var in self.circuit.vars if var.name == name): v
                for name, v in inputs.items()}

    def compute(self, inputs):
        inputs = self.map_inputs(inputs)
        values = [None for _ in self.circuit.vars]
        for idx, v in inputs.items():
            values[idx] = v
        for var in self.circuit.vars:
            if var.kind == 'random':
                values[var.idx] = random.choice(self.domain)
        for idx in nx.topological_sort(self.g):
            if values[idx] is None:
                op = {'+': sum, '*': utils.product}[self.g.nodes[idx]['op']]
                values[idx] = op(values[pred] for pred in self.g.predecessors(idx))
        output_res = {
            var.idx: values[var.idx] for var in self.circuit.vars
            if var.kind == 'output'
            }
        return output_res, values
            

