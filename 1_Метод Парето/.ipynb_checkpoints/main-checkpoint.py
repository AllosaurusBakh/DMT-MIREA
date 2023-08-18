import numpy as np
import csv
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt


file = "/Users/sheeesh/Documents/Главное/Учёба/2 курс 4 семестр/ТПР/ДЗ/Таблица.csv"
dataset = pd.read_csv(file, delimiter=',')


if __name__ == '__main__':
    print(dataset)
