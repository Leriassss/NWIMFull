from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model

from sklearn.model_selection import GridSearchCV
from backend.ptq.PTQ import PTQ
from backend.criteria.Criteria import Criteria
import pandas as pd
import numpy as np

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

    def knn(self, models_results : SimulationModel):
        n = 35
        best_calibration_results, best_validation_results = self._prepare_data(models_results)

        
        param_grid = {
            'n_neighbors': range(1, n),  
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan', 'minkowski']
        }

        knn = KNeighborsRegressor()
        grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
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

    def svm(self, models_results):
        best_calibration_results, best_validation_results = self._prepare_data(models_results)

        svr = SVR()
        svr.fit(best_calibration_results, self.calage.q)

        q_sim_cal = np.maximum(0, svr.predict(best_calibration_results))
        q_sim_val = np.maximum(0, svr.predict(best_validation_results))

        metrics_cal = RegressionMetric(np.array(self.calage.q), np.array(q_sim_cal)).get_metrics_by_list_names(self.Metrics)
        metrics_val = RegressionMetric(np.array(self.validation.q), np.array(q_sim_val)).get_metrics_by_list_names(self.Metrics)

        return SimulationModel(q_sim_cal, q_sim_val, [svr.kernel, svr.C, svr.epsilon], metrics_cal, metrics_val), [metrics_cal, metrics_val]

    def random_forest(self, models_results):
        best_calibration_results, best_validation_results = self._prepare_data(models_results)

        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2],
            'bootstrap': [True, False]
        }

        grid_search = GridSearchCV(RandomForestRegressor(), param_grid=param_grid, cv=5)
        grid_search.fit(best_calibration_results, self.calage.q)

        best_rf = grid_search.best_estimator_

        q_sim_cal = np.maximum(0, best_rf.predict(best_calibration_results))
        q_sim_val = np.maximum(0, best_rf.predict(best_validation_results))

        metrics_cal = RegressionMetric(np.array(self.calage.q), np.array(q_sim_cal)).get_metrics_by_list_names(self.Metrics)
        metrics_val = RegressionMetric(np.array(self.validation.q), np.array(q_sim_val)).get_metrics_by_list_names(self.Metrics)

        return SimulationModel(q_sim_cal, q_sim_val, grid_search.best_params_, metrics_cal, metrics_val), [metrics_cal, metrics_val]

    def methods(self):
        return {
        "knn" : self.knn,
        "linreg" : self.linreg,
        "svm": self.svm,
        "random_forest": self.random_forest

    }
    @staticmethod
    def methodsList():
        return [
        "knn",
        "linreg",
        "svm",
        "random_forest"
    ]
