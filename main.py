from scipy.optimize import minimize
from tabulate import tabulate
from math import exp

def sciM():
    g = [lambda x: -(-x[0] - x[1] + 2), lambda x: -(x[0] - 2 * x[1] + 1), lambda x: -(-2 * x[0] + x[1])]
    x0 = [0.8, 1.3]
    cons = ({'type': 'ineq', 'fun': g[0]},
            {'type': 'ineq', 'fun': g[1]},
            {'type': 'ineq', 'fun': g[2]})
    answer = minimize(fx, x0, constraints=cons)
    print('scipy:', answer.x)

def getPen1(x, C):
    q = 2
    return C * sum([pow(max(0, i(x)), q) for i in g])

def getPen2(x, C):
    negorzr = True
    for i in g:
        negorzr = negorzr and i(x) <= 0
    if negorzr:
        return 0
    else:
        return C * exp((-1) / max([i(x) for i in g]))

def getPen4(x, C):
    neg = True
    for i in g:
        neg = neg and i(x) < 0
    if neg:
        return (-1) * C * sum([1 / i(x) for i in g])
    else:
        return pow(10, 10)

fx = lambda x: 2 * pow(x[0], 2) + pow(x[1], 2)

g = [lambda x: (-x[0] - x[1] + 2), lambda x: (x[0] - 2 * x[1] + 1), lambda x: (-2 * x[0] + x[1])]

def MPF(penalty, eps, x0, C, b, pv):
    k = 1
    table = [['k', 'x', 'penalty', 'C'], [0, x0, penalty, C]]
    while penalty > eps:
        Fx = {
            1: lambda x: fx(x) + getPen1(x, C),
            2: lambda x: fx(x) + getPen2(x, C),
            4: lambda x: fx(x) + getPen4(x, C)
        }.get(pv)
        x0 = minimize(Fx, x0).x
        penalty = {
            1: getPen1(x0, C),
            2: getPen2(x0, C),
            4: getPen4(x0, C)
        }.get(pv)
        table.append([k, x0, penalty, C])
        C *= b
        k += 1
        if (k >= 1000):
            break
    print(tabulate(table, tablefmt="fancy_grid") + '\n')

#sciM()
MPF(10, 0.0001, [0.8, 1.3], 1, 2, 1)
MPF(10, 0.0001, [0.8, 1.3], 1, 2, 2)
MPF(10, 0.0001, [0.8, 1.3], 1, 0.5, 4)