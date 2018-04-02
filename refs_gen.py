
import random

import circuit_model

def simple_ref(circuit, inputs, outputs=None, out_name='sr'):
    d = len(inputs)
    if outputs is None:
        outputs = [circuit.var(f'{out_name}_{i}') for i in range(d)]
    c = circuit
    r = [c.var(f'r_{i}', kind='random') for i in range(d-1)]
    if d == 1:
        c.bij(outputs[0], inputs[0])
    elif d == 2:
        c.l_sum(outputs[0], (inputs[0], r[0]))
        c.l_sum(outputs[1], (inputs[1], r[0]))
    elif d >= 3:
        t = [c.var(f't_{i}') for i in range(d-2)]
        for i in range(d-1):
            c.l_sum(outputs[i], (inputs[i], r[i]))
        c.l_sum(t[0], (inputs[-1], r[0]))
        for i in range(1, d-2):
            c.l_sum(t[i], (t[i-1], r[i]))
        c.l_sum(outputs[d-1], (t[d-3], r[d-2]))
    return outputs

def isw_ref(circuit, inputs, outputs=None, out_name=''):
    d = len(inputs)
    if outputs is None:
        outputs = [circuit.var(f'{out_name}_{i}') for i in range(d)]
    c = [[circuit.var(f'c_{i}_{j}') for j in range(d)] for i in range(d)]
    r = [{j: circuit.var(f'r_{i}_{j}', kind='random') for j in range(i)} for i in range(d)]
    for i in range(d):
        circuit.bij(c[i][0], inputs[i])
        circuit.bij(outputs[i], c[i][d-1])
    for i in range(d):
        for j in range(i):
            circuit.l_sum(c[i][j+1], (c[i][j], r[i][j]))
        for j in range(i+1, d):
            circuit.l_sum(c[i][j], (c[i][j-1], r[j][i]))
    return outputs

def bat_ref_layer(circuit, inputs, outputs, d, d2):
    r = [circuit.var(f'r_{i}', kind='random') for i in range(d2)]
    for i in range(d2):
        circuit.l_sum(outputs[i], (inputs[i], r[i]))
        circuit.l_sum(outputs[d2+i], (inputs[d2+i], r[i]))
    if d % 2 == 1:
        circuit.bij(outputs[d-1], inputs[d-1])

def bat_ref(circuit, inputs, outputs=None, out_name=''):
    d = len(inputs)
    if outputs is None:
        outputs = [circuit.var(f'{out_name}_{i}') for i in range(d)]
    if d == 1:
        circuit.bij(outputs[0], inputs[0])
    elif d == 2:
        r = circuit.var('r', kind='random')
        circuit.l_sum(outputs[0], (inputs[0], r))
        circuit.l_sum(outputs[1], (inputs[1], r))
    else:
        d2 = d//2
        b = [circuit.var(f'b_{i}') for i in range(d)]
        bat_ref_layer(circuit, inputs, b, d, d2)
        c = [circuit.var(f'b_{i}') for i in range(d)]
        bat_ref(circuit, b[:d2], c[:d2])
        bat_ref(circuit, b[d2:], c[d2:])
        bat_ref_layer(circuit, c, outputs, d, d2)
    return outputs

def half_ref(circuit, inputs, outputs=None, out_name=''):
    d = len(inputs)
    if outputs is None:
        outputs = [circuit.var(f'{out_name}_{i}') for i in range(d)]
    if d == 1:
        circuit.bij(outputs[0], inputs[0])
    else:
        d2 = d//2
        bat_ref_layer(circuit, inputs, outputs, d, d2)
    return outputs

def half1_ref(circuit, inputs, outputs=None, out_name=''):
    d = len(inputs)
    if outputs is None:
        outputs = [circuit.var(f'{out_name}_{i}') for i in range(d)]
    if d == 1:
        circuit.bij(outputs[0], inputs[0])
    else:
        d2 = d//2
        if d % 2 == 1:
            r = circuit.var('r', kind='random')
            t = circuit.var('t')
            circuit.l_sum(outputs[d-1], (inputs[d-1], r))
            circuit.l_sum(t, (inputs[0], r))
            inputs = [t] + inputs[1:]
        r = [circuit.var(f'r_{i}', kind='random') for i in range(d2)]
        for i in range(d2):
            circuit.l_sum(outputs[i], (inputs[i], r[i]))
            circuit.l_sum(outputs[d2+i], (inputs[d2+i], r[i]))
    return outputs


refs = {
        'simple_ref': simple_ref,
        'isw_ref': isw_ref,
        'bat_ref': bat_ref,
        'half_ref': half_ref,
        'half1_ref': half1_ref,
        }


def gen_random_input(d, domain=(0,1)):
    return [random.choice(domain) for i in range(d)]

def test_refresh(d, ref=simple_ref):
    circuit = circuit_model.Circuit()
    var_inputs = [circuit.var(f'x_{i}', kind='input') for i in range(d)]
    var_outputs = [circuit.var(f'y_{i}', kind='output') for i in range(d)]
    ref(circuit=circuit, inputs=var_inputs, outputs=var_outputs)
    g = circuit_model.CompGraph(circuit)
    x = gen_random_input(d)
    inputs = {f'x_{i}': v for i, v in enumerate(x)}
    res, _ = g.compute(inputs)
    y = [v for var, v in res.items() if circuit.vars[var].name.startswith('y_')]
    assert (sum(x) % 2) == (sum(y) % 2)

if __name__ == '__main__':
    import sys
    try:
        d = int(sys.argv[1])
    except IndexError:
        d = 3
    for ref_name, ref_f in refs.items():
    #for ref_name, ref_f in ():
        print(f'---- {ref_name}, d={d} ----')
        circuit = circuit_model.Circuit()
        var_inputs = [circuit.var(f'x_{i}', kind='input') for i in range(d)]
        ref_f(circuit, var_inputs, out_name='y')
        print(circuit)
        for _ in range(100):
            test_refresh(d, ref_f)

