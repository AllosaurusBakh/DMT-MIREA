import pandas as pd


def create_table():
    file = "/Users/sheeesh/Documents/Главное/Учёба/2 курс 4 семестр/ТПР/ДЗ/Таблица9.csv"
    data_set = pd.read_csv(file, delimiter=',')

    return data_set


def pareto_optimal(skates):
    if len(skates) == 1:
        return skates[0]

    res_1 = set()

    for i in range(len(skates)):
        for j in range(len(skates)):
            if i <= j:
                continue
            if (skates[i][1] <= skates[j][1])\
                    and (skates[i][4] <= skates[j][4])\
                    and (skates[i][2] >= skates[j][2])\
                    and (skates[i][3] >= skates[j][3]):
                res_1.add(tuple(skates[i]))

    return res_1


def limits(skates, max_price, max_size):
    res_2 = []

    for criteria in skates:
        if criteria[1] <= max_price and criteria[4] <= max_size:
            res_2.append(criteria)

    return res_2


def sub_optimization(skates, min_layers, min_durable):
    min_price = 50000
    res_3 = 0
    pre_res = []

    for criteria in skates:
        if criteria[2] >= min_layers and criteria[3] >= min_durable:
            pre_res.append(criteria)

    print('\n Предварительный результат (Субоптимизация):\n   > ', pre_res)

    for favorite in pre_res:
        if favorite[1] < min_price:
            res_3 = favorite
            min_price = favorite[1]

    return res_3


def lexico_optimization(skates):
    min_price = 70000
    max_durable = 0
    res_4 = 0
    pre_res = []

    for criteria in skates:
        if criteria[1] < min_price:
            min_price = criteria[1]

    for criteria in skates:
        if criteria[1] == min_price:
            pre_res.append(criteria)

    if len(pre_res) == 1:
        return pre_res[0]

    for favorite in pre_res:
        if favorite[3] > max_durable:
            max_durable = favorite[3]

    for favorite in pre_res:
        if favorite[3] == max_durable:
            res_4 = favorite

    return res_4


if __name__ == '__main__':
    dataset = create_table()
    print('\n', dataset.to_string(), '\n')
    alternatives = dataset.values.tolist()

    while 1:
        print('--ВЫБЕРИТЕ ДЕЙТСВИЕ--')
        print(' 1 - Метод Парето')
        print(' 2 - Границы')
        print(' 3 - Субоптимизация')
        print(' 4 - Лексикографическая оптимизация')
        print(' 5 - Вывести таблицу')
        print(' 0 - Выход')
        answer = int(input('   > '))

        if answer == 1:
            res1 = pareto_optimal(alternatives)
            print('\n Метод Парето:\n   > ', res1, '\n')

        elif answer == 2:
            print('\n Введите вверхнюю границу по стоимости (от 4000 до 15000):')
            limit_price = int(input('   > '))
            print('\n Введите вверхнюю границу по площади (от 65 до 120):')
            limit_size = int(input('   > '))
            pre_res2 = limits(alternatives, limit_price, limit_size)
            print('\n Предварительный результат (Границы):\n   > ', pre_res2)
            res2 = pareto_optimal(pre_res2)
            print('\n Границы:\n   > ', res2, '\n')

        elif answer == 3:
            print('\n Введите нижнюю границу по слоям деки (от 1 до 8):')
            limit_layers = int(input('   > '))
            print('\n Введите нижнюю границу по прочности (от 6 до 15):')
            limit_durable = int(input('   > '))
            res3 = sub_optimization(alternatives, limit_layers, limit_durable)
            print('\n Субоптимизация:\n   > ', res3, '\n')

        elif answer == 4:
            res4 = lexico_optimization(alternatives)
            print('\n Лексикографическая оптимизация (сначала по цене потом по прочности):\n   > ', res4, '\n')

        elif answer == 5:
            print('\n', dataset.to_string(), '\n')

        else:
            break
