"""
The basis for the categorical tests come from:

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4966396/
"""

# TODO: make the interfaces consistent with the Dict2Class object

import numpy as np
import pandas as pd
from scipy.stats import (
    chi2_contingency,
    barnard_exact,
    chisquare
)
from sklearn.metrics import log_loss
from statsmodels.stats.contingency_tables import (
    mcnemar,
    cochrans_q
)

class Dict2Class(object): 
      
    def __init__(self, my_dict): 
          
        for key in my_dict: 
            setattr(self, key, my_dict[key])
            
def chi_squared_test(
    df: pd.DataFrame,
    column_one: str,
    column_two: str,
    Yates_correction : bool = False
) -> object:
    """
    Pearson's Chi-Squared Test

    Assumptions:
    * Assumes two or more independent groups.

    Concerns:
    * Subject to Type 1 Error, false positives, when
    the total number of observations is small.

    When observed samples is small, use the Yates'
    correction, with Yates_correction=True
    Null Hypothesis: there is no difference between these two proportions

    Note: If you have small values and only two
    classes, it is recommended that you use Barnard's exact test
    instead.

    Note: this contingency table is 2 x 2 if there
    are two values per column and will be larger
    if either group can take on more than two values.

    Parameters
    ----------
    df : pd.DataFrame - the data to test

    column_one : str - the column containing counts
    of the first group

    column_two : str - the column containing counts
    of the second group

    Yates_correction : bool - whether to apply Yates
    correction or not.  See reference for details.

    Returns
    -------
    A class object with the following attributes:
    * chi2
    * p_value
    * degrees_of_freedom
    
    Note - degrees of freedom is used in part to approximate
    the Chi-Squared distribution, and is a distribution
    parameter.  So knowledge of it, can be helpful in
    understanding the test

    Reference: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4966396/
    """
    groupsizes = df.groupby([column_one, column_two]).size()
    contingency_table = groupsizes.unstack(column_one)
    # fillna(0) is necessary to remove any NAs which will cause exceptions
    chi2, p, dof, _ = (
        chi2_contingency(
            contingency_table.fillna(0),
            correction=Yates_correction
        )
    )
    dictionary = {
        "chi2": chi2,
        "p_value": p,
        "degrees_of_freedom": dof
    }
    return Dict2Class(dictionary)

def barnard_exact_test(
    df: pd.DataFrame,
    column_one: str,
    column_two: str,
    pooled : bool = True,
    alternative : str = "two-sided",
    n : int = 32
) -> object:
    """
    Barnard's Exact Test.

    Assumptions:
    * Assumes two independent groups.
    
    Null Hypothesis: there is no difference between these two proportions

    Note: this contingency table is 2 x 2 if there
    are two values per column and will be larger
    if either group can take on more than two values.

    Parameters
    ----------
    df : pd.DataFrame - the data to test

    column_one : str - the column containing counts
    of the first group

    column_two : str - the column containing counts
    of the second group

    pooled : bool - if the variances between the columns
    are equal, it's best to set pooled equal to true.
    If they are not, please set it to false.

    alternative : str - one of "less", "greater", "two-sided"

    Note:
    * two-sided is for equivalence
    * less means column_one < column_two
    * greater means column_one > column_two

    n : int - the number of sampling points used
    in the construction of the sampling method.
    
    See reference for details.

    Returns
    -------
    A class object with the following attributes:
    * chi2
    * p_value
    * degrees_of_freedom
    
    Reference:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.barnard_exact.html
    """
    groupsizes = df.groupby([column_one, column_two]).size()
    contingency_table = groupsizes.unstack(column_one)
    # fillna(0) is necessary to remove any NAs which will cause exceptions
    return barnard_exact(
        contingency_table.fillna(0),
        alternative=alternative,
        pooled=pooled,
        n=n
    )

def chisquare(f_obs, f_exp=None, ddof=0, axis=0):
    """
    This is just a wrapper for scipy's chisquare
    test, for now.

    Docs:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
    """
    return chisquare(
        f_obs,
        f_exp=f_exp,
        ddof=ddof,
        axis=axis
    )

def contingency_describe(
    df: pd.DataFrame,
    column_one: str,
    column_two: str,
    alternative : str = "attribute_vs_attribute"
):
    """

    Explanation of alternatives:
    * attribute_vs_attribute -
    This option assumes that your data is of the form
    attribute, compared to some other attribute.
    The classic example is:

    sex   0  1
    hand      
    0.0   1  2
    1.0   3  1

    Here sex=0 is female and sex=1 is male,
    hand=0 is left and hand=1 is right.

    So we can compare how many people in our dataset
    are (male, right-handed), (male, left-handed),
    (female, right-handed), (female, left-handed)
    by looking at the contingency table.
    In order to describe the contingency table we do
    the following:
    * conditional average
    * conditional standard deviation

    * paired_B_by_K -
    This option assumes that your data is of the form
    attribute, compared to some group or entity.
    Here the columns contain the attribute, test result,
    or quantity of measurement.  And the rows contain
    unique identifiers, signifying membership to some group,
    or identifying an individual.

    An example would be:

    medicine 0  1
    id      
    0        1  2
    1        3  1

    Here the id=0 refers to the first
    patient.  And medicine=0 means placebo
    is taken instead of the medication.
    So the combination id=0,medicine=0 with
    count 1 could mean, the number of times
    the patient complained of pain.
    We can run the same logic across the rest of
    the patients.

    Thus the conditional mean given placebo, would fix the
    state of the medicine, and vary the patient id.
    Thus the conditional mean tells us the average
    number of complaints of pain across all patients,
    given they did not take the medicine.
    
    
    Parameters
    -----------
    df : pd.DataFrame - the data to test

    column_one : str - the column containing counts
    of the first group

    column_two : str - the column containing counts
    of the second group

    alternative : str - options:
    * attribute_vs_attribute
    * paired_B_by_K

    Returns
    -------
    A dictionary of the conditional mean and standard deviation,
    for attribute_vs_attribute this occurs over each attribute axis.
    For paired_B_by_K we assume that the unique identifiers tie to
    an group or entity, therefore we only consider the conditional mean
    subject to the columns and not the rows.
    Thus we can get descriptions of inter group variation from the
    description.
    """
    groupsizes = df.groupby([column_one, column_two]).size()
    contingency_table = groupsizes.unstack(column_one)
    descriptions = {}
    matrix = contingency_table.values
    col_name = contingency_table.columns.name
    index_name = contingency_table.index.name
    
    for col in contingency_table.columns:
        descriptions[f"(name, value) conditional mean :({col_name},{col})"] = contingency_table[col].mean()
        descriptions[f"(name, value) conditional std :({col_name},{col})"] = contingency_table[col].std()
    
    if alternative == "attribute_vs_attribute":
        for index in contingency_table.T.index:
            descriptions[f"(name, value) conditional mean :({index_name},{index})"] = contingency_table.T[index].mean()
            descriptions[f"(name, value) conditional std :({index_name},{index})"] = contingency_table.T[index].std()

    return descriptions

def mcnemar_test(
    df: pd.DataFrame,
    column_one: str,
    column_two: str,
    exact : bool = True,
    correction : bool = False,
):
    """
    McNemar's chi-squared test is used for the
    difference between paired proportions.

    Note: A proportion is considered "paired" if there
    is a dependency between the samples.

    Note: McNemar's test assumes a 2x2 contingency table

    Naively a simple dependence structure implies
    at least two of the samples came from the same
    person.  So if we sample 3 people, say repeatedly,
    generating 6 samples, two from each, then the data
    is paired.  Whenever there is a unique identifier
    associated with multiple samples, we can think of
    that data as being paired.

    Note: For McNemar's test to be valid the only
    possible outcomes are positive or negative,
    sometimes depicted as 1 or 0.

    Parameters
    ---------
    df : pd.DataFrame - the data to test

    column_one : str - the column containing counts
    of the first group

    column_two : str - the column containing counts
    of the second group

    exact : bool - if exact is True, then bionomial
    distribution is used.  If False, then chi-squared
    distribution is used.
    Chi-squared should be used for large samples.

    correction : bool - if True then a continuity correction
    is used, for the chisquared distribution.
    Note: cannot be true for the binomial distribution.

    Example DataFrame:
       A  B
    0  1  1
    1  0  1
    2  1  1
    3  1  1
    4  0  0

    References:
    * https://en.wikipedia.org/wiki/McNemar%27s_test#:~:text=The%20Liddell's%20exact%20test%20is,more%20than%20two%20rows%2Fcolumns.
    * https://www.statsmodels.org/dev/generated/statsmodels.stats.contingency_tables.mcnemar.html
    """
    groupsizes = df.groupby([column_one, column_two]).size()
    contingency_table = groupsizes.unstack(column_one)
    bunch = mcnemar(
        contingency_table,
        exact=exact,
        correction=correction
    )
    dictionary = {
        "statistic": bunch.statistic,
        "p_value": bunch.pvalue
    }
    return Dict2Class(dictionary)

def cochrans_q_test(
    df: pd.DataFrame,
    column_one: str,
    column_two: str,
):
    """
    Cochran's Q test is used for the
    difference between paired proportions.
    
    It is an extension of McNemar's test beyond the
    2 x 2 contingency table, to m x n contingency tables.

    This test assumes the rows represent individuals
    that are paired and that the columns represent treatments.
    Therefore column_one

    Note: A proportion is considered "paired" if there
    is a dependency between the samples.
    
    Naively a simple dependence structure implies
    at least two of the samples came from the same
    person.  So if we sample 3 people, say repeatedly,
    generating 6 samples, two from each, then the data
    is paired.  Whenever there is a unique identifier
    associated with multiple samples, we can think of
    that data as being paired.

    Parameters
    ---------
    df : pd.DataFrame - the data to test

    column_one : str - the column containing counts
    of the first group

    column_two : str - the column containing counts
    of the second group

    Example DataFrame:
       A  B
    0  2  1
    1  0  1
    2  2  1
    3  0  1
    4  1  0

    References:
    * https://en.wikipedia.org/wiki/Cochran%27s_Q_test
    * https://www.statsmodels.org/dev/generated/statsmodels.stats.contingency_tables.cochrans_q.html
    """
    groupsizes = df.groupby([column_one, column_two]).size()
    contingency_table = groupsizes.unstack(column_one)
    bunch = cochrans_q(
        contingency_table,
    )
    dictionary = {
        "statistic": bunch.statistic,
        "p_value": bunch.pvalue
    }
    return Dict2Class(dictionary)

