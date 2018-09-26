import pandas as pd
import numpy as np
import scipy as sp


def get_df(path):
    columns_list = ["Page Popularity", "Page Checkins", "Page Talking About", "Page Category",
                    "extra_0", "extra_1", "extra_2", "extra_3", "extra_4", "extra_5", "extra_6",
                    "extra_7", "extra_8", "extra_9", "extra_10", "extra_11", "extra_12", "extra_13",
                    "extra_14", "extra_15", "extra_16", "extra_17", "extra_18", "extra_19", "extra_20",
                    "extra_21", "extra_22", "extra_23", "extra_24", "CC1", "CC2", "CC3", "CC4", "CC5",
                    "Base Time", "Post Length", "Post Share Count", "Post Promotion Status", "H Local",
                    "published_weekday_0", "published_weekday_1", "published_weekday_2",
                    "published_weekday_3", "published_weekday_4", "published_weekday_5",
                    "published_weekday_6", "base_weekday_0", "base_weekday_1", "base_weekday_2",
                    "base_weekday_3", "base_weekday_4", "base_weekday_5", "base_weekday_6", "Target"]

    return pd.read_csv(path, names=columns_list)


def get_normalized_df(df):
    return ((df - df.mean()) / df.std()).fillna(value=0.0)


# def get_normalized_by_minmax(df):
#     return (df - df.min()) / (df.max() - df.min())


def count_error(w, df):
    summ = 0.0

    for row in df.values:
        row1 = np.concatenate((row, [1.0]))
        summ += sp.square(row[0] - np.dot(w, row1[1:]))

    return summ / len(df)


df = get_df('dataset/Training/Features_Variant_1.csv')

dfn = get_normalized_df(df)

zero_values_vector = np.array([0.0] * len(dfn.columns))


def count_gradient(w, df):
    summ = zero_values_vector.copy()

    for row in df.values:
        row1 = np.concatenate((row, [1.0]))
        summ += (row[0] - np.dot(w, row1[1:])) * row1[1:]

    return (-2) * summ / len(df)


differnce = 1
previous_error = 1000000000000000
w = [0.0] * len(dfn.columns)

step = 0

while True:
    step += 1

    print(step)

    w = w + (1.0 / sp.power(2, step)) * count_gradient(w, dfn)

    error = count_error(w, dfn)

    differnce = error - previous_error

    previous_error = error

    if differnce > 0:
        break


print(error, w)
