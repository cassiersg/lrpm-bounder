
import itertools as it

def isw(d):
    res = ''

    res += 'C x\n'
    res += 'B x y\n'
    res += 'B x z\n'

    res += 'P x = ' + ' + '.join(f'x_{i}' for i in range(d)) + '\n'
    res += 'P y = ' + ' + '.join(f'y_{i}' for i in range(d)) + '\n'
    res += 'P z = ' + ' + '.join(f'z_{i}' for i in range(d)) + '\n'

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

if __name__ == '__main__':
    d = 3
    print(f'---- ISW, d={d} ----')
    print(isw(d))

