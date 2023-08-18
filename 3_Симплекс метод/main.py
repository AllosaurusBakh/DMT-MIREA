import numpy as np


class LinearModel:

    def __init__(self, A=np.empty([0, 0]), b=np.empty([0, 0]), c=np.empty([0, 0]), minmax="MAX"):
        self.A = A
        self.b = b
        self.c = c
        self.x = [float(0)] * len(c)
        self.minmax = minmax
        self.printIter = True
        self.optimalValue = None
        self.transform = False

    def addA(self, A):
        self.A = A

    def addB(self, b):
        self.b = b

    def addC(self, c):
        self.c = c
        self.transform = False

    def setObj(self, minmax):
        self.minmax = minmax
        self.transform = False

    def setPrintIter(self, printIter):
        self.printIter = printIter

    def printSoln(self):
        print("  Коеффциенты: ")
        print(">", self.x)
        print("\n  Оптимальное значение: ")
        print(">", self.optimalValue)

    def getTableau(self):
        num_var = len(self.c)
        num_slack = len(self.A)

        t1 = np.hstack(([None], [0], self.c, [0] * num_slack))
        basis = np.array([0] * num_slack)

        for i in range(0, len(basis)):
            basis[i] = num_var + i
        A = self.A

        if not ((num_slack + num_var) == len(self.A[0])):
            B = np.identity(num_slack)
            A = np.hstack((self.A, B))

        t2 = np.hstack((np.transpose([basis]), np.transpose([self.b]), A))
        tableau = np.vstack((t1, t2))
        tableau = np.array(tableau, dtype='float')
        return tableau

    def optimize(self):
        tableau = self.getTableau()
        if self.printIter:
            print("  Стартовая таблица:")
            print_table(tableau)

        optimal = False
        iter = 0

        while 1:
            if self.printIter:
                print("\n----------------------------------\n")
                print("  Итерация :", iter - 1)
                print_table(tableau)

            for profit in tableau[0, 2:]:
                if profit > 0:
                    optimal = False
                    break
                optimal = True

            if optimal:
                break

            n = tableau[0, 2:].tolist().index(np.amax(tableau[0, 2:])) + 2
            minimum = 99999
            r = -1

            for i in range(1, len(tableau)):
                if tableau[i, n] > 0:
                    val = tableau[i, 1] / tableau[i, n]
                    if val < minimum:
                        minimum = val
                        r = i

            pivot = tableau[r, n]

            print("\n  Разрешающая колонна:", n - 1)
            print("  Разрешающая строка:", r)
            print("  Разрешающий элемент: ", pivot)

            tableau[r, 1:] = tableau[r, 1:] / pivot
            for i in range(0, len(tableau)):
                if i != r:
                    mult = tableau[i, n] / tableau[r, n]
                    tableau[i, 1:] = tableau[i, 1:] - mult * tableau[r, 1:]

            tableau[r, 0] = n - 2
            iter += 1

        if self.printIter:
            print("\n----------------------------------\n")
            print("  Финальная таблица была получена за", iter, "итерации")
            print_table(tableau)
        else:
            print("Решено")

        self.x = np.array([0] * len(c), dtype=float)
        for key in range(1, (len(tableau))):
            if tableau[key, 0] < len(c):
                self.x[int(tableau[key, 0])] = tableau[key, 1]

        self.optimalValue = -1 * tableau[0, 1]


def print_table(tableau):
    print("ind  A0\t\t ", end="")
    for i in range(1, len(c) + 1):
        print("x_" + str(i), end="\t ")
    for i in range(1, 5):
        print("b_" + str(i), end="\t ")

    print()
    for j in range(0, len(tableau)):
        for i in range(0, len(tableau[0])):
            if not np.isnan(tableau[j, i]):
                if i == 0:
                    print('x_' + str(int(tableau[j, i]) + 1), end="\t ")
                else:
                    print(round(tableau[j, i], 2), end="\t ")
            else:
                print('F', end="\t ")
        print()


if __name__ == '__main__':
    model1 = LinearModel()

    A = np.array([[0.2, 0.1],
                  [0.75, 0.2],
                  [0.15, 0.2],
                  [0.15, 0.25]])
    
    b = np.array([100, 150, 100, 150])
    
    c = np.array([1.4, 0.9])

    model1.addA(A)
    model1.addB(b)
    model1.addC(c)

    print("\n  Дано:")
    print("> A =\n", A, "\n")
    print("> А0 =\n", b, "\n")
    print("> C  =\n", c, "\n\n")
    model1.optimize()
    print("\n")
    model1.printSoln()
