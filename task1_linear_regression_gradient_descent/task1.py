import random

import scipy as sp
from numpy.linalg import norm
from scipy import matrix
from sklearn.model_selection import KFold

from task1_linear_regression_gradient_descent.utils import *


def get_speed(stepp):
    if stochastically:
        multiplier = step_stoch
    else:
        multiplier = step_no_stoch
    return multiplier / sp.sqrt(stepp)


def rmse(y_true, y_pred):
    return sp.sqrt(sp.mean(sp.square(y_true - y_pred)))


def r2(y_true, y_pred):
    mse = sp.mean(sp.square(y_true - y_pred))
    msemean = sp.mean(sp.square(y_true - sp.mean(y_true)))
    return 1 - mse / msemean


def count_gradient(y, x, w):
    return (2 / len(y)) * ((x * w - y).T * x).T


def update_weight_gradient(y, x, w, stepp):
    return w - get_speed(stepp) * count_gradient(y, x, w)


def update_weight_stochastically(y, x, w, stepp):
    pos = random.randint(0, len(y) - 1)
    xi = x[pos]
    yi = y[pos]
    errr = float(yi - xi * w)
    lambdaa = get_speed(stepp)

    return (w + 2 * lambdaa * errr * xi.T), errr


def make_a_step(y, x, w, stepp):
    if stochastically:
        weights, err = update_weight_stochastically(y, x, w, stepp)
    else:
        weights = update_weight_gradient(y, x, w, stepp)

    return weights


def print_r2_rmse(r2_test, r2_train, rmse_test, rmse_train):
    print("  R2_TEST  = %s" % r2_test)
    print("  R2_TRAIN = %s" % r2_train)
    print("RMSE_TEST  = %s" % rmse_test)
    print("RMSE_TRAIN = %s" % rmse_train)


results = []


def print_and_remember_result(y_true_test, x_test, y_true_train, x_train, w, step_when_finished):
    print("FINISHED ON STEP %s" % step_when_finished)

    r2_test = r2(y_true_test, x_test * w)
    r2_train = r2(y_true_train, x_train * w)
    rmse_test = rmse(y_true_test, x_test * w)
    rmse_train = rmse(y_true_train, x_train * w)

    print_r2_rmse(r2_test, r2_train, rmse_test, rmse_train)
    results.append([r2_test, r2_train, rmse_test, rmse_train] + list(w))


df = get_normalized_df(df_path)
# print("DATAFRAME SIZE = %s" % len(df))
kfold_indexes = KFold(n_splits=5, random_state=None, shuffle=True).split(df)

number_of_round = 0
if stochastically:
    eps = eps_stoch
    number_of_steps_when_log = when_to_log_stoch
else:
    eps = eps_no_stoch
    number_of_steps_when_log = when_to_log_no_stoch

for train_indexes, test_indexes in kfold_indexes:
    number_of_round += 1
    print("\nROUND %s" % number_of_round)

    train_df = df.iloc[train_indexes]
    test_df = df.iloc[test_indexes]

    train_df, test_df = drop_outliers_if_necessary(train_df, test_df, df)

    y_true = matrix(train_df['target']).T
    x = matrix(train_df.loc[:, train_df.columns != 'target'])
    y_true_test = matrix(test_df['target']).T
    x_test = matrix(test_df.loc[:, test_df.columns != 'target'])

    step = 0
    current_w = zero_values_vector(x.shape[1])
    previous_w = zero_values_vector(x.shape[1]) + 0.5

    while True:
        step += 1
        previous_w = current_w
        current_w = make_a_step(y_true, x, current_w, step)

        if norm(previous_w - current_w) < eps:
            print_and_remember_result(y_true_test, x_test, y_true, x, current_w, step)
            break

        if step % number_of_steps_when_log == 0:
            print("\nSTEP %s OF ROUND %s" % (step, number_of_round))
            print_r2_rmse(r2(y_true_test, x_test * current_w),
                          r2(y_true, x * current_w),
                          rmse(y_true_test, x_test * current_w),
                          rmse(y_true, x * current_w))
            print(" ...")

print_report_to_csv(results)
