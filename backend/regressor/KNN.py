
import numpy as np
import pandas as pd


from backend.regressor.MachineLearning import MachineLearning
from backend.regressor.Regressor import Regressor
from backend.regressor.models.KNNModel import KNNModel
from backend.simulation.models.SimulationModel import SimulationModel
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV

class KNN(MachineLearning):
    def __init__(self,regressor : Regressor, models_results : SimulationModel):
        self.regressor = regressor
        self.best_calibration_results, self.best_validation_results = self.regressor._prepare_data(models_results)
        
    def tuning(self)  -> SimulationModel:

        param_grid = {
            'n_neighbors': range(1, 100),  
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan', 'minkowski']
        }

        grid_search = GridSearchCV(KNeighborsRegressor(), param_grid, cv=5, scoring="neg_root_mean_squared_error", n_jobs=-1)
        #grid_search = GridSearchCV(knn, param_grid, cv=5, scoring=make_scorer(Regressor.custom_scoring, greater_is_better = False), n_jobs=-1)
        grid_search.fit(self.best_calibration_results, self.regressor.calage)

        best_knn = grid_search.best_estimator_
        
        q_sim_knn_calage = np.maximum(0, best_knn.predict(self.best_calibration_results))
        q_sim_knn_validation = np.maximum(0, best_knn.predict(self.best_validation_results))

        return self.regressor.fitting(q_sim_knn_calage,q_sim_knn_validation,grid_search.best_params_)

    def run(self, knnModel : KNNModel) -> SimulationModel:
        knn = KNeighborsRegressor(**knnModel.to_dict())
        knn.fit(self.best_calibration_results, self.regressor.calage)

        q_sim_knn_calage = np.maximum(0, knn.predict(self.best_calibration_results))
        q_sim_knn_validation = np.maximum(0, knn.predict(self.best_validation_results))

        return self.regressor.fitting(q_sim_knn_calage,q_sim_knn_validation,knnModel.to_dict())


