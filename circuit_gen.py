
import itertools as it

d = 3

print("C x")
print("B x y")
print("B x z")

print("P x = " + " + ".join(f'x_{i}' for i in range(d)))
print("P y = " + " + ".join(f'y_{i}' for i in range(d)))
print("P z = " + " + ".join(f'z_{i}' for i in range(d)))

for i, j in it.product(range(d), range(d)):
    print(f'L p_{i}_{j} = x_{i} * y_{j}')

for i in range(d):
    for j in range(i):
        print(f'B m_{i}_{j} r_{j}_{i}')
    for j in range(i+1, d):
        print(f'L t_{i}_{j} = r_{i}_{j} + p_{i}_{j}')
        print(f'L m_{i}_{j} = t_{i}_{j} + p_{j}_{i}')

for i in range(d):
    print(f'B c_{i}_{i} p_{i}_{i}')
    for j in range(i+1, d):
        print(f'L c_{i}_{j} = c_{i}_{j-1} + m_{i}_{j}')

for i in range(d):
    print(f'B z_{i} c_{i}_{d-1}')

