import csv
import math
from time import localtime, strftime

import numpy as np
import pandas as pd
from scipy import mean
from scipy import std

from task1_linear_regression_gradient_descent.config import *


# import matplotlib.pyplot as plt


def zero_values_vector(size):
    return np.matrix([0.0] * size).T


def drop_outliers_quantile(dframe, base_dframe, low=0.01, high=0.99):
    quant_df = base_dframe.quantile([low, high])

    res = dframe.apply(lambda x: x[(x >= quant_df.loc[low, x.name]) &
                                   (x <= quant_df.loc[high, x.name]) &
                                   (x.name == df_columns_list[0]) |
                                   (x.name != df_columns_list[0])], axis=0)
    res.dropna(inplace=True)

    return res


def drop_outliers_std(dframe, base_dframe, std_coeff=1):
    base_std = base_dframe.std()
    base_mean = base_dframe.mean()

    res = dframe.apply(lambda x: x[(np.abs(x - base_mean[x.name]) <= std_coeff * base_std[x.name]) &
                                   (x.name == df_columns_list[0]) |
                                   (x.name != df_columns_list[0])], axis=0)
    res.dropna(inplace=True)

    return res


def drop_outliers(dframe, base_dframe):
    if drop_outliers_method_is_quantile:
        filt_df = drop_outliers_quantile(dframe, base_dframe, outliers_quantile_low, outliers_quantile_high)
    else:
        filt_df = drop_outliers_std(dframe, base_dframe, outliers_std_coeff)

    rate = 1 - len(filt_df) / len(dframe)

    return filt_df, rate


def drop_outliers_if_necessary(train_df, test_df, df):
    if do_drop_outliers:
        train_df, train_df_outliers_rate = drop_outliers(train_df, df)

        if do_drop_outliers_from_test_df:
            test_df, test_df_outliers_rate = drop_outliers(test_df, df)
        else:
            test_df_outliers_rate = 0.0
    else:
        train_df_outliers_rate = 0.0
        test_df_outliers_rate = 0.0

    return train_df, test_df, train_df_outliers_rate, test_df_outliers_rate


def drop_outliers_from_specific_column(dframe, column_name, border):
    res = dframe.apply(lambda x: x[(x < border) &
                                   (x.name == column_name) |
                                   (x.name != column_name)], axis=0)

    res.dropna(inplace=True)

    return res


def names_by_indexes(indexes):
    names = []
    for index in indexes:
        names += [df_columns_list[index]]

    return names


def get_normalized_df(path):
    df = pd.read_csv(path, names=df_columns_list)

    # df = drop_outliers_from_specific_column(df, 'Page Popularity', 1 * 1e8)
    # df = drop_outliers_from_specific_column(df, 'CC2', 1700)
    # df = drop_outliers_from_specific_column(df, 'Target', 1200)
    # # df = drop_outliers_from_specific_column(df, 'target', 1000)
    # df = drop_outliers_from_specific_column(df, 'Page Talking About', 2000000)
    # df = drop_outliers_from_specific_column(df, 'extra_0', 1000)
    # df = drop_outliers_from_specific_column(df, 'extra_2', 1500)
    # df = drop_outliers_from_specific_column(df, 'extra_3', 1500)
    # df = drop_outliers_from_specific_column(df, 'extra_5', 250)
    # df = drop_outliers_from_specific_column(df, 'extra_7', 600)  # 750
    # df = drop_outliers_from_specific_column(df, 'extra_8', 500)  # 750
    # # df = drop_outliers_from_specific_column(df, 'extra_10', 10) ? # 10# 100
    # df = drop_outliers_from_specific_column(df, 'extra_15', 750)
    # df = drop_outliers_from_specific_column(df, 'extra_17', 1250)
    # df = drop_outliers_from_specific_column(df, 'extra_18', 1250)
    # df = drop_outliers_from_specific_column(df, 'extra_19', 600)
    # df = drop_outliers_from_specific_column(df, 'extra_20', 250)
    # df = drop_outliers_from_specific_column(df, 'extra_22', 250)  # 1000
    # df = drop_outliers_from_specific_column(df, 'extra_23', 250)  # 1000
    # df = drop_outliers_from_specific_column(df, 'extra_24', 250)
    # df = drop_outliers_from_specific_column(df, 'Post Length', 10000)
    # df = drop_outliers_from_specific_column(df, 'Post Share Count', 40000)

    # df = df.apply(lambda x: x[(x['target'] < 300) | (x['Post Length'] < 3000)], axis=1)

    # for name in df_columns_list:
    #     if name != 'target':
    #         df.plot(x='target', y=name, marker='.', linestyle='')
    #         plt.show()

    df = df.apply(lambda x: (x - x.mean()) / x.std()
    if x.name not in ['target']
    else x * 1.0, axis=0).fillna(value=0.0)

    df['constant_b'] = zero_values_vector(len(df)) + 1

    return df


def unlog(log_value):
    return np.power(math.e, log_value) - 1


def first_row(t_size):
    res = ['']
    for i in range(1, t_size + 1):
        res.append('T%s' % i)

    return res + ['E'] + ['STD']


def names_of_rows():
    return ['R2_TEST'] + ['R2_TRAIN'] + ['RMSE_TEST'] + ['RMSE_TRAIN'] + df_columns_list[:53] + ['CONST_B']


def print_report_to_csv(results):
    if stochastically:
        stoch_name = 'stoch_'
    else:
        stoch_name = ''
    filename = "reports/report_%s%s.csv" % (stoch_name, strftime("%Y-%m-%d_%H.%M.%S", localtime()))
    num_of_chunks = len(results)
    num_of_result_rows = len(results[0])
    row_names = names_of_rows()

    with open(filename, 'w', newline='') as csvfile:
        res_writer = csv.writer(csvfile)

        res_writer.writerow(first_row(num_of_chunks))

        for i in range(num_of_result_rows):
            values = []

            for j in range(num_of_chunks):
                values.append(float(results[j][i]))

            res_writer.writerow([row_names[i]] + values + [mean(values)] + [std(values)])
