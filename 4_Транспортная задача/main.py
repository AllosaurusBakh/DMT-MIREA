import numpy as np
from scipy.optimize import linprog
import warnings


def sev_zap(a_, b_, c_):
    a = np.copy(a_)
    b = np.copy(b_)
    c = np.copy(c_)

    if a.sum() > b.sum():
        b = np.hstack((b, [a.sum() - b.sum()]))
        c = np.hstack((c, np.zeros(len(a)).reshape(-1, 1)))
    elif a.sum() < b.sum():
        a = np.hstack((a, [b.sum() - a.sum()]))
        c = np.vstack((c, np.zeros(len(b))))

    m = len(a)
    n = len(b)
    i = 0
    j = 0
    funk = 0
    x = np.zeros((m, n), dtype=int)
    counter = 0

    while (i < m) and (j < n):
        x_ij = min(a[i], b[j])
        funk += c[i, j] * min(a[i], b[j])
        a[i] -= x_ij
        b[j] -= x_ij
        x[i, j] = x_ij

        if a[i] > b[j]:
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            i += 1
            j += 1

        counter = counter + 1
        print('\nШаг', counter, ':\n', x)

    print('\nРезультат:')
    return x, funk


def find_coordinates(c_min):
    c = np.inf

    for i in range(c_min.shape[0]):
        for j in range(c_min.shape[1]):
            if (c_min[i, j] != 0) and (c_min[i, j] < c):
                c = c_min[i, j]
                i_, j_ = i, j

    return i_, j_


def min_elem(a_, b_, c_):
    a = np.copy(a_)
    b = np.copy(list(reversed(b_)))
    c = np.copy(c_)

    if a.sum() > b.sum():
        b = np.hstack((b, [a.sum() - b.sum()]))
        c = np.hstack((c, np.zeros(len(a)).reshape(-1, 1)))
    elif a.sum() < b.sum():
        a = np.hstack((a, [b.sum() - a.sum()]))
        c = np.vstack((c, np.zeros(len(b))))

    m = len(a)
    n = len(b)
    x = np.zeros((m, n), dtype=int)
    funk = 0
    counter = 0

    while 1:
        c_min = np.zeros((m, n))

        for i in range(m):
            for j in range(n):
                c_min[i, j] = (c[i, j] * min(a[i], b[j]))

        i, j = find_coordinates(c_min)
        x_ij = int(min(a[i], b[j]))
        x[i, j] = x_ij
        funk += int(c_min[i, j])
        a[i] -= x_ij
        b[j] -= x_ij

        if len(c_min[c_min > 0]) == 1:
            break

        counter = counter + 1
        print('\nШаг', counter, ':\n', x)

    print('\nРезультат:')
    return x, funk


def prepare(a, b):
    m = len(a)
    n = len(b)
    h = np.diag(np.ones(n))
    v = np.zeros((m, n))
    v[0] = 1

    for i in range(1, m):
        h = np.hstack((h, np.diag(np.ones(n))))
        k = np.zeros((m, n))
        k[i] = 1
        v = np.hstack((v, k))

    return np.vstack((h, v)).astype(int), np.hstack((b, a))


def potenz(a_, b_, c_):
    a = np.copy(a_)
    b = np.copy(b_)
    c = np.copy(c_)

    if a.sum() > b.sum():
        b = np.hstack((b, [a.sum() - b.sum()]))
        c = np.hstack((c, np.zeros(len(a)).reshape(-1, 1)))
    elif a.sum() < b.sum():
        a = np.hstack((a, [b.sum() - a.sum()]))
        c = np.vstack((c, np.zeros(len(b))))

    m = len(a)
    n = len(b)
    A_eq, b_eq = prepare(a, b)
    res = linprog(c.reshape(1, -1), A_eq=A_eq, b_eq=b_eq, bounds=(0, None), method='simplex')

    print('\nРезультат:')
    return res.x.astype(int).reshape(m, n), res.fun.astype(int)


if __name__ == '__main__':
    warnings.filterwarnings('ignore')

    a = np.array([60, 70, 20])

    b = np.array([40, 30, 30, 50])

    D = np.array([[2, 3, 5, 1],
                  [3, 4, 9, 4],
                  [2, 5, 2, 5]])

    print('\nМЕТОД СЕВЕРО-ЗАПАДНОГО УГЛА')
    x, funk = sev_zap(a, b, D)
    print(x)
    print('\nЦелевая функция: \n> ', funk)
    print("\n------------------------------------------------------------\n")

    print('МЕТОД МИНИМАЛЬНОГО ЭЛЕМЕНТА')
    x1, funk1 = min_elem(a, b, D)
    print(x1)
    print('\nЦелевая функция: \n> ', funk1)
    print("\n------------------------------------------------------------\n")

    print('МЕТОД ПОТЕНЦИАЛОВ')
    x2, funk2 = potenz(a, b, D)
    print(x2)
    print('\nЦелевая функция: \n> ', funk2)
    