from scipy.stats import (
    ks_2samp,
    ttest_ind,
    kruskal,
    f_oneway
)
import numpy as np
from sklearn.feature_selection import mutual_info_classif

class Dict2Class(object): 
    def __init__(self, my_dict): 
        for key in my_dict: 
            setattr(self, key, my_dict[key])

def ks_2sample_test(sample_one, sample_two, method :str ="auto"):
    result = ks_2samp(sample_one, sample_two, method=method)
    return Dict2Class({
        "statistic": result.statistic,
        "p_value": result.pvalue
    })

def t_test(sample_one, sample_two, equal_var=True, trim=0):
    result = ttest_ind(sample_one, sample_two, equal_var=equal_var, trim=trim)
    return Dict2Class({
        "statistic": result.statistic,
        "p_value": result.pvalue,
        "degrees_of_freed": result.df,
        "confidence_interval": result.confidence_interval
    })
    
def kruskal_test(samples : list):
    result = kruskal(samples)
    return Dict2Class({
        "statistic": result.statistic,
        "p_value": result.pvalue
    })


def f_test(samples : list):
    result = f_oneway(samples)
    return Dict2Class({
        "statistic": result.statistic,
        "p_value": result.pvalue
    })


def mutual_information(
    sample_one,
    sample_two,
    discrete_features=False,
    n_neighbors = 3
):
    sample_one = sample_one.reshape(-1, 1)
    return mutual_info_classif(
        sample_one, sample_two,
        discrete_features=discrete_features,
        n_neighbors=n_neighbors
    )
    
def mean_squared_error(sample_one : np.array, sample_two: np.array):
    return np.sum(
        np.square(sample_one - sample_two)
    )/len(sample_one)

def mean_absolute_error(sample_one : np.array, sample_two: np.array):
    return np.sum(
        np.abs(sample_one - sample_two)
    )/len(sample_one)

