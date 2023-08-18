import math
import pandas as pd
import numpy as np


def create_table():
    file = "/Users/sheeesh/Documents/Главное/Учёба/2 курс 4 семестр/ТПР/ДЗ/Таблица5.csv"
    data_set = pd.read_csv(file, delimiter=',')

    return data_set


def electro(skates, result, min_limit):
    for i in range(len(skates) - 2):
        arr = []

        for j in range(len(skates) - 2):
            P = 0
            N = 0

            if i == j:
                arr.append(0)
                continue

            if int(skates[i][1]) < int(skates[j][1]):
                P += 5
            elif int(skates[i][1]) > int(skates[j][1]):
                N += 5

            if int(skates[i][2]) > int(skates[j][2]):
                P += 4
            elif int(skates[i][2]) < int(skates[j][2]):
                N += 4

            if int(skates[i][3]) > int(skates[j][3]):
                P += 4
            elif int(skates[i][3]) < int(skates[j][3]):
                N += 4

            if int(skates[i][4]) < int(skates[j][4]):
                P += 3
            elif int(skates[i][4]) > int(skates[j][4]):
                N += 3

            if P == 0 or (P == 0 and N == 0):
                arr.append(math.inf)
            elif N == 0 or P == N:
                arr.append(0)
            else:
                D = round(P / N, 1)
                if D <= min_limit:
                    arr.append(0)
                else:
                    arr.append(D)

        result[skates[i][0]] = arr

    return result


def list_of_the_best(table):
    res = []
    matrix = np.array(table)

    for i in range(0, len(matrix)):
        arr_skate_float = list(map(float, matrix[i]))
        arr_skate_no_zero = [i for i in arr_skate_float if i != 0.0]
        elem_res = [len(arr_skate_no_zero), i + 1]
        res.append(elem_res)

    res = sorted(res, key=lambda favorite: favorite[0], reverse=True)
    print('Топ:')
    for finaly in res:
        print('   > Альтернатива', finaly[1])


if __name__ == '__main__':
    dataset = create_table()
    print('\n', dataset.to_string(), '\n')
    alternatives = dataset.values.tolist()

    data = {'Трюковой': [], 'Круизер': [], 'Лонгборд': [], 'Пластборд': [], 'Фристайл': []}
    index = ['Трюковой', 'Круизер', 'Лонгборд', 'Пластборд', 'Фристайл']
    result_table = pd.DataFrame(data)

    while 1:
        print('--ВЫБЕРИТЕ ДЕЙТСВИЕ--')
        print(' 1 - Метод Электра II')
        print(' 2 - Метод Электра II с границами')
        print(' 3 - Вывести таблицу')
        print(' 0 - Выход')
        answer = int(input('   > '))

        if answer == 1:
            limit = 1
            result_table = electro(alternatives, result_table, limit)
            result_table.index = index
            print('\nМетод Электра II:\n', result_table, '\n')
            list_of_the_best(result_table)
            print('')

        elif answer == 2:
            print(' \nВведите минимальный предел оценки (от 1 до 5):')
            limit = float(input('   > '))
            result_table = electro(alternatives, result_table, limit)
            result_table.index = index
            print('\nМетод Электра II с границами:\n', result_table, '\n')
            list_of_the_best(result_table)
            print('')

        elif answer == 3:
            print('\n', dataset.to_string(), '\n')

        else:
            break
