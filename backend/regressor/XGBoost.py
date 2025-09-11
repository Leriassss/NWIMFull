
import numpy as np
from backend.regressor.MachineLearning import MachineLearning
from backend.regressor.Regressor import Regressor
from backend.regressor.models.XGBoostModel import XGBoostModel
from backend.simulation.models.SimulationModel import SimulationModel
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV

class XGBoost(MachineLearning):
    def __init__(self,regressor : Regressor, models_results : SimulationModel):
        self.regressor = regressor
        self.best_calibration_results, self.best_validation_results = self.regressor._prepare_data(models_results)
        
    def tuning(self)  -> SimulationModel:
        
        parameters_grid ={
            'max_depth': list(range(1,10)),
            'learning_rate': [0.1, 0.2, 0.3, 0.4],
            'n_estimators': list(range(1,200)),
            'gamma': list(range(0,200)),
            'lambda': [0, 0.01, 0.05, 0.1, 0.5, 1]
        }

        grid_search = RandomizedSearchCV(xgb.XGBRegressor(), parameters_grid, n_iter = 500, cv=5, scoring="neg_mean_absolute_error", n_jobs=-1, random_state = 123)
    
        grid_search.fit(self.best_calibration_results, self.regressor.calage)

        best_rr = grid_search.best_estimator_

        return self.regressor.fitting(np.maximum(0, best_rr.predict(self.best_calibration_results)),
                                      np.maximum(0, best_rr.predict(self.best_validation_results)),
                                      grid_search.best_params_)

    def run(self, xgbModel : XGBoostModel) -> SimulationModel:
        params = xgbModel.to_dict()
        ridge_reg = xgb.XGBRegressor(**params)
        ridge_reg.fit(self.best_calibration_results, self.regressor.calage)

        return self.regressor.fitting(np.maximum(0, ridge_reg.predict(self.best_calibration_results)),
                                      np.maximum(0, ridge_reg.predict(self.best_validation_results)),
                                      params)


