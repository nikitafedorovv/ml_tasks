import csv
from time import localtime, strftime

import numpy as np
import pandas as pd
import scipy as sp

import math

from task1_linear_regression_gradient_descent.config import *


# from scipy import optimize
# import matplotlib.pyplot as plt


# res = optimize.minimize(count_error, x0=zero_values_vector, method='Nelder-Mead')
#
# print_results(res.x)


# def drop_outliers_quantile(dframe, base_dframe, low=0.01, high=0.99):
#     quant_df = base_dframe.quantile([low, high])
#
#     res = dframe.apply(lambda x: x[(x >= quant_df.loc[low, x.name]) &
#                                    (x <= quant_df.loc[high, x.name]) &
#                                    (x.name == df_columns_list[0]) |
#                                    (x.name != df_columns_list[0])], axis=0)
#     res.dropna(inplace=True)
#
#     return res
#
#
# def drop_outliers_std(dframe, base_dframe, std_coeff=0.1):
#     base_std = base_dframe.std()
#     base_mean = base_dframe.mean()
#
#     res = dframe.apply(lambda x: x[(np.abs(x - base_mean[x.name]) <= std_coeff * base_std[x.name]) &
#                                    (x.name == df_columns_list[0]) |
#                                    (x.name != df_columns_list[0])], axis=0)
#     res.dropna(inplace=True)
#
#     return res
#
#
# def drop_outliers(dframe, base_dframe):
#     if drop_outliers_method_is_quantile:
#         filt_df = drop_outliers_quantile(dframe, base_dframe, outliers_quantile_low, outliers_quantile_high)
#     else:
#         filt_df = drop_outliers_std(dframe, base_dframe, outliers_std_coeff)
#
#     rate = 1 - len(filt_df) / len(dframe)
#
#     return filt_df, rate


def drop_outliers_1(dframe, column_index, std_coeff):
    res = dframe.apply(lambda x: x[(np.abs(x - x.mean()) <= std_coeff * x.std()) &
                                   (x.name == df_columns_list[column_index]) |
                                   (x.name != df_columns_list[column_index])], axis=0)
    res.dropna(inplace=True)

    return res


def names_by_indexes(indexes):
    names = []
    for index in indexes:
        names += [df_columns_list[index]]

    return names


log_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
               30, 31, 32, 33, 35, 36, 9, 53]

log_log_indexes = []


def get_normalized_df(path):
    df = pd.read_csv(path, names=df_columns_list)

    df = drop_outliers_1(df, 11, 20)

    df = df.apply(lambda x:
                  sp.sign(x) * sp.log(np.abs(x) + 1)
                  if x.name in names_by_indexes(log_indexes)
                  else sp.sign(x) * sp.log(sp.log(np.abs(x) + 1) + 1)
                  if x.name in names_by_indexes(log_log_indexes)
                  else x, axis=0)

    # for name in [df_columns_list[9], df_columns_list[53]]:
    #     df[[name]].plot()
    #     plt.show()

    df = df.apply(lambda x: (x - x.mean()) / x.std()
                  if x.name != df_columns_list[53]
                  else x * 1.0).fillna(value=0.0)

    # df = ((df - df.mean()) / df.std()).fillna(value=0.0)

    return df


def target(log_value):
    return np.power(math.e, log_value) - 1


def e(values):
    return np.mean(values)


def std(values):
    return np.std(values)


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
                values.append(results[j][i])

            res_writer.writerow([row_names[i]] + values + [e(values)] + [std(values)])


def get_df_with_valuable_fields(dframe, weights, edge=0.01):
    valuable_names = [df_columns_list[53]]
    for i in range(len(weights) - 1):
        weight = weights[i]
        if weight > edge:
            if i < 53:
                valuable_name = df_columns_list[i]
            else:
                valuable_name = 'CONST_B'
            valuable_names += [valuable_name]

    dframe = dframe.apply(lambda x: 1 * x if x.name in valuable_names else x * 0, axis=0)

    print(dframe)

    return dframe
