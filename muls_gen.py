
import itertools as it
import random

import circuit_model

def mul_preamble(d, c, x_name='x', y_name='y', z_name='z'):
    x = c.var(x_name, continuous=True, kind='output')
    y = c.var(y_name, kind='output')
    z = c.var(z_name, kind='output')
    c.bij((x, y))
    c.bij((x, z))
    sh_x = []
    sh_y = []
    sh_z = []
    for i in range(d):
        sh_x.append(c.var(f'{x_name}_{i}', kind='input'))
        sh_y.append(c.var(f'{y_name}_{i}', kind='input'))
        sh_z.append(c.var(f'{z_name}_{i}', kind='output'))
    c.p_sum(x, sh_x)
    c.p_sum(y, sh_y)
    c.p_sum(z, sh_z)
    return x, y, z, sh_x, sh_y, sh_z

def isw(d):
    c = circuit_model.Circuit()
    _, _, _, x, y, z = mul_preamble(d, c)

    # product matrix
    p = [[c.var(f'p_{i}_{j}') for j in range(d)] for i in range(d)]
    for i, j in it.product(range(d), range(d)):
        c.l_prod(p[i][j], (x[i], y[j]))

    # randoms & temps in matrix
    r = [[0 if j <= i else c.var(f'r_{i}_{j}', kind='random') for j in
        range(d)] for i in range(d)]
    t = [[0 if j <= i else c.var(f't_{i}_{j}') for j in range(d)] for i in
            range(d)]
    m = [[c.var(f'm_{i}_{j}') for j in range(d)] for i in range(d)]
    for i in range(d):
        for j in range(i):
            c.p_sum(m[i][j], (r[j][i],))
        for j in range(i+1, d):
            c.l_sum(t[i][j], (r[i][j], p[i][j]))
            c.l_sum(m[i][j], (t[i][j], p[j][i]))

    # compression
    c_var = [[c.var(f'c_{i}_{j}') for j in range(d)] for i in range(d)]
    for i in range(d):
        c.p_sum(m[i][i], (p[i][i],))
        c.p_sum(c_var[i][0], (m[i][0],))
        for j in range(1, d):
            c.l_sum(c_var[i][j], (c_var[i][j-1], m[i][j]))
        c.p_sum(z[i], (c_var[i][d-1],))

    return c

def BBP15(d):
    d2 = d-1
    c = circuit_model.Circuit()
    _, _, _, x, y, z = mul_preamble(d, c)

    # product matrix
    p = [[c.var(f'p_{i}_{j}') for j in range(d)] for i in range(d)]
    for i, j in it.product(range(d), range(d)):
        c.l_prod(p[i][j], (x[i], y[j]))

    # randoms & temps in matrix & compression
    r = [
            {d2-j: c.var(f'r_{i}_{j}', kind='random') for j in range(d2-i)}
            for i in range(d)
            ]
    r2 = {j: c.var(f'r2_{j}', kind='random') for j in range(d2-1, 0, -2)}
    t = [
            {j: [c.var(f't_{i}_{j}_{k}') for k in range(5)]
                    for j in range(d2, i+1, -2)}
            for i in range(d)
            ]
    c_var = [{j: c.var(f'c_{i}_{j}') for j in range(d2+2, i+1, -2)}
            for i in range(d)
            ]
    for i in range(d):
        c.p_sum(c_var[i][d2+2], (p[i][i],))
        for j in range(d2, i+1, -2):
            c.l_sum(t[i][j][0], (r[i][j], p[i][j]))
            c.l_sum(t[i][j][1], (t[i][j][0], p[j][i]))
            c.l_sum(t[i][j][2], (t[i][j][1], r2[j-1]))
            c.l_sum(t[i][j][3], (t[i][j][2], p[i][j-1]))
            c.l_sum(t[i][j][4], (t[i][j][3], p[j-1][i]))
            c.l_sum(c_var[i][j], (c_var[i][j+2], t[i][j][4]))
        if (i-d2) % 2 != 0:
            t[i][i+1] = [c.var(f't_{i}_{i+1}_0'), c.var(f't_{i}_{i+1}_1')]
            c_var[i][i+1] = c.var(f'c_{i}_{i+1}')
            c.l_sum(t[i][i+1][0], (r[i][i+1], p[i][i+1]))
            c.l_sum(t[i][i+1][1], (t[i][i+1][0], p[i+1][i]))
            c.l_sum(c_var[i][i+1], (c_var[i][i+3], t[i][i+1][1]))
            if i % 2 == 1:
                c.l_sum(z[i], (c_var[i][i+1], r2[i]))
            else:
                c.p_sum(z[i], (c_var[i][i+1],))
        else:
            for j in range(i-1, -1, -1):
                c_var[i][j+2] = c.var(f'c_{i}_{j+2}')
                c.l_sum(c_var[i][j+2], (c_var[i][j+3], r[j][i]))
            c.p_sum(z[i], (c_var[i][2],))

    return c

muls = {'isw': isw, 'BBP15': BBP15}

import sys

def gen_random_input(d, domain=(0,1)):
    return [random.choice(domain) for i in range(d)]

def gen_random_inputs(d, domain=(0,1)):
    x = gen_random_input(d)
    y = gen_random_input(d)
    res = {f'x_{i}': v for i, v in enumerate(x)}
    res.update({f'y_{i}': v for i, v in enumerate(y)})
    return res, x, y

def assert_sh_prod(x, y, z):
    assert (sum(x) % 2) * (sum(y) % 2) == (sum(z) % 2)

def test_mul(d, mul=isw):
    c = mul(d)
    g = circuit_model.CompGraph(c)
    inputs, x, y  = gen_random_inputs(d)
    res, _ = g.compute(inputs)
    z = [v for var, v in res.items() if c.vars[var].name.startswith('z_')]
    assert_sh_prod(x, y, z)

if __name__ == '__main__':
    try:
        d = int(sys.argv[1])
    except IndexError:
        d = 3
    #gen_all(d)
    #for mul_name, mul_f in muls.items():
    for mul_name, mul_f in [('BBP15', BBP15)]:
        print(f'---- {mul_name}, d={d} ----')
        print(mul_f(d))
        for _ in range(100):
            test_mul(d, mul_f)

    #print(f'---- BBP15, d={d} ----')
    #print(BBP15(d))
    #print(f'---- pini1, d={d} ----')
    #print(pini1(d))
    #print(f'---- pini2, d={d} ----')
    #print(pini2(d))
    #print(f'---- isw_ref, d={d} ----')
    #print(isw_ref(d, 'ref', 'a', 'b', range(5, 5+d), range(10, 10+d)))

