#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Dictionary of performance metrics. Any of these metrics can be used
    in Experiment.

    RMSE - Root Mean Squared Error
    NMSE - Normalized Mean Squared Error (see function for definition)
    Accuracy - Classification Accuracy
    Accuracy_per_class - Classification Accuracy per class

Created on Mon Oct 23 14:42:35 2017

@author: widemann1
"""
import matplotlib.pyplot as plt

import numpy as np
import sklearn
from sklearn import metrics
# from lifelines.utils import concordance_index

from sklearn.metrics import average_precision_score, roc_curve, auc, confusion_matrix
from sklearn.metrics import accuracy_score, recall_score, precision_score


def area_under_curve(y_pred, y_true, **kwargs):
    y_true = y_true.ravel()
    y_pred = y_pred.ravel()
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    return auc(fpr, tpr)


def area_under_curve_uncensored(y_pred, y_true, **kwargs):
    y_true = y_true.ravel()
    y_pred = y_pred.ravel()
    censor_flag = kwargs['censor_flag'].astype(np.int8).ravel()  # censor flag
    # ignore all censored cases
    y_true = y_true[censor_flag.astype(bool)].copy()
    y_pred = y_pred[censor_flag.astype(bool)].copy()
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    return auc(fpr, tpr)


def avg_precision_uncensored(y_pred, y_true, **kwargs):
    y_true = y_true.ravel().astype(int)
    y_pred = y_pred.ravel()
    censor_flag = kwargs['censor_flag'].astype(int).ravel()  # censor flag
    # print(len(y_true))
    # print(censor_flag[(censor_flag == 0) & (y_true == 1)].shape)  # 0: censored and output 1
    # print(censor_flag[(censor_flag == 1) & (y_true == 1)].shape)  # 1: uncensored and output 1
    # print(censor_flag[(censor_flag == 0)].shape)
    # print(censor_flag[(censor_flag == 1)].shape)
    # print(y_pred)

    # print('uncensored + censored: ')
    # print('perc of y_true == 1: {}'.format(y_true.sum() / len(y_true)))
    # print('perc of y_pred == 1: {}'.format(y_pred.sum() / len(y_pred)))
    # print('perc uncensored == {}'.format(censor_flag.sum() / len(censor_flag)))
    # print('-' * 10)
    # print('Only uncensored: ')
    y_true = y_true[censor_flag.astype(bool)].copy()
    y_pred = y_pred[censor_flag.astype(bool)].copy()
    # print(y_true.shape)
    # print(y_pred.shape)
    # print('perc of y_true == 1: {}'.format(y_true.sum() / len(y_true)))
    # print('perc of y_true == 0: {}'.format((1 - y_true).sum() / len(y_true)))
    # print('perc of y_pred == 1: {}'.format(y_pred.sum() / len(y_pred)))
    # print('perc uncensored {}'.format(censor_flag.sum() / len(censor_flag)))

    # print('+' * 20)
    # print(y_true)
    # print(y_pred.astype(int))

    # print(confusion_matrix(y_true, y_pred.astype(int)))
    return average_precision_score(y_true, y_pred, pos_label=1)
    # return average_precision


def avg_precision(y_pred, y_true, **kwargs):
    y_true = y_true.ravel()
    y_pred = y_pred.ravel()
    return average_precision_score(y_true, y_pred, pos_label=1)


def recall(y_pred, y_true, **kwargs):
    y_true = y_true.ravel().astype(int)
    y_pred = y_pred.ravel().astype(int)
    return recall_score(y_true, y_pred)


def precision(y_pred, y_true, **kwargs):
    y_true = y_true.ravel().astype(int)
    y_pred = y_pred.ravel().astype(int)
    return precision_score(y_true, y_pred)


def rmse(y_pred, y_true, **kwargs):
    """ Compute Root Mean Squared Error."""
    # prepare input data to make sure they have the same dimension
    y_pred = y_pred.ravel()
    y_true = y_true.ravel()
    return np.sqrt(((y_pred - y_true)**2).mean())


def nmse(y_pred, y_true, **kwargs):
    """ Compute Normalized-MSE.
    The normalized mean squared error (NMSE), which is defined as the
    MSE divided by the variance of the ground truth.
    See paper: https://arxiv.org/pdf/1206.4601.pdf
    """
    # prepare input data to make sure they have the same dimension
    y_pred = y_pred.ravel()
    y_true = y_true.ravel()
    return ((y_pred - y_true)**2).mean() / np.var(y_true)


def accuracy(y_pred, y_true, **kwargs):
    """ Compute classification accuracy. """
    # prepare input data to make sure they have the same dimension
    y_pred = y_pred.ravel()
    y_true = y_true.ravel()
    return np.average(np.around(y_pred) == y_true)


def accuracy_per_class(y_pred, y_true, **kwargs):
    """ Compute classification accuracy per class. """
    # prepare input data to make sure they have the same dimension
    y_pred = y_pred.ravel()
    y_true = y_true.ravel()
    set_y = set(y_true)  # this should sort too - unique classes
    y_pred = np.round(y_pred).astype(int)  # just to make sure it's int
    out = []
    # for each class compute accuracy
    for c in set_y:
        inds = np.where(y_true == c)
        acc = accuracy(y_pred[inds], y_true[inds])
        out.append((c, acc))
    return out


def rmse_survival(y_pred, y_true, **kwargs):
    """ Compute Root Mean Squared Error."""
    # prepare input data to make sure they have the same dimension
    y_pred = y_pred.ravel()
    y_true = y_true.ravel()
    d = np.array(kwargs['censor_flag'].astype(np.int8).ravel())  # censor flag
    # return np.sqrt( (((d == 1).astype(float)*(y_pred-y_true)**2)).mean()  )
    return np.sqrt(((y_pred[d == 1] - y_true[d == 1])**2).mean())


def mse_survival(y_pred, y_true, **kwargs):
    """ Compute MSE. """
    # prepare input data to make sure they have the same dimension
    y_pred = y_pred.ravel()
    y_true = y_true.ravel()
    d = np.array(kwargs['censor_flag'].astype(np.int8).ravel())  # censor flag
    # return ((d == 1).astype(float)*(y_pred-y_true)**2).mean()
    return ((y_pred[d == 1] - y_true[d == 1])**2).mean()


# def c_index(y_pred, y_true, **kwargs):
#    """  Compute a concordance-index using lifelines library.
#        It is faster than our previous code, as it uses clever data
#        structures like B-tree to fasten the access to the data.
#    """
#    y_pred = y_pred.ravel()
#    y_true = y_true.ravel()
#    censor_flag = kwargs['censor_flag'].astype(np.int8).ravel()
#    return concordance_index(y_true, y_pred, event_observed=censor_flag)


def c_index_ours(y_pred, y_true, **kwargs):
    """  Compute a concordance-index.
    The c-index is a measure of accuracy similar to the area under the
    ROC (AUC). It is computed by assessing relative risks (orderings of
    survival times across patients) where comparisons are restricted based
    on censoring. See paper http://dmkd.cs.vt.edu/papers/CSUR17.pdf for details

    " It can be interpreted as the fraction of all pairs of
      subjects whose predicted survival times are correctly ordered
      among all subjects that can actually be ordered."
      This quote is from https://papers.nips.cc/paper/3375-on-ranking-in-survival-analysis-bounds-on-the-concordance-index.pdf

    """
    # prepare input data to make sure they have the same dimension
    d = np.array(kwargs['censor_flag'].astype(np.int8).ravel())  # censor flag
    v = np.array(kwargs['survival_time'].astype(np.float32).ravel())  # survival time

    numerator_denominator = np.sum([np.sum([[float(yi_pred < yj_pred), 1.] for yj_pred in y_pred[v > vi]], axis=0) for vi, yi_pred, yi_true in zip(v[d == 1], y_pred[d == 1], y_true[d == 1])], axis=0)
    C = numerator_denominator[0] / numerator_denominator[1]

    return C


def brier_score(y_pred, y_true, **kwargs):
    d = np.array(kwargs['censor_flag'].astype(np.int8).ravel())  # censor flag
    v = np.array(kwargs['survival_time'].astype(np.float32).ravel())  # survival

    w = inverse_probability_of_censoring_weights(v, d)
    mask = (w > 0)
    w[mask] = w[mask] / w[mask].sum()
    bscore = sklearn.metrics.brier_score_loss(y_true, y_pred,
                                              sample_weight=w)

    return bscore


def mae_survival(y_pred, y_true, **kwargs):
    """ Compute Mean Absolute Error for uncensored data. """
    # prepare input data to make sure they have the same dimension
    y_pred = y_pred.ravel()
    y_true = y_true.ravel()
    d = np.array(kwargs['censor_flag'].astype(np.int8).ravel())  # censor flag
    # return ((d == 1).astype(float) * np.abs(y_pred-y_true)).mean()
    return (np.abs(y_pred[d == 1] - y_true[d == 1])).mean()


def weighted_accuracy(y_pred, y_true, **kwargs):
    """ Compute classification accuracy. """
    # prepare input data to make sure they have the same dimension
    d = np.array(kwargs['censor_flag'].astype(np.int8).ravel())  # censor flag
    v = np.array(kwargs['survival_time'].astype(np.float32).ravel())  # srvival

    w = inverse_probability_of_censoring_weights(v, d)
    # w == 1
    mask = (w > 0)
    w[mask] = w[mask] / w[mask].sum()

    y_pred = np.around(y_pred.ravel()).astype(int)
    y_true = y_true.ravel().astype(int)

    return accuracy_score(y_true, y_pred, normalize=True, sample_weight=w)
    # return np.average(np.around(y_pred) == y_true, weights=w)
