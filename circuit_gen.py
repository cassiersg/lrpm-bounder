
import itertools as it

def mul_preamble(d):
    res = ''
    res += 'C x\n'
    res += 'B x y\n'
    res += 'B x z\n'
    res += 'P x = ' + ' + '.join(f'x_{i}' for i in range(d)) + '\n'
    res += 'P y = ' + ' + '.join(f'y_{i}' for i in range(d)) + '\n'
    res += 'P z = ' + ' + '.join(f'z_{i}' for i in range(d)) + '\n'
    return res

def isw(d):
    res = mul_preamble(d)

    for i, j in it.product(range(d), range(d)):
        res += f'L p_{i}_{j} = x_{i} * y_{j}\n'

    for i in range(d):
        for j in range(i):
            res += f'B m_{i}_{j} r_{j}_{i}\n'
        for j in range(i+1, d):
            res += f'L t_{i}_{j} = r_{i}_{j} + p_{i}_{j}\n'
            res += f'L m_{i}_{j} = t_{i}_{j} + p_{j}_{i}\n'

    for i in range(d):
        res += f'B c_{i}_{i} p_{i}_{i}\n'
        for j in range(i+1, d):
            res += f'L c_{i}_{j} = c_{i}_{j-1} + m_{i}_{j}\n'

    for i in range(d):
        res += f'B z_{i} c_{i}_{d-1}\n'

    return res


def BBP15(d):
    res = mul_preamble(d)

    for i, j in it.product(range(d), range(d)):
        res += f'L p_{i}_{j} = x_{i} * y_{j}\n'

    d2 = d-1
    for i in range(d):
        res += f'B c_{i}_{d+1} p_{i}_{i}\n'
        for j in range(d2, i+1, -2):
            res += f'L t_{i}_{j}_0 = r_{i}_{j} + p_{i}_{j}\n'
            res += f'L t_{i}_{j}_1 = t_{i}_{j}_0 + p_{j}_{i}\n'
            res += f'L t_{i}_{j}_2 = t_{i}_{j}_1 + r_{j-1}\n'
            res += f'L t_{i}_{j}_3 = t_{i}_{j}_2 + p_{i}_{j-1}\n'
            res += f'L t_{i}_{j}_4 = t_{i}_{j}_3 + p_{j-1}_{i}\n'
            res += f'L c_{i}_{j} = c_{i}_{j+2} + t_{i}_{j}_4\n'
        if (i-d2) % 2 != 0:
            res += f'L t_{i}_{i+1}_0 = r_{i}_{i+1} + p_{i}_{i+1}\n'
            res += f'L t_{i}_{i+1}_1 = t_{i}_{i+1}_0 + p_{i+1}_{i}\n'
            res += f'L c_{i}_{i+1} = c_{i}_{i+3} + t_{i}_{i+1}_1\n'
            if i % 2 == 1:
                res += f'L z_{i} = c_{i}_{i+1} + r_{i}\n'
            else:
                res += f'B z_{i} c_{i}_{i+1}\n'
        else:
            for j in range(i-1, -1, -1):
                res += f'L c_{i}_{j+2} = c_{i}_{j+3} + r_{j}_{i}\n'
            res += f'B z_{i} c_{i}_{2}\n'

    return res

def pini1(d):
    res = mul_preamble(d)

    for i in range(d):
        res += f'B nx_{i} x_{i}\n'

    for i in range(d):
        for j in range(i):
            res += f'B r_{i}_{j} r_{j}_{i}\n'

    for i, j in it.product(range(d), range(d)):
        res += f'L s_{i}_{j} = y_{j} + r_{i}_{j}\n'
        res += f'L p_{i}_{j}_0 = nx_{i} * r_{i}_{j}\n'
        res += f'L p_{i}_{j}_1 = x_{i} * s_{i}_{j}\n'
        res += f'L p_{i}_{j} = p_{i}_{j}_0 + p_{i}_{j}_1\n'

    for i in range(d):
        res += f'B c_{i}_{i} p_{i}_{i}\n'

    for i in range(d):
        for j in range(i+1, d):
            res += f'L c_{i}_{j} = c_{i}_{j-1} + p_{i}_{j}\n'

    for i in range(d):
        res += f'B z_{i} c_{i}_{d-1}\n'

    return res

def pini2(d):
    d2 = d-1
    res = mul_preamble(d)

    for i in range(d):
        for j in range(i+1, d):
            res += f'L s_{i}_{j} = s_{i} + s_{j}\n'
            res += f'L u_{i}_{j}_0 = y_{j} + s_{i}_{j}\n'
            res += f'L u_{i}_{j}_1 = x_{j} + s_{i}_{j}\n'
            res += f'L p_{i}_{j}_0 = x_{i} * s_{i}_{j}\n'
            res += f'L p_{i}_{j}_1 = x_{i} * u_{i}_{j}_0\n'
            res += f'L p_{i}_{j}_2 = y_{i} * s_{i}_{j}\n'
            res += f'L p_{i}_{j}_3 = y_{i} * u_{i}_{j}_1\n'
    for i in range(d):
        res += f'L c_{i}_{d2} = x_{i} * y_{i}\n'
        for j in range(d2, i+1, -2):
            res += f'L t_{i}_{j}_0 = r_{i}_{j} + p_{i}_{j}_0\n'
            res += f'L t_{i}_{j}_1 = t_{i}_{j}_0 + p_{i}_{j}_1\n'
            res += f'L t_{i}_{j}_2 = t_{i}_{j}_1 + p_{i}_{j}_2\n'
            res += f'L t_{i}_{j}_3 = t_{i}_{j}_2 + p_{i}_{j}_3\n'
            res += f'L t_{i}_{j}_4 = t_{i}_{j}_3 + r_{j-1}\n'
            res += f'L t_{i}_{j}_5 = t_{i}_{j}_4 + p_{i}_{j-1}_0\n'
            res += f'L t_{i}_{j}_6 = t_{i}_{j}_5 + p_{i}_{j-1}_1\n'
            res += f'L t_{i}_{j}_7 = t_{i}_{j}_6 + p_{i}_{j-1}_2\n'
            res += f'L t_{i}_{j} = t_{i}_{j}_7 + p_{i}_{j-1}_3\n'
            res += f'L t_{i}_{j-2} = c_{i}_{j} + t_{i}_{j}\n'
        if (i-d2) % 2 != 0:
            res += f'L t_{i}_{i+1}_0 = r_{i}_{i+1} + p_{i}_{i+1}_0\n'
            res += f'L t_{i}_{i+1}_1 = t_{i}_{i+1}_0 + p_{i}_{i+1}_1\n'
            res += f'L t_{i}_{i+1}_2 = t_{i}_{i+1}_1 + p_{i}_{i+1}_2\n'
            res += f'L t_{i}_{i+1} = t_{i}_{i+1}_2 + p_{i}_{i+1}_3\n'
            res += f'L c_{i}_{i} = c_{i}_{i+1} + t_{i}_{i+1}\n'
            if i % 2 == 1:
                res += f'L z_{i} = c_{i}_{i} + r_{i}\n'
            else:
                res += f'B z_{i} c_{i}_{i}\n'
        else:
            for j in range(i-1, -1, -1):
                res += f'L c_{i}_{j} = c_{i}_{j+1} + r_{j}_{i}\n'
            res += f'B z_{i} = c_{i}_0\n'
    return res

import os

def gen_all(d):
    os.makedirs(f'circuits-{d}', exist_ok=True)
    with open(f'circuits-{d}/isw.txt', 'w') as f:
        f.write(isw(d))
    with open(f'circuits-{d}/BBP15.txt', 'w') as f:
        f.write(BBP15(d))
    with open(f'circuits-{d}/pini1.txt', 'w') as f:
        f.write(pini1(d))
    with open(f'circuits-{d}/pini2.txt', 'w') as f:
        f.write(pini2(d))


if __name__ == '__main__':
    d = 3
    gen_all(d)
    print(f'---- ISW, d={d} ----')
    print(isw(d))
    print(f'---- BBP15, d={d} ----')
    print(BBP15(d))
    print(f'---- pini1, d={d} ----')
    print(pini1(d))
    print(f'---- pini2, d={d} ----')
    print(pini2(d))

