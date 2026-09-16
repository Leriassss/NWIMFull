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
    Metrics = ["NSE", "KGE", "RMSE", "MAE", "MAPE"]
    def __init__(self, ptq_calage: PTQ, ptq_validation: PTQ):
        self.q_cal = ptq_calage.q
        self.q_val = ptq_validation.q
        self.calage = ptq_calage.q.dropna()
        self.validation = ptq_validation.q.dropna()

        

    def _prepare_data(self, models_results):
        best_calibration_results = [pd.Series(sim.calibration_sim) for sim in models_results]
        best_validation_results = [pd.Series(sim.validation_sim) for sim in models_results]

        best_calibration_results = pd.concat(best_calibration_results, axis=1)
        best_validation_results = pd.concat(best_validation_results, axis=1)
        best_calibration_results[len(best_calibration_results.columns)] = self.q_cal
        best_validation_results[len(best_validation_results.columns)] = self.q_val

        best_calibration_results = best_calibration_results.dropna().drop(best_calibration_results.columns[-1],axis =1)
        best_validation_results = best_validation_results.dropna().drop(best_validation_results.columns[-1],axis =1)
        return best_calibration_results, best_validation_results

    @staticmethod
    def custom_scoring(y_true, y_pred):
        metric = RegressionMetric(np.array(y_true), np.array(y_pred)).get_metrics_by_list_names(["NSE"])["NSE"]
        return float(metric)

    def fitting(self, q_sim_calage, q_sim_validation, params):

        nse_knn_calage = RegressionMetric(1e-10+np.array(self.calage),1e-10+np.array(q_sim_calage)).get_metrics_by_list_names(self.Metrics)

        nse_knn_validation = RegressionMetric(1e-10+np.array(self.validation),1e-10+np.array(q_sim_validation)).get_metrics_by_list_names(self.Metrics)
        cal = pd.Series([np.nan]*len(self.q_cal))
        cal[np.isnan(self.q_cal)== False] = q_sim_calage

        val = pd.Series([np.nan]*len(self.q_val))
        val[np.isnan(self.q_val)== False] = q_sim_validation
        #print(len(q_sim_calage), len(self.q_cal))
        return SimulationModel(cal, val, params, nse_knn_calage, nse_knn_validation), [nse_knn_calage, nse_knn_validation]
        
