from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import make_scorer

from backend.ptq.PTQ import PTQ
import pandas as pd
import numpy as np
#import xgboost as xgb

from backend.simulation.models.SimulationModel import SimulationModel
from permetrics.regression import RegressionMetric
class Regressor:
    Metrics = ["NSE", "KGE", "RMSE", "MAE", "MAPE", "R2"]
    def __init__(self, ptq_calage: PTQ, ptq_validation: PTQ):
        self.calage = ptq_calage
        self.validation = ptq_validation
        

    def _prepare_data(self, models_results):
        best_calibration_results = [pd.Series(sim.calibration_sim) for sim in models_results]
        best_validation_results = [pd.Series(sim.validation_sim) for sim in models_results]

        best_calibration_results = pd.concat(best_calibration_results, axis=1)
        best_validation_results = pd.concat(best_validation_results, axis=1)

        return best_calibration_results, best_validation_results

    @staticmethod
    def custom_scoring(y_true, y_pred):
        metric = RegressionMetric(np.array(y_true), np.array(y_pred)).get_metrics_by_list_names(["NSE"])["NSE"]
        return float(metric)

    def fitting(self, q_sim_calage, q_sim_validation, params):

        nse_knn_calage = RegressionMetric(1e-10+np.array(self.calage.q),1e-10+np.array(q_sim_calage)).get_metrics_by_list_names(self.Metrics)

        nse_knn_validation = RegressionMetric(1e-10+np.array(self.validation.q),1e-10+np.array(q_sim_validation)).get_metrics_by_list_names(self.Metrics)

        return SimulationModel(q_sim_calage, q_sim_validation, params, nse_knn_calage, nse_knn_validation), [nse_knn_calage, nse_knn_validation]
        

    def knn(self, models_results : SimulationModel):
        n = 100
        best_calibration_results, best_validation_results = self._prepare_data(models_results)

        
        param_grid = {
            'n_neighbors': range(1, n),  
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan', 'minkowski']
        }

        knn = KNeighborsRegressor()
        grid_search = GridSearchCV(knn, param_grid, cv=5, scoring="neg_root_mean_squared_error", n_jobs=-1)
        #grid_search = GridSearchCV(knn, param_grid, cv=5, scoring=make_scorer(Regressor.custom_scoring, greater_is_better = False), n_jobs=-1)
        grid_search.fit(best_calibration_results, self.calage.q)

        best_knn = grid_search.best_estimator_
        q_sim_knn_calage = np.maximum(0, best_knn.predict(best_calibration_results))
        q_sim_knn_validation = np.maximum(0, best_knn.predict(best_validation_results))

        nse_knn_calage = RegressionMetric(np.array(self.calage.q),np.array(q_sim_knn_calage)).get_metrics_by_list_names(self.Metrics)

        nse_knn_validation = RegressionMetric(np.array(self.validation.q),np.array(q_sim_knn_validation)).get_metrics_by_list_names(self.Metrics)

        return SimulationModel(q_sim_knn_calage, q_sim_knn_validation, grid_search.best_params_, None, None), [nse_knn_calage, nse_knn_validation]

    def linreg(self, models_results):
        best_calibration_results, best_validation_results = self._prepare_data(models_results)

        linreg = linear_model.LinearRegression()
        linreg.fit(best_calibration_results, self.calage.q)

        q_sim_lin_calage = np.maximum(0, linreg.predict(best_calibration_results))
        q_sim_lin_validation = np.maximum(0, linreg.predict(best_validation_results))

        nse_lin_calage = RegressionMetric(np.array(self.calage.q),np.array(q_sim_lin_calage)).get_metrics_by_list_names(self.Metrics)

        nse_lin_validation = RegressionMetric(np.array(self.validation.q),np.array(q_sim_lin_validation)).get_metrics_by_list_names(self.Metrics)

        return SimulationModel(q_sim_lin_calage,q_sim_lin_validation, [linreg.coef_,linreg.intercept_] , nse_lin_calage, nse_lin_validation), [nse_lin_calage, nse_lin_validation]

    def ridgereg(self, models_results):
        best_calibration_results, best_validation_results = self._prepare_data(models_results)

        ridge_reg = linear_model.Ridge()
        param_grid = {
            "alpha" : list(range(-250,250))
        }
        grid_search = GridSearchCV(ridge_reg, param_grid, cv=5,  scoring="neg_root_mean_squared_error", n_jobs=-1)
        grid_search.fit(best_calibration_results, self.calage.q)

        ridge_reg = grid_search.best_estimator_

        q_sim_lin_calage = np.maximum(0, ridge_reg.predict(best_calibration_results))
        q_sim_lin_validation = np.maximum(0, ridge_reg.predict(best_validation_results))

        nse_lin_calage = RegressionMetric(np.array(self.calage.q),np.array(q_sim_lin_calage)).get_metrics_by_list_names(self.Metrics)

        nse_lin_validation = RegressionMetric(np.array(self.validation.q),np.array(q_sim_lin_validation)).get_metrics_by_list_names(self.Metrics)

        return SimulationModel(q_sim_lin_calage,q_sim_lin_validation, grid_search.best_params_ , nse_lin_calage, nse_lin_validation), [nse_lin_calage, nse_lin_validation]

    def svm(self, models_results):
        best_calibration_results, best_validation_results = self._prepare_data(models_results)

        svr = SVR()
        param_grid = {
            'kernel' : ('linear', 'rbf'),
            'C': list(range(1,100)),
            'gamma': [0.01, 0.05,  0.1, 0.5,  1],
            'epsilon': [0.01, 0.05, 0.1, 0.5, 1]
        }
        grid_search = RandomizedSearchCV(svr, param_grid, n_iter = 100, cv=5,  scoring="neg_root_mean_squared_error", n_jobs=-1, random_state = 123)
        grid_search.fit(best_calibration_results, self.calage.q)

        best_svr = grid_search.best_estimator_

        q_sim_cal = np.maximum(0, best_svr.predict(best_calibration_results))
        q_sim_val = np.maximum(0, best_svr.predict(best_validation_results))

        metrics_cal = RegressionMetric(np.array(self.calage.q), np.array(q_sim_cal)).get_metrics_by_list_names(self.Metrics)
        metrics_val = RegressionMetric(np.array(self.validation.q), np.array(q_sim_val)).get_metrics_by_list_names(self.Metrics)

        return SimulationModel(q_sim_cal, q_sim_val, grid_search.best_params_, metrics_cal, metrics_val), [metrics_cal, metrics_val]

    def random_forest(self, models_results):
        best_calibration_results, best_validation_results = self._prepare_data(models_results)

        param_grid = {
            'n_estimators': list(range(1,200)),
            'max_depth': list(range(1,100)),
            'min_samples_split': list(range(2,10)),
        }

        grid_search = RandomizedSearchCV(RandomForestRegressor(), param_grid, n_iter = 250, cv=5, scoring="neg_root_mean_squared_error", n_jobs=-1, random_state = 123)
        grid_search.fit(best_calibration_results, self.calage.q)

        best_rf = grid_search.best_estimator_

        q_sim_cal = np.maximum(0, best_rf.predict(best_calibration_results))
        q_sim_val = np.maximum(0, best_rf.predict(best_validation_results))

        metrics_cal = RegressionMetric(np.array(self.calage.q), np.array(q_sim_cal)).get_metrics_by_list_names(self.Metrics)
        metrics_val = RegressionMetric(np.array(self.validation.q), np.array(q_sim_val)).get_metrics_by_list_names(self.Metrics)

        return SimulationModel(q_sim_cal, q_sim_val, grid_search.best_params_, metrics_cal, metrics_val), [metrics_cal, metrics_val]

    def xgboost_model(self, models_results):
        best_calibration_results, best_validation_results = self._prepare_data(models_results)
        parameters_grid ={
            'max_depth': list(range(1,10)),
            'learning_rate': [0.1, 0.2, 0.3, 0.4],
            'n_estimators': list(range(1,200)),
            'gamma': list(range(0,200)),
            'lambda': [0, 0.01, 0.05, 0.1, 0.5, 1]
        }

        xgboost = xgb.XGBRegressor()

        grid_search = RandomizedSearchCV(xgboost, parameters_grid, n_iter = 500, cv=5, scoring="neg_mean_absolute_error", n_jobs=-1, random_state = 123)
        grid_search.fit(best_calibration_results, self.calage.q)
        best_xgb = grid_search.best_estimator_

        q_sim_cal = np.maximum(0, best_xgb.predict(best_calibration_results))
        q_sim_val = np.maximum(0, best_xgb.predict(best_validation_results))

        metrics_cal = RegressionMetric(np.array(self.calage.q), np.array(q_sim_cal)).get_metrics_by_list_names(self.Metrics)
        metrics_val = RegressionMetric(np.array(self.validation.q), np.array(q_sim_val)).get_metrics_by_list_names(self.Metrics)

        return SimulationModel(q_sim_cal, q_sim_val, grid_search.best_params_, metrics_cal, metrics_val), [metrics_cal, metrics_val]


    def methods(self):
        return {
            "knn" : KNeighborsRegressor,
            "ridge": self.ridgereg,
            "svm": SVR,
            "random_forest": RandomForestRegressor,
            "xgboost" : self.xgboost_model
        }

    @staticmethod
    def methodsList():
        return [
        "knn",
        "ridge",
        "svm",
        "random_forest",
        "xgboost"
    ]
