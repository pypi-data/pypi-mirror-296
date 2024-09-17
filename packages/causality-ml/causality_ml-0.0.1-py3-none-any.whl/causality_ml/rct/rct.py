import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import style

style.use("fivethirtyeight")

def plot_treatments_by_group(data, outcome, treatment, context):
    """
    Note: this function expects a single "treatment" column
    that should have all the categorical treatment variables.
    This column should either be strings or nominal numbers.
    
    Example with strings:
    >>> df
            outcome           treatment
        0  0.604729        no_treatment
        1 -0.057185  received_treatment
        2  0.533553        no_treatment
        3  0.552999  received_treatment
        4  0.992704  received_treatment
    Example with nominal numbers:
    >>> df
             outcome treatment
        0   2.150041         1
        1  11.392058         0
        2 -13.991566         0
        3 -16.072526         0
        4  -7.585248         1
    """
    plt.figure(figsize=(6,8))
    sns.boxplot(y=f"{outcome}", x=f"{treatment}", data=data).set_title(f'{outcome} by {treatment} in {context}')
    plt.show()
    
def treatment_groups_to_treatment_index(data, treatment_index_name, treatment_groups, default_group):
    return data.assign(**{
         f"{treatment_index_name}": np.select(
             [data[group].astype(bool) for group in treatment_groups],
             treatment_groups,
             default=f"{default_group}"
     )})

def recover_average_treatment_effect(data, treatment):
    return (
        data
        .groupby([treatment])
        .mean()
    )
