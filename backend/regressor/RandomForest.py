
import numpy as np
from backend.regressor.MachineLearning import MachineLearning
from backend.regressor.Regressor import Regressor
from backend.regressor.models.RandomForestModel import RandomForestModel
from backend.simulation.models.SimulationModel import SimulationModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

class RandomForest(MachineLearning):
    def __init__(self,regressor : Regressor, models_results : SimulationModel):
        self.regressor = regressor
        self.best_calibration_results, self.best_validation_results = self.regressor._prepare_data(models_results)
        
    def tuning(self)  -> SimulationModel:
        
        param_grid = {
            'n_estimators': list(range(1,200)),
            'max_depth': list(range(1,100)),
            'min_samples_split': list(range(2,10)),
        }

        grid_search = RandomizedSearchCV(RandomForestRegressor(), param_grid, n_iter = 250, cv=5, scoring="neg_root_mean_squared_error", n_jobs=-1, random_state = 123)
    
        grid_search.fit(self.best_calibration_results, self.regressor.calage.q)

        best_rr = grid_search.best_estimator_

        return self.regressor.fitting(np.maximum(0, best_rr.predict(self.best_calibration_results)),
                                      np.maximum(0, best_rr.predict(self.best_validation_results)),
                                      grid_search.best_params_)

    def run(self, rfModel : RandomForestModel) -> SimulationModel:
        params = rfModel.to_dict()
        ridge_reg = RandomForestRegressor(**params)
        ridge_reg.fit(self.best_calibration_results, self.regressor.calage.q)

        return self.regressor.fitting(np.maximum(0, ridge_reg.predict(self.best_calibration_results)),
                                      np.maximum(0, ridge_reg.predict(self.best_validation_results)),
                                      params)


