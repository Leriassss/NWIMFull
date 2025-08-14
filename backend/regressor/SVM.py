
import numpy as np
from backend.regressor.MachineLearning import MachineLearning
from backend.regressor.Regressor import Regressor
from backend.regressor.models.SVMModel import SVMModel
from backend.simulation.models.SimulationModel import SimulationModel
from sklearn.svm import SVR
from sklearn.model_selection import RandomizedSearchCV

class SVM(MachineLearning):
    def __init__(self,regressor : Regressor, models_results : SimulationModel):
        self.regressor = regressor
        self.best_calibration_results, self.best_validation_results = self.regressor._prepare_data(models_results)
        
    def tuning(self)  -> SimulationModel:
        
        param_grid = {
            'kernel' : ('linear', 'rbf'),
            'C': list(range(1,100)),
            'gamma': [0.01, 0.05,  0.1, 0.5,  1],
            'epsilon': [0.01, 0.05, 0.1, 0.5, 1]
        }

        grid_search = RandomizedSearchCV(SVR(), param_grid,  n_iter = 100, cv=5,  scoring="neg_root_mean_squared_error", n_jobs=-1, random_state = 123)
    
        grid_search.fit(self.best_calibration_results, self.regressor.calage.q)

        best_rr = grid_search.best_estimator_

        return self.regressor.fitting(np.maximum(0, best_rr.predict(self.best_calibration_results)),
                                      np.maximum(0, best_rr.predict(self.best_validation_results)),
                                      grid_search.best_params_)

    def run(self, svmModel : SVMModel) -> SimulationModel:
        params = svmModel.to_dict()
        ridge_reg = SVR(**params)
        ridge_reg.fit(self.best_calibration_results, self.regressor.calage.q)

        return self.regressor.fitting(np.maximum(0, ridge_reg.predict(self.best_calibration_results)),
                                      np.maximum(0, ridge_reg.predict(self.best_validation_results)),
                                      params)


