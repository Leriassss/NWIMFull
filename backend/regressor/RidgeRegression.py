
import numpy as np
from backend.regressor.MachineLearning import MachineLearning
from backend.regressor.Regressor import Regressor
from backend.regressor.models.RidgeRegressionModel import RidgeRegressionModel
from backend.simulation.models.SimulationModel import SimulationModel
from sklearn import linear_model
from sklearn.model_selection import GridSearchCV

class RidgeRegression(MachineLearning):
    def __init__(self,regressor : Regressor, models_results : SimulationModel):
        self.regressor = regressor
        self.best_calibration_results, self.best_validation_results = self.regressor._prepare_data(models_results)
        
    def tuning(self)  -> SimulationModel:
        
        param_grid = {
            "alpha" : list(range(0,250))
        }

        grid_search = GridSearchCV(linear_model.Ridge(), param_grid, cv=5, scoring="neg_root_mean_squared_error")
    
        grid_search.fit(self.best_calibration_results, self.regressor.calage)

        best_rr = grid_search.best_estimator_

        return self.regressor.fitting(np.maximum(0, best_rr.predict(self.best_calibration_results)),
                                      np.maximum(0, best_rr.predict(self.best_validation_results)),
                                      grid_search.best_params_)

    def run(self, ridgeRegressionModel : RidgeRegressionModel) -> SimulationModel:
        ridge_reg = linear_model.Ridge(**ridgeRegressionModel.to_dict())
        ridge_reg.fit(self.best_calibration_results, self.regressor.calage)

        return self.regressor.fitting(np.maximum(0, ridge_reg.predict(self.best_calibration_results)),
                                      np.maximum(0, ridge_reg.predict(self.best_validation_results)),
                                      ridgeRegressionModel.to_dict())


