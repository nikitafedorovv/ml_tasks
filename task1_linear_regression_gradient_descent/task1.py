from numpy.linalg import norm
from sklearn.model_selection import KFold

from task1_linear_regression_gradient_descent.utils import *


def get_speed(stepp):
    if stochastically:
        multiplier = step_stoch
    else:
        multiplier = step_no_stoch
    return multiplier / sp.sqrt(stepp)


def rmse(weights, dataframe):
    summ = 0.0

    for row in dataframe.values:
        row_with1_without_target = np.concatenate((row[:53], [1.0]))
        summ += sp.square(target(row[53]) - target(np.dot(weights, row_with1_without_target)))

    return sp.sqrt(summ / len(dataframe))


def r2(weights, dataframe):
    sum1 = 0.0
    sum2 = 0.0

    for row in dataframe.values:
        row_with1_without_target = np.concatenate((row[:53], [1.0]))
        sum1 += sp.square(row[53] - np.dot(weights, row_with1_without_target))

    mean = sp.mean(list(dataframe[df_columns_list[53]]))

    for row in dataframe.values:
        sum2 += sp.square(row[53] - mean)

    return 1 - sum1 / sum2


def zero_values_vector(size):
    return np.array([0.0] * size)


def count_gradient(weights, df_train):
    summ = zero_values_vector(len(df_train.columns))

    for row in df_train.values:
        yi = row[53]
        xi = np.concatenate((row[:53], [1.0]))

        summ += (yi - np.dot(weights, xi)) * xi

    return (-2) * summ / len(df_train)


def update_weight_gradient(weights, stepp, df_train):
    return weights - get_speed(stepp) * count_gradient(weights, df_train)


def update_weight_stochastically(weights, stepp, df_train):
    row = df_train.sample(n=1).values[0]
    xi = np.concatenate((row[:53], [1.0]))
    yi = row[53]

    errr = yi - np.dot(weights, xi)
    lambdaa = get_speed(stepp)

    return (weights + 2 * lambdaa * errr * xi), errr


results = []


def print_and_remember_result(weights, df_test, df_train, step_when_finished):
    r2_test = r2(weights, df_test)
    r2_train = r2(weights, df_train)
    rmse_test = rmse(weights, df_test)
    rmse_train = rmse(weights, df_train)

    print("FINISHED ON STEP %s" % step_when_finished)
    print("  R2_TEST  = %s" % r2_test)
    print("  R2_TRAIN = %s" % r2_train)
    print("RMSE_TEST  = %s" % rmse_test)
    print("RMSE_TRAIN = %s" % rmse_train)

    results.append([r2_test, r2_train, rmse_test, rmse_train] + list(weights))


def go(df):
    weights = zero_values_vector(len(df.columns))
    count_weights = 0

    print("DATAFRAME SIZE = %s" % len(df))
    kfold_indexes = KFold(n_splits=5, random_state=None, shuffle=True).split(df)

    number_of_round = 0

    for train_indexes, test_indexes in kfold_indexes:
        number_of_round += 1

        train_df = df.iloc[train_indexes]
        test_df = df.iloc[test_indexes]

        print("\nROUND %s" % number_of_round)

        w = zero_values_vector(len(train_df.columns))
        step = 0
        current_norm = 100000

        while True:
            step += 1
            previous_norm = current_norm

            if stochastically:
                w, err = update_weight_stochastically(w, step, train_df)
                number_of_steps_when_log = when_to_log_stoch
                eps = eps_stoch
                current_norm = err
            else:
                w = update_weight_gradient(w, step, train_df)
                number_of_steps_when_log = when_to_log_no_stoch
                eps = eps_no_stoch
                current_norm = norm(w)

            if np.abs(previous_norm - current_norm) < eps:
                weights += w
                count_weights += 1
                print_and_remember_result(w, test_df, train_df, step)
                break

            if step % number_of_steps_when_log == 0:
                print("\nSTEP %s OF ROUND %s" % (step, number_of_round))
                print("  R2_TEST  = %s" % r2(w, test_df))
                print("  R2_TRAIN = %s" % r2(w, train_df))
                print("RMSE_TEST  = %s" % rmse(w, test_df))
                print("RMSE_TRAIN = %s" % rmse(w, train_df))
                print(" ...")

    weights /= count_weights
    print_report_to_csv(results)

    return weights


dfr = get_normalized_df(df_path)

res_weights = go(dfr)

dfr = get_df_with_valuable_fields(dfr, res_weights, 0.05)

go(dfr)
