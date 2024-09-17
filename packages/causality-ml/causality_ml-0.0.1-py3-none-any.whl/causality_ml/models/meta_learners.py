from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# turn this into a test later:
# fit(X, y, sample_weight=[0.1 for _ in range(10)])
# generalize to check against other kwargs on fit and predict

# predict(X, check_input=True)
class SLearner:
    def __init__(self, model, hp : dict):
        # generalize this out to handle
        # libraries that don't follow the sklearn specification
        self.model = model(**hp)

    def fit(self, X : pd.DataFrame, T: np.array, y: np.array, **kwargs):
        X = X.assign(**{"treatment": T})
        self.model.fit(X, y, **kwargs)

    def predict(self, X: pd.DataFrame, T: np.array, **kwargs):
        X = X.assign(**{"treatment": T})
        return self.model.predict(X, **kwargs)
    
    def get_cate(self, X: pd.DataFrame, T: np.array, **kwargs) -> np.array:
        """
        Return
        ------
        CATE
        """
        # Note we will probably need to generalize this out later
        X = X.assign(**{"treatment": 1}) 
        treatment_prediction = self.model.predict(X, **kwargs)
        X["treatment"] = 0
        control_prediction = self.model.predict(X, **kwargs)
        return treatment_prediction - control_prediction

class TLearner:
    def __init__(self, model, hp : dict):
        self.model_zero = model(**hp)
        self.model_one = model(**hp)

    def _assign_treat_control_outcome(self, X, T, y):
        X = X.assign(**{
            "treatment": T,
            "outcome": y
        })
        X_control = X[X["treatment"] == 0]
        outcome_control = X_control["outcome"]
        X_treat = X[X["treatment"] == 1]
        outcome_treat = X_treat["outcome"]
        X_control.drop("outcome", axis=1, inplace=True)
        X_treat.drop("outcome", axis=1, inplace=True)
        return (
            X_control,
            X_treat,
            outcome_control,
            outcome_treat
        )
        
    def _assign_treat_control(self, X, T):
        X = X.assign(**{
            "treatment": T
        })
        X_control = X[X["treatment"] == 0]
        X_treat = X[X["treatment"] == 1]
        return X_control, X_treat
        
    def fit(self, X: pd.DataFrame, T: np.array, y: np.array, **kwargs):
        (
            X_control,
            X_treat,
            outcome_control,
            outcome_treat
        ) = self._assign_treat_control_outcome(X, T, y)
        self.model_zero.fit(X_control, outcome_control, **kwargs)
        self.model_one.fit(X_treat, outcome_treat, **kwargs)

    def predict(self, X: pd.DataFrame, T: np.array, **kwargs):
        X_control, X_treat = self._assign_treat_control(X, T)
        X_control["predicted_outcome"] = self.model_zero.predict(X_control, **kwargs)
        X_treat["predicted_outcome"] = self.model_one.predict(X_treat, **kwargs)
        tmp_X = pd.concat([X_control, X_treat], sort=False).sort_index()
        return tmp_X["predicted_outcome"].values

    def get_cate(X: pd.DataFrame, T: np.array, **kwargs) -> np.array:
        return self.model_one.predict(X) - self.model_zero.predict(X)

class XLearner:
    def __init__(self, model, hp : dict, propensity_model, propensity_hp: dict):
        self.model_zero = model(**hp)
        self.model_one = model(**hp)
        self.propensity_model = propensity_model(**propensity_hp)

    def _assign_treat_control_outcome(self, X, T, y):
        X = X.assign(**{
            "treatment": T,
            "outcome": y
        })
        X_control = X[X["treatment"] == 0]
        outcome_control = X_control["outcome"]
        X_treat = X[X["treatment"] == 1]
        outcome_treat = X_treat["outcome"]
        X_control.drop("outcome", axis=1, inplace=True)
        X_treat.drop("outcome", axis=1, inplace=True)
        return (
            X_control,
            X_treat,
            outcome_control,
            outcome_treat
        )
        
    def _assign_treat_control(self, X, T):
        X = X.assign(**{
            "treatment": T
        })
        X_control = X[X["treatment"] == 0]
        X_treat = X[X["treatment"] == 1]
        return X_control, X_treat
        
    def fit(self, X: pd.DataFrame, T: np.array, y: np.array, **kwargs):
        (
            X_control,
            X_treat,
            outcome_control,
            outcome_treat
        ) = self._assign_treat_control_outcome(X, T, y)
        self.model_zero.fit(X_control, outcome_control, **kwargs)
        self.model_one.fit(X_treat, outcome_treat, **kwargs)

    def predict(self, X: pd.DataFrame, T: np.array, **kwargs):
        X_control, X_treat = self._assign_treat_control(X, T)
        X_control["predicted_outcome"] = self.model_zero.predict(X_control, **kwargs)
        X_treat["predicted_outcome"] = self.model_one.predict(X_treat, **kwargs)
        tmp_X = pd.concat([X_control, X_treat], sort=False).sort_index()
        return tmp_X["predicted_outcome"].values

    def get_cate(X: pd.DataFrame, T: np.array, **kwargs) -> np.array:
        return self.model_one.predict(X) - self.model_zero.predict(X)

def standard_error(y: pd.Series):
    return y.std() / np.sqrt(len(y))

def confidence_interval(data):
    exp_mean = data.mean()
    exp_se = standard_error(data)
    return (
        exp_mean - 2*exp_se,
        exp_mean + 2*exp_se
    )

def plot_interval(data):
    exp_mean = data.mean()
    exp_se = standard_error(data)
    x = np.linspace(
        exp_mean - 4*exp_se,
        exp_mean + 4*exp_se,
        100
    )
    y = stats.norm.pdf(x, exp_mean, exp_se)
    ci = confidence_interval(data)
    plt.plot(x, y)
    plt.vlines(ci[1], ymin=0, ymax=1)
    plt.vlines(ci[0], ymin=0, ymax=1)
    plt.legend()
    plt.show()

